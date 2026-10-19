# Optimization playbook
Purpose: diagnose under- and over-performing campaigns with ordered checks, and operate accounts on a fixed rhythm with thresholds tied to break-even.
Last updated: 2026-10-19

Platform-specific wait rules, "do not touch" lists and cases are in `platforms/*.md` section 9 and 12; use them for platform detail. Thresholds here are **heuristics** expressed relative to the client's break-even CPA (`scripts/ads_math.py breakeven`), never fixed currency numbers. Do not apply any change without user approval (SKILL.md); produce a change list: what, where, why, expected effect, rollback condition.

## 1. Method
1. State the symptom with numbers and the date range. Compare the same window and the same attribution setting.
2. Walk the checks in order. Stop at the first broken layer and fix it before touching later layers: **delivery/status -> tracking -> economics and landing page -> audience and bid -> creative**. Reason: upstream faults make downstream numbers meaningless (a tracking fault looks like a creative problem).
3. Change one thing at a time unless a fault is clearly independent (for example, fixing a broken pixel and replacing a rejected ad).
4. Wait the platform's window before judging the change; log it (section 7).
5. If the cause is outside the ad account (price, stock, site, seasonality, a competitor), say so; do not bid your way out of a product problem.

## 2. Standing pre-checks (run first on any symptom)
- Status: ads approved? any ad/ad set in review, rejected, limited, paused by rule or schedule? Payment current? Account restricted? (`policy-and-account-health.md`)
- Tracking: platform event count vs shop/CRM for the same days is in the usual ratio (`tracking-and-attribution.md` s4 and s9).
- Edits: what changed in the last 7 days? (change log) Significant edits reset learning; check the platform's "last significant edit" indicator where it exists (`meta-ads.md` s5).
- Context: price, promotion, stock, delivery coverage, competitor activity, payday, holiday, news, site release.
- Data maturity: conversions still arriving (lag), too few events to judge (use `ads_math.py abtest` if comparing), learning phase.

## 3. Diagnosis tree by symptom
Each block: ordered checks, then decision.

### 3.1 No delivery (zero impressions)
1. Review status: pending, rejected, limited by policy -> fix per `policy-and-account-health.md` s2-s3.
2. Account: payment failure, spend limit reached, billing threshold, account restriction.
3. Schedule: start date in the future, end date passed, ad schedule excludes now, campaign group or parent paused.
4. Audience: too small or contradictory exclusions, wrong location/language, placements all disabled, minimum audience size (LinkedIn in `linkedin-ads.md` s3).
5. Bid/budget: bid cap or cost cap far below the market (a bid of 0 means no delivery on LinkedIn manual bidding), budget below the minimum (`platforms/*.md` s5).
6. Eligibility: restricted category, special ad category mis-declared, app/catalog/feed not approved.
Decision: fix the first failing item; do not raise budget while status or billing is broken.

### 3.2 Delivery but little or no spend (under-delivery)
1. Budget-limited vs bid-limited vs audience-limited (status column in the platform).
2. Cost cap, target CPA or ROAS floor too tight (the Google 2026-08-17 change makes tight targets throttle budget-limited campaigns: `google-ads.md` s5). Loosen to the recent actual CPA or switch to lowest cost.
3. Audience exhausted (frequency high, reach flat): widen, add lookalikes/broad, new creative.
4. Learning limited: raise event volume (`bidding-and-budgets.md` s4).
5. Creative ineligible for some placements or low relevance; add formats.
6. Seasonal competition: market demand rose; the bid is no longer competitive.
Decision: first remove constraints one at a time (cap -> audience -> placements); then add budget.

### 3.3 High CPM
1. Compare with this account's own history, same audience and placements; no external benchmark (`SKILL.md`).
2. Audience too narrow or heavily layered; auction competition (seasonal peaks); placement mix shifted to expensive inventory.
3. Low creative engagement (quality/relevance rank in platform diagnostics) raises costs; fatigue (frequency up).
4. Objective/optimization event change; new targeting restrictions (special categories).
5. Currency effect: USD-billed account with a falling EGP.
Decision: if CTR and CVR are healthy, a high CPM can be acceptable; judge on CPA. Fix creative and audience breadth before adjusting bids.

### 3.4 Low CTR
1. Hook weak (hook rate, first 3 seconds) -> test hooks (`creative-testing.md`).
2. Message-audience mismatch or wrong placement (e.g., an Arabic ad shown to an English-device audience; RTL/layout issues: `creative-testing.md` s9).
3. Fatigue: CTR down over a week with frequency up.
4. Format mismatch: wrong aspect ratio, text outside safe zone, no sound-on design.
5. Metric trap: use link CTR, not all-clicks CTR (`meta-ads.md` s10).
Decision: low CTR with good CVR and CPA at target is not a problem; fix only if CPA suffers or volume is capped.

### 3.5 Clicks but no conversions
1. Tracking: event fires? (`tracking-and-attribution.md` s9 A). Compare landing page views vs link clicks: a big gap means slow page or accidental clicks.
2. Landing page: speed on mobile, message match with the ad, price shown, trust cues, form length, working checkout, payment methods, COD option, WhatsApp button.
3. Traffic quality: placements (Audience Network, in-app browsers), bot/accidental clicks, objective set to traffic/engagement, audience too broad for a niche offer.
4. Offer: price, shipping fee, delivery time, reviews.
5. Funnel capacity: leads not answered, stock out.
6. Time since launch: under one conversion cycle.
Decision: fix page/offer/tracking before changing ads. If CTR is high and CVR near zero, suspect curiosity or misleading creative.

### 3.6 CPA spike (CPA suddenly up)
1. Compare day-over-day only after allowing for lag; look at 3-7 day windows. Wait 48 hours before acting unless tracking is broken (`meta-ads.md` s12).
2. Edits in the last 7 days (budget jump, new ads, event change, bid change) -> restore the last stable setting if the cause is clear.
3. Tracking outage/dedup change (A/B/C of `tracking-and-attribution.md` s9).
4. Creative fatigue (frequency, CTR trend).
5. Landing page/price/stock/shipping/payment change, promo ended.
6. Competition/season, payday, holiday.
7. Attribution setting or window change (Meta March 2026 per `meta-ads.md` s7; do not compare across).
Decision: reverse the cause if known; otherwise hold budget, add new creative, and re-evaluate after the platform's wait window. Do not cut and rebuild.

### 3.7 ROAS drop
1. Separate AOV from conversion rate from CPA: ROAS = AOV x CVR x clicks / spend; find which moved (`ads_math.py metrics --revenue`).
2. Tracking: value parameter missing or wrong currency; COD: placed vs delivered mix changed (`ads_math.py cod`).
3. Mix: more retargeting or brand search share (flattering) or less; new low-AOV product; discounts.
4. Returns/refusals rise (delivered-order ROAS falls first).
5. Demand and creative as in 3.6.
Decision: act on delivered-order economics, not platform ROAS alone (`reporting.md`).

### 3.8 Frequency climbing
1. Audience size vs spend: small audience with rising spend saturates quickly.
2. Retargeting pool depletion (too much retargeting share: `funnel-and-objectives.md` s4).
3. Creative count too low.
Decision: widen audience, add new concepts, cap or lower retargeting spend, exclude recent converters, reduce budget on the saturated ad set. Frequency is a symptom; act only if results decline or comments turn negative (heuristic).

### 3.9 Learning limited / stuck in learning
1. Event volume below the platform threshold at this budget: `ads_math.py budget`.
2. Too many ad sets/ads splitting events; frequent edits resetting learning; cap too tight.
Decision: consolidate, move up the funnel, widen the audience, loosen caps, raise budget modestly, stop editing.

### 3.10 Good ads but bad sales
(Platform metrics look healthy but the business has few sales.)
1. Funnel after the click: site speed, checkout errors, payment failures, COD confirmation process, lead response time (`mena-and-egypt-notes.md` s5, s6).
2. Traffic quality: low-intent clicks (view-through credited, cheap-click placements), fake orders, duplicate leads.
3. Measurement: platform conversions inflated by duplicates or view-through; reconcile with CRM and delivered orders (`tracking-and-attribution.md` s4, s6).
4. Offer/pricing vs competitors; stock; delivery promise vs reality.
5. Sales process: unqualified leads, missed calls, slow follow-up.
Decision: this is rarely an ad-tuning problem; run the funnel audit and show the user where the people drop off.

## 4. Operating rhythm
**Daily (5-10 minutes, no optimization changes unless broken)**
- Billing/payment, policy status (rejections, limited ads), spend vs pacing, delivery anomalies (zero spend, spike), tracking health (event counts present).
- Do not judge or edit on one day of data.

**Weekly**
- Performance vs target CPA/ROAS by campaign, ad set and ad, on a weekly window with mature conversions.
- Winners/losers by the thresholds in section 5; creative status (fatigue signals, pipeline of new concepts); search terms (Google) and placement reports; frequency and audience saturation.
- Reconcile platform vs shop/CRM; COD three layers (`tracking-and-attribution.md` s6).
- Decide: scale, hold, cut, iterate; prepare the change list for approval; update the test log and change log.
- Send `templates/weekly-report.md`.

**Monthly**
- Break-even and target refresh (price, COGS, delivery rate, FX).
- Budget allocation across platforms and funnel stages; pacing close.
- Test roadmap and learnings; creative library audit; naming and tracking audit; account health review (`policy-and-account-health.md`); roles/access review.
- Reporting pack and plan for next month (seasons, launches).

## 5. Kill / hold / scale / iterate thresholds (relative to break-even)
Let BE = break-even CPA (per placed order, adjusted for delivery and returns), T = target CPA (heuristic T = 0.7 to 0.8 x BE). Reasoning: decisions based on multiples of CPA scale with the product's economics; fixed amounts do not transfer between clients or currencies. All require tracking verified and a mature window.

| Situation | Evidence needed | Action |
|---|---|---|
| Ad has spent > 2-3 x T, zero conversions, weak engagement vs siblings | spend multiple reached; tracking OK | Pause the ad (not the ad set) |
| Ad set past learning, CPA > BE after a full window, with new creative tried | at least one full conversion cycle and several x T of spend | Cut or restructure; do not scale |
| CPA between T and BE | enough events | Hold; iterate creative/landing page; do not scale |
| CPA <= T for several days with enough events (Meta file example: 3+ days, 20+ conversions) | stable | Scale: +20% steps every 3-4 days, tolerance 20% over T (`ads_math.py scale`) |
| CPA <= 0.8 x T with volume | stable and capacity available | Scale faster only within platform limits (`platforms/*.md` s5) or duplicate horizontally |
| Strong upstream metrics, low volume on the final event | below event volume | Consider optimizing one step up the funnel |
| Fatigue signals, CPA rising within the allowed band | frequency/CTR trend | Iterate: add new concepts; do not edit the winner |
| ROAS (platform) above target but delivered ROAS below | COD reconciliation | Treat as below target; fix confirmation/delivery process or the event |
For leads, replace CPA with cost per qualified lead against allowable cost (`bidding-and-budgets.md` s1). For ROAS-based accounts, express T as a ROAS floor against break-even ROAS.

## 6. What not to change during learning
Applies to any ad set/campaign in learning or inside its platform wait window (lists in each platform file s9):
- Optimization event or conversion goal set; bid strategy or large target changes; targeting/audience (including exclusions); creative text/media inside a live ad (add a new ad instead); large budget jumps; pausing for days then restarting; many new ads at once; landing page main URL on Google (`google-ads.md` s9 rule 11).
- Allowed: renames; small budget increases (see `bidding-and-budgets.md` s4); fixing a tracking fault or policy rejection (log it and note the effect on learning).
- Emergency exception: pause when an ad violates policy, a price is wrong, stock is out, a tracking fault is wasting spend, or a legal/brand-safety incident occurs.

## 7. Change log discipline
Every change gets a row (use the Changes section of `templates/test-log.md`): date and time, platform and object (campaign/ad set/ad ID and the standard name from `scripts/naming.py`), the change (before -> after), reason/hypothesis, expected effect and how to detect it, evaluation date (after the wait window), rollback condition, approver, result.
Rules:
- No change without a row; no row without a reason.
- Review the log before diagnosing a spike; most spikes line up with an edit.
- Automated rules and API scripts write to the same log with a run ID; automated changes follow the platform file's agent rules (once-a-day budget changes, no editing live creative; `meta-ads.md` s11).
- Evaluate each change on its evaluation date and mark: kept, rolled back, inconclusive.
- Keep the log in the client's workspace, not in chat memory.

## 8. Common mistakes
- Reacting to one day; changing several levers at once; scaling on platform ROAS in COD markets; judging ads by CTR alone; refreshing winners instead of adding next to them; raising budget to "get data" on a broken funnel; editing live ads; adding ad sets to a small budget; comparing periods across an attribution or tracking change; chasing a result for a campaign the account cannot support economically.

## Sources
- Platform files section 9 (optimization) and 12 (cases), dated 2026-10-19, each with its own sources: Meta, Google, TikTok, Snapchat, LinkedIn, X, Pinterest, YouTube, Telegram.
- `tracking-and-attribution.md`, `bidding-and-budgets.md`, `creative-testing.md`. Thresholds are heuristics; no external benchmark is cited.
