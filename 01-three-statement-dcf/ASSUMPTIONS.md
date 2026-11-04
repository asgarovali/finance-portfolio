# Assumptions memo (draft)

Working document for the forecast. Each assumption gets a source, a reason and a note on what happens if it's wrong. Numbers in the history tables come from `outputs/tables/history_ratios.csv` and `history_segments.csv`, built by `src/analysis/history.py`.

Status: sections 1 to 7 agreed (from my own views, 22 Oct 2026), to be re-checked against the Q3 2026 results on 29 Oct. The FY2027 growth anchor on backlog (section 5) is agreed; its numbers are final after Q3. The smaller-lines rules (section 6) are agreed and built in. Section 8 agreed, including the terminal RONIC (9.7%) and the sales-to-capital ratio excluding goodwill (3.87). Section 9 (cost of capital) and section 10 (DCF) are built. The valuation date (29 Oct 2026), the risk-free rate and the cost of debt are set; the share price, diluted shares, debt, cash and the other Q3 balances are still pending.

## 1. Valuation date and balance sheet

- **Balance sheet:** 30 September 2026, from the Q3 2026 10-Q. This is the first balance sheet after the 2028 convertible notes were settled (12 Aug 2026), so net debt and the share count won't need a manual adjustment.
- **Filing date:** Granite has announced it will release Q3 2026 results before the market opens on Thursday 29 October 2026. In 2023 to 2025 the 10-Q was filed the same day as the earnings release.
- **Share price:** closing price on the day the 10-Q appears on EDGAR (expected 29 Oct 2026). That's the first close that reflects the new balance sheet. If the 10-Q comes later than the release, I use the close on the 10-Q filing date.
- **What happened:** the Q3 10-Q (accession 0000861459-26-000042) has an EDGAR filing date of 29 Oct 2026. It was accepted at 17:14 New York time, after the close. The earnings 8-K (0000861459-26-000040) was accepted at 06:45, before the open, and its press release already had the full 30 Sep balance sheet. So the 29 Oct close reflects the new balance sheet, and the valuation date is **29 Oct 2026**.
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

**FY2027E to FY2030E: organic growth only, fading to 4% by FY2030.** After FY2026 there are no further acquisitions unless I model one explicitly, with its price (section 4). 4% is long-run US nominal GDP growth: the Fed's September 2026 projections put longer-run real growth at 2.0% and inflation at 2.0%, which gives 4.04% (section 9).

**FY2027E starting point: backlog, not H1 growth (proposed 22 Oct).** My first version started the fade from H1 2026 organic growth (15.9%). That's one half-year in a strong period. Backlog is a better anchor for a contractor, because most of next year's construction revenue is work already won.

Granite's backlog measure is CAP (committed and awarded projects): signed contracts not yet performed (unearned revenue, the GAAP backlog) plus contracts awarded but not yet signed (other awards). All of it is in the Construction segment. Source: the MD&A of each 10-K and 10-Q, read by `src/data/extract_cap.py`.

| USD m | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 30 Jun 2026 |
|---|---|---|---|---|---|---|
| CAP at year-end | 4,010 | 4,485 | 5,546 | 5,296 | 6,969 | 7,419 |
| Growth | | 11.8% | 23.6% | -4.5% | 31.6% | 6.5% (6 months) |
| of which unearned revenue | 2,595 | 2,877 | 3,597 | 3,584 | 4,123 | 5,056 |
| CAP at 30 Sep | 4,328 | 4,078 | 5,585 | 5,620 | 6,338 | |
| Construction revenue | 3,076 | 2,804 | 2,992 | 3,415 | 3,655 | |
| Next year's Construction revenue / CAP at 30 Sep | 0.648 | 0.734 | 0.612 | 0.650 | 0.697 (FY2026E) | |
| Same, excluding revenue from businesses acquired that year | | 0.734 | 0.612 | 0.630 | | |

How I use it: FY2027E Construction revenue = CAP at 30 Sep 2026 × the average share of September CAP that turned into the next year's Construction revenue over FY2023-25 (0.659, using the second ratio row). September is used because it's the last backlog figure before the valuation date, and the ratio is measured on the same date each year. FY2022 is left out because the Inliner business (USD 199m of CAP) was sold in Q1 2022. Until the Q3 10-Q is out, the model uses CAP at 30 June 2026 (USD 7,419m). In past years September CAP was within about 5% of June CAP.

With the June figure this gives FY2027E Construction growth of **10.6%** (USD 7,419m × 0.659 = USD 4,885m, against USD 4,417m in FY2026E). Growth then fades in a straight line to 4% in FY2030E (8.4%, 6.2%, 4.0%).

**Acquired revenue taken out of the ratio (agreed 22 Oct).** FY2025 Construction revenue includes USD 112.1m from Warren Paving and Papich, bought in 2025 (FY2025 10-K, MD&A). That work was never in Granite's September 2024 backlog, so it inflates the FY2025 ratio (0.650 instead of 0.630). FY2027E has no acquisitions, so the ratio should describe backlog Granite already holds turning into revenue. FY2023 and FY2024 also had smaller acquisitions (Lehman-Roberts and Memphis Stone, November 2023; Dickerson & Bowen, 2024). I haven't found a construction revenue figure for them in the filings, so those years aren't adjusted. I'd still rather remove the one distortion I can measure than keep it because the others can't be fixed. Without the adjustment the ratio would be 0.665 and growth 11.7%.

**Materials follows the same path.** Materials has no backlog of its own, and part of its output goes into Granite's own construction projects. Per the segment note (FY2025 10-K, Note 21), intersegment sales to Construction were USD 200.5m, 246.8m and 275.2m in FY2023-25, or 28%, 29% and 26% of total Materials output. So about a quarter of Materials volume moves directly with Construction. The rest goes to third parties, mostly other contractors and builders whose demand depends on the same public and private construction spending. Using one path for both segments is a simplification, but not an unreasonable one.

What this says and doesn't say:
- Backlog supports double-digit growth in FY2027. CAP has risen 40% since the end of FY2024, faster than revenue, so the anchor comes out only about 2 points below the old 12.9%. The data doesn't support a much lower base case.
- The ratio moves a lot from year to year (0.61 to 0.73). Each 0.01 changes FY2027E growth by about 1.7 points, so the full historical range gives 3% to 23%. The average is the only defensible single number, but it's a weak anchor.
- IIJA risk sits mostly outside CAP. Work in CAP is already awarded, with funding judged probable. What a reauthorisation gap hits is new lettings, including work that is won and built in the same year. That's why the downside case (0% Construction growth in FY2027) still makes sense on top of this anchor.

**Federal funding (IIJA).** IIJA authorised federal highway programmes through federal fiscal year 2026, which ended on 30 Sep 2026. Current status:
- Congress extended the programmes to 11 Dec 2026 through the Surface Transportation Extension Act of 2026, which is Division C of H.R. 6500 and became P.L. 119-103 (enrolled bill text, Sec. 3001 and 3002(2); CRS R48845, p. 4). The bill was signed into law on 2 Sep 2026 (White House statement).
- The House reauthorisation bill, the BUILD America 250 Act (H.R. 8870), was ordered to be reported by the committee in May 2026. CRS says it would raise assured annual highway funding by 7% over the IIJA (CRS R48845, p. 2).
- I found no Senate bill and no enacted multi-year reauthorisation as of 22 Oct 2026.
- None of the last five highway acts was replaced on time; each time Congress used short extensions (CRS R48845, p. 4). So a late reauthorisation is the usual pattern, not an unusual one. What hurts contractors is a long gap, when states hold back new work.

So the base case assumes reauthorisation passes without a long gap, and the downside case covers a gap lasting through FY2027. Sources are in `data/SOURCES.md`.

**Downside case: reauthorisation late (agreed 22 Oct).** If the programme runs on short extensions through FY2027, state DOTs tend to hold back new lettings because they can't plan multi-year work. I model this as no Construction growth in FY2027, with the fade path then starting one year later. Materials growth is unchanged in this case, because about three quarters of Materials output goes to third parties (intersegment sales were 26-29% of Materials output in FY2023-25, FY2025 10-K Note 21). The exact mechanics are open for review.

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

| Case | Gross margin from FY2027E |
|---|---|
| Base | **15.0%**, the midpoint of the 14.6-15.4% range above |
| Downside | 14.5%: all FY2025 upward revisions treated as one-off. Combined with the reauthorisation gap in section 5 |
| Upside | about 17.0%: management's FY2026 guidance, translated as below |

FY2026E uses the 9M actual margin once it's out (see the note on interim values below).

**Why the base case moved from 14.5% to 15.0% (22 Oct).** With 14.5% the base case stacked three conservative choices on top of each other: low-end revenue, the most conservative margin normalisation, and high-end SG&A. Each one is defensible, but together they describe a worse year than any single piece of evidence supports. 15.0% sits in the middle of the range the revision data gives, and 14.5% becomes the downside.

**Upside: management guidance.** Guidance is for adjusted EBITDA margin (12.25-13.25% for FY2026), not gross margin, so it needs translating. Using Granite's own definition (net income after the JV partners' share, plus interest, tax, D&A, stock-based compensation and "other costs, net"), I rebuilt FY2025 adjusted EBITDA from the filed lines at 11.9% of revenue, against a 16.1% gross margin, a gap of 4.2 points. For H1 2026 the same rebuild gives 10.1%, against Granite's reported 10.3%, so the definition matches. Adding the 4.2-point gap to the 12.75% guidance midpoint gives an upside gross margin of about 17.0%. This is approximate: forecast SG&A (8.75%) is lower than FY2025's 9.2%, so guidance could be met with a slightly lower gross margin. Adjusted EBITDA starts from net income after the JV partners' share, so it needs interest and NCI, which come with the debt schedule after Q3. Then I'll add an adjusted EBITDA row and check the upside against guidance directly.

**The gap to guidance that remains.** On the same translation, the base case's 15.0% gross margin gives an adjusted EBITDA margin of roughly 10.8%, still 1.5-2.5 points below FY2026 guidance. I keep that gap on purpose, because of Granite's forecasting history. The 2017-2019 restatement came from project forecasts that were too optimistic. FY2025 and H1 2026 margins were helped by claim settlements, which management itself calls out. Until margins without the claim benefits show up in the reported numbers, I don't take guidance as the central case.

Segment margins follow from the total, with Materials kept above Construction as in every year since FY2021 except FY2024. The exact segment margins are set after Q3.

**Interim values until Q3.** The FY2026E gross margin (14.7%) and Materials share (16.7%) in the model are H1 2026 actuals, and CAP is the 30 June figure, used as placeholders until the 9M figures come out on 29 Oct. H1 margins are seasonally low for road construction: paving and highway work is concentrated in the warmer months. The filings show this. H1 2026 gross margin was 14.7%, but Q2 alone was 16.4%; H1 2025 was 15.5%, against 16.1% for the full year 2025. So the FY2026E placeholder understates the full year.

**SG&A: 8.75% of revenue in FY2026E, the top of guidance** (8.25% to 8.75%, including about USD 48m of stock-based compensation). Much of SG&A is fixed: offices, management, systems. If revenue comes in at the low end of guidance, as I assume, the same cost base is a larger share of it, so the ratio sits at the high end. That's consistent with the revenue choice, not just extra caution. After FY2026 SG&A is held at 8.75% of revenue.

**Smaller lines (agreed 22 Oct, in the model).** Simple rules, each calculated in the workbook from the filed history. Interest income and the NCI share are used once cash and interest are forecast after Q3.

| Line | FY2022 | FY2023 | FY2024 | FY2025 | Proposed rule |
|---|---|---|---|---|---|
| Other costs, net, % revenue | -0.73% | -1.43% | -1.00% | -0.94% | FY2022-25 average, -1.02% |
| Gain on sale of PP&E, % revenue | 0.38% | 0.81% | 0.22% | 0.46% | FY2022-25 average, 0.47% |
| Proceeds from PP&E sales, % revenue (cash flow) | 0.79% | 1.09% | 0.35% | 0.74% | FY2022-25 average, 0.74% |
| Equity income of affiliates, % revenue | 0.41% | 0.73% | 0.42% | 0.34% | FY2022-25 average, 0.48% |
| Other income, net, % revenue | -0.03% | 0.17% | 0.11% | 0.27% | FY2022-25 average, 0.13% |
| Interest income / average cash and securities | 1.69% | 4.31% | 4.69% | 4.35% | FY2025 yield, 4.35%, on forecast cash |
| Interest expense / average debt | 4.02% | 3.92% | 4.19% | 4.54% | not history: contractual rates of the debt at 30 Sep 2026 (Q3 10-Q) |
| NCI share of pre-tax income | -4.8% | -23.4% | 7.2% | 9.5% | FY2024-25 average, 8.3% |

Notes on the rules:
- **Gains and proceeds together.** Granite sells used equipment every year, so the gain is part of normal operating income. I model the gain on the income statement and the cash proceeds in investing cash flow, both at their averages. The difference (about 0.27% of revenue) is the book value of what's sold, which comes off PP&E. If I modelled only the gain, operating income and cash flow wouldn't match.
- **Interest income** uses the FY2025 yield, not the four-year average, because 2022 rates were near zero and don't describe today.
- **Interest expense.** The 2026 refinancing replaced most of the old debt: 6.375% senior notes, a term loan swapped to a fixed rate, and the settlement of the 2028 convertibles. Past ratios don't describe the new debt, so the rate per instrument comes from the Q3 10-Q debt note.
- **Non-controlling interests.** The four-year average (-2.9%) is meaningless: in FY2022-23 the consolidated JVs made losses, so the partners' share was negative. FY2024-25 (8.3%) is a better guide. H1 2026 was higher (14.6% excluding the convertible loss), so 8.3% may be on the low side.
- Equity income of affiliates and other income are non-operating. They stay below operating income and out of FCFF; affiliates are valued separately in the equity bridge (step 6).

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

**Depreciation and depletion: 3.3% of revenue.** This is the FY2025 level, excluding intangible amortisation. It rose from 2.6% (FY2023) and 2.8% (FY2024) because the 2025 acquisitions added a lot of quarry and plant assets. Net PP&E went from USD 716m to USD 1,261m in one year. An FY2022-25 average would understate depreciation on today's asset base, so I don't use it here. H1 2026 total D&A was 3.8% of revenue, which is consistent with this.

**Intangible amortisation: Granite's own schedule.** The FY2025 10-K gives expected amortisation of USD 21.6m, 13.2m, 13.0m, 13.0m and 13.0m for 2026 to 2030. Kenny Seng (bought in 2026) will add some, so I update this from the Q3 10-Q. It's a non-cash charge with no effect on FCFF apart from tax.

**Capex**
- FY2026E: USD 150m, the midpoint of guidance (USD 140m to 160m, including about USD 50m of strategic materials investment). That's 2.8% of USD 5.3bn.
- FY2027E-30E: driven by a sales-to-capital ratio, so invested capital grows with revenue (agreed 22 Oct). My first version (3.5% of revenue) let revenue grow 38% while capital stayed flat, which only works if the new revenue needs no new capital.

Each year, net investment = increase in revenue / sales-to-capital. Net investment covers both net capex and the increase in working capital, because the invested capital the ratio is measured on includes working capital. Working capital is already modelled from the days in section 7, so net capex is what's left, and nothing is counted twice:

> capex = depreciation + book value of equipment sold + increase in revenue / sales-to-capital - increase in working capital

The book value of equipment sold (proceeds minus gain, section 6) is in there because selling equipment shrinks the capital base, and it has to be replaced for capital to keep growing with revenue. In cash terms it nets out: the sale proceeds come back in investing cash flow.

The ratio comes from Granite's FY2022-25 history (revenue / year-end invested capital). **I use the version excluding goodwill and acquired intangibles (3.87, agreed 22 Oct)**, because organic growth doesn't create goodwill. FY2025 shows why it matters: the 2025 acquisitions added goodwill and intangibles, and the ratio including them fell to 2.32. For the same reason capex replaces depreciation only, not intangible amortisation: amortisation runs off intangibles bought with acquisitions, and organic growth doesn't renew them.

| Sales-to-capital | FY2022 | FY2023 | FY2024 | FY2025 | Average |
|---|---|---|---|---|---|
| Including goodwill and intangibles | 3.61 | 2.86 | 3.25 | 2.32 | 3.01 |
| Excluding goodwill and intangibles | 3.97 | 3.67 | 4.50 | 3.33 | 3.87 |

The resulting path in the base case, with FY2027E growth anchored on backlog (section 5). USD m:

| | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E | Terminal |
|---|---|---|---|---|---|---|
| Increase in revenue | | 563 | 493 | 395 | 270 | |
| Net investment (÷ 3.87) | | 146 | 128 | 102 | 70 | |
| of which increase in working capital | 37 | 11 | 13 | 16 | 18 | 0 |
| of which net capex | | 134 | 114 | 86 | 51 | |
| Depreciation | 177 | 196 | 212 | 226 | 235 | |
| Book value of equipment sold | 15 | 16 | 18 | 19 | 19 | |
| Capex | 150 | 347 | 344 | 330 | 305 | 407 |
| Capex % revenue | 2.8% | 5.9% | 5.4% | 4.9% | 4.3% | 5.6% |
| ROIC on opening capital | 11.3% | 12.2% | 12.5% | 12.6% | 12.6% | |
| FCFF | 242 | 118 | 157 | 199 | 243 | 183 |

FCFF includes the smaller operating lines from section 6 (other costs, gains and proceeds from equipment sales). Interest, affiliates and other income are outside FCFF. Historical capex is gross too: FY2021-25 proceeds from equipment sales were shown separately in investing cash flow, as here.

FY2027E capex (5.9% of revenue) is still well above anything in Granite's FY2021-25 history (2.7-4.0%). I haven't smoothed it. It's what 10.6% organic growth costs at Granite's historical capital intensity. Granite's recent growth was partly bought, and an acquisition shows up as an acquisition, not as capex. The real lever is the growth rate, not the capex rule.

One consequence to be aware of: because net investment in total is set by the ratio, the working-capital days in section 7 only decide how it splits between capex and working capital. From FY2027E on they don't change FCFF. The alternative would be a ratio on fixed capital only (revenue / invested capital excluding goodwill, intangibles and trade working capital, FY2022-25 average 3.69), with working capital added on top. That would cost about USD 15-20m a year more in reinvestment, so I've kept the simpler version.

**Terminal year: reinvestment consistent with growth.** A business can only grow forever at rate g if it reinvests enough to fund that growth. The reinvestment rate, as a share of after-tax operating profit (NOPAT), has to be:

> reinvestment rate = g / RONIC

RONIC is the return earned on new capital. Net reinvestment is capex minus D&A plus the increase in working capital. By FY2030 trade working capital reaches 0% of revenue (section 7), so it doesn't grow after that, and all the reinvestment is net capex. So in the terminal year:

> capex = D&A + (g / RONIC) × NOPAT

Capex in the terminal year therefore comes from this formula, not from a fixed percentage of revenue. In the model the terminal year is a separate, normalised column after FY2030E (FY2030E NOPAT grown by g). I do it this way because in FY2030E itself working capital is still moving to its target, which would muddle the rule.

**Base case (agreed 22 Oct): RONIC = 9.7%, Granite's FY2022-25 average ROIC**, entered as a formula over the history (7.0%, 5.6%, 12.6% and 13.5%; `history_ratios.csv`). My first proposal was to use the model's own terminal ROIC, on the expectation that it would land near 9.7%. That expectation was wrong. With capex at 3.5% of revenue the model's ROIC climbed to 15.6%, because capital didn't grow with revenue. So the historical average is now an input in its own right.

With RONIC at 9.7% and g at 4%, the terminal reinvestment rate is 41% of NOPAT, and terminal capex is about 5.6% of revenue. That is a step up from 4.3% in FY2030E.

**Why terminal FCFF is below FY2030E.** Terminal FCFF is USD 183m, against USD 243m in FY2030E, even though NOPAT is 4% higher. The difference is the return on new capital:
- In FY2027E-30E, each extra dollar of revenue needs 1/3.87 of a dollar of capital and earns the NOPAT margin of about 4.3%. That's a return on new capital of about 16-17% (4.3% × 3.87).
- In the terminal year, new capital earns RONIC, 9.7%. To grow 4% a year at 9.7%, Granite has to reinvest 41% of NOPAT, against 19% in FY2030E.

I think the step down is right. Returns well above the cost of capital attract competition: other contractors bid more aggressively for the same public work, and margins on new contracts get pushed down. Over a long horizon, excess returns on new investment shrink, so the perpetuity shouldn't assume today's 16-17% on every new dollar. It is still one of the biggest single drivers of the value, so the RONIC sensitivities below matter.

During FY2027E-30E the model's ROIC on opening capital runs at about 12-13% (table above), above the 9.7% assumed for new capital in the terminal year. That's deliberate: by then the returns on today's business shouldn't be assumed to carry over to every new dollar invested.

Sensitivities:
- **RONIC = WACC (conservative):** growth creates no value.
- **RONIC = 13% (optimistic):** about Granite's FY2024-25 ROIC. FY2022-23 were much lower, so I don't treat 13% as normal.

**Tax rate on operating profit: 25%.** This is the 21% federal rate plus about 4% state tax. In FY2025, state tax was USD 12.3m on USD 288.8m of pre-tax income, or 4.2% (tax rate reconciliation, FY2025 10-K). Several things support it:
- Guidance is "mid-20s".
- The FY2025 effective rate was 23.7% on all pre-tax income. On income excluding the non-controlling interests' share (consolidated JV partners, who pay their own tax) it was 26.2%.
- Damodaran unlevers his betas with a 25% marginal rate, so using 25% keeps the beta and the debt tax shield consistent.

Cash taxes have been below the book charge (USD 49.0m paid against USD 68.5m in FY2025) because of deferred taxes. I don't model that gap past FY2026, which is slightly conservative.

**Non-controlling interests.** Granite consolidates some construction JVs, so its cash flows include the partners' share. FCFF is for the whole consolidated group, and the value of the NCI is deducted in the bridge from enterprise value to equity value. The method (book value of USD 42.5m, or a share of value based on income) is set in step 6.

## 9. Cost of capital

Data downloaded on 2026-10-22 and 23: Damodaran `betas.xls` and `psdata.xls` (updated 5 Jan 2026), `histimpl.xls`, `ERPbymonth.xlsx`, `ratings.xls`, `indname.xls`, and FRED DGS10, GDPC1MDLR and PCECTPIMDLR. The calculation is on the WACC sheet.

**Beta: bottom-up, weighted by segment.** Damodaran classifies Granite under Engineering/Construction. He puts the US aggregates companies (Vulcan, Martin Marietta, Knife River) under Construction Supplies, not Building Materials, so that's the right group for the Materials segment (`indname.xls`).

| Unlevered beta, corrected for cash | Jan 2026 | Average 2022-26 |
|---|---|---|
| Engineering/Construction | 1.137 | 0.978 |
| Construction Supplies | 1.047 | 1.049 |

**Base case: the 2022-26 averages (0.978 and 1.049). Sensitivity: the January 2026 values (1.137 and 1.047).** The 2026 Engineering/Construction beta is above every year from 2022 to 2025 (0.84 to 1.02), and I don't want one year's jump to drive the valuation. Granite's work is mostly public infrastructure, which is less cyclical than private construction. For Construction Supplies the choice hardly matters.

**Segment weights by estimated value, not revenue.** Aggregates businesses are worth much more per dollar of sales than contractors, so a revenue weighting would understate Materials. I estimate each segment's value as its FY2025 revenue × Damodaran's industry EV/Sales (`psdata.xls`, Jan 2026):

| | FY2025 revenue | EV/Sales | Estimated value | Weight | Unlevered beta (base) |
|---|---|---|---|---|---|
| Construction (Eng./Construction) | 3,655 | 1.74x | 6,341 | 71.8% | 0.978 |
| Materials (Construction Supplies) | 769 | 3.23x | 2,487 | 28.2% | 1.049 |
| Granite | | | | | **0.998** |

With the January 2026 betas (the sensitivity) Granite's unlevered beta is 1.111.

Materials revenue here is external revenue only. The USD 275m of materials Granite used on its own projects in FY2025 is already inside Construction revenue (it's eliminated on consolidation, Note 21), so counting it again in Materials would value the same sales twice.

**Relevering.** Levered beta = unlevered beta × (1 + (1 - 25%) × D/E), with D/E at market values on the valuation date. Damodaran's cash-corrected unlevered beta is the beta of the operating business, so I relever with gross debt and add cash separately in the equity bridge. Damodaran's industry D/E ratios (14.0% Eng./Construction, 17.6% Construction Supplies, 15.0% value-weighted) are a cross-check on Granite's own D/E, not an input. A regression beta (weekly returns against the S&P 500) is a cross-check only.

**Risk-free rate:** the 10-year Treasury yield (FRED DGS10) on the valuation date, the same day as the share price. It was 5.12% on 20 Oct 2026.

**Long-run growth below the risk-free rate.** A firm can't grow faster than the economy forever, and the risk-free rate is a rough ceiling for long-run nominal growth. The WACC sheet has a check row: it shows 0 if terminal growth (4%) is below the risk-free rate, 1 if not, and the build stops on 1. The source for 4%: the FOMC's median longer-run projections in the September 2026 Summary of Economic Projections are 2.0% real GDP growth and 2.0% PCE inflation (FRED GDPC1MDLR and PCECTPIMDLR), so (1.02 × 1.02) - 1 = 4.04%, rounded to 4.0%.

**Equity risk premium: 4.20%, Damodaran's implied ERP on 1 Oct 2026** (`ERPbymonth.xlsx`, the trailing-12-month series with sustainable payout, which is the one he quotes on his home page). At the start of 2026 it was 4.23% (`histimpl.xls`). I use the monthly figure so the ERP and the risk-free rate are both from October. His next update is on 1 Nov, after the valuation date, so 1 Oct is the latest available on 29 Oct.

**Cost of debt**
- **Main estimate: the risk-free rate on the valuation date plus the credit spread on Granite's 6.375% senior notes due 2034.** My first plan was to read the notes' yield on 29 Oct from FINRA's TRACE data. That didn't work. The notes were sold in a private Rule 144A offering (8-K, 2 Jun 2026), and FINRA's lookup needs a CUSIP or TRACE symbol. Neither the indenture nor any other EDGAR filing gives one: the form of note in the indenture leaves the CUSIP blank.
- **Using the 10-Q fair value instead.** The Q3 10-Q fair value table gives the notes a fair value of USD 579.9m against USD 600.0m principal at 30 Sep 2026, a price of 96.65. It's a Level 2 measurement, "based on the median price of the notes in an active market" (10-Q, fair value note). From that price and the indenture terms I get a yield to maturity of **6.94%**. The terms are a 6.375% coupon paid on 15 Jun and 15 Dec, 30/360, issued 2 Jun 2026 with a long first coupon on 15 Dec 2026, maturing 15 Jun 2034. The workbook computes the yield with Excel's ODDFYIELD, and the build checks it against my own Python version (`src/analysis/bond.py`).
- **Spread and cost of debt.** DGS10 on 30 Sep 2026 was 5.29%, so the spread is 1.65%. Cost of debt = DGS10 on 29 Oct (4.98%) + 1.65% = **6.63%** pre-tax, 4.97% after tax.
- **What this assumes:**
  - The fair value is a clean price (accrued interest excluded). The 10-Q doesn't say. If it included accrued interest (2.09 per 100 at 30 Sep), the yield would be 7.31% and the cost of debt about 0.37 points higher.
  - The spread didn't move between 30 Sep and 29 Oct. Treasury yields fell 0.31 points over that month. Spreads can move too, but I have no bond price for 29 Oct to check.
  - The notes have about 7.7 years left, and I measure the spread against the 10-year yield. With an upward-sloping curve this slightly overstates the spread over a matching Treasury. I keep DGS10 so the spread and the risk-free rate are on the same basis.
  - It's a promised yield. For a bond priced in the BB range, the expected return is a bit lower because of default risk. Like Damodaran, I don't adjust for this.
- At 30 Jun 2026 the notes had a fair value of USD 611.3m (Q2 10-Q), above par, so the price fell over the third quarter.
- Fallback and cross-check: a synthetic rating from interest coverage, using Damodaran's `ratings.xls`. Coverage is EBIT / interest expense. Damodaran has one table for firms above USD 5bn market cap and a stricter one for smaller firms, and the WACC sheet picks the table from Granite's equity value on the valuation date. The synthetic cost of debt is the risk-free rate plus the default spread for that rating. An input switch (1 = bond yield, 2 = synthetic) sets which one goes into the WACC; the base case is the bond yield.
- For now coverage uses FY2025 (operating income USD 282.4m / interest expense USD 47.2m = 6.0x). That understates the current interest bill: H1 2026 interest expense was already USD 38.1m (Q2 10-Q). At Q3 I switch to the last twelve months to September 2026, which will give lower coverage.
- The WACC sheet shows the synthetic result under both of Damodaran's tables, so the comparison is visible before the market cap is set. At 6.0x coverage it's A1/A+ (0.70%) on the large-firm table and A3/A- (0.89%) on the smaller-firm one. The bond market's 1.65% sits between Damodaran's Ba1/BB+ (1.38%) and Ba2/BB (1.84%) spreads. So the market prices Granite's debt in Damodaran's BB range, while FY2025 coverage gives an A rating. Part of the gap is that FY2025 interest expense flatters coverage (see above). The market spread is direct evidence on Granite's own debt, so it stays the base case.
- The convertible notes count as debt at their debt component. The option part goes into the diluted share count, not the cost of debt.

**Capital structure weights: Granite's own market values on the valuation date.** Equity = share price × diluted shares. Debt = senior notes and the convertibles' debt component at market value, plus the term loan at book value (it's floating-rate, swapped to fixed, so book is close to market). Lease liabilities are left out because lease costs stay in operating costs and so in FCFF; including them would count them twice. All of these come from the Q3 10-Q.

## 10. DCF and terminal value

The calculation is on the DCF sheet. Everything that needs a valuation-date input stays blank until the Q3 10-Q.

**Timing.** The balance sheet is at 30 Sep 2026, so the DCF values FCFF from 1 Oct onwards: a Q4 2026 stub, then FY2027E to FY2030E. Cash flows are discounted from the valuation date (the 10-Q filing date) with a mid-year convention: the stub at the middle of Q4, each full year at its midpoint.

**Q4 stub = FY2026E FCFF × 25.2% (92/365 days).** This ignores seasonality. Granite's operating cash flow comes mostly in the second half: in FY2025 it was USD 5.4m in H1 out of USD 468.9m for the year (Q2 2025 10-Q, FY2025 10-K). So a straight share probably understates Q4. The alternative is FY2026E FCFF minus 9M 2026 actual FCFF from the 10-Q. That needs the 9M cash flow rebuilt on the same basis as the model (with SBC as a cost and interest taken out), which I can do at Q3. <!-- ALI: keep the straight share, or switch to FY2026E minus 9M actual at Q3? -->

**Terminal value, main method: Gordon growth.** TV = terminal FCFF / (WACC − g), with g = 4% and terminal FCFF = FY2030E NOPAT × 1.04 × (1 − g / RONIC) (section 8). The formula values the FY2031E+ cash flows one year before the first of them. With mid-year timing the first one lands in mid-2031, so the value sits at mid-2030 and I discount it with the FY2030E mid-year factor. Applying the end-of-year factor instead would understate the value by about half a year of discounting.

**Exit multiple, cross-check only.** Today's multiples price today's growth, and the industry is growing well above 4% now, so a multiple applied in 2030 would assume that growth continues indefinitely. I use it to test the Gordon value, not to replace it.
- Multiple: Damodaran's EV/EBITDA (`vebitda.xls`, Jan 2026, positive-EBITDA firms): 17.18x for Engineering/Construction and 16.82x for Construction Supplies. Weighted by segment value as for the beta (28.2% Materials), this gives 17.08x.
- Weighting: value weights apply to EBITDA/EV, not EV/EBITDA, so the combined multiple is the value-weighted harmonic mean. With two multiples this close the difference is tiny, but the arithmetic mean would be wrong in general.
- EBITDA definition: Damodaran defines EBITDA as operating income plus D&A, and his EV as market cap + total debt − cash. My FY2030E EBITDA is built the same way: reported-style operating income (after SBC, other costs and gains on equipment sales) plus depreciation and amortisation. It's a trailing figure, as his is, so the multiple goes on FY2030E EBITDA for the value at the end of FY2030.
- Leases: Damodaran counts lease commitments as debt in his datasets (his 2020 data update on debt). So his multiple gives an EV that includes leases, while my FCFF keeps lease costs in operating costs and leaves leases out of debt. I subtract FY2030E lease liabilities (3.6% of revenue, the FY2025 level from the 10-K) from the multiple-based value so the two methods measure the same thing. One caveat: his lease debt is his own estimate from lease commitments, and he says it runs about 60% above the accounting figure in aggregate. I can't rebuild his number for the industry, so I use Granite's accounting liability. At about USD 250m against a terminal value of about USD 11bn, this line moves the exit-multiple value by roughly 2%.
- I couldn't confirm from his documentation whether his operating income adds back lease expense. If it does, the multiple applies to EBITDA plus rent, which for Granite is about USD 36m a year (FY2025 operating lease expense). That would raise the exit-multiple value by about 5-6%. It doesn't change the main valuation.

**Cross-check table.** It shows two things:
- the EV/EBITDA implied by the Gordon value, with leases added back so it compares with Damodaran's multiple;
- the long-run growth rate implied by the exit multiple.

The implied growth uses the same terminal rule as the model, FCFF = NOPAT × (1 + g) × (1 − g / RONIC). Setting value × (WACC − g) equal to that gives a quadratic in g; the smaller root is the answer. Holding FY2030E's reinvestment fixed instead would ignore that faster growth needs more reinvestment. The check row at the top of the sheet runs the same formula on the Gordon value and must return exactly 4.0%.

**Equity bridge (30 Sep 2026 balances).** Enterprise value
+ cash and marketable securities
+ investments in affiliates (their income is outside FCFF)
− debt at market value (the same figure as in the WACC; convertibles at principal, with the value above par in diluted shares)
− non-controlling interests at book value
= equity value, divided by diluted shares.

Equity in construction joint ventures is not added: that income is in revenue and gross profit, so it's already in FCFF. Before finalising I'll re-check the convertible treatment against the settlement terms in the Q3 10-Q.

A small timing gap remains: balances are at 30 Sep and discounting starts at the filing date about a month later. I leave it, because rolling the balance sheet forward a month would mean estimating October cash flows.

Sensitivity tables (WACC × g and WACC × exit multiple) come next, on a separate sheet.
