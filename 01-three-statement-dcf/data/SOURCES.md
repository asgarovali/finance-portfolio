# Data sources

Company: Granite Construction Incorporated (NYSE: GVA), SEC CIK 861459 (from https://www.sec.gov/files/company_tickers.json).

All SEC requests send a User-Agent with a contact email, as SEC's fair-access policy asks. SEC EDGAR data is public and free to use.

## SEC EDGAR

| Dataset | Endpoint | Saved as | Retrieved |
|---|---|---|---|
| XBRL company facts | https://data.sec.gov/api/xbrl/companyfacts/CIK0000861459.json | `raw/sec_companyfacts_0000861459.json` | 2026-10-22 |
| Filing history | https://data.sec.gov/submissions/CIK0000861459.json | `raw/sec_submissions_0000861459.json` | 2026-10-22 |
| 10-K and 10-Q documents, 2018 to Q2 2026 | https://www.sec.gov/Archives/edgar/data/861459/{accession}/{document} | `raw/sec/{accession}_{document}` | 2026-10-22 |

`processed/filings_index.csv` lists every 10-K and 10-Q used, with accession number, filing date and period end. It's built from the submissions JSON by `src/data/download_sec.py`. The filing HTML files (about 90 MB) are not committed; running the script downloads them again from the accession numbers in that index.

The exact retrieval time of each file is in the `.meta.json` file next to it.

## Restatements and recasts that affect the history

These come from the filings themselves, not from news coverage.

- **FY2017 and FY2018 were restated** in the FY2019 10-K (accession 0001437749-21-003662, filed 2021-02-22), along with Q1 to Q3 2019 and all 2018 quarters. The cause was misstated project forecasts in the Heavy Civil group, found by an Audit Committee investigation. Granite did not file a 10-K/A or amended 10-Qs; the explanatory note says the restated figures appear only in that 10-K.
- **Internal control over financial reporting was not effective** at 31 Dec 2019 and 31 Dec 2020. Management reported the weaknesses as remediated in the FY2021 10-K.
- **The Water and Mineral Services (WMS) group** was presented as discontinued operations in the FY2021 10-K. In the FY2022 10-K it was moved back to continuing operations, and prior years were conformed. The FY2021 balance sheet still shows WMS as held for sale.
- **Q1 to Q3 2022 were restated** in the FY2022 10-K (accession 0001437749-23-004014) for a tax error on the Inliner sale. A new material weakness was reported at 31 Dec 2022. The FY2022 annual figures were not restated. Controls were reported as effective again from FY2023.

For any year, I use the figure from the latest 10-K that reports it, so restated and recast numbers replace the originals.

## Which years the model uses, and why

The history is **FY2021 to FY2025**, plus H1 2025 and H1 2026 from the Q2 2026 10-Q as a check on the first forecast year.

FY2019 is technically the first year after the restated period, but FY2019 and FY2020 were reported while the control weaknesses behind the restatement were still in place. FY2021 is the first year with effective controls, and the FY2022/FY2023 10-Ks present it on today's basis (WMS in continuing operations). I keep FY2022 even though there was a year-end material weakness, because it related to tax on the Inliner sale and the annual figures were not restated.

The cost is a short history: five years, which is less than a full construction cycle and includes the post-COVID infrastructure spending ramp. Averages of margins and working-capital days over this window may not be "normal" levels. I treat this as a limitation in the README.

## How the statements are built

`src/data/clean_statements.py` reads the inline XBRL tags inside each filing (`src/data/ixbrl.py`), not the companyfacts API, because several face-statement lines use Granite's own `gva:` tags (equity in construction JVs, accrued liabilities, capped calls, NCI distributions) that companyfacts leaves out. For each period, every number is taken from the single latest filing that presents it:

| Period | Income statement and cash flow | Balance sheet |
|---|---|---|
| FY2021 | FY2023 10-K (0000861459-24-000006) | FY2022 10-K (0001437749-23-004014) |
| FY2022 | FY2024 10-K (0000861459-25-000007) | FY2023 10-K (0000861459-24-000006) |
| FY2023 to FY2025 | FY2025 10-K (0000861459-26-000004) | FY2024 / FY2025 10-K |
| H1 2025, H1 2026 | Q2 2026 10-Q (0000861459-26-000029) | 30 Jun 2026 from the same 10-Q |

Units are USD millions. Lines keep the sign they have in the statement's arithmetic (costs and cash outflows negative). Retention receivable comes from the custom tag `gva:ContractWithCustomerRetention` in the receivables note, and backlog from `RevenueRemainingPerformanceObligation`.

Processed files:
- `processed/facts.csv`: every numeric fact from the six filings used, with tag, period, dimensions and accession number
- `processed/statements_long.csv`: the condensed statements with source tag and accession for every number
- `processed/is.csv`, `bs.csv`, `cf.csv`, `memo.csv`: the same in wide format

## Reconciliation

`src/analysis/reconcile.py` checks every subtotal against the filed subtotal, the balance sheet balance, CF net income against IS net income, the net change in cash against the filed cash balances, and revenue, net income, total assets, equity, CFO and capex against the companyfacts API. On 2026-10-22 all 149 checks matched with zero difference (`outputs/tables/reconciliation.csv`).

The one visible recast: FY2021 revenue was first filed as USD 3,010.1m, with WMS in discontinued operations. The figure I use is USD 3,501.9m from the FY2023 10-K, after WMS moved back into continuing operations. FY2021 net income, total assets and CFO are unchanged (`outputs/tables/recast_fy2021_fy2022.csv`).

## Backlog (Committed and Awarded Projects)

Granite's own backlog measure, CAP, is in the MD&A of every 10-K and 10-Q but isn't tagged in XBRL. `src/data/extract_cap.py` reads the "unearned revenue / other awards / total" table from the text of each filing saved in `raw/sec/` (FY2021 10-K onwards) and writes `processed/cap.csv`, one row per quarter-end, taking each date from the latest filing that shows it. Two checks run every time: the parts add up to the total, and unearned revenue equals the XBRL tag for remaining performance obligations (`RevenueRemainingPerformanceObligation`) at all six dates where both exist. Other awards (contracts awarded but not yet signed, plus probable options) is management's number and has no GAAP equivalent.

From the FY2021 10-K on, all CAP sits in the Construction segment. Earlier filings split it across the old operating segments, so they aren't used. CAP at 31 Dec 2021 excludes USD 252.7m held for sale (FY2022 10-K, MD&A footnote).

## Events after the last annual report that matter for valuation

From the Q2 2026 10-Q, Note 9 and Note 14:
- On 19 May 2026 Granite called the remaining USD 273.7m of its 3.75% convertible notes due 2028 for redemption on 10 Aug 2026. It elected to settle conversions in cash up to USD 2,617.40 per USD 1,000 principal and in shares for any excess. That election forced the conversion option to be bifurcated as a derivative liability (USD 630.5m at 30 Jun 2026). The fair-value change runs through "loss on convertible debt transactions" (USD 369.4m in H1 2026), which is why H1 2026 shows a net loss.
- Granite issued USD 600m of 6.375% senior notes due 2034 during H1 2026.
- The settlement happened after 30 Jun 2026, so it is not in any filed balance sheet yet. The Q3 2026 10-Q had not been filed on 2026-10-22.
- 8-K filed 2026-08-13 (accession 0000861459-26-000036): on 12 Aug 2026 Granite paid about USD 715m in cash and issued 662,383 shares to settle conversions of the USD 273.7m 2028 notes. The 2028 capped calls were unwound for about USD 148m received on 11 Aug 2026. Saved in `raw/sec/`.

## Other documents

| Document | Source | Used for |
|---|---|---|
| Q2 2026 earnings release (8-K Exhibit 99.1, filed 2026-07-30, accession 0000861459-26-000027) | EDGAR, saved in `raw/sec/` | FY2026 guidance and revenue from acquired businesses |
| Q3 2026 results timing announcement (Business Wire, 2026-10-15) | Read on 2026-10-22 via https://www.stocktitan.net/news/GVA/granite-announces-timing-of-earnings-release-and-investor-conference-zivyqtefyhoz.html, because the Business Wire page wasn't reachable | Valuation date only: results before market open on 29 Oct 2026. To be confirmed by the EDGAR filing date |

## Cost of capital inputs

Downloaded by `src/data/download_market.py` on 2026-10-22. Damodaran's data is free to use with attribution (pages.stern.nyu.edu/~adamodar). He overwrites the files when he updates them, so the saved copies are the versions used.

| File | Source | Content | Version |
|---|---|---|---|
| `raw/damodaran/betas.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/betas.xls | US industry betas, unlevered and cash-corrected | "Date updated" 2026-01-05 |
| `raw/damodaran/histimpl.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/histimpl.xls | implied ERP by year | latest row: 2025 (start of 2026), 4.23% |
| `raw/damodaran/ratings.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/ratings.xls | interest coverage to rating to default spread (large-firm and smaller-firm tables, rows 19-33 and 38-52 of the first sheet) | no date in the file; downloaded 2026-10-22 |
| `raw/damodaran/indname.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/indname.xls | companies in each industry | 22 MB, not committed; re-download with the script |
| `raw/fred/fred_DGS10.json` | FRED API, series DGS10 (10-year Treasury constant maturity) | daily yields | last observation 2026-10-20: 5.12% |
| `raw/damodaran/psdata.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/psdata.xls | price and EV to sales by industry (segment value weights) | "Date updated" 2026-01-05; downloaded 2026-10-23 |
| `raw/damodaran/ERPbymonth.xlsx` | https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPbymonth.xlsx | implied ERP at the start of each month since Sep 2008 | latest row: 1 Oct 2026, 4.20% (T12m with sustainable payout); downloaded 2026-10-23 |
| `raw/fred/fred_GDPC1MDLR.json` | FRED API, series GDPC1MDLR (FOMC longer-run real GDP growth, median) | Summary of Economic Projections | latest: 2026-09-16, 2.0% |
| `raw/fred/fred_PCECTPIMDLR.json` | FRED API, series PCECTPIMDLR (FOMC longer-run PCE inflation, median) | Summary of Economic Projections | latest: 2026-09-16, 2.0% |
| `raw/damodaran/vebitda.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/vebitda.xls | EV/EBITDA and EV/EBIT by industry (exit-multiple cross-check); EV = market cap + total debt - cash | "Date updated" 2026-01-05; downloaded 2026-10-23 |

DGS10 was refreshed on 2026-11-03 (`python -m src.data.download_market --refresh`). The model looks up two dates in it: 29 Oct 2026, the valuation date (4.98%), and 30 Sep 2026, the date of the notes' fair value (5.29%). The FOMC long-run series are looked up on the 16 Sep 2026 projection date, so a later refresh can't change them.

**Cost of debt: 6.375% senior notes due 2034.** The plan was a TRACE yield from FINRA (https://www.finra.org/finra-data/fixed-income) on the valuation date. That wasn't possible. The notes are a private Rule 144A issue: the offering was announced and priced in the 8-Ks of 18 and 19 May 2026 (0001437749-26-017523, 0001437749-26-017652). It closed under the indenture filed as Exhibit 4.1 to the 8-K of 2 Jun 2026 (0001437749-26-019166). No EDGAR filing gives a CUSIP (the form of note leaves it blank), and FINRA's lookup needs one. Instead:

| Item | Source | Value |
|---|---|---|
| Fair value and carrying amount at 30 Sep 2026 | Q3 2026 10-Q (0000861459-26-000042), fair value table, XBRL us-gaap:NotesPayableFairValueDisclosure; Level 2, "based on the median price of the notes in an active market" | USD 579.888m and 600.000m |
| Coupon, dates, day count | Indenture (Exhibit 4.1 above): 6.375%, interest from 2 Jun 2026, paid 15 Jun and 15 Dec from 15 Dec 2026, 30/360, maturity 15 Jun 2034 | |
| Yield to maturity | Computed: Excel ODDFYIELD, checked against `src/analysis/bond.py` | 6.94% |

**Q3 2026 filings** (downloaded 2026-11-03 with `python -m src.data.download_sec --refresh`): 10-Q 0000861459-26-000042, filing date 29 Oct 2026, accepted 17:14 New York time; earnings 8-K 0000861459-26-000040, accepted 06:45 the same day.

## Federal highway funding (IIJA)

Used only for the downside scenario, not for any number in the base case. The statute is downloaded by script. The other pages block scripted downloads, so they were read in a browser on 2026-10-22 and saved by hand as PDFs in `raw/policy/`.

| Fact | Source |
|---|---|
| Division C of H.R. 6500 is the Surface Transportation Extension Act of 2026 (Sec. 3001), with "extension end date" 11 Dec 2026 (Sec. 3002(2)) | Enrolled bill text, govinfo.gov (U.S. Government Publishing Office): https://www.govinfo.gov/content/pkg/BILLS-119hr6500enr/html/BILLS-119hr6500enr.htm, saved as `raw/policy/BILLS-119hr6500enr.htm` by `src/data/download_policy.py`, retrieved 2026-10-22 |
| H.R. 6500, the Continuing Appropriations and Extensions Act, 2027, signed into law 2 Sep 2026 | White House statement: https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/ |
| BUILD America 250 Act (H.R. 8870) "ordered to be reported (amended) in May 2026"; would increase assured annual highway funding by 7% over the IIJA | CRS R48845 (published 8 Sep 2026), Summary, p. 2 |
| IIJA authorizations extended to 11 Dec 2026 by P.L. 119-103 | CRS R48845, notes to Table 1, p. 4 |
| ISTEA, TEA-21, SAFETEA, MAP-21 and the FAST Act all expired before the next act passed, and Congress extended the programmes each time | CRS R48845, notes to Table 1, p. 4 |

The House committee's own press release on H.R. 8870 wouldn't load in a browser (blank page), so the committee action is cited from CRS.

Files in `raw/policy/`:

| File | Document | URL |
|---|---|---|
| `BILLS-119hr6500enr.htm` | H.R. 6500 enrolled bill text (by script) | see table above |
| `fhwa_n4520297.pdf` | FHWA Notice N 4520.297, obligation limitation for the extension | https://highways.dot.gov/laws-regulations/directives/notices/n-4520297 |
| `fhwa_n4510916.pdf` | FHWA Notice N 4510.916, apportionment for the extension | https://highways.dot.gov/laws-regulations/directives/notices/n-4510916 |
| `crs_r48845.pdf` | CRS R48845, Surface Transportation Reauthorization: Federal Highway Programs (8 Sep 2026) | https://www.congress.gov/crs-product/R48845 |

## Valuation date

Balance sheet at 30 Sep 2026 from the Q3 2026 10-Q, and share price at the close on the day that 10-Q is filed on EDGAR (expected 29 Oct 2026).

Definitions used to match the exit multiple: Damodaran's variable definitions page (https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/variable.htm), where EBITDA is operating income plus D&A, and his post "Data Update 7 for 2020: Debt Delusions and Reality" (https://aswathdamodaran.blogspot.com/2020/03/data-update-7-for-2020-debt-delusions.html), which says lease commitments are counted as debt in his data. Operating lease liabilities at 31 Dec 2025 (USD 158.5m) are the XBRL tag us-gaap:OperatingLeaseLiability in the FY2025 10-K.

**Share price.** `raw/market/gva_yfinance.csv`, downloaded by `src/data/download_market.py` on 2026-11-04 with yfinance (`Ticker("GVA").history`, 1 Oct 2025 to 3 Nov 2026, unadjusted). yfinance is an unofficial wrapper around Yahoo Finance's data, so it's not a primary source. The close used is USD 121.69 on 29 Oct 2026. I checked it by hand on the Yahoo Finance historical prices page, which is the same underlying source as yfinance, so this is a transcription check rather than an independent one. Stooq, the planned second source, now blocks scripted downloads.

**Q3 2026 inputs** (10-Q 0000861459-26-000042 and earnings release 8-K 0000861459-26-000040, Exhibit 99.1):
- 9M 2025 and 9M 2026 statements: added to `data/processed/` by `clean_statements.py` (columns "9M 2025", "9M 2026"), and they reconcile to the filed subtotals.
- Two cash flow tags are new in this 10-Q: gva:GainLossOnRemeasurementOfEquityMethodInvestment (Asphalt Terminal Entity) and gva:ProceedsFromUnwindOfCappedCall.
- CAP at 30 Sep 2026: USD 7,455.5m (`extract_cap.py`).
- 3.75% convertibles discount amortisation: USD 273.7m (XBRL InterestExpenseNonoperating on the 3.75% notes member; MD&A).
- 2030 convertibles: conversion rate 12.8398 per USD 1,000 and capped call cap price USD 119.82 (debt note, text). 3.25% principal and term loan: XBRL LongTermDebt by instrument.
- Unvested RSUs, 0.501m: EPS note, text.
- Shares outstanding, 44,130,293 at 23 Oct 2026: XBRL dei:EntityCommonStockSharesOutstanding.
- Revisions in estimates for 9M 2026: Note 3, text.
- FY2026 guidance and 2029 targets: Exhibit 99.1.
