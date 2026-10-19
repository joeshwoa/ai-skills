# Pinterest Ads — rules and playbook
Last verified: 2026-10-19

Scope: Pinterest Ads Manager, objectives, ad formats, catalogs/shopping, Pinterest Tag and API for Conversions, specs, policies. Items marked `unverified` were not confirmed in an official source in this pass. "Practitioner observation" means lore, not an official rule. Honest summary for Egypt/MENA: Pinterest is a limited option there (section 1); verify access before promising a client anything.

## 1. When to use it
- What it is: a visual search/discovery platform where people save ideas ("Pins"); ads are Promoted Pins in the home feed, search results and related Pins (help targeting overview). The usual description is planning/shopping-oriented browsing (home, fashion, beauty, food, travel); that is general knowledge, not sourced in this pass, and no audience statistics were collected for Egypt/MENA.
- Strengths: shopping/catalog formats, keyword targeting inside Pinterest search, long-lived Pins, visual-first creative, "Performance+" automated bidding and targeting.
- Weaknesses: limited local availability and support in Egypt/MENA, no verified audience-size data for the region, shopping ads available only in some markets, and fewer measurement partners locally.
- Best objectives: Sales (catalog or Pins) for e-commerce; Consideration (Pin clicks/traffic); Leads (non-transactional events). Brand awareness remains in the product (default Performance+ bidding page names it).
- Egypt / MENA availability (official, Pinterest Ads overview, help node 821):
  - Direct ad account setup is listed only for a limited country list; the only Middle Eastern country on the direct list is Jordan. Egypt, Saudi Arabia and the UAE are NOT on the direct list.
  - For Egypt, Saudi Arabia, UAE, Bahrain, Iraq, Kuwait, Oman and Qatar, Pinterest points advertisers to a partner (Choueiri Group; the page gives a contact email at choueirigroup.com). Pinterest works with partners to manage ad accounts and bill locally in select markets. Israel and Turkey go through a different partner.
  - Pinterest appointed DMS (a Choueiri Group brand) as its sales representative in Algeria, Bahrain, Egypt, Iraq, Kuwait, Oman, Qatar, Saudi Arabia and UAE (published 2024-07-03).
  - The page also says shopping ads are available only in some listed markets and that Business Access accounts are limited to the listed countries. Whether Egypt supports shopping ads and catalogs: `unverified`; Pinterest says catalogs and the Pinterest Tag are "not available in every region".
  - Arabic language support in ads/targeting, local currency (EGP) billing, local payment methods: `unverified`.
- Rule: for Egypt-based advertisers, start by confirming with the Pinterest partner (not by trying to self-serve) that an ad account can be opened, which billing currency applies, and which formats are enabled. If answers are not confirmed in writing, recommend Meta/TikTok/Google for the same budget and treat Pinterest as a test.
- Benchmarks: no reliable CPM/CPC/CPA benchmark for Egypt/MENA was found; do not quote any.

## 2. Account, billing and access
- Structure: Pinterest Business account > Ad account (advertiser) > Campaign > Ad group > Ad. Tag and catalog are tied to the business/ad account. Roles/permissions model (admin, analyst etc.): not fetched; `unverified`.
- Account creation: direct for listed countries; via partner for Egypt/MENA (section 1).
- Billing (help how-billing-works): spend accrues while ads run; a charge triggers when spend reaches a billing threshold (example starts at $50 and rises after successful payments) or on the first day of the next month; the amount charged can exceed the threshold because it covers all spend to the end of the day. Custom billing threshold ($50, $100, $250, $500, $1,000 or system default) is available only for USD-billed ad accounts and cannot exceed the current threshold. Eligible advertisers can get monthly invoicing with a credit limit. Failed card charges must be cleared before switching to invoice billing.
- Payment methods and supported currencies: the billing page does not list them; `unverified`. Egypt-specific cards/currency: `unverified`.
- VAT/tax: not researched; `unverified`. If billed through a local partner, the invoice entity and VAT treatment come from the partner.
- Agency access: Pinterest supports partners/agencies that manage ad accounts and bill locally (help node 821). Exact steps for granting access: `unverified`.
- Verification: a "Verified Merchant Program" exists and requires specific tag events (tag page); business verification details were not fetched.

## 3. Campaign structure
- Hierarchy: Campaign (objective, budget option) > Ad group (targeting, schedule, bid, placements, budget) > Ad (Pin creative or catalog product).
- Objectives (Pinterest renamed objectives; announced 2026-09-08 per Social Media Today; Pinterest help "simplified objectives"):
  - Consideration: drives Pin clicks (CPC optimization) with catalog shopping ads or Pins.
  - Sales: transactional outcomes such as add-to-cart and checkout; with a catalog it optimizes for conversion/ROAS; with Pins, transactional events (CPM).
  - Leads: non-transactional outcomes (sign-ups, leads) with Pins.
  - Legacy "Conversions" and "Catalog sales" are being replaced; existing campaigns using them remain editable until 2027-04-30, after which they are archived. The rename does not change performance or ramp times (Pinterest statement via Social Media Today).
  - Awareness and Video views appear in an older help page ("Ads overview") and in the bidding page's list (Brand awareness); current status of those two objectives: `unverified`. Check Ads Manager.
- Campaign budget optimization shifts spend across ad groups toward the best results for the objective: Awareness optimizes impressions, Consideration clicks, Leads conversions, Sales clicks or conversions (budget help).
- Ad formats (help ads pages): standard image, video, max width video (paid only), carousel (2-5 images; sales objective 2-10 images and video from the catalog), collections (1 hero + 3-24 secondaries), idea ads, shopping ads (from catalog), showcase and quiz ads (named, not detailed).
- Buying: auction. Reservation products (Premiere Spotlight etc.): not covered on fetched pages; `unverified`.
- Recommended structure (heuristic):
  - Small budget: 1 Sales or Consideration campaign, 1 ad group, Performance+ bidding, broad keyword + interest combination, 3-5 creatives; test only if access is confirmed.
  - Medium: separate prospecting (keywords/interests/actalike) from retargeting (site visitors, engagement); separate catalog (shopping) from standard Pins.
  - Large: segment by product set/margin, run CBO, use Conversions API alongside the tag, test creative types (static, video, collections).

## 4. Targeting and audiences
- Options (help targeting-overview): audiences (customer lists, site visitors via tag, people who interacted with your content), actalike audiences (lookalike), interests, keywords (include/exclude; Pinterest search terms), demographics (gender, age, location, language, device), placement (home feed, search, related Pins), targeting templates, "Performance+" targeting expansion that extends to similar keywords/interests.
- Minimum audience size: not stated on the page; Ads Manager shows a "potential audience size" bar.
- Restrictions (Advertising guidelines):
  - No targeting by sensitive categories (health conditions, race/ethnicity, religion, sexual orientation/gender identity, political views, union membership, personal hardship) or proxies for them.
  - Ads cannot target Pinners under 18.
  - Credit, employment and housing ads have market-specific limits on actalike, age, gender, and postal-code targeting.
  - Some categories are approved but shown only to a limited audience.
- Arabic/regional notes: keywords in Arabic vs English availability and quality: `unverified`. Test Arabic and English keyword sets separately only if the account is confirmed to support Arabic Pins. Location targeting at governorate level: `unverified`.
- Contextual: keyword targeting is the main contextual lever. Include and exclude keywords (negative keywords exist as "exclude").

## 5. Bidding, budget and delivery
- Bid types (help set-your-bid): Custom (manual max bid) and Pinterest Performance+ (Pinterest manages bids, adjusting several times a day to get the most Pin clicks at the lowest cost per result while spending the full budget). Performance+ is the default for Consideration, Leads, Sales and Brand awareness. You can switch an ad group between Custom and Performance+ at any time. Ad group budgets are still required with Performance+.
- Minimum bids: each campaign type and country has a floor; for multiple countries the highest USD-converted floor becomes the minimum. Example from the page: a US/UK/Canada CPC campaign has floors of $0.10, GBP 0.07 and $0.10 (minimum $0.10). You pay only what you need to win. Floors for Egypt/MENA: `unverified`.
- Budget types (help set-up-campaign-budgets):
  - Lifetime: total spent flexibly across the flight.
  - Daily: Performance+ daily (an average; spend can go above or below) or Fixed daily (same amount each day).
  - Performance+ daily pacing: spend averages no more than the daily budget over a Sunday-to-Saturday week; Pinterest aims to keep any single day at or below 125% of the daily budget. A $100 budget may spend $125 one day and $75 another. Editing the budget mid-week or unpausing re-averages from that point to Saturday. Narrow audiences or restrictive bids can keep spend below budget.
  - Minimum budget: not stated on the budget page; `unverified`.
- Learning: the bid page says Performance+ costs can fluctuate, mostly at the start, while the algorithm explores; it gives no learning-phase length or conversion threshold. Treat as `unverified`; do not invent a number.
- How not to disturb delivery (practitioner observation): avoid frequent bid/budget/targeting edits in the first week; edits to targeting or description resubmit the ad for review (adds up to 24 h; help ad-review) and may interrupt delivery.
- Frequency: no frequency controls documented on fetched pages; `unverified`.
- Billing threshold and failed payment can stop delivery (section 2).

## 6. Creative specs and requirements
Source: Pinterest product specs page and Ads overview (help `pinterest-product-specs`, `ads`). Re-check before production.

| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Standard image ad | 2:3 recommended; wider may be cropped in feed | 1000x1500 px recommended | n/a | 20 MB desktop, 32 MB in-app; PNG or JPEG | Title 100 chars (first 40 show in feed; 30 for double-byte languages); description 800 chars (not shown in feed or close-up) | Pins taller/wider than 2:3 can be cut off; keep at or below 2:3 |
| Standard width video | between 1:2 and 1.91:1; square (1:1) or vertical (2:3, 4:5, 9:16) recommended | n/a on page | 4 s to 15 min; 6 to 15 s recommended | 2 GB; MP4, MOV, M4V (H.264/H.265) | same as image | |
| Max width video (paid only) | not wider than 1:1 (width cannot exceed height) | n/a | 4 s to 15 min; 6 to 15 s recommended | 2 GB | Title 100, description 800 (not shown in feed/search/close-up) | Ads overview page recommends square or 16:9 for max width, while the specs page limits width to at most height; conflict, check the builder |
| Carousel | 1:1 or 2:3 | n/a | n/a | 20 MB per image (non-sales) | same as image | 2 to 5 images (non-sales); sales objective 2 to 10 images and video, from catalog |
| Collections | static hero 1:1 or 2:3; video hero between 1:2 and 1.91:1; secondaries must all match | n/a | video hero 4 s to 15 min | 10 MB static; 2 GB video | Title 100, description 800 | 1 hero, 3+ secondaries recommended, up to 24; max width collections: hero video 1:1 or 16:9 and at least 4 secondaries |
| Idea ads | 9:16 (1080x1920 recommended) | 1080x1920 | videos 3 s to 5 min | about 16 MB recommended on Android/iOS; web: 20 MB images, 100 MB videos | multi-page with text | Ads overview page |
| Shopping ads | follow image/video specs | catalog images (see below) | n/a | n/a | from catalog | One image or video at a time |

- Catalog data source spec (help data-source-specification): required id, title, description, link, image_link, price, availability; add item_group_id for variants; missing or badly formatted required fields can fail the whole catalog ingestion. image_link at least 1000x1500 px (URL up to 2,000 chars, no placeholder); additional_image_link up to 10, each at least 75x75; title up to 500 chars; description up to 10,000 plain-text chars; price needs an ISO 4217 code if not USD (no symbols); files UTF-8; hosted data sources are fetched daily; up to 20 million products per retail catalog. A changed image needs a new URL to refresh.
- Destinations: website, board, profile or app deep link; UTM parameters and third-party click/impression trackers are allowed (ads overview).
- Ads are built from existing Pins or new Pins created in the Pin builder, then published and selected for promotion.
- Arabic/RTL cautions: Pinterest crops non-2:3 images in feed, so keep Arabic text inside the central area; right-to-left text in the first 40 title characters is what shows in feed; mixed Arabic/Latin titles can reorder; support for Arabic descriptions/keywords in search: `unverified`. Practitioner observation for the layout cautions.
- Creative guidance (practitioner observation): vertical 2:3 images with a clear subject, text overlay of 5-8 words, brand visible but not dominant, lifestyle context for products, video of 6-15 s with the product in the first 2 s. Pinterest's own creative best-practice pages were not fetched; `unverified`.

## 7. Tracking and measurement
- Pinterest Tag (help add-event-codes): base code on every page; event codes only on pages where the action happens. 20 standard event types including PageVisit, ViewCategory, Search, AddToCart, Checkout, Signup, Lead, WatchVideo, Subscribe, ViewContent, plus custom events. Event data: value, currency, order_quantity, order_id, line_items (product_id etc.), event_id and others; only value and order_quantity appear in paid and organic conversion reporting. Currency is converted to the ad account currency.
- Required events by goal: Conversion campaigns need at least one of Signup, Lead, AddToCart or Checkout; catalog sales need PageVisit, AddToCart and Checkout; dynamic retargeting needs product ID and value. The tag is "not yet available in all regions" per the help page.
- Enhanced match: an option in tag setup; details `unverified`.
- Pinterest API for Conversions (CAPI) (help the-pinterest-api-for-conversions; developers conversions best practices):
  - Sends web, app or offline events from your server; needs a Business account and an access token from Ads Manager Conversions page. Conversion access token allows unlimited conversion events.
  - Required per the best-practices page: event_time (Unix seconds), action_source (web, app_ios, app_android, offline), user_data with at least one of em (hashed email), hashed_maids, or client_ip_address + client_user_agent. Other fields (external_id, ph, ln, ct, st, zp, country, db, ge) recommended for all events.
  - Hash with SHA-256: em (lowercase), ph (digits with country code, no leading zeros), zp, st, ct, country, db (YYYYMMDD), ge (f, m, n), ln, external_id. Do not hash IP or user agent.
  - Deduplication: when using both Tag and API, send the same event_id from browser and server; Pinterest keeps the first event and removes duplicates within 48 hours. Event ID can be an order/transaction ID.
  - Send in real time or with at most one hour lag. Batch up to 1,000 events per request. Test with test=true (sandbox; test batches limited to 20 events).
  - Pass `_epik` cookie as click_id for add_to_cart, checkout, lead, page_visit.
  - Quality: Event Quality Score (EQS) and the Conversions Health page; aim for "Good".
- Attribution windows: Conversion insights default is 1-day view and 30-day click when none is set in Ads Manager; windows can be changed per account; 60-day is not available in Conversion insights (help conversion-insights). Conversion insights uses last-touch (credit to the last Pin engaged, organic or paid) and splits organic, paid unassisted, paid assisted. Ads Manager default attribution windows for reporting: `unverified` (the insights page says the Conversion insights default follows the Ads Manager setting).
- UTM: allowed in destination URLs (ads overview). Use utm_source=pinterest&utm_medium=paid_social. Convention.
- Pinterest vs GA4: expect differences (view and click windows, last-touch vs GA4 model, cross-device); no official reconciliation page fetched; `unverified`.
- Privacy/consent: Pinterest guidelines forbid collecting sensitive data through its ad services and joining ad-service data with personal identifiers (Advertising guidelines). Consent-mode-like controls, iOS ATT impact and GDPR handling for Pinterest tag: `unverified`; apply your CMP and only fire tag/CAPI with consent where required.

## 8. Policies and restricted content
Source: Pinterest Advertising guidelines (policy.pinterest.com, effective update 2026-11-12 noted on page).
- Review: up to 24 hours after creation; editing targeting or description resubmits (up to another 24 h). Disapproval shows in Ads Manager and by email from the ad-review address with the reason (help ad-review).
- Prohibited (examples): adult/nudity, clickbait, drugs and paraphernalia (including most CBD), endangered species/live animals, illegal products/services, counterfeits, political campaigning, sensitive/divisive content, tobacco, weapons/explosives; unacceptable business practices (penny auctions, payday loans, bail bonds, most cryptocurrency products, multilevel marketing, get-rich-quick schemes, social follower sales).
- Promotions: no sweepstakes, trade-in offers or discounts on free products; discount cannot exceed 90%; conditions must be clear.
- Restricted: alcohol (cannot target minors or link drinking to success), contests, financial products (disclosure; some need pre-approval), gambling (most online gambling prohibited), healthcare (prescription drugs and pharmacies need prior permission; disease prevention/cure claims prohibited). Country-specific rules apply (e.g. alcohol bans, licensing). Local-law compliance and permits may be requested.
- Health/weight loss: weight-loss language or imagery prohibited (narrow US/Canada GLP-1 exception); weight-loss pills/supplements, procedures, testimonials, BMI references prohibited; before-and-after weight-loss imagery prohibited; unrealistic cosmetic results prohibited; body shaming prohibited; exaggerated or "magical" claims prohibited.
- Landing pages: no forced sign-up unless the ad says so; no pop-ups, automatic downloads or forced redirects; must not be primarily advertising; ad image, description and landing page must be consistent and the product must be available on the page.
- Enforcement: Pinterest may reject or remove any ad that harms its relationship with Pinners, may remove advertisers with significant negative feedback or poor third-party ratings. Sanctioned regions are barred (Crimea, Cuba, Iran, North Korea, Syria, certain Ukraine regions).
- Appeals: email the ad-review team with the disapproval reason and the ad URLs (help ad-review). Escalation path for account-level suspension: `unverified`. Through a partner (Egypt), ask the partner's account manager to escalate.
- While rejected: fix the cause (claim, landing page, image), create a new Pin if needed, do not repeatedly resubmit the identical ad.
- Top rejection causes (from the guidelines above): weight-loss/health claims, before/after imagery, misleading or clickbait landing pages, restricted products without permission, disallowed business practices.

## 9. Optimization playbook
Numbers marked heuristic are practitioner rules, not Pinterest rules; Pinterest gives no learning-phase length.
1. Before spending: confirm account access, billing and region availability (section 1). Confirm the tag/CAPI events and EQS.
2. First look (day 3-7): delivery (impressions vs budget), Pin click rate, saves, outbound clicks (name `unverified`), checkout/lead events, spend pacing vs the 125% rule.
3. Wait rule (heuristic): Pinterest pins have slower discovery curves; judge Sales campaigns after at least 7-14 days and one attribution window. No official number.
4. Performance+ bidding first: start with Performance+ for new campaigns; switch to Custom bids only to control cost after you see the clearing range. Floors vary by country; do not set bids under the floor.
5. Scale (heuristic): budget +20% per step every 3-7 days when CPA/ROAS holds; use lifetime budgets for events; avoid mid-week resets (Performance+ daily averages from the edit to Saturday).
6. Cut: pause ad groups with spend above 2-3x target CPA and no conversions after tracking is verified (heuristic); keep keyword/interest tests small.
7. Creative fatigue: falling CTR/save rate for 7+ days; add new Pins (new images) not only new copy.
8. Test budget rule (heuristic): each creative variant should get enough budget for roughly 10 expected conversions or 1,000+ clicks before declaring a winner; for low volume, test on Pin click rate and accept lower confidence.
9. Catalog hygiene: feed errors can stop a whole feed; keep prices and availability current; new image requires a new URL.
10. What not to touch while delivery stabilizes: objective, optimization event, catalog source, and landing pages; edit targeting only when needed because edits can trigger re-review.
11. Dedup rule: if both Tag and CAPI are live, confirm event_id matches; otherwise conversions double count.
12. Retarget: use site-visitor audiences from the tag; exclude purchasers; check audience size before launching.

## 10. Metrics and definitions
Only names confirmed on fetched pages are marked; others are `unverified`.
| Pinterest name | Standard | Notes |
|---|---|---|
| Impressions | Impressions | Confirmed (Conversion insights) |
| Pin clicks | Clicks | Confirmed; Consideration optimizes Pin clicks (CPC) |
| Saves | Engagement | Confirmed in Conversion insights |
| Outbound click | Link click | `unverified` as a Pinterest metric name |
| CPM, CPC | CPM, CPC | Billing basis depends on objective and goal (Consideration CPC; Sales/Leads CPM per the objectives page) |
| Checkouts, Revenue, AOV, Page visits, Add to cart | Conversions, revenue | Confirmed in Conversion insights |
| Total conversions / CPA | CPA | Name `unverified`; compute as spend / conversions |
| ROAS | ROAS | Sales with catalog optimizes conversion/ROAS |
| Event Quality Score (EQS) | CAPI data quality | Confirmed (CAPI page) |
| Frequency | Frequency | `unverified` as a reported metric |
| Hook rate / thumb-stop | n/a | Not a Pinterest metric; use video view or 3-second view metrics if present; `unverified` |

## 11. API and automation
- Pinterest API v5 (developers.pinterest.com). Ads endpoints can read and create ads in both access tiers (access-tiers page).
- Access tiers: Trial (after app approval; sandbox content visible only to creator; 1,000 requests/day per app) and Standard (production; 100 requests/second per user per app). Upgrade requires a demo video of OAuth flow, privacy policy link and use case; common denial reasons: inaccessible privacy policy, vague description, demo missing authentication, non-OAuth login, demo without live integration. Appeals via Help Center ticket.
- Rate limits (developers.pinterest.com ratelimits): per category.
| Category | Trial (per day, per app) | Standard (per minute, per user, per app) |
|---|---|---|
| ads_analytics | 1,000 | 300 |
| ads_read | 1,000 | 1,000 |
| ads_write | 300 | 400 |
| ads_conversions | 1,000 per ad account | 120,000 per ad account |
- Test conversions (is_test true): 10 per app per second. Rate-limit headers: x-ratelimit-limit, x-ratelimit-remaining, x-ratelimit-reset. Limits can change without notice; 429 behavior not documented on the page.
- Automatable: reporting pulls, budget and status changes, creative/ad creation, catalog feed management, CAPI event upload. Needs Business account and token; store tokens outside the repo.
- Business account does not automatically give API access; an app must be approved (CAPI page).
- Built-in automated rules: not covered by fetched pages; `unverified`.
- Guardrails for agents: no budget changes within the same day as a manual edit; cap budget steps at 20%; never auto-edit targeting (it triggers re-review); alert on rejected ads and catalog errors.

## 12. Cases
**Situation: Ad rejected.**
**Do:** read the reason in Ads Manager/email; fix claim, image or landing page; email the ad-review team with the reason and ad URLs if it looks wrong; allow up to 24 h for re-review.
**Avoid:** weight-loss or before/after content, exaggerated claims, pop-ups on the landing page; resubmitting unchanged.

**Situation: Account disabled or cannot be opened (Egypt).**
**Do:** go through the Pinterest partner (Choueiri Group/DMS contact on the Ads overview page); ask for written confirmation of eligibility, currency and formats; keep documents ready.
**Avoid:** assuming self-serve works in Egypt; using a foreign entity or proxy billing to bypass local setup (policy and sanctions risk; `unverified` as a specific rule, but account accuracy is required).

**Situation: Spend without results.**
**Do:** verify the tag fires and events match the objective (conversion campaigns need Signup, Lead, AddToCart or Checkout); check feed errors; confirm CAPI dedup; review keyword relevance; wait for the attribution window.
**Avoid:** judging after 2 days; changing objective repeatedly.

**Situation: CPA doubled suddenly.**
**Do:** check recent edits (targeting, budget, creative), feed/price changes, conversion tracking breaks (EQS, Conversions Health), seasonality, auction competition (Performance+ costs rise or fall with competition).
**Avoid:** switching to Custom bidding blindly.

**Situation: Learning limited / low volume.**
**Do:** consolidate ad groups; use a higher-funnel event (AddToCart) until Checkout volume exists; widen keywords/Performance+ targeting.
**Avoid:** narrow audiences plus low bids (keeps spend below budget).

**Situation: Creative fatigue.**
**Do:** add new image/video Pins; refresh the first visual; test collections or idea ads.
**Avoid:** deleting top Pins; only changing text.

**Situation: Tracking mismatch (Pinterest vs GA4).**
**Do:** compare using 1-day view/30-day click vs GA4 model; check duplicate events; check CAPI event_id; trust CRM for leads.
**Avoid:** adding click and view conversions as if they were all clicks.

**Situation: Tiny budget.**
**Do:** one campaign, Performance+ bidding, broad keyword/interest mix, 3-5 Pins, Consideration objective (Pin clicks) to gather data.
**Avoid:** shopping catalog setup for a handful of products without confirmed regional availability.

**Situation: Local lead gen / WhatsApp (Egypt).**
**Do:** treat Pinterest as a low-priority channel for local lead-gen unless access and regional reach are confirmed; if used, Leads objective with a landing page and tracked WhatsApp click event.
**Avoid:** sending Pinterest budget to a market where partner onboarding is unconfirmed.

**Situation: Scaling too fast.**
**Do:** +20% budget every 3-7 days; keep the weekly average rule in mind (budget edits re-average to Saturday).
**Avoid:** doubling budgets mid-week.

**Situation: Seasonal peak (Ramadan, White Friday, Black Friday).**
**Do:** Pinterest users plan ahead (practitioner observation, not sourced), so start earlier than on other platforms; refresh catalog prices; launch creative early for review (up to 24 h).
**Avoid:** last-minute launches that hit ad review; promo claims above the 90% discount cap.

## 13. Pre-launch checklist
1. Is a Pinterest ad account confirmed for the advertiser's country (partner route for Egypt)?
2. Are billing method, currency and invoice entity confirmed in writing?
3. Does the offer avoid prohibited/restricted categories and weight-loss or before/after claims?
4. Does the landing page match the ad and have no pop-ups, forced sign-up or auto-downloads?
5. Is the Pinterest Tag installed with base code on every page and the right events?
6. Is CAPI sending with event_id matching the browser event?
7. Is event quality (EQS) "Good" or at least reviewed?
8. Are images 2:3 (1000x1500) and video 6-15 s with a clear first frame?
9. Is Arabic text inside the central safe area?
10. If catalog: required fields complete, 1000x1500 images, ISO currency code, UTF-8, region availability confirmed?
11. Is the objective right (Consideration, Sales, Leads) and is the optimization event the one you can measure?
12. Is Performance+ bidding chosen for the first run and the budget type understood (125% pacing)?
13. Is targeting free of sensitive categories and under-18?
14. Are UTMs set on destination URLs?
15. Is there a review buffer (24 h) before the launch date?
16. Are alerts set for rejections, catalog errors and billing thresholds?

## 14. Sources
- Ads overview and regional availability: https://help.pinterest.com/en/node/821 ; https://help.pinterest.com/business/article/ads/
- Simplified objectives: https://help.pinterest.com/en-gb/business/article/simplified-objectives ; https://socialmediatoday.com/news/pinterest-renames-campaign-objectives-to-simplify-ad-focus/829869
- Product specs: https://help.pinterest.com/business/article/pinterest-product-specs
- Targeting: https://help.pinterest.com/business/article/targeting-overview
- Budgets: https://help.pinterest.com/business/article/set-up-campaign-budgets
- Bidding: https://help.pinterest.com/en/business/article/set-your-bid
- Billing: https://help.pinterest.com/en/business/article/how-billing-works
- Ad review: https://help.pinterest.com/en/business/article/ad-review
- Advertising guidelines: https://policy.pinterest.com/en/advertising-guidelines
- Tag events: https://help.pinterest.com/en/business/article/add-event-codes
- API for Conversions: https://help.pinterest.com/business/article/the-pinterest-api-for-conversions ; https://developers.pinterest.com/docs/conversions/best/
- Conversion insights: https://help.pinterest.com/business/article/conversion-insights
- Catalog data spec: https://help.pinterest.com/en/business/article/data-source-specification
- API access tiers and limits: https://developers.pinterest.com/docs/key-concepts/access-tiers/ ; https://developers.pinterest.com/docs/reference/ratelimits/
- MENA partner: https://communicateonline.me/news/pinterest-appoints-dms-as-sales-representative-across-mena/

Unverified summary: Egypt shopping/catalog availability, Arabic support, local currency and payment methods, VAT, roles/permissions, agency access steps, Awareness/Video views objective status, Performance+ learning length, minimum budgets/bids for Egypt, frequency controls, automated rules, metric names (outbound click, frequency), Ads Manager default attribution windows, consent/ATT handling, Egypt/MENA benchmarks and audience data.
