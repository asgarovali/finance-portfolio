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
