"""Two-page PDF summary of the valuation, built from the recalculated workbook and the charts.

Run from the project folder (after the model and charts):  python -m src.report.summary
"""
from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "model" / "granite_model.xlsx"
OUT = ROOT / "report" / "granite_dcf_summary.pdf"
NAVY = colors.HexColor("#1f3b5c")

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=12, alignment=TA_LEFT, spaceAfter=4)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=NAVY, spaceAfter=2)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=NAVY,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.5, leading=9.5, textColor=colors.HexColor("#666666"))


def _rows(ws) -> dict[str, int]:
    return {ws.cell(row=r, column=1).value: r for r in range(1, ws.max_row + 1)}


def values() -> dict:
    wb = load_workbook(MODEL, data_only=True)
    dcf, wacc, sens, sch, inp = wb["DCF"], wb["WACC"], wb["Sens"], wb["Sched"], wb["Inputs"]
    D, W, N, S, I = _rows(dcf), _rows(wacc), _rows(sens), _rows(sch), _rows(inp)
    d = lambda k, c="B": dcf[f"{c}{D[k]}"].value
    return {
        "vps": d("Value per share (USD)"), "exit": d("Value per share (USD)", "C"), "price": d("Share price (USD)"),
        "ev": d("Enterprise value"), "eq": d("Equity value"), "tv": d("Terminal value % of EV"),
        "wacc": wacc[f"B{W['WACC']}"].value, "ke": wacc[f"B{W['Cost of equity']}"].value,
        "kd": wacc[f"B{W['Pre-tax cost of debt used']}"].value, "de": wacc[f"B{W['Debt / equity']}"].value,
        "bl": wacc[f"B{W['Levered beta']}"].value,
        "down": sens[f"B{N['Downside: no Construction growth in FY2027E, gross margin 14.5%']}"].value,
        "up": sens[f"B{N['Upside: gross margin implied by FY2026 guidance']}"].value,
        "mgmt": [sens[f"E{N[k]}"].value for k in ("Low end", "Midpoint", "High end")],
        "gm_implied": sens[f"C{N['Gross margin from FY2027E']}"].value,
        "g27": sch[f"H{S['Organic growth, base path']}"].value,
        "gm26": sch[f"G{S['Gross margin']}"].value,
        "shares": d("Diluted shares (m)"),
    }


CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.5, leading=10.5, spaceAfter=0)


def table(data, widths, bold_rows=(), left_last=False):
    if left_last:  # wrap the last (text) column
        data = [row[:-1] + [Paragraph(row[-1], CELL) if i else row[-1]] for i, row in enumerate(data)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
             ("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]
    style += [("FONT", (0, r), (-1, r), "Helvetica-Bold", 8.5) for r in bold_rows]
    if left_last:
        style += [("ALIGN", (-1, 0), (-1, -1), "LEFT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    t.setStyle(TableStyle(style))
    return t


def build() -> Path:
    v = values()
    pct = lambda x: f"{x:+.0%}".replace("+-", "-")
    vs = lambda x: pct(x / v["price"] - 1)
    story = [
        Paragraph("Granite Construction (NYSE: GVA): DCF summary", H1),
        Paragraph("Ali Asgarov. Valuation date 29 Oct 2026 (Q3 2026 10-Q). USD unless stated. "
                  "Model, data and code: 01-three-statement-dcf in my finance-portfolio repository.", SMALL),
        Spacer(1, 4),
        Paragraph("Result", H2),
        Paragraph(f"My base case values Granite at <b>USD {v['vps']:.2f} per share</b>, against a share price of "
                  f"USD {v['price']:.2f} on the valuation date ({vs(v['vps'])}). Enterprise value is USD {v['ev']:,.0f}m, "
                  f"{v['tv']:.0%} of it from the terminal value, and equity value USD {v['eq']:,.0f}m on "
                  f"{v['shares']:.2f}m diluted shares. A reverse DCF shows the price is roughly what the model gives if "
                  f"Granite meets the middle of its new 2029 targets (11% organic growth a year, 15% adjusted EBITDA margin) "
                  f"and then grows at 4%.", BODY),
        table([["Case", "Value per share", "vs price"],
               ["Downside: no Construction growth in FY2027E, gross margin 14.5%", f"{v['down']:.2f}", vs(v["down"])],
               ["Base case (Gordon growth)", f"{v['vps']:.2f}", vs(v["vps"])],
               ["Upside: gross margin implied by FY2026 guidance", f"{v['up']:.2f}", vs(v["up"])],
               ["Management 2029 targets, low / mid / high",
                " / ".join(f"{x:.0f}" for x in v["mgmt"]), vs(v["mgmt"][1])],
               ["Exit multiple cross-check (Damodaran industry, 17.1x FY2030E EBITDA)", f"{v['exit']:.2f}", vs(v["exit"])]],
              [118 * mm, 30 * mm, 22 * mm], bold_rows=(2,)),
        Spacer(1, 6),
        Image(str(ROOT / "outputs" / "figures" / "football_field.png"), width=170 * mm, height=89 * mm),
        Paragraph("Key assumptions", H2),
        table([["Assumption", "Value", "Basis"],
               ["FY2026E revenue", "5,400m", "Low end of guidance (raised 29 Oct)"],
               ["FY2027E organic growth, fading to 4% by FY2030E", f"{v['g27']:.1%}", "Backlog (CAP) at 30 Sep 2026 x historical conversion"],
               ["Gross margin FY2026E / from FY2027E", f"{v['gm26']:.1%} / 15.5%", "9M actual + seasonal Q4 / net estimate revisions removed"],
               ["SG&A, % revenue", "8.75%", "Top of guidance; SBC treated as a cost"],
               ["Sales-to-capital; terminal RONIC", "3.87; 9.7%", "Granite FY2022-25 averages"],
               ["WACC", f"{v['wacc']:.2%}", f"Cost of equity {v['ke']:.2%} (levered beta {v['bl']:.2f}), pre-tax cost of debt {v['kd']:.2%}, D/E {v['de']:.0%}"],
               ["Long-run growth", "4.0%", "FOMC long-run real growth 2.0% + PCE inflation 2.0%"]],
              [62 * mm, 25 * mm, 83 * mm], left_last=True),
        PageBreak(),
        Paragraph("What the share price implies", H2),
        Paragraph(f"Changing one input at a time, the price needs a gross margin of {v['gm_implied']:.1%} from FY2027E "
                  f"(Granite reported 10.4% to 16.1% in FY2021-25), or about 33% organic growth a year to FY2030E. "
                  f"No terminal return on new capital is enough on its own. The Gordon value implies about 6.5x FY2030E "
                  f"EBITDA; the industry's 17.1x would mean growing 8.6% a year forever.", BODY),
        Image(str(ROOT / "outputs" / "figures" / "revenue_margins.png"), width=150 * mm, height=112 * mm),
        Paragraph("Interpretation", H2),
        Paragraph("My base case gives about $59 per share, well below the $121.69 price on 29 Oct. The reverse DCF shows why: "
                  "the price is roughly what you get if Granite hits the middle of its 2029 targets (about 11% organic growth "
                  "and a 15% adjusted EBITDA margin) and then slows to 4%. That needs a gross margin of about 18-19%, above "
                  "anything Granite reported in FY2021-25 (10.4-16.1%). So the gap is mostly a question of whether management "
                  "delivers its margin targets. The record backlog supports the growth part. Granite's history of optimistic "
                  "project forecasts, and the open question on federal highway funding, make me cautious about the margin "
                  "part. I read the current price as leaving little room for error rather than as clearly wrong.", BODY),
        Paragraph("Limitations", H2),
        Paragraph("Five years of history, all inside the federal infrastructure ramp-up. Reported margins depend on project cost "
                  "estimates, and Granite restated 2017-2019 for exactly that. The credit spread comes from the 30 Sep fair value "
                  "of the 6.375% notes, not a trade on the valuation date. Construction and Materials share one margin path. The "
                  "forecast is built as operating schedules driving FCFF; forecast balance sheet and cash flow statements are "
                  "not built yet.", BODY),
        Spacer(1, 4),
        Paragraph("Sources: Granite 10-K and 10-Q filings and 8-Ks (SEC EDGAR, inline XBRL); Damodaran datasets, Jan and Oct 2026 "
                  "(betas, implied ERP, EV/Sales, EV/EBITDA, return on capital, synthetic ratings); FRED (DGS10, GDPC1MDLR, "
                  "PCECTPIMDLR); share price from yfinance (Yahoo Finance). Full list with accession numbers in data/SOURCES.md; "
                  "every assumption is explained in ASSUMPTIONS.md.", SMALL),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                            bottomMargin=14 * mm, title="Granite Construction: DCF summary", author="Ali Asgarov")
    doc.build(story)
    return OUT


def main() -> None:
    print(f"saved {build().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
