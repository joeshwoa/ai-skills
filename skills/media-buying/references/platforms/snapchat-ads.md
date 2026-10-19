# Snapchat Ads — rules and playbook
Last verified: 2026-10-19

Scope: Snapchat Ads Manager, Snap Pixel and Conversions API (CAPI), Snapchat Marketing API, ad formats (Snap Ads, Story Ads, Collection Ads, Sponsored Snaps, Commercials, AR Lenses). Source key: **[official]** = Snap developer docs, Snap policy or Snap for Business page read on 2026-10-19; **[secondary]** = third party; **[practitioner]** = observation, not an official rule; `unverified` = not confirmed. Research note: the Snapchat Business Help Center (businesshelp.snapchat.com) is client-rendered and could not be read, so learning-phase, billing, payment-method, ad-review timing, appeal and Ads Manager UI details are `unverified` unless a developer-doc or policy page is cited.

## 1. When to use it
- Strengths: young audience with very high penetration in Saudi Arabia and the Gulf; immersive full-screen vertical formats; AR Lenses and Filters; Sponsored Snaps (ads in the Chat tab); Dynamic Product Ads from a product catalog; in-app lead forms. Snap's own page says about 80% of Snapchatters are over 18 and nearly 1 in 4 are over 35; it also states 443 million daily users (Snap-reported, undated on the page). https://forbusiness.snapchat.com/advertising
- Weaknesses: much smaller reach than Meta or TikTok in Egypt; smaller third-party tooling ecosystem; fewer public benchmarks; creative must be vertical and fast; some bidding options have been deprecated (see section 5).
- Best objectives (Ads Manager goals per Snap: App Downloads, Shopify Store Sales, Online Sales, Lead Generation, Brand Awareness; API objective types: AWARENESS_AND_ENGAGEMENT, SALES, TRAFFIC, APP_PROMOTION, LEADS). Use Sales / Leads when the Snap Pixel or CAPI is clean; Awareness for reach with Lenses or Commercials in Gulf launches.
- Egypt / MENA relevance (DataReportal Digital 2026, published 2025-11-08; Snap-reported ad reach, not MAU):
  - Saudi Arabia: Snapchat 25.3M (72.9% of population) vs TikTok 38.6M (18+), Instagram 18.2M, Facebook 17.7M. https://datareportal.com/reports/digital-2026-saudi-arabia
  - UAE: Snapchat 5.13M (44.9%). https://datareportal.com/reports/digital-2026-united-arab-emirates
  - Kuwait: Snapchat 2.43M (48.2%). https://datareportal.com/reports/digital-2026-kuwait
  - Egypt: Snapchat 20.6M (17.3%) vs Facebook 51.6M and TikTok 48.8M (18+). https://datareportal.com/reports/digital-2026-egypt
  - Reading: Snapchat is a first-tier channel for KSA / Kuwait / UAE audiences and a secondary channel for Egypt.
- Benchmarks: no reliable public CPM / CPC / CPA benchmark for KSA, Gulf or Egypt was found. Do not quote any.

## 2. Account, billing and access
- Structure: Organization (Business Manager / Business Details) -> Ad accounts -> Pixels, Public Profiles, catalogs, audiences, members. The API entity model is Organizations, Ad Accounts, Campaigns, Ad Squads and Ads [official: https://developers.snap.com/api/marketing-api/Ads-API/introduction]. Ad squad = ad group.
- Public Profile: Snap Ads and Sponsored Snaps pull the brand name from the Public Profile; the creative brand_name is optional when a Public Profile is attached and would overwrite the profile name if set [official, creatives doc].
- Roles and agency access: Organization Admin controls OAuth apps and Conversions API tokens; members are invited by role. How to give an agency access in the UI: `unverified`.
- Ad account facts [official: https://developers.snap.com/api/marketing-api/Ads-API/ad-accounts]: timezone is required (Africa/Cairo, Asia/Riyadh, Asia/Dubai and Asia/Qatar appear in the list); billing_type is IO or REVOLVING; test ad accounts never serve live ads; `restricted_delivery_signals` must be set to true for credit, housing or employment ads and cannot be changed afterwards.
- Funding sources [official: https://developers.snap.com/api/marketing-api/Ads-API/funding-sources]: LINE_OF_CREDIT, CREDIT_CARD, COUPON, PAYPAL (cards and PayPal set up in Business Manager; credit lines and coupons by Snap's partner team). Currencies named on that page: USD, CAD, GBP, AUD, EUR. The bid-limit table in the ad squad doc also lists AED, SAR, QAR, KWD (among others) but does not list EGP, and the ad account page lists a shorter set. Conclusion: Gulf currencies appear supported; whether an Egypt-based advertiser can open an EGP account or pay with an Egyptian card: `unverified`. Plan for USD / hard-currency payment via an international card unless Snap confirms otherwise (the budget minimums in section 5 are published in USD / micro-units).
- Tax: Egypt's Tax Authority guidance applies 14% VAT to non-resident digital services (vatcalc, 2023: https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/); how Snap invoices VAT for Egyptian or Saudi advertisers: `unverified`. Confirm with the client's accountant. Saudi VAT treatment of Snap invoices: `unverified`.
- Verification and advertiser identity (some categories and political ads require extra verification): see section 8.

## 3. Campaign structure
Hierarchy: Campaign (objective, buy model, optional spend caps and Smart Budget) -> Ad Squad (budget, schedule, targeting, placement, optimization goal, bid strategy) -> Ad (creative, attachment, CTA).
- Buy models: AUCTION (default) and RESERVED. RESERVED campaigns cannot be changed through the API and must be managed in Ads Manager. [official: campaigns doc, https://developers.snap.com/api/marketing-api/Ads-API/campaigns]
- Objective -> optimization goals (API v2 mapping, examples) [official, same doc]:
  - AWARENESS_AND_ENGAGEMENT (web): IMPRESSIONS, SWIPES, STORY_OPENS, USES (Lens uses), VIDEO_VIEWS, VIDEO_VIEWS_15_SEC.
  - TRAFFIC: SWIPES, PIXEL_PAGE_VIEW, LANDING_PAGE_VIEW (web).
  - SALES (web): SWIPES, STORY_OPENS, PIXEL_PURCHASE, PIXEL_SIGNUP, PIXEL_ADD_TO_CART, PIXEL_PAGE_VIEW, LANDING_PAGE_VIEW.
  - LEADS: LEAD_FORM_SUBMISSIONS and SWIPES (lead form); SWIPES, STORY_OPENS, PIXEL sign-up, LANDING_PAGE_VIEW (web); IMPRESSIONS and SWIPES (call / text).
  - APP_PROMOTION: IMPRESSIONS, SWIPES, APP_INSTALLS, APP_PURCHASE, APP_SIGNUP, APP_ADD_TO_CART, re-engagement goals.
  - The legacy objective list (BRAND_AWARENESS, WEB_CONVERSION, LEAD_GENERATION, CATALOG_SALES, ENGAGEMENT, VIDEO_VIEW, PROMOTE_STORIES ...) is mapped automatically to the 5 v2 types for apps still creating campaigns with `objective` since 2025-03-21.
- Smart Budget: moves budget control to the campaign so spend can shift between ad squads by performance; requires pacing_level CAMPAIGN, shared properties mirrored on every ad squad, one of daily_budget_micro or lifetime_spend_cap_micro; works with AUTO_BID or LOWEST_COST_WITH_MAX_BID and optimization goals IMPRESSIONS or PIXEL_PURCHASE; not for Dynamic Ads; ad squad pacing cannot be ACCELERATED [official]. Snap's UI branding of this feature: `unverified`.
- Recommended structure [practitioner unless stated]:
  - Small budget: 1 campaign, 1 ad squad, 2-4 creatives (Single Image or Video), optimize SWIPES / LANDING_PAGE_VIEW or the lowest-funnel event that can get volume.
  - Medium: prospecting (broad + interest) and retargeting (pixel audiences) campaigns; separate ad squads for Arabic and English; test Collection or Story Ads for e-commerce.
  - Large: add Smart Budget at campaign level, Dynamic Product Ads, Lenses for awareness, creative testing campaign, separate KSA / UAE / Kuwait campaigns for currency, language and policy differences.
- Limits [official]: up to 100 campaigns per ad account; ad name max 375 characters.

## 4. Targeting and audiences
- Exists: geography (country, region, city / radius; Gulf and Egypt markets), demographics (age, gender, language), interests and behaviors (lifestyle categories), devices (OS and version), custom audiences from hashed first-party data (customer lists, pixel events, app activity), engagement audiences, lookalike audiences, audience expansion options (interest and custom-audience expansion exist as `auto_expansion_options`) [official: Ads API introduction and ad squad doc]. Detailed segment list and minimum audience sizes: `unverified`.
- Restrictions [official: https://snap.com/en-US/ad-policies]: Snapchat is a 13+ app; ads targeting children under 13 are rejected; many categories need higher minimum ages (alcohol, dating 18+, gambling etc.); sensitive categories (health, financial, religious, political data) cannot be collected or targeted; ads may not imply knowledge of personal data or precise location; some categories are barred in specific countries; credit / housing / employment ads need `restricted_delivery_signals` and `regulated_content` handling.
- Arabic / regional: targeting by language and by country; many Saudi users run the app in Arabic and others in English, so produce both language variants and let performance decide [practitioner]. Use Gulf dialect copy for KSA / UAE / Kuwait and Egyptian dialect for Egypt where the audience is Egyptian [practitioner].
- Placement: `placement_v2` with AUTOMATIC is the default config; custom placements exist (which surfaces are selectable: `unverified`).

## 5. Bidding, budget and delivery
- Bid strategies [official: https://developers.snap.com/api/marketing-api/Ads-API/ad-squads]:
  - AUTO_BID: most efficient cost per action while spending the budget; allowed for most optimization goals (IMPRESSIONS, SWIPES, VIDEO_VIEWS, PIXEL_PURCHASE, PIXEL_SIGNUP, PIXEL_ADD_TO_CART, LANDING_PAGE_VIEW, APP goals, etc.).
  - LOWEST_COST_WITH_MAX_BID: bid cap; works with any goal; needs bid_micro.
  - TARGET_COST: target CPA; allowed for APP_INSTALLS, SWIPES, USES, VIDEO_VIEWS_15_SEC, PIXEL_PURCHASE, PIXEL_SIGNUP, PIXEL_PAGE_VIEW, PIXEL_ADD_TO_CART, APP_PURCHASE, APP_SIGNUP, APP_ADD_TO_CART, STORY_OPENS, LANDING_PAGE_VIEW, etc.; SKAdNetwork-enrolled ad squads cannot use it.
  - MIN_ROAS: deprecated on 2025-02-10; do not plan on it.
  - Bid limits: bid_micro minimum 10,000 micro-units in every listed currency; maximum 500,000,000 for AED, QAR, SAR and USD and 100,000,000 for KWD (and AUD, CAD, CHF, EUR, GBP) [official]. 1 currency unit = 1,000,000 micro.
  - A spend_guidance endpoint returns suggested min / max bids and a default daily budget for TARGET_COST goals.
- Budgets [official, ad squad and campaign docs]:
  - Ad squad: set exactly one of daily_budget_micro or lifetime_budget_micro; the ad squad doc gives a minimum of 5,000,000 micro (5 currency units) for daily budget across supported currencies (confirm in UI); lifetime budgets need start and end times.
  - Campaign: daily_budget_micro and lifetime_spend_cap_micro must each be at least 20,000,000 micro (US$20 per the doc); a campaign daily budget must be at least 0.25 times the sum of its ad squads' budgets; ad account spend cap can be raised or removed but only lowered to 1.1x what is already spent. Delivery stops at the ad account cap or campaign lifetime cap.
  - billing_event: IMPRESSION only. pacing_type STANDARD (default) or ACCELERATED (avoid ACCELERATED with cost controls and Smart Budget).
- Learning phase: Snap documents a learning period for auto-optimized ad squads, but the help articles with thresholds could not be read; no numeric threshold is stated here: `unverified`. Treat the first several days after launch or after any significant edit as unstable, and avoid frequent edits [practitioner].
- Frequency: Reach & Frequency (RESERVED) exists in Ads Manager and cannot be edited via API; auction frequency controls: `unverified`.
- Daily budget vs CPA rule [practitioner]: size the ad squad so it can produce at least a handful of optimization events per day; if the CPA is above one fifth of the daily budget, move to a higher-funnel goal (SWIPES, LANDING_PAGE_VIEW, ADD_TO_CART).

## 6. Creative specs and requirements
Sources: https://forbusiness.snapchat.com/advertising/ad-formats (formats), https://developers.snap.com/api/marketing-api/Ads-API/media (media upload), https://developers.snap.com/api/marketing-api/Ads-API/creatives (creative fields). Snap's full specs live in Business Help Center article "top-snap-specs", which could not be read; verify in the upload UI.

| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Single Image or Video (Top Snap) | 9:16 | 1080x1920 (image and video per the media doc); formats page cites 720x1280 as the baseline | video 3-180 s per formats page (media doc lists 3-1800 s; plan for 180 s) | video 32 MB per upload, up to 1 GB via chunked upload (max 32 chunks of 32 MB); image 5 MB PNG / JPG | brand name up to 25 chars (formats page; API max 32), headline up to 34 | MP4 / MOV for video; headline required; CTA depends on attachment |
| Story Ads | 9:16 | 720x1280+ | video 3-180 s | as above | brand up to 25, headline up to 34 | needs a PREVIEW creative: 3:5, min 360x600, PNG, 2 MB |
| Collection Ads | 9:16 | 720x1280+ | video 3-180 s | as above | brand up to 25, headline up to 34 | product tiles from catalog; ecommerce |
| Sponsored Snaps (Chat) | 9:16 | 720x1280; branded chat background 1080x1920 | up to 180 s (under 10 s recommended) | as above | headline 25-28 recommended, 34 max; chat message up to 500 chars; auto-response up to 500 chars | brand name pulled from Public Profile |
| Commercials | 9:16 | 720x1280 | 3-6 s non-skippable (standard); 7-180 s with first 6 s non-skippable (Extended Play) | MP4 / MOV, H.264 | n/a | awareness only |
| AR Lenses | n/a | static filter PNG 945x2048; animated filter GIF 720x1560, 1-3 s | | | visible logo / brand name required, top left or top right | Snap adds a 2-second "SPONSORED" label |
| Logo (profile / headline logo) | | 993x284 | | | | |
| App end card | 1080x1920 or 1920x1080 | | | 1 MB JPG / PNG | | |
| Playable | ZIP with index.html and config.json | | | 5 MB | | |
- CTA options depend on attachment type: WEB_VIEW, APP_INSTALL, DEEP_LINK, AD_TO_LENS, AD_TO_CALL, AD_TO_MESSAGE, LEAD_GENERATION, collection and lens variants (examples: Shop Now, Sign Up, Apply Now, Book Now, Message Now, Call Now) [official].
- Safe zones: keep text and logo away from top and bottom UI areas (exact percentages: `unverified`; the Top Snap article could not be read). Use the Ads Manager preview.
- Arabic / RTL cautions [practitioner]: keep Arabic headline within 34 characters and test truncation; place key text away from the bottom swipe-up and caption area; avoid long mixed Arabic-Latin lines; burn in Arabic captions; use fast first-second hooks because ads are skipped easily.

## 7. Tracking and measurement
- Snap Pixel (browser) via `snaptr('track', ...)` and the Conversions API (server). Standard event names include PURCHASE, ADD_CART, PAGE_VIEW, SIGN_UP, APP_INSTALL (full list: `unverified`).
- Conversions API [official: https://developers.snap.com/api/marketing-api/Conversions-API/GetStarted and /Parameters]:
  - IDs: pixel_id for web and offline events; snap_app_id for app events. Static long-lived tokens are created in Ads Manager > Business Details > Conversions API Tokens by an Organization Admin; they do not expire; a token only works for pixel and app IDs of its own organization. OAuth scope for CAPI via the Marketing API: snapchat-offline-conversions-api.
  - Required for web and app events: event_name, event_time (epoch; must not be more than 7 days in the past), action_source (WEB, OFFLINE, MOBILE_APP).
  - Hash with SHA-256 after normalization: em, ph, fn, ln, ge, ct, st, zp, country; recommended to hash external_id; do not hash client_ip_address, client_user_agent, madid, sc_click_id, sc_cookie1. Normalization: emails trimmed and lowercased; phone numbers with country code, numerals only, without leading zeros / double zero; MAIDs lowercase with hyphens; lowercase hex SHA-256 [official best-practices page].
  - Limits: up to 2,000 events per batch request; standard rate limit 10 requests per second per token; long-lived token guidance mentions much higher throughput (about 1,000 QPS recommended) [official, GetStarted page].
  - Endpoint URL and version: the page says to use the token "in the v3 endpoint"; exact URL: `unverified`.
- Deduplication [official: https://developers.snap.com/api/marketing-api/Conversions-API/Deduplication]: Pixel SDK client_dedup_id must equal the CAPI event_id, with identical casing and whitespace, for the same pixel ID; event names must match (for example SIGN_UP, not "signup"); set client_dedup_id explicitly (the SDK otherwise creates a browser-only ID prefixed "@-"); use one unique ID per conversion; dedup window 48 hours; for PURCHASE also send transaction_id (Pixel) and order_id (inside custom_data in CAPI v3), which can dedup late events up to 30 days. Verify in Events Manager > Diagnostics (allow up to 24 hours).
- Attribution windows [official: https://developers.snap.com/api/marketing-api/Ads-API/measurement]: swipe-up window values 1_DAY, 7_DAY, 28_DAY with default 28_DAY; view window values none, 1_HOUR, 3_HOUR, 6_HOUR, 1_DAY, 7_DAY (28_DAY deprecated), default 1_DAY. The bid-recommendation tool accepts SWIPE_28DAY_VIEW_1DAY and SWIPE_7DAY. These are the API defaults; the Ads Manager UI default and whether it matches: `unverified`. Always record the window in reports.
- Events to set: PAGE_VIEW, VIEW_CONTENT, ADD_CART, START_CHECKOUT, PURCHASE (with price and currency), SIGN_UP / lead; for apps, APP_INSTALL and purchase events via SDK / MMP. Names beyond those listed: `unverified`.
- UTM convention: utm_source=snapchat, utm_medium=paid_social, utm_campaign={campaign}, utm_content={ad}; Snap URL macros for dynamic parameters exist (exact names: `unverified`).
- Platform vs GA4: Snap counts swipe-up conversions over up to 28 days plus view-through (1 day default), so it reports higher than last-click GA4; Snap's in-app browser and the Snap click ID (sc_click_id) help match; keep the sc_click_id from the landing URL and pass it in CAPI where possible [practitioner].
- Privacy: iOS ATT limits app measurement (SKAdNetwork; ad squads enrolled in SKAdNetwork cannot use TARGET_COST or re-engagement goals); GDPR / consent for EU users; Saudi PDPL and Egypt Law 151 of 2020 apply to personal data processing: `unverified` details; ask counsel.

## 8. Policies and restricted content
Source: Snap Advertising Policies https://snap.com/en-US/ad-policies (read 2026-10-19).
- Scope and review: policies cover creative, landing pages and related components; Snap reviews and approves all ads and may reject or remove any ad, request modification, substantiation or licence documents; categories needing advance approval include prescription and OTC medicines, supplements, gambling, complex financial products, government ads and political ads. Review timing (commonly about a day): `unverified`. API: `review_status` is PENDING, APPROVED or REJECTED with read-only `review_status_reasons` [official, ads doc].
- Prohibited: harassment; graphic violence and gore; deceptive content (false or misleading claims, fraud, counterfeit goods, imitating Snapchat features, cloaking, non-delivery, subliminal techniques); hate speech and extremism; illegal and dangerous activity; sexually explicit content; weapons and explosives; vape sales; IP infringement.
- Restricted (approval, age, country or disclosure rules): adult content (18+ age-gate), alcohol (age by country, warnings), CBD and cannabis (where legal), tobacco (public-health only), health products (prescription and OTC medicines, supplements, weight loss, cosmetic procedures, condoms, online pharmacies), gaming and gambling (pre-approval, licensing proof, direct advertiser submission, country lists), financial products (disclose material terms; complex products need approval; get-rich-quick and guaranteed returns prohibited), dating (18+), telecom (clear pricing), government entities (authorization), political and advocacy ads (transparency, "paid for by", case-by-case review; EU restrictions from 2025-10-01; foreign-funded political ads not allowed).
- Claims: substantiation may be requested; health, diet and supplement claims must not be exaggerated or unrealistic; before-and-after weight-loss images are prohibited; OTC ads cannot imply prescription-strength efficacy; do not misrepresent authority approvals.
- Landing pages: reviewed with the creative; rejected if dead links, not mobile-formatted, disruptive (loud noises, aggressive flashing), irrelevant or mismatched, unsafe (auto-downloads, phishing); cloaking and changing the URL after submission are prohibited.
- Account ban causes: policy violations can lead to suspension or termination; circumvention via new accounts: treat as violation [practitioner].
- Appeal process: use the review-rejection details in Ads Manager and the Snap support / appeal form; review time and success rates: `unverified`.
- While rejected: fix the cited element (creative, text, page), resubmit as a new ad; keep other compliant ads running; for restricted categories submit the pre-approval form before launching.
- Egypt / KSA / UAE category specifics (alcohol, gambling, pharmaceuticals, real estate, cryptocurrency): `unverified`; the policy lists country-level restrictions in category pages not retrieved.

## 9. Optimization playbook
Inspection order: (1) delivery_status and review status (campaign / ad squad / ad), payment, caps; (2) pixel / CAPI event counts vs CRM and deduplication; (3) optimization goal vs volume; (4) creative metrics (hook / view rates, swipes); (5) audience and bid.
- Wait: allow roughly 3-7 days and enough conversions before major decisions [practitioner]; Snap-published learning thresholds `unverified`. Avoid editing ad squads during the first days.
- Cut: ads with spend above ~2-3x target CPA and no conversions and weak swipe rate vs siblings; ad squads that stay unprofitable after a fresh creative round [practitioner].
- Scale: raise budgets in steps of about 20% every 2-3 days [practitioner; no Snap-published rule found]; duplicate the winning ad squad for bigger jumps; use Smart Budget to let Snap move spend between ad squads.
- Test budget per variant: enough for about 10-15 target-CPA worth of daily spend for conversion goals (so each variant can produce several events per day), otherwise use SWIPES / LANDING_PAGE_VIEW as a proxy. Reasoning: with fewer events per day the bid model has no signal; this is a practitioner heuristic because Snap's help page with thresholds was not readable.
- Bid choice: start with AUTO_BID; use TARGET_COST when you know break-even CPA and have stable volume; use a bid cap (LOWEST_COST_WITH_MAX_BID) to protect against runaway cost. Do not rely on MIN_ROAS (deprecated 2025-02-10).
- Creative fatigue [practitioner]: swipe rate and video completion falling, CPM or CPA rising, frequency rising, comments and negative signals. Response: new hooks and formats, new Lens or Story variants; rotate every 1-2 weeks on small audiences.
- Not to touch during learning: optimization goal, pixel event, bid strategy, targeting, large budget swings, ACCELERATED pacing.
- Automation hygiene: log changes with reasons; one budget change per ad squad per 2 days; respect API rate limits (section 11).

## 10. Metrics and definitions
Names are as commonly shown in Ads Manager / the stats API; exact column names: `unverified`.
| Standard | Snapchat term | Note |
|---|---|---|
| Impressions | Impressions | |
| Reach / Frequency | Uniques / Frequency | |
| CPM | eCPM | spend per 1,000 impressions |
| CTR | Swipe-up rate (swipes / impressions) | "swipe" is the click equivalent |
| CPC | Cost per swipe | |
| Results | Results by optimization goal | e.g. Purchases, Sign ups, Lead form submissions |
| CPA | Cost per conversion | |
| CVR | Conversion rate (conversions / swipes) | |
| ROAS | Purchase ROAS | needs PURCHASE with price |
| Hook / view rate | Video views (3 s+) / impressions | practitioner metric; Snap also tracks 15-second views and quartiles |
| Screen time | Average screen time | engagement metric specific to Snap |
Stats granularity: hourly, daily or total via the API [official]. State the attribution window with every number.

## 11. API and automation
- Official API: Snapchat Marketing API (https://developers.snap.com/api/marketing-api/Ads-API/introduction) plus the Conversions API and the Public Profile API.
- What can be automated [official]: manage campaigns, ad squads and ads; upload media and build creatives; Dynamic Product Ads from catalogs; sponsored AR Lenses and Filters; targeting and custom audiences from hashed data; performance stats; lead collection forms; Smart Budget; spend guidance. RESERVED campaigns cannot be modified via the API.
- Access: create an OAuth app in Business Manager (Business Details) as an Organization Admin; client_secret is shown once; authorize at accounts.snapchat.com/login/oauth2/authorize, exchange the code at accounts.snapchat.com/login/oauth2/access_token; access tokens last 3,600 seconds and are refreshed with the refresh token; scopes: snapchat-marketing-api, snapchat-offline-conversions-api, snapchat-profile-api [official: https://developers.snap.com/api/marketing-api/Ads-API/authentication]. Whether the app needs approval before production use: `unverified`.
- Rate limits [official: https://developers.snap.com/marketing-api/Ads-API/rate-limits]: the app averages 20 requests per second; each access token averages 10 requests per second; exceeding returns HTTP 429; reduce request rate. CAPI: 10 requests per second per standard limit, batches up to 2,000 events (see section 7). Other codes: 400, 401, 403, 404, 405, 406, 410, 429, 500, 503.
- Built-in automation in Ads Manager: Smart Budget (campaign-level budget optimization), AUTO_BID, automatic placements, audience expansion options. Automated rules in Ads Manager: `unverified`.
- Rules for agents making automated changes: obey rate limits with backoff; do not change optimization goals on live ad squads; budgets at most once per 2 days; never auto-resubmit rejected ads in loops; refresh tokens before expiry; never store client_secret or tokens in repos or logs.

## 12. Cases
**Ad rejected**
- **Situation**: Ad status REJECTED with reasons.
- **Do**: read review_status_reasons; fix the cited element (claim, imagery, landing page, age targeting); for restricted categories submit pre-approval forms; resubmit as a new ad.
- **Avoid**: changing the landing URL after approval to something different (prohibited), guaranteed-returns language, before / after weight-loss images.

**Account disabled**
- **Situation**: Ad account suspended or terminated.
- **Do**: identify the policy cited; contact Snap support / account manager; submit documents; stop all similar ads.
- **Avoid**: opening new accounts to keep running the same ads.

**Spend without results**
- **Situation**: Spend with no conversions.
- **Do**: verify the pixel and CAPI (Events Manager Diagnostics), dedup, event names, landing page speed and mobile format; check the optimization goal volume; try SWIPES or LANDING_PAGE_VIEW goal; refresh creative (first 2 seconds).
- **Avoid**: raising budget; many ad squads.

**CPA doubled**
- **Situation**: CPA doubled.
- **Do**: check edits, budget jumps, creative fatigue, tracking or site changes, attribution window, competing seasonal demand; wait 48 hours unless tracking is broken.
- **Avoid**: switching bid strategy and goals at the same time.

**Learning / unstable delivery**
- **Situation**: Delivery is erratic after a change.
- **Do**: stop editing; widen the audience; remove an over-tight bid cap or target cost; use AUTO_BID; consolidate ad squads.
- **Avoid**: ACCELERATED pacing with cost controls.

**Creative fatigue**
- **Situation**: Swipe rate down, CPM up.
- **Do**: new hooks, formats (Story / Collection / Lens), new Public Profile content; rotate more often in small countries such as Kuwait.
- **Avoid**: leaving the same creative for weeks on a small audience.

**Tracking mismatch**
- **Situation**: Snap shows more purchases than the shop.
- **Do**: compare equal windows (28-day swipe plus 1-day view default); confirm event_id / client_dedup_id match; check transaction_id / order_id; remove duplicate pixels; check sc_click_id passing.
- **Avoid**: comparing a 28-day Snap window to GA4 last-click.

**Tiny budget**
- **Situation**: Very small daily budget.
- **Do**: one ad squad, above the ad squad minimum (5 currency units per day per the doc; campaign minimum US$20 per the doc), optimize SWIPES / LANDING_PAGE_VIEW, 2-3 creatives, run 7+ days unedited.
- **Avoid**: purchase optimization without volume.

**Local lead-gen / WhatsApp-click campaigns (Gulf / Egypt)**
- **Situation**: Business wants phone, message or form leads.
- **Do**: use the Leads objective with a lead form, or an AD_TO_CALL / AD_TO_MESSAGE attachment (CTAs Call Now, Message Now); a web CTA to a WhatsApp click-to-chat link tracked as an event; follow up quickly; keep sensitive-data fields out of forms.
- **Avoid**: promising results in health or finance; collecting ID numbers or health data.

**Scaling too fast**
- **Situation**: Budget doubled and CPA rose.
- **Do**: revert to the last stable budget; scale about 20% every 2-3 days or duplicate ad squads; use Smart Budget for allocation.
- **Avoid**: raising bid caps and budget together.

**Seasonal peak (Ramadan, White Friday, Saudi National Day)**
- **Situation**: Demand spike and CPM inflation in the Gulf.
- **Do**: schedule creative and budgets weeks ahead; consider Commercials or Lenses for reach; add retargeting and Collection Ads with real prices and stock; raise budgets in steps before the peak.
- **Avoid**: launching new goals or untested creative on the peak day; assuming last year's CPA applies. No reliable seasonal benchmark was found.

## 13. Pre-launch checklist
1. Is the ad account timezone (Africa/Cairo, Asia/Riyadh, etc.) and currency correct and confirmed for the advertiser's payment method?
2. Is a valid funding source attached (card, PayPal, credit line)?
3. Is the Public Profile attached and the brand name within limits?
4. Does the Snap Pixel fire, and is CAPI connected with the same event names and IDs?
5. Is client_dedup_id = event_id and, for purchases, transaction_id = order_id?
6. Is the CAPI event_time within 7 days and PII hashed with normalization?
7. Is the optimization goal expected to produce enough events per day?
8. Is the bid strategy valid for the goal (not MIN_ROAS; TARGET_COST only on allowed goals)?
9. Are ad squad budgets at or above the minimums and the campaign budget at least 0.25x the sum of ad squad budgets?
10. Are creatives 9:16, correct resolution, within file size limits and with a strong first-second hook?
11. Is the headline within 34 characters and the brand name within limits?
12. Is the creative free of prohibited claims (guaranteed returns, weight-loss before / after, exaggerated health claims)?
13. Is the landing page mobile-formatted, working, matching the ad, and not changed after submission?
14. Is age targeting compliant for the category (18+ where needed)?
15. Are restricted categories pre-approved?
16. Is the attribution window (default 28-day swipe, 1-day view in API) recorded?
17. Is there a UTM scheme and sc_click_id passing?
18. Are API rate limits and token refresh handled if automation is used?

## 14. Sources
- https://developers.snap.com/api/marketing-api/Ads-API/introduction
- https://developers.snap.com/api/marketing-api/Ads-API/authentication
- https://developers.snap.com/marketing-api/Ads-API/rate-limits
- https://developers.snap.com/api/marketing-api/Ads-API/errors
- https://developers.snap.com/api/marketing-api/Ads-API/campaigns
- https://developers.snap.com/api/marketing-api/Ads-API/ad-squads
- https://developers.snap.com/api/marketing-api/Ads-API/ads
- https://developers.snap.com/api/marketing-api/Ads-API/ad-accounts
- https://developers.snap.com/api/marketing-api/Ads-API/funding-sources
- https://developers.snap.com/api/marketing-api/Ads-API/creatives
- https://developers.snap.com/api/marketing-api/Ads-API/media
- https://developers.snap.com/api/marketing-api/Ads-API/measurement
- https://developers.snap.com/api/marketing-api/Conversions-API/GetStarted
- https://developers.snap.com/api/marketing-api/Conversions-API/Parameters
- https://developers.snap.com/api/marketing-api/Conversions-API/Deduplication
- https://developers.snap.com/api/marketing-api/Conversions-API/BestPractices
- https://snap.com/en-US/ad-policies
- https://forbusiness.snapchat.com/advertising
- https://forbusiness.snapchat.com/advertising/ad-formats
- https://datareportal.com/reports/digital-2026-saudi-arabia , -united-arab-emirates , -kuwait , -egypt
- https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/ (secondary, tax)
- Not readable (client-rendered), cited by title only: https://businesshelp.snapchat.com/s/article/top-snap-specs
