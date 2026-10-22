# Assumptions memo (draft)

Working document for the forecast. Each assumption gets a source, a reason and a note on what happens if it's wrong. Numbers in the history tables come from `outputs/tables/history_ratios.csv` and `history_segments.csv`, built by `src/analysis/history.py`.

Status: sections 1 to 7 drafted. Sections 5 to 7 are written from my own views (given 22 Oct 2026) and get re-checked against the Q3 2026 results on 29 Oct. Sections 8 and 9 follow.

## 1. Valuation date and balance sheet

- **Balance sheet:** 30 September 2026, from the Q3 2026 10-Q. This is the first balance sheet after the 2028 convertible notes were settled (12 Aug 2026), so net debt and the share count won't need a manual adjustment.
- **Filing date:** Granite has announced it will release Q3 2026 results before the market opens on Thursday 29 October 2026. In 2023 to 2025 the 10-Q was filed the same day as the earnings release.
- **Share price:** closing price on the day the 10-Q appears on EDGAR (expected 29 Oct 2026). That's the first close that reflects the new balance sheet. If the 10-Q comes later than the release, I use the close on the 10-Q filing date.
- **Forecast years:** FY2026E to FY2030E. FY2026E is a full-year forecast checked against 9M 2026 actuals and guidance. Cash flows are discounted from the valuation date with a mid-year convention, and Q4 2026 is treated as a stub period.

## 2. What the history says

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Revenue (USD m) | 3,502 | 3,301 | 3,509 | 4,008 | 4,424 |
| Revenue growth | | -5.7% | 6.3% | 14.2% | 10.4% |
| Gross margin | 10.4% | 11.2% | 11.3% | 14.3% | 16.1% |
| SG&A % revenue | 8.7% | 8.3% | 8.4% | 8.3% | 9.2% |
| EBIT margin | 0.7% | 2.6% | 2.3% | 5.2% | 6.4% |
| EBIT + D&A margin | 3.8% | 5.1% | 4.9% | 8.3% | 10.1% |
| Capex % revenue | 2.7% | 3.7% | 4.0% | 3.4% | 3.1% |
| D&A % revenue | 3.1% | 2.5% | 2.6% | 3.2% | 3.7% |
| CFO % revenue | 0.6% | 1.7% | 5.2% | 11.4% | 10.6% |
| Backlog / revenue | 0.74 | 0.87 | 1.03 | 0.89 | 0.93 |

By segment:

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Construction revenue growth | | -8.9% | 6.7% | 14.1% | 7.0% |
| Construction gross margin | 9.9% | 10.8% | 10.9% | 14.4% | 15.7% |
| Materials revenue growth | | 16.8% | 3.9% | 14.6% | 29.9% |
| Materials gross margin | 14.0% | 13.2% | 13.8% | 13.8% | 17.8% |
| Materials share of revenue | 12.2% | 15.1% | 14.7% | 14.8% | 17.4% |

Working capital (year-end balances over full-year revenue or cost of revenue):

| Days | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Receivables (revenue) | 48 | 51 | 62 | 47 | 52 |
| Contract assets (revenue) | 15 | 27 | 27 | 30 | 20 |
| Inventories (cost of revenue) | 7 | 11 | 12 | 11 | 14 |
| Accounts payable (cost of revenue) | 38 | 42 | 48 | 43 | 42 |
| Contract liabilities (revenue) | 21 | 19 | 25 | 27 | 27 |
| Accrued and other (revenue) | 47 | 32 | 35 | 30 | 29 |
| Trade working capital % revenue | -8.7% | -0.1% | -0.7% | -2.1% | -2.2% |
| Retention receivable % revenue | 3.7% | 4.9% | 4.6% | 4.7% | 3.7% |

Things worth noting before forming a view:
- **Acquisitions:** part of the recent growth was bought. In FY2025, acquired businesses (Warren Paving, Papich, Cinderlite) added USD 112.1m of construction revenue and USD 106.4m of materials revenue (FY2025 10-K, MD&A). Without them, FY2025 growth would have been about 5% rather than 10.4%. For H1 2026, the Q2 earnings release gives USD 142m (construction) and USD 110m (materials) from acquired businesses, which leaves organic growth of roughly 16% against H1 2025. These are my calculations from the company's disclosures.
- **FY2021 accrued liabilities** include the USD 129m legal settlement accrual, which reversed in FY2022. That's why FY2021 working capital looks so negative.
- **Year-end vs mid-year:** working capital is seasonal. At 30 June 2026, receivables were USD 887m against USD 630m at December 2025. Year-end days are the consistent basis for an annual model.

## 3. Management guidance for FY2026

From the Q2 2026 earnings release (8-K, 30 Jul 2026, accession 0000861459-26-000027, Exhibit 99.1):
- Revenue USD 5.3bn to 5.5bn (raised from 5.2bn to 5.4bn), which implies growth of 19.8% to 24.3% over FY2025.
- Adjusted EBITDA margin 12.25% to 13.25%.
- SG&A 8.25% to 8.75% of revenue, including about USD 48m of stock-based compensation.
- Effective tax rate on adjusted net income "in the mid-20s".
- Capex about USD 140m to 160m, including about USD 50m of strategic materials investments.

Adjusted EBITDA is Granite's own non-GAAP measure, so it isn't directly comparable with my EBIT + D&A margin (10.1% in FY2025). Before using the guidance I'll reconcile the two from the non-GAAP tables in the release.

## 4. Treatment of acquisitions

The forecast includes acquisitions that have closed by the valuation date: Kenny Seng was bought in H1 2026, and its results will be in the Q3 10-Q. It does not include future, unannounced acquisitions. Bought growth costs cash, and if I modelled the growth without the purchase price the valuation would be too high. If Granite keeps buying, that's upside or downside depending on the price paid, not something the DCF should assume.

## 5. Revenue growth

I forecast Construction and Materials separately, because their margins differ and Materials has grown from 12% to 17% of revenue.

**FY2026E: USD 5.3bn, the low end of guidance.** Granite raised its range in July, but the restatement came from optimistic project forecasts, so I take the bottom of the range rather than the midpoint. That is still growth of 19.8% over FY2025, and it includes the acquisitions closed in 2025 and 2026. I re-check this against 9M 2026 actuals on 29 Oct. The segment split also waits for the 9M figures. In H1 2026 Materials was 16.7% of revenue, but H1 is the weak season for materials.

**FY2027E to FY2030E: organic growth only, fading to 4% by FY2030.** After FY2026 there are no further acquisitions unless I model one explicitly, with its price (section 4). Growth fades in a straight line from the FY2026 organic rate to 4% in FY2030. I chose 4% as a rough long-run US nominal GDP growth rate, and it will be sourced in step 5 alongside the terminal growth rate. The FY2026 organic rate needs the acquired-revenue figure for 9M 2026, which comes with the Q3 release. In H1 2026 organic growth was about 16%.

**Federal funding (IIJA).** IIJA authorised federal highway programmes through federal fiscal year 2026, which ended on 30 Sep 2026. Current status:
- Congress extended the programmes to 11 Dec 2026 through the Surface Transportation Extension Act of 2026, which is Division C of H.R. 6500 and became P.L. 119-103 (enrolled bill text, Sec. 3001 and 3002(2); CRS R48845, p. 4). The bill was signed into law on 2 Sep 2026 (White House statement).
- The House reauthorisation bill, the BUILD America 250 Act (H.R. 8870), was ordered to be reported by the committee in May 2026. CRS says it would raise assured annual highway funding by 7% over the IIJA (CRS R48845, p. 2).
- I found no Senate bill and no enacted multi-year reauthorisation as of 22 Oct 2026.
- None of the last five highway acts was replaced on time; each time Congress used short extensions (CRS R48845, p. 4). So a late reauthorisation is the usual pattern, not an unusual one. What hurts contractors is a long gap, when states hold back new work.

So the base case assumes reauthorisation passes without a long gap, and the downside case covers a gap lasting through FY2027. Sources are in `data/SOURCES.md`.

**Downside case: reauthorisation late (agreed 22 Oct).** If the programme runs on short extensions through FY2027, state DOTs tend to hold back new lettings because they can't plan multi-year work. I model this as no Construction growth in FY2027, with the fade path then starting one year later. Materials growth is unchanged in this case, because about half of materials revenue goes to third parties. The exact mechanics are open for review.

## 6. Margins

**Gross margin.** Part of the FY2025 margin was one-off. Granite's Note 3 lists projects where estimate revisions moved gross profit by USD 5m or more. It doesn't separate claim settlements from other upward revisions, but it gives a range:

| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Upward revisions (USD m) | 8.1 | 25.6 | 64.9 |
| Downward revisions (USD m) | -96.9 | -50.2 | -33.5 |
| Net, % of revenue | -2.5% | -0.6% | +0.7% |

- FY2025 gross margin was 16.1%.
- Removing the net revisions gives 15.4%.
- Removing all upward revisions, as if none of them recur, gives 14.6%. On the same basis Construction alone falls from 15.7% to 13.9%.
- The MD&A says FY2025 had "more net increases from revisions in estimates due to claim settlements than in the prior year".
- The Q2 2026 10-Q says H1 2026 margin fell year on year "primarily due to a reduction in the favorable impact of claim settlements".

Projects below USD 5m aren't disclosed, so this is a partial view.

| Case | Gross margin |
|---|---|
| Base | 14.5% from FY2027 (agreed 22 Oct), slightly below FY2025 and between the two adjusted FY2025 figures above. FY2026E uses the 9M actual margin. |
| Upside | 16%, the FY2025 level, held. |

Segment margins follow from the total, with Materials kept above Construction as in every year since FY2021 except FY2024. The exact segment margins are set after Q3.

**SG&A.** I use guidance for FY2026E: 8.25% to 8.75% of revenue, including about USD 48m of stock-based compensation. After that, SG&A is held as a percentage of revenue.

**Stock-based compensation is a real cost.** It stays in SG&A and isn't added back to free cash flow. The equity value is then divided by today's diluted share count, without adding shares for future grants. Expensing SBC and also adding future dilution would count the same cost twice.

## 7. Working capital

My view, from progress-payment work: when a contractor takes on more projects, cash gets tighter, not looser. Retention builds up on every running job and only comes back at completion, and work often runs ahead of approved progress payments. So I don't expect the slightly negative working capital of FY2024-25 (about -2% of revenue) to hold while Granite grows.

**Days.** Starting days are FY2022-25 averages. FY2021 is left out because of the USD 129m legal settlement accrual. Retention is a separate line, taken out of receivables.

| Line | FY2022-25 average | Basis |
|---|---|---|
| Receivables excl. retention | 36.7 days | revenue |
| Retention receivable | 4.5% | revenue |
| Contract assets | 25.9 days | revenue |
| Inventories | 12.1 days | cost of revenue |
| Accounts payable | 43.8 days | cost of revenue |
| Contract liabilities | 24.7 days | revenue |
| Accrued and other liabilities | 31.3 days | revenue |

At a 14.5% gross margin these averages imply trade working capital of about **-1.1% of revenue**. That's already less negative than the -2.2% at the end of FY2025.

**Path to 0%.** FY2026E uses the averages. Retention stays at its average 4.5% of revenue: that already ties up more cash every year as revenue grows, so I don't push it higher as well. The rest of the move to 0% goes through contract assets, which is work done ahead of approved progress payments. They rise in a straight line from 25.9 days in FY2026E to 30.0 days in FY2030E (26.9, 27.9, 29.0 in between). All other days stay at their averages. 30 days isn't outside Granite's own range: contract assets were 29.9 days at the end of FY2024.

Moving from -2.2% (FY2025 actual) to about -1.1% (FY2026E) is a cash outflow of roughly 1% of revenue in FY2026. The Q3 balance sheet will show whether that is already happening; at 30 June it is distorted by seasonality.

## 8. Capex, D&A and tax

To follow once growth is set, since capex and D&A scale with the size of the business.

## 9. Cost of capital

Base case uses Damodaran's bottom-up beta for the relevant industry group(s), relevered at Granite's market debt-to-equity. A regression beta from weekly returns against the S&P 500 is shown only as a cross-check. Details to follow in step 5.
