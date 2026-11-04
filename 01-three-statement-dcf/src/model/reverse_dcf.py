"""Reverse DCF and what-if cases, run in Excel on the built model.

Each case opens the workbook, changes a few cells, recalculates and (for the
reverse DCF) uses Goal Seek to find the value of one driver that makes the
Gordon value per share equal to the share price. The workbook is closed
without saving, so the base case is never touched. Windows + Excel only.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from openpyxl import load_workbook

FREE_CELL = "Inputs!$Z$1"  # scratch input used by the growth case (empty in the model)


def _rows(ws) -> dict[str, int]:
    """Label in column A -> row (last occurrence, so section headers lose to the line itself)."""
    return {ws.cell(row=r, column=1).value: r for r in range(1, ws.max_row + 1)}


def cells(path: Path) -> dict[str, str]:
    """Addresses of the cells the cases touch, found by label so row moves don't break them."""
    wb = load_workbook(path)
    inp, sch, dcf = _rows(wb["Inputs"]), _rows(wb["Sched"]), _rows(wb["DCF"])
    ronic = next(k for k in inp if k and k.startswith("Terminal RONIC"))
    return {
        "gm": f"Inputs!B{inp['Gross margin from FY2027E, base']}",
        "ronic": f"Inputs!B{inp[ronic]}",
        "price": f"Inputs!B{inp['Share price (USD)']}",
        "sga": f"Inputs!$B${inp['SG&A % revenue']}",
        "gain": f"Inputs!$B${inp['Gain on sale of PP&E, % revenue']}",
        "aff": f"Inputs!$B${inp['Equity income of affiliates, % revenue']}",
        "oth": f"Inputs!$B${inp['Other income, net, % revenue']}",
        "gLR": f"Inputs!$B${inp['Long-run growth (FY2030E and terminal)']}",
        "org_row": str(sch["Organic growth, base path"]),
        "gm_row": str(sch["Gross margin"]),
        "rev_row": str(sch["Revenue"]),
        "da_row": str(sch["D&A"]),
        "vps": f"DCF!B{dcf['Value per share (USD)']}",
    }


def _ref(addr: str) -> str:
    sheet, cell = addr.split("!")
    return f"$wb.Worksheets.Item('{sheet}').Range('{cell.replace('$', '')}')"


def run_case(path: Path, sets: list[tuple[str, str]], read: list[str], seek: tuple[str, float, str] | None = None) -> list[float]:
    """sets: (address, formula or value); seek: (target cell, goal, changing cell). Returns the read cells."""
    lines = ["$x = New-Object -ComObject Excel.Application; $x.Visible = $false; $x.DisplayAlerts = $false",
             f"$wb = $x.Workbooks.Open('{Path(path).resolve()}', 0, $true)"]
    for addr, val in sets:
        lines.append(f"{_ref(addr)}.Formula = '{val}'")
    lines.append("$x.CalculateFull()")
    if seek:
        target, goal, changing = seek
        lines.append(f"[void]{_ref(target)}.GoalSeek({goal}, {_ref(changing)}); $x.CalculateFull()")
    lines.append("Write-Output ('RESULT|' + ((@(" + ",".join(f"{_ref(a)}.Value2" for a in read) + ")) -join '|'))")
    lines.append("$wb.Close($false); $x.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($x)")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", "; ".join(lines)],
                         capture_output=True, text=True, check=True).stdout
    vals = next(l for l in out.splitlines() if l.startswith("RESULT|")).split("|")[1:]
    return [float(v) if v not in ("", None) else float("nan") for v in vals]


# Translating management's adjusted EBITDA target into the model's gross margin needs two lines
# the model doesn't forecast: SBC (FY2026 guidance, about USD 48m, 8-K 29 Oct 2026) and NCI
# (9M 2026 share of revenue, Q3 10-Q). adj EBITDA = GM - SG&A + gain + D&A + SBC + affiliates + other income - NCI
SBC_PCT = 48 / 5400
NCI_PCT = 19.069 / 4134.668
MGMT = (("Low end", 0.10, 0.14), ("Midpoint", 0.11, 0.15), ("High end", 0.12, 0.16))
MAT_SHARE = 0.234  # Materials share of segment operating income, FY2022-25 average (10-K segment notes)
MAT_RONIC = (("Granite Materials segment, FY2022-25", 0.098), ("Damodaran Construction Supplies ROC", 0.167))


def adjusted_ebitda_2026(path: Path) -> float:
    """FY2026E adjusted EBITDA margin on Granite's definition, from the model's FY2026E lines.
    SBC and NCI for Q4 are taken at the Q3 2026 rate (9M adjusted-EBITDA table, 8-K 29 Oct 2026)."""
    s = load_workbook(path, data_only=True)["Sched"]
    g = lambda k: s[f"G{_rows(s)[k]}"].value
    sbc, nci = 50.972 + 2.701, 19.069 + 7.181
    adj = g("Operating income") + g("D&A") + sbc - g("Other costs, net") + g("Equity income of affiliates") \
        + g("Other income, net") - nci
    return adj / g("Revenue")


def run_all(path: Path) -> dict:
    c = cells(path)
    v = load_workbook(path, data_only=True)
    val = lambda a: v[a.split("!")[0]][a.split("!")[1].replace("$", "")].value
    price, ronic = val(c["price"]), val(c["ronic"])
    cols = ["H", "I", "J", "K"]  # FY2027E-FY2030E on Sched
    out = {"price": price}
    out["gm"] = run_case(path, [], [c["gm"]], (c["vps"], price, c["gm"]))[0]
    out["ronic_max"] = run_case(path, [(c["ronic"], "1000")], [c["vps"]])[0]
    growth = [(FREE_CELL, "0.09")] + [(f"Sched!{x}{c['org_row']}", f"={FREE_CELL}") for x in cols]
    out["growth"] = run_case(path, growth, [FREE_CELL], (c["vps"], price, FREE_CELL))[0]
    adj26 = adjusted_ebitda_2026(path)
    out["adj26"], out["mgmt"] = adj26, []
    for label, gr, target in MGMT:
        sets = [(f"Sched!{x}{c['org_row']}", str(gr)) for x in cols[:3]] + [(f"Sched!K{c['org_row']}", f"={c['gLR']}")]
        for k, x in enumerate(cols):
            t = adj26 + (target - adj26) * min(k + 1, 3) / 3  # linear to the target in FY2029E, held in FY2030E
            sets.append((f"Sched!{x}{c['gm_row']}", f"={t}+{c['sga']}-{c['gain']}-{x}{c['da_row']}/{x}{c['rev_row']}"
                         f"-{SBC_PCT}-{c['aff']}-{c['oth']}+{NCI_PCT}"))
        vps, gm29 = run_case(path, sets, [c["vps"], f"Sched!J{c['gm_row']}"])
        out["mgmt"].append((label, gr, target, gm29, vps))
    out["mat"] = []
    for label, rm in MAT_RONIC:
        eff = 1 / ((1 - MAT_SHARE) / ronic + MAT_SHARE / rm)
        out["mat"].append((label, rm, eff, run_case(path, [(c["ronic"], str(eff))], [c["vps"]])[0]))
    return out
