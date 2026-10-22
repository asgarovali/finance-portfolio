"""Historical ratios that the forecast assumptions are argued from.

Run from the project folder:  python -m src.analysis.history
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"

YEARS = [f"FY{y}" for y in range(2021, 2026)]
SEGMENT_AXIS = "us-gaap:StatementBusinessSegmentsAxis="
REVENUE_TAG = "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"


def ratios(is_: pd.DataFrame, bs: pd.DataFrame, cf: pd.DataFrame, memo: pd.DataFrame) -> pd.DataFrame:
    rev = is_.loc["Revenue", YEARS]
    cogs = -is_.loc["Cost of revenue", YEARS]
    ebit = is_.loc["Operating income", YEARS]
    da = cf.loc["D&A", YEARS]
    trade_nwc = (bs.loc[["Receivables, net", "Contract assets", "Inventories"], YEARS].sum()
                 - bs.loc[["Accounts payable", "Contract liabilities",
                           "Accrued and other current liabilities"], YEARS].sum())
    out = {
        "Revenue (USD m)": rev,
        "Revenue growth": rev.pct_change(),
        "Gross margin": is_.loc["Gross profit", YEARS] / rev,
        "SG&A % revenue": -is_.loc["SG&A", YEARS] / rev,
        "EBIT margin": ebit / rev,
        "EBITDA margin (EBIT + D&A)": (ebit + da) / rev,
        "Stock-based comp % revenue": cf.loc["Stock-based compensation", YEARS] / rev,
        "D&A % revenue": da / rev,
        "Capex % revenue": -cf.loc["Capex", YEARS] / rev,
        "CFO % revenue": cf.loc["Cash from operations", YEARS] / rev,
        # year-end balances over full-year flows, so these move with seasonality and timing
        "Receivable days (revenue)": bs.loc["Receivables, net", YEARS] / rev * 365,
        "Contract asset days (revenue)": bs.loc["Contract assets", YEARS] / rev * 365,
        "Inventory days (cost of revenue)": bs.loc["Inventories", YEARS] / cogs * 365,
        "Payable days (cost of revenue)": bs.loc["Accounts payable", YEARS] / cogs * 365,
        "Contract liability days (revenue)": bs.loc["Contract liabilities", YEARS] / rev * 365,
        "Accrued and other days (revenue)": bs.loc["Accrued and other current liabilities", YEARS] / rev * 365,
        "Trade working capital % revenue": trade_nwc / rev,
        "Retention receivable % revenue": memo.loc["Retention receivable", YEARS] / rev,
        "Backlog / revenue": memo.loc["Backlog (RPO)", YEARS] / rev,
    }
    return pd.DataFrame(out).T


def segments(facts: pd.DataFrame) -> pd.DataFrame:
    """Construction and Materials revenue and gross profit (the segments since FY2022)."""
    f = facts[facts["dims"].str.startswith(SEGMENT_AXIS) & ~facts["dims"].str.contains(";")
              & facts["start"].notna()]
    f = f[(pd.to_datetime(f["end"]) - pd.to_datetime(f["start"])).dt.days > 350]
    f = f[f["tag"].isin([REVENUE_TAG, "us-gaap:GrossProfit"])]
    f = f[f["dims"].str.contains("ConstructionsMember|MaterialsMember")]
    f = f.sort_values("filed").groupby(["tag", "dims", "end"]).last().reset_index()
    f["segment"] = f["dims"].str.contains("Materials").map({True: "Materials", False: "Construction"})
    f["item"] = f["tag"].map({REVENUE_TAG: "revenue", "us-gaap:GrossProfit": "gross profit"})
    f["year"] = "FY" + f["end"].str[:4]
    t = f.pivot_table(index=["segment", "item"], columns="year", values="value") / 1e6
    t = t[[c for c in YEARS if c in t.columns]]
    for seg in ("Construction", "Materials"):
        t.loc[(seg, "gross margin"), :] = t.loc[(seg, "gross profit")] / t.loc[(seg, "revenue")]
        t.loc[(seg, "revenue growth"), :] = t.loc[(seg, "revenue")].pct_change()
    return t.sort_index()


def main() -> None:
    read = lambda name: pd.read_csv(PROCESSED / f"{name}.csv", index_col=0)
    facts = pd.read_csv(PROCESSED / "facts.csv", dtype={"dims": str}).fillna({"dims": ""})
    r = ratios(read("is"), read("bs"), read("cf"), read("memo"))
    s = segments(facts)
    TABLES.mkdir(parents=True, exist_ok=True)
    r.to_csv(TABLES / "history_ratios.csv")
    s.to_csv(TABLES / "history_segments.csv")
    print(r.round(3).to_string())
    print()
    print(s.round(3).to_string())


if __name__ == "__main__":
    main()
