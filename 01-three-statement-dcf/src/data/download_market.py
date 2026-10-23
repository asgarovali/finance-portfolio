"""Download cost-of-capital inputs: Damodaran datasets and the US 10-year yield.

Damodaran overwrites these files on his site when he updates them, so the
copy in data/raw/damodaran/ is the version the model uses. Check the
"Date updated" cell before refreshing.

Run from the project folder:  python -m src.data.download_market
"""
from __future__ import annotations

from pathlib import Path

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
}
# monthly implied ERP, start of each month since Sep 2008
ERP_MONTHLY_URL = "https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPbymonth.xlsx"
# DGS10: 10-year Treasury yield. GDPC1MDLR / PCECTPIMDLR: FOMC median longer-run
# projections of real GDP growth and PCE inflation (source for long-run growth)
FRED_SERIES = ["DGS10", "GDPC1MDLR", "PCECTPIMDLR"]


def main() -> None:
    for name in DAMODARAN_FILES:
        path = download(DAMODARAN_URL.format(name=name), RAW / "damodaran" / f"{name}.xls")
        print(f"saved {path.relative_to(ROOT)}")
    path = download(ERP_MONTHLY_URL, RAW / "damodaran" / "ERPbymonth.xlsx")
    print(f"saved {path.relative_to(ROOT)}")
    for series in FRED_SERIES:
        path = fred_series(series, RAW / "fred")
        print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
