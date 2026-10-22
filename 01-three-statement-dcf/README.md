# Granite Construction: three-statement model and DCF

<!-- Executive summary goes here once the valuation is done. -->

## Question

<!-- ALI: why I chose Granite and what I want to find out -->

## Data

All financial statement figures come from Granite's 10-K and 10-Q filings on [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000861459&type=10-K). I read them from the inline XBRL tags in each filing, so every number in the model can be traced to a tag and an accession number. `data/SOURCES.md` has the details.

The history starts in **FY2021**, not earlier. Granite restated FY2017 and FY2018 (and the quarters of 2018 and 2019) in its FY2019 10-K, after an Audit Committee investigation found that Heavy Civil project forecasts had been too optimistic. FY2019 and FY2020 were filed while the control weaknesses behind that restatement were still open, so I didn't want to build forecasts on them. FY2021 is the first year with effective controls.

That leaves five years of history (FY2021 to FY2025) plus H1 2026. Before building anything I checked that my condensed statements add up to every subtotal in the filings and agree with the SEC's companyfacts API. All 149 checks matched exactly.

## Methodology

<!-- To be written as the model is built. -->

## Key results

<!-- To be written. -->

## Interpretation

<!-- ALI: my view, to be written after the valuation -->

## Limitations and what I'd do next

- **Short history.** Five years is less than a full construction cycle, and FY2021 to FY2025 covers the ramp-up in federal infrastructure spending. Average margins and working-capital days from this window may not be normal levels, so the forecast leans on them less than it otherwise would.
- **Restatement history.** The 2017 to 2019 restatement and the 2022 tax-related weakness are a reminder that a contractor's reported margins depend on project cost estimates. The model can't test those estimates; it takes the audited figures as given.

## How to reproduce

```
cd 01-three-statement-dcf
python -m src.run
```

This downloads the filings (needs `SEC_EMAIL` and `FRED_API_KEY` in the repo's `.env`), rebuilds the statements in `data/processed/`, prints the reconciliation and writes `model/granite_model.xlsx`. The last step opens the workbook in Excel to recalculate it and check for formula errors, so it needs Excel on Windows.
