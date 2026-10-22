"""Reconcile the cleaned statements with the filed figures.

Checks, for every period:
  1. each of my subtotals equals the subtotal tagged in the filing
  2. the balance sheet balances
  3. net income on the cash flow statement equals net income on the IS
  4. net change in cash equals the change in the filed cash balance
     (cash on the CF includes restricted cash and cash held for sale)
  5. headline numbers agree with the SEC companyfacts API, an independent
     extraction of the same filings
Anything over 0.5% is flagged and has to be explained in SOURCES.md.

It also prints how FY2021 and FY2022 looked when first filed vs the recast
figures I use.

Run from the project folder:  python -m src.analysis.reconcile
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"

TOLERANCE = 0.005
CASH_TAG = "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations"
API_CHECKS = {  # model line -> companyfacts tag
    ("IS", "Revenue"): "RevenueFromContractWithCustomerExcludingAssessedTax",
    ("IS", "Net income to Granite"): "NetIncomeLoss",
    ("BS", "Total assets"): "Assets",
    ("BS", "Granite shareholders' equity"): "StockholdersEquity",
    ("CF", "Cash from operations"): "NetCashProvidedByUsedInOperatingActivities",
    ("CF", "Capex"): "PaymentsToAcquirePropertyPlantAndEquipment",
}


def _row(check, period, model, filed):
    diff = model - filed
    pct = abs(diff) / abs(filed) if filed else (0.0 if abs(diff) < 1e-6 else float("inf"))
    return dict(check=check, period=period, model=round(model, 3), filed=round(filed, 3),
                diff=round(diff, 3), pct=pct, ok=pct <= TOLERANCE)


def companyfacts_value(facts: dict, tag: str, period: str) -> float | None:
    """Value from the latest 10-K in the companyfacts JSON for FYxxxx."""
    if not period.startswith("FY"):
        return None
    year = period[2:]
    units = facts["facts"]["us-gaap"].get(tag, {}).get("units", {}).get("USD", [])
    hits = [u for u in units if u["form"] == "10-K" and u["end"] == f"{year}-12-31"
            and u.get("start", f"{year}-01-01") == f"{year}-01-01"]
    if not hits:
        return None
    return max(hits, key=lambda u: u["filed"])["val"] / 1e6


def run_checks(long: pd.DataFrame, facts: pd.DataFrame, api: dict) -> pd.DataFrame:
    rows = []
    v = long.set_index(["statement", "line", "period"])["value"]

    for r in long[long["is_total"] & long["filed_total"].notna()].itertuples():
        rows.append(_row(f"{r.statement} subtotal: {r.line}", r.period, r.value, r.filed_total))

    for p in long.loc[long["statement"] == "BS", "period"].unique():
        rows.append(_row("BS balances (assets - L&E)", p,
                         v["BS", "Total assets", p] - v["BS", "Total liabilities and equity", p], 0.0))

    cf = long[long["statement"] == "CF"]
    for p in cf["period"].unique():
        rows.append(_row("CF net income = IS net income", p,
                         v["CF", "Net income incl. NCI", p], v["IS", "Net income incl. NCI", p]))

        # opening and closing cash as filed in the same filing as the CF
        acc = cf.loc[cf["period"] == p, "accession"].iloc[0]
        year = int(p[-4:])
        end = f"{year}-12-31" if p.startswith("FY") else f"{year}-06-30"
        cash = facts[(facts["accession"] == acc) & (facts["tag"] == CASH_TAG) & (facts["dims"] == "")]
        cash = cash.set_index("end")["value"] / 1e6
        if end in cash.index and f"{year - 1}-12-31" in cash.index:
            rows.append(_row("CF net change = change in cash balance", p,
                             v["CF", "Net change in cash", p], cash[end] - cash[f"{year - 1}-12-31"]))

    for (stmt, line), tag in API_CHECKS.items():
        for p in long.loc[long["statement"] == stmt, "period"].unique():
            filed = companyfacts_value(api, tag, p)
            if filed is not None:
                model = v[stmt, line, p]
                if line == "Capex":
                    model = -model  # stored as an outflow
                rows.append(_row(f"companyfacts API: {line}", p, model, filed))
    return pd.DataFrame(rows)


def recast_table(facts: pd.DataFrame, long: pd.DataFrame) -> pd.DataFrame:
    """FY2021 and FY2022 as first filed vs the figures used in the model."""
    tags = {"Revenue": "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
            "Net income to Granite": "us-gaap:NetIncomeLoss",
            "Total assets": "us-gaap:Assets",
            "Cash from operations": "us-gaap:NetCashProvidedByUsedInOperatingActivities"}
    stmt = {"Revenue": "IS", "Net income to Granite": "IS", "Total assets": "BS", "Cash from operations": "CF"}
    v = long.set_index(["statement", "line", "period"])["value"]
    plain = facts[facts["dims"] == ""]
    rows = []
    for year in (2021, 2022):
        first = plain[plain["form"] == "10-K"].sort_values("filed")
        first = first[first["end"] == f"{year}-12-31"]["accession"].iloc[0]
        for line, tag in tags.items():
            f = plain[(plain["accession"] == first) & (plain["tag"] == tag) & (plain["end"] == f"{year}-12-31")]
            if line != "Total assets":
                f = f[f["start"] == f"{year}-01-01"]
            orig = f["value"].iloc[0] / 1e6 if len(f) else float("nan")
            used = v[stmt[line], line, f"FY{year}"]
            rows.append(dict(year=f"FY{year}", line=line, first_filed=round(orig, 1), used=round(used, 1),
                             change=round(used - orig, 1), first_accession=first))
    return pd.DataFrame(rows)


def main() -> None:
    long = pd.read_csv(PROCESSED / "statements_long.csv")
    facts = pd.read_csv(PROCESSED / "facts.csv", dtype={"dims": str}).fillna({"dims": ""})
    api = json.loads((RAW / "sec_companyfacts_0000861459.json").read_text())

    checks = run_checks(long, facts, api)
    recast = recast_table(facts, long)
    TABLES.mkdir(parents=True, exist_ok=True)
    checks.to_csv(TABLES / "reconciliation.csv", index=False)
    recast.to_csv(TABLES / "recast_fy2021_fy2022.csv", index=False)

    summary = checks.assign(kind=checks["check"].str.split(":").str[0]).groupby("kind")["ok"].agg(["sum", "count"])
    print(summary.rename(columns={"sum": "passed", "count": "checks"}).to_string())
    bad = checks[~checks["ok"]]
    print(f"\n{len(bad)} check(s) over {TOLERANCE:.1%}")
    if len(bad):
        print(bad.to_string(index=False))
    print("\nFY2021-22 as first filed vs used (USD m):")
    print(recast.drop(columns="first_accession").to_string(index=False))


if __name__ == "__main__":
    main()
