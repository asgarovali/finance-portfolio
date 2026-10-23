from openpyxl import load_workbook

from src.model import build_excel


def test_workbook_layout(tmp_path, monkeypatch):
    # build only (no Excel recalculation), into a temp file
    monkeypatch.setattr(build_excel, "MODEL", tmp_path / "m.xlsx")
    wb = load_workbook(build_excel.build())

    assert wb.sheetnames == ["Cover", "Inputs", "IS", "BS", "CF", "Sched", "WACC"]
    ws = wb["IS"]
    labels = {ws.cell(row=r, column=1).value: r for r in range(1, ws.max_row + 1)}
    revenue = ws.cell(row=labels["Revenue"], column=2)
    gross = ws.cell(row=labels["Gross profit"], column=2)

    assert revenue.font.color.rgb.endswith("0000FF")  # reported history is a blue input
    assert gross.value.startswith("=")                # subtotals are formulas
    assert str(wb["BS"]["B3"].value).startswith("=ROUND(")  # balance check row
    # pending inputs stay empty instead of being guessed
    inp = wb["Inputs"]
    pending = [r for r in range(1, inp.max_row + 1)
               if str(inp.cell(row=r, column=13).value or "").startswith("PENDING")]
    assert pending and all(inp.cell(row=r, column=2).value is None for r in pending)
    # interim stand-ins are filled and labelled
    interim = [r for r in range(1, inp.max_row + 1)
               if str(inp.cell(row=r, column=13).value or "").startswith("INTERIM")]
    assert interim and all(inp.cell(row=r, column=2).value is not None for r in interim)
