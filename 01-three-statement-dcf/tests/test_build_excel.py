from openpyxl import load_workbook

from src.model import build_excel


def test_workbook_layout(tmp_path, monkeypatch):
    # build only (no Excel recalculation), into a temp file
    monkeypatch.setattr(build_excel, "MODEL", tmp_path / "m.xlsx")
    wb = load_workbook(build_excel.build())

    assert wb.sheetnames == ["Cover", "Inputs", "IS", "BS", "CF", "Sched", "WACC", "DCF"]
    ws = wb["IS"]
    labels = {ws.cell(row=r, column=1).value: r for r in range(1, ws.max_row + 1)}
    revenue = ws.cell(row=labels["Revenue"], column=2)
    gross = ws.cell(row=labels["Gross profit"], column=2)

    assert revenue.font.color.rgb.endswith("0000FF")  # reported history is a blue input
    assert gross.value.startswith("=")                # subtotals are formulas
    assert str(wb["BS"]["B3"].value).startswith("=ROUND(")  # balance check row
    # after the Q3 10-Q nothing is left pending or interim, and every input row has a value
    inp = wb["Inputs"]
    notes = [str(inp.cell(row=r, column=13).value or "") for r in range(1, inp.max_row + 1)]
    assert not [n for n in notes if n.startswith(("PENDING", "INTERIM"))]
    labels = {inp.cell(row=r, column=1).value: r for r in range(1, inp.max_row + 1)}
    for key in ("Valuation date", "Share price (USD)", "Diluted shares (m)", "Debt at market value (USD m)",
                "Risk-free rate (10y Treasury)", "Cash and marketable securities, 30 Sep 2026"):
        assert inp.cell(row=labels[key], column=2).value is not None, key
