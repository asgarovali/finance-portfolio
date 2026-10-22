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
}


def main() -> None:
    for name in DAMODARAN_FILES:
        path = download(DAMODARAN_URL.format(name=name), RAW / "damodaran" / f"{name}.xls")
        print(f"saved {path.relative_to(ROOT)}")
    path = fred_series("DGS10", RAW / "fred")
    print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
