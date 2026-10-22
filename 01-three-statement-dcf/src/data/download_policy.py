"""Download the statute behind the IIJA extension (used for the downside scenario).

FHWA, congress.gov and the CRS block scripted downloads, so those documents
are saved by hand in data/raw/policy/. govinfo.gov doesn't, so the enrolled
bill text comes from there.

Run from the project folder:  python -m src.data.download_policy
"""
from __future__ import annotations

from pathlib import Path

from common.data import download

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "data" / "raw" / "policy"

# H.R. 6500 (119th Congress), enrolled: Division C is the Surface Transportation Extension Act of 2026
HR6500_URL = "https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm"


def main() -> None:
    path = download(HR6500_URL, POLICY / "BILLS-119hr6500enr.htm")
    print(f"saved {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
