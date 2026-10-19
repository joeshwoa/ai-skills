# Bidding and budgets
Purpose: set budgets and bid strategies from unit economics, protect learning, scale safely and control pacing and currency risk.
Last updated: 2026-10-19

Platform-specific bid names, minimums, learning thresholds and change limits are in `platforms/*.md` section 5. This file is platform-neutral; where it gives a number it is a **heuristic** with its reasoning, and the platform file wins if the two differ. Arithmetic: `scripts/ads_math.py`.

## 1. Start from economics, not from a round number
1. Break-even CPA/ROAS: `python3 scripts/ads_math.py breakeven --price P --cogs C --other-var V --cod-delivery-rate R --return-rate X` (platform numbers count orders placed, so the COD and return adjustment matters; `tracking-and-attribution.md` s6).
2. Target CPA = break-even CPA x (1 - cushion). Heuristic cushion 20-30% to leave profit and absorb noise; use a smaller cushion only when strategic (acquisition for lifetime value) and approved by the client in writing.
3. Target ROAS = 1 / (target CPA / order value), expressed on the same basis the platform reports (order value placed).
4. For leads: allowable cost per lead = allowable cost per sale x lead-to-sale rate; judge qualified leads, not raw leads (`funnel-and-objectives.md` s5).
5. Everything else (bids, budgets, thresholds) is a function of target CPA. If you cannot state it, stop and ask for margin data (SKILL.md workflow step 1).

## 2. Setting the budget
- **Volume method**: budget = target CPA x conversions needed in the period. `python3 scripts/ads_math.py budget --target-cpa 150 --conversions-needed 50 --days 7` gives 7,500 total and about 1,071 per day. The conversions needed are the learning/volume threshold in the platform file (about 50 per ad set per week on Meta in `meta-ads.md` s5; about 25 results or 7 days for TikTok in `tiktok-ads.md` s5; Google Smart Bidding thresholds in `google-ads.md` s5).
- **Multiples of CPA**: platform files give floors as multiples of target CPA (for example TikTok daily ad group floors by funnel depth in `tiktok-ads.md` s5; Google's tCPA daily budget guidance in `google-ads.md` s5; Meta's reported lower bound in `meta-ads.md` s5, which is secondary). A budget below the platform's floor means the ad set will not learn; fix by moving up the funnel, widening the audience or consolidating, not by squeezing more ad sets in.
- **Minimums**: platform minimums are in the platform files (TikTok in USD only, LinkedIn per day and lifetime, Snapchat per ad squad and campaign). Read the minimum in the account currency from the UI; some are `unverified`.
- **Total budget from goal**: required spend = target conversions x target CPA; if the client's budget is lower, the achievable volume is budget / target CPA. Tell the client the gap instead of promising the goal.
- **Budget level**: campaign-level budget (CBO/Advantage+ campaign budget, Snap Smart Budget, LinkedIn campaign groups, Pinterest CBO) lets the platform shift money to winners; ad-set budgets give control. Use campaign-level for a prospecting campaign with similar ad sets; use ad-set level when ad sets are deliberately different (test cells, different markets). Do not use both.
- **Daily vs lifetime**: daily for always-on; lifetime for fixed promotions and where day-parting needs it (Meta requires lifetime for ad scheduling in `meta-ads.md` s5). Many platforms let a day overspend and balance over the week or month (Meta up to 75% over a day in `meta-ads.md` s5; Google up to 2x per day, monthly cap in `google-ads.md` s5; LinkedIn lifetime pacing up to 150% in `linkedin-ads.md` s5; Pinterest up to about 125% in `pinterest-ads.md` s5). Expect daily spend swings; judge weekly.
- **Split across funnel stages**: see `funnel-and-objectives.md` s4 (80-90% prospecting / 10-20% retargeting as a starting heuristic).
- **Reserve** a testing slice: 10-20% of spend for creative and audience tests once the account has a stable scaling base (heuristic; below that, tests are too small to read).

## 3. Bid strategy ladder (platform-neutral)
| Rung | Meaning | Use when | Risks | Platform names |
|---|---|---|---|---|
| 1. Lowest cost / maximize volume | Spend the budget, get the most results; cost is not controlled | New campaigns, learning, small data, wide targeting | CPA can drift up; fine for finding what works | Meta highest volume/lowest cost (`meta-ads.md` s5); Google Maximize conversions (`google-ads.md` s5); Snap AUTO_BID (`snapchat-ads.md` s5); LinkedIn maximum delivery (`linkedin-ads.md` s5); Pinterest Performance+ (`pinterest-ads.md` s5); X automatic bidding (`x-ads.md` s5) |
| 2. Cost cap / target CPA | Keep average cost near a number | After the campaign has stable volume at known CPA; to protect margin when scaling | Too tight = under-delivery, learning limited; changes restart calibration | Meta cost per result goal; Google Target CPA; Snap TARGET_COST; LinkedIn target cost/cost cap; X target bidding |
| 3. Bid cap | Hard maximum per auction | Only when you understand the auction price; advanced | Can stop delivery completely; bid is not cost | Meta bid cap; Snap LOWEST_COST_WITH_MAX_BID; X maximum bid |
| 4. ROAS goal / value optimization | Optimize for value, with a minimum return | Many conversions with varied values and clean value tracking | Needs reliable values; floor too high = no delivery | Meta ROAS goal; Google Maximize conversion value/Target ROAS; Snap MIN_ROAS is deprecated (`snapchat-ads.md` s5) |
Rules:
- Start at rung 1 and move up only when the data supports it: enough conversions at stable CPA for the platform file's threshold. Moving up early is the most common cause of "no delivery".
- When moving to a target, set it at or slightly above the recent actual CPA (heuristic: within 10-20% of the last stable CPA) and tighten in steps. Google's Demand Gen guidance suggests starting tROAS about 20% below the last 30 days' ROAS and adjusting about 10% at a time (`google-ads.md` s5).
- The Google 2026-08-17 change makes budget-limited tCPA/tROAS campaigns deliver closer to the entered target, so audit every target there (`google-ads.md` s5).
- Do not run a cap and a tight audience and a small budget together: three constraints leave no room to deliver.
- Frequency, pacing and billing event details differ (impression, click, view billing); read the platform file before comparing costs across objectives (`x-ads.md` s5).

## 4. Learning-phase management
Learning is the period when the system explores and the results are volatile. Platform definitions: `meta-ads.md` s5 (about 50 events in 7 days after the last significant edit), `tiktok-ads.md` s5 (about 25 results or 7 days), `google-ads.md` s5 (calibration over 1-2 conversion cycles; conflicting help pages noted there), Snap/LinkedIn/X/Pinterest/Telegram have no verified numeric threshold in their files.
Rules:
1. **Know the status** each time you open an account: learning, learning limited, normal. Learning limited is a signal that volume is too low (`meta-ads.md` s12 cases).
2. **Do not judge** an ad set in learning; wait for the platform's exit or the wait rule (spend of 2-3x target CPA plus the minimum days).
3. **Protect it**: no changes to optimization event, targeting, bid strategy, or creative inside a live ad; no big budget jumps; no pausing for a week and restarting (lists per platform in s9).
4. **Fix learning limited** by raising event volume: upstream event, wider audience, fewer ad sets, fewer ads, looser cap, modest budget increase. Never fix it by adding more ad sets.
5. **Batch changes**: make one deliberate change, then wait the full window; log it (`optimization-playbook.md` s7).
6. **Budget changes**: small changes are usually safe; large ones can restart learning. No platform publishes a universal percentage (Meta says none; "20%" is a third-party convention). TikTok publishes per-change limits (`tiktok-ads.md` s5).

## 5. Scaling methods
**Vertical (raise the budget of the winner)**
- `python3 scripts/ads_math.py scale --budget 1000 --step 0.2 --steps 4` gives 1,200, 1,440, 1,728, 2,074. Heuristic rule from the script: step at most every 3-4 days, only while CPA stays within 20% of target; hold or step back if it breaks. Reasoning: smaller steps keep the optimizer calibrated; waiting a few days separates a real trend from lag and noise.
- Platform context: Meta file describes about 20% every 2-3 days as a convention (`meta-ads.md` s9); TikTok limits are stricter and published (`tiktok-ads.md` s5, agent default at most 30% per change, 2+ days apart, 20% when CPA is near the limit); Google says evaluate after 1-2 conversion cycles (`google-ads.md` s9 rule 6). Use the stricter of the platform file and this heuristic.
- Condition to scale (heuristic): CPA at or under target for several days with enough conversions to trust it (Meta file: 3+ days with 20+ conversions); the campaign is budget-limited; stock, team capacity and delivery capacity can absorb more orders.
- Step back, not off: when CPA breaks target after a step, return to the previous budget over 2-3 days rather than pausing.

**Horizontal (add reach)**
- Duplicate a winning ad set into a new ad set/campaign with its own budget instead of editing the live one (`meta-ads.md` s9).
- New audiences, new countries, new placements, new products, new creative concepts. Add creative volume before spend increases. Duplicates compete in the same auctions if audiences overlap; exclude the original audience or consolidate.
- New markets (KSA, UAE) need separate campaigns for currency, language and policy (`snapchat-ads.md` s3 large structure; `mena-and-egypt-notes.md` s3).

**Efficiency vs volume**: scale the winning layer first (prospecting winner), but monitor marginal CPA, not average CPA: the next 20% of budget buys more expensive conversions than the first 20%. Compare incremental spend with incremental conversions between two dates.

## 6. Pacing and end-of-month control
- `python3 scripts/ads_math.py pacing --budget-total 30000 --spent 12000 --days-total 30 --days-elapsed 10` shows expected spend 10,000, a +20% deviation and a daily budget of 900 to land the total. Use it every few days and at the end of the month.
- Overpacing early with a fixed monthly cap risks running dry on the best days; underpacing means the money is wasted on unused demand. Correct over several days, not in one jump (large budget moves affect learning).
- Platform quirks: Google monthly charge cannot exceed daily budget x 30.4 and day-off schedules changed on 2026-06-01 (`google-ads.md` s5); X/Google spend and conversions have reporting lag; TikTok lifetime budgets spend unevenly (`tiktok-ads.md` s5); LinkedIn lifetime pacing can overspend a day (`linkedin-ads.md` s5).
- Platform spend caps and account limits give a hard stop: set an account spending limit at the approved monthly amount where the platform supports it (Meta in `meta-ads.md` s2) and keep alerts on billing failures.
- Month-end: do not cut or raise sharply on the last days to "hit the number"; deviation of a few percent is normal. Report the pacing deviation and the reason (`reporting.md`).
- Agencies/clients: write the budget cap and the approval rule for increases in the plan; no budget increase without approval (SKILL.md).

## 7. Seasonal budgeting (Ramadan, White Friday)
Dates and patterns: `mena-and-egypt-notes.md` s7 (Ramadan 2027 expected about 8 February to 8 March 2027, moon dependent; White Friday 2026 on 27 November 2026; verify each year). No sourced CPM uplift exists for Egypt; check the account's own prior-year data.
- **Plan backwards**: lock offer and budget 8-10 weeks ahead; produce creative 6 weeks ahead; build warm audiences 3-4 weeks ahead; soft-launch 1 week ahead (`mena-and-egypt-notes.md` s7).
- **Ramp budgets before the peak** in steps so learning completes (the Meta file recommends this: `meta-ads.md` s12 seasonal case), instead of tripling on the peak day.
- **Allocate**: shift more to retargeting and conversion in the last days; keep a prospecting stream to refill pools. Reserve a post-peak reactivation slice; the weeks after Eid can be softer.
- **Don't**: change the optimization event, create many new ad sets on the peak day, or plan on last year's CPA (`meta-ads.md` s12).
- **Budget caps and stock**: tie spend to inventory and fulfilment capacity; stop-loss rule agreed in advance (when CPA exceeds X% of target for Y days, step back).
- **Day-parting** (post-iftar, late evening): treat as a hypothesis to test, not a rule (`meta-ads.md` s12). Lifetime budgets are required for ad scheduling on Meta.
- **Review queues grow**: submit creative early and keep spares.

## 8. Multi-currency, USD billing and EGP movement
- Account currency is fixed at creation on most platforms (X confirmed in `x-ads.md` s2 and `mena-and-egypt-notes.md` s1). Choose currency and time zone before the first dollar.
- Billing currency by platform: TikTok supports EGP or USD in Egypt; LinkedIn lists EGP, SAR, AED and USD; X bills Egypt, KSA and UAE in USD; Telegram uses a crypto token; Meta and Google EGP billing is `unverified` (`mena-and-egypt-notes.md` s1).
- **If the account bills in USD while revenue is in EGP**: a falling EGP raises the EGP cost of the same USD CPA, and the same USD budget buys the same impressions but costs more EGP. Targets set in USD go stale. Rules:
  1. State targets in the currency the client earns in (EGP), and also in the billing currency.
  2. Refresh the EGP-based target CPA and ROAS monthly or when the rate moves materially (`mena-and-egypt-notes.md` s1).
  3. Report with the FX rate and date used. Do not compare months at different rates without converting.
  4. Card fees, bank FX spreads and VAT sit on top of the invoice; the effective cost of a USD spend in EGP is higher than the converted platform number. Ask the accountant for the real landed cost and use that in break-even (`mena-and-egypt-notes.md` s1 for VAT and e-invoicing questions).
  5. For a price-list in EGP with USD input costs, margin moves with the rate; recompute break-even whenever the price or the rate changes.
- Budgets in local currency are rounded by platforms; confirm the minimum in the account currency.
- Payment resilience: two valid payment methods, billing alerts, and a plan for a declined charge (`mena-and-egypt-notes.md` s1; `policy-and-account-health.md` s4).

## 9. When to cut
Cut (pause the ad, then the ad set, then the campaign) in this order; use thresholds relative to target CPA (`optimization-playbook.md` s5).
- Ad: spend above about 2-3x target CPA with no conversions and below-sibling engagement, after tracking is verified. Cut the ad, not the ad set.
- Ad set: has had its learning window and several multiples of CPA spend, remains well above break-even CPA and new creative did not change it.
- Campaign: negative contribution after delivered-order reconciliation across two full conversion cycles, or tracking cannot be trusted and cannot be fixed this week.
- Immediate pause (with user approval): policy action risk on an account, payment failure loops, a broken landing page, stock out, or a legal/brand-safety incident.
- Cut vs fix: if the cause is a broken pixel, stock, or landing page, fix the cause; pausing a healthy campaign resets momentum.
- Hold budget when uncertain: reallocate to winners in small steps rather than deleting everything at once.

## 10. Quick reference of scripts
| Task | Command |
|---|---|
| Break-even | `ads_math.py breakeven --price --cogs [--other-var] [--cod-delivery-rate] [--return-rate]` |
| Budget to buy N conversions | `ads_math.py budget --target-cpa --conversions-needed [--days]` |
| Minimum test budget | `ads_math.py test-size --cpa [--variants] [--events-per-variant]` |
| Scale schedule | `ads_math.py scale --budget [--step] [--steps]` |
| Pacing | `ads_math.py pacing --budget-total --spent --days-total --days-elapsed` |
| COD reality | `ads_math.py cod --orders --delivered-rate --aov --spend` |

## 11. Worked example (illustrative, not a benchmark)
Break-even CPA 283.5 EGP per placed order (price 1,000, COD delivery 70%, returns 10%, see `funnel-and-objectives.md` s10). Target CPA 210.
1. Volume method: 50 purchases per week at 210 = 10,500 EGP per week, about 1,500 per day. If the client budget is 700 per day, a purchase-optimized ad set is under-sized: switch the event to initiate checkout (cheaper, more frequent) and judge with the confirmed-order rate.
2. Bid rung: start at lowest cost. After two stable weeks with CPA inside target, test a cost cap set at about the recent CPA, in a duplicate ad set, not on the live one.
3. Scale: if CPA holds at or under 210 for several days, step 20% every 3 to 4 days (`ads_math.py scale`), watching marginal CPA; stop when CPA exceeds the 20% tolerance and step back.
4. Month-end: check `ads_math.py pacing`; correct over several days.
5. FX: if the account bills in USD and the EGP weakens 10%, the EGP target of 210 now needs a USD CPA about 9% lower to keep the same EGP cost; re-run the break-even in EGP at the new landed cost and report the rate used.

## Sources
- Platform files (dated 2026-10-19) section 5 for bid, budget and learning facts: Meta, Google, TikTok, Snapchat, LinkedIn, X, Pinterest, YouTube.
- `mena-and-egypt-notes.md` s1, s7. Scaling steps, cushions and split ratios are heuristics. No benchmark cited.
