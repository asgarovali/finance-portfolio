"""Build condensed IS, BS and CF for FY2021-FY2025 and H1 2025/H1 2026.

Values come from the iXBRL facts in each filing. For every period I take all
numbers from the single latest filing that presents that period on its face
statements, so a restated or recast year is never mixed with original figures.

Sign convention: each line is stored with the sign it has in the statement's
arithmetic (costs, cash outflows negative), so totals are plain sums. The
filed subtotals are kept next to my computed ones for the reconciliation.

Run from the project folder:  python -m src.data.clean_statements
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from src.data.ixbrl import read_facts

ROOT = Path(__file__).resolve().parents[2]
SEC_DIR = ROOT / "data" / "raw" / "sec"
PROCESSED = ROOT / "data" / "processed"

FIRST_FY, LAST_FY = 2021, 2025
H1_YEARS = (2025, 2026)
H1_10Q_PERIOD = "2026-06-30"


@dataclass
class Row:
    label: str
    tags: list[str] = field(default_factory=list)  # alternatives, first one found is used
    sign: int = 1
    parts: list[str] | None = None                 # set for subtotals
    check: str | None = None                       # filed tag the subtotal must match


def item(label, tags, sign=1):
    return Row(label, tags if isinstance(tags, list) else [tags], sign)


def total(label, parts, check=None):
    return Row(label, parts=parts, check=check)


G, C = "us-gaap:", "gva:"

IS_ROWS = [
    item("Revenue", [G + "RevenueFromContractWithCustomerExcludingAssessedTax",
                     G + "RevenueFromContractWithCustomerIncludingAssessedTax"]),
    item("Cost of revenue", G + "CostOfGoodsAndServicesSold", -1),
    total("Gross profit", ["Revenue", "Cost of revenue"], G + "GrossProfit"),
    item("SG&A", G + "SellingGeneralAndAdministrativeExpense", -1),
    item("Other costs, net", G + "OtherOperatingIncomeExpenseNet"),
    item("Gain on sale of PP&E", [G + "GainLossOnDispositionOfAssets1",
                                  G + "GainLossOnSaleOfPropertyPlantEquipment"]),
    item("Impairment charges", G + "AssetImpairmentCharges", -1),
    total("Operating income", ["Gross profit", "SG&A", "Other costs, net",
                               "Gain on sale of PP&E", "Impairment charges"], G + "OperatingIncomeLoss"),
    # FY2023-24: repurchases of the 2024 convertibles; H1 2026: conversion option remeasurement
    item("Loss on convertible debt transactions", G + "GainsLossesOnExtinguishmentOfDebt"),
    item("Interest income", G + "InvestmentIncomeInterest"),
    item("Interest expense", [G + "InterestExpenseNonoperating", G + "InterestExpense"], -1),
    item("Equity income of affiliates", G + "IncomeLossFromEquityMethodInvestments"),
    item("Other income, net", G + "OtherNonoperatingIncomeExpense"),
    total("Pre-tax income", ["Operating income", "Loss on convertible debt transactions", "Interest income",
                             "Interest expense", "Equity income of affiliates", "Other income, net"],
          G + "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"),
    item("Income tax", G + "IncomeTaxExpenseBenefit", -1),
    total("Net income incl. NCI", ["Pre-tax income", "Income tax"], G + "ProfitLoss"),
    item("Non-controlling interests", G + "NetIncomeLossAttributableToNoncontrollingInterest", -1),
    total("Net income to Granite", ["Net income incl. NCI", "Non-controlling interests"], G + "NetIncomeLoss"),
]

BS_ROWS = [
    item("Cash and cash equivalents", G + "CashAndCashEquivalentsAtCarryingValue"),
    item("Marketable securities, current", G + "MarketableSecuritiesCurrent"),
    item("Receivables, net", G + "ReceivablesNetCurrent"),
    item("Contract assets", [G + "ContractWithCustomerAssetNet", G + "ContractWithCustomerAssetNetCurrent"]),
    item("Inventories", G + "InventoryNet"),
    item("Equity in construction JVs", C + "EquityInConstructionJointVenturesCurrentAssets"),
    item("Other current assets", G + "OtherAssetsCurrent"),
    item("Current assets held for sale", G + "AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent"),
    total("Total current assets", ["Cash and cash equivalents", "Marketable securities, current",
                                   "Receivables, net", "Contract assets", "Inventories",
                                   "Equity in construction JVs", "Other current assets",
                                   "Current assets held for sale"], G + "AssetsCurrent"),
    item("PP&E, net", G + "PropertyPlantAndEquipmentNet"),
    item("Marketable securities, long-term", G + "HeldToMaturitySecuritiesNoncurrent"),
    item("Investments in affiliates", G + "InvestmentsInAffiliatesSubsidiariesAssociatesAndJointVentures"),
    item("Goodwill", G + "Goodwill"),
    item("Intangible assets", G + "IntangibleAssetsNetExcludingGoodwill"),
    item("Right of use assets", G + "OperatingLeaseRightOfUseAsset"),
    item("Deferred tax assets", G + "DeferredIncomeTaxAssetsNet"),
    item("Other noncurrent assets", G + "OtherAssetsNoncurrent"),
    total("Total assets", ["Total current assets", "PP&E, net", "Marketable securities, long-term",
                           "Investments in affiliates", "Goodwill", "Intangible assets",
                           "Right of use assets", "Deferred tax assets", "Other noncurrent assets"],
          G + "Assets"),
    item("Current debt", G + "LongTermDebtCurrent"),
    item("Accounts payable", G + "AccountsPayableCurrent"),
    item("Contract liabilities", [G + "ContractWithCustomerLiabilityCurrent", G + "ContractWithCustomerLiability"]),
    item("Conversion option derivative", G + "DerivativeLiabilitiesCurrent"),
    item("Accrued and other current liabilities", C + "AccruedExpensesAndOtherCurrentLiabilities"),
    item("Current liabilities held for sale", G + "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent"),
    total("Total current liabilities", ["Current debt", "Accounts payable", "Contract liabilities",
                                        "Conversion option derivative", "Accrued and other current liabilities",
                                        "Current liabilities held for sale"], G + "LiabilitiesCurrent"),
    item("Long-term debt", G + "LongTermDebtNoncurrent"),
    item("Long-term lease liabilities", G + "OperatingLeaseLiabilityNoncurrent"),
    item("Deferred tax liabilities", G + "DeferredIncomeTaxLiabilitiesNet"),
    item("Other long-term liabilities", G + "OtherLiabilitiesNoncurrent"),
    total("Total liabilities", ["Total current liabilities", "Long-term debt", "Long-term lease liabilities",
                                "Deferred tax liabilities", "Other long-term liabilities"]),
    item("Common stock", G + "CommonStockValue"),
    item("Additional paid-in capital", G + "AdditionalPaidInCapitalCommonStock"),
    item("AOCI", G + "AccumulatedOtherComprehensiveIncomeLossNetOfTax"),
    item("Retained earnings", G + "RetainedEarningsAccumulatedDeficit"),
    total("Granite shareholders' equity", ["Common stock", "Additional paid-in capital", "AOCI",
                                           "Retained earnings"], G + "StockholdersEquity"),
    item("Non-controlling interests", G + "MinorityInterest"),
    total("Total equity", ["Granite shareholders' equity", "Non-controlling interests"],
          G + "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
    total("Total liabilities and equity", ["Total liabilities", "Total equity"],
          G + "LiabilitiesAndStockholdersEquity"),
]

CF_ROWS = [
    item("Net income incl. NCI", G + "ProfitLoss"),
    item("D&A", G + "DepreciationDepletionAndAmortization"),
    item("Stock-based compensation", G + "ShareBasedCompensation"),
    item("Deferred income taxes", G + "DeferredIncomeTaxExpenseBenefit"),
    item("Gain on sale of PP&E", G + "GainLossOnSaleOfPropertyPlantEquipment", -1),
    item("Amortisation of debt costs", [G + "AmortizationOfFinancingCostsAndDiscounts", G + "AmortizationOfFinancingCosts"]),
    item("Amortisation of convertible discount", G + "AmortizationOfDebtDiscountPremium"),
    item("Non-cash loss on debt extinguishment", C + "GainLossOnExtinguishmentOfDebtNonCash", -1),
    item("Loss on conversion option derivative", G + "DerivativeLossOnDerivative"),
    item("Convertible inducement expense", G + "InducedConversionOfConvertibleDebtExpense"),
    item("Impairment charges", G + "AssetImpairmentCharges"),
    item("Construction JV (income) loss", C + "UnconsolidatedConstructionJointVentureNetIncomeLoss"),
    item("Income from affiliates", [G + "IncomeLossFromEquityMethodInvestments",
                                    C + "CompanyOwnedLifeInsuranceNetIncomeLoss"], -1),
    item("Other non-cash items", G + "OtherNoncashIncomeExpense", -1),
    item("Change in receivables", G + "IncreaseDecreaseInReceivables", -1),
    item("Change in contract assets", G + "IncreaseDecreaseInContractWithCustomerAsset", -1),
    item("Change in inventories", G + "IncreaseDecreaseInInventories", -1),
    item("Contributions to construction JVs", C + "EquityInConstructionJointVentures", -1),
    item("Distributions from construction JVs", G + "EquityMethodInvestmentDividendsOrDistributions"),
    item("Change in other assets", G + "IncreaseDecreaseInOtherOperatingAssets", -1),
    item("Change in accounts payable", G + "IncreaseDecreaseInAccountsPayable"),
    item("Change in accrued and other liabilities", G + "IncreaseDecreaseInOtherAccountsPayableAndAccruedLiabilities"),
    item("Legal settlement deposit", C + "IncreaseDecreaseInInsuranceReceivableForLegalSettlement", -1),
    item("Legal settlement accrual", C + "IncreaseDecreaseInAccrualForLegalSettlement"),
    total("Cash from operations", ["Net income incl. NCI", "D&A", "Stock-based compensation",
                                   "Deferred income taxes", "Gain on sale of PP&E",
                                   "Amortisation of debt costs", "Amortisation of convertible discount",
                                   "Non-cash loss on debt extinguishment", "Loss on conversion option derivative",
                                   "Convertible inducement expense",
                                   "Impairment charges", "Construction JV (income) loss",
                                   "Income from affiliates", "Other non-cash items", "Change in receivables",
                                   "Change in contract assets", "Change in inventories",
                                   "Contributions to construction JVs", "Distributions from construction JVs",
                                   "Change in other assets", "Change in accounts payable",
                                   "Change in accrued and other liabilities", "Legal settlement deposit",
                                   "Legal settlement accrual"],
          G + "NetCashProvidedByUsedInOperatingActivities"),
    item("Capex", G + "PaymentsToAcquirePropertyPlantAndEquipment", -1),
    item("Proceeds from sale of PP&E", G + "ProceedsFromSaleOfPropertyPlantAndEquipment"),
    item("Acquisitions", [G + "PaymentsToAcquireBusinessesGross", G + "PaymentsToAcquireBusinessesNetOfCashAcquired"], -1),
    item("Acquisition price adjustments", G + "PaymentsForProceedsFromPreviousAcquisition", -1),
    item("Proceeds from sale of business", G + "ProceedsFromDivestitureOfBusinessesNetOfCashDivested"),
    item("Purchases of marketable securities", G + "PaymentsToAcquireMarketableSecurities", -1),
    item("Maturities of marketable securities", G + "ProceedsFromSaleAndMaturityOfHeldToMaturitySecurities"),
    item("Called marketable securities", G + "ProceedsFromSaleAndMaturityOfMarketableSecurities"),
    item("Notes receivable issued", C + "PaymentsForProceedsFromNotesReceivableNetOfCollections", -1),
    item("Notes receivable collected", G + "ProceedsFromCollectionOfNotesReceivable"),
    item("Life insurance proceeds", G + "ProceedsFromLifeInsurancePolicies"),
    item("Other investing", G + "PaymentsForProceedsFromOtherInvestingActivities", -1),
    total("Cash from investing", ["Capex", "Proceeds from sale of PP&E", "Acquisitions",
                                  "Acquisition price adjustments", "Proceeds from sale of business",
                                  "Purchases of marketable securities", "Maturities of marketable securities",
                                  "Called marketable securities", "Notes receivable issued",
                                  "Notes receivable collected", "Life insurance proceeds", "Other investing"],
          G + "NetCashProvidedByUsedInInvestingActivities"),
    item("Convertible notes issued", G + "ProceedsFromConvertibleDebt"),
    item("Other debt issued", [G + "ProceedsFromLongTermLinesOfCredit", G + "ProceedsFromIssuanceOfLongTermDebt"]),
    item("Debt repaid", G + "RepaymentsOfLongTermDebt", -1),
    item("Capped calls", C + "PaymentsForCappedCallTransaction", -1),
    item("Capped call unwind", C + "ProceedsFromPartialUnwindOfCappedCall"),
    item("Warrants redeemed", G + "PaymentsForRepurchaseOfWarrants", -1),
    item("Debt issuance costs", G + "PaymentsOfDebtIssuanceCosts", -1),
    item("Dividends paid", G + "PaymentsOfDividendsCommonStock", -1),
    item("Share repurchases", G + "PaymentsForRepurchaseOfCommonStock", -1),
    item("NCI contributions", G + "ProceedsFromMinorityShareholders"),
    item("NCI distributions", C + "DistributionsToNoncontrollingPartnersNet", -1),
    item("Other financing", G + "ProceedsFromPaymentsForOtherFinancingActivities"),
    total("Cash from financing", ["Convertible notes issued", "Other debt issued", "Debt repaid", "Capped calls", "Capped call unwind",
                                  "Warrants redeemed", "Debt issuance costs", "Dividends paid",
                                  "Share repurchases", "NCI contributions", "NCI distributions",
                                  "Other financing"],
          G + "NetCashProvidedByUsedInFinancingActivities"),
    total("Net change in cash", ["Cash from operations", "Cash from investing", "Cash from financing"],
          G + "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect"),
]

# lines kept for the model that aren't part of any statement's arithmetic
MEMO_TAGS = {
    "Diluted shares (m)": G + "WeightedAverageNumberOfDilutedSharesOutstanding",
    "Basic shares (m)": G + "WeightedAverageNumberOfSharesOutstandingBasic",
    "Diluted EPS (USD)": G + "EarningsPerShareDiluted",
    "Retention receivable": C + "ContractWithCustomerRetention",
    "Backlog (RPO)": G + "RevenueRemainingPerformanceObligation",
}

STATEMENTS = {"IS": IS_ROWS, "BS": BS_ROWS, "CF": CF_ROWS}
# a tag that only appears on that statement, used to find which filing presents a period
ANCHOR = {"IS": G + "ProfitLoss", "CF": G + "NetCashProvidedByUsedInOperatingActivities",
          "BS": G + "LiabilitiesAndStockholdersEquity"}


def periods() -> dict[str, tuple[str | None, str]]:
    """Column label -> (start, end). start is None for balance sheet dates."""
    out = {f"FY{y}": (f"{y}-01-01", f"{y}-12-31") for y in range(FIRST_FY, LAST_FY + 1)}
    out.update({f"H1 {y}": (f"{y}-01-01", f"{y}-06-30") for y in H1_YEARS})
    return out


def load_facts(index: pd.DataFrame) -> pd.DataFrame:
    """Facts from the 10-Ks for FY2021 onwards and the Q2 2026 10-Q."""
    keep = index[((index["form"] == "10-K") & (index["reportDate"] >= f"{FIRST_FY}-12-31"))
                 | ((index["form"] == "10-Q") & (index["reportDate"] == H1_10Q_PERIOD))]
    frames = []
    for f in keep.itertuples():
        df = read_facts(SEC_DIR / f"{f.accessionNumber}_{f.primaryDocument}")
        frames.append(df.assign(accession=f.accessionNumber, form=f.form, filed=f.filingDate))
    return pd.concat(frames, ignore_index=True)


def _source_filing(facts: pd.DataFrame, stmt: str, start: str | None, end: str) -> str | None:
    """Accession of the latest filing that shows this period on the given statement."""
    f = facts[(facts["tag"] == ANCHOR[stmt]) & (facts["dims"] == "") & (facts["end"] == end)]
    f = f[f["start"].isna()] if start is None else f[f["start"] == start]
    if f.empty:
        return None
    return f.sort_values("filed")["accession"].iloc[-1]


def build(facts: pd.DataFrame) -> pd.DataFrame:
    """Long table: statement, line, period, value (USD m), filed subtotal, tag, accession."""
    plain = facts[facts["dims"] == ""]
    out = []
    for stmt, rows in STATEMENTS.items():
        for col, (start, end) in periods().items():
            s = None if stmt == "BS" else start
            acc = _source_filing(facts, stmt, s, end)
            if acc is None:
                continue  # e.g. no June 2025 balance sheet in the Q2 2026 10-Q
            f = plain[(plain["accession"] == acc) & (plain["end"] == end)]
            f = f[f["start"].isna()] if s is None else f[f["start"] == s]
            vals = f.set_index("tag")["value"]

            computed: dict[str, float] = {}
            for r in rows:
                if r.parts is None:
                    tag = next((t for t in r.tags if t in vals.index), None)
                    v = r.sign * vals[tag] / 1e6 if tag else 0.0
                    filed = None
                else:
                    tag = r.check
                    v = sum(computed[p] for p in r.parts)
                    filed = vals[r.check] / 1e6 if r.check in vals.index else None
                computed[r.label] = v
                out.append(dict(statement=stmt, line=r.label, period=col, value=v,
                                filed_total=filed, is_total=r.parts is not None,
                                tag=tag, accession=acc))
            # memo lines from the same filing
            if stmt in ("IS", "BS"):
                for label, tag in MEMO_TAGS.items():
                    is_flow = tag.endswith(("Outstanding", "Diluted"))
                    if (stmt == "IS") == is_flow and tag in vals.index:
                        scale = 1 if label.endswith("(USD)") else 1e6
                        out.append(dict(statement="Memo", line=label, period=col, value=vals[tag] / scale,
                                        filed_total=None, is_total=False, tag=tag, accession=acc))
    return pd.DataFrame(out)


def wide(long: pd.DataFrame, stmt: str) -> pd.DataFrame:
    df = long[long["statement"] == stmt]
    order = list(dict.fromkeys(df["line"]))
    cols = [c for c in periods() if c in set(df["period"])]
    return df.pivot(index="line", columns="period", values="value").loc[order, cols]


def main() -> None:
    index = pd.read_csv(PROCESSED / "filings_index.csv")
    facts = load_facts(index)
    facts.to_csv(PROCESSED / "facts.csv", index=False)

    long = build(facts)
    long.to_csv(PROCESSED / "statements_long.csv", index=False)
    for stmt in ("IS", "BS", "CF", "Memo"):
        wide(long, stmt).round(3).to_csv(PROCESSED / f"{stmt.lower()}.csv")
    print(f"{len(facts)} facts from {facts['accession'].nunique()} filings; "
          f"statements saved to {PROCESSED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
