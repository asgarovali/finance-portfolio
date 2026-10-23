"""Build the Excel model: Cover, Inputs, IS, BS, CF.

History (FY2021-FY2025) is written as hard-coded blue inputs from
data/processed/statements_long.csv; every subtotal is an Excel formula, so the
workbook re-proves the arithmetic. Forecast columns (FY2026E-FY2030E) are laid
out but empty until the forecast step. Inputs that wait for the Q3 2026 10-Q
are left blank and labelled.

Run from the project folder:  python -m src.model.build_excel
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

from common import excel as xl
from src.analysis.history import segments
from src.data.clean_statements import BS_ROWS, CF_ROWS, IS_ROWS

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
MODEL = ROOT / "model" / "granite_model.xlsx"

HIST = [f"FY{y}" for y in range(2021, 2026)]
FCST = [f"FY{y}" for y in range(2026, 2031)]
FIRST_COL = 2  # column B = FY2021
COL = {p: get_column_letter(FIRST_COL + i) for i, p in enumerate(HIST + FCST)}
LAST_COL = FIRST_COL + len(HIST) + len(FCST) - 1
HEADER_ROW, FIRST_ROW = 5, 7

# key totals shown in bold
BOLD_TOTALS = {"Gross profit", "Operating income", "Pre-tax income", "Net income to Granite",
               "Total assets", "Total liabilities", "Total equity", "Total liabilities and equity",
               "Cash from operations", "Cash from investing", "Cash from financing", "Net change in cash"}


def damodaran_inputs() -> dict[str, float]:
    """Betas and ERP read from the saved Damodaran files, not typed in."""
    b = pd.read_excel(RAW / "damodaran" / "betas.xls", sheet_name="Industry Averages", header=None)
    b = b.set_index(0)
    h = pd.read_excel(RAW / "damodaran" / "histimpl.xls", sheet_name=0, header=6)
    erp = h.loc[h["Year"] == 2025, "Implied ERP (FCFE)"].iloc[0]
    # column 7 = unlevered beta corrected for cash (current), 15 = average 2022-2026
    return {
        "beta_ec_avg": b.loc["Engineering/Construction", 15], "beta_ec_2026": b.loc["Engineering/Construction", 7],
        "beta_cs_avg": b.loc["Construction Supplies", 15], "beta_cs_2026": b.loc["Construction Supplies", 7],
        "erp": erp,
    }


def amortisation_history(facts: pd.DataFrame) -> dict[str, float]:
    """Intangible amortisation by year, from the latest 10-K that reports it."""
    f = facts[(facts["tag"] == "us-gaap:AmortizationOfIntangibleAssets") & (facts["dims"] == "")
              & (facts["form"] == "10-K") & facts["start"].notna()]
    f = f[f["start"].str[5:] == "01-01"].sort_values("filed").groupby("end").last()
    return {f"FY{end[:4]}": v / 1e6 for end, v in f["value"].items()}


def amortisation_schedule(facts: pd.DataFrame) -> list[float]:
    """Expected amortisation 2026-2030 as disclosed in the FY2025 10-K."""
    acc = "0000861459-26-000004"
    keys = ["NextTwelveMonths", "YearTwo", "YearThree", "YearFour", "YearFive"]
    f = facts[(facts["accession"] == acc) & (facts["end"] == "2025-12-31") & (facts["dims"] == "")]
    vals = f.set_index("tag")["value"]
    return [vals[f"us-gaap:FiniteLivedIntangibleAssetsAmortizationExpense{k}"] / 1e6 for k in keys]


def interim_h1(facts: pd.DataFrame, is_: pd.DataFrame, cf: pd.DataFrame) -> dict[str, float]:
    """Stand-ins for the inputs that wait for the Q3 10-Q, all from H1 2026 filings."""
    seg = facts[(facts["accession"] == "0000861459-26-000029")
                & (facts["tag"] == "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax")
                & (facts["dims"] == "us-gaap:StatementBusinessSegmentsAxis=gva:MaterialsMember")
                & (facts["start"] == "2026-01-01") & (facts["end"] == "2026-06-30")]
    rev = is_.loc["Revenue", "H1 2026"]
    return {
        "materials_share": seg["value"].iloc[0] / 1e6 / rev,
        "gross_margin": is_.loc["Gross profit", "H1 2026"] / rev,
        "acquisitions": -cf.loc["Acquisitions", "H1 2026"],
    }


def build_sched(wb, I: dict, is_at: dict, bs_at: dict) -> tuple:
    """Operating forecast: revenue by segment, margins, working capital, capex,
    invested capital and FCFF, plus a normalised terminal-year column.

    Financing (debt, interest, cash, NCI) is not here yet: it waits for the
    debt terms in the Q3 10-Q."""
    ws = wb.create_sheet("Sched")
    xl.setup_sheet(ws, freeze=f"B{FIRST_ROW}", col_a_width=46)
    year_header(ws, "Forecast schedules")
    term = get_column_letter(LAST_COL + 1)
    ws[f"{term}{HEADER_ROW}"] = "Terminal"
    ws[f"{term}{HEADER_ROW}"].font = xl.BOLD
    ws[f"{term}{HEADER_ROW}"].alignment = Alignment(horizontal="right")
    ws[f"{term}{HEADER_ROW}"].border = xl.THIN_BOTTOM
    ws.column_dimensions[term].width = 11
    # only FY2025A is used here (opening balances), so the older history columns are hidden
    for p_ in HIST[:-1]:
        ws.column_dimensions[COL[p_]].hidden = True

    f25 = COL["FY2025"]
    fc = [COL[p] for p in FCST]
    prev = {c: get_column_letter(FIRST_COL + len(HIST) + i - 1) for i, c in enumerate(fc)}
    at: dict[str, int] = {}
    row = FIRST_ROW

    def sec(title):
        nonlocal row
        row += 1
        xl.header(ws, row, title, LAST_COL + 1)
        row += 1

    def line(key, label, f, fmt=xl.FMT_NUM, hist=None, terminal=None, bold=False, inputs=None):
        """f(c, p) gives the formula for forecast column c (p = previous column)."""
        nonlocal row
        at[key] = row
        ws.cell(row=row, column=1, value=label).font = xl.BOLD if bold else xl.BASE
        for c in fc:
            formula = f(c, prev[c])
            if formula is None:
                continue
            if inputs:  # hard-coded counters are inputs, so they're blue
                xl.put_input(ws, f"{c}{row}", formula, fmt)
            else:
                xl.put_formula(ws, f"{c}{row}", formula, fmt, bold=bold)
        if hist:
            xl.put_formula(ws, f"{f25}{row}", hist, fmt, bold=bold)
        if terminal:
            xl.put_formula(ws, f"{term}{row}", terminal, fmt, bold=bold)
        row += 1

    t_start = {c: i for i, c in enumerate(fc)}
    g = fc[0]

    sec("Revenue")
    g27 = fc[1]
    line("t", "Years after FY2026", lambda c, p: t_start[c], "0", inputs=True)
    line("t27", "Years after FY2027", lambda c, p: None if c == g else t_start[c] - 1, "0", inputs=True)
    # FY2027E Construction revenue = latest CAP x the historical conversion of CAP into next-year revenue
    line("capg", "Construction growth implied by CAP",
         lambda c, p: f"={I['cap_now']}*{I['burn']}/({I['rev26']}*(1-{I['mshare']}))-1" if c == g27 else None,
         xl.FMT_PCT)
    line("org", "Organic growth, base path",
         lambda c, p: None if c == g else f"={c}{at['capg']}" if c == g27 else
         f"=${g27}{at['org']}+({I['gLR']}-${g27}{at['org']})*MIN({c}{at['t27']}/{I['gfade']},1)", xl.FMT_PCT)
    line("cg", "Construction growth",
         lambda c, p: None if c == g else
         f"=IF({I['scen']}=2,IF({c}{at['t']}=1,{I['down']},{p}{at['org']}),{c}{at['org']})", xl.FMT_PCT)
    line("mg", "Materials growth", lambda c, p: None if c == g else f"={c}{at['org']}", xl.FMT_PCT)
    line("crev", "Construction revenue",
         lambda c, p: f"={I['rev26']}*(1-{I['mshare']})" if c == g else f"={p}{at['crev']}*(1+{c}{at['cg']})")
    line("mrev", "Materials revenue",
         lambda c, p: f"={I['rev26']}*{I['mshare']}" if c == g else f"={p}{at['mrev']}*(1+{c}{at['mg']})")
    line("burn", "Construction revenue / CAP at prior 30 Sep",
         lambda c, p: f"={c}{at['crev']}/{I['cap_s25']}" if c == g else
         f"={c}{at['crev']}/{I['cap_now']}" if c == g27 else None, "0.000")
    line("rev", "Revenue", lambda c, p: f"={c}{at['crev']}+{c}{at['mrev']}",
         hist=f"=IS!{f25}{is_at['Revenue']}", terminal=f"={COL['FY2030']}{{r}}*(1+{I['gLR']})", bold=True)
    line("revg", "Revenue growth", lambda c, p: f"={c}{at['rev']}/{p}{at['rev']}-1", xl.FMT_PCT)

    sec("Operating profit")
    line("gm", "Gross margin",
         lambda c, p: f"={I['gm26']}" if c == g else f"=CHOOSE({I['scen']},{I['gm']},{I['gm_down']},{I['gm_up']})", xl.FMT_PCT,
         hist=f"=IS!{f25}{is_at['Gross profit']}/IS!{f25}{is_at['Revenue']}")
    line("gp", "Gross profit", lambda c, p: f"={c}{at['rev']}*{c}{at['gm']}")
    line("cogs", "Cost of revenue", lambda c, p: f"=-({c}{at['rev']}-{c}{at['gp']})")
    line("sga", "SG&A", lambda c, p: f"=-{c}{at['rev']}*{I['sga']}")
    line("oc", "Other costs, net", lambda c, p: f"={c}{at['rev']}*{I['oc']}")
    line("gain", "Gain on sale of PP&E", lambda c, p: f"={c}{at['rev']}*{I['gain']}")
    line("ebit", "Operating income",
         lambda c, p: f"={c}{at['gp']}+{c}{at['sga']}+{c}{at['oc']}+{c}{at['gain']}", bold=True)
    line("dep", "Depreciation and depletion", lambda c, p: f"={c}{at['rev']}*{I['dep']}")
    line("amort", "Intangible amortisation", lambda c, p: f"=Inputs!{c}{I['amort']}")
    line("da", "D&A", lambda c, p: f"={c}{at['dep']}+{c}{at['amort']}",
         terminal=f"={COL['FY2030']}{{r}}*(1+{I['gLR']})")
    line("ebitda", "EBITDA", lambda c, p: f"={c}{at['ebit']}+{c}{at['da']}")
    line("ebitdam", "EBITDA margin", lambda c, p: f"={c}{at['ebitda']}/{c}{at['rev']}", xl.FMT_PCT)
    line("taxop", "Tax on operating income", lambda c, p: f"=-{c}{at['ebit']}*{I['tax']}")
    line("nopat", "NOPAT", lambda c, p: f"={c}{at['ebit']}+{c}{at['taxop']}",
         terminal=f"={COL['FY2030']}{{r}}*(1+{I['gLR']})", bold=True)

    sec("Below operating income (not in FCFF; interest and NCI after Q3)")
    line("aff", "Equity income of affiliates", lambda c, p: f"={c}{at['rev']}*{I['aff']}")
    line("oth", "Other income, net", lambda c, p: f"={c}{at['rev']}*{I['oth']}")

    sec("Working capital (year-end)")
    line("costr", "Cost of revenue / revenue", lambda c, p: f"=-{c}{at['cogs']}/{c}{at['rev']}", xl.FMT_PCT)
    line("wcavg", "Trade WC % revenue at average days",
         lambda c, p: f"=({I['recd']}+{I['cad']})/365+{I['ret']}+({I['invd']}-{I['apd']})/365*{c}{at['costr']}"
                      f"-({I['cld']}+{I['accd']})/365", xl.FMT_PCT)
    # contract asset days needed in FY2030E to hit the working-capital target
    at["catgt"] = row
    ws.cell(row=row, column=1, value="Contract asset days, FY2030E target").font = xl.BASE
    xl.put_formula(ws, f"{COL['FY2030']}{row}", f"={I['cad']}+({I['nwc_target']}-{COL['FY2030']}{at['wcavg']})*365", "0.0")
    row += 1
    line("cad", "Contract asset days",
         lambda c, p: f"={I['cad']}+(${COL['FY2030']}${at['catgt']}-{I['cad']})*MIN({c}{at['t']}/{I['fade']},1)", "0.0")
    line("rec", "Receivables excl. retention", lambda c, p: f"={c}{at['rev']}*{I['recd']}/365")
    line("ret", "Retention receivable", lambda c, p: f"={c}{at['rev']}*{I['ret']}")
    line("ca", "Contract assets", lambda c, p: f"={c}{at['rev']}*{c}{at['cad']}/365")
    line("inv", "Inventories", lambda c, p: f"=-{c}{at['cogs']}*{I['invd']}/365")
    line("ap", "Accounts payable", lambda c, p: f"=-{c}{at['cogs']}*{I['apd']}/365")
    line("cl", "Contract liabilities", lambda c, p: f"={c}{at['rev']}*{I['cld']}/365")
    line("acc", "Accrued and other liabilities", lambda c, p: f"={c}{at['rev']}*{I['accd']}/365")
    bs = lambda name: f"BS!{f25}{bs_at[name]}"
    line("twc", "Trade working capital",
         lambda c, p: f"={c}{at['rec']}+{c}{at['ret']}+{c}{at['ca']}+{c}{at['inv']}-{c}{at['ap']}-{c}{at['cl']}-{c}{at['acc']}",
         hist=f"={bs('Receivables, net')}+{bs('Contract assets')}+{bs('Inventories')}-{bs('Accounts payable')}"
              f"-{bs('Contract liabilities')}-{bs('Accrued and other current liabilities')}", bold=True)
    line("twcp", "Trade working capital % revenue", lambda c, p: f"={c}{at['twc']}/{c}{at['rev']}", xl.FMT_PCT,
         hist=f"={f25}{{r_twc}}/{f25}{{r_rev}}")
    line("dwc", "Change in working capital (cash)", lambda c, p: f"=-({c}{at['twc']}-{p}{at['twc']})")

    sec("Capex and invested capital")
    line("proc", "Proceeds from sale of PP&E", lambda c, p: f"={c}{at['rev']}*{I['proc']}")
    line("nbv", "Book value of PP&E sold", lambda c, p: f"={c}{at['proc']}-{c}{at['gain']}")
    # FY2027E on: net investment (net capex + working capital) = revenue growth / sales-to-capital.
    # Working capital comes from its own schedule, so capex = depreciation + equipment sold + the rest.
    # Only depreciation is replaced: the ratio excludes acquired intangibles, which organic growth doesn't renew.
    line("capex", "Capex", lambda c, p: f"=-{I['capex26']}" if c == g else
         f"=-({c}{at['dep']}+{c}{at['nbv']}+({c}{at['rev']}-{p}{at['rev']})/{I['s2c']}+{c}{at['dwc']})")
    line("capexp", "Capex % revenue", lambda c, p: f"=-{c}{at['capex']}/{c}{at['rev']}", xl.FMT_PCT,
         terminal="=-{t}{r_fcap}/{t}{r_rev}")
    line("acq", "Acquisitions (none modelled after FY2026)", lambda c, p: f"=-{I['acq26']}" if c == g else None)
    eq = (f"=BS!{f25}{bs_at['Total equity']}+BS!{f25}{bs_at['Current debt']}+BS!{f25}{bs_at['Long-term debt']}"
          f"-BS!{f25}{bs_at['Cash and cash equivalents']}-BS!{f25}{bs_at['Marketable securities, current']}"
          f"-BS!{f25}{bs_at['Marketable securities, long-term']}")
    line("ic", "Invested capital (year-end)",
         lambda c, p: f"={p}{at['ic']}-{c}{at['capex']}-{c}{at['acq']}-{c}{at['da']}-{c}{at['nbv']}-{c}{at['dwc']}",
         hist=eq)
    line("icr", "Invested capital / revenue", lambda c, p: f"={c}{at['ic']}/{c}{at['rev']}", xl.FMT_PCT,
         hist=f"={f25}{{r_ic}}/{f25}{{r_rev}}")
    line("roic", "ROIC on opening capital", lambda c, p: f"={c}{at['nopat']}/{p}{at['ic']}", xl.FMT_PCT)

    sec("Free cash flow to the firm (acquisitions excluded)")
    f30 = COL["FY2030"]
    line("fn", "NOPAT", lambda c, p: f"={c}{at['nopat']}", terminal="={t}{r_nopat}")
    line("fda", "D&A", lambda c, p: f"={c}{at['da']}", terminal="={t}{r_da}")
    line("fgain", "Gain on sale of PP&E (non-cash)", lambda c, p: f"=-{c}{at['gain']}",
         terminal=f"=-{f30}{at['gain']}*(1+{I['gLR']})")
    # terminal capex: replace D&A and the equipment sold, plus g / RONIC of NOPAT
    line("fcap", "Capex", lambda c, p: f"={c}{at['capex']}",
         terminal=f"=-({{t}}{{r_da}}+{{t}}{{r_fproc}}+{{t}}{{r_fgain}}+{I['gLR']}/{I['ronic']}*{{t}}{{r_nopat}})")
    line("fproc", "Proceeds from sale of PP&E", lambda c, p: f"={c}{at['proc']}",
         terminal=f"={f30}{at['proc']}*(1+{I['gLR']})")
    line("fwc", "Change in working capital", lambda c, p: f"={c}{at['dwc']}", terminal="=0")
    parts = ("fn", "fda", "fgain", "fcap", "fproc", "fwc")
    line("fcff", "FCFF", lambda c, p: "=" + "+".join(f"{c}{at[k]}" for k in parts),
         terminal="=" + "+".join(f"{{t}}{{r_{k}}}" for k in parts), bold=True)
    # net investment = capex - D&A - book value sold + increase in working capital
    inv = ("fcap", "fda", "fgain", "fproc", "fwc")
    line("rr", "Reinvestment rate (net investment / NOPAT)",
         lambda c, p: "=-(" + "+".join(f"{c}{at[k]}" for k in inv) + f")/{c}{at['fn']}", xl.FMT_PCT,
         terminal="=-(" + "+".join(f"{{t}}{{r_{k}}}" for k in inv) + ")/{t}{r_fn}")

    # fill in the {r}/{t} placeholders now that every row number is known
    subs = {"t": term, "r_twc": at["twc"], "r_rev": at["rev"], "r_nopat": at["nopat"], "r_ic": at["ic"],
            "r_da": at["da"], "r_roic": at["roic"], "r_fn": at["fn"], "r_fda": at["fda"], "r_fcap": at["fcap"],
            "r_fwc": at["fwc"], "r_fgain": at["fgain"], "r_fproc": at["fproc"]}
    for key, r_ in at.items():
        for col in (f25, term):
            cell = ws[f"{col}{r_}"]
            if isinstance(cell.value, str) and "{" in cell.value:
                cell.value = cell.value.format(r=r_, **subs)

    # check row: working capital lands on its FY2030E target
    ws["A3"] = "WC check (FY2030E trade WC % - target, should be 0)"
    ws["A3"].font = xl.BOLD
    xl.put_formula(ws, f"{COL['FY2030']}3", f"=ROUND({COL['FY2030']}{at['twcp']}-{I['nwc_target']},6)", xl.FMT_PCT)
    return ws, at


def year_header(ws, title: str, inputs: bool = False) -> None:
    """Title, units and the year row. On Inputs, column B holds single values
    and the history columns are left empty, so only the forecast years get headers."""
    ws["A1"] = title
    ws["A1"].font = xl.BOLD
    ws["A2"] = "USD m unless stated"
    ws["A2"].font = xl.NOTE
    labels = {p: p + ("A" if p in HIST else "E") for p in COL}
    if inputs:
        labels = {p: ("Value" if p == HIST[0] else "") for p in HIST} | {p: labels[p] for p in FCST}
    for p, c in COL.items():
        cell = ws[f"{c}{HEADER_ROW}"]
        cell.value = labels[p] or None
        cell.font = xl.BOLD
        cell.alignment = Alignment(horizontal="right")
    xl.header(ws, HEADER_ROW, "", LAST_COL)
    for p, c in COL.items():
        ws.column_dimensions[c].width = 3 if inputs and p in HIST[1:] else 11


def write_statement(ws, stmt: str, rows, values: pd.DataFrame, start_row: int) -> dict[str, int]:
    """History values in blue, subtotals as formulas. Returns label -> row."""
    # drop lines that are zero in every year, and take them out of the subtotals too
    used = [r for r in rows if r.parts is not None
            or values.loc[r.label, HIST].abs().sum() > 1e-9]
    labels = {r.label for r in used}
    at: dict[str, int] = {}
    row = start_row
    for r in used:
        at[r.label] = row
        ws.cell(row=row, column=1, value=r.label).font = xl.BOLD if r.label in BOLD_TOTALS else xl.BASE
        for p in HIST:
            ref = f"{COL[p]}{row}"
            if r.parts is None:
                xl.put_input(ws, ref, round(float(values.loc[r.label, p]), 3), xl.FMT_NUM)
            else:
                parts = [q for q in r.parts if q in labels]
                xl.put_formula(ws, ref, "=" + "+".join(f"{COL[p]}{at[q]}" for q in parts), xl.FMT_NUM,
                               bold=r.label in BOLD_TOTALS)
        if r.label in BOLD_TOTALS:
            for c in range(1, LAST_COL + 1):
                ws.cell(row=row, column=c).border = xl.Border(top=xl.Side(style="thin"))
        row += 1
    return at


def build() -> Path:
    long = pd.read_csv(PROCESSED / "statements_long.csv")
    facts = pd.read_csv(PROCESSED / "facts.csv", dtype={"dims": str}).fillna({"dims": ""})
    wide = {s: long[long["statement"] == s].pivot(index="line", columns="period", values="value")
            for s in ("IS", "BS", "CF", "Memo")}
    dam = damodaran_inputs()
    cap = pd.read_csv(PROCESSED / "cap.csv", parse_dates=["date"])

    wb = Workbook()
    cover = wb.active
    cover.title = "Cover"
    xl.setup_sheet(cover, freeze=None, col_a_width=90, landscape=False)
    lines = [
        ("Granite Construction (NYSE: GVA): three-statement model and DCF", xl.BOLD),
        ("Ali Asgarov", xl.BASE),
        (f"Draft, {date.today():%d %b %Y}. Forecast and valuation not yet built.", xl.BASE),
        ("", xl.BASE),
        ("Sources: Granite 10-K and 10-Q filings (SEC EDGAR, inline XBRL); Damodaran datasets (Jan 2026);", xl.NOTE),
        ("FRED series DGS10. Full list with accession numbers in data/SOURCES.md.", xl.NOTE),
        ("Blue = hard-coded input or reported figure. Black = formula. USD m unless stated.", xl.NOTE),
    ]
    for i, (text, font) in enumerate(lines, start=1):
        cover.cell(row=i, column=1, value=text).font = font

    # Inputs: scalars in B with a note in C; year-by-year inputs in the forecast columns
    inp = wb.create_sheet("Inputs")
    xl.setup_sheet(inp, freeze="B6", col_a_width=44)
    year_header(inp, "Inputs", inputs=True)
    note_col = LAST_COL + 2  # one empty column so numbers and notes don't touch
    inp.column_dimensions[get_column_letter(note_col)].width = 78

    r = FIRST_ROW
    I: dict[str, str] = {}  # input key -> absolute reference, used by the Sched formulas

    def section(title):
        nonlocal r
        r += 1
        xl.header(inp, r, title, LAST_COL)
        r += 1

    def scalar(key, label, value, fmt, note, status=""):
        # status "PENDING" leaves the cell empty; "INTERIM" marks a stand-in value
        nonlocal r
        inp.cell(row=r, column=1, value=label).font = xl.BASE
        I[key] = f"Inputs!$B${r}"
        if status != "PENDING":
            xl.put_input(inp, f"B{r}", value, fmt)
        text = f"{status}: {note}" if status else note
        inp.cell(row=r, column=note_col, value=text).font = xl.NOTE
        r += 1

    def series(key, label, values, fmt, note):
        nonlocal r
        inp.cell(row=r, column=1, value=label).font = xl.BASE
        I[key] = r  # row number; Sched picks the column
        for p, v in zip(FCST, values):
            if v is not None:
                xl.put_input(inp, f"{COL[p]}{r}", v, fmt)
        inp.cell(row=r, column=note_col, value=note).font = xl.NOTE
        r += 1

    later: dict[str, int] = {}  # formula inputs filled once the statement rows are known

    def placeholder(key, label, note):
        nonlocal r
        inp.cell(row=r, column=1, value=label).font = xl.BASE
        inp.cell(row=r, column=note_col, value=note).font = xl.NOTE
        I[key] = f"Inputs!$B${r}"
        later[key] = r
        r += 1

    h1 = interim_h1(facts, wide["IS"], wide["CF"])
    interim = "H1 2026 actual (Q2 10-Q); replace with 9M on 29 Oct"

    section("Scenario")
    scalar("scen", "Scenario (1 base, 2 downside, 3 upside)", 1, "0",
           "2 = reauthorisation gap + 14.5% gross margin; 3 = gross margin implied by FY2026 guidance; memo s.5-6")

    section("Revenue")
    scalar("rev26", "FY2026E revenue", 5300, xl.FMT_NUM, "Low end of guidance (USD 5.3-5.5bn), 8-K 30 Jul 2026; memo s.5")
    scalar("mshare", "FY2026E Materials share of revenue", round(h1["materials_share"], 4), xl.FMT_PCT,
           interim, "INTERIM")
    for y in (2022, 2023, 2024, 2025):
        d = cap.loc[cap["date"] == f"{y}-09-30"].iloc[0]
        scalar(f"cap_s{y % 100}", f"CAP at 30 Sep {y}", d["cap"], xl.FMT_NUM,
               f"Committed and awarded projects, {d['form']} {d['accession']}, MD&A")
    scalar("acq_c25", "FY2025 Construction revenue from 2025 acquisitions", 112.1, xl.FMT_NUM,
           "Warren Paving and Papich, not in Sep 2024 CAP; FY2025 10-K, MD&A (Construction revenue)")
    placeholder("burn", "Construction revenue next FY / CAP at 30 Sep, FY2023-25 avg",
                "Share of September backlog that becomes next year's Construction revenue, FY2025 excl. acquisitions; memo s.5")
    d = cap.iloc[-1]
    scalar("cap_now", "CAP at latest quarter-end", d["cap"], xl.FMT_NUM,
           f"{d['date']:%d %b %Y}, {d['form']} {d['accession']}; replace with 30 Sep 2026 on 29 Oct", "INTERIM")
    scalar("gLR", "Long-run growth (FY2030E and terminal)", 0.04, xl.FMT_PCT, "Approx. long-run US nominal GDP; source in step 5; memo s.5")
    scalar("gfade", "Years to fade growth to long-run rate", 3, "0", "FY2027E (CAP-anchored) to FY2030E; memo s.5")
    scalar("down", "Downside: FY2027E Construction growth", 0.0, xl.FMT_PCT, "Reauthorisation gap through FY2027; memo s.5")

    section("Margins")
    scalar("gm26", "FY2026E gross margin", round(h1["gross_margin"], 4), xl.FMT_PCT,
           "H1 2026 actual (Q2 10-Q), seasonally low; replace with 9M on 29 Oct", "INTERIM")
    scalar("gm", "Gross margin from FY2027E, base", 0.15, xl.FMT_PCT,
           "Midpoint of the 14.6-15.4% FY2025 normalisation range; memo s.6")
    scalar("gm_down", "Gross margin from FY2027E, downside", 0.145, xl.FMT_PCT,
           "All FY2025 upward revisions treated as one-off; memo s.6")
    scalar("adj_lo", "FY2026 guidance: adjusted EBITDA margin, low", 0.1225, xl.FMT_PCT, "8-K 30 Jul 2026, Exhibit 99.1")
    scalar("adj_hi", "FY2026 guidance: adjusted EBITDA margin, high", 0.1325, xl.FMT_PCT, "8-K 30 Jul 2026, Exhibit 99.1")
    placeholder("adj25", "FY2025 adjusted EBITDA margin (rebuilt)",
                "Granite definition from filed lines: EBIT + D&A + SBC + other costs + affiliates + other income - NCI")
    placeholder("gm_up", "Gross margin from FY2027E, upside",
                "Guidance midpoint + FY2025 gap between gross margin and adjusted EBITDA margin; memo s.6")
    scalar("sga", "SG&A % revenue", 0.0875, xl.FMT_PCT,
           "Top of FY2026 guidance (8.25-8.75%, incl. SBC), held; low-end revenue on a largely fixed cost base; memo s.6")

    section("Smaller lines (memo s.6)")
    placeholder("oc", "Other costs, net, % revenue", "FY2022-25 average")
    placeholder("gain", "Gain on sale of PP&E, % revenue", "FY2022-25 average; operating, recurring equipment sales")
    placeholder("proc", "Proceeds from sale of PP&E, % revenue",
                "FY2022-25 average (cash flow); proceeds - gain = book value sold")
    placeholder("aff", "Equity income of affiliates, % revenue",
                "FY2022-25 average; non-operating, valued in the equity bridge")
    placeholder("oth", "Other income, net, % revenue", "FY2022-25 average; non-operating")
    placeholder("yld", "Interest income / average cash and securities", "FY2025 yield; used with the cash forecast after Q3")
    placeholder("nci", "NCI share of pre-tax income",
                "FY2024-25 average (FY2022-23 JV losses not representative); used after Q3")

    section("Working capital (FY2022-25 averages)")
    wc_start = r
    r += 7  # filled once the IS/BS rows are known
    scalar("nwc_target", "Trade working capital % revenue, FY2030E target", 0.0, xl.FMT_PCT,
           "Gap closed through contract assets only; memo s.7")
    scalar("fade", "Years for contract asset days to reach target", 4, "0", "FY2026E to FY2030E; memo s.7")

    section("Capex, D&A, tax")
    scalar("capex26", "FY2026E capex", 150, xl.FMT_NUM, "Midpoint of guidance USD 140-160m, 8-K 30 Jul 2026")
    placeholder("s2c", "Sales-to-capital, FY2022-25 avg, excl. goodwill/intangibles",
                "Revenue / year-end invested capital excl. goodwill and intangibles; drives FY2027E-30E reinvestment; memo s.8")
    dep_row = r
    I["dep"] = f"Inputs!$B${r}"
    r += 1  # formula, filled below
    series("amort", "Intangible amortisation", amortisation_schedule(facts), xl.FMT_NUM,
           "FY2025 10-K expected amortisation; Kenny Seng to be added from Q3 10-Q")
    scalar("acq26", "FY2026E acquisitions (cash)", round(h1["acquisitions"], 1), xl.FMT_NUM,
           "Kenny Seng, H1 2026 cash flow (Q2 10-Q); none modelled after FY2026 (memo s.4); replace with 9M on 29 Oct",
           "INTERIM")
    scalar("tax", "Tax rate on operating profit", 0.25, xl.FMT_PCT, "21% federal + ~4% state (FY2025 rate reconciliation); memo s.8")

    section("Cost of capital")
    scalar("beta_ec", "Unlevered beta, Eng./Construction, 2022-26 avg", round(dam["beta_ec_avg"], 4), "0.000",
           "Damodaran betas.xls (5 Jan 2026), cash-corrected; base case")
    scalar("beta_ec26", "Unlevered beta, Eng./Construction, Jan 2026", round(dam["beta_ec_2026"], 4), "0.000",
           "Damodaran betas.xls; sensitivity")
    scalar("beta_cs", "Unlevered beta, Constr. Supplies, 2022-26 avg", round(dam["beta_cs_avg"], 4), "0.000",
           "Damodaran betas.xls; Materials segment (VMC, MLM, KNF peer group); base case")
    scalar("beta_cs26", "Unlevered beta, Constr. Supplies, Jan 2026", round(dam["beta_cs_2026"], 4), "0.000",
           "Damodaran betas.xls; sensitivity")
    scalar("w_mat", "Segment value weight, Materials", None, xl.FMT_PCT, "step 5: value weights by segment", "PENDING")
    scalar("erp", "Equity risk premium", round(dam["erp"], 4), "0.00%",
           "Damodaran histimpl.xls, implied ERP start of 2026; check Oct 2026 monthly in step 5")
    scalar("rf", "Risk-free rate (10y Treasury)", None, xl.FMT_PCT, "FRED DGS10 on valuation date", "PENDING")
    scalar("kd", "Pre-tax cost of debt", None, xl.FMT_PCT, "market yield on 6.375% 2034 notes at valuation date", "PENDING")
    placeholder("ronic", "Terminal RONIC, base (FY2022-25 average ROIC)",
                "EBIT after 25% tax / average invested capital; sensitivities WACC and 13%; memo s.8")

    # statements
    sheets = {}
    for stmt, rows, title in [("IS", IS_ROWS, "Income statement"), ("BS", BS_ROWS, "Balance sheet"),
                              ("CF", CF_ROWS, "Cash flow statement")]:
        ws = wb.create_sheet(stmt)
        xl.setup_sheet(ws, freeze=f"B{FIRST_ROW}", col_a_width=40)
        year_header(ws, title)
        sheets[stmt] = (ws, write_statement(ws, stmt, rows, wide[stmt], FIRST_ROW))

    is_ws, is_at = sheets["IS"]
    bs_ws, bs_at = sheets["BS"]
    cf_ws, cf_at = sheets["CF"]

    # memo lines
    memo_next: dict[str, int] = {}

    def memo_row(ws, at, label, values=None, formula=None, fmt=xl.FMT_NUM):
        # memo block starts one blank row below the statement, then one row per line
        row = memo_next.get(ws.title, max(at.values()) + 2)
        memo_next[ws.title] = row + 1
        at["memo:" + label] = row
        ws.cell(row=row, column=1, value=label).font = xl.BASE
        for p in HIST:
            ref = f"{COL[p]}{row}"
            if formula:
                xl.put_formula(ws, ref, formula(COL[p]), fmt)
            elif values is not None and p in values:
                xl.put_input(ws, ref, round(float(values[p]), 3), fmt)
        return row

    amort = amortisation_history(facts)
    memo_row(cf_ws, cf_at, "of which: intangible amortisation (in D&A)", amort)
    memo_row(bs_ws, bs_at, "of which: retention receivable (in receivables)", wide["Memo"].loc["Retention receivable"])
    memo_row(bs_ws, bs_at, "Backlog (remaining performance obligations)", wide["Memo"].loc["Backlog (RPO)"])
    memo_row(is_ws, is_at, "D&A (from CF)", formula=lambda c: f"=CF!{c}{cf_at['D&A']}")
    memo_row(is_ws, is_at, "EBITDA (operating income + D&A)",
             formula=lambda c: f"={c}{is_at['Operating income']}+{c}{is_at['memo:D&A (from CF)']}")
    memo_row(is_ws, is_at, "Diluted shares (m)", wide["Memo"].loc["Diluted shares (m)"])
    memo_row(is_ws, is_at, "Construction segment revenue", segments(facts).loc[("Construction", "revenue")])

    # check rows at the top of BS and CF
    bs_ws["A3"] = "BS check (assets - L&E, should be 0)"
    cf_ws["A3"] = "CF check (vs IS net income, should be 0)"
    for p in HIST:
        c = COL[p]
        xl.put_formula(bs_ws, f"{c}3", f"=ROUND({c}{bs_at['Total assets']}-{c}{bs_at['Total liabilities and equity']},3)", xl.FMT_NUM)
        xl.put_formula(cf_ws, f"{c}3", f"=ROUND({c}{cf_at['Net income incl. NCI']}-IS!{c}{is_at['Net income incl. NCI']},3)", xl.FMT_NUM)
    for ws in (bs_ws, cf_ws):
        ws["A3"].font = xl.BOLD

    # working capital averages: formulas over FY2022-FY2025 history
    span = lambda sheet, row: f"{sheet}!{COL['FY2022']}{row}:{COL['FY2025']}{row}"
    rev, cogs = is_at["Revenue"], is_at["Cost of revenue"]
    ret_row = bs_at["memo:of which: retention receivable (in receivables)"]

    def days(bs_row, base_row, sign=1):
        # average over the four years of balance / flow * 365
        terms = ",".join(f"BS!{COL[p]}{bs_row}/({sign}*IS!{COL[p]}{base_row})*365"
                         for p in ["FY2022", "FY2023", "FY2024", "FY2025"])
        return f"=AVERAGE({terms})"

    wc_lines = [
        ("Receivables excl. retention, days of revenue",
         "=AVERAGE(" + ",".join(f"(BS!{COL[p]}{bs_at['Receivables, net']}-BS!{COL[p]}{ret_row})/IS!{COL[p]}{rev}*365"
                                for p in ["FY2022", "FY2023", "FY2024", "FY2025"]) + ")", "0.0"),
        ("Retention receivable, % revenue",
         "=AVERAGE(" + ",".join(f"BS!{COL[p]}{ret_row}/IS!{COL[p]}{rev}" for p in ["FY2022", "FY2023", "FY2024", "FY2025"]) + ")",
         xl.FMT_PCT),
        ("Contract assets, days of revenue", days(bs_at["Contract assets"], rev), "0.0"),
        ("Inventories, days of cost of revenue", days(bs_at["Inventories"], cogs, -1), "0.0"),
        ("Accounts payable, days of cost of revenue", days(bs_at["Accounts payable"], cogs, -1), "0.0"),
        ("Contract liabilities, days of revenue", days(bs_at["Contract liabilities"], rev), "0.0"),
        ("Accrued and other liabilities, days of revenue", days(bs_at["Accrued and other current liabilities"], rev), "0.0"),
    ]
    for i, (key, (label, formula, fmt)) in enumerate(zip(["recd", "ret", "cad", "invd", "apd", "cld", "accd"], wc_lines)):
        inp.cell(row=wc_start + i, column=1, value=label).font = xl.BASE
        xl.put_formula(inp, f"B{wc_start + i}", formula, fmt)
        I[key] = f"Inputs!$B${wc_start + i}"
    inp.cell(row=wc_start, column=note_col, value="FY2021 excluded (USD 129m legal accrual); memo s.7").font = xl.NOTE

    inp.cell(row=dep_row, column=1, value="Depreciation and depletion % revenue").font = xl.BASE
    f25 = COL["FY2025"]
    xl.put_formula(inp, f"B{dep_row}",
                   f"=(CF!{f25}{cf_at['D&A']}-CF!{f25}{cf_at['memo:of which: intangible amortisation (in D&A)']})/IS!{f25}{rev}",
                   xl.FMT_PCT)
    inp.cell(row=dep_row, column=note_col, value="FY2025 level, excl. amortisation; memo s.8").font = xl.NOTE

    yrs = ["FY2022", "FY2023", "FY2024", "FY2025"]

    def ic(c):  # invested capital = equity incl. NCI + debt - cash - marketable securities
        b = lambda name: f"BS!{c}{bs_at[name]}"
        return (f"({b('Total equity')}+{b('Current debt')}+{b('Long-term debt')}-{b('Cash and cash equivalents')}"
                f"-{b('Marketable securities, current')}-{b('Marketable securities, long-term')})")

    fills = {
        "s2c": ("=AVERAGE(" + ",".join(
            f"IS!{COL[y]}{rev}/({ic(COL[y])}-BS!{COL[y]}{bs_at['Goodwill']}-BS!{COL[y]}{bs_at['Intangible assets']})"
            for y in yrs) + ")", "0.00"),
        # September CAP of one year against Construction revenue of the next; FY2025 revenue
        # from businesses bought in 2025 was never in the September 2024 backlog, so it's taken out
        "burn": ("=AVERAGE(" + ",".join(
            f"(IS!{COL[f'FY{y + 1}']}{is_at['memo:Construction segment revenue']}"
            + (f"-{I['acq_c25']}" if y == 2024 else "") + f")/{I[f'cap_s{y % 100}']}"
            for y in (2022, 2023, 2024)) + ")", "0.000"),
        **{k: ("=AVERAGE(" + ",".join(f"{sh}!{COL[y]}{row_}/IS!{COL[y]}{rev}" for y in yrs) + ")", "0.00%")
           for k, sh, row_ in (("oc", "IS", is_at["Other costs, net"]), ("gain", "IS", is_at["Gain on sale of PP&E"]),
                               ("proc", "CF", cf_at["Proceeds from sale of PP&E"]),
                               ("aff", "IS", is_at["Equity income of affiliates"]),
                               ("oth", "IS", is_at["Other income, net"]))},
        "yld": (f"=IS!{f25}{is_at['Interest income']}/AVERAGE(" + ",".join(
            "SUM(" + ",".join(f"BS!{COL[y]}{bs_at[n]}" for n in ("Cash and cash equivalents",
                                                              "Marketable securities, current",
                                                              "Marketable securities, long-term")) + ")"
            for y in ("FY2024", "FY2025")) + ")", "0.00%"),
        "nci": ("=AVERAGE(" + ",".join(
            f"-IS!{COL[y]}{is_at['Non-controlling interests']}/IS!{COL[y]}{is_at['Pre-tax income']}"
            for y in ("FY2024", "FY2025")) + ")", xl.FMT_PCT),
        "ronic": ("=AVERAGE(" + ",".join(
            f"IS!{COL[y]}{is_at['Operating income']}*(1-{I['tax']})/(({ic(COL[y])}+{ic(COL[HIST[HIST.index(y) - 1]])})/2)"
            for y in yrs) + ")", xl.FMT_PCT),
        "adj25": (f"=(IS!{f25}{is_at['Operating income']}+CF!{f25}{cf_at['D&A']}+CF!{f25}{cf_at['Stock-based compensation']}"
                  f"-IS!{f25}{is_at['Other costs, net']}+IS!{f25}{is_at['Equity income of affiliates']}"
                  f"+IS!{f25}{is_at['Other income, net']}+IS!{f25}{is_at['Non-controlling interests']})/IS!{f25}{rev}",
                  xl.FMT_PCT),
        "gm_up": (f"=AVERAGE({I['adj_lo']},{I['adj_hi']})+(IS!{f25}{is_at['Gross profit']}/IS!{f25}{rev}-{I['adj25']})",
                  xl.FMT_PCT),
    }
    for key, (formula, fmt) in fills.items():
        xl.put_formula(inp, f"B{later[key]}", formula, fmt)

    sched_ws, _ = build_sched(wb, I, is_at, bs_at)

    # Print areas end in a narrow empty spacer column: the PDF printer clips the last
    # column at its hard margin, and this way it clips the spacer, not FY2030E.
    for ws, last in ((is_ws, LAST_COL), (bs_ws, LAST_COL), (cf_ws, LAST_COL), (inp, note_col),
                     (sched_ws, LAST_COL + 1)):
        spacer = get_column_letter(last + 1)
        ws.column_dimensions[spacer].width = 3
        ws.print_area = f"A1:{spacer}{ws.max_row}"
        # a fixed scale prints more reliably than Excel's fit-to-width, which left
        # FY2030E half off the page in the PDF export
        if ws is inp:
            ws.page_setup.fitToHeight = 1  # fit-to-page works here and keeps it on one sheet
        else:
            ws.sheet_properties.pageSetUpPr.fitToPage = False
            ws.page_setup.scale = 80

    MODEL.parent.mkdir(parents=True, exist_ok=True)
    wb.save(MODEL)
    return MODEL


def check(path: Path) -> None:
    """After Excel recalculation: no errors, checks at zero, totals equal the filings."""
    errors = xl.find_errors(path)
    print("Excel errors:", errors or "none")

    wb = load_workbook(path, data_only=True)
    long = pd.read_csv(PROCESSED / "statements_long.csv")
    filed = long[long["is_total"] & long["filed_total"].notna() & long["period"].isin(HIST)]
    worst = 0.0
    for stmt in ("IS", "BS", "CF"):
        ws = wb[stmt]
        rows = {ws.cell(row=i, column=1).value: i for i in range(FIRST_ROW, ws.max_row + 1)}
        for p in HIST:
            if stmt in ("BS", "CF"):
                v = ws[f"{COL[p]}3"].value
                assert v is not None and abs(v) < 1e-6, f"{stmt} check {p} = {v}"
        for r in filed[filed["statement"] == stmt].itertuples():
            v = ws[f"{COL[r.period]}{rows[r.line]}"].value
            worst = max(worst, abs(v - r.filed_total))
    print(f"BS and CF check rows: 0 in all years; largest gap between workbook totals and filed totals: {worst:.3f} USD m")
    sched = wb["Sched"]
    k = COL["FY2030"]
    assert abs(sched[f"{k}3"].value) < 1e-9, f"WC check = {sched[k + '3'].value}"
    print("Sched WC check: 0 (FY2030E trade working capital on target)")


def main() -> None:
    path = build()
    xl.recalc_with_excel(path)
    check(path)
    print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
