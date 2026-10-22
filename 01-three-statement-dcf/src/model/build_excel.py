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

    def section(title):
        nonlocal r
        r += 1
        xl.header(inp, r, title, LAST_COL)
        r += 1

    def scalar(label, value, fmt, note):
        nonlocal r
        inp.cell(row=r, column=1, value=label).font = xl.BASE
        if value is None:
            inp.cell(row=r, column=note_col, value="PENDING: " + note).font = xl.NOTE
        else:
            xl.put_input(inp, f"B{r}", value, fmt)
            inp.cell(row=r, column=note_col, value=note).font = xl.NOTE
        r += 1

    def series(label, values, fmt, note):
        nonlocal r
        inp.cell(row=r, column=1, value=label).font = xl.BASE
        for p, v in zip(FCST, values):
            if v is not None:
                xl.put_input(inp, f"{COL[p]}{r}", v, fmt)
        inp.cell(row=r, column=note_col, value=note).font = xl.NOTE
        r += 1

    section("Revenue")
    scalar("FY2026E revenue", 5300, xl.FMT_NUM, "Low end of guidance (USD 5.3-5.5bn), 8-K 30 Jul 2026; memo s.5")
    scalar("FY2026E Materials share of revenue", None, xl.FMT_PCT, "from 9M 2026 actuals (Q3 10-Q)")
    scalar("FY2026E organic growth (start of fade)", None, xl.FMT_PCT, "from 9M 2026 acquired revenue (Q3 release)")
    scalar("Long-run growth (FY2030E and terminal)", 0.04, xl.FMT_PCT, "Approx. long-run US nominal GDP; source in step 5; memo s.5")
    scalar("Downside: FY2027E Construction growth", 0.0, xl.FMT_PCT, "Reauthorisation gap through FY2027; memo s.5")

    section("Margins")
    scalar("FY2026E gross margin", None, xl.FMT_PCT, "9M 2026 actual (Q3 10-Q)")
    scalar("Gross margin from FY2027E, base", 0.145, xl.FMT_PCT, "FY2025 16.1% less claim-driven revisions; memo s.6")
    scalar("Gross margin from FY2027E, upside", 0.16, xl.FMT_PCT, "FY2025 level held; memo s.6")
    scalar("SG&A % revenue FY2026E", None, xl.FMT_PCT, "guidance 8.25-8.75% incl. SBC; point in range to confirm")

    section("Working capital (FY2022-25 averages)")
    wc_start = r
    r += 7  # filled once the IS/BS rows are known
    scalar("Trade working capital % revenue, FY2030E target", 0.0, xl.FMT_PCT, "Gap closed through contract assets only; memo s.7")

    section("Capex, D&A, tax")
    scalar("FY2026E capex", 150, xl.FMT_NUM, "Midpoint of guidance USD 140-160m, 8-K 30 Jul 2026")
    scalar("Capex % revenue FY2027E-FY2029E", 0.035, xl.FMT_PCT, "Near FY2022-25 average 3.6%; FY2030E set by reinvestment rule; memo s.8")
    dep_row = r
    r += 1  # formula, filled below
    series("Intangible amortisation", amortisation_schedule(facts), xl.FMT_NUM,
           "FY2025 10-K expected amortisation; Kenny Seng to be added from Q3 10-Q")
    scalar("Tax rate on operating profit", 0.25, xl.FMT_PCT, "21% federal + ~4% state (FY2025 rate reconciliation); memo s.8")

    section("Cost of capital")
    scalar("Unlevered beta, Eng./Construction, 2022-26 avg", round(dam["beta_ec_avg"], 4), "0.000",
           "Damodaran betas.xls (5 Jan 2026), cash-corrected; base case")
    scalar("Unlevered beta, Eng./Construction, Jan 2026", round(dam["beta_ec_2026"], 4), "0.000",
           "Damodaran betas.xls; sensitivity")
    scalar("Unlevered beta, Constr. Supplies, 2022-26 avg", round(dam["beta_cs_avg"], 4), "0.000",
           "Damodaran betas.xls; Materials segment (VMC, MLM, KNF peer group); base case")
    scalar("Unlevered beta, Constr. Supplies, Jan 2026", round(dam["beta_cs_2026"], 4), "0.000",
           "Damodaran betas.xls; sensitivity")
    scalar("Segment value weight, Materials", None, xl.FMT_PCT, "step 5: value weights by segment")
    scalar("Equity risk premium", round(dam["erp"], 4), "0.00%",
           "Damodaran histimpl.xls, implied ERP start of 2026; check Oct 2026 monthly in step 5")
    scalar("Risk-free rate (10y Treasury)", None, xl.FMT_PCT, "FRED DGS10 on valuation date")
    scalar("Pre-tax cost of debt", None, xl.FMT_PCT, "market yield on 6.375% 2034 notes at valuation date")
    scalar("Terminal RONIC", None, xl.FMT_PCT, "= model terminal-year ROIC (formula, forecast step); memo s.8")

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
    for i, (label, formula, fmt) in enumerate(wc_lines):
        inp.cell(row=wc_start + i, column=1, value=label).font = xl.BASE
        xl.put_formula(inp, f"B{wc_start + i}", formula, fmt)
    inp.cell(row=wc_start, column=note_col, value="FY2021 excluded (USD 129m legal accrual); memo s.7").font = xl.NOTE

    inp.cell(row=dep_row, column=1, value="Depreciation and depletion % revenue").font = xl.BASE
    f25 = COL["FY2025"]
    xl.put_formula(inp, f"B{dep_row}",
                   f"=(CF!{f25}{cf_at['D&A']}-CF!{f25}{cf_at['memo:of which: intangible amortisation (in D&A)']})/IS!{f25}{rev}",
                   xl.FMT_PCT)
    inp.cell(row=dep_row, column=note_col, value="FY2025 level, excl. amortisation; memo s.8").font = xl.NOTE

    # Print areas end in a narrow empty spacer column: the PDF printer clips the last
    # column at its hard margin, and this way it clips the spacer, not FY2030E.
    for ws, last in ((is_ws, LAST_COL), (bs_ws, LAST_COL), (cf_ws, LAST_COL), (inp, note_col)):
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


def main() -> None:
    path = build()
    xl.recalc_with_excel(path)
    check(path)
    print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
