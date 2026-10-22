"""Formatting helpers for openpyxl models.

Plain analyst look: white background, no gridlines, Arial 10, blue font for
inputs and black for formulas, headers as bold text with a thin bottom border.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Border, Font, Side
from openpyxl.worksheet.worksheet import Worksheet

FONT_NAME = "Arial"
FONT_SIZE = 10
BLUE = "0000FF"
ACCENT = "1F3B5C"  # the one accent colour, use sparingly

FMT_NUM = '#,##0.0;(#,##0.0);"-"'
FMT_INT = '#,##0;(#,##0);"-"'
FMT_PCT = '0.0%;(0.0%);"-"'
FMT_MULT = '0.0"x"'

BASE = Font(name=FONT_NAME, size=FONT_SIZE)
INPUT = Font(name=FONT_NAME, size=FONT_SIZE, color=BLUE)
BOLD = Font(name=FONT_NAME, size=FONT_SIZE, bold=True)
NOTE = Font(name=FONT_NAME, size=9, italic=True, color="808080")
THIN_BOTTOM = Border(bottom=Side(style="thin"))


def setup_sheet(ws: Worksheet, freeze: str | None = "B2", col_a_width: float = 32,
                landscape: bool = True) -> None:
    """Gridlines off, freeze panes, print settings."""
    ws.sheet_view.showGridLines = False
    if freeze:
        ws.freeze_panes = freeze
        # openpyxl leaves the old selection in place, which can open the file
        # scrolled to the wrong spot; point it at the top-left cell instead
        for sel in ws.sheet_view.selection:
            sel.activeCell = "A1"
            sel.sqref = "A1"
    ws.column_dimensions["A"].width = col_a_width
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def header(ws: Worksheet, row: int, text: str, last_col: int = 1) -> None:
    """Section header: bold text with a thin line under it across the used columns."""
    ws.cell(row=row, column=1, value=text).font = BOLD
    for col in range(1, last_col + 1):
        ws.cell(row=row, column=col).border = THIN_BOTTOM


def put_input(ws: Worksheet, ref: str, value, fmt: str | None = None, note: str | None = None,
              note_col_offset: int = 1) -> None:
    """Hard-coded input in blue, with an optional short source note to its right."""
    cell = ws[ref]
    cell.value = value
    cell.font = INPUT
    if fmt:
        cell.number_format = fmt
    if note:
        note_cell = ws.cell(row=cell.row, column=cell.column + note_col_offset, value=note)
        note_cell.font = NOTE


def put_formula(ws: Worksheet, ref: str, formula: str, fmt: str | None = None, bold: bool = False) -> None:
    cell = ws[ref]
    cell.value = formula
    cell.font = BOLD if bold else BASE
    if fmt:
        cell.number_format = fmt


def recalc_with_excel(path: str | Path) -> None:
    """Open the workbook in Excel, recalculate everything and save.

    openpyxl writes formulas but never calculates them, so the cached values
    stay empty until a spreadsheet program has opened the file. Windows only.
    """
    path = Path(path).resolve()
    script = (
        "$x = New-Object -ComObject Excel.Application; $x.Visible = $false; $x.DisplayAlerts = $false; "
        f"$wb = $x.Workbooks.Open('{path}'); $x.CalculateFull(); $wb.Save(); $wb.Close($false); $x.Quit(); "
        "[void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($x)"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True)


def find_errors(path: str | Path) -> list[str]:
    """Cells whose calculated value is an Excel error (#REF!, #DIV/0!, ...)."""
    wb = load_workbook(path, data_only=True)
    errors = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("#") and c.value.endswith(("!", "?", "A")):
                    errors.append(f"{ws.title}!{c.coordinate} {c.value}")
    return errors
