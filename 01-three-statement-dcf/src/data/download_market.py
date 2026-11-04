"""Download market inputs: Damodaran datasets, FRED series and the GVA share price.

Damodaran overwrites these files on his site when he updates them, so the
copy in data/raw/damodaran/ is the version the model uses. Check the
"Date updated" cell before refreshing.

Run from the project folder:  python -m src.data.download_market
Add --refresh to fetch the FRED series again (the Damodaran files are left as they are).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from common.data import download, fred_series

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

DAMODARAN_URL = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/{name}.xls"
DAMODARAN_FILES = {
    "betas": "US industry betas, unlevered and cash-corrected",
    "histimpl": "historical implied equity risk premiums",
    "ratings": "synthetic ratings: interest coverage to rating to default spread",
    "indname": "list of companies in each industry",
    "psdata": "price and enterprise value to sales by industry (segment value weights)",
    "vebitda": "EV/EBITDA and EV/EBIT by industry (exit multiple)",
    "EVA": "return on capital and cost of capital by industry (Materials RONIC benchmark)",
}
# monthly implied ERP, start of each month since Sep 2008
ERP_MONTHLY_URL = "https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPbymonth.xlsx"
# DGS10: 10-year Treasury yield. GDPC1MDLR / PCECTPIMDLR: FOMC median longer-run
# projections of real GDP growth and PCE inflation (source for long-run growth). SOFR: term loan and revolver rate
FRED_SERIES = ["DGS10", "GDPC1MDLR", "PCECTPIMDLR", "SOFR"]
# daily GVA prices; a fixed window so a re-run gives the same file (52-week range kept for the comps project)
PRICE_TICKER, PRICE_START, PRICE_END = "GVA", "2025-10-01", "2026-11-04"


def gva_prices(refresh: bool = False) -> Path:
    """Daily prices from yfinance (unofficial Yahoo Finance API), unadjusted closes."""
    dest = RAW / "market" / "gva_yfinance.csv"
    if dest.exists() and not refresh:
        return dest
    h = yf.Ticker(PRICE_TICKER).history(start=PRICE_START, end=PRICE_END, auto_adjust=False)
    dest.parent.mkdir(parents=True, exist_ok=True)
    h.index = h.index.strftime("%Y-%m-%d")
    h.to_csv(dest, index_label="Date")
    meta = {"source": "yfinance Ticker.history", "ticker": PRICE_TICKER, "start": PRICE_START, "end": PRICE_END,
            "auto_adjust": False,
            "retrieved_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
    dest.with_name(dest.name + ".meta.json").write_text(json.dumps(meta, indent=2))
    return dest


def main(refresh: bool = False) -> None:
    for name in DAMODARAN_FILES:
        path = download(DAMODARAN_URL.format(name=name), RAW / "damodaran" / f"{name}.xls")
        print(f"saved {path.relative_to(ROOT)}")
    path = download(ERP_MONTHLY_URL, RAW / "damodaran" / "ERPbymonth.xlsx")
    print(f"saved {path.relative_to(ROOT)}")
    for series in FRED_SERIES:
        path = fred_series(series, RAW / "fred", refresh)
        print(f"saved {path.relative_to(ROOT)}")
    print(f"saved {gva_prices().relative_to(ROOT)}")


if __name__ == "__main__":
    main(refresh="--refresh" in sys.argv)
