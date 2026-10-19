# LinkedIn Ads — rules and playbook
Last verified: 2026-10-19

Conventions in this file: every number has a source URL nearby or is marked `unverified`. LinkedIn's own help-center pages (linkedin.com/help/...) and the ads policy page block automated fetching, so policy and payment details marked `unverified` must be confirmed in Campaign Manager or on those pages by a human or a browser-capable agent. Where LinkedIn pages disagree, both values are shown.

## 1. When to use it
- Audience: professionals, targeted by job title, function, seniority, company, industry, company size, skills, groups and more. LinkedIn states 1 billion+ members, of which 60 million are in "Middle East & Africa" (regional figure, not per country). Source: https://business.linkedin.com/advertise/ads/audience
- Strengths: B2B targeting precision (job title, company lists, account-based marketing), lead gen with pre-filled forms, thought-leader/employee-post promotion, document (gated PDF) distribution, Message/Conversation ads delivered to inbox.
- Weaknesses: high cost per click and per lead compared with consumer channels (relative statement; no Egypt/MENA benchmark is sourced here), small audiences cap scale, weak for mass-market B2C, e-commerce or cash-on-delivery products.
- Best objectives: Lead Generation (forms), Website Conversions (with Insight Tag or Conversions API), Brand Awareness for account-based reach, Engagement/Video Views for warm-up. Match objective to the funnel stage; see section 3.
- Relevance in Egypt / MENA: useful for B2B SaaS, IT services, recruitment/employer branding, finance, real estate developers selling to executives or investors, training providers, and regional sales into Gulf enterprises. Not a primary channel for mass consumer offers. Third-party reach estimates from DataReportal (late 2025, registered LinkedIn members, not monthly active users): Egypt 15.0 million, Saudi Arabia 12.0 million, UAE 10.0 million (UAE figure equals about 88% of its population, so it overstates real activity; treat all three as upper bounds). Sources: https://datareportal.com/reports/digital-2026-egypt , https://datareportal.com/reports/digital-2026-saudi-arabia , https://datareportal.com/reports/digital-2026-united-arab-emirates . No reliable public per-country benchmark (CPM, CPC, CPL) for Egypt, KSA or UAE was found in official sources; do not quote one. Use the in-platform audience forecast and a small pilot instead.
- Use LinkedIn when the buyer can be identified by role or company and one lead is worth enough to absorb a high CPL. Otherwise prefer Meta or Google.

## 2. Account, billing and access
- Structure: Ad account (nine-digit ID) sits under a LinkedIn Page (company page) and optionally under Business Manager. Roles: account-level (billing admin, account manager, campaign manager, creative manager, viewer) and Page-level roles. Source for role names: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api
- A Company Page is needed to advertise; Thought Leader Ads additionally need the member's consent (section 3).
- Billing currency is chosen at account creation and, per LinkedIn's API docs, cannot be assumed changeable later (unverified). Supported billing currencies include EGP, SAR, AED, USD, EUR, GBP; KWD, QAR and MAD are not in the list. Full 31-currency list: https://learn.microsoft.com/en-us/linkedin/shared/references/v2/ads/supported-currencies
- Currency must match the parent account for all budgets, bids and conversion values. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns
- Payment methods: credit/debit card is the standard route; invoicing for approved advertisers exists. Exact methods available to Egyptian advertisers, billing thresholds and invoicing eligibility: `unverified` (help pages blocked). Confirm in Campaign Manager > Billing.
- Tax: VAT/withholding treatment for Egyptian and Gulf advertisers: `unverified`. Treat LinkedIn invoices as foreign-service purchases and confirm with the company accountant. See ../mena-and-egypt-notes.md.
- Agency access: add the agency by granting account roles to individual users or through Business Manager. Never share a personal login. Prefer the minimum role (campaign manager) over billing admin. Whether a Business Manager partner link is required for a given setup: `unverified`.
- Verification: LinkedIn may ask to verify the Page or the advertiser; requirements and timing: `unverified`.

## 3. Campaign structure
Hierarchy: Ad account > Campaign group (optional; budget and status roll-up) > Campaign (objective, audience, budget, bid, schedule, format) > Ad / creative. Targeting is set at campaign level and applies to every creative in it. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/ads-targeting

Limits per ad account: 5,000 campaigns total, 1,000 active at once, 15 active and 85 inactive creatives per campaign. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns

### Objectives (what each optimizes for)
Source for the mapping: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/campaign-objectives (the source itself warns some cells are inconsistent; verify in the UI).
| Objective | Optimization goals available | Formats (summary) |
|---|---|---|
| Brand Awareness | Reach, Impressions, Sends (messaging) | Image, Video, Event, Carousel, Document, Text/Spotlight/Follower, Conversation |
| Website Visits | Landing page clicks, Impressions, Sends | Image, Carousel, Video, Event, Text/Spotlight, Message, Conversation |
| Engagement | Engagement clicks, Impressions, Sends, Reach (Document) | Image, Carousel, Video, Event, Follower, Conversation, Document |
| Video Views | Video views, Impressions | Video only |
| Lead Generation | Leads, Qualified leads, Clicks, Impressions, Sends | Lead gen form on Image/Carousel/Video, Message, Conversation, Document |
| Website Conversions | Website conversions, Landing page clicks (text), Impressions, Sends | Image, Carousel, Video, Text/Spotlight, Message, Conversation |
| Job Applicants | Landing page clicks, Impressions | Job ads, Image, Spotlight |
| Talent Lead | Talent leads, clicks, impressions | Image, Carousel, Video, Spotlight |
- The "Leads" and "Website conversions" goals exist only for Sponsored Content (single image, carousel, video) formats, not for text ads.
- A campaign optimizing for website conversions needs a conversion rule associated before it can be activated.
- API objective enum names (`BRAND_AWARENESS`, `ENGAGEMENT`, `JOB_APPLICANTS`, `LEAD_GENERATION`, `WEBSITE_CONVERSIONS`, `WEBSITE_VISITS`, `VIDEO_VIEWS`) differ slightly in spelling across the same page; test in the current API version.

### Formats and what they are for
- Sponsored Content (single image, carousel, video, event, document): native feed ads, also eligible for the LinkedIn Audience Network when enabled. API format values: `STANDARD_UPDATE`, `CAROUSEL`, `SINGLE_VIDEO`, `SPONSORED_UPDATE_EVENT`. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/campaign-formats
- Document Ads: PDF/Office file shown in feed, can be gated with a form; good for guides and case studies.
- Message Ads (`SPONSORED_INMAIL`): paid message in the inbox from a named sender, with CTA or lead gen form. Conversation Ads (`SPONSORED_MESSAGE`): branching chat-style message with up to 5 CTAs. Message formats optimize for sends and are billed per send (CPM x 1000, per API docs).
- Thought Leader Ads: promote an organic post from an employee or other member (page lists employees and 1st/2nd/3rd-degree connections; text, image, video, newsletter, article posts). Requires the member's profile, post and CTA. Source: https://business.linkedin.com/advertise/ads/ads-guide. Authorization flow details (member approval steps, expiry): `unverified`.
- Dynamic ads (Spotlight, Follower, Job) and Text Ads: right-rail, desktop only, low volume (spec in section 6).
- Connected TV ads exist (US and Canada, English only per API docs); irrelevant for MENA.

### Recommended structures
- Small (under about USD 1,500 per month; thresholds are this file's judgment, not LinkedIn's): one campaign group, one campaign, objective Lead Generation with a lead gen form or Website Visits, 3 to 4 single-image or document creatives, one audience of 50,000+ members. Do not split audiences; LinkedIn has high cost per click, and splitting starves each campaign.
- Medium: 2 to 3 campaigns by funnel stage: (a) Brand Awareness or Video Views or Engagement to the cold target audience, (b) Lead Generation or Website Conversions to the same audience plus Matched Audience retargeting of engagers, (c) retargeting website visitors. Exclude converted leads and your own employees.
- Large / ABM: separate campaign groups per account tier. Company lists (Matched Audiences) for Tier 1, firmographic targeting for Tier 2, add Thought Leader Ads and Conversation Ads for decision makers. Keep audiences above the optimal size or accept higher costs.
- Rule of thumb for creative: 3 to 5 active creatives per campaign (judgment; the platform allows 15).

## 4. Targeting and audiences
Source for facets: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/ads-targeting
- Facets available: locations, profile locations, industries, company size/category, revenue, growth rate, employers (current, past, all), job titles, job functions, seniorities, skills, schools, fields of study, degrees, interests, member behaviors, age ranges, genders, buyer groups (API 202603+). Member Groups targeting is disabled in the EEA and Switzerland since May 2024.
- Logic: include groups combine with AND between facets and OR within a facet; "Narrow" and "Exclude" refine. Source: https://business.linkedin.com/advertise/ads/audience
- Minimum audience: a campaign needs at least 300 members to run. LinkedIn's guidance: 50,000 or more for single image and text ads, over 15,000 for message ads. Sources: https://business.linkedin.com/advertise/ads/audience and https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/getting-started
- Audience expansion (`audienceExpansionEnabled`, default off in API) broadens targeting to similar members. Treat as off for precise B2B and ABM; on only when the audience is too small to deliver. Not allowed for some formats.
- LinkedIn Audience Network (`offsiteDeliveryEnabled`): extends image, carousel and video ads to third-party apps and sites. Must be off for Lead Gen campaigns per API docs. Can restrict with IAB categories or publisher block files. Default recommendation: off for B2B quality control, test separately (judgment).
- Matched Audiences: contact list upload, company list upload (account-based), website retargeting (Insight Tag), and engagement retargeting (video, lead form, event, page). Minimum list size and match thresholds to become usable: `unverified` (the audience page cites 300 as the campaign minimum; check the Audience page in Campaign Manager for the ready status). Matched Audiences API is private and needs additional approval: https://learn.microsoft.com/en-us/linkedin/marketing/overview
- Predictive/lookalike audience options: availability changes; check Campaign Manager. `unverified`.
- Restrictions: LinkedIn bans discriminatory use of targeting on personal characteristics such as gender, age, race, ethnicity. Source: the required notice at https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/ads-targeting
- Arabic/regional notes:
  - Location targeting is by member profile location or recent location; Egypt, KSA and UAE are separate countries in the geo list. Gulf regions are heavily weighted to expatriate professionals, so check profile language and nationality are not what you actually need; there is no nationality facet.
  - Job title targeting works on standardized titles mostly in English; Arabic job titles are weakly standardized. Use job function plus seniority plus company lists rather than free-text Arabic titles (practitioner observation, not an official rule).
  - Profile language can differ from ad language. Many MENA professionals use English LinkedIn profiles; test English creative first for B2B and add Arabic variants for specific segments. The campaign `locale` (language) must be set; see section 11.
  - Per-country audience sizes are not published here. Read them from the audience forecast in Campaign Manager before building.

## 5. Bidding, budget and delivery
Source for all bid fields below: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns
- Bid strategies:
  - Maximum delivery (automated bidding): spends the budget; goals include max reach, impressions, clicks, conversions, video views, leads, qualified leads.
  - Target cost (TCPC, TCPM, TCPV): keeps average lifetime cost per result near your target.
  - Cost cap (cap cost and maximize clicks, impressions, video views or leads): keeps average cost per result under the cap.
  - Manual bidding: you set the bid; a bid of 0 means no delivery.
- Cost types: CPM, CPC, CPV (video). Message formats are billed per send. Note that for goals like max clicks or max leads, the cost type is CPM even though you optimize for a click or lead (per the objective table).
- Budgets: daily or lifetime (total). Lifetime budget with lifetime pacing is LinkedIn's recommendation. With lifetime pacing LinkedIn can spend up to 150% of the daily average on a single day.
- Minimums: USD 10 per day for any format; lifetime minimum USD 100 for new inactive campaigns (afterward 10 x number of scheduled days); defaults suggest USD 25 for new advertisers or its equivalent in another currency. Minimum bid is not stated; use `adBudgetPricing` for suggested, minimum and maximum bid for your targeting. Sources: https://business.linkedin.com/marketing-solutions/best-practices/ad-tips/maximize-your-budget and https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/getting-started. Equivalent minimum in EGP/SAR/AED: `unverified`; read it in the budget field.
- Frequency: a frequency cap of 3 to 30 impressions per member per 7 days exists for Brand Awareness campaigns only (API docs). Frequency caps for message formats (how often one member can receive a message): `unverified`.
- Learning phase: LinkedIn publishes no formal learning-phase threshold in the sources used. Practitioner observation, not an official rule: allow 2 to 4 weeks and a few hundred clicks or a couple dozen conversions before judging, and do not change targeting or bid mid-flight because the audience is small. Mark any threshold you use as judgment.
- Pacing: LinkedIn spreads spend using a one-week forecast under lifetime pacing. Check at day 3 and day 7 for delivery only; stop judging cost per lead before the week ends.
- Switching bid mode: update `unitCost` and `optimizationTargetType` together; a wrong `unitCost` can overspend. Source: same API page.
- Schedule: `runSchedule.start` is immutable once set.

## 6. Creative specs and requirements
Sources: https://business.linkedin.com/marketing-solutions/success/ads-guide/single-image-ads , https://business.linkedin.com/marketing-solutions/success/ads-guide/video-ads , https://business.linkedin.com/marketing-solutions/success/ads-guide/document-ads , https://business.linkedin.com/marketing-solutions/success/ads-guide/click-to-message-ads , https://business.linkedin.com/advertise/ads/ads-guide , https://business.linkedin.com/advertise/ads/sponsored-content/lead-gen-ads/specs . Re-check before production: specs change.

| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Single image | 1.91:1, 1:1, vertical (1:1.91, 2:3, 4:5; mobile only) | 1.91:1 rec 1200x628 (min 640x360); 1:1 rec 1200x1200 (min 360x360); vertical min 360x640, e.g. 720x900 | n/a | 5 MB; JPG, PNG, GIF | Headline 70; intro text 150 (page value; the video page says 600 max with 150 recommended, so 150 is the visible-before-truncation guideline, verify); ad name 255; description 70 (Audience Network only) | CTA list: View Quote, Learn More, Sign Up, Request Demo; URL max 2,000 chars |
| Video | 16:9, 1:1, 4:5, 9:16 | 360 to 1920 px per side (e.g. 1080x1920 for 9:16) | 3 s to 30 min | 75 KB to 500 MB; MP4 | Headline 70 rec, 200 max; intro 150 rec, 600 max | 30 fps rec; optional captions; thumbnail JPG/PNG up to 2 MB; many CTAs including Register, Attend, Subscribe |
| Carousel | 1:1 recommended | 1080x1080 recommended | 2 to 10 cards | max 10 MB per image | per-card headline: `unverified` | Page: 2 to 10 cards |
| Document | vertical, horizontal or square pages | standard PDF page sizes | recommend under 10 pages; max 300 pages or 1M words | up to 100 MB; PDF, DOC, DOCX, PPT, PPTX | Headline 70; intro 150; ad name 255 | Flatten layered PDFs; keep one page size; hyperlinks must be secure |
| Message ad | n/a | optional banner 300x250 (desktop only, not clickable) | n/a | banner JPG/PNG up to 2 MB | Body 8,000 (message-ads page) vs 1,500 (ads guide); CTA 25 (message page) vs 20 (ads guide); footer 20,000 | Pages disagree; test in Campaign Manager. Sender photo comes from sender profile |
| Conversation ad | n/a | image up to 250x250; banner 300x250 | n/a | image up to 5 MB; banner up to 2 MB | Subject 60; intro and response 8,000 each; up to 5 CTAs; up to 10 emojis per layer | Avoid > < # " % { } [ ] in URLs |
| Lead Gen Form | n/a | n/a | n/a | n/a | Form name 256; headline 60; details 160; CTA 20; confirmation 300; privacy policy text 2,000; max 12 fields; up to 3 custom questions of 100 chars | 3 to 4 fields recommended |
| Spotlight / Follower / Text (right rail) | n/a | logo 100x100; background 300x250 | n/a | n/a | Headline 50 | Desktop only; the guide's text-ad row looks copied from Spotlight (verify) |
| Event ad | 4:1 image from event page | per event page | n/a | n/a | Intro up to 600 | Needs a LinkedIn event |
| Thought Leader | the member's post | the member's post | n/a | n/a | the post's own | Needs member authorization |

- Arabic / RTL cautions: Arabic text in images (not editable text) is fine for single image; check line breaks and punctuation direction in the ad preview, because mixed Arabic and Latin text (brand names, numbers, URLs) can reorder in headlines. Keep headline under the limit with Arabic characters counted as characters, not words. Avoid placing key text in the bottom 20% of video (UI overlay) and the left/right edges of 9:16 (judgment). Arabic documents in Document Ads: embed fonts and export as RTL PDF; test on mobile. Use native Arabic review for copy, not machine translation alone. Whether LinkedIn Arabic profile language targeting exists separately from `locale`: `unverified`.

## 7. Tracking and measurement
- Insight Tag: one JavaScript tag per ad account, placed in the global site header or just above the closing body tag. One tag per account and an account can have only one tag. Roles: `FULL` (admin) and `USE_ONLY`. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking
- Enhanced conversion tracking appends `li_fat_id` to landing URLs on ad clicks. The cookie lasts 30 days after the last ad click on a page with the tag; LinkedIn keeps the id-to-member mapping 365 days, usable for Conversions API matching. Capture `li_fat_id` into a hidden form field. Source: https://learn.microsoft.com/en-us/linkedin/marketing/conversions/enabling-first-party-cookies
- Conversion rules: types include `ADD_TO_CART`, `DOWNLOAD`, `INSTALL`, `KEY_PAGE_VIEW`, `LEAD`, `PURCHASE`, `SIGN_UP`, `OTHER` (the Conversions API page also lists `QUALIFIED_LEAD`, `MARKETING_QUALIFIED_LEAD`, `SALES_QUALIFIED_LEAD`, `SUBMIT_APPLICATION`). Trigger by URL rule or event-specific (CSS/JS) method; the specifics: `unverified`.
- Attribution windows: post-click 1, 7 or 30 days (default 30); view-through 1, 7 or 30 days (default 7) in the conversion-tracking docs. The Conversions API page shows a 90-day post-click example and says 180 and 365 are supported for certain conversion types (text garbled in the source: verify). Sources: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking and https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api
- Attribution counting: `LAST_TOUCH_BY_CAMPAIGN` (default; a conversion can count in each campaign that touched the member, so campaign totals can exceed unique conversions) vs `LAST_TOUCH_BY_CONVERSION` (counted once). Reconcile LinkedIn totals with CRM, not with the sum of campaigns.
- Conversion value: set per rule or sent per event; `DYNAMIC` event value overrides the rule value; currency must match the account.
- Conversions API (server-side): create a rule with `conversionMethod: CONVERSIONS_API`, associate campaigns, stream to `POST /rest/conversionEvents`. Identifiers: SHA-256 hashed email, `li_fat_id`, Acxiom ID, IP address, Google AID, or name fields, plus lead form response URN. Only matched events count. `conversionHappenedAt` must be within the last 90 days. Batches up to 5,000 events; one invalid record fails the batch. Limits 600 requests per minute and 500,000 per day per token. Dedup with the Insight Tag: the docs do not describe it; do not double count (use CAPI for offline/CRM stages, Insight Tag for page events, or test). Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api
- Offline/CRM stages: send `QUALIFIED_LEAD`, `MARKETING_QUALIFIED_LEAD`, `SALES_QUALIFIED_LEAD` events and use the `MAX_QUALIFIED_LEAD` goal (API 202602+) so the algorithm optimizes for lead quality, not form fills.
- Revenue attribution: connect a CRM (Salesforce, Dynamics 365, HubSpot, Sales Navigator CRM) to Business Manager to get ROAS and pipeline metrics; date range must be 30 to 366 days. Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting
- UTM: LinkedIn does not auto-tag for GA4. Use `utm_source=linkedin`, `utm_medium=paid-social` (or `cpc`), `utm_campaign={name}`, `utm_content={creative}`; keep names consistent with other platform files. GA4 will show LinkedIn sessions with UTMs; GA4 uses its own attribution (data-driven or last click), so conversions differ from LinkedIn's last touch within its windows.
- Lead gen forms track leads inside LinkedIn (no click-out). GA4 never sees them; reconcile with CRM.
- Consent/privacy: the Insight Tag sets cookies (including first-party `li_fat_id`); in the EEA/UK and wherever consent law applies, load it only after consent. For Egyptian (Law 151 of 2020) and Saudi (PDPL) data, consult counsel before uploading customer lists: `unverified` as legal advice. See ../mena-and-egypt-notes.md.

## 8. Policies and restricted content
Sources: https://members.linkedin.com/legal/ads-policy (LinkedIn Advertising Policies, mirror of linkedin.com/legal/ads-policy) and https://business.linkedin.com/advertise/ads/best-practices/how-ads-are-reviewed
- Review: new ads and edits to existing ads are reviewed before going live. LinkedIn aims for 24 hours, longer at high volume. Status shows on the Ad tab; rejection emails go to subscribed contacts (only an Account Manager can change that setting). Editing a rejected direct Sponsored Content or Text Ad resubmits it automatically. For a rejected boosted Page post, turn off promotion, publish a compliant new update, and sponsor that. No formal appeal process is described on the review page; contact Help Center support.
- Prohibited (summary): illegal products, discrimination, hateful or sexually suggestive content, fraud or counterfeit, IP infringement, tobacco and vaping, drugs, weapons, adult content, gambling and sweepstakes, fortune telling (unless for amusement), misleading health claims, affiliate advertising, political ads, hacking tools, incomplete ads.
- Restricted (conditions apply): alcohol (certain countries only; not to under-legal-age), dating, contests, fundraising, prescription/OTC drugs, pharmacy, telehealth and medical devices (prior authorization, geographic limits), financial services (lending, investing, trading, insurance, pensions), cryptocurrency, animal products.
- Targeting restrictions: no targeting on sensitive categories (political views, ethnicity, health, religion, criminal record, sexual orientation, union membership, income) and no under-18 targeting for age-restricted categories.
- Landing page rules: display URL domain must match the destination domain; same landing page for all clicks; no pop-ups; users must be able to leave with the Back button; HTTPS for sensitive data; no phishing or malware; cross-site tracking cookies require disclosure and consent.
- Claims: must be factually supported; accurate prices and offers easy to find; no implied endorsement; competitor claims must be accurate; do not use "LinkedIn" to imply affiliation. Professional language, correct grammar, limited emojis and hashtags.
- Top rejection causes to avoid (from the policy list and review page; frequency ranking `unverified`): misleading or unsupported claims, unrealistic health or income claims, domain mismatch between display and destination URL, affiliate-style pages, incomplete ads (missing headline, CTA or URL), restricted category without authorization, copyright or trademark use.
- MENA-specific: ads for gambling, alcohol and dating are prohibited or restricted globally; local laws add further limits. Whether crypto and financial services ads are allowed in Egypt, KSA or UAE specifically: `unverified`; request authorization before building.
- Lead gen forms: need a privacy policy URL and consent text; requirement specifics: `unverified`. Sensitive-category questions in forms are restricted by policy (confirm in the form builder).

## 9. Optimization playbook
First look (daily, first 7 days): delivery and spend pacing, then audience size and CTR. After day 7: cost per result vs target, then lead quality in CRM.
1. If the campaign does not spend: check audience size vs the 300 minimum and 50,000 recommendation, bid below the suggested range (from `adBudgetPricing`), daily budget under minimum for the chosen CPC, ad rejected or pending, schedule start date in the future. Raise the bid or switch to maximum delivery; widen the audience before raising bids on a small audience.
2. Do not judge a campaign before it has spent roughly 3 to 5 times your target cost per lead or collected at least a few dozen clicks per creative (judgment; no official threshold). B2B volumes are low, so decide on directional metrics (CTR, form completion rate) and then confirm on cost per qualified lead.
3. CTR guidance: use your own account history as baseline. LinkedIn does not publish country benchmarks in the sources used here. Within a campaign, pause a creative whose CTR is under about half of the best creative after both have 1,000+ impressions (judgment).
4. Lead gen form completion rate low: shorten fields (3 to 4 recommended), match pre-filled fields to what you need, review the offer headline. If leads are poor, add a custom qualifying question or switch the goal to qualified leads with Conversions API feedback.
5. Fatigue: LinkedIn audiences are small; frequency climbs fast. Watch CTR decay and rising cost per click over 2 to 3 weeks; rotate creative every 3 to 4 weeks for audiences under 50,000 (judgment). Exclude people who already converted and employees.
6. Scale: raise budgets by at most 20% every 3 to 4 days (judgment); broaden audience by adding adjacent job functions or titles, not by removing seniority filters.
7. Test budget: A/B test one variable at a time (offer, creative, CTA, audience). At the USD 10 per day floor, one campaign for 14 to 28 days costs USD 140 to 280 at minimum; at LinkedIn click costs that may yield very few clicks, so size the test so each variant can reach roughly 100 clicks (judgment) or test only one variable at a time with big differences.
8. Do not touch during the first week: audience definition, objective, bid mode, or conversion rules. Do not edit a running creative's text heavily; editing sends it back to review and can reset delivery (the review resubmit is documented; the delivery reset is practitioner observation).
9. Account-based reporting: use `MEMBER_COMPANY` pivots to see which companies engaged; feed engaged accounts into retargeting and to sales.
10. Audience Network: compare separately; cut if lead quality or CTR is much lower than on feed (judgment).
11. Always reconcile: LinkedIn "leads" counts vs CRM leads; sum of campaign conversions vs unique conversions (attribution type).
12. Kill rules (judgment, tune to account): pause a campaign after 3x target CPL with no qualified lead; pause creatives with CTR far below sibling creatives; never pause a whole account on a 2-day dip.

## 10. Metrics and definitions
Metric names in Campaign Manager and the Ad Analytics API (field names from https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting where documented):
| Standard term | LinkedIn name | Notes |
|---|---|---|
| Impressions | `impressions` | |
| Clicks | `clicks` (all clicks including reactions, comments, follows) | Use `landingPageClicks` for clicks to your site |
| CPM | derived: cost / impressions x 1000 | Cost field: `costInLocalCurrency` |
| CTR | `clicks` / `impressions` (shown as CTR) | Prefer landing-page CTR for traffic goals |
| CPC | average CPC; note "cost per click" in UI may be per any click | Check which click is in the denominator |
| Conversions | `externalWebsiteConversions` (website conversions) | Subject to attribution type and windows |
| Leads | lead gen form leads (`oneClickLeads` and form completions in UI; `oneClickLeads` not confirmed in the page read, `unverified`) | |
| CPA / CPL | derived: cost / conversions or leads | |
| CVR | conversions / clicks | Compute yourself |
| ROAS | `returnOnAdSpend` in attributed revenue finder (CRM required) | Otherwise compute from conversion value |
| Frequency | not reported as a standard field here; reach and impressions per member: `approximateMemberReach` | Impressions / reach; `unverified` as a field in all views |
| Reach | `approximateMemberReach` | Unavailable with `MEMBER_` pivots |
| Engagement | `reactions`, `shares`, comments, follows | |
- Freshness: performance metrics near real time; professional demographics delayed 12 to 24 hours; video watch time up to 48 hours; attributed revenue up to 72 hours after first connection. Demographic data is approximate and drops values with fewer than 3 events.

## 11. API and automation
- Official API: LinkedIn Marketing APIs (Advertising API, Conversions API, Lead Sync API, Matched Audiences, Community Management). Versioned (header `Linkedin-Version: yyyymm`); default doc version li-lms-2026-10. Marketing Version 202511 sunsets November 16, 2026: migrate to the current version (docs default li-lms-2026-10). Source: https://learn.microsoft.com/en-us/linkedin/marketing/overview
- Access: all apps start at Development tier (read data for any ad account you administer, create 1 test ad account, edit up to 5 ad accounts). Standard tier (multi-account management, unlimited) requires a support-ticket application and LinkedIn may decline. Apps map ad accounts in the Developer Portal in Development tier. Source: https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access
- Private APIs needing extra approval: Matched Audiences, Audience Insights, Media Planning, Company Intelligence. Lead Sync is a separate program from Advertising API (scope `r_marketing_leadgen_automation`). Advertising API access is a prerequisite for several of these.
- Scopes: `r_ads`, `rw_ads`, `r_ads_reporting`, `rw_conversions`, `r_organization_admin`, and others. These are 3-legged (a member must authorize), so an automation needs a stored refresh token owned by an authorized human account.
- Rate limits: daily per app and per member, reset at midnight UTC; limits by endpoint are not published, see the Developer Portal Analytics tab; 429 on exceed. Conversions API: 600 requests per minute and 500,000 per day per token. Analytics: 45 million metric values per 5 minutes, max 15,000 elements, no pagination. Sources: https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits , https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api , https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting
- Automatable: create and update campaigns, groups, creatives; targeting discovery (`adTargetingFacets`, `audienceCounts`, `adBudgetPricing`); reporting; lead form creation and lead retrieval via webhooks (HTTPS, validated since March 16, 2026; dedupe on response URN plus `occurredAt`); conversion streaming; audience segments (private API).
- Not automatable or not documented: access to Campaign Manager billing setup (real ad accounts must be created in Campaign Manager in Development tier), Thought Leader member authorization (member action), policy appeals.
- Rules for automated changes (this file's guardrails): never change `unitCost` and `optimizationTargetType` separately; never set a bid to 0 (stops delivery); require a human approval for budget changes above 20% or for new campaigns above a set spend; log every change; activation of `MAX_CONVERSION` campaigns requires the association first.
- Campaign limits when automating: 5,000 campaigns per account, 1,000 active, 15 active creatives per campaign.

## 12. Cases
**Situation** Campaign approved but spends almost nothing after 3 days.
**Do** Check audience size (needs 300 minimum; 50,000+ recommended for image ads), compare bid with the suggested range from budget pricing, check daily budget against the minimum, switch to maximum delivery, widen job function or seniority, turn on audience expansion only if still small.
**Avoid** Raising budget on a manual-bid campaign without raising the bid; setting `unitCost` to 0.

**Situation** Lead gen form produces many leads but sales says they are junk.
**Do** Add a qualifying custom question (up to 3), prefer work email, tighten seniority and company-size targeting, send qualified-lead events through the Conversions API, switch the goal to qualified leads (API 202602+), and report on cost per qualified lead.
**Avoid** Optimizing on cost per form fill alone; adding more form fields without testing completion rate.

**Situation** Egyptian company wants to sell B2B software to Gulf enterprises.
**Do** Build company lists for KSA and UAE accounts, target by function and seniority, run English creative first with a short Arabic variant test, use Thought Leader Ads from a founder or sales leader, and route form leads to WhatsApp or email within minutes.
**Avoid** Targeting by Arabic job-title free text, and broad "Middle East" region targeting that mixes markets with different economics.

**Situation** Audience is 12,000 members and frequency is already high at day 10.
**Do** Rotate creative, exclude converters, widen to adjacent titles, consider Matched Audience retargeting of engagers, and accept a higher CPM as the price of a tight audience.
**Avoid** Turning on the Audience Network blindly to "fix" delivery; running 5 campaigns on the same small audience (they compete).

**Situation** LinkedIn shows 40 conversions, GA4 shows 22 and CRM 15.
**Do** Check attribution type (each campaign vs single), windows (post-click 30 and view-through 7 default), consent loss in GA4, form-fill vs qualified, and duplicate events from Insight Tag plus Conversions API. Report CRM-confirmed numbers as the truth.
**Avoid** Summing campaign conversions across campaigns when the rule counts per campaign; mixing LinkedIn and GA4 numbers in one table without labels.

**Situation** Conversion campaign cannot be activated.
**Do** Associate a conversion rule with the campaign first (API requirement for `MAX_CONVERSION`), verify the Insight Tag is active, then activate.
**Avoid** Creating the campaign directly in an active state via API.

**Situation** Ad rejected for "misleading claim" or domain mismatch.
**Do** Match display and destination domains, remove unsupported superlatives, add a source or qualifier, edit the ad (auto resubmits), and wait for the next review cycle.
**Avoid** Re-uploading the same ad repeatedly; running the same ad under another account to bypass review (account-level risk).

**Situation** Budget of USD 300 per month for a first test.
**Do** Use one campaign, a lifetime budget at or above the minimum, a single objective (Website Visits or Lead Generation), 3 creatives, one audience of 50,000+ members, and judge on CTR and landing-page behavior only; expect too little data for CPA decisions.
**Avoid** Splitting into multiple objectives or audiences; judging cost per lead on 2 leads.

**Situation** Promoting an employee's post from a CEO or expert (Thought Leader Ads).
**Do** Get the member's explicit authorization, pick a post that stands alone without a hard sell, add a CTA, measure with engagement and website visits, and run it next to a conversion campaign for retargeting engagers.
**Avoid** Boosting posts that name restricted claims; assuming the member can revoke without you noticing (monitor status).

**Situation** An API automation starts returning 429 and 403 errors.
**Do** Check daily app and member limits in the Developer Portal Analytics tab, reduce `fields`, batch events (5,000 max), back off, and confirm the token's user still has an ad-account role.
**Avoid** Retrying in a tight loop; running one shared token across many clients without per-member planning.

## 13. Pre-launch checklist
1. Is the Company Page set up and the right person assigned a campaign manager role on the ad account?
2. Is the billing currency correct (EGP, SAR, AED, USD or other) and the payment method valid?
3. Is the objective matched to the funnel stage and to a goal that exists for the chosen format?
4. Does the audience forecast show at least 300 members (ideally 50,000+ for image ads, 15,000+ for message ads)?
5. Are audience expansion and Audience Network deliberately set (and off for Lead Gen)?
6. Are existing customers, employees and converted leads excluded?
7. Is the budget at or above the minimum (USD 10 per day or equivalent; lifetime minimum USD 100 for a new campaign)?
8. Is the bid strategy chosen with `unitCost` correct for the cost type?
9. Is the Insight Tag installed, verified and enhanced conversion tracking on?
10. Are conversion rules created, set to the right type and windows, and associated with the campaigns?
11. Is a Conversions API feed connected for CRM or offline stages, with no double counting?
12. Do creatives meet current specs (ratio, size, text limits) and pass the ad preview in Arabic and English?
13. Do headline, claims and offer pass the ad policy (no unsupported claims, domain match, no restricted category)?
14. Do landing pages load fast on mobile, match the ad, have a privacy policy and consent where needed?
15. Are UTMs added and named consistently?
16. Is the lead gen form tested (test lead) and routed to CRM or WhatsApp with an owner and a response-time target?
17. Is a reporting cadence and a decision rule (pause, scale) written down before launch?
18. Is the start date and run schedule correct (start date cannot be changed later)?

## 14. Sources
- https://business.linkedin.com/advertise/ads/audience
- https://business.linkedin.com/marketing-solutions/best-practices/ad-tips/maximize-your-budget
- https://business.linkedin.com/advertise/ads/ads-guide
- https://business.linkedin.com/marketing-solutions/success/ads-guide/single-image-ads
- https://business.linkedin.com/marketing-solutions/success/ads-guide/video-ads
- https://business.linkedin.com/marketing-solutions/success/ads-guide/document-ads
- https://business.linkedin.com/marketing-solutions/success/ads-guide/message-ads
- https://business.linkedin.com/marketing-solutions/success/ads-guide/click-to-message-ads
- https://business.linkedin.com/advertise/ads/sponsored-content/lead-gen-ads/specs
- https://business.linkedin.com/advertise/ads/best-practices/how-ads-are-reviewed
- https://members.linkedin.com/legal/ads-policy
- https://learn.microsoft.com/en-us/linkedin/marketing/overview
- https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/getting-started
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/campaign-objectives
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/campaign-formats
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/ads-targeting
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking
- https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting
- https://learn.microsoft.com/en-us/linkedin/marketing/conversions/enabling-first-party-cookies
- https://learn.microsoft.com/en-us/linkedin/marketing/lead-sync/leadsync
- https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits
- https://learn.microsoft.com/en-us/linkedin/shared/references/v2/ads/supported-currencies
- https://datareportal.com/reports/digital-2026-egypt (and -saudi-arabia, -united-arab-emirates) for third-party reach estimates
- Not fetchable (blocked to automated tools; confirm manually): https://www.linkedin.com/help/lms/answer/a424570 (objectives), https://www.linkedin.com/help/lms/answer/a417960 (currencies), https://www.linkedin.com/help/lms/answer/a421456 (payments), https://www.linkedin.com/help/lms/answer/a493903 (document specs)
