# Assumptions memo (draft)

Working document for the forecast. Each assumption gets a source, a reason and a note on what happens if it's wrong. Numbers in the history tables come from `outputs/tables/history_ratios.csv` and `history_segments.csv`, built by `src/analysis/history.py`.

Status: sections 1 to 7 agreed (from my own views, 22 Oct 2026) and updated for the Q3 2026 results (10-Q filed 29 Oct). The FY2027 growth anchor on backlog (section 5) now uses CAP at 30 Sep 2026. The smaller-lines rules (section 6) are agreed and built in. Section 8 agreed, including the terminal RONIC (9.7%) and the sales-to-capital ratio excluding goodwill (3.87). Sections 9 (cost of capital) and 10 (DCF) are built with all valuation-date inputs (29 Oct 2026). Decisions of 4 Nov: base gross margin 15.5% from FY2027E, a seasonal Q4 in FY2026E, no Materials RONIC premium, management's 2029 targets as scenarios only (sections 6 and 12). Results and my interpretation are in section 11.

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

**Q3 update (8-K, 29 Oct 2026, accession 0000861459-26-000040, Exhibit 99.1).** Revenue guidance went up to USD 5.4bn to 5.5bn; everything else is unchanged, including SG&A at 8.25% to 8.75% with about USD 48m of SBC. The release also introduced **2029 targets**:
- organic revenue growth of 10% to 12% a year;
- adjusted EBITDA margin of 14% to 16%;
- SG&A of about 7.5% of revenue;
- operating cash flow of about 13% of revenue and capex of about 3%, so free cash flow of about 10% of revenue;
- continued M&A with a 2.5x net leverage target.

These targets are well above my base case (sections 5, 6 and 10). They're management targets, not guidance, and Granite gives no reconciliation of the adjusted EBITDA target to GAAP.

Adjusted EBITDA is Granite's own non-GAAP measure, so it isn't directly comparable with my EBIT + D&A margin (10.1% in FY2025). Before using the guidance I'll reconcile the two from the non-GAAP tables in the release.

## 4. Treatment of acquisitions

The forecast includes acquisitions that have closed by the valuation date. In 2026 these are Kenny Seng (23 Apr, USD 164.1m) and the remaining 50% of the Asphalt Terminal Entity (9 Sep, USD 38.3m). Together with closing adjustments, 9M 2026 cash paid for acquisitions was USD 184.3m (Q3 10-Q). It does not include future, unannounced acquisitions. Bought growth costs cash, and if I modelled the growth without the purchase price the valuation would be too high. If Granite keeps buying, that's upside or downside depending on the price paid, not something the DCF should assume.

## 5. Revenue growth

I forecast Construction and Materials separately, because their margins differ and Materials has grown from 12% to 17% of revenue.

**FY2026E: USD 5.4bn, the low end of guidance.** Granite raised the bottom of its range from 5.3bn to 5.4bn on 29 Oct. The restatement came from optimistic project forecasts, so I keep taking the bottom of the range rather than the midpoint. That is growth of 22.1% over FY2025, including the acquisitions closed in 2025 and 2026. 9M 2026 revenue was USD 4,135m, so the low end implies USD 1,265m in Q4, against USD 1,165m in Q4 2025. Materials was 16.6% of 9M 2026 revenue, and the model uses that share for FY2026E.

**FY2027E to FY2030E: organic growth only, fading to 4% by FY2030.** After FY2026 there are no further acquisitions unless I model one explicitly, with its price (section 4). 4% is long-run US nominal GDP growth: the Fed's September 2026 projections put longer-run real growth at 2.0% and inflation at 2.0%, which gives 4.04% (section 9).

**FY2027E starting point: backlog, not H1 growth (proposed 22 Oct).** My first version started the fade from H1 2026 organic growth (15.9%). That's one half-year in a strong period. Backlog is a better anchor for a contractor, because most of next year's construction revenue is work already won.

Granite's backlog measure is CAP (committed and awarded projects): signed contracts not yet performed (unearned revenue, the GAAP backlog) plus contracts awarded but not yet signed (other awards). All of it is in the Construction segment. Source: the MD&A of each 10-K and 10-Q, read by `src/data/extract_cap.py`.

| USD m | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 30 Sep 2026 |
|---|---|---|---|---|---|---|
| CAP at year-end | 4,010 | 4,485 | 5,546 | 5,296 | 6,969 | 7,455 |
| Growth | | 11.8% | 23.6% | -4.5% | 31.6% | 7.0% (9 months) |
| of which unearned revenue | 2,595 | 2,877 | 3,597 | 3,584 | 4,123 | 4,853 |
| CAP at 30 Sep | 4,328 | 4,078 | 5,585 | 5,620 | 6,338 | 7,455 |
| Construction revenue | 3,076 | 2,804 | 2,992 | 3,415 | 3,655 | |
| Next year's Construction revenue / CAP at 30 Sep | 0.648 | 0.734 | 0.612 | 0.650 | 0.697 (FY2026E) | |
| Same, excluding revenue from businesses acquired that year | | 0.734 | 0.612 | 0.630 | | |

How I use it: FY2027E Construction revenue = CAP at 30 Sep 2026 × the average share of September CAP that turned into the next year's Construction revenue over FY2023-25 (0.659, using the second ratio row). September is used because it's the last backlog figure before the valuation date, and the ratio is measured on the same date each year. FY2022 is left out because the Inliner business (USD 199m of CAP) was sold in Q1 2022. CAP at 30 Sep 2026 was USD 7,455m (Q3 10-Q), only 0.5% above June.

This gives FY2027E Construction growth of **9.0%** (USD 7,455m × 0.659 = USD 4,910m, against USD 4,503m in FY2026E). Growth then fades in a straight line to 4% in FY2030E (7.4%, 5.7%, 4.0%). With the June CAP it was 10.6%; it fell because FY2026E revenue went up to USD 5.4bn while CAP was flat in Q3. FY2026E itself implies a ratio of 0.710 on September 2025 CAP, above every year in the table, partly because of the 2026 acquisitions.

**Acquired revenue taken out of the ratio (agreed 22 Oct).** FY2025 Construction revenue includes USD 112.1m from Warren Paving and Papich, bought in 2025 (FY2025 10-K, MD&A). That work was never in Granite's September 2024 backlog, so it inflates the FY2025 ratio (0.650 instead of 0.630). FY2027E has no acquisitions, so the ratio should describe backlog Granite already holds turning into revenue. FY2023 and FY2024 also had smaller acquisitions (Lehman-Roberts and Memphis Stone, November 2023; Dickerson & Bowen, 2024). I haven't found a construction revenue figure for them in the filings, so those years aren't adjusted. I'd still rather remove the one distortion I can measure than keep it because the others can't be fixed. Without the adjustment the ratio would be 0.665 and growth 11.7%.

**Materials follows the same path.** Materials has no backlog of its own, and part of its output goes into Granite's own construction projects. Per the segment note (FY2025 10-K, Note 21), intersegment sales to Construction were USD 200.5m, 246.8m and 275.2m in FY2023-25, or 28%, 29% and 26% of total Materials output. So about a quarter of Materials volume moves directly with Construction. The rest goes to third parties, mostly other contractors and builders whose demand depends on the same public and private construction spending. Using one path for both segments is a simplification, but not an unreasonable one.

What this says and doesn't say:
- Backlog supports growth of about 9% in FY2027. CAP has risen 41% since the end of FY2024, faster than revenue, but the anchor is now about 4 points below the old 12.9%. It's also below the 10% to 12% organic growth in Granite's 2029 targets (section 3).
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

| | FY2023 | FY2024 | FY2025 | 9M 2026 |
|---|---|---|---|---|
| Upward revisions (USD m) | 8.1 | 25.6 | 64.9 | 58.3 |
| Downward revisions (USD m) | -96.9 | -50.2 | -33.5 | -18.5 |
| Net, % of revenue | -2.5% | -0.6% | +0.7% | +1.0% |

- FY2025 gross margin was 16.1%.
- Removing the net revisions gives 15.4%.
- Removing all upward revisions, as if none of them recur, gives 14.6%. On the same basis Construction alone falls from 15.7% to 13.9%.
- The MD&A says FY2025 had "more net increases from revisions in estimates due to claim settlements than in the prior year".
- The Q2 2026 10-Q says H1 2026 margin fell year on year "primarily due to a reduction in the favorable impact of claim settlements".

Projects below USD 5m aren't disclosed, so this is a partial view.

**9M 2026 check (Q3 10-Q, Note 3).** Five projects had upward revisions of USD 58.3m and one had a downward revision of USD 18.5m (USD 5m threshold). Only USD 10.6m of the upward revisions came in Q3. Granite gives the reasons as lower estimated costs from mitigated risks, contract modifications, changes in the probable recovery on outstanding claims, faster production and acceleration. Unlike 9M 2025, it doesn't list claim settlements. On the same method as FY2025:
- 9M 2026 gross margin was 16.55%;
- removing the net revisions gives 15.59%;
- removing all upward revisions gives 15.14%.

For Construction alone the range is 15.0% to 15.5% (reported 16.7%). So the normalised range is 15.1-15.6% for 9M 2026, against 14.6-15.4% for FY2025. The 15.0% base sits just below the 9M range and at the midpoint of the FY2025 range; across both periods the range is 14.6-15.6%. Two other points from the 10-Q:
- Materials gross margin fell to 15.9% in 9M 2026 (20.6% in 9M 2025), below Construction's 16.7%. Granite puts this down to energy surcharges offsetting higher diesel costs.
- Q3 alone was 19.0%. That's the seasonal peak, so 9M is a better basis than the quarter.

**Decision (4 Nov): 15.5% from FY2027E.** Revisions are a normal part of contracting, so I only remove the net effect. Removing net revisions gives 15.37% for FY2025 and 15.59% for 9M 2026, 15.47% for the two together, which I round to 15.5%. The downside case stays at 14.5% (all FY2025 upward revisions treated as one-off).

| Case | Gross margin from FY2027E |
|---|---|
| Base | **15.5%**, net revisions removed, FY2025 and 9M 2026 together (decided 4 Nov; 15.0% until then) |
| Downside | 14.5%: all FY2025 upward revisions treated as one-off. Combined with the reauthorisation gap in section 5 |
| Upside | about 17.0%: management's FY2026 guidance, translated as below |

FY2026E uses the 9M actual margin once it's out (see the note on interim values below).

**Why the base case moved from 14.5% to 15.0% (22 Oct).** With 14.5% the base case stacked three conservative choices on top of each other: low-end revenue, the most conservative margin normalisation, and high-end SG&A. Each one is defensible, but together they describe a worse year than any single piece of evidence supports. 15.0% sits in the middle of the range the revision data gives, and 14.5% becomes the downside.

**Upside: management guidance.** Guidance is for adjusted EBITDA margin (12.25-13.25% for FY2026), not gross margin, so it needs translating. Using Granite's own definition (net income after the JV partners' share, plus interest, tax, D&A, stock-based compensation and "other costs, net"), I rebuilt FY2025 adjusted EBITDA from the filed lines at 11.9% of revenue, against a 16.1% gross margin, a gap of 4.2 points. For H1 2026 the same rebuild gives 10.1%, against Granite's reported 10.3%, so the definition matches. Adding the 4.2-point gap to the 12.75% guidance midpoint gives an upside gross margin of about 17.0%. This is approximate: forecast SG&A (8.75%) is lower than FY2025's 9.2%, so guidance could be met with a slightly lower gross margin. Adjusted EBITDA starts from net income after the JV partners' share, so it needs interest and NCI, which come with the debt schedule after Q3. Then I'll add an adjusted EBITDA row and check the upside against guidance directly.

**The gap to guidance that remains.** On the same translation, the base case's 15.5% gross margin gives an adjusted EBITDA margin of about 11.8% from FY2027E, 0.5-1.5 points below FY2026 guidance. I keep that gap on purpose, because of Granite's forecasting history. The 2017-2019 restatement came from project forecasts that were too optimistic. FY2025 and H1 2026 margins were helped by claim settlements, which management itself calls out. Until margins without the claim benefits show up in the reported numbers, I don't take guidance as the central case.

Segment margins follow from the total, with Materials kept above Construction as in every year since FY2021 except FY2024. The exact segment margins are set after Q3.

**FY2026E: 9M 2026 actuals plus a seasonal Q4 (decided 4 Nov).** Margins are seasonal: paving and highway work is concentrated in the warmer months. Q4 2025 gross margin was 14.4% (FY2025 less 9M 2025), against 16.7% for 9M 2025. FY2026E takes the 9M 2026 gross profit and adds Q4 at the Q4 2025 margin. That gives 16.05% for the year, not the 16.55% you'd get by applying the 9M margin to Q4 as well. This is the same seasonal logic as the Q4 cash flow stub in section 10. Materials share is the 9M 2026 actual, 16.6%.

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

**Intangible amortisation: Granite's own schedule.** The FY2025 10-K gives expected amortisation of USD 21.6m, 13.2m, 13.0m, 13.0m and 13.0m for 2026 to 2030. The 2026 acquisitions add more: Kenny Seng brought USD 43.4m of identifiable intangibles (backlog, trade name, water rights and customer relationships). The Q3 10-Q gives no useful lives or amortisation schedule, and the purchase price allocation is still preliminary, so I leave it out until the FY2026 10-K. It's a non-cash charge, so the only effect on FCFF is the tax saving: 25% of whatever share of the USD 43.4m is amortised each year, a few USD m at most.

**Capex**
- FY2026E: USD 150m, the midpoint of guidance (USD 140m to 160m, including about USD 50m of strategic materials investment). That's 2.8% of USD 5.4bn.
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
| Increase in revenue | | 488 | 434 | 359 | 267 | |
| Net investment (÷ 3.87) | | 126 | 112 | 93 | 69 | |
| of which increase in working capital | 42 | 8 | 13 | 16 | 17 | 0 |
| of which net capex | | 119 | 99 | 77 | 52 | |
| Depreciation | 180 | 197 | 211 | 223 | 232 | |
| Book value of equipment sold | 15 | 16 | 17 | 18 | 19 | |
| Capex | 150 | 331 | 328 | 319 | 303 | 414 |
| Capex % revenue | 2.8% | 5.6% | 5.2% | 4.8% | 4.4% | 5.7% |
| ROIC on opening capital | 14.3% | 13.2% | 13.5% | 13.6% | 13.7% | |
| FCFF | 298 | 160 | 195 | 230 | 267 | 197 |

FCFF includes the smaller operating lines from section 6 (other costs, gains and proceeds from equipment sales). Interest, affiliates and other income are outside FCFF. Historical capex is gross too: FY2021-25 proceeds from equipment sales were shown separately in investing cash flow, as here.

FY2027E capex (5.7% of revenue) is still well above anything in Granite's FY2021-25 history (2.7-4.0%). I haven't smoothed it. It's what 9.0% organic growth costs at Granite's historical capital intensity. Granite's recent growth was partly bought, and an acquisition shows up as an acquisition, not as capex. The real lever is the growth rate, not the capex rule.

One consequence to be aware of: because net investment in total is set by the ratio, the working-capital days in section 7 only decide how it splits between capex and working capital. From FY2027E on they don't change FCFF. The alternative would be a ratio on fixed capital only (revenue / invested capital excluding goodwill, intangibles and trade working capital, FY2022-25 average 3.69), with working capital added on top. That would cost about USD 15-20m a year more in reinvestment, so I've kept the simpler version.

**Terminal year: reinvestment consistent with growth.** A business can only grow forever at rate g if it reinvests enough to fund that growth. The reinvestment rate, as a share of after-tax operating profit (NOPAT), has to be:

> reinvestment rate = g / RONIC

RONIC is the return earned on new capital. Net reinvestment is capex minus D&A plus the increase in working capital. By FY2030 trade working capital reaches 0% of revenue (section 7), so it doesn't grow after that, and all the reinvestment is net capex. So in the terminal year:

> capex = D&A + (g / RONIC) × NOPAT

Capex in the terminal year therefore comes from this formula, not from a fixed percentage of revenue. In the model the terminal year is a separate, normalised column after FY2030E (FY2030E NOPAT grown by g). I do it this way because in FY2030E itself working capital is still moving to its target, which would muddle the rule.

**Base case (agreed 22 Oct): RONIC = 9.7%, Granite's FY2022-25 average ROIC**, entered as a formula over the history (7.0%, 5.6%, 12.6% and 13.5%; `history_ratios.csv`). My first proposal was to use the model's own terminal ROIC, on the expectation that it would land near 9.7%. That expectation was wrong. With capex at 3.5% of revenue the model's ROIC climbed to 15.6%, because capital didn't grow with revenue. So the historical average is now an input in its own right.

With RONIC at 9.7% and g at 4%, the terminal reinvestment rate is 41% of NOPAT, and terminal capex is about 5.7% of revenue. That is a step up from 4.4% in FY2030E.

**Why terminal FCFF is below FY2030E.** Terminal FCFF is USD 197m, against USD 267m in FY2030E, even though NOPAT is 4% higher. The difference is the return on new capital:
- In FY2027E-30E, each extra dollar of revenue needs 1/3.87 of a dollar of capital and earns the NOPAT margin of about 4.6%. That's a return on new capital of about 18% (4.6% × 3.87).
- In the terminal year, new capital earns RONIC, 9.7%. To grow 4% a year at 9.7%, Granite has to reinvest 41% of NOPAT, against 17% in FY2030E.

I think the step down is right. Returns well above the cost of capital attract competition: other contractors bid more aggressively for the same public work, and margins on new contracts get pushed down. Over a long horizon, excess returns on new investment shrink, so the perpetuity shouldn't assume today's 18% on every new dollar. It is still one of the biggest single drivers of the value, so the RONIC sensitivities below matter.

During FY2027E-30E the model's ROIC on opening capital runs at about 13-14% (table above), above the 9.7% assumed for new capital in the terminal year. That's deliberate: by then the returns on today's business shouldn't be assumed to carry over to every new dollar invested.

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
- **Coverage: last twelve months to September 2026.** Operating income is FY2025 + 9M 2026 − 9M 2025 = USD 395.0m. Interest expense on the same basis is USD 73.9m, after taking out USD 273.7m. That amount is the non-cash amortisation of the debt discount on the 3.75% convertibles, which were settled in August 2026 (Q3 10-Q, MD&A and Note 14). It's an accounting charge from the conversion and won't recur. Coverage is 5.3x, against 6.0x on FY2025.
- Equity value is USD 5.44bn, above Damodaran's USD 5bn cut-off, so the large-firm table applies: A2/A, spread 0.78%, synthetic cost of debt 5.76%. The smaller-firm table would give A3/A- (0.89%). The WACC sheet shows both. The bond market's 1.65% sits between Damodaran's Ba1/BB+ (1.38%) and Ba2/BB (1.84%) spreads. So the market prices Granite's debt in Damodaran's BB range, while coverage gives an A rating. The market-based cost of debt (6.63%) is 0.88 points above the synthetic one. The market spread is direct evidence on Granite's own debt, so it stays the base case.
- The convertible notes count as debt at their debt component. The option part goes into the diluted share count, not the cost of debt.

**Capital structure weights: Granite's own market values on the valuation date.** Equity = share price × diluted shares = USD 121.69 × 44.70m = USD 5,440m. Debt = USD 1,565m:
- 6.375% notes USD 591m. That's the 600m principal priced at the 29 Oct market-based cost of debt (6.63%), using Excel's ODDFPRICE: 98.47, clean. Accrued interest is in accrued liabilities, which are already in working capital.
- 2030 convertibles at their USD 373.75m principal. The principal is settled in cash, and the value above par is in the share count (section 10).
- Term loan at its USD 600m book value. It's floating-rate and swapped to fixed; its Level 3 fair value is USD 604.4m.

The balance sheet carries USD 1,556m, USD 17.7m below principal (unamortised issuance costs and discounts). Lease liabilities are left out, because lease costs stay in operating costs and so in FCFF; including them would count them twice. D/E is 28.8% (industry 15.0%), the levered beta 1.213, the cost of equity 10.07% and the **WACC 8.93%**.

## 10. DCF and terminal value

The calculation is on the DCF sheet. All inputs are from the Q3 10-Q and the valuation date (29 Oct 2026).

**Timing.** The balance sheet is at 30 Sep 2026, so the DCF values FCFF from 1 Oct onwards: a Q4 2026 stub, then FY2027E to FY2030E. Cash flows are discounted from the valuation date (the 10-Q filing date) with a mid-year convention: the stub at the middle of Q4, each full year at its midpoint.

**Q4 stub = FY2026E FCFF minus 9M 2026 actual FCFF on the model's basis (agreed 4 Nov).** A straight 25% share would ignore seasonality: in FY2025 operating cash flow was USD 5.4m in H1 out of USD 468.9m for the year. 9M 2026 FCFF is rebuilt from the Q3 10-Q the way the model defines it:
- operating income USD 320.0m × (1 − 25%);
- \+ D&A 139.8m;
- − gain on equipment sales 3.9m;
- − capex 89.9m;
- \+ proceeds from equipment sales 16.6m;
- − the trade working capital build of 22.1m (receivables, contract assets, inventories, payables and accrued liabilities, from the cash flow statement).

That gives USD 280.5m. SBC stays a cost, and interest and acquisitions are left out. FY2026E FCFF is USD 298.2m, so Q4 2026E is USD 17.8m. That's low against the cash flow pattern above, because of what the full-year assumptions leave for Q4:
- operating income of USD 44m (FY2026E 364m − 9M 320m, with Q4 at the Q4 2025 gross margin);
- capex of USD 60m (the USD 150m guidance midpoint − 89.9m spent);
- equipment-sale gains of USD 21m, taken out as non-cash;
- a further USD 19m working capital build.

If Q4 capex comes in lower or working capital releases at year-end, as it often has, Q4 FCFF will be higher. At about 1% of EV, it doesn't change the result.

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

Equity in construction joint ventures is not added: that income is in revenue and gross profit, so it's already in FCFF. **Diluted shares: 44.70m.**
- 44.13m shares outstanding at 23 Oct 2026 (10-Q cover page).
- \+ 0.50m unvested RSUs, all counted, since they have no exercise price.
- \+ 0.07m from the 2030 convertibles.

Settlement terms (Q3 10-Q, debt note): the principal is paid in cash and the conversion premium in cash, shares or both. The conversion rate is 12.8398 shares per USD 1,000, a conversion price of USD 77.88, on USD 373.75m of principal, which is 4.80m underlying shares. At USD 121.69 the value above par is worth 1.73m shares. The 2024 capped call covers the premium up to its cap price of USD 119.82, and it's Granite's asset, so only the part above the cap dilutes: 0.07m shares. The workbook recalculates this from the share price, so if the price moves further above the cap the dilution grows.

A small timing gap remains: balances are at 30 Sep and discounting starts at the filing date about a month later. I leave it, because rolling the balance sheet forward a month would mean estimating October cash flows.

Sensitivity tables (WACC × g and WACC × exit multiple) come next, on a separate sheet.

## 11. Results (29 Oct 2026 valuation date; base case as decided on 4 Nov)

| | Gordon growth (main) | Exit multiple (cross-check) |
|---|---|---|
| PV of FCFF, Q4 2026E to FY2030E | 716 | 716 |
| PV of terminal value | 2,913 | 7,897 |
| Enterprise value | 3,629 | 8,612 |
| Terminal value % of EV | 80% | 92% |
| + cash and securities, + affiliates, − debt, − NCI | -1,004 | -1,004 |
| Equity value | 2,625 | 7,609 |
| Value per share (USD) | **58.72** | 170.20 |
| vs share price USD 121.69 | **-52%** | +40% |

WACC 8.93%; terminal growth 4%; terminal RONIC 9.7%; gross margin 15.5% from FY2027E.

Cross-check between the methods:
- The Gordon value implies 6.5x FY2030E EBITDA, leases added back. Damodaran's industry multiple is 17.1x.
- The exit multiple implies perpetual growth of 8.6%, on the model's own reinvestment rule.

Scenarios (Gordon value per share, USD; Sens sheet and section 12):

| Case | Value per share | vs price |
|---|---|---|
| Downside: no Construction growth in FY2027E, gross margin 14.5% | 43.28 | -64% |
| **Base** | **58.72** | **-52%** |
| Upside: gross margin implied by FY2026 guidance (about 17%) | 79.37 | -35% |
| Management 2029 targets, low end (10% growth, 14% adj. EBITDA) | 94.55 | -22% |
| Management 2029 targets, midpoint (11%, 15%) | 111.38 | -8% |
| Management 2029 targets, high end (12%, 16%) | 129.02 | +6% |

The checks all pass (balance sheet and cash flow history, working capital, g < risk-free rate, Gordon value implies 4.0%), so the gap to the price is about assumptions, not arithmetic.

**Sensitivity tables (Sens sheet, live formulas).**

At the base WACC (8.93%), long-run growth from 3.0% to 4.5% moves the value only from USD 56.68 to 60.00. The terminal RONIC (9.7%) is close to WACC, so faster growth needs almost as much extra reinvestment as it adds in profit. With WACC 1 point higher, growth adds almost nothing at all (USD 45.48 to 45.66). That's the main reason the Gordon value is so far below the exit-multiple value: a 17x multiple only makes sense if new investment earns well above the cost of capital for a long time.

WACC matters more than growth: 7.93% gives USD 78.43 and 9.93% gives USD 45.64, both at 4% growth.

**Interpretation.** My base case gives about $59 per share, well below the $121.69 price on 29 Oct. The reverse DCF shows why: the price is roughly what you get if Granite hits the middle of its 2029 targets (about 11% organic growth and a 15% adjusted EBITDA margin) and then slows to 4%. That needs a gross margin of about 18-19%, above anything Granite reported in FY2021-25 (10.4-16.1%). So the gap is mostly a question of whether management delivers its margin targets. The record backlog supports the growth part. Granite's history of optimistic project forecasts, and the open question on federal highway funding, make me cautious about the margin part. I read the current price as leaving little room for error rather than as clearly wrong.

## 12. What the share price implies (4 Nov 2026)

This analysis was run on the earlier base case (15.0% gross margin, FY2026E at the 9M margin), and the numbers below are from that run. The Sens sheet always shows the current values: with the 4 Nov decisions, the price implies a gross margin of 20.0% from FY2027E, and the management midpoint case gives USD 111.38.

The numbers are on the Sens sheet. The build produces them by changing one thing at a time in Excel and using Goal Seek on the Gordon value per share (`src/model/reverse_dcf.py`). The base case itself isn't touched.

**Reverse DCF, one driver at a time (price USD 121.69, base USD 52.07)**

| Driver | Base | Needed to reach the price |
|---|---|---|
| Gross margin from FY2027E | 15.0% | 19.9% |
| Organic growth FY2027E-30E, flat, then 4% | 9.0% fading to 4.0% | 38.0% a year |
| Terminal RONIC | 9.7% | not reachable: even with no terminal reinvestment the value is USD 94.30 |

For comparison, Granite's gross margin was 10.4% to 16.1% in FY2021-25.

**Management's 2029 targets as one case.** Organic growth at the target for FY2027E-29E, then 4% in FY2030E. The adjusted EBITDA margin rises in a straight line from FY2026E (13.1%) to the target in FY2029E. To translate the margin into the model's gross margin I keep SG&A at 8.75% and add SBC (FY2026 guidance, USD 48m) and NCI (9M 2026 share of revenue). The result depends only on EBITDA, so using Granite's 7.5% SG&A target with a lower gross margin would give the same value.

| | Organic growth | Adj. EBITDA margin FY2029E | Gross margin FY2029E | Value per share | vs price |
|---|---|---|---|---|---|
| Low end | 10% | 14% | 17.7% | 95.43 | -22% |
| Midpoint | 11% | 15% | 18.7% | 112.27 | -8% |
| High end | 12% | 16% | 19.7% | 129.92 | +7% |

So the share price is roughly what the model gives if Granite meets the middle of its 2029 targets and then grows at 4%.

**Margin normalisation on net revisions only.** The gross margin with net revisions removed:

| Period | Margin, net revisions removed |
|---|---|
| FY2025 | 15.37% |
| 9M 2026 | 15.59% |
| Both together, revenue-weighted | **15.47%** |

At a 15.5% base the value is USD 59.13 (scratch run). Two facts to weigh: net revisions were negative in FY2023 (-2.5% of revenue) and FY2024 (-0.6%), and positive in FY2025 (+0.7%) and 9M 2026 (+1.0%). Averaged over the four periods they come to about -0.35% of revenue.

**Why FY2027E steps down from FY2026E.** FY2026E uses the 9M 2026 gross margin (16.55%) for the whole year. The base 15.0% from FY2027E is lower for three reasons:

| Step | Effect | Margin after the step |
|---|---|---|
| FY2026E gross margin (9M 2026) | | 16.55% |
| Remove net revisions | -0.96 points | 15.59% |
| Remove the rest of the upward revisions | -0.45 points | 15.14% |
| Move to the FY2025-range midpoint | -0.14 points | 15.00% |

Part of the step is FY2026E itself being high. Applying the 9M margin to the whole year puts Q4 2026 at 16.55%. Q4 2025 was 14.4% (FY2025 less 9M 2025), so at the Q4 2025 margin FY2026E would be 16.05%, not 16.55%. The EBITDA margin goes from 11.0% to 9.3%, and adjusted EBITDA (Granite's definition) from 13.1% to 11.3%.

**FY2026E adjusted EBITDA against guidance.** Granite's definition starts from net income after NCI and adds back interest, tax, D&A, SBC, other costs, net, convertible debt gains and losses, and the remeasurement gain. Rebuilt from the model's lines (operating income + D&A + SBC + other costs + affiliate income + other income − NCI), 9M 2026 comes to USD 526.98m. Granite reports USD 526.981m (Q3 release), so the definition matches. For FY2026E, with SBC and NCI for Q4 at the Q3 rate:

| | Adjusted EBITDA | Margin |
|---|---|---|
| Model FY2026E | USD 708.7m | **13.1%** |
| Guidance range | | 12.25% to 13.25% |
| Implied Q4 2026 (model) | | 14.4% |
| Q4 2025 | | 11.1% |
| Q4 2026 at the guidance midpoint | | 12.8% |

So FY2026E is inside guidance, near the top. There's no modelling gap. If anything, FY2026E is slightly high because the 9M gross margin is used for Q4 as well.

**Terminal RONIC by segment.** Granite's own Materials returns, from the 10-K segment notes, are after-tax segment operating income divided by average segment assets:

| | FY2022 | FY2023 | FY2024 | FY2025 | Average |
|---|---|---|---|---|---|
| Materials return on segment assets | 12.1% | 10.3% | 6.6% | 7.9% | 9.2% |
| Same, excluding goodwill | | | | | 9.8% |

The return fell as the 2023-25 acquisitions added assets at their purchase prices. This isn't the same measure as RONIC:
- Segment assets aren't invested capital. They leave out most working capital, which is why the same ratio for Construction (about 33%) can't be compared with anything.
- Segment operating income is before corporate costs.

Damodaran's industry return on capital (`EVA.xls`, Jan 2026) is on the same book-capital basis as Granite's own 9.7%:
- Construction Supplies 16.7%, against an 8.3% cost of capital;
- Engineering/Construction 25.3%, against 8.7%.

With Construction at 9.7% and Materials at 23.4% of segment operating income (FY2022-25 average), the effect on value is small:
- Materials at Granite's own 9.8%: effective RONIC 9.70%, USD 52.20.
- Materials at Damodaran's 16.7%: effective RONIC 10.73%, USD 56.23.

Materials is under a quarter of profit, and terminal reinvestment is only part of the value.

**Decisions (4 Nov).**
- **Base gross margin 15.5%** from FY2027E, removing only the net revisions (section 6).
- **No Materials RONIC premium.** The terminal RONIC stays 9.7%, because Granite's own Materials returns average about 9%.
- **Management's 2029 targets stay as scenarios**, not in the base case.
- **FY2026E Q4 uses the Q4 2025 gross margin pattern** instead of the 9M margin, consistent with the seasonal stub (section 6).

