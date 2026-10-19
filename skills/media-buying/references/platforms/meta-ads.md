# Meta Ads — rules and playbook
Last verified: 2026-10-19

Scope: Facebook, Instagram, Messenger, WhatsApp and Audience Network placements bought through Meta Ads Manager / Marketing API. Source key: **[official]** = Meta help center, developer docs or policy page; **[secondary]** = third-party article that reports Meta's rule; **[practitioner]** = observation, not an official rule; `unverified` = could not confirm. Note for agents: Meta's Business Help Center (facebook.com/business/help) could not be fetched programmatically during this research (robots restriction), so help-center rules below are cited via secondary reports unless marked official. Re-check the "Last significant edit" column and Ads Manager previews before acting on them.

## 1. When to use it
- Strengths: largest reach in Egypt; strong for demand generation, e-commerce, lead generation, app installs and conversation-based (WhatsApp / Messenger) sales. Broad automated delivery (Advantage+) works best with enough conversion volume and several distinct creatives.
- Weaknesses: results depend on pixel / Conversions API data quality; no keyword intent (unlike search); policy review is strict on health, finance, "personal attributes" and landing pages; ad accounts can be restricted with slow appeals.
- Best objectives (ODAX objective names): Sales (OUTCOME_SALES) for purchases / catalog; Leads (OUTCOME_LEADS) for instant forms, website leads or messaging leads; Engagement for conversations / page growth; Traffic only when no conversion event is feasible; Awareness for reach / video views; App promotion for installs.
- Egypt / MENA relevance (DataReportal Digital 2026, published 2025-11-08, figures are Meta-reported ad-audience estimates, not MAU):
  - Egypt: Facebook ad reach 51.6M (43.4% of population), Instagram 21.7M (18.2%). Source: https://datareportal.com/reports/digital-2026-egypt
  - Saudi Arabia: Facebook 17.7M (50.8%), Instagram 18.2M (52.4%). Source: https://datareportal.com/reports/digital-2026-saudi-arabia
  - Interpretation: in Egypt, Meta is the broadest reach channel (Facebook > Instagram); in KSA, Instagram is larger than Facebook and Snapchat / TikTok are strong alternatives.
- Benchmarks: no reliable, current, public CPM / CTR / CPA benchmark for Egypt or MENA was found. Do not quote any; derive targets from the client's own margin and past data.

## 2. Account, billing and access
- Structure: Business portfolio (formerly Business Manager) -> Ad account(s) -> Pages / Instagram accounts / WhatsApp Business accounts / datasets (pixel). People get roles per asset (partial access) or full control. Agencies get access via "Partners" in Business Settings; ask the client to share the ad account, Page, dataset and catalog, and keep the client as portfolio owner.
- Dataset = pixel + Conversions API events in one object. One dataset per Page is the limit for business-messaging events [official, Conversions API for business messaging doc].
- Business verification: needed for some features and for apps requesting advanced API access to sensitive data [official: https://developers.facebook.com/docs/marketing-api/overview/authorization]. Verification time (reported 2-5 business days) and its effect on restriction leniency are [secondary] / `unverified`.
- Two-factor authentication for admins and at least two valid payment methods are [practitioner] hygiene, not Meta requirements.
- Payment methods and currency for Egypt: Meta's per-country payment table exists in the help center (https://www.facebook.com/business/help/212763688755026 and https://www.facebook.com/business/help/1622234084485141 "Egypt") but could not be read here. Do not assume the accepted methods: `unverified`. Practitioner reports say Egyptian-issued cards sometimes fail on international transactions and that virtual USD cards are commonly used; treat as [practitioner]. Whether EGP is selectable as ad account currency: a LinkedIn article title says Meta "now accepts payment in Egyptian pound" but its date and details could not be read: `unverified`. Currency of an ad account cannot be changed after creation (widely known; `unverified` here), so confirm currency and time zone before creating the account.
- Billing model: postpaid by threshold and monthly bill date; the starting threshold depends on country, currency and payment method and rises with spend [secondary: https://kb.orbee.com/billing-meta-ads]. A failed payment can restrict the account [practitioner]. Account spending limits and daily spend limits exist (API: spend_cap on campaigns, account spend limit changeable at most 10 times per day via API) [official rate-limit page].
- Tax (high level, not tax advice): Egypt's Tax Authority guidance applies 14% VAT to digital services supplied by foreign providers to Egyptian consumers, B2B handled by reverse charge (vatcalc summary of ETA guidance, Aug 2023: https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/). An Egyptian accountancy article (ECPA, 2025-01-30) says social ads must be documented with e-invoices and that foreign platforms are expected to withhold tax: https://ecpa-eg.com/en/eg/articles/coding-of-ads-on-social-media-for-the-egyptian-tax-authority. Whether and how Meta itself charges VAT on an Egyptian advertiser's invoices: `unverified`. Tell the client to confirm with their accountant.
- API access: Marketing API access tiers are now "Limited Access" (default, dev-only, heavily rate-limited) and "Full Access" (after App Review; 500 API calls in 15 days with error rate under 15% to keep it). Managing only your own ad accounts needs only standard permission access; managing other people's ad accounts needs advanced access to ads_read / ads_management. [official: https://developers.facebook.com/docs/marketing-api/overview/authorization]

## 3. Campaign structure
Hierarchy: Campaign (objective, special ad category, buying type, optional campaign budget / Advantage+ campaign budget) -> Ad set (budget, schedule, audience, placements, optimization goal, attribution setting, bid strategy) -> Ad (creative, text, destination, tracking).

Objectives (API enum) [official: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group]: OUTCOME_AWARENESS, OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT, OUTCOME_LEADS, OUTCOME_APP_PROMOTION, OUTCOME_SALES. Legacy objectives (CONVERSIONS, APP_INSTALLS, REACH...) were deprecated from API v17.0.
- What each optimizes: the ad set optimization goal inside the objective decides. Sales -> purchases / value / add to cart etc. (needs a pixel or CAPI event, or conversations); Leads -> leads on site / instant form / calls / conversations; Traffic -> link clicks or landing page views (landing_page_views is a better proxy than link clicks); Engagement -> conversations, post engagement, video plays; Awareness -> reach / ad recall.
- Buying types: AUCTION (default) or RESERVED (Reach & Frequency, not available for housing/employment/credit categories). All ad sets in a campaign must match.
- Advantage+ campaigns (Sales, App, Leads): the manual/automated choice is gone in the Sales/App/Leads flow; Advantage+ audience, placements and campaign budget are on by default and can be overridden, which may turn Advantage+ off for that component [secondary: https://www.jonloomer.com/advantage-plus-sales-app-leads-campaigns/]. Hard audience controls: location, minimum age, excluded custom audiences, languages. Age maximum, gender, included custom audiences and detailed targeting are suggestions only. Legacy ASC had an "existing customer budget cap" that was not offered in the new flow as of that article; to limit retargeting, split into separate ad sets / campaigns. Up to 50 ads per ad set in Advantage+ Sales. All of this changes often: `unverified` for 2026 UI details.
- What Meta automates: audience expansion, placement allocation, budget allocation across ad sets, creative enhancements (Advantage+ creative). It does NOT choose your offer, event, or landing page.
- Recommended structure (rules of thumb; practitioner unless stated):
  - Small budget (below what 1 ad set needs for ~50 events/week, see section 9): ONE campaign, ONE ad set, 3-5 distinct creatives, optimize for the lowest-funnel event that can still reach ~50/week; if impossible, move one step up the funnel (purchase -> add to cart / initiate checkout; lead -> instant form or conversation).
  - Medium: separate prospecting (Advantage+ / broad) and retargeting (website + engagement audiences) campaigns; 1-3 ad sets each; test creatives inside a dedicated testing ad set or campaign.
  - Large: add a creative-testing campaign that graduates winners into scaling campaigns; separate campaigns by country / language / product line; keep a fixed naming convention (objective_audience_creative_date) for automations.
- Fewer ad sets and fewer ads concentrate data: Meta's own guidance (as reported) is that many ads and ad sets make the system learn less about each [secondary: https://ads.expert/guides/meta-learning-phase].

## 4. Targeting and audiences
- Exists: location, age, gender, language, detailed targeting (interests, behaviors, demographics), custom audiences (website via pixel / CAPI, customer lists, app activity, engagement on video / Page / Instagram / lead forms / WhatsApp), lookalike audiences, Advantage+ audience (AI-expanded, uses your inputs as suggestions), saved audiences.
- Special Ad Categories [official: https://developers.facebook.com/docs/marketing-api/audiences/special-ad-category]: API values NONE, EMPLOYMENT, HOUSING, FINANCIAL_PRODUCTS_SERVICES (replaced CREDIT on 2025-01-14), ISSUES_ELECTIONS_POLITICS; the campaign-reference page also lists ONLINE_GAMBLING_AND_GAMING. A declaration is required at campaign creation (use NONE if no category). For housing, employment and financial products: age fixed 18-65+, no gender, no location exclusion, minimum radius around cities / pins, no behavior / demographic targeting, no lookalikes, interests only from an approved list. A wrongly declared category can pause ads until corrected. Political / issue ads need authorization per country (EU ban took effect 2025-10-06).
- Sensitive / personal-attribute rule: copy and targeting must not imply knowledge of someone's health, financial status, religion, etc. (see section 8).
- Arabic / regional: targeting by language "Arabic" is weak for Egypt because many users keep device language in English; target by location and write creative in the dialect of the audience. Egyptian Arabic copy for Egypt, Gulf / Khaleeji or MSA for KSA / UAE is a [practitioner] convention. Check that detailed-targeting interests are available for the country; availability varies and Meta periodically removes options `unverified`.
- Retargeting windows: choose based on volume; for small sites, 30-180 day windows to reach enough audience size [practitioner]. Lookalikes need a source of at least a few hundred matched people (Meta's documented minimum is 100 people from one country; `unverified` for 2026).

## 5. Bidding, budget and delivery
- Bid strategies [official: https://developers.facebook.com/docs/marketing-api/bidding/overview/bid-strategy]:
  - Highest volume / lowest cost (LOWEST_COST_WITHOUT_CAP): default; spends the budget; cost not controlled.
  - Cost per result goal (COST_CAP): target average CPA; delivery may fall short of budget; needs billing_event IMPRESSIONS and standard pacing.
  - Bid cap (LOWEST_COST_WITH_BID_CAP): hard max bid in each auction; needs bid management, can underspend; bid is not the same as reported cost.
  - ROAS goal (LOWEST_COST_WITH_MIN_ROAS): needs value optimization with purchase values passed back; floor too high causes under-delivery. roas_average_floor is scaled by 10,000 (15000 = 1.5x).
  - For iOS 14.5+ campaigns using cost cap or min ROAS the duration must be at least 3 days [official].
- Budgets: daily or lifetime; at campaign level (Advantage+ campaign budget / CBO) or ad set level, not both. Lifetime budget is required for day-parting (ad scheduling) [secondary]. Daily budget can be exceeded by up to 75% on a day, weekly spend stays within 7x the daily budget [secondary: https://www.jonloomer.com/updates-to-meta-ads-budgeting/, Nov 2023]. Budget scheduling allows up to 50 timed increases per ad set [same source].
- Minimum budgets: no universal figure was confirmed; the Ads Manager UI shows the minimum for the chosen currency / optimization / bid. Guidance reported as Meta's: set the daily budget at about 5x the target cost per result for a cost-per-result goal [secondary: https://www.tryvizup.com/blog/meta-ads-minimum-budget-requirements-2026, `unverified` against Meta]. Minimum for EGP accounts: `unverified`; read it from the UI or the API's minimum budget fields.
- Learning phase [secondary reports of Meta Help Center "About the learning phase" https://www.facebook.com/business/help/112167992830700 and "About learning limited" https://www.facebook.com/business/help/269269737396981; neither page was machine-readable here]:
  - An ad set exits learning after about 50 optimization events in the 7 days after its last significant edit. "Learning limited" means it is unlikely to reach that. It is a signal, not a penalty.
  - Always-significant edits: targeting, creative, optimization event, adding a new ad to the ad set, pausing 7+ days then restarting, changing bid strategy.
  - Magnitude-dependent: budget amount, bid / cost / ROAS goal amount, ad set spend limit. Meta's example: $100 -> $101 unlikely to reset, $100 -> $1,000 may. No percentage threshold is published. The "20% rule" is a third-party convention, not Meta policy.
  - Not significant: renames, small budget changes, moving budget between ad sets under campaign-level budget.
  - A Shops-ads variant threshold (17 website purchases + 5 through Meta in 7 days) was reported once: `unverified`.
  - The authoritative check for whether an edit reset learning is the "Last significant edit" column in Ads Manager.
- Frequency: no hard cap in auction buying; Reach & Frequency (RESERVED) sets caps. Watch frequency per ad set / ad, see section 9.
- Pacing: use standard delivery. Accelerated delivery is not recommended for cost-cap strategies.

## 6. Creative specs and requirements
IMPORTANT: Meta's official Ads Guide (facebook.com/business/ads-guide) could not be fetched. Values below are from third-party spec summaries that mostly agree; they are recommendations, not hard limits. Always confirm in the Ads Manager placement preview, which flags crops and violations. Sources: https://benly.ai/learn/ad-creative/meta-ads-creative-specs-2026, https://moda.app/resources/sizes/meta-ad-specs, https://adsuploader.com/blog/meta-ad-copy-specs (all [secondary]).

| Placement / format | Ratio | Size / resolution | Length | File size | Text (primary / headline / description) | Notes |
|---|---|---|---|---|---|---|
| Feed image (FB + IG) | 1:1 or 4:5 (4:5 takes more screen) | 1080x1080 or 1080x1350 | n/a | up to 30 MB | primary ~125 (FB Feed 50-150), headline 27 on FB Feed / 40 elsewhere, description ~25 | JPG / PNG; primary text is truncated behind "See more" |
| Feed video | 1:1 or 4:5 | 1080x1080 / 1080x1350 | 1 s to 240 min per one source | up to 4 GB | same as above | MP4 / MOV |
| Stories (FB, IG, Messenger) | 9:16 | 1080x1920 (min width 500) | 1-60 s video (one source); image shows ~5-16 s | image 30 MB, video 4 GB | ~125 primary, 40 headline | keep text out of top ~14% and bottom ~35%, ~6% sides |
| Reels | 9:16 | 1080x1920 | 3-90 s per one source (longer allowed? `unverified`) | 4 GB | FB Reels primary ~40, IG Reels primary ~44 (awareness) | Reels UI covers the bottom third; same safe zone |
| Carousel | 1:1 | 1080x1080 | video up to 240 s per card | 30 MB image / 4 GB video | headline ~45 per card, description ~18 | 3-7 cards recommended (card maximum: `unverified`) |
| Marketplace | 1:1 | 1080x1080 min | n/a | 30 MB | description ~30 | JPG / PNG |
| Right column (desktop) | 1:1 | min 254x133 | n/a | `unverified` | avoid text on image | desktop Facebook only |
| In-stream video | 16:9 or 1:1 | 1920x1080 / 1080x1080 | 5 s-10 min mobile, 5-15 s desktop | 4 GB | description ~30 | MP4 / MOV |
| Audience Network | 9:16 | 1080x1920 | n/a | 30 MB | n/a | optional placement; consider excluding for lead quality [practitioner] |

- Up to 5 variations each of primary text, headline and description per ad (dynamic creative / flexible format) [secondary].
- API input limits are far above displayed limits (primary text up to 2,200 characters in one report); write for the visible limit, not the API limit.
- Arabic / RTL cautions [practitioner]: check the preview with RTL; a headline that mixes Arabic and numbers or Latin brand names can reorder visually; keep punctuation inside the same text direction; use native Arabic fonts with sufficient size (avoid thin decorative scripts); place burned-in captions inside the safe zone; put the Arabic caption before emojis; do not rely on diacritics; text-heavy images reduce readability on mobile.
- Creative diversity: Meta's delivery rewards genuinely different concepts (hook, format, angle), not recolors. This is [practitioner]; Meta's own guidance on "creative diversification" exists but was not fetched.

## 7. Tracking and measurement
- Setup: Meta Pixel (browser) + Conversions API (server) sending the same events to one dataset. Use CAPI through a partner integration or direct server calls. Endpoint: POST https://graph.facebook.com/{version}/{dataset_id}/events (example uses v25.0; the CTWA doc references v26.0; each API version is supported at least two years) [official: https://developers.facebook.com/docs/marketing-api/conversions-api/using-the-api].
- CAPI rules [official]:
  - action_source and event_time required; event_time Unix seconds, may be up to 7 days old; if any event in a batch is older, the whole request errors and no events process.
  - up to 1,000 events per request; one invalid event rejects the batch.
  - Website events also need client_user_agent and event_source_url.
  - Hash em, ph, fn, ln, ge, db, ct, st, zp, country (SHA-256); do NOT hash client_ip_address, client_user_agent, fbc, fbp, ctwa_clid, lead_id etc. https://developers.facebook.com/docs/marketing-api/conversions-api/parameters
  - Deduplication: send the same event_name and event_id (pixel eventID) from browser and server; matching events within 48 hours are discarded, first received kept. Fallback is fbp / external_id, works only if the browser event came first within 48 hours. https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
  - test_event_code sends test events that still count for targeting and measurement: remove it in production.
  - LDU (Limited Data Use) is the only data-processing option value; needed for US state-law compliance.
- Events to set: Purchase (with value and currency), Lead / LeadSubmitted, InitiateCheckout, AddToCart, ViewContent, CompleteRegistration, Contact. Pass value and currency (EGP / SAR / USD as the account uses). Optimize for the lowest-funnel event that still gets ~50 events per ad set per week.
- AEM / domain verification: Meta said advertisers no longer need to configure and rank eight events and that domain verification is no longer required for AEM (Jon Loomer, last modified 2023-09-15: https://www.jonloomer.com/qvt/aggregated-event-measurement-isnt-going-away/). Current requirement status in 2026: `unverified`. Domain verification still matters for other features (ownership); `unverified`.
- Attribution (changed March 2026) [secondary: https://www.jonloomer.com/meta-ads-attribution-2026/]: click-through now counts only conversions after a click on an ad link (7-day default, 1-day option); non-link clicks and engaged views are separated into "engage-through" (default 1 day, can be none); view-through default 1 day (can be none); 28-day click is no longer an optimization option but can still be viewed with Compare Attribution Settings. Default for website conversion ad sets: 7-day click, 1-day engage, 1-day view. Rollout was still in progress at publication of that article, so confirm in the account.
- Platform vs GA4: Meta counts view-through and engage-through conversions and uses its own windows; GA4 is last-click / data-driven with sessions. Expect Meta to report more conversions than GA4 and lower for logged-out / consent-blocked sessions. Reconcile by comparing the same window and the same conversion definition, and use UTMs for click-based comparison.
- UTM convention: utm_source=facebook (or meta), utm_medium=paid_social, utm_campaign={campaign name or id}, utm_content={ad name or id}, utm_term={ad set}; use dynamic URL parameters ({{campaign.name}}, {{adset.name}}, {{ad.name}}) so names match reporting. [practitioner]
- Privacy: iOS App Tracking Transparency limits app-side tracking; in the EU / UK consent is required before firing the pixel; CAPI does not remove the consent requirement. In Egypt the personal data protection law (Law 151 of 2020) applies; confirm requirements with counsel (`unverified` here).
- Click-to-WhatsApp: pass ctwa_clid from the inbound webhook referral object; send action_source=business_messaging and messaging_channel=whatsapp, user_data with whatsapp_business_account_id and ctwa_clid. Supported events include Purchase, LeadSubmitted, QualifiedLead, InitiateCheckout, AddToCart, ViewContent, OrderCreated, OrderShipped, OrderDelivered, CartAbandoned, RatingProvided. Meta does not deduplicate these events. Without ctwa_clid matching is limited to the last 7 days and some countries only. [official: https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging]

## 8. Policies and restricted content
Primary policy source: Meta Advertising Standards, https://transparency.meta.com/policies/ad-standards/ (page body is JavaScript-rendered and could not be read; the subpolicy pages cited below were readable only where noted).
- Review process: ads are checked by automated systems before and while they run, with human review on escalation; most ads are reviewed within about 24 hours [secondary / well-known, `unverified` for 2026]. Ads can be rejected after they start delivering. Landing pages are reviewed too [secondary: https://www.auditsocials.com/blog/meta-ad-misleading-claims-personal-attributes-prohibited-content-policy-2026].
- Top rejection causes [secondary, same article]:
  1. Personal attributes: copy that asserts or implies a viewer's health condition, disability, finances, age, sexual orientation etc. Second-person phrasing ("you have...", "your debt") is the main trigger, even when targeting is accurate. Fix: write about the topic or the audience, not the viewer.
  2. Misleading claims: guaranteed income or returns, results presented as typical, unrepresentative testimonials, fake countdown timers / scarcity, news-style formatting, material omissions. The landing page must match the claim level.
  3. Prohibited content: tobacco, recreational drugs, weapons, adult content, surveillance tools, counterfeit documents, unsafe supplements, deceptive MLM, penny auctions. Rewording will not fix a banned category.
  4. Landing page problems: broken page, mismatched offer, no clear business information, aggressive pop-ups, non-functional checkout.
  5. Circumventing systems: cloaking, redirect tricks, repeated near-identical resubmissions (reported to trigger spam flags).
- Health and appearance [official: https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance]: no ad may imply or create negative self-perception for diet / weight-loss / appearance products; before-and-after weight-loss images are non-compliant; zoomed-in abs, images implying weight loss, a person on a scale (when promoting diet products), wrinkle images and skin-lightening imagery are non-compliant. Cosmetics, hair extensions, non-permanent beauty products and digital editing apps are outside that specific policy. The separate Health and wellness policy (https://transparency.meta.com/en-gb/policies/ad-standards/restricted-goods-services/health-wellness) exists but its body was not readable: `unverified` details (age targeting, claims).
- Restricted (allowed with conditions, authorization or targeting limits; confirm per country): alcohol, online gambling and gaming (written permission needed in many countries), pharmaceuticals, financial products and services (special category; some countries require advertiser verification), cryptocurrency (licence required in many regions), political and social-issue ads (authorization), dating, weight loss. Exact Egypt / KSA / UAE rules per category: `unverified`; check the policy page and local law before launching.
- Claims rules: no guaranteed outcomes; before/after only for non-health, non-weight products with truthful, representative results; testimonials must be genuine and typical or flagged; "free" must be free; discounts need a real reference price.
- Landing page: fast, functional, mobile-friendly, same offer as the ad, visible business identity, privacy policy, working contact info; no deceptive pop-ups.
- Account bans: repeated or severe violations, "circumventing systems" (creating new accounts to bypass a restriction), payment failures, suspicious login / spend behavior [secondary: https://benly.ai/learn/meta-ads/ad-account-restricted-fix]. Account Quality (Business Settings / Account Quality) shows status and violations.
- Appeal process: in Ads Manager use "Request review" on the rejected ad or the Account Quality case; cite the policy, explain how each flagged element complies, attach evidence (licences, receipts, screenshots) [practitioner / secondary]. Reported review times range from 24-48 hours to 5-14 business days; there is no guaranteed SLA. Do not duplicate-submit the same ad repeatedly.
- While rejected: do not edit-and-resubmit endlessly. Read the exact reason, fix all fields (primary text, headline, image text, landing page), submit once as a new ad if the fix is substantive, and keep running compliant ads in the same ad set. Never create a new account just to bypass a restriction.

## 9. Optimization playbook
Order of inspection (agent should go top-down; stop at the first broken layer):
1. Delivery and status: any ad / ad set in review, rejected, "learning limited", budget-limited or payment-failed? Fix these first.
2. Tracking: do the pixel / CAPI event counts in Events Manager roughly match the CRM / shop orders (within the expected attribution gap)? If not, fix tracking before touching bids or creative.
3. Conversion rate and CPA vs the client's break-even CPA, with a statistically meaningful number of conversions.
4. Top-of-funnel signals (CPM, CTR link, hook rate, frequency) to diagnose why.

Decision rules (thresholds are [practitioner] defaults to tune per account; reasoning given):
- Wait: do not judge an ad set before it has spent at least ~2-3x the target CPA (reason: below that a single conversion swings CPA wildly) and, if possible, has left learning (~50 events in 7 days). Early CPA is higher during learning by Meta's own description.
- Cut: an ad with spend above ~2-3x target CPA, zero conversions and below-account-average CTR; or an ad set that has spent ~3x target CPA with no conversion after the learning window. Pause the ad, not the ad set, unless the whole ad set fails. Pausing a single ad is not known to reset learning (reported by practitioners, not by Meta).
- Scale: when CPA is at or under target for 3+ days with 20+ conversions. Raise budget in steps of about 20% every 2-3 days (a third-party convention, not Meta policy); bigger jumps can re-enter learning (Meta's example of a 10x jump) and destabilize CPA. For faster scaling duplicate the winning ad set into a new ad set or campaign with a fresh budget instead of editing the live one. Horizontal scaling: new audiences / countries / new creative concepts.
- Test budget per variant: size the ad set so it can reach ~50 optimization events per week: daily budget ~ (target CPA x 50) / 7. Reasoning: that is Meta's learning exit threshold; below it you test on noise. If the budget cannot support it, test fewer variants, or optimize for an upstream event, and judge creatives on leading indicators (hook rate, CTR link, cost per landing page view / add to cart), not on CPA. The tryvizup-reported rule "daily budget ~5x target cost per result" is a lower bound of what Meta suggests for cost-per-result goals [secondary].
- Creative fatigue signals [practitioner]: frequency rising (about 3+ in a week for prospecting is a common alarm; for small audiences, sooner), CTR (link) falling over 5-7 days, CPM rising with stable audience, negative comments rising, CPA rising while conversion rate on the landing page is stable. Response: add 2-4 new concepts (not recolors) as new ads; avoid rebuilding the ad set; retire only the clear losers.
- Audience overlap / auction overlap: prefer consolidation to many similar ad sets competing against each other (listed by Meta as a cause of learning limited).
- What NOT to touch during learning: optimization event, targeting / audience, creative text or media in a live ad (create a new ad instead), bid strategy, large budget jumps, adding many new ads at once; do not pause for 7+ days and restart. Allowed: small budget increases, renaming, adding exclusions only if essential (still counts as targeting edit: avoid).
- Automated rules from agents: every change by a rule is also a platform edit. Do not run rules that edit budgets or bids more than once per day per ad set (API blocks ad set budget changes beyond 4 per hour anyway, see section 11).
- Always compare attribution consistently: choose one attribution setting for reporting (e.g., 7-day click + 1-day view) and note that March 2026 changes altered what "click" means; do not compare periods across the change without checking.

## 10. Metrics and definitions
| Standard term | Ads Manager name | Definition / note |
|---|---|---|
| Impressions | Impressions | times ads were on screen |
| Reach | Reach | accounts that saw it at least once |
| Frequency | Frequency | impressions / reach |
| CPM | CPM (cost per 1,000 impressions) | spend / impressions x 1000 |
| CTR (link) | CTR (link click-through rate) | link clicks / impressions; use this one for performance |
| CTR (all) | CTR (all) | includes likes, shares, profile clicks; inflated, do not use for CPC math |
| CPC | CPC (cost per link click) | spend / link clicks; "CPC (all)" is different |
| Landing page views | Landing page views | clicks that loaded the page; better than link clicks for traffic quality |
| Results | Results | count of the optimization event chosen for the ad set (differs by objective) |
| CPA / CPL | Cost per result | spend / results; make sure "results" is the event you care about |
| CVR | Conversion rate (computed) | results / link clicks or landing page views, depending on definition; Ads Manager may show "Website purchase conversion rate" |
| ROAS | Purchase ROAS (return on ad spend) | purchase conversion value / spend, under the attribution setting selected |
| Hook rate | not native; compute 3-second video plays / impressions | practitioner metric |
| Hold rate | not native; ThruPlays / 3-second plays (or 15 s plays) | ThruPlay = watched to 15 s or to completion if shorter (well-known definition) |
| Diagnostics | Quality ranking, Engagement rate ranking, Conversion rate ranking | relative to ads competing for the same audience; diagnostic only |
Always state the attribution setting and date range when quoting any conversion metric (see section 7).

## 11. API and automation
- Official API: Meta Marketing API (Graph API), Insights API for reporting, Conversions API for server events. Docs: https://developers.facebook.com/docs/marketing-api/ . Versions are numbered (v25.0 / v26.0 appear in current docs); pin a version and plan upgrades.
- What can be automated: create / update campaigns, ad sets, ads, creatives (image and video upload), audiences (custom audiences, lookalikes), budgets and bids, status changes, reports (Insights with breakdowns, async reports for large jobs), CAPI events, click-to-WhatsApp ad creation (needs a Page with a linked WhatsApp number, ads_management, pages_manage_ads, pages_read_engagement, pages_show_list; optimization_goal CONVERSATIONS for leads; billing_event IMPRESSIONS) [official: https://developers.facebook.com/docs/marketing-api/ad-creative/messaging-ads/click-to-whatsapp].
- Access: Limited Access tier by default; Full Access after App Review; system users (1 admin system user at Limited; up to 10 plus 1 admin at Full); permissions ads_read, ads_management; business verification for sensitive data apps [official: https://developers.facebook.com/docs/marketing-api/overview/authorization].
- Rate limits [official: https://developers.facebook.com/docs/marketing-api/overview/rate-limiting]:
  - Business Use Case limits per ad account per hour: ads_management base 100,000 (Full) or 300 (Development) plus 40 points per active ad; ads_insights base 190,000 (Full) / 600 (Development) plus 400 per active ad. Check the X-Business-Use-Case response header.
  - Error codes 80000 / 80003 / 80004 / 80014 = BUC limit; code 17 / 613 with the listed subcodes = score-based account limits (reads 1 point, writes 3; Development cap 60 points, Full 9,000).
  - 613 subcode 5044001: more than 100 mutation requests per second per app and ad account. 613 subcode 4841018: default one edit per object per 30 seconds. 613 subcode 1487632: an ad set budget changed more than 4 times in an hour is blocked for an hour. 17 subcode 1885172: account spend limit changed more than 10 times per day.
  - Retry with exponential backoff on these.
- Built-in automated rules: Ads Manager has automated rules (notify, pause, change budget / bid on conditions or schedule). Ad Rules Engine API supports schedule- and trigger-based rules built from evaluation, execution and change specs [official: https://developers.facebook.com/docs/marketing-api/ad-rules]. Details of limits per rule: `unverified`.
- Rules for agents that make automated changes: (1) change budgets at most once a day and by at most ~20%; (2) never edit creative on live ads, create a new ad; (3) log every change with a reason and a revert plan; (4) only act on ad sets with enough data (see rule thresholds above); (5) respect the human approval policy of the client for anything that raises spend; (6) never send customer PII to CAPI unhashed; (7) store tokens in a secret manager, never in logs or repos.
- Legacy Advantage Shopping / Advantage App campaign API fields vs new Advantage+ state fields: whether legacy creation paths are still accepted in the current API version: `unverified`. Always read the current campaign reference.

## 12. Cases
**Ad rejected**
- **Situation**: Ad status "Rejected" for personal attributes / misleading claim.
- **Do**: read the exact policy cited; rewrite copy to talk about the topic, not the viewer; remove guaranteed-result language and fake timers; make the landing page match; submit once; request review only if you are sure it complies, citing the policy.
- **Avoid**: duplicating the same ad 5 times; cloaking; editing only the image when the text is the cause.

**Ad account disabled / restricted**
- **Situation**: Account Quality shows Restricted or Disabled.
- **Do**: read the reason in Account Quality; complete business verification and identity checks; fix payment issues; submit one documented appeal; use partner / support channels if available; keep a second clean account only with the client's own legitimate business assets and do not move policy-violating ads into it.
- **Avoid**: creating new accounts to bypass a restriction (can cause bans on linked assets), changing the payment method repeatedly, ignoring unsettled invoices.

**Spend without results**
- **Situation**: Spend is above 2-3x target CPA with no conversions.
- **Do**: confirm the event fires (Test Events, Events Manager); check the offer and landing page speed; check whether the event is too rare to learn (move up funnel); check audience too narrow; review creative; confirm ads are not in learning; then cut the loser.
- **Avoid**: raising budget "to get data"; changing five things at once.

**CPA suddenly doubled**
- **Situation**: CPA doubled day over day.
- **Do**: check for edits (Last significant edit), new ads added, budget jump, creative fatigue (frequency), tracking outage (CAPI or pixel errors, site checkout change), stock-out, price change, holiday / payday effects, attribution settings change (March 2026), then wait 48 hours before reacting unless tracking is broken.
- **Avoid**: reacting on one day of data; resetting learning by editing the ad set.

**Learning limited**
- **Situation**: Ad set shows "Learning limited".
- **Do**: raise the volume of events: optimize for an earlier funnel event, widen the audience, consolidate ad sets, raise the budget moderately, cut the number of ads, remove cost caps that are too tight.
- **Avoid**: splitting a small budget over many ad sets.

**Creative fatigue**
- **Situation**: CTR down, frequency up, CPA up over a week.
- **Do**: add new concepts (different hook, angle, format); keep the winning ad live while testing; refresh landing page hooks.
- **Avoid**: editing the ad in place; pausing the whole ad set.

**Tracking mismatch (Meta vs shop / GA4)**
- **Situation**: Meta reports 120 purchases, shop shows 70.
- **Do**: compare at the same window; check deduplication (same event_id on pixel and CAPI), duplicate pixel installs, double-firing on thank-you page reloads, view-through share, test orders; for WhatsApp sales, confirm CRM matching via ctwa_clid.
- **Avoid**: trusting either number blindly; changing windows mid-month.

**Tiny budget (for example below roughly $5 a day)**
- **Situation**: Small local business with a very small budget.
- **Do**: one campaign, one ad set, a conversation or lead goal that can realistically get results (click-to-WhatsApp conversations or instant-form leads); narrow geography; 3 creatives; run 7+ days without edits; judge on cost per conversation / lead, not on purchases.
- **Avoid**: purchase optimization without volume; many ad sets; frequent edits.

**Local lead-gen / WhatsApp-click campaigns (Egypt / MENA)**
- **Situation**: Clinic, real-estate, education, or service business wants WhatsApp enquiries.
- **Do**: Leads or Engagement objective with WhatsApp destination (Sales for direct purchases); set up a welcome message and ice breakers; capture ctwa_clid in the CRM and send LeadSubmitted / QualifiedLead / Purchase back via CAPI so Meta can optimize for quality (Meta reports lead optimization lowers cost per lead by 24% vs conversation optimization and purchase optimization lowers cost per purchase by 10%; Meta-reported, eligibility-gated: https://whatsappbusiness.com/resources/resource-library/down-funnel-optimizations-whatsapp/); reply to messages quickly; use a CRM stage as the qualified lead signal.
- **Avoid**: counting "conversations" as the final result; leaving enquiries unanswered; promising price or medical outcomes in ads.

**Scaling too fast**
- **Situation**: Budget doubled, CPA climbed and delivery became erratic.
- **Do**: step back to the last stable budget over 2-3 days; scale by ~20% steps or duplicate the ad set; add creative volume before spend.
- **Avoid**: 3-5x jumps; changing bid strategy at the same time.

**Seasonal peak (Ramadan, White Friday / Black Friday)**
- **Situation**: CPMs rise and demand spikes in Ramadan or White Friday.
- **Do**: prepare creative, offers and landing pages 2-3 weeks ahead; warm audiences before the peak; raise budgets in steps before the peak so learning is complete; schedule budget increases (budget scheduling allows timed increases); watch stock and delivery capacity; use daily payday and late-evening timing in Ramadan as a hypothesis to test, not a rule.
- **Avoid**: launching new ad sets on peak day; changing events during the peak; assuming last year's CPA applies. (No reliable Egypt benchmark for seasonal CPM changes was found.)

## 13. Pre-launch checklist
1. Is the ad account currency and time zone correct and a valid payment method added with a spending limit set?
2. Is the business portfolio verified (or verification started) and are admin roles limited with 2FA?
3. Are the Page, Instagram account and WhatsApp number linked and owned by the client's portfolio?
4. Does the pixel + Conversions API send the optimization event with value and currency?
5. Are pixel and CAPI deduplicated with the same event_id and event_name?
6. Did the Test Events tool confirm events and was test_event_code removed from production calls?
7. Is the chosen optimization event expected to reach ~50 events per ad set per week at the planned budget?
8. Is the correct objective and conversion location (website / messaging / instant form) selected?
9. Is the special ad category declared correctly (or NONE)?
10. Is the attribution setting chosen and recorded for reporting?
11. Do all ads pass the personal-attribute and misleading-claim checks (no "you have...", no guarantees)?
12. Does the landing page load fast on mobile, match the offer, and show business details and privacy policy?
13. Are Arabic creatives checked in placement previews (RTL, safe zones for Stories / Reels)?
14. Is there a UTM scheme using dynamic parameters?
15. Are there at least 3 genuinely different creatives per ad set?
16. For WhatsApp ads: is the welcome message set, is someone assigned to reply, and is ctwa_clid stored?
17. Is a naming convention applied and a reporting dashboard ready?
18. Has the client confirmed VAT / e-invoice handling with their accountant?

## 14. Sources
- https://developers.facebook.com/docs/marketing-api/overview/authorization
- https://developers.facebook.com/docs/marketing-api/overview/rate-limiting
- https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group
- https://developers.facebook.com/docs/marketing-api/audiences/special-ad-category
- https://developers.facebook.com/docs/marketing-api/bidding/overview/bid-strategy
- https://developers.facebook.com/docs/marketing-api/conversions-api/
- https://developers.facebook.com/docs/marketing-api/conversions-api/parameters
- https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/server-event
- https://developers.facebook.com/docs/marketing-api/conversions-api/using-the-api
- https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
- https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging
- https://developers.facebook.com/docs/marketing-api/ad-creative/messaging-ads/click-to-whatsapp
- https://developers.facebook.com/docs/marketing-api/ad-rules
- https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance
- https://whatsappbusiness.com/resources/resource-library/down-funnel-optimizations-whatsapp/
- https://datareportal.com/reports/digital-2026-egypt
- https://datareportal.com/reports/digital-2026-saudi-arabia
- https://www.jonloomer.com/meta-ads-attribution-2026/ (secondary)
- https://www.jonloomer.com/updates-to-meta-ads-budgeting/ (secondary)
- https://www.jonloomer.com/advantage-plus-sales-app-leads-campaigns/ (secondary)
- https://www.jonloomer.com/facebook-ads-edits-learning-phase/ (secondary)
- https://www.jonloomer.com/qvt/aggregated-event-measurement-isnt-going-away/ (secondary)
- https://ads.expert/guides/meta-learning-phase (secondary)
- https://goodmorningco.com/blog/meta-ads-significant-edits-learning-phase (secondary)
- https://www.tryvizup.com/blog/meta-ads-minimum-budget-requirements-2026 (secondary)
- https://benly.ai/learn/ad-creative/meta-ads-creative-specs-2026 , https://moda.app/resources/sizes/meta-ad-specs , https://adsuploader.com/blog/meta-ad-copy-specs (secondary, specs)
- https://www.auditsocials.com/blog/meta-ad-misleading-claims-personal-attributes-prohibited-content-policy-2026 (secondary)
- https://benly.ai/learn/meta-ads/ad-account-restricted-fix (secondary)
- https://kb.orbee.com/billing-meta-ads (secondary)
- https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/ , https://ecpa-eg.com/en/eg/articles/coding-of-ads-on-social-media-for-the-egyptian-tax-authority (tax, secondary)
- Not readable by the research tool (robots restriction), cited by title only: https://www.facebook.com/business/help/112167992830700 (learning phase), https://www.facebook.com/business/help/269269737396981 (learning limited), https://www.facebook.com/business/help/212763688755026 (payment options), https://www.facebook.com/business/help/1622234084485141 (Egypt), https://transparency.meta.com/policies/ad-standards/ (Advertising Standards)
