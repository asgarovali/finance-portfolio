"""Committed and Awarded Projects (CAP), Granite's backlog measure, from the MD&A.

CAP isn't tagged in XBRL, so it's read from the text of each 10-K and 10-Q
(the table "Unearned revenue / Other awards / Total"). Only the unearned
revenue part is a GAAP number (remaining performance obligations), and that
part is checked against the XBRL tag. Each date is taken from the latest filing
that shows it, as for the statements.

Run from the project folder:  python -m src.data.extract_cap
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SEC_DIR = ROOT / "data" / "raw" / "sec"
PROCESSED = ROOT / "data" / "processed"

# From the FY2021 10-K on, all CAP sits in the Construction segment. Earlier
# filings split it across the old Transportation/Water/Specialty segments.
FIRST_REPORT_DATE = "2021-12-31"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def _text(path: Path) -> str:
    t = re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8", errors="ignore"))
    return re.sub(r"\s+", " ", html.unescape(t).replace("\xa0", " "))


def _numbers(s: str) -> list[float]:
    return [float(x.replace(",", "")) / 1000 for x in re.findall(r"\$ ?([\d,]{4,})", s)]


def parse_cap(text: str) -> pd.DataFrame:
    """The CAP-by-component table of one filing, in USD m, one row per date."""
    m = re.search(r"Unearned revenue (\$ ?[\d,]+.*?)Other awards (.*?)Total (\$ ?[\d,]+.*?)(?=\(|[A-Z][a-z])", text)
    if not m:
        return pd.DataFrame()
    unearned = _numbers(m.group(1))
    total = _numbers(m.group(3))
    # other awards has no $ sign after the first column
    other = [float(x.replace(",", "")) / 1000 for x in re.findall(r"([\d,]{5,})", m.group(2))]
    header = text[max(0, m.start() - 250):m.start()]
    n = len(total)
    tenk = re.search(rf"({MONTHS}) (\d{{1,2}}), (\d{{4}}) (\d{{4}}) (?:\(1\) )?\(dollars", header)
    if tenk:  # 10-K layout: "December 31, 2025 2024"
        dates = [f"{tenk.group(1)} {tenk.group(2)}, {y}" for y in (tenk.group(3), tenk.group(4))]
    else:
        dates = re.findall(rf"(?:{MONTHS}) \d{{1,2}}, \d{{4}}", header)[-n:]
    assert len(dates) == n == len(unearned) == len(other), (dates, unearned, other, total)
    return pd.DataFrame({"date": pd.to_datetime(dates), "unearned_revenue": unearned,
                         "other_awards": other, "cap": total})


def main() -> pd.DataFrame:
    index = pd.read_csv(PROCESSED / "filings_index.csv")
    index = index[index["form"].isin(["10-K", "10-Q"]) & (index["reportDate"] >= FIRST_REPORT_DATE)]
    rows = []
    for f in index.itertuples():
        t = parse_cap(_text(SEC_DIR / f"{f.accessionNumber}_{f.primaryDocument}"))
        rows.append(t.assign(form=f.form, accession=f.accessionNumber, filed=f.filingDate))
    cap = (pd.concat(rows).sort_values("filed").groupby("date").last().reset_index())
    for c in ("unearned_revenue", "other_awards", "cap"):
        cap[c] = cap[c].round(3)
    # the parts must add up, and unearned revenue must equal the XBRL backlog (RPO) where I have it
    assert ((cap["unearned_revenue"] + cap["other_awards"] - cap["cap"]).abs() < 0.002).all()
    memo = pd.read_csv(PROCESSED / "memo.csv", index_col=0).loc["Backlog (RPO)"].dropna()
    ends = {"FY2021": "2021-12-31", "FY2022": "2022-12-31", "FY2023": "2023-12-31", "FY2024": "2024-12-31",
            "FY2025": "2025-12-31", "H1 2026": "2026-06-30"}
    for period, rpo in memo.items():
        u = cap.loc[cap["date"] == ends[period], "unearned_revenue"].iloc[0]
        assert abs(u - rpo) < 0.002, f"{period}: CAP unearned revenue {u} vs RPO {rpo}"
    cap.to_csv(PROCESSED / "cap.csv", index=False, date_format="%Y-%m-%d")
    print(f"CAP: {len(cap)} quarter-ends; unearned revenue matches the XBRL RPO at {len(memo)} dates")
    return cap


if __name__ == "__main__":
    main()
