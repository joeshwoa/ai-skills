# Reporting
Purpose: produce weekly and monthly paid-media reports that a business owner can act on, with honest numbers and clear next steps.
Last updated: 2026-10-19

Templates: `templates/weekly-report.md` (weekly), and the monthly structure below. Metric definitions per platform are in `platforms/*.md` section 10. Reconciliation and COD layers are in `tracking-and-attribution.md` s4 and s6. Figures in this file are illustrative; no benchmarks are cited.

## 1. Principles
1. **Lead with the business result**, then the platform metrics that explain it. The reader wants: did we make money, what is the trend, what do we do next.
2. **Judge against targets, not against the past alone**: break-even and target CPA/ROAS first (`scripts/ads_math.py breakeven`), then week-over-week and month-over-month.
3. **State the basis of every number**: date range, attribution setting and window, currency and FX rate, source (platform, GA4, shop, CRM), and whether it is placed, confirmed or delivered.
4. **Do not mix sources in one ratio.** Platform revenue over platform spend, or shop revenue over spend: never platform revenue over analytics spend or the like (`tracking-and-attribution.md` s4).
5. **Show uncertainty**: lag (recent days under-reported), small samples, modeled values. Mark estimates as estimates.
6. **Report what you did and what happened**: link changes in the change log to results (`optimization-playbook.md` s7).
7. **One recommended action per finding**, with expected effect and what approval is needed (SKILL.md: no spend changes without approval).

## 2. KPI hierarchy
| Level | KPIs | Why it matters | Source of truth |
|---|---|---|---|
| Business | net revenue (delivered/collected), gross margin, contribution after ad spend, new customers, cost per new customer (blended), MER, qualified leads/pipeline and sales for B2B | Pays the bills | shop/ERP/CRM, bank/courier settlement |
| Marketing efficiency | blended CPA, MER, platform ROAS/CPA vs break-even, cost per qualified lead, delivery-adjusted ROAS (`ads_math.py cod`) | Is paid media profitable | combination; state sources |
| Platform delivery | spend, impressions, reach, frequency, CPM | Is the budget buying attention | ad platforms |
| Engagement/creative | link CTR, hook rate, hold rate, landing page view rate, cost per landing page view | Why efficiency moves | ad platforms (definitions s10 of platform files) |
| Site/funnel | sessions, add to cart rate, checkout rate, conversion rate, response time, confirmation rate | Where people drop | GA4/shop/CRM |
Report from the top down. A drop in platform CTR is not a headline unless it explains a business change.

## 3. Weekly report (structure; fill `templates/weekly-report.md`)
1. **Headline (3 lines)**: result vs target (spend, revenue or leads, CPA/ROAS vs break-even), trend, the decision needed.
2. **Scorecard table**: this week, last week, change, target; spend, orders/leads, CPA, ROAS, delivered ROAS (if COD), qualified leads, MER.
3. **What happened**: 3-5 bullets explaining the biggest movements with evidence (creative, audience, funnel, seasonality, tracking).
4. **By platform and funnel stage**: spend share, CPA/ROAS vs target, one-line status (scale/hold/fix/cut).
5. **Creative**: top and bottom ads by the decision metric, tests running and results (`creative-testing.md`), fatigue flags, next concepts.
6. **Changes made** (from the change log) and their effect; changes proposed for approval (what, where, why, expected effect, rollback condition).
7. **Reconciliation**: platform vs shop/CRM ratio and COD layers; any tracking issues.
8. **Risks and blockers**: policy, payment, stock, site, tracking, capacity.
9. **Next week plan** and budget pacing (`ads_math.py pacing`).
Length: one page plus an appendix table. Send on a fixed weekday after conversion lag has settled (for example 3 days after week end for slow cycles).

## 4. Monthly report (structure)
1. **Executive summary** (half a page): month result vs plan and vs previous month, profit or loss on paid media (contribution after ad spend), 3 key learnings, 3 decisions requested.
2. **Business outcomes**: delivered revenue, new vs returning customers, blended CAC/CPA, MER, margin; lead-to-sale funnel for lead-gen; pipeline for B2B.
3. **Spend and efficiency**: spend vs budget and pacing deviation; CPA/ROAS vs target by platform, funnel stage and market; marginal efficiency (what the last 20% of spend returned).
4. **Funnel diagnostics**: traffic -> add to cart -> checkout -> order -> confirmed -> delivered (or lead -> qualified -> won) with drop-offs.
5. **Creative and test review**: winning concepts, retired concepts, test results and what they imply, creative pipeline for next month.
6. **Audience and market insights**: segments, geographies, devices, placements that over/under-performed.
7. **Account health**: policy events, payment/verification status, access review (`policy-and-account-health.md`).
8. **Tracking audit**: tracking plan state, reconciliation ratio, issues found and fixed.
9. **Plan for next month**: objectives, budget, structure changes, tests, calendar (Ramadan, White Friday, payday: `mena-and-egypt-notes.md` s7), targets refreshed for price/FX changes (`bidding-and-budgets.md` s8).
10. **Appendix**: platform tables, definitions, window/attribution settings used, FX rate used and date.

## 5. Blended vs platform-reported numbers
- **Platform-reported** (ROAS, CPA): counts conversions the platform claims under its attribution; includes view-through; can double count across platforms because each claims credit; excludes what its tag cannot see. Use for in-platform optimization and relative comparison.
- **Blended** (business-level, source-agnostic): total business outcome divided by total ad spend, independent of attribution.
  - **MER (marketing efficiency ratio)** = total revenue / total marketing spend for the period, all channels, using one revenue source (shop/ERP). It answers "what do we get for each unit of marketing money, however it was attributed". Also called blended ROAS.
  - **Blended ROAS** (paid only) = total revenue / paid media spend; if revenue includes organic and repeat customers, label it so.
  - **Blended CPA / CAC** = total ad spend / total new customers (or orders), from the shop or CRM.
  - **Delivered ROAS** (COD) = delivered revenue / spend (`ads_math.py cod`).
- Compare the two: if platform ROAS is flat while MER falls, suspect attribution drift, organic decline or tracking; if MER rises while platform ROAS falls, check for brand lift, promotions or channel mix shifts. The gap itself is information; do not hide it.
- Rule: decide budget between channels by incremental evidence where possible (section 6), by blended results next, and by platform-reported numbers last.
- Customer lifetime value: if the client uses repeat purchases to justify a higher CPA, require a computed repeat-rate from their data, not an assumption.

## 6. Incrementality basics (plain language)
Attribution assigns credit; incrementality asks "how many of these sales would not have happened without the ads?" Retargeting and brand search often look excellent in attributed numbers because they target people already likely to buy.
- **Holdout test**: show ads to most of an audience and withhold from a random slice (or run a PSA/blank ad for the slice). Compare conversion rates; the difference is the lift. Needs random assignment, enough volume, and a period long enough to cover the conversion cycle. Some platforms offer built-in conversion lift/experiment tools; availability and requirements vary and are `unverified` in the platform files: check the current help pages.
- **Geo test**: switch ads off (or on, or up) in some regions or cities and compare sales against similar regions that stayed unchanged, before and after. Works when sales are tracked by region and regions are similar (for example matched governorates or cities). Weaknesses: spillover, few regions, regional events, courier coverage differences.
- **Time-based (on/off) test**: pause for a period and compare; weakest design because season, payday and promotions confound it. Use only with caution and say so.
- **Reading results**: report the lift with its range of uncertainty, not a single number; a small lift with a wide range is "unclear". Test one channel at a time.
- **Practical heuristics**: run a geo or holdout test before moving a large budget share on attribution evidence alone; always run retargeting with an exclusion group; compare new-customer vs returning share; track branded search demand as a sanity check.
- **Do not overclaim**: incrementality results apply to the tested conditions and time frame.

## 7. How to present bad news
1. **Say it first, plainly**: "Paid media lost money this month: delivered ROAS 1.8 vs break-even 3.5" (illustrative). No burying in appendices.
2. **Separate fact from cause**: what the numbers show, what we know about the cause, what we still need to test.
3. **Show the diagnostics you ran** (tracking ok? offer? creative? audience?) following `optimization-playbook.md` s3; this builds trust and shows it is not random.
4. **Own your part** (changes we made, what we missed) and the outside factors (stock, price, seasonality, site), without blaming.
5. **Give options with consequences**: continue as is, fix X then re-test, reduce spend and protect margin, pause. State cost and risk of each, and recommend one.
6. **Set a decision date and a stop-loss rule** agreed in advance (for example "if CPA stays above break-even for two full conversion cycles after the fix, we reduce budget by half").
7. **Do not manipulate metrics** (changing windows, selective periods, counting view-through) to soften the message. State any window changes explicitly.
8. Keep the tone constructive: next actions, owner and date.

## 8. QA checklist before sending
- [ ] Date ranges identical across sections; the week/month boundaries match the shop's time zone.
- [ ] Attribution setting and window recorded; no change mid-period without a note.
- [ ] Currency and FX rate/date stated; totals recomputed with `ads_math.py metrics` where unsure.
- [ ] Spend matches the platform billing/ad account totals (allow for reporting lag; X spend lag in `x-ads.md` s5).
- [ ] Revenue/leads reconcile with shop/CRM within the documented ratio; COD layers shown.
- [ ] No source mixing in ratios; blended and platform numbers labeled.
- [ ] Recent days flagged as incomplete (conversion lag).
- [ ] Targets and break-even current (price, COGS, delivery rate, FX).
- [ ] Every chart/number has a source; every claim has a metric.
- [ ] Changes list matches the change log; proposed changes marked "needs approval".
- [ ] Sensitive data removed (customer names, phones, emails, tokens).
- [ ] Spelling, Arabic/English consistency, numerals and currency tokens consistent.
- [ ] Someone other than the author read the headline and the recommendation.

## 9. Automation (high level)
- **Data sources**: official reporting APIs (Meta Insights API, Google Ads API, TikTok, Snap, LinkedIn, X, Pinterest; per-platform API sections in `platforms/*.md` s11), the shop/CRM, GA4. Scheduled pulls into a sheet or warehouse, with a daily snapshot so numbers do not shift under you (platforms revise data for days: X note in `x-ads.md` s5).
- **Connectors**: reporting connectors and automation tools (for example Make or n8n workflows, spreadsheet connectors, BI tools) can fetch, join and refresh dashboards. Choose connectors that use the platform's official OAuth/system-user flow and minimum read scopes.
- **Joining**: use consistent names (`scripts/naming.py`) and UTMs (`scripts/utm_builder.py`) as join keys between ad platform rows, analytics and CRM; the order ID joins shop and courier data.
- **Secrets**: store API tokens and credentials in the tool's secret manager or environment variables; never paste them in prompts, chat, spreadsheets or reports; rotate on staff changes (`policy-and-account-health.md` s6). The agent should call a scheduled job or a read-only endpoint rather than receive credentials.
- **Rate limits and errors**: respect platform limits and retry with backoff (`meta-ads.md` s11); alert on failures and on empty days.
- **LLM-assisted commentary**: have the model write the summary from the computed tables only; do not let it recompute figures; keep a human reviewer; label AI-generated text where clients need to know.
- **Read-only by default**: automation that reads for reports needs no write scope. Any automation that changes budgets or bids requires the client's approval policy and logging (`optimization-playbook.md` s7; `meta-ads.md` s11 agent rules).
- **Dashboards vs reports**: dashboards for daily monitoring, written reports for decisions; the weekly narrative is not replaced by a dashboard.

## 10. Example scorecard and wording (illustrative numbers)
| Metric | This week | Last week | Change | Target / break-even |
|---|---|---|---|---|
| Spend (EGP) | 20,000 | 18,000 | +11% | budget 20,000 |
| Orders placed | 100 | 95 | +5% | n/a |
| Platform CPA (placed) | 200 | 189 | +6% | target 210, break-even 283 |
| Platform ROAS (placed) | 5.0 | 5.3 | -6% | break-even 3.5 |
| Delivered ROAS (cohort lag, provisional) | 3.5 | 3.7 | -5% | break-even 3.5 |
| MER (all revenue / all marketing spend) | 4.1 | 4.3 | -5% | plan 4.0 |
Wording: "Platform numbers look healthy, but delivered ROAS is at break-even once refused orders are counted (`ads_math.py cod`: 100 orders, 70% delivered, AOV 1,000, spend 20,000 gives platform ROAS 5.0 and delivered ROAS 3.5). Recommendation: keep spend flat, introduce phone confirmation before dispatch, and re-evaluate on the next cohort. Needs your approval: yes / no."

## 11. Cadence summary
| Cadence | Audience | Content | Time |
|---|---|---|---|
| Daily alert | media buyer | billing, rejections, spend anomalies, tracking gaps | minutes |
| Weekly | client owner/marketing lead | section 3 | one page |
| Monthly | owner/management | section 4 | two to four pages |
| Quarterly | management | strategy review, incrementality tests, channel mix, targets reset | review meeting |

## Sources
- Platform files (dated 2026-10-19) section 10 (metrics) and section 11 (API): Meta, Google, TikTok, Snapchat, LinkedIn, X, Pinterest, YouTube, Telegram.
- `tracking-and-attribution.md`, `mena-and-egypt-notes.md` s6. Definitions of MER, blended ROAS and incrementality tests are standard marketing-analytics practice written here in plain terms; no external benchmark cited. Platform-specific lift tools were not verified in this pass.
