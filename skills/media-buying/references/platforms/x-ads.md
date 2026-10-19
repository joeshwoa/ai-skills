# X Ads — rules and playbook
Last verified: 2026-10-19

Notes on sourcing: X's help center (help.x.com) and developer docs (docs.x.com) were readable; the web search tool was exhausted partway through research, so no third-party reporting on platform health, reach or performance was gathered. Anything about audience size, market share or benchmark performance is `unverified` and should not be asserted. The X pages themselves do not always agree (examples flagged below).

## 1. When to use it
- What it is: paid promotion on X (formerly Twitter): promoted posts in timeline, search and profile, video alongside premium publisher content (Amplify), takeovers, follower and app campaigns. Source: https://business.x.com/en/advertising
- Strengths: real-time conversation and news adjacency, keyword and conversation-topic targeting, follower look-alike targeting (reach people like a given account's followers), event and cultural-moment buying, Arabic-language conversation (Arabic is one of 46 targetable languages). Source: https://help.x.com/en/business-and-advertising/geo-gender-and-language-targeting
- Weaknesses: brand-safety sensitivity (content next to posts is less controllable than on most platforms; see section 8), history of shifting advertiser trust, smaller and noisier conversion signal than Meta or Google, USD-only billing for Egypt/KSA/UAE (section 2), weaker local payment support.
- Current state of the platform, as far as sourced: X's advertising page carries a 2026 copyright by ">x< Corp.", markets a new Ads Manager, objectives named sales, leads, website traffic, engagement, video views and app installs, and says there is no stated minimum budget and charges apply only when ads run. It lists Amplify, image and carousel ads (up to six items), collection and shoppable ads, dynamic product ads, boost existing posts, and Mentions Boost (Premium Business). Its performance claims on that page appear as unrendered placeholders and must not be quoted. Source: https://business.x.com/en/advertising . No official monthly active user figure and no CPM/CTR benchmark was found. Third-party estimate from DataReportal (late 2025, X's own ad-tool reach, not active users): Egypt 4.64 million (3.9% of population), Saudi Arabia 15.0 million (43.1%), UAE 2.85 million (25.0%). Sources: https://datareportal.com/reports/digital-2026-egypt , https://datareportal.com/reports/digital-2026-saudi-arabia , https://datareportal.com/reports/digital-2026-united-arab-emirates . Implication: X is far larger in Saudi Arabia than in Egypt; Egypt reach is small relative to Facebook (51.6 million) and TikTok (48.8 million adults 18+) in the same report.
- Best objectives: Website Traffic and Engagements for conversation-driven brands; Video Views / Pre-Roll for campaign moments; Followers for account growth; Reach for launches. Conversion optimization works only with X Pixel or Conversions API events.
- Relevance in Egypt / MENA: Arabic-language news, sports, entertainment and political commentary are native to X, and Gulf audiences are commonly cited as heavy users (`unverified`, no official figure in sources). Typical fits: media and entertainment launches, telecom, banking campaigns, events, sports, government and public-awareness campaigns, tech announcements. Poor fit when brand safety is strict or when the goal is a cash-on-delivery e-commerce purchase at low CPA (judgment). Political content is a restricted policy category (section 8).

## 2. Account, billing and access
- Account hierarchy: Ads account (tied to an X user; created at ads.x.com) > Funding instrument (credit card, credit line, partner-managed; cannot be created through the API) > Campaign > Line item (ad group) > Targeting criteria and Creatives. Source: https://docs.x.com/x-ads-api/campaign-management.md
- Currency: set at account creation from the country and time zone chosen. Egypt, Saudi Arabia and the UAE are all in the list of countries charged in USD; EGP, SAR and AED are not supported. Changing currency requires a support ticket and X creates a new linked account; pause campaigns on the old account first. Advertiser stays responsible for charges on every ads account tied to the handle. Source: https://help.x.com/en/business-and-advertising/ads-currency
- Payment: self-serve advertisers pay by credit and debit card (Visa, Mastercard, American Express; plus Discover, Diners Club US only, JCB in some currencies, China UnionPay). Invoices are visible in the Billing tab only with an authorized credit card on file. Billing thresholds, when charges occur, local Egyptian payment methods, and bank transfer for MENA: `unverified` (not on the billing page). Source: https://help.x.com/en/business-and-advertising/billing-basics
- Egyptian cards: many Egyptian-issued cards are EGP-only or have foreign-currency limits; whether a given card passes is not documented by X (`unverified`). See ../mena-and-egypt-notes.md.
- VAT: X International Company (Ireland) sells to the UAE and the rest of the world (excluding the US, Australia, Québec). Rest of world, including a billing address outside the EU: X adds no VAT, and the advertiser may need to self-assess locally. UAE: personal use is charged UAE VAT; business use may provide a VAT ID; standard UAE VAT applies without a valid ID. Egypt and Saudi Arabia are not covered by that page (fall under "rest of world" by inference only; `unverified`). Tax info: Account Settings > Tax Information. Source: https://help.x.com/en/business-and-advertising/value-added-tax-vat-information
- Agency access: ad account access is tied to authorized users, and the API's GET accounts call returns the ad accounts a user can access. A per-account permission model is linked from the docs but detail was not read here. Source: https://docs.x.com/x-ads-api/getting-started/step-by-step-guide
- Account review: ads accounts and promoted posts are reviewed; a Follower Ads review can pause all campaigns, and disapproval ends the ability to advertise. A ToS violation can suspend the account from X entirely. Source: https://help.x.com/en/business-and-advertising/about-x-ads-approval

## 3. Campaign structure
Hierarchy: Account > Campaign (schedule, daily and total budget, funding instrument) > Line item / ad group (objective, bid, placements, targeting) > Creatives (promoted posts, cards, media). Line items with different objectives cannot share a campaign. Source: https://docs.x.com/x-ads-api/campaign-management.md

Objectives (help center list): Source https://help.x.com/en/business-and-advertising/campaigns-101
| Objective | Optimizes for | Billing |
|---|---|---|
| Reach | impressions to unique people | per impression (CPM) |
| Video Views | video views (completed) | CPM and CPV |
| Pre-Roll Views | views of video before creators' and publishers' videos | CPV |
| App Installs | app clicks | per app click |
| Website Traffic | link clicks and site visits | CPM and CPC |
| Engagements | likes, reposts, replies, profile visits | per engagement (automatic bidding recommended) |
API objective enums: `REACH` (CPM), `FOLLOWERS` (CPF), `ENGAGEMENTS` (CPE), `VIDEO_VIEWS`, `PREROLL_VIEWS` (CPV or cost per 3s / 100% view), `WEBSITE_CLICKS` (CPLC), `APP_INSTALLS` (CPAC or CPI), `APP_ENGAGEMENTS` (CPAC). Target bidding also lists `WEBSITE_CONVERSIONS`. Sales and Leads objectives appear on the marketing page (new Ads Manager) but not in the help list or the API enum list read: the current UI may differ from the API; verify in the UI. `unverified` how the new objectives map to API enums.
- Buying types: auction (self-serve). Reserved/managed buys such as Spotlight and Timeline takeovers and Amplify Sponsorships go through an X sales rep (inferred from product names; details `unverified`).
- Placements (API): `ALL_ON_TWITTER`, `PUBLISHER_NETWORK`, `TWITTER_PROFILE`, `TWITTER_SEARCH`, `TWITTER_TIMELINE`, `SPOTLIGHT`, `TREND`. Rules: `TWITTER_PROFILE` cannot run alone, `TWITTER_SEARCH` requires keyword targeting, `REACH` must include timeline.
- Limits: 200 active campaigns per account (raise to 4,000 via account manager), 100 line items per campaign, 8,000 active line items per account. Line item total budget cannot exceed its campaign's total budget.
- Recommended structures (judgment):
  - Small: one campaign, one objective (Website Traffic or Engagements), 2 line items separating keyword targeting from follower look-alikes (X says do not mix interest and handle targeting in one campaign), 3 to 4 creatives.
  - Medium: separate campaigns per objective and per targeting type (competitor handles, industry media handles, keywords, interests, retargeting from Website Activity audience).
  - Large: add Video Views or Pre-Roll for reach, Conversions-based line items once the pixel has volume, and a managed Amplify or takeover for launches through an X rep.

## 4. Targeting and audiences
- Geo: countries, regions, metros, cities, postal codes (availability varies by country). Selecting a country plus a region inside it reaches the whole country; add only the region to restrict. Uses recent location (IP, GPS). Adding geo after launch can serve worldwide impressions initially; check the History tab. Self-serve targeting is limited to countries where X Ads is available. Source: https://help.x.com/en/business-and-advertising/geo-gender-and-language-targeting
- Language: 46 languages including Arabic; reaches people who understand any selected language. For Egyptian audiences, Arabic language targeting plus Egypt geo is the baseline; whether X distinguishes Arabic dialects: `unverified` (no dialect option documented).
- Gender and age: from profile with inference. Geo, gender, language and age are AND (narrowing); interests and handles are OR (adding).
- Interests: 82 categories. Follower look-alikes: enter @handles; X suggests about 30 handles per campaign; do not combine interest and handle targeting in the same campaign; segment competitors and media in separate campaigns. Source: https://help.x.com/en/business-and-advertising/interest-and-follower-targeting
- Other types referenced: keywords (including negative keywords for exclusion), conversation topics, events, movies and TV, post engager, your followers, device, carrier, new mobile users. API limits per line item: up to 2,000 locations, 100 interests, 1,000 keywords, 100 "similar to followers of" users. Source: https://docs.x.com/x-ads-api/campaign-management.md
- Custom audiences: List (CRM data matched to @handles), Website Activity (X Pixel or Conversions API), App Activity, App Activity Combination. Minimum list size is 100 X users; smaller shows "Audience too small". Only audiences with status Ready can be used. Source: https://help.x.com/en/business-and-advertising/custom-audiences
- Optimized Targeting: pre-selected by default for all campaigns in supported objectives, lets X reach beyond your targeting for better performance; gender, age, location, language, device, OS and exclusions stay enforced. Turn it off when you need strict targeting (for example narrow keyword or handle lists for competitor conquesting). Source: https://help.x.com/en/business-and-advertising/optimized-targeting
- Audience Expansion: look-alike expansion with three levels (Defined, Expanded, Broad); supported for Reach, Engagements, Video views, Pre-roll views, Followers, App re-engagements. For App installs and Website traffic X recommends Automated Targeting instead. Source: https://help.x.com/en/business-and-advertising/audience-expansion
- Restrictions: no targeting by sensitive categories (criminal involvement, health, negative financial status, race or ethnicity, religion, sexual orientation, other gender identities, political affiliation, trade union, genetic or biometric data), including via keywords; no reaching under 13. Source: https://help.x.com/en/business-and-advertising/targeting-of-sensitive-categories
- Arabic notes: keyword targeting must include Arabic spelling variants and dialect spellings; transliterated Arabic (Arabizi) is common on X, so include Latin-letter variants (practitioner observation, not an official rule). Check keyword reach estimates in the UI.

## 5. Bidding, budget and delivery
Source: https://docs.x.com/x-ads-api/campaign-management.md unless noted.
- Bid strategies: automatic bidding (`AUTO`, X recommends it for Engagements), target bidding (`TARGET`; you set a target cost and X aims to keep the average within 20% of it; supported for Website Clicks, Website Conversions, App Installs, App Engagements, Reach), maximum bid (`MAX`, manual cap). Ads API v10+ expresses this as `bid_strategy` plus `goal`.
- Pricing models by objective: CPM for Reach, CPE for Engagements, CPF for Followers, CPV or cost per 3-second / 100% view for video, CPLC (link click) for Website Clicks, CPAC/CPI for apps. Billing event can differ from what you optimize for; read the line item's billing event before comparing costs across objectives.
- Budgets: daily and total budget on campaigns; line item budget cannot exceed campaign total; set bids at or below the campaign budgets or the campaign can end up paused and unservable (docs warning). Amounts in the API are in micros (1,000,000 = 1 unit).
- Minimums: X's marketing page states no minimum budget; the help pages and docs read do not give minimum daily budget or minimum bid. `unverified`; read the minimum in the campaign form.
- Pacing: standard delivery (default) spreads spend evenly across the account-time-zone day; setting `standard_delivery` false (accelerated) spends the daily budget as fast as possible and can exhaust it early.
- Frequency caps: not documented in the pages read (the field is null in examples). `unverified`.
- Learning rules: no official learning-phase threshold in the sources. Practitioner observation, not an official rule: give each line item several days and a few hundred engagements or clicks before changing bids; avoid editing targeting daily. Optimized Targeting and Audience Expansion add model learning; narrow enforced criteria (geo, language, device) can limit reach.
- Spend data lag: spend is generally final within 3 days but billing can be adjusted for up to 14 days; metrics are final after 24 hours except billed spend. Source: https://docs.x.com/x-ads-api/analytics.md . Do not reconcile invoices to the cent against the same-day dashboard.

## 6. Creative specs and requirements
Source for all rows: https://help.x.com/en/business-and-advertising/creative-ad-specifications (re-check before production; specs change).
| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Image ad | 1.91:1, 1:1, 4:5, 2:3, 16:9, 9:16 | Recommended 800x418 or 800x800; supported e.g. 1080x1080, 1440x1800 (4:5), 1920x1080, 1080x1920 | n/a | 5 MB; PNG or JPEG (BMP, TIFF rejected; GIF shows static) | Post copy 280 (257 when the post has a link; links count 23) | App buttons: title comes from the app store, truncated at 200; CTAs Install, Open, Play, Shop, Book, Connect, Order |
| Video ad | same six ratios | recommended 1200x1200 (1:1) or 1920x1080 (16:9) | 15 s or less recommended; up to 2:20; select advertisers up to 10 min | 1 GB max, under 30 MB for best performance; MP4 or MOV | Post copy 280 (257 with link) | H.264, AAC LC, 29.97 or 30 fps (up to 60); 1080p bitrate 6,000 to 10,000 kbps; thumbnail PNG/JPEG up to 5 MB; videos under 60 s loop |
| Vertical video | 9:16 recommended | min 720x1280, max 1080x1920 | under 15 s recommended, up to 2:20 | per video limits | as above | bitrate 5 to 10 Mbps target, 25 Mbps max |
| Carousel | one ratio per carousel | image 800x418 or 800x800; video 800x450 or 800x800 | per slide | per slide | Website card title 70 (aim under 50) | 2 to 6 slides; single-destination or up to 6 web destinations |
| Conversation button | with image or video | n/a | n/a | n/a | Post 280; hashtag 21 incl #; pre-populated post 256; headline 23; thank-you text 23 | Must be paired with media |
| Poll | optional media | n/a | poll 5 min to 7 days | n/a | Post 280; 2 to 4 options of 25 chars | Duration starts at post creation, not promotion |
| Amplify Pre-roll | 1:1 recommended | 1200x1200 (min 600x600); non-1:1 min 640x360 | 15 s or less recommended, 2:20 max | 1 GB; MP4 or MOV | optional URL | |
| Amplify Sponsorship | 16:9 or 1:1 | as pre-roll | 6 s or less recommended | 1 GB | optional URL | Taller-than-wide video cropped to 1:1 |
| Spotlight Takeover | 16:9 | 1280x720 | n/a | image 5 MB; GIF 15 MB | Trend name 20 (required); description 30 | Needs 3 to 6 companion promoted ads |
- Arabic / RTL cautions: X renders post copy in the user's language direction automatically, but mixed Arabic and Latin text, hashtags and @handles can reorder visually, especially with trailing punctuation. Preview on iOS, Android and web. Hashtags with Arabic letters and numbers: test that they link correctly. Put Arabic text in video as burned-in captions with safe margins; most users watch muted (common practice, `unverified` for X). Do not exceed 280 characters counting Arabic letters and emojis as characters; links count 23.

## 7. Tracking and measurement
- X Pixel: JavaScript base code from Events Manager, placed in the page header before `</head>` on all pages (not in an iframe, because that can block first-party cookies); event code at action points. Events types now: Page view, Add to cart, Lead, Added payment info, Purchase, Custom. Base code auto-creates "Site Visit" and "Landing Page View". Do not create several events of the same type (splits signal). Tag managers supported: Google Tag Manager, Ensighten, Tealium iQ. Verify with the X Pixel Helper extension and Events Manager status (Active = activity in last 24 hours). Sources: https://help.x.com/en/business-and-advertising/about-conversion-tracking and https://help.x.com/en/business-and-advertising/conversion-tracking-for-websites
- Conversions API: `POST /{version}/measurement/conversions/:pixel_id` on `ads-api.x.com`. Requires Ads API access and a developer account. Identifiers: X Click ID (`twclid`, not hashed, always include), email (trim then SHA-256, no salt), phone (E.164 then SHA-256), IP and user agent (not hashed, must accompany another identifier). Fields include `conversion_time`, `event_id`, `identifiers`, `value`, `number_items`, `conversion_id`, `contents`. Rate: 60,000 events per account per 15 minutes. Supports offline conversions that start online. Source: https://docs.x.com/x-ads-api/measurement/web-conversions.md
- Deduplication: when using both pixel and API for the same event, send the same `conversion_id` in both. The testing section of the docs was empty when read.
- Attribution windows (post-view, post-engagement) and their defaults: the pages read only say the window can be adjusted when creating an event. `unverified`; read them in Events Manager and note them in every report.
- Cookies: the pixel supports first-party and third-party cookies; first-party improves match. Consent: under the ePrivacy Directive consent is needed for non-essential cookies; you must explain how to opt out of interest-based advertising. Restricted Data Use can be requested for sensitive contexts but may reduce reach and performance. Set `hide_page_location` true if URLs contain sensitive data. Sensitive-category conversion events and audiences are forbidden. Source: https://help.x.com/en/business-and-advertising/policies-for-conversion-tracking-and-custom-audiences
- UTM conventions: `utm_source=x` (or `twitter`, pick one and keep it), `utm_medium=paid-social`, `utm_campaign`, `utm_content=creative id`. Platform auto-tagging into GA4 is not guaranteed; use explicit UTMs. X clicks are counted per link click and can include in-app browser behavior; GA4 sessions will be lower than X clicks (expected gap; no sourced ratio).
- GA4 differences: X reports conversions through its own pixel and windows; GA4 uses its own attribution and does not see lead forms or users who block the tag. Compare trends, not totals, and reconcile with the CRM or the order system.

## 8. Policies and restricted content
- Policy categories (names only were readable): adult content, alcohol, deceptive and fraudulent, drugs and paraphernalia, financial products and services, gambling and games, healthcare and pharmaceuticals, political content, prohibited content for minors, quality policy, tobacco, unacceptable content, weapons. Rules inside each restricted category (and whether crypto sits under financial services): `unverified`; read the specific policy page before advertising any of these. Source: https://business.x.com/en/help/ads-policies/ads-content-policies
- Unacceptable content: derogatory or discriminatory content, inflammatory or profane content, harmful weight-loss or body-image content, exploiting sensitive events, and unauthorized references that imply X affiliation or endorsement. Advertisers are responsible for complying with applicable advertising laws. Source: https://help.x.com/en/business-and-advertising/unacceptable-content
- Review process: promoted posts are marked for review once included in a campaign and cannot run until approved; account-level (Follower Ads) review can pause every campaign. Review timing is not documented. Status and expedited review: support ticket from the Help button in the Ads dashboard. No formal appeal process is described; the ticket is the route. Source: https://help.x.com/en/business-and-advertising/about-x-ads-approval
- Top causes of rejection or ban (judgment from the policy list; no ranking published): deceptive claims, restricted categories without certification, sensitive-category targeting, misuse of X branding, spammy or low-quality posts (Quality policy), account profile that does not match the advertised business.
- Brand safety: content-adjacent controls exist but pages describe them thinly. The Brand Safety page names adjacency controls, keyword targeting, placement controls and sensitivity settings, and says X works with Integral Ad Science and DoubleVerify for independent measurement and post-bid adjacency reporting. The Brand Safety Policy page lists content that Amplify Pre-roll ads should not run beside (adult, hate and extremist, profanity, restricted products, sensitive events, spam, graphic violence). The advertiser-control details are described only by pointer to ads.x.com or the X sales line. Sources: https://help.x.com/en/business-and-advertising/brand-safety and https://help.x.com/en/business-and-advertising/brand-safety-policy . Practical stance: for brand-sensitive clients, require IAS or DoubleVerify reporting, use keyword exclusions, prefer Amplify pre-roll or placements with controls, avoid pure timeline buys with unrestricted adjacency, and put a written approval for the residual risk in the plan.
- Landing page requirements: not detailed in the pages read; general expectations (working page, matches the ad, privacy notice, HTTPS) are `unverified` for X specifically.
- Political content in MENA: treat as restricted; do not run. Gambling and alcohol: prohibited or restricted; no sourced allowance for Egypt, KSA or UAE.

## 9. Optimization playbook
1. First check delivery: is the campaign approved, are the funding instrument and budget valid, is the audience too narrow (geo + language + device enforced), is the bid below auction? If impressions are tiny, widen language or geo and turn on Optimized Targeting before raising bids.
2. Judge on the metric that matches the billing: CPE for Engagements, CPLC / cost per link click for Website Traffic, CPV for Video. Do not compare a CPM-billed campaign with a CPC-billed one directly; convert to cost per result.
3. Wait: do not make major changes in the first 3 days or before the line item has several hundred engagements/clicks (judgment). Spend data is final only after about 3 days and billing can adjust for up to 14.
4. Keep tests clean: one variable per line item (creative, handle set, keyword set). Do not mix interest and handle targeting in the same campaign (X guidance). Segment handles by type (competitors, media, influencers).
5. Cut: pause a line item whose cost per result is 2x the best sibling after it has spent at least 3x the target cost (judgment). Pause a creative with high impressions and very low engagement rate relative to siblings.
6. Fatigue signals: engagement rate falling while frequency per user climbs, rising CPE with stable targeting. X audiences for narrow handle lists are small; rotate creative every 2 to 3 weeks (judgment) and refresh keyword sets weekly during news-driven campaigns.
7. Scale: raise budgets gradually (about 20% steps, judgment) and add adjacent handles and keywords rather than switching to Broad expansion immediately; test Audience Expansion levels (Defined, then Expanded) on a separate line item.
8. Conversion optimization: only after a pixel or Conversions API event has steady volume; first use Website Traffic objective to build a Website Activity audience; verify events in Events Manager; use `conversion_id` dedup when both sources are on.
9. Brand safety audit weekly for sensitive clients: review placement or adjacency reports (IAS or DoubleVerify) and add keyword exclusions.
10. Do not touch during learning: bid strategy, objective, optimized targeting toggle, and creative swaps all at once. Change one thing per 3 to 4 days.
11. Test budget reasoning: with link clicks the likely measure, size each test cell to reach at least about 100 clicks or 100 engagements (judgment), using your own account CPC/CPE from the first 2 days to estimate the budget. No sourced benchmark for Egypt/MENA exists; calibrate in-account.

## 10. Metrics and definitions
Names from the Ads API analytics (https://docs.x.com/x-ads-api/analytics.md):
| Standard term | X name | Notes |
|---|---|---|
| Impressions | `impressions` | |
| Spend | `billed_charge_local_micro` | divide by 1,000,000 for currency units; USD for Egypt/KSA/UAE |
| CPM | derived: billed_charge_local_micro / impressions / 1000 (per the docs' formula) | X's doc formula; check scaling of micros |
| CTR | `clicks` / `impressions`, where `clicks` includes all clicks | Prefer `url_clicks` / impressions for link CTR |
| CPC | spend / `url_clicks` (link click cost) | `clicks` also counts expansions, profile clicks |
| Engagements | `engagements`, `likes`, `retweets` (reposts), `replies`, `follows` | `billed_engagements` for CPE objective |
| Video views | `video_total_views`, `video_3s100pct_views`, `video_6s_views`, `video_15s_views` | |
| Conversions | `conversion_purchases`, `conversion_site_visits`, `conversion_sign_ups` etc. (WEB_CONVERSION group) | Event-based; window per event |
| CPA / ROAS | derived: spend / conversions; value from event `value` | Window and attribution as set in Events Manager |
| CVR | conversions / url_clicks | |
| Frequency | impressions / reach; reach/frequency availability in the API: `unverified` | |
- Segmentation: age, gender, metros, regions, platforms, conversion tags; one dimension per request. Metrics are final after 24 hours (except spend).

## 11. API and automation
- Official API: X Ads API (host `ads-api.x.com`), latest documented version 12 (introduced October 2022; versions 11 and 12 are current with no end-of-life date). Source: https://docs.x.com/x-ads-api/fundamentals/versioning.md
- Access: needs an X developer account and a developer app; basic X API access first, then submit the Ads API Access Form per app. Tiers: Conversion Only (web and mobile conversion endpoints) and Standard (analytics, campaign management, creatives, custom audiences, conversions). Increasing access is done through an X representative (no self-serve process documented). Approval timeline: not documented. After approval regenerate user access tokens. Sources: https://docs.x.com/x-ads-api/getting-started/step-by-step-guide and https://docs.x.com/x-ads-api/getting-started/increasing-access.md
- Authentication: OAuth 1.0a for all Ads API calls. Store keys securely; keys display once; regeneration invalidates old ones. Applicants before July 2023 may be capped at 5 OAuth tokens.
- Rate limits (docs): writes 450 per minute per category; audience endpoints 1,500 per minute; 15-minute windows: sync analytics 250, core entity reads 10,000 (ad account level), other account reads 2,000, targeting criteria 400, conversions 60,000, global reads 5. Headers: `x-rate-limit-*` and `x-account-rate-limit-*`. X does not raise rate limits. Source: https://docs.x.com/x-ads-api/fundamentals/rate-limiting.md
- Analytics: sync endpoint (7-day range, 250 requests per 15 minutes) for optimization loops; async jobs (90 days non-segmented, 45 segmented, 100 concurrent jobs) for backfills. On 429 wait for the reset header; on 503 wait `retry-after`.
- Can automate: campaigns, line items, targeting, creatives (promoted posts, cards, media), custom audiences, lead forms and lead export, DPA catalogs, analytics, conversion events. Cannot automate: creating funding instruments (payment), changing currency, account approval.
- Sandbox exists for testing: https://docs.x.com/x-ads-api/fundamentals/sandbox.md (not read in detail).
- An "X Ads MCP" page is linked from the docs home but was not in the index read; availability and scope: `unverified`.
- Guardrails for automated changes (judgment): keep bids below campaign budgets, never set a total budget below spend, throttle write bursts under 450 per minute, log every change, require human approval for budget increases above 20% or for activating new campaigns above a set spend, and pause automatically if brand-safety keywords appear in monitored contexts.

## 12. Cases
**Situation** Egyptian advertiser's card is declined when adding a funding instrument.
**Do** Remember that the account bills in USD (EGP is not supported), confirm the card allows international USD online payments and is not EGP-only, try another Visa or Mastercard, and check with the issuing bank; if the account was created with the wrong country or time zone, request a new linked account via ads.x.com/help.
**Avoid** Opening several new accounts to bypass declines; each account on the handle stays liable for charges.

**Situation** Campaign for a bank or telecom must not run near controversial posts.
**Do** Use Amplify pre-roll or publisher-controlled placements, apply keyword exclusions, request Integral Ad Science or DoubleVerify measurement, document the residual adjacency risk, and review adjacency reports weekly.
**Avoid** Assuming all adjacency risk is removable on timeline placements; promising a client "100% brand safe".

**Situation** Website Traffic campaign has cheap clicks but no conversions.
**Do** Check that clicks are link clicks (`url_clicks`), landing page speed on mobile, pixel events firing in Events Manager, and event windows. Build a Website Activity audience and test a lower-funnel line item only if events have volume.
**Avoid** Judging by `clicks` (which includes non-link clicks); switching to conversion optimization with a handful of events.

**Situation** Launch of an Arabic product or film needs fast reach in Egypt.
**Do** Combine Reach or Video Views with Arabic language targeting and Egypt geo, add interest and follower look-alikes of relevant Arabic accounts (separate line items), keep creative short (under 15 seconds) with burned-in Arabic captions, and run Optimized Targeting on.
**Avoid** Targeting "Arabic" alone with a wide MENA geo for a product available only in Egypt.

**Situation** Follower look-alike campaign delivers to irrelevant audiences.
**Do** Replace very famous handles (millions of followers who do not share your interest) with niche, business-related ones, keep about 30 handles, split competitors and media into separate campaigns, and turn Optimized Targeting off if it drifts.
**Avoid** Mixing interests and handles in the same campaign; adding hundreds of handles.

**Situation** Ads are paused after an "account review".
**Do** File a support ticket from the Ads dashboard Help button to check status or request expedited review, review profile, bio, recent posts and draft campaign targeting against policy, fix issues, and wait; no appeal process is documented.
**Avoid** Deleting and recreating the same promoted posts repeatedly; launching new campaigns during review.

**Situation** X shows 120 conversions, GA4 shows 60, CRM 40.
**Do** Check the attribution window set in Events Manager, pixel plus API duplicates (use the same `conversion_id`), consent loss in GA4, and the difference between site visits and purchases. Report CRM numbers as truth and X as directional.
**Avoid** Mixing event types that count the same action twice (Purchase created several times).

**Situation** Automation hits 429 on analytics reads during optimization.
**Do** Move bulk pulls to async jobs, use the sync endpoint only for small windows (7 days, up to 20 IDs), read `x-rate-limit-reset`, sync incrementally with `sort_by=updated_at-desc`.
**Avoid** Polling sync analytics every minute across many accounts; asking X to raise limits (they do not raise Ads API limits).

**Situation** Brand wants to promote an event during a trending moment.
**Do** Use event or conversation-topic targeting plus keywords, a promoted post with an image or short video, accelerated delivery only if the window is hours long, and a prepared Arabic copy set with spelling variants.
**Avoid** Running generic pre-approved copy that ignores the conversation; leaving accelerated delivery on for multi-day campaigns (budget exhausts early).

## 13. Pre-launch checklist
1. Is the ads account's country and time zone correct (this fixes currency; Egypt, KSA and UAE bill in USD)?
2. Is a valid funding instrument (international card) on file and are invoices visible?
3. Does the account profile (name, bio, image, recent posts) match the advertised business and policies?
4. Is the objective correct and does it match the billing event you expect (CPM, CPE, CPLC, CPV)?
5. Is language set to Arabic (and English if needed) and geo to the exact countries or regions?
6. Is Optimized Targeting deliberately on or off, and Audience Expansion level chosen?
7. Are interest and handle targeting separated into different campaigns?
8. Are keyword lists reviewed for Arabic spellings, dialect and Latin transliteration, plus negative keywords?
9. Is the budget valid (campaign total above line item totals, bids below budgets) and pacing (standard or accelerated) set on purpose?
10. Do creatives meet the specs (5 MB images, MP4/MOV under 1 GB, text limits, link counts as 23 characters)?
11. Has the Arabic copy been previewed for RTL and hashtag behavior on mobile?
12. Is the X Pixel installed in the header and verified with the Pixel Helper and Events Manager (Active)?
13. If using Conversions API, is `conversion_id` shared with the pixel for dedup and are identifiers hashed correctly?
14. Are attribution windows documented in the plan and the report template?
15. Is a brand-safety plan written (exclusions, IAS or DoubleVerify, escalation route)?
16. Is the content outside restricted categories (political, gambling, alcohol, financial, health) or are authorizations in place?
17. Are UTMs added and named consistently with other platforms?
18. Does a person know how to file an Ads support ticket for review or expedite?

## 14. Sources
- https://business.x.com/en/advertising
- https://help.x.com/en/business-and-advertising (index of help articles)
- https://help.x.com/en/business-and-advertising/campaigns-101
- https://help.x.com/en/business-and-advertising/creative-ad-specifications
- https://help.x.com/en/business-and-advertising/ads-currency
- https://help.x.com/en/business-and-advertising/billing-basics
- https://help.x.com/en/business-and-advertising/value-added-tax-vat-information
- https://help.x.com/en/business-and-advertising/about-conversion-tracking
- https://help.x.com/en/business-and-advertising/conversion-tracking-for-websites
- https://help.x.com/en/business-and-advertising/geo-gender-and-language-targeting
- https://help.x.com/en/business-and-advertising/interest-and-follower-targeting
- https://help.x.com/en/business-and-advertising/custom-audiences
- https://help.x.com/en/business-and-advertising/optimized-targeting
- https://help.x.com/en/business-and-advertising/audience-expansion
- https://help.x.com/en/business-and-advertising/about-x-ads-approval
- https://help.x.com/en/business-and-advertising/unacceptable-content
- https://help.x.com/en/business-and-advertising/targeting-of-sensitive-categories
- https://help.x.com/en/business-and-advertising/policies-for-conversion-tracking-and-custom-audiences
- https://help.x.com/en/business-and-advertising/brand-safety
- https://help.x.com/en/business-and-advertising/brand-safety-policy
- https://business.x.com/en/help/ads-policies/ads-content-policies
- https://docs.x.com/x-ads-api/introduction.md and https://docs.x.com/x-ads-api/llms.txt
- https://docs.x.com/x-ads-api/getting-started/step-by-step-guide
- https://docs.x.com/x-ads-api/getting-started/increasing-access.md
- https://docs.x.com/x-ads-api/campaign-management.md
- https://docs.x.com/x-ads-api/analytics.md
- https://docs.x.com/x-ads-api/measurement/web-conversions.md
- https://docs.x.com/x-ads-api/fundamentals/rate-limiting.md
- https://docs.x.com/x-ads-api/fundamentals/versioning.md
- https://datareportal.com/reports/digital-2026-egypt (and -saudi-arabia, -united-arab-emirates) for third-party reach estimates
