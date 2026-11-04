"""Charts for the README and the summary report, read from the recalculated workbook.

Run from the project folder (after the model is built):  python -m src.viz.charts
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook

from common.style import GREY, PALETTE, add_source, save, use_style

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "model" / "granite_model.xlsx"
FIG = ROOT / "outputs" / "figures"
TABLES = ROOT / "outputs" / "tables"
HIST = [f"FY{y}" for y in range(2021, 2026)]
FCST = [f"FY{y}E" for y in range(2026, 2031)]
SRC = "Source: Granite 10-K/10-Q filings (SEC EDGAR); forecast from model/granite_model.xlsx"


def _rows(ws) -> dict[str, int]:
    return {ws.cell(row=r, column=1).value: r for r in range(1, ws.max_row + 1)}


def load() -> dict:
    wb = load_workbook(MODEL, data_only=True)
    is_, sch, dcf, sens = wb["IS"], wb["Sched"], wb["DCF"], wb["Sens"]
    I, S, D, N = _rows(is_), _rows(sch), _rows(dcf), _rows(sens)
    hist = lambda k, r: [is_.cell(row=r[k], column=c).value for c in range(2, 7)]
    fc = lambda k: [sch.cell(row=S[k], column=c).value for c in range(7, 12)]
    rev = hist("Revenue", I) + fc("Revenue")
    gp_h = hist("Gross profit", I)
    ebitda_h = hist("EBITDA (operating income + D&A)", I)
    sv = lambda k, col="B": sens[f"{col}{N[k]}"].value
    dv = lambda k, col="B": dcf[f"{col}{D[k]}"].value
    # WACC x g and WACC x multiple tables: centre +/- one step on each axis
    start = N["Value per share: WACC x long-run growth (Gordon)"]
    g_grid = [[sens.cell(row=r, column=c).value for c in range(3, 7)] for r in range(start + 2, start + 7)]
    start = N["Value per share: WACC x exit multiple (EV/EBITDA on FY2030E)"]
    x_grid = [[sens.cell(row=r, column=c).value for c in range(3, 8)] for r in range(start + 2, start + 7)]
    px = pd.read_csv(ROOT / "data" / "raw" / "market" / "gva_yfinance.csv", index_col="Date")["Close"]
    year = px.loc["2025-10-30":"2026-10-29"]
    return {
        "years": HIST + FCST, "rev": rev,
        "gm": [g / r for g, r in zip(gp_h, rev[:5])] + fc("Gross margin"),
        "em": [e / r for e, r in zip(ebitda_h, rev[:5])] + fc("EBITDA margin"),
        "fcff": [dv("FCFF", c) for c in "BCDEFG"],
        "base": dv("Value per share (USD)"), "exit": dv("Value per share (USD)", "C"),
        "price": dv("Share price (USD)"),
        "down": sv("Downside: no Construction growth in FY2027E, gross margin 14.5%"),
        "up": sv("Upside: gross margin implied by FY2026 guidance"),
        "mgmt": [sv(k, "E") for k in ("Low end", "Midpoint", "High end")],
        "g_range": (min(min(r[1:4]) for r in g_grid[1:4]), max(max(r[1:4]) for r in g_grid[1:4])),
        "x_range": (min(r[4] for r in x_grid[1:4]), max(r[4] for r in x_grid[1:4])),
        "wk52": (year.min(), year.max()),
    }


def revenue_margins(d: dict) -> Path:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True, gridspec_kw={"height_ratios": [3, 2]})
    x = range(len(d["years"]))
    ax1.bar(x[:5], [r / 1000 for r in d["rev"][:5]], color=PALETTE[0], label="Reported")
    ax1.bar(x[5:], [r / 1000 for r in d["rev"][5:]], color=PALETTE[0], alpha=0.45, label="Forecast (base case)")
    ax1.set_ylabel("Revenue (USD bn)")
    ax1.set_title("Revenue and margins, FY2021-FY2030E")
    ax1.legend(loc="upper left")
    ax2.plot(x, [m * 100 for m in d["gm"]], marker="o", label="Gross margin")
    ax2.plot(x, [m * 100 for m in d["em"]], marker="o", label="EBITDA margin (operating income + D&A)")
    ax2.axvline(4.5, color=GREY, linewidth=0.8, linestyle="--")
    ax2.set_ylabel("% of revenue")
    ax2.set_xticks(list(x), d["years"], rotation=0, fontsize=8)
    ax2.legend(loc="lower right", fontsize=8)
    add_source(fig, SRC + ". Dashed line: last reported year.")
    p = save(fig, "revenue_margins", FIG)
    plt.close(fig)
    return p


def fcff(d: dict) -> Path:
    fig, ax = plt.subplots()
    labels = ["Q4 2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "Terminal\n(FY2031E)"]
    colors = [PALETTE[0]] * 5 + [GREY]
    bars = ax.bar(labels, d["fcff"], color=colors)
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in d["fcff"]], fontsize=8, padding=2)
    ax.set_ylabel("FCFF (USD m)")
    ax.set_title("Free cash flow to the firm, base case")
    add_source(fig, SRC + ". Q4 2026E = FY2026E less 9M 2026 actual; terminal year reinvests g / RONIC of NOPAT.")
    p = save(fig, "fcff", FIG)
    plt.close(fig)
    return p


def football_field(d: dict) -> Path:
    rows = [
        ("52-week trading range (closes)", *d["wk52"], None),
        ("Exit multiple, 17.1x FY2030E EBITDA\n(WACC +/- 0.5 pt)", *d["x_range"], d["exit"]),
        ("Management 2029 targets\n(low end to high end)", d["mgmt"][0], d["mgmt"][2], d["mgmt"][1]),
        ("DCF scenarios\n(downside to upside)", d["down"], d["up"], d["base"]),
        ("DCF base, Gordon growth\n(WACC and g +/- 0.5 pt)", *d["g_range"], d["base"]),
    ]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for i, (label, lo, hi, mid) in enumerate(rows):
        ax.barh(i, hi - lo, left=lo, color=PALETTE[0] if i else GREY, alpha=0.8 if i else 0.6, height=0.5)
        ax.text(lo - 2, i, f"{lo:.0f}", ha="right", va="center", fontsize=8)
        ax.text(hi + 2, i, f"{hi:.0f}", ha="left", va="center", fontsize=8)
        if mid is not None:
            ax.plot([mid, mid], [i - 0.25, i + 0.25], color="white", linewidth=2)
    ax.axvline(d["price"], color=PALETTE[1], linewidth=1.5)
    ax.text(d["price"], len(rows) - 0.4, f"Price 29 Oct 2026: {d['price']:.2f}", color=PALETTE[1], fontsize=8, ha="center")
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=8)
    ax.set_xlabel("Value per share (USD)")
    ax.set_xlim(0, max(r[2] for r in rows) * 1.12)
    ax.grid(axis="y", visible=False)
    ax.set_title("Valuation summary")
    add_source(fig, "Source: model/granite_model.xlsx (DCF and Sens sheets); prices from yfinance (Yahoo Finance), "
                    "retrieved 2026-11-04. White marks: base or midpoint.")
    p = save(fig, "football_field", FIG)
    plt.close(fig)
    return p


def main() -> None:
    use_style()
    plt.rcParams["axes.axisbelow"] = True  # gridlines behind the bars
    d = load()
    TABLES.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        ("DCF base (Gordon)", d["base"]), ("DCF downside", d["down"]), ("DCF upside", d["up"]),
        ("Management targets, low", d["mgmt"][0]), ("Management targets, midpoint", d["mgmt"][1]),
        ("Management targets, high", d["mgmt"][2]), ("Exit multiple 17.1x", d["exit"]),
        ("52-week low", d["wk52"][0]), ("52-week high", d["wk52"][1]), ("Share price 29 Oct 2026", d["price"]),
    ], columns=["item", "usd_per_share"]).round(2).to_csv(TABLES / "valuation_summary.csv", index=False)
    for f in (revenue_margins, fcff, football_field):
        print(f"saved {f(d).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
