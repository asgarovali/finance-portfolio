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
| `raw/damodaran/ratings.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/ratings.xls | interest coverage to rating to default spread | |
| `raw/damodaran/indname.xls` | https://pages.stern.nyu.edu/~adamodar/pc/datasets/indname.xls | companies in each industry | 22 MB, not committed; re-download with the script |
| `raw/fred/fred_DGS10.json` | FRED API, series DGS10 (10-year Treasury constant maturity) | daily yields | last observation 2026-10-20: 5.12% |

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
