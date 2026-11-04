"""Download Granite Construction's SEC data: XBRL facts, filing history and
the annual/quarterly report documents.

Raw files go to data/raw/ untouched. The only thing written to
data/processed/ is a list of the 10-K, 10-K/A and 10-Q filings, so the
later steps (and SOURCES.md) can point to exact accession numbers.

Run from the project folder:  python -m src.data.download_sec
Add --refresh to fetch the facts and filing list again after a new filing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

from common.data import sec_company_facts, sec_filing_doc, sec_submissions

CIK = 861459  # GRANITE CONSTRUCTION INC, from sec.gov/files/company_tickers.json
FIRST_YEAR = 2018  # filing date cut-off; early enough to see the restatement filings

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
SEC_DIR = RAW / "sec"
PROCESSED = ROOT / "data" / "processed"

FORMS = ("10-K", "10-K/A", "10-Q", "10-Q/A")

# 8-K documents quoted in the assumptions memo
EXTRA_DOCS = [
    ("0000861459-26-000027", "gva-20260630xexx991.htm"),  # Q2 2026 earnings release, FY2026 guidance
    ("0000861459-26-000036", "gva-20260811.htm"),          # settlement of the 2028 convertible notes
    ("0000861459-26-000040", "gva-20260930xexx991.htm"),   # Q3 2026 earnings release, guidance, 2029 targets
    ("0001437749-26-019166", "ex_970386.htm"),             # indenture, 6.375% senior notes due 2034
]


def filings_index(submissions_path: Path) -> pd.DataFrame:
    """Periodic reports from the submissions JSON, oldest first."""
    sub = json.loads(submissions_path.read_text())
    recent = pd.DataFrame(sub["filings"]["recent"])
    # older filings sit in extra JSON pages; GVA's recent block reaches back far
    # enough, but check so a silent gap can't slip through
    if recent["filingDate"].min() > f"{FIRST_YEAR}-01-01":
        raise RuntimeError("recent filings don't reach back to FIRST_YEAR; load the extra pages")

    cols = ["form", "filingDate", "reportDate", "accessionNumber", "primaryDocument"]
    df = recent.loc[recent["form"].isin(FORMS), cols]
    df = df[df["filingDate"] >= f"{FIRST_YEAR}-01-01"]
    return df.sort_values("filingDate").reset_index(drop=True)


def main(refresh: bool = False) -> None:
    facts = sec_company_facts(CIK, RAW, refresh)
    subs = sec_submissions(CIK, RAW, refresh)
    print(f"saved {facts.name} and {subs.name}")

    idx = filings_index(subs)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    idx.to_csv(PROCESSED / "filings_index.csv", index=False)
    print(f"{len(idx)} periodic filings since {FIRST_YEAR}:")
    print(idx["form"].value_counts().to_string())

    for row in idx.itertuples():
        sec_filing_doc(CIK, row.accessionNumber, row.primaryDocument, SEC_DIR)
    for accession, document in EXTRA_DOCS:
        sec_filing_doc(CIK, accession, document, SEC_DIR)
    print(f"documents saved to {SEC_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main(refresh="--refresh" in sys.argv)
