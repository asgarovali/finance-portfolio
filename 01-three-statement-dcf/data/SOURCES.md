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

## Federal highway funding (IIJA): not yet verified from primary sources

Used only for the downside scenario, not for any number in the base case. The points below come from search results and the Union of Concerned Scientists blog post of 24 Sep 2026 (https://blog.ucs.org/kshen/extra-time-quiet-cuts-surface-transportation-reauthorization-extension/), read on 2026-10-22:
- Programmes extended from 30 Sep 2026 to 11 Dec 2026, a 72-day extension (Surface Transportation Extension Act of 2026, reported as P.L. 119-103, in continuing resolution H.R. 6500)
- BUILD America 250 Act (H.R. 8870) approved by the House Transportation and Infrastructure Committee on 22 May 2026; no Senate bill found

The primary sources below returned HTTP 403 to automated requests. They need to be downloaded by hand into `raw/policy/` before the memo is final:
- FHWA Notice N 4520.297 (obligation limitation for the extension): https://highways.dot.gov/laws-regulations/directives/notices/n-4520297
- FHWA Notice N 4510.916 (apportionment for the extension): https://highways.dot.gov/laws-regulations/directives/notices/n-4510916
- CRS R48845, Surface Transportation Reauthorization: Federal Highway Programs: https://www.congress.gov/crs-product/R48845

## Valuation date

Balance sheet at 30 Sep 2026 from the Q3 2026 10-Q, and share price at the close on the day that 10-Q is filed on EDGAR (expected 29 Oct 2026).
