# TikTok Ads — rules and playbook
Last verified: 2026-10-19

Scope: TikTok Ads Manager (auction buying), Spark Ads, Smart+ automation, lead generation, Events API and the TikTok API for Business. Source key: **[official]** = TikTok Business Help Center / policy / dev page read on 2026-10-19; **[secondary]** = third party; **[practitioner]** = observation, not an official rule; `unverified` = not confirmed. Research note: the TikTok help center renders article by article and many guessed article URLs returned "article no longer exists"; the developer portal (business-api.tiktok.com) is JavaScript-rendered and could not be read. Everything about API endpoints, rate limits, Smart+ internals, bidding, payment methods and attribution defaults is therefore marked `unverified` unless a source is given.

## 1. When to use it
- Strengths: young, mobile-first, sound-on short-video audience; strong for discovery, creator-style (UGC) creative, app installs, e-commerce, local offers and lead generation; Spark Ads lets you boost organic posts and creator content with social proof.
- Weaknesses: creative-hungry (fatigue is fast), results depend on vertical video with audio; weaker search-style intent; policy review is strict on claims, health, finance and misleading UI; lower conversion intent than search for many B2B / high-ticket offers [practitioner].
- Best objectives: Reach, Traffic, Video views, Community interaction, App promotion, Conversions (website), Lead generation, Sales (product / TikTok Shop). The Spark Ads help article lists these as the objectives supported under auction buying; Reach & Frequency buying supports only Reach, Traffic and Video views. https://ads.tiktok.com/help/article/spark-ads
- Egypt / MENA relevance (DataReportal Digital 2026, published 2025-11-08; "ad reach" figures reported by the platforms, not MAU; adults 18+ for TikTok):
  - Egypt: TikTok 48.8M adults 18+ (+25.2% since end-2024); Facebook 51.6M; Instagram 21.7M; Snapchat 20.6M. https://datareportal.com/reports/digital-2026-egypt
  - Saudi Arabia: TikTok 38.6M adults 18+; Snapchat 25.3M; Instagram 18.2M; Facebook 17.7M. https://datareportal.com/reports/digital-2026-saudi-arabia
  - UAE: TikTok 12.5M adults 18+; Snapchat 5.13M; Facebook 9.70M; Instagram 8.05M (figures above 100% of population appear in the source and may be anomalous). https://datareportal.com/reports/digital-2026-united-arab-emirates
  - Reading: TikTok reach is comparable to Facebook in Egypt and far larger than Snapchat; in the Gulf it is a primary awareness and performance channel.
- Benchmarks: no reliable public CPM / CTR / CPA benchmarks for Egypt or MENA were found. Do not quote any; derive targets from the client's margin and own data.

## 2. Account, billing and access
- Structure: TikTok Business Center (central place for assets, ad accounts, members, billing) -> Ad account(s) -> Pixel / Events API datasets, TikTok accounts (for Spark Ads), catalogs, audiences, lead assets. Business Center supports role-based user management, sharing assets with internal teams and outside partners, finance management (billing, payments, invoices), 2-Step Verification and an email-domain allowlist, and an Enterprise Business Center for agencies. https://ads.tiktok.com/help/article/tiktok-business-center
- Agency access: share the ad account, pixel, TikTok account and catalog with the agency's Business Center through partner sharing; keep the client's Business Center as the owner [practitioner pattern, follows the documented sharing features].
- Verification: some industries require certificates / industry entry (see section 8). Business verification steps and review times for general advertisers: `unverified`.
- Payment (Egypt): per TikTok's EMEA payment page, pre-pay in EGP by bank card or Fawry (or USD by card/PayPal), autopay in EGP by card, and a monthly-invoicing credit line in EGP by card or Fawry. Source: https://ads.tiktok.com/help/article/europe-middle-east-and-africa-emea-supported-payment-methods (verify in Business Center > Billing). USD is the only currency in which TikTok publishes its budget minimums (see section 5).
- Tax: Egypt's Tax Authority guidance applies 14% VAT to digital services from non-resident providers (vatcalc summary of ETA guidance, 2023: https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/); an Egyptian accountancy article (2025-01-30) says social-media ads should be covered by e-invoices and that foreign platforms are expected to withhold tax: https://ecpa-eg.com/en/eg/articles/coding-of-ads-on-social-media-for-the-egyptian-tax-authority. How TikTok itself invoices Egyptian advertisers: `unverified`. Confirm with the client's accountant.

## 3. Campaign structure
Hierarchy: Campaign (objective, buying type, optional campaign budget) -> Ad group (placement, audience, budget, schedule, optimization goal, bid) -> Ad (video / image / Spark post, text, CTA, destination).
- Objectives (as shown in Ads Manager): reach, video views, conversions, app promotion, lead generation, sales (https://ads.tiktok.com/business/en/solutions/ads-manager); plus Traffic and Community interaction per the Spark Ads article.
- Buying types: Auction (all objectives) and Reach & Frequency (Reach, Traffic, Video views only).
- Smart+ (automation): TikTok's "What's new" lists an upgraded Smart+ for SMBs with full, partial or manual control; Smart+ Lead Generation supports multiple locations in one campaign; a "Summary" feature explains Smart+ results (https://ads.tiktok.com/resources/blog). Exact Smart+ campaign types (Web, App, Catalog), minimum requirements and which levers you can still control: `unverified`; read the in-product description before use. What Smart+ generally automates (audience, creative combination, budget allocation) is [practitioner]; verify.
- Recommended structure (TikTok's own creative guidance): 3-5 creatives per ad group and 3-5 diversified ad groups per campaign; add new creatives to existing ad groups rather than creating new ones. https://ads.tiktok.com/help/article/creative-best-practices
  - Small budget: 1 campaign, 1 ad group, 3-5 creatives, a daily ad group budget (not lifetime) set from the formula in section 5.
  - Medium: separate prospecting and retargeting campaigns; 2-3 ad groups each with different audiences or optimization goals; run structured tests with Split Test.
  - Large: dedicated creative-testing campaign, scaling campaigns by product / market, Spark Ads from creator partners, Smart+ for scale when manual structures plateau.
- Split testing: Split Testing divides the audience evenly so ad groups do not compete for the same users; variables include targeting, placement, bidding and optimization, budget strategy, creative, catalog, custom and Smart+; the model names a winner only when results reach statistical significance (90% confidence). Budget and duration minimums: not given in the article. https://ads.tiktok.com/help/article/split-testing

## 4. Targeting and audiences
- Exists: location, language, age, gender, interests and behaviors, device / OS, custom audiences (website via pixel / Events API, customer file, app activity, engagement such as video views and profile visits, lead gen form interactions), lookalike audiences, broad / automated audiences under Smart+. Exact list and sizes for the Egypt / MENA markets: `unverified`.
- Restrictions: sensitive-data collection and targeting is limited (lead forms must not collect sensitive data without written consent from a TikTok representative); financial, alcohol, gambling and health ads have age and market rules; housing, employment and credit ads have separate rules. Teen and minors protection policy exists (rules not retrieved): `unverified`.
- Arabic / regional: ad and landing page language and currency must match the ad's setting language or be acceptable for the market; multi-market ad groups must only target markets where the ad and landing page language match [official: https://ads.tiktok.com/help/article/tiktok-ads-policy-ad-format-and-functionality]. So run separate ad groups for Egyptian Arabic, Gulf Arabic and English audiences.
- Spoken-audio clarity and natural speech for the target market are required by policy; dialect-matched voiceover (Egyptian Arabic for Egypt; Gulf dialect for KSA / UAE) is [practitioner] best practice.

## 5. Bidding, budget and delivery
- Bid strategies: TikTok's bidding article was not readable. Strategies commonly offered are lowest cost (maximum delivery), cost cap and bid cap; confirm names in Ads Manager: `unverified`. One fact from official budget guidance: setting up or changing a Maximum Delivery strategy mid-day may reduce spend based on the remaining effective delivery hours.
- Budget types: daily or lifetime at campaign and ad group level; you cannot switch between daily and lifetime once live; the campaign budget should not be lower than the ad group budget; when an ad group exhausts its budget, delivery pauses until the budget or schedule is raised. [official, last updated July 2026: https://ads.tiktok.com/help/article/budget]
- Minimums (USD only; no other currency is published; confirm the minimum in your account currency in the UI):
  - Daily, campaign: more than $50. Daily, ad group: more than $20.
  - Lifetime, campaign: more than $50. Lifetime, ad group: $20 multiplied by total campaign days including past days (31 days = $620).
- Recommended minimum daily ad group budget relative to CPA [official: https://ads.tiktok.com/help/article/budget-best-practices; date not shown]: shallow / non-conversion goals 50x CPA or CPR; install campaigns 20x CPA; deep conversion campaigns (add to cart, purchase) 10x CPA. With no CPA history, floors of $100 (non-conversion, shallow) and $200 (install, deep conversion) or equivalents. Use a daily budget, and leave the campaign budget open at first.
- Learning phase [official: https://ads.tiktok.com/help/article/learning-phase]: volatility typically declines after about 25 campaign results or 7 days from entering learning. The article cautions against edits that re-trigger learning (it does not list them), pausing campaigns or ad groups, and unreasonable budgets or creative volumes. For conversion campaigns, avoid changing targeting, bids or budget until learning ends.
- Budget changes (two TikTok articles disagree, use the stricter): the July 2026 budget article says increase by no more than 40% per adjustment while in learning and no more than 30% out of learning, with at least 2 days between adjustments. The budget best-practices article says stay within a 50% range of the previous budget after learning and wait at least 2 days between targeting, bid or budget changes. Default for agents: <=30% once every 2+ days, <=20% if CPA is near the limit.
- Pacing and frequency: lifetime-budget spend may be uneven across days but will not exceed the total. Frequency caps are available under Reach & Frequency buying; auction frequency controls: `unverified`.

## 6. Creative specs and requirements
Sources are limited; always verify in the upload UI. Policy requirements from https://ads.tiktok.com/help/article/tiktok-ads-policy-ad-format-and-functionality and https://ads.tiktok.com/help/article/creative-best-practices.

| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| In-feed video (auction) | 9:16 recommended; 1:1 and 16:9 supported | at least 720p (best practices); suggested minimums 720x1280, 640x640, 1280x720 (spec article) | 5-60 s per policy page | up to 500 MB per the spec article for the placements it lists; In-Feed row itself `unverified` | ad text and display name limits: spec article gives display / brand name 2-20 Latin chars (4-40 for app names), ad description 1-100 Latin chars for the placements it lists; In-Feed values `unverified` | audio required and clear; must be dynamic (static image not main element, not over 50% of video); bitrate at least 516 kbps in spec article |
| Spark Ads (organic post) | any | no restrictions on ratio, resolution, type, duration, bitrate, size | max 10 min | n/a | display name and text come from the post; not editable in Ads Manager | up to 10,000 Spark Ads per ad account; banned organic posts are rejected; un-authorize before deleting the organic post |
| Image / carousel ads | `unverified` | `unverified` | n/a | `unverified` | `unverified` | not retrieved |
| Instant Form (lead gen) | n/a | n/a | n/a | n/a | privacy policy link required | see policies |
| Pangle / Global App Bundle | 9:16, 1:1, 16:9 | suggested min as above | 5-60 s (Pangle); 30 s (App Bundle) | 500 MB | description 1-100 Latin chars (Pangle) | app profile image 1:1 under 50 KB |
Spec article: "List of Video Ad Specifications", last updated July 2024: https://ads.tiktok.com/help/article/video-ads-specifications

- Creative guidance [official: creative best practices]: vertical 9:16, at least 720p, use sound or music, keep key content inside the UI safe zone, state the value proposition within 3 seconds and prioritize the hook within 6 seconds, captions at about 5-10 words per second, native / creator / UGC style, trends when relevant, hook -> selling points -> clear CTA, refresh creatives when results decline.
- Do not use: QR codes in ad content (packaging QR allowed), "swipe up" text (it only advances to the next video), motionless ads in listed markets (US, UK, Canada), misspellings and excessive caps, blurred or masked third-party watermarks, a Hashtag Challenge page as landing page.
- Arabic / RTL cautions [practitioner]: check caption placement against TikTok UI overlays; right-aligned Arabic captions can collide with the right-side action buttons; keep captions within the safe zone, use high-contrast legible fonts, avoid mixing Latin brand names mid-sentence without testing the rendering, and add burned-in captions because many people watch muted in public places even though audio is required by policy.

## 7. Tracking and measurement
- Pixel: JavaScript tag for your website; standard events (view product, add to cart, purchase, etc.), managed in Events Manager; cookies for measurement, optimization and targeting (third-party on by default, first-party optional); Advanced Matching can improve performance; use Pixel Helper to check what is sent; no sensitive data. https://ads.tiktok.com/help/article/tiktok-pixel
- Events API: server-to-server; supports website, app and offline (store / CRM) data; Pixel or Events API setup is a prerequisite for the Web Conversions objective; TikTok recommends running both with deduplication and sending consistent events with all relevant match keys. https://ads.tiktok.com/help/article/events-api
- Deduplication [official: https://ads.tiktok.com/help/article/event-deduplication]: required if you send the same event through both Pixel and Events API; pass the same event_id from both; the first event received is kept; Pixel-to-Pixel and API-to-API duplicates with same event name and event_id are deduplicated within 48 hours; for Pixel plus Events API the article says matching events merge when they arrive more than 5 minutes apart and within 48 hours of the first. Not needed when different events travel via different channels (for example, AddToCart via Pixel and Purchase via API).
- Events to send: ViewContent, AddToCart, InitiateCheckout, CompletePayment (Purchase), SubmitForm / Lead, Contact, with value and currency; exact event names in TikTok's current list: confirm in Events Manager (`unverified`).
- Apps: the legacy MMP integration ended 2025-03-31; apps must use SAN (Self-Attributing Network) integration with MMPs; SAN adds engaged view-through attribution (watched more than 6 seconds). https://ads.tiktok.com/help/article/about-self-attribution-transition
- Attribution windows: adjustable in Ads Manager; the default lengths for click-through, view-through and engaged-view were not retrievable: `unverified`. Always record the window used in reports.
- UTM convention: utm_source=tiktok, utm_medium=paid_social, utm_campaign={campaign name}, utm_content={ad name}; TikTok supports macro parameters in the URL (for example campaign / ad group / ad name and ID placeholders); exact macro names: `unverified`.
- Platform vs GA4: TikTok includes view-through and engaged-view conversions and a longer window, so it reports more than GA4's last-click; much TikTok traffic is in-app browser, which can lose cookies and under-report in GA4 [practitioner].
- Privacy: iOS ATT limits app measurement (SAN / SKAdNetwork); GDPR / UK consent applies to the pixel in the EU; in Egypt the Personal Data Protection Law (Law 151 of 2020) applies: `unverified` details. Lead forms need a clear privacy policy link and must not collect sensitive data.

## 8. Policies and restricted content
Policy index and industry entry: https://ads.tiktok.com/help/article/tiktok-advertising-policies-industry-entry . Categories listed there: ad format and functionality, adult content, alcohol, animals and environment, dangerous products, deceptive practices, discrimination / harassment, financial services, gambling and games, healthcare and pharmaceuticals, IP infringement, misinformation, misleading and false content, other products and services, politics / governments / elections, suicide and self-harm, teen safety, TikTok After Conversion Experience policy, violence, weight management and body image. Also: housing / employment / credit ads, industries requiring certificates, branded content, data collection, government and NGO advertisers, market-specific approval requirements.
- Ad review: automated plus human review before delivery and during delivery; poor-quality signals can mean rejection, fewer impressions or a higher cost per impression (landing page rules page). Review SLA and appeal steps were not retrievable: `unverified`; use the rejection notice in Ads Manager and the appeal option attached to it.
- Top rejection causes (from official policy pages):
  1. Misleading claims: promising or exaggerating effects, absolute claims about time, region or brand (examples: "slim legs right away", "money in 10 seconds", "number 1 song on TikTok"); before-and-after comparisons that could give a false impression (wrinkles disappearing); negative comparisons with other brands; fake play / close / CTA buttons and blurred clickbait. https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content
  2. AI-generated or significantly AI-edited media without a label or clear disclosure; using a public figure's likeness without permission.
  3. Landing page problems: broken, under construction, not mobile-friendly, auto-download, high ads-to-content ratio, missing e-commerce information (contact details, company name and address, business license, local-currency prices, shipping, returns, refunds, terms, privacy policy), mismatch between ad and page (offer, price, brand, display name).
  4. Format and functionality: no or poor audio, static content, QR codes, "swipe up", spelling errors, excessive caps / symbols.
  5. Lead forms without a privacy policy, or collecting sensitive data (health, religion, ID numbers, finances, exact age or date of birth, etc.) without written consent from a TikTok representative.
  6. Restricted categories without approval.
- Restricted / prohibited examples: financial services (licence, disclaimers, adults only; get-rich-quick, pyramid schemes, MLM, penny auctions, payday loans prohibited or common bans; crypto often restricted and needs approval) https://ads.tiktok.com/help/article/tiktok-ads-policy-financial-services ; gambling (certification, licences, never to minors, only where legal) ; alcohol (local-law based, show strength and responsible-drinking message, no people under 25 shown, no excessive drinking) ; other products and services (many conditional or banned by market: real estate needs local licence; VPN, horoscope and fortune-telling banned in many Middle Eastern markets; energy drinks banned in Kuwait among others; legal services restricted; as of March 2026 per the article) https://ads.tiktok.com/help/article/tiktok-ads-policy-other-products-and-services . The weight management / body image and healthcare policy pages were not retrievable: treat health, weight loss and cosmetic claims as high risk and `unverified`. Egypt-, KSA- and UAE-specific allow / ban lists per category: `unverified`; read the market-specific requirements in each policy article.
- Account ban causes: deceptive or inauthentic behavior or patterns of abuse; distributing high volumes of identical content across accounts; repeated policy violations. https://ads.tiktok.com/help/article/tiktok-ads-policy-deceptive-practices
- While rejected: read the exact reason; fix text, video, landing page and display name together; resubmit as a new ad if the creative changed; keep compliant ads running; do not mass-resubmit identical content.

## 9. Optimization playbook
Order of inspection: (1) delivery status, review status, budget exhausted, payment; (2) tracking: pixel / Events API events and deduplication, event counts vs the shop or CRM; (3) learning status (about 25 results / 7 days); (4) creative diagnostics (hook, completion, CTR); (5) audience and bid.
- Wait: judge an ad group only after learning (about 25 results or 7 days per TikTok) and after spend of at least 2-3x target CPA [practitioner threshold]. Do not edit targeting, bids or budget during learning (official guidance for conversion campaigns). Do not pause ad groups to "save" budget.
- Cut: ad (not ad group) with spend above ~2-3x target CPA, no conversions and weak hook / CTR vs siblings; ad group that stays unprofitable after learning and a fresh creative round [practitioner].
- Scale: raise budget no more than 30% per change out of learning (40% inside), at least 2 days between changes; or duplicate the winning ad group with a new budget. Do not stack budget, bid and audience changes in one go.
- Budget per variant: set the ad group daily budget at about 10x CPA for deep conversion goals, 20x for installs, 50x for shallow goals (official floors above). Reason: that is TikTok's stated minimum for the optimizer to gather enough results. If the client cannot afford it, test fewer ad groups, optimize one step higher in the funnel (for example add to cart or lead) and judge creatives on hook rate and CTR.
- Creative fatigue [practitioner]: CTR and hook rate falling, CPM rising, frequency rising, daily new users falling (TikTok's own guidance says refresh creatives when results decline or daily new users drop). Response: add new creatives into the existing ad group (TikTok advice), including new hooks on the same winning concept; Spark Ads from fresh creator posts.
- Creative testing: 3-5 creatives per ad group; change one variable (hook, first 3 s, offer, CTA); run until each has statistically meaningful spend; use Split Test for audience / bid / budget variables (90% confidence).
- Not to touch during learning: targeting, bid strategy or bid amount, optimization event, large budget changes, pausing / unpausing, adding many creatives at once.
- Automation hygiene: log each change with its reason; at most one budget change per ad group per 2 days; respect the client's approval for spend increases.

## 10. Metrics and definitions
Names below are as shown in TikTok Ads Manager columns; confirm in the column picker (`unverified` for exact wording).
| Standard | TikTok name | Note |
|---|---|---|
| Impressions | Impressions | |
| Reach / Frequency | Reach / Frequency | |
| CPM | CPM (cost per 1,000 impressions) | |
| CTR | CTR (destination) | clicks to destination / impressions; "CTR (all)" includes profile clicks etc. |
| CPC | CPC (destination) | |
| Results | Results / Cost per result | depend on optimization goal |
| CPA | Cost per conversion | |
| CVR | Conversion rate (CVR) | conversions / clicks |
| ROAS | ROAS (purchase) / Total purchase value | needs value passed back |
| Hook rate | 2-second video views / impressions (compute) or "2-second view rate" | practitioner metric; TikTok also reports 6-second views |
| Hold / completion | Average play time, video views at 25 / 50 / 75 / 100% | |
| Engaged view | Engaged view-through | counts viewers who watched more than 6 seconds (SAN article) |
Always state attribution window and date range.

## 11. API and automation
- Official API: TikTok API for Business (Marketing API) covering Ads Manager, TikTok accounts and the Creator Marketplace; portal https://business-api.tiktok.com/portal/docs (JavaScript-rendered; not readable here). Official SDK libraries exist for Java, Python and JavaScript (repo reports API version 1.0.1): https://github.com/tiktok/tiktok-business-api-sdk . Each call takes an access token; you register as a developer, create an app and obtain authorization.
- What can be automated: campaign / ad group / ad management, creative upload, audience management, reporting (including async reports), Business Center administration, Events API. Spark Ads authorization via authorization code (the Spark article says code duration is customizable).
- Endpoints, versions, rate limits, app review requirements: `unverified`. Implement exponential backoff and read the portal's rate-limit section before building.
- Built-in automation: Smart+ (see section 3) and Ads Manager automated rules: `unverified` in detail. Treat any rule change as an edit that may re-trigger learning.
- Rules for agents making automated changes: follow section 9; do not auto-edit live ads; never push unhashed PII to the Events API; store tokens in a secret manager.

## 12. Cases
**Ad rejected**
- **Situation**: Rejected for misleading claim, landing page or format.
- **Do**: read the reason; remove absolutes and before / after claims; add the AIGC label if AI-edited; fix landing page (contact details, policies, currency); ensure display name matches the page; resubmit once.
- **Avoid**: "swipe up" copy, QR codes, silent or static videos, repeated identical resubmissions.

**Account disabled**
- **Situation**: Ad account suspended.
- **Do**: identify the cited policy; submit the appeal in the notice with documents (business registration, licences); fix the cause; check payments.
- **Avoid**: opening new accounts to continue the same ads; spreading identical content across accounts (flagged as abuse).

**Spend without results**
- **Situation**: Spend of 2-3x target CPA, no conversions.
- **Do**: check the event fires (Pixel Helper, Events Manager), deduplication, landing page speed and relevance; check you are inside learning; test a new hook; consider optimizing a higher-funnel event.
- **Avoid**: budget increases, editing during learning.

**CPA doubled suddenly**
- **Situation**: CPA doubles overnight.
- **Do**: check edits, budget jumps, creative fatigue, tracking changes (SAN, event outage), site changes, stock / price; wait 48 hours unless tracking is broken.
- **Avoid**: reacting to one day.

**Learning limited / not exiting learning**
- **Situation**: Ad group volatile or stuck.
- **Do**: raise the budget toward the CPA multiple in section 5, optimize a higher-funnel event, consolidate ad groups, reduce changes.
- **Avoid**: many small ad groups, frequent pausing.

**Creative fatigue**
- **Situation**: CTR and daily new users falling.
- **Do**: add new creatives (new hook / creator) to the existing ad group; refresh Spark Ads posts.
- **Avoid**: rebuilding the ad group; relying on one asset.

**Tracking mismatch**
- **Situation**: TikTok reports more conversions than GA4 or the shop.
- **Do**: compare same window; confirm event_id deduplication; remember engaged-view and view-through; check in-app browser cookie loss; reconcile with server-side orders.
- **Avoid**: changing windows mid-flight.

**Tiny budget**
- **Situation**: Below the platform minimum for the objective.
- **Do**: use a single ad group at or above the ad group minimum (above $20 per day, USD equivalent) and an upstream goal such as landing page views or leads; run at least 7 days without edits; judge on cost per lead and hook rate. Note the 10x CPA minimum cannot be met.
- **Avoid**: purchase optimization without volume.

**Local lead-gen / WhatsApp-click campaigns**
- **Situation**: Business wants enquiries.
- **Do**: use the Lead generation objective with Instant Form (privacy policy link required; no sensitive-data fields), or website form conversion; respond fast; use Smart+ Lead Generation if suitable; for WhatsApp, use a landing page with a click-to-chat button and track the click as an event (no native click-to-WhatsApp destination was verified: `unverified`).
- **Avoid**: requesting sensitive data in forms; promising medical / financial outcomes.

**Scaling too fast**
- **Situation**: Budget doubled; CPA climbs.
- **Do**: return to the last stable budget; scale at most 30% per change every 2+ days; add creatives first.
- **Avoid**: multi-change edits.

**Seasonal peak (Ramadan, White Friday)**
- **Situation**: High demand, rising CPMs.
- **Do**: prepare creatives and landing pages in advance; raise budgets early in steps so learning is done before the peak; refresh creatives often; use trend-based and creator content.
- **Avoid**: launching untested ad groups on peak day; edits during peak. No reliable Egypt seasonal benchmark was found.

## 13. Pre-launch checklist
1. Is the Business Center set up with the client as owner and 2-Step Verification on?
2. Is a valid payment method and currency confirmed for the ad account?
3. Is the TikTok account linked (for Spark Ads) and authorization codes ready?
4. Does the pixel fire and is Events API connected with the same event_id for deduplication?
5. Is the optimization event expected to produce about 25+ results in the first 7 days at this budget?
6. Is the ad group daily budget at least the CPA-multiple floor and above the platform minimum?
7. Is the budget type (daily vs lifetime) final? (it cannot be changed after launch)
8. Are 3-5 distinct creatives in each ad group?
9. Are videos 9:16, at least 720p, with audio, hook inside 3 seconds, inside the safe zone?
10. Is there no QR code, no "swipe up", no absolute or before / after claim?
11. Is AI-generated content labeled where required?
12. Does the landing page load fast on mobile, match the ad, and show business details, prices in local currency, returns and privacy policy?
13. Is the ad and landing page language correct for each market?
14. Are lead forms free of sensitive fields, with a privacy policy link?
15. Is the restricted category (finance, health, alcohol, gambling) approved for the target country?
16. Is the attribution window recorded for reporting?
17. Is a UTM scheme in place?
18. Is a testing plan (one variable, Split Test where needed) written down?

## 14. Sources
- https://ads.tiktok.com/help/article/budget (last updated July 2026)
- https://ads.tiktok.com/help/article/budget-best-practices
- https://ads.tiktok.com/help/article/learning-phase
- https://ads.tiktok.com/help/article/creative-best-practices
- https://ads.tiktok.com/help/article/split-testing
- https://ads.tiktok.com/help/article/spark-ads
- https://ads.tiktok.com/help/article/tiktok-pixel
- https://ads.tiktok.com/help/article/events-api
- https://ads.tiktok.com/help/article/event-deduplication
- https://ads.tiktok.com/help/article/about-self-attribution-transition
- https://ads.tiktok.com/help/article/tiktok-business-center
- https://ads.tiktok.com/help/article/set-up-lead-generation-with-instant-form
- https://ads.tiktok.com/help/article/video-ads-specifications
- https://ads.tiktok.com/help/article/tiktok-advertising-policies-industry-entry
- https://ads.tiktok.com/help/article/tiktok-ads-policy-ad-format-and-functionality
- https://ads.tiktok.com/help/article/tiktok-ads-policy-misleading-and-false-content
- https://ads.tiktok.com/help/article/tiktok-ads-policy-financial-services
- https://ads.tiktok.com/help/article/tiktok-ads-policy-gambling-and-games
- https://ads.tiktok.com/help/article/tiktok-ads-policy-alcohol
- https://ads.tiktok.com/help/article/tiktok-ads-policy-other-products-and-services
- https://ads.tiktok.com/help/article/tiktok-ads-policy-deceptive-practices
- https://ads.tiktok.com/help/article/data-collection-standards
- https://ads.tiktok.com/business/en/solutions/ads-manager
- https://ads.tiktok.com/resources/blog (Smart+ headlines)
- https://github.com/tiktok/tiktok-business-api-sdk
- https://business-api.tiktok.com/portal/docs (landing only)
- https://datareportal.com/reports/digital-2026-egypt , https://datareportal.com/reports/digital-2026-saudi-arabia , https://datareportal.com/reports/digital-2026-united-arab-emirates
- https://www.vatcalc.com/egypt/egypt-vat-on-digital-services-foreign-providers/ , https://ecpa-eg.com/en/eg/articles/coding-of-ads-on-social-media-for-the-egyptian-tax-authority (secondary, tax)
