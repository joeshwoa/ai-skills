# Measurement

Purpose: define what to measure, how to read attribution honestly, how to run experiments that end in a decision, and how to review performance without vanity metrics.
Last updated: 2026-10-19

Use with `templates/kpi-tree.md`. Paid-media tracking, pixels and CAPI are in `media-buying` (`references/tracking-and-attribution.md`); social reporting in `social-media-manager` (`analytics-and-reporting.md`). Arithmetic helpers live in `media-buying/scripts/ads_math.py`.

## 1. KPI tree
Start at the business goal and break it into drivers until each leaf is something a person can change this week.
```
Delivered revenue (goal)
 = Orders delivered x Average order value
 Orders delivered = Confirmed orders x Delivery rate
 Confirmed orders = Leads/chats x Confirmation rate
 Leads/chats = Reach/visits x Click-or-start rate
 Repeat revenue = Customers x Repeat rate x Repeat order value
```
Rules: each branch has an owner, a baseline, a target and a data source; no more than 5 to 8 leaves tracked weekly; every leaf has a "so what" action. Template: `templates/kpi-tree.md`. For services replace orders with bookings and delivery rate with show-up rate; for B2B use qualified meetings, proposals, win rate, deal size, cycle time.

## 2. Leading vs lagging
| Type | Meaning | Examples | Use |
|---|---|---|---|
| Lagging | Result you care about, slow to move | Delivered revenue, profit, repeat purchases, retention | Judge the strategy at monthly/quarterly review |
| Leading | Early signals you can influence | Qualified chats started, first-reply time, landing conversion, email click rate, review rate | Steer weekly |
| Guardrail | Protects against bad growth | Refusal/return rate, complaint rate, unsubscribe/block rate, cost per delivered order | Stop rule |
Pair each leading metric with the lagging result it should predict, and check the link with your own data after 8 to 12 weeks; if the relationship does not hold, change the leading metric.

## 3. What to measure per funnel stage
| Stage | Metrics | Notes |
|---|---|---|
| Awareness | Qualified reach (target audience), branded search, video completion, profile visits | Reach alone is not a goal; report in the segment you target |
| Consideration | Product page views, chats started, saves/shares, email signups, GBP actions (calls, directions) | Track the first real intent action |
| Conversion | Confirmed orders/bookings, conversion rate, cost per confirmed order, average order value | For COD add confirmed and delivered layers |
| Retention | Repeat rate by cohort, time to second order, churn, referral rate, review rate | Often the cheapest lever |
| Operations | First-reply time, delivery time, refusal rate, stock-outs | They decide whether marketing money pays back |
Cash-on-delivery businesses: report three layers (platform-reported orders, confirmed orders, delivered/collected orders) and compare cohorts by order date with a lag (see `../../media-buying/references/mena-and-egypt-notes.md`, section 6).

## 4. Attribution reality
No tool gives the truth; each gives a view with a bias.
| Source | What it counts | Bias |
|---|---|---|
| Ad platform (Meta, Google, TikTok) | Conversions it can link to its own ads, within its attribution window, often including view-through | Over-credits itself; windows and modelling differ across platforms; sees order placed, not delivered |
| GA4 | Sessions and key events from your site, by channel | Misses chats and offline; consent and tracking prevention reduce data; default channel credit differs from platforms |
| CRM / order sheet | Real customers and revenue by source you recorded | Depends on someone capturing source; best for delivered revenue |
| Survey ("How did you hear about us?") | Self-reported source | Remembers the last or most memorable touch; useful for dark social and word of mouth |
Facts from Google's GA4 help (read 2026-10-19): the reporting attribution models available are data-driven and paid and organic last click ("last non-direct click" is the same model); first click, linear, time decay and position-based models were removed in November 2023. Paid and organic last click ignores direct traffic and gives 100 percent of the key event value to the last channel clicked; data-driven attribution distributes credit using your account's data and can reattribute conversions for up to 7 days after the event.
Practical approach:
1. Define one source of truth for revenue (CRM or order sheet) and reconcile platform numbers to it monthly. Expect platform totals to exceed it; the gap is normal, track it as a ratio.
2. Tag everything: UTM on every link, a source prefix or unique link for WhatsApp, coupon codes for offline and creators, a source field in the order form.
3. Use platform data for within-platform decisions (which creative), CRM data for money decisions (which channel to fund), surveys to find channels that tracking cannot see.
4. For big spend, test incrementality with a holdout or geo/time test where practical instead of arguing about attribution.
5. Do not add platform-reported conversions across platforms; they overlap.

## 5. Experiment design
Write before running: hypothesis, metric, sample, duration, decision rule.
- **Hypothesis**: "If we [change] for [segment], then [metric] will [direction/size] because [reason]." One change at a time.
- **Primary metric**: the one that decides (cost per confirmed order, conversion rate, reply rate). A guardrail metric too (refusal rate, unsubscribe rate).
- **Sample and duration**: decide the minimum number of conversions or recipients before starting. For ad creative tests use `media-buying/scripts/ads_math.py test-size` and `abtest`; for email/WhatsApp use a random split of the same segment. Do not stop early because the numbers look good on day 2. Run whole weeks to cover weekday cycles; avoid Ramadan, Eid and White Friday boundaries unless you are testing those.
- **Decision rule** (example, adjust): "Keep B if it improves the primary metric by at least [x] with the planned sample and does not worsen the guardrail; otherwise keep A." If the result is inconclusive, treat it as "no evidence" and move to a bigger change, not a longer test.
- **Log** every test: date, setup, result, decision, next test (`media-buying/templates/test-log.md` for ads).
- **Small-business reality**: with low volume use bigger changes (offer, channel, page) and longer windows; compare before/after cautiously; accept directional evidence and say so.

## 6. Reading results and decisions
Every review ends with continue / change / stop for each initiative. Use these checks before acting: tracking works; sample is enough; the comparison is fair (same period, same budget); external events (holiday, stock-out, outage) are noted; effect size matters in money, not only in percent. If data is thin, run the cheaper, reversible action first.

## 7. Cohorts, CAC, LTV and payback
- **CAC** (customer acquisition cost) = acquisition spend (media plus the share of creative, tools and labour you decide to include) / new customers. State what is included.
- **Allowable CPA** = contribution margin per delivered order x delivery rate (for COD) minus a profit target. Break-even CPA is the ceiling, not the goal. Margin must include product cost, packaging, delivery both ways for refused parcels, COD and payment fees, returns.
- **LTV**: revenue or gross profit per customer over a stated period. Use observed cohorts (customers who bought in month M and what they bought after), not forecasts. Caveats: small samples, survivorship in old cohorts, price/mix changes, discounting; use gross profit and a cap (for example 6 or 12 months) rather than lifetime fantasies; do not base spend on LTV you have not observed.
- **Payback period**: months until cumulative gross profit from a cohort covers its CAC. Choose a limit tied to cash (a business that cannot wait should require first-order payback).
- **Cohort table**: rows = acquisition month, columns = months since, cell = share repeating or cumulative gross profit per customer. Compare cohorts by order date.
- Avoid blended numbers when mixing paid and organic; report both blended and paid-only CAC.

## 8. Dashboards and review cadence
- **Dashboard**: one page, 5 to 8 numbers, each with target, last week, trend and note. Sources: CRM/order sheet, GA4, platform dashboards, Search Console, GBP, WhatsApp/email tools. Automation can feed it (`automation-studio`, `n8n-agent-studio`), with human review of anomalies.
- **Cadence**: daily 10-minute check during launches (orders, errors, replies); weekly 30-minute review (leading metrics, blockers, one decision); monthly review (lagging, cohort, budget shift); quarterly strategy review (OKRs, positioning, channel mix, "not now" list).
- **Report shape**: headline result, vs target, what worked and why, what failed and why, next 3 actions, risks. Use `premium-documents` or `premium-presentations` for formal reports and `premium-spreadsheets` for the tracker.
- Always show the date range, data sources and known data gaps. Unknown is a valid number.

## 9. Marketing OKR examples (illustrative; replace numbers with your baselines)
| Business | Objective | Key results |
|---|---|---|
| Online store (COD) | Make marketing pay back on delivered orders | KR1 delivered orders per month from [baseline] to [target]; KR2 cost per delivered order at or below [allowable]; KR3 refusal rate at or below [limit] |
| Local clinic/shop | Become the first choice in the neighbourhood | KR1 GBP calls and direction requests from [baseline] to [target]; KR2 reviews with replies from [n] to [n]; KR3 WhatsApp bookings from [baseline] to [target] |
| B2B services | Build a predictable pipeline | KR1 qualified meetings per month [target]; KR2 proposals sent [target]; KR3 two published case studies |
| Creator | Turn attention into owned audience | KR1 WhatsApp/email subscribers from [baseline] to [target]; KR2 revenue per 1,000 views; KR3 one product validated by [n] paid users |
| App/startup | Prove activation and retention | KR1 activation rate [target]; KR2 week-4 retention [target]; KR3 cost per activated user at or below [allowable] |
Rules: 2 to 3 objectives, 2 to 4 KRs each, scored 0 to 1 at quarter end, stretch targets labelled, one owner each.

## 10. Avoiding vanity metrics
| Vanity | Why misleading | Use instead |
|---|---|---|
| Followers, page likes | Can be bought, not tied to sales | Reach in target segment, saves, chats, subscribers |
| Impressions/views alone | No intent signal | Cost per qualified chat, branded search |
| Open rate | Inflated by image pre-loading and privacy features | Click, reply, conversion |
| Platform ROAS on COD | Counts orders placed | Net ROAS on delivered revenue |
| Total website traffic | Includes bots and wrong audience | Conversion-intent actions |
| "Engagement rate" without context | Rewards giveaway/bait posts | Engagement from target segment, comments with intent |
| Blended CAC | Hides paid inefficiency | Paid-only and organic split |
Test: if this number doubled, would profit change? If not, it is a diagnostic at best.

## Sources (accessed 2026-10-19)
- https://support.google.com/analytics/answer/10596866 (GA4 attribution models: data-driven; paid and organic last click; deprecation note)
- Internal: `../../media-buying/references/mena-and-egypt-notes.md` (section 6), `media-buying` tracking and testing files.
- Formulas and cadences are standard practice; thresholds are labelled as examples or heuristics. Platform attribution windows differ and change; check each platform's current documentation.
