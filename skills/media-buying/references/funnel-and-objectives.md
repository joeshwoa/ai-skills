# Funnel and objectives
Purpose: choose the campaign objective and funnel structure that fit the goal, the budget and the available conversion volume.
Last updated: 2026-10-19

Platform objective names, optimization goals and per-platform structure live in `platforms/*.md` section 3 (and section 5 for bidding). This file gives the platform-neutral decision logic. Numbers marked **heuristic** are judgment rules with their reasoning, not platform rules. No CPM/CTR/CPA/ROAS benchmarks are stated here; derive targets from the client's own economics (`scripts/ads_math.py breakeven`).

## 1. The one rule that decides most choices
Optimize for the lowest-funnel event that can still collect enough volume to learn. Reason: delivery systems learn from the events you count; a rare event (a purchase at 3 per week) gives the optimizer almost no signal, while an upstream event (add to cart, lead) is plentiful but correlates less with revenue. Move up one step only when the lower event cannot reach the volume the platform file asks for (Meta and TikTok files give their own thresholds in section 5; Google Smart Bidding thresholds are in `platforms/google-ads.md` section 5).

Quick volume check before picking the event:
1. Target CPA = break-even CPA x safety margin (`ads_math.py breakeven`, then decide the margin; heuristic: aim 20-30% under break-even so there is profit and room for noise).
2. Weekly events needed = platform threshold (for example the roughly 50 events per week that `platforms/meta-ads.md` cites for learning exit).
3. Weekly budget needed = events x target CPA (`ads_math.py budget --target-cpa A --conversions-needed N --days 7`).
4. If the real budget is below that: choose the next event up the funnel, or fewer ad sets, or a longer window. Do not run the lower event with an under-sized budget and call the result a test.

## 2. Goal to objective map (platform-neutral)
| Business goal | Funnel stage | Neutral objective | Optimization event (preferred -> fallback) | Where the platform names are |
|---|---|---|---|---|
| Sell products online | conversion | Sales / Conversions | purchase with value -> initiate checkout -> add to cart | `meta-ads.md` s3 (Sales), `tiktok-ads.md` s1/s3, `snapchat-ads.md` s3 (SALES), `pinterest-ads.md` s3 (Sales), `google-ads.md` s3 (Shopping, PMax, Search) |
| Collect leads | conversion | Leads | qualified lead (CRM-fed) -> lead form submit -> landing page view | `meta-ads.md` (Leads), `linkedin-ads.md` s3 (Lead Generation), `snapchat-ads.md` (LEADS), `tiktok-ads.md` (Lead generation), `google-ads.md` (Search leads) |
| Get chats (WhatsApp, Messenger) | conversion | Leads or Engagement with a messaging destination | qualified conversation (fed back) -> conversation started | `meta-ads.md` s7 and s12 (click-to-WhatsApp); `mena-and-egypt-notes.md` s5 |
| Drive intent-led demand | capture | Search / Shopping | conversions on the site | `google-ads.md` |
| Bring people who do not know you yet | prospecting | Reach / Video views / Traffic with a quality event | video views, landing page views, reach | `youtube-ads.md` s3, `meta-ads.md` s3, `tiktok-ads.md`, `x-ads.md` s3 |
| Re-engage visitors, carts, engagers | retargeting | Sales/Leads limited to a warm audience | purchase or lead | each platform's audiences section (s4) |
| Install an app | conversion | App promotion | install -> in-app registration -> in-app purchase | `meta-ads.md`, `google-ads.md` s3 (App campaigns), `tiktok-ads.md`, `snapchat-ads.md` (APP_PROMOTION) |
| Reach professionals or accounts | prospecting + conversion | Lead Generation / Website Conversions | form submit or qualified lead | `linkedin-ads.md` s3 |
| Grow a Telegram channel or bot | conversion (native) | Platform-native | joins or starts | `telegram-ads.md` s3 |

Rules:
- Traffic and Engagement objectives optimize for clicks and reactions, which often come from people who never buy. Use them only when no conversion event is possible (new site with no tracking, a platform with no pixel such as Telegram), and measure on a downstream event captured elsewhere (CRM, GA4). Landing page views are a better traffic proxy than raw link clicks (`meta-ads.md` s3).
- Awareness objectives buy reach and recall. They are justified when the brand is unknown, the cycle is long, or retargeting pools are too small. They are not justified when the budget cannot also feed a conversion layer (section 4).
- When a platform renames objectives (Pinterest and Meta both did), map by what the objective optimizes, not by the label. Check the platform file's Last verified date.

## 3. Full-funnel structure by budget
"Budget" here means what one conversion ad set needs to leave learning at your target CPA (section 1 step 3), not an absolute amount. Thresholds are **heuristic** unless a platform file states them.

| Tier | Test: can the budget feed N events per week per ad set? | Structure | Reasoning |
|---|---|---|---|
| Small | Only one ad set reaches the platform threshold | 1 campaign, 1 ad set, 3-5 distinct creatives, lowest viable event, no separate retargeting campaign (retargeting pool is too small to deliver) | Fragmenting a small budget starves every ad set; see `platforms/meta-ads.md` s3 for the same logic |
| Medium | 2-4 ad sets reach the threshold | Prospecting campaign (broad or lookalike) + retargeting campaign (site visitors, engagers) + a small creative-testing slot inside prospecting | Separate reporting for cold vs warm so retargeting does not flatter blended CPA |
| Large | 5+ ad sets can each exit learning | Testing campaign graduates winners into scaling campaigns; split by country/language/product/margin; always-on retargeting plus periodic reactivation | Testing is isolated so scale budgets are not disturbed by new ads (`optimization-playbook.md`) |

Per-platform small/medium/large recommendations are in each platform file's section 3; follow them for platform-specific limits (for example LinkedIn audiences of 50,000+ members, Google brand isolation).

## 4. Prospecting vs retargeting split (heuristic)
- Starting split: **80-90% prospecting / 10-20% retargeting** for e-commerce and lead gen once the site has steady traffic. Reasoning: retargeting converts warm people at a lower cost but only as many as prospecting feeds in. A retargeting share that is too high drains the pool, drives frequency up, and the account looks efficient while growth stalls.
- Raise the retargeting share only when the pool is large (retargeting frequency stays low at the spend) and prospecting is saturated. Cut it when frequency in the retargeting ad set keeps climbing or CPA rises while pool size shrinks.
- Brand search is retargeting-like (people already know you). Keep it in its own Google campaign so its cheap conversions do not hide non-brand performance (`platforms/google-ads.md` s9 rule 12).
- Measure each layer with its own CPA and a combined view. Report blended (`reporting.md`); a cold CPA above target with a retargeting CPA far below target usually means the prospecting layer is feeding the whole business and must not be cut because retargeting "looks better".
- Exclusions: exclude recent purchasers/converted leads from prospecting and from retargeting; exclude employees on LinkedIn (`platforms/linkedin-ads.md` s3). Overlapping audiences make the same people compete against themselves.
- Window lengths: pick retargeting windows by pool size, not by habit. Small sites use longer windows so the audience is deliverable; the platform audience sections list the maximum windows.

## 5. Variants by business model
**E-commerce (prepaid or card)**
- Event: purchase with value and currency. Sequence: prospecting -> add-to-cart/checkout retargeting -> post-purchase (cross-sell, replenishment).
- Feed-based formats (Shopping, catalog, dynamic product ads) once the product feed is clean; platform names in `google-ads.md`, `meta-ads.md`, `snapchat-ads.md`, `pinterest-ads.md`.
- Judge on ROAS or MER against break-even ROAS (`reporting.md` for MER).

**E-commerce with cash on delivery (Egypt and Gulf)**
- The order event fires before delivery, so the platform optimizes toward orders that may be refused. Report three layers (placed, confirmed, delivered) and use `ads_math.py cod` and `ads_math.py breakeven --cod-delivery-rate ... --return-rate ...`.
- Prefer sending a confirmed-order event to the platform (server-side) once volume allows (`tracking-and-attribution.md` s6). Until then, optimize on orders but judge on delivered economics. Details: `mena-and-egypt-notes.md` s6.
- Add friction against fake orders (phone verification, address checks) before scaling spend.

**Lead generation (services, education, real estate, clinics)**
- Event: form lead is cheap and noisy; qualified lead is the real signal. Feed the CRM stage back to the platform (`tracking-and-attribution.md` s5). Measure cost per qualified lead and cost per sale, not CPL alone.
- Speed to first contact matters; an unanswered lead is a wasted click. Set an SLA before launching (`mena-and-egypt-notes.md` s5).

**Local business (single city, walk-in or call)**
- Small geography means small pools: use one campaign, one ad set, radius/city targeting, click-to-call or click-to-WhatsApp or a short form. Measure calls, chats and store visits where available; ask "how did you hear about us". Judge over 2-4 weeks, not days.
- Do not split a tiny budget between platforms; pick the one where the customers are (check their own analytics).

**App**
- Install campaigns bring the cheapest event and the weakest quality; optimize for an in-app event (registration, first purchase) as soon as volume exists. Measurement on iOS is limited by platform privacy rules; see each platform file's tracking section. A Play/App Store listing and an attribution partner must exist first.

**B2B**
- Low volume, high value: optimize for qualified leads or meetings, not clicks. Sales cycle is weeks to months, so use long evaluation windows, account lists, and CRM-stage import. LinkedIn is the precision channel with a high cost per lead (`platforms/linkedin-ads.md` s1); Google Search captures active demand; Meta/YouTube can warm audiences for a retargeting layer.
- Judge by pipeline/opportunities, with a lag, never by form fills alone.

## 6. WhatsApp and Messenger click-to-chat funnels
- Structure: ad -> chat opens with a prefilled or welcome message -> qualification questions -> human or bot handoff -> sale or booking. Platform setup (objective, welcome message, ice breakers, the `ctwa_clid` click ID) is in `platforms/meta-ads.md` s7 and s12; messaging cost rules and the free entry window are in `mena-and-egypt-notes.md` s5.
- What the platform counts is a conversation started. Add stage events: qualified, quote sent, purchase. Send them back where supported so the platform can optimize beyond "conversation" (`tracking-and-attribution.md` s5).
- Funnel capacity is the constraint: if replies take hours, more ad spend only makes more unanswered chats. Cap budget by team reply capacity (heuristic: leads per day your team can answer within the SLA).
- Cost per conversation is not comparable to CPL or CPA. Compare cost per qualified conversation and cost per sale.
- Tag each chat with source, campaign and creative (message prefix or click ID) so the CRM can attribute sales (`tracking-and-attribution.md` s3).

## 7. When NOT to run ads
Stop and fix the underlying problem if any of these is true. Spending anyway buys data about a broken funnel.
- **Unit economics do not work**: break-even CPA is below any plausible acquisition cost (`ads_math.py breakeven` shows margin too thin after delivery rate and returns). Fix price, margin or offer first.
- **No tracking**: no verified conversion event and no UTMs (`tracking-and-attribution.md`). Hard rule in SKILL.md.
- **Landing page or checkout is broken**: slow, errors, no mobile layout, no visible contact or payment path. Run `templates/launch-checklist.md`.
- **No capacity to fulfil or reply**: stock out, no delivery coverage, no one answering WhatsApp.
- **Policy-restricted category without approval or licence** (finance, health, gambling, crypto, alcohol): get certification first (`policy-and-account-health.md`).
- **Offer has no demonstrated demand**: nobody buys even from organic traffic or direct outreach. Validate with warm channels before paying for cold traffic. (Paid ads accelerate a working offer; they rarely create one.)
- **Budget too small for the chosen event**: see section 1. Either upgrade the budget, move up the funnel, or switch to a cheaper channel (organic, referral, direct outreach; organic content belongs to `social-media-manager`).
- **Payment method cannot survive one decline**, or the account has an unresolved restriction: the campaign will stop mid-test (`mena-and-egypt-notes.md` s1).
- **Post-peak or stock-limited timing**: right after a sale event when the audience is exhausted, or when the product will sell out in days.

## 8. Decision procedure for an agent
1. Write the goal as one measurable event and its value to the business.
2. Compute break-even and target CPA/ROAS.
3. Check the event's weekly volume at the budget (section 1). Pick the event.
4. Choose the tier (section 3), then the channel using `mena-and-egypt-notes.md` s3 and the platform file's "When to use it".
5. Pick the structure from the platform file section 3 and the split from section 4.
6. Run `tracking-and-attribution.md` before spend and `templates/launch-checklist.md`.
7. Write the plan in `templates/media-plan.md`; show the change list to the user for approval before anything goes live.

## 9. Metrics to read per funnel stage
| Stage | Read first | Then | Do not judge on |
|---|---|---|---|
| Prospecting (awareness/video) | reach, frequency, cost per landing page view or 3-second view | hook rate, hold rate, new-visitor share in analytics | CPA from this layer alone; it feeds other layers |
| Prospecting (conversion) | CPA vs target, CVR click to event | CPM, link CTR, frequency | single days; wait for the platform file's wait rule |
| Retargeting | CPA, frequency, pool size trend | share of conversions that were view-through | ROAS in isolation (it claims credit for people who would have bought anyway) |
| Capture (Search/brand) | impression share, CPA, search terms | brand vs non-brand split | blended CPA with brand mixed in |
| Messaging | cost per qualified conversation, first-reply time | cost per sale | raw conversations count |

## 10. Worked example (illustrative numbers, not benchmarks)
A Cairo home-goods store sells at 1,000 EGP, product cost 500, packaging and COD fee 50, delivery rate 70%, returns 10%.
- `python3 scripts/ads_math.py breakeven --price 1000 --cogs 500 --other-var 50 --cod-delivery-rate 0.7 --return-rate 0.1` gives a break-even CPA of 283.5 per placed order. Target CPA with a 25% cushion is about 210.
- Purchase event at 210 EGP and about 50 events per week needs about 10,500 EGP per week (`ads_math.py budget --target-cpa 210 --conversions-needed 50 --days 7`). If the client has 4,000 EGP per week, purchases cannot exit learning on one ad set: run one ad set on initiate checkout, judge on cost per checkout and the CRM-confirmed rate, and revisit the purchase event when the budget grows.
- Result: small tier, one campaign, one ad set, 4 distinct creatives, a WhatsApp confirmation step, a weekly delivered-orders reconciliation.

## Sources
Derived from the platform files in this skill (each dated 2026-10-19 and carrying its own source list) and `mena-and-egypt-notes.md`. No external benchmark is cited. Funnel split and tier thresholds are heuristics.
