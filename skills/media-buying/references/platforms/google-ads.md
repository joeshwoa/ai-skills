# Google Ads — rules and playbook
Last verified: 2026-10-19

Scope: Search, Performance Max (PMax), Shopping/Merchant Center, Demand Gen, Display, App campaigns (high level). YouTube video buying has its own file (`youtube-ads.md`). Facts come from Google help pages fetched on 2026-10-19 (URLs in section 14). Items marked `unverified` were not confirmed in an official source in this pass. Items marked "practitioner observation" are lore, not official rules.

## 1. When to use it
- Google Search captures existing intent (the user typed the need). Use it first when people already search for the product/service, for local lead-gen, and for any business that can measure a conversion on a website or call.
- Strengths: intent-based demand, keyword control, strong measurement/bidding stack (Smart Bidding), one account reaches Search, YouTube, Display, Gmail, Discover and Maps (via PMax/Demand Gen).
- Weaknesses: low-search-volume niches cannot scale; automation (PMax, broad match, AI-powered Search) reduces transparency; Smart Bidding needs conversion data (section 5); policies and suspensions are strict (section 8).
- Best objectives by situation:
  - Known demand, any budget: Search with exact/phrase + broad match under Smart Bidding.
  - E-commerce with a clean product feed: Shopping or PMax with feed.
  - Leads with a site/WhatsApp/call flow: Search first; PMax only after conversion tracking is proven.
  - Awareness/consideration, creative-led: Demand Gen (YouTube, Discover, Gmail, Display inventory).
  - Apps: App campaigns (installs / engagement / pre-registration).
- Display: Google is retiring standalone Display campaigns in favor of Demand Gen. Eligible advertisers started seeing a migration tool in June 2026; creation of new standalone Display campaigns is to stop later (no date); existing ones stay editable until migrated; migration runs into 2027 (reported by Search Engine Journal, citing a Google blog; Demand Gen help page confirms "June 2026" voluntary migration). Check the account for the current state before planning Display.
- Egypt / MENA relevance:
  - Merchant Center lists Egypt (currency EGP), Saudi Arabia (SAR) and UAE (AED) as supported countries. The Shopping tab is marked available in Saudi Arabia and UAE but NOT in Egypt (Merchant Center supported languages and currencies page). Shopping ads/free listings can still be configured for Egypt; do not assume a Shopping-tab surface there.
  - No reliable, sourced Egypt/MENA benchmarks for CPC, CPM, CVR or CPA were found. Do not quote any; build the baseline from the account's own first 2-4 weeks.
  - Search-market size and Arabic query volume for a given niche: `unverified`; check Keyword Planner in the account.

## 2. Account, billing and access
- Structure: manager account (MCC) > Google Ads accounts (customer IDs) > campaigns. Tags: Google tag and Google Tag Manager containers are separate from the ad account. Merchant Center is a separate account linked to Google Ads. Google Analytics 4 property can be linked.
- Access: Admin is needed to set up monthly invoicing or apply for a credit line. Google advises at least two admins so tag access is not lost with one person (help page 6372672). Access-level definitions (Admin / Standard / Read only / Email only): `unverified` in this pass; confirm in "About access levels in your Google Ads account".
- Agency access: invite via Admin > Access and security, or link the account to a manager account (steps are on a separate Google page; not fetched). Prefer manager-account link over sharing a personal login. Never ask for or store a client's Google password.
- Advertiser verification: Google is rolling it out gradually; "all advertisers will eventually" need it. Early triggers: suspicious behavior, financial services, brand-related queries, appeals. Tasks vary (organization questions, possibly a document). Status can take up to 5 business days. If not completed: some ads may be restricted and the account may be paused. Re-verification can be triggered by payment-profile, billing-address or legal-name changes. False info can cause suspension. Sources: advertiser verification pages (section 14). Egypt-specific document list: `unverified`.
- Payment setup types (Google payments page): postpay (automatic; charged after ads run, on a threshold or the first day of the month, whichever comes first), prepay (manual; ads stop when credit is used), monthly invoicing (credit line; limited to eligible businesses; requirements not stated). Prepaid cards are not accepted for postpay. Available options depend on billing country and currency.
- Prepay is not offered in a list of countries that includes Saudi Arabia, UAE, Qatar and Israel (examples on the manual-payments page). Whether Egypt is on that list: `unverified` (the page shows "e.g." names and the full list was not read). Check Billing > Payment settings in the account.
- Egypt VAT (official, Google Ads tax page): since 2024-07-01, Google Ads accounts with an Egypt business address are charged 14% VAT unless the advertiser provides both a Tax Registration Number (TRN) and a Unique Identification Number (UIN). Enter them in Billing > Settings > Payer details > "Egypt tax info" (or in Google Payments Center). The account is served by Google Ireland Ltd. Google does not give tax advice; send tax questions to an accountant.
- Currency: EGP as an Ads account billing currency for Egypt advertisers: `unverified` (the Egypt EGP announcements found concern AdSense/YouTube creator payouts, not advertiser billing). Account currency is fixed at creation; confirm before launching.
- Local cards: a third-party vendor page (Figo, commercial, treat with caution) claims Egyptian bank cards are often declined for foreign-currency reasons and that failed charges pause campaigns. Practitioner observation, not an official rule. Operational rule: keep a second valid payment method, and alert on billing failures.
- Billing threshold: starts small and rises with payment history; exact amount not documented on the help page.

## 3. Campaign structure
- Hierarchy: Campaign (type, budget, bid strategy, locations, languages, networks) > Ad group (Search: keywords + RSAs; Demand Gen: audiences/placements) > Ads/assets. PMax uses Asset groups instead of ad groups.
- Campaign types and what they optimize for:
  - Search: queries matching keywords (plus broad-match/AI-powered expansion). Optimizes toward the chosen Smart Bidding goal (clicks, conversions, conversion value).
  - Performance Max: all Google inventory (Search, YouTube, Display, Discover, Gmail, Maps) from one campaign; goals Sales, Leads, Website traffic, Local store visits; optimizes conversions or conversion value. Controls: brand exclusions, negative keywords, search themes, final URL expansion on/off, placement exclusions, content suitability. Search campaigns with exact-match keywords take priority over PMax when a query matches (PMax help page).
  - Shopping: product listings from the Merchant Center feed. Optimizes via Target ROAS, Maximize conversion value, etc.
  - Demand Gen: YouTube (incl. Shorts), Discover, Gmail, Google Display Network, Maps; formats image, video, carousel (2-10 cards), product feed; bidding Maximize Clicks, Maximize Conversions, Target CPA, value-based. Billing varies by surface (YouTube CPM, Gmail teaser click, Discover image CPC, GDN CPM).
  - Display (legacy, being merged into Demand Gen): see section 1.
  - App campaigns: installs, engagement (re-engage users), pre-registration. Inventory: Search, Google Play, YouTube, GDN, Discover. App must be on Google Play or Apple App Store and a payment method must be on file. Target ROAS for app needs the Google Analytics for Firebase SDK.
  - Video: see `youtube-ads.md`.
- Buying types: auction is default. Reservation (fixed CPM) exists for YouTube (Masthead, Premier reach) through a Google rep; not for Search.
- AI-powered Search / AI Max for Search: features exist (see the "Improve with AI-powered Search" page) but their details were `unverified` in this pass. Treat as opt-in and check each setting (text customization, final URL expansion) before enabling.
- Recommended structures (decision rules, not Google rules):
  - Small budget (under ~USD 20-30/day, reasoning: Target CPA needs spend of roughly 10x tCPA per day, see section 5): 1 Search campaign, 1-3 tight ad groups (exact + phrase), Maximize Conversions or Maximize Clicks with a cap until 15-30 conversions exist; no PMax, no Display. Practitioner heuristic.
  - Medium: separate Search campaigns by intent (brand, non-brand core, competitor), brand isolated so its cheap conversions do not hide non-brand performance; add PMax or Shopping if a feed exists; add Demand Gen for retargeting/prospecting with video.
  - Large: segment by margin/product group/country; value-based bidding (tROAS) with proper conversion values; use experiments (campaign drafts/experiments) before structural changes; central negative keyword lists at account level.

## 4. Targeting and audiences
- Search:
  - Keywords with match types (below), locations, languages, devices, ad schedule, audience segments in observation or targeting mode.
  - Match types (Google help 7478529):
    - Broad: no symbols; default. Ads can show for related searches, also considering landing page, recent search activity and other keywords in the ad group. Google says Smart Bidding is "critical" with broad match.
    - Phrase: "keyword" in quotes. Matches the meaning, including implied meaning and more specific versions.
    - Exact: [keyword] in brackets. Same meaning or intent; most control, least reach.
  - Negative keywords (help 2453972):
    - Negative broad: blocks if the query contains all negative terms in any order.
    - Negative phrase: blocks if terms appear in the same order, extra words allowed.
    - Negative exact: blocks only the exact terms with no extra words.
    - Negatives do NOT match close variants, plurals or synonyms. Add singular/plural/spelling variants yourself. Case and misspellings are handled.
    - Account-level negative lists apply to eligible Search and Shopping inventory.
    - An ad may still show if the negative appears after the 16th word of a long query.
    - Display and Video: up to 1,000 negative keywords at account level. Search negative limits: `unverified`.
  - Arabic note (inference from the no-close-variants rule): Arabic has many spelling variants (hamza forms, ta marbuta vs ha, Egyptian dialect vs Modern Standard Arabic, Arabizi/Latin spellings). Add each variant as its own negative and review the search terms report in Arabic and Latin script weekly.
- Shopping/PMax/Demand Gen: audience signals (PMax; speeds learning, not a hard target), Customer Match (first-party lists), lookalike segments (Demand Gen: built from purchasers, site visitors, YouTube viewers), custom segments (Demand Gen: 10-15 keywords suggested), in-market and affinity segments.
- Remarketing: audience lists from the Google tag / GA4 / app / YouTube interactions. Customer Match via API is restricted for new adopters since 2026-04-01; use the Data Manager API for new integrations (API quotas page).
- Contextual/placements: YouTube channels/videos, GDN sites/apps, topics, keywords (see `youtube-ads.md` for inventory types).
- Restrictions:
  - Sensitive categories (gambling, alcohol, political, etc.) in Demand Gen are mostly limited to YouTube and must use predefined Google audiences; alcohol advertisers cannot use product feeds.
  - Personalized advertising restrictions (health, financial hardship, etc.): Google's personalized advertising policy was not fetched; `unverified` for exact lists. Assume remarketing is blocked for sensitive health/financial categories and verify in Policy Manager.
  - Location targeting is an intersection with other targeting (video targeting page).
- Regional notes (Egypt/MENA):
  - Target by location (country, governorate, radius) AND set language(s). Language targeting matches the user's Google interface language, not the ad language. For Arabic and English audiences in Egypt, usually target both Arabic and English. Practitioner observation; the exact rule on language targeting was not fetched.
  - Use "Presence" (people in the location) rather than "Presence or interest" for local lead-gen so out-of-country traffic does not consume budget. Option name per Google UI; the setting is documented in Google location-targeting help (not fetched).
  - Call and location assets need verified, active, local numbers related to the advertiser (destination requirements policy).

## 5. Bidding, budget and delivery
- Smart Bidding strategies (help 10970825): Maximize conversions, Target CPA, Maximize conversion value, Target ROAS. Manual CPC and enhanced CPC exist but have no learning period in the Smart Bidding sense.
- Data requirements (official numbers; confirm before use because Google changes them):
  - Target CPA: no history required to start. Evaluate with 30 days of data and at least 30 conversions. Budget comfortable with spend up to 2x the daily budget. (help 6268632)
  - Target ROAS: Search and Shopping at least 15 conversions in the past 30 days; Display 15 conversions with values in 30 days across campaigns; App 10 conversions per day or 300 in 30 days; Demand Gen 50 conversions in 35 days (10 in the last 7) within the campaign or 100 in 35 days across Demand Gen campaigns, values above 0. Report conversion values for 4 weeks or 1-2 conversion cycles (the longer) before setting tROAS. (help 6268637)
  - Demand Gen FAQ: start with Maximize Conversions; move to tCPA/tROAS after at least 50 conversions; start tROAS about 20% below the last 30 days' ROAS; adjust in steps of about 10%. For Target CPA set the daily budget at least 10 times the target CPA. (help 14509385, 13695777)
  - Data-driven attribution: recommended at least 200 conversions and 2,000 ad interactions in 30 days for the most accurate results; any conversion action can use it regardless of volume. (help 7003150)
- 2026-08-17 change (official, help 17061251): budget-limited campaigns on Target CPA or Target ROAS now deliver closer to the entered target. A campaign with a $10 tCPA that was achieving $5 will move toward $10. Scope: Search, Shopping, PMax, Demand Gen, Travel. App, Video reach and Video view are excluded. Google will not change targets or budgets for you. Rule: audit every tCPA/tROAS campaign that is budget-limited; set the target to the outcome you really want (or switch to Maximize Conversions / Conversion Value if you want volume, accepting variable CPA).
- Budgets (help 1704424): daily budget is an average; any day can spend up to 2x; monthly charge cannot exceed daily budget x 30.4. Overdelivery above the monthly cap is credited.
- Ad-schedule pacing (help 16913225, effective 2026-06-01): for schedules that switch off whole days of the week, pacing now aims at 30.4 x daily budget, so lower the daily budget to hit a monthly total (example in the page: $2,000 over 20 days needs about $66/day instead of $100). Hour-based schedules unaffected. Local Services, Hotel Commission, Smart campaigns and App excluded.
- Minimum budget: no official minimum for Search. PMax help shows Low/Medium/High suggestions in the budget panel; Low is "the minimum recommended" for that campaign. Demand Gen Max Clicks has no minimum budget.
- Learning:
  - Bid strategy shows "Learning" after: new/reactivated strategy, setting change, composition change (campaigns/ad groups/keywords added or removed), ad-group target change (Shopping). Typically 1-2 conversion cycles to calibrate; longer with few conversions or long conversion cycles (help 13020501).
  - Help 10970825 says changing a CPA/ROAS target does not trigger the learning status or reset what was learned. Help 13020501 lists "setting change" as a trigger. Treat them as conflicting; keep target changes small and infrequent.
  - Help 12563349: wait about 50 conversion events before further bidding changes; ads review takes at least 24 hours. Campaign type scope of this article is unclear.
  - After a target change evaluate after 1-2 conversion cycles; after other changes allow at least one cycle.
  - Do not reset learning by: swapping bid strategy repeatedly, adding/removing many keywords or whole ad groups, changing the conversion goal set, editing budgets in big jumps, pausing and reactivating.
- Frequency: not controllable in Demand Gen (FAQ); use Video reach target frequency on YouTube (see `youtube-ads.md`).

## 6. Creative specs and requirements
Specs change often; re-check the linked pages before bulk uploads.

| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Search RSA (text) | n/a | n/a | n/a | n/a | Headline 30 chars (3 to 15); description 90 chars (2 to 4); path fields 15 chars each | At least 2 RSAs per ad group recommended; pinning to H1/H2/D1 always shows, H3/D2 not guaranteed; double-width chars (CJK) count 2. Source: help 7684791 |
| PMax text | n/a | n/a | n/a | n/a | Headline 30 (3 to 15, one at most 15 chars); long headline 90 (1 to 5); description 90 (2 to 5); business name 25 | CTA required; final URL required; Source: help 14528220, API asset requirements |
| PMax image landscape | 1.91:1 | rec 1200x628, min 600x314 | n/a | 5120 KB | n/a | 1 to 20; jpg/png (API also lists GIF) |
| PMax image square | 1:1 | rec 1200x1200, min 300x300 | n/a | 5120 KB | n/a | 1 to 20 |
| PMax image portrait | 4:5 | rec 960x1200, min 480x600 | n/a | 5120 KB | n/a | optional, up to 20 |
| PMax logos | 1:1 (required) and 4:1 (optional) | 1200x1200 (min 128x128); 1200x300 (min 512x128) | n/a | 5120 KB | n/a | Up to 5 square logos |
| PMax video | 16:9, 9:16, 1:1 | n/a (no resolution limit listed) | 10 to 60 s (help page); API says at least 10 s | n/a | n/a | Up to 15; if none, Google may auto-generate. Wait 2 to 3 weeks before replacing low assets |
| Demand Gen image ad | 1:1, 1.91:1, 4:5, 9:16 | min 300x300 / 600x314 / 480x600 / 600x1067; rec 1200x1200 / 1200x628 / 960x1200 / 1080x1920 | n/a | 5 MB | Headline 40 chars (up to 5, min 3 recommended); description 90 (up to 5); business name 25 | Up to 20 images; logo 1:1 min 144x144 (spec table says 128x128), 150 KB max |
| Demand Gen carousel | consistent across cards | as image | n/a | as image | Ad-level headline 40, description 40; card headline 40 | 2 to 10 cards; not available with a Merchant Center feed |
| Demand Gen video | 16:9, 1:1, 4:5, 9:16 | rec 1920x1080, 1080x1080, 1080x1350, 1080x1920 | min 5 s; under 10 s cannot serve on YouTube in-stream | 256 GB | as image ad | Format MPG (MPEG-2/4). Source: help 13704860 |
| Display uploaded ads | sizes: 300x250, 336x280, 728x90, 970x90, 160x600, 300x600, 320x50 | as listed | n/a | 150 KB | n/a | jpg, png, non-animated gif |
| Shopping product (Merchant Center) | n/a | image min 500x500 (enforced from 2027-01-31) | n/a | no limit shown | Title 150 chars; description 5,000 chars | See below |

- Merchant Center feed rules (help 7052112): required id (50 chars), title, description, link, image_link, availability, price; brand required for new products (except movies/books/music); MPN only if no GTIN; GTIN must pass GS1 checksum, never invent one; brand field must be empty if no brand (no "N/A"/"Generic"); no promo text, all caps or watermarks in titles/images; keep AI-generation metadata (IPTC DigitalSourceType) on AI images; up to 10 additional images.
- Arabic/RTL creative cautions:
  - Text in image assets: PMax/Demand Gen crop and recombine images; keep Arabic text inside a central safe area and test every ratio (1:1, 4:5, 1.91:1, 9:16).
  - Mixed Arabic + Latin + digits can reorder in text assets; preview every combination in the ad preview tool. Practitioner observation.
  - Do not paste prices or phone numbers as images only; put them in text/assets so they can be reviewed.
  - Character limits count characters; the "double-width" rule applies to Korean, Japanese, Chinese only (help 7684791), so Arabic counts 1 per character, but Arabic words often need more characters than English; budget the 30-char headlines accordingly.
  - Use Egyptian vs Modern Standard Arabic consistently within an ad group; review which one matches queries in the search terms report. Practitioner observation.
- Generative AI / AI labels: ads with AI-generated or AI-edited assets may need an AI label under EU, Indian and New York rules (video specs page).

## 7. Tracking and measurement
- Tag: Google tag (gtag.js) or Google Tag Manager. Set a primary conversion action per business goal (purchase, lead, call) and secondary actions for observation. Primary vs secondary action semantics: `unverified` in this pass; check Goals > Conversions > Summary.
- Enhanced conversions (help 9888656, 15712870): send hashed first-party data (email, name, address, phone) from the tag; normalize (trim, lowercase, E.164 phone) then SHA-256 hex. Setup via GTM, the Google tag directly (not in a third-party iFrame), or the Google Ads API; Chrome extension "Enhanced Conversions Assist" helps validate. From April 2026 enhanced conversions for web and for leads are one on/off setting. Matching uses signed-in Google accounts that engaged with ads.
- Offline / CRM conversions: import by click ID (gclid) or enhanced conversions for leads. For new integrations Google says to use the Data Manager API (UploadClickConversions restricted for new adopters from 2026-06-15). Up to 2,000 conversions per request.
- Conversion windows (help 3123169): defaults click 30 days, engaged-view 3 days, view-through 1 day. Range 1 to 90 days overall. Changes apply only to future conversions. Smart Bidding optimizes for the window you choose. Google recommends windows of at least 7 days. Store visits with Smart Bidding: 7-day click window recommended.
- Attribution: data-driven is the default for most conversion actions (help 7003150). Whether a report column dates a conversion by interaction day or conversion day: `unverified` in this pass; check column definitions before comparing periods.
- Consent mode v2 (help 13695607; developers.google.com consent mode):
  - Parameters: ad_storage, ad_user_data, ad_personalization, analytics_storage (plus functionality, personalization, security storage).
  - Required for EEA traffic if you use personalized advertising / remarketing; send consent signals through a Google-certified CMP or your own implementation. Advertisers not using personalized advertising need no action (per the help page).
  - Basic mode: tags are blocked until the user interacts with the banner; no data is sent before; declined means no data and generic modeling. Advanced mode: tags load, send cookieless pings while denied, enabling advertiser-specific modeling. Denying ad_user_data blocks personal-data use incl. enhanced conversions.
  - Modeling needs a data threshold; losing consent data means lower observed conversions.
  - Egypt/MENA: GDPR consent mode matters only for EEA/UK visitors; local data-protection law (Egypt Law 151/2020) compliance and its application to ad tags: `unverified`; ask the client's legal counsel.
- iOS ATT: affects app campaigns on iOS (SKAdNetwork/MMP measurement); not researched in this pass; `unverified`.
- UTM conventions: autotagging (gclid) is on by default; add UTM only for non-Google reporting and never remove autotagging. Use `utm_source=google&utm_medium=cpc&utm_campaign={campaignid}` style via ValueTrack. Convention, not an official rule.
- Google Ads vs GA4 numbers differ by design: attribution model, window, counting day, imported-vs-native conversions, consent modeling, cross-device. Official page not fetched; `unverified`. Rule: report platform-native numbers for bidding decisions and GA4 for cross-channel; never mix them in one ROAS figure.
- Conversion diagnostics tab in Google Ads shows tag and consent status (help 13695607).

## 8. Policies and restricted content
- Policy areas (help 6316): Prohibited content (e.g. counterfeit goods, dangerous goods, sexually explicit content), Prohibited practices (e.g. misrepresentation), Restricted content (e.g. alcohol, gambling, healthcare), Editorial and technical standards. Full lists are on the policy pages; this file does not reproduce them.
- Review: ads are reviewed after creation/edit; allow at least 24 hours (help 12563349). Saving an edited ad resubmits it. Unreliable-claims edits re-review typically 24-48 hours.
- Top causes of disapproval / suspension (official):
  - Misrepresentation / unacceptable business practices: hiding or misrepresenting business info, implying endorsement by a brand/public figure, selling what you cannot deliver (including lacking required licenses/qualifications), impersonation. Violations are treated as egregious: account suspended on detection WITHOUT warning, and the advertiser may not advertise again; reinstatement only in "compelling circumstances" (help 6020955, 14599564, 14092889).
  - Destination problems: page returns HTTP errors to AdsBot, not crawlable or not accessible in the target location, display URL domain differs from final URL, redirects to other domains, mostly-ads or copied pages, forced downloads. Policy violations here do not cause immediate suspension; a warning is issued at least 7 days before any suspension (help 6368661).
  - Unreliable claims: improbable results as typical, miracle cures, unrealistic weight loss, "get rich quick", guaranteed or exaggerated returns, risk-free investments. Guaranteed results need a clear refund policy; testimonials with specific results need a "results not guaranteed" disclaimer. Warning of at least 7 days before suspension. Before/after claims: not addressed on this page (`unverified` for Google's own before/after rule; Pinterest bans them, see `pinterest-ads.md`). (help 15936857)
  - Payment/billing failures and unverified accounts: ads or accounts paused until fixed (section 2).
  - Circumventing systems (cloaking, creating new accounts after suspension): the policy page was not fetched in this pass; `unverified`. Verification page states false info breaches "Circumventing systems" and can lead to suspension.
- Restricted verticals (healthcare, financial services, gambling, alcohol, political, etc.): each has a separate policy, often with country-specific allowances, certification or verification. The exact Egypt/Saudi/UAE rules per vertical were NOT retrieved; treat every regulated vertical as `unverified` for MENA and check Policy Manager and the vertical policy page before building the campaign. Financial-services advertiser verification applies in listed countries; whether Egypt is included: `unverified`.
- Landing page requirements: working on common browsers/devices, same domain as display URL, original content, easy navigation, no abusive experience, privacy/contact basics are good practice. Phone numbers in call/location assets must be verified, active, local and related to the advertiser; fax, premium, vanity and virtual numbers are disallowed.
- Appeal process (help 9338593):
  1. Open the disapproved ad > fix and Save (auto-resubmits), or point to a compliant landing page.
  2. If you believe it is wrong: Policy manager > Appeal (choose a reason). Appeal in batches by ad group/campaign.
  3. Check again after 24 hours; wait at least 24 hours between appeals on the same ad; max 3 unsuccessful appeals per ad, then contact support. Do not resubmit identical appeals; make a small edit to ad text or final URL to trigger a re-crawl.
  4. From 2026-07-21, in-account appeals are not available for decisions older than 6 months; go through support.
  5. Account suspension appeals use Google's appeal form; explain honestly; there is no warning for egregious violations.
- While rejected: do not clone the ad under a new name repeatedly (can look like circumvention; `unverified` as an exact rule but widely reported); keep other ads running; fix the root cause (claim, page, feed) rather than rewording.

## 9. Optimization playbook
Decision rules for an agent. Numbers marked "heuristic" are practitioner rules of thumb, not Google rules.
1. First look (daily, 2 minutes): billing status, policy status (Policy manager), budget limited? (Status column), conversion tracking health (conversion diagnostics), then spend vs plan.
2. Do not judge a campaign before one full conversion cycle (click to conversion lag from the bid strategy report) and at least 7 days; do not change targets during that window except to fix tracking or policy.
3. Search terms (weekly): add irrelevant queries as negatives (use phrase/exact; remember no close-variant matching for negatives); promote converting queries to exact/phrase. Check Arabic and Latin variants.
4. Wasted spend rule (heuristic): a keyword/ad group/asset with spend above about 2-3x the target CPA and zero conversions, after tracking is confirmed working, is a candidate to pause or demote. With no CPA target, use 2-3x the average CPA of the campaign.
5. When to wait: Learning status; fewer than one conversion cycle since a change; conversion lag still open (recent days under-reported). Never compare yesterday's CPA with last month's CPA when the lag is 3+ days.
6. When to scale budget (heuristic): raise daily budget 20% at most per step, at most every 3-7 days or after 1-2 conversion cycles, only if the campaign is budget-limited and the CPA/ROAS is inside target. Google's own advice after a budget increase: evaluate over 1-2 conversion cycles; keep daily budget comfortably above average spend (help 17061251). Doubling a budget in one step is the common cause of CPA spikes.
7. When to change tCPA/tROAS (heuristic): move the target in steps of about 10-20% (Demand Gen FAQ cites about 10% steps and starting tROAS 20% below the last 30 days). After the 2026-08-17 change, a tight target on a budget-limited campaign now restricts delivery; loosen it or raise budget.
8. When to switch bidding: Manual/Maximize Clicks to Maximize Conversions once about 15-30 conversions in 30 days exist; to tCPA/tROAS once the section 5 thresholds are met and conversion values are reliable. Use experiments for the switch if spend allows ("Save as experiment" option on the tCPA page).
9. Creative fatigue / asset decay: CTR and conversion rate falling for 7+ days while impressions are stable, or "Low" asset ratings after enough impressions. PMax: wait 2-3 weeks before replacing low-performing assets (help 14528220); add new assets rather than deleting winners.
10. Testing budget rule (heuristic with reasoning): to compare two variants on CPA you need enough conversions per variant for the difference to be visible; as a minimum, budget at least 10x the target CPA per variant per week (aligned with Google's "10 times tCPA" daily budget guidance for Demand Gen). If a variant cannot reach that, test on a higher-funnel metric (CTR, CVR to lead) and accept lower confidence.
11. What not to touch during learning: bid strategy type, conversion goals, campaign composition (adding/removing keywords/ad groups), big budget changes, final URLs of the main landing page, and audience signals in PMax; make one change at a time and log it.
12. Brand vs non-brand: never evaluate blended CPA when brand is mixed in; brand search is cheap and flatters results.
13. PMax cannibalization: Search with exact keywords wins over PMax for matching queries; use brand exclusions/negatives in PMax if it takes brand traffic you want in Search.
14. Frequency/reach (Demand Gen/YouTube): frequency cannot be capped in Demand Gen; watch unique reach and impressions per user instead.

## 10. Metrics and definitions
| Google Ads term | Standard | Notes |
|---|---|---|
| Impr. (impressions) | Impressions | Search: ad shown; Shopping/PMax similar |
| Interactions / Clicks | Link clicks | "Interactions" includes engagements in some formats |
| Avg. CPM | CPM | cost per 1,000 impressions |
| CTR | CTR | clicks / impressions |
| Avg. CPC | CPC | actual price paid per click; often below max bid |
| Conversions | Conversions | counts per the "Include in Conversions" setting and conversion action count (one vs every) |
| Conv. rate | CVR | conversions / interactions |
| Cost / conv. | CPA | |
| Conv. value | Revenue | needs values on conversion actions |
| Conv. value / cost | ROAS | multiply by 100 for tROAS percent (help 6268637) |
| All conv. | all conversions | includes secondary actions and cross-device/view-through where configured |
| Search impr. share, lost IS (budget/rank) | Impression share | Lost IS (budget) tells you if more budget could buy volume; lost IS (rank) points to bid/quality |
| Quality Score (1-10, keyword level) | Diagnostic only | Not an auction input; do not optimize or aggregate it (help 6167118). Components: expected CTR, ad relevance, landing page experience (Below/Average/Above average) |
| Ad Rank | Auction score | Bid, ad and landing-page quality, thresholds, context, expected impact of assets (help 1722122) |
| Ad Strength | Creative completeness | Poor/Average/Good/Excellent; Google says raising it from Poor to Excellent gave about 15% more clicks and conversions on average (Google internal data, Aug 2025); it is not a performance guarantee |
| Engaged-view conversions, view-through conversions | video-influenced | See `youtube-ads.md` |

## 11. API and automation
- Official API: Google Ads API (GAQL reporting via Search/SearchStream; mutates for campaigns, budgets, ads, assets, keywords, negatives, conversion uploads). Data Manager API is the route for new conversion/Customer Match integrations.
- Access levels (developers.google.com access-levels; daily operation limits use a sliding 24 h window):
  - Test: test accounts only, 15,000 ops/day.
  - Explorer: production 2,880 ops/day (test 15,000); apply in Cloud Console; automated review in most cases; restricted: account creation, user management, planning, billing.
  - Basic: 15,000 ops/day; requires brand verification and Explorer first.
  - Standard: unlimited daily operations; manual audit (about 10 business days), must meet required minimum functionality.
  - Per-service quotas still apply at Standard; system rate limits are per hour.
- Requirements: a developer token (from a manager account), OAuth2 credentials, Cloud project with the API enabled. Do not store tokens or refresh tokens in the repo; use a secret store.
- Limits (quotas page): up to 10,000 mutate operations per request; Planning Service 1 req/s; keyword planning 1 req/s per customer ID; 2,000 click/call conversions per upload request; GAQL IN clause up to 20,000 items; 64 MB gRPC message limit; RESOURCE_EXHAUSTED (HTTP 429) on quota. Search and SearchStream count as one op each; failed requests still count.
- Restrictions for new adopters: UploadClickConversions restricted from 2026-06-15; Customer Match restricted from 2026-04-01; use Data Manager API.
- What an agent can automate safely:
  - Read-only: daily/weekly reports, search term mining, budget-pacing alerts, policy status, billing status.
  - Low-risk writes: add negative keywords, pause assets/keywords flagged by explicit rules, budget changes within a percentage cap, label creation.
  - High-risk writes (require human approval): changing bid strategies or targets, creating campaigns, uploading conversions, changing billing/payments, account-level negatives. Billing and account budget mutates only work on monthly-invoiced accounts and need at least 12 hours between changes (quotas page).
- Guardrails for automated changes: max budget step 20% per change; at most one budget/target change per campaign per 3 days; never change during "Learning"; log before/after; stop on policy or billing errors; dry-run first. These are heuristic safety rules, not Google requirements.
- Google Ads scripts (developers.google.com scripts limits): JavaScript in the account; max 30 minutes per run (changes already made remain); iterators return 50,000 entities by default; withIds up to 10,000 IDs; log truncated at 100 KB; manager scripts run up to 50 accounts in parallel; bulk upload up to 50 MB / 1 million rows; up to 250 authorized scripts per account.
- Built-in automated rules (UI) and Recommendations exist; applying "Auto-apply recommendations" can change bids, keywords and assets without review. `unverified` in this pass for the exact auto-apply list; rule: review auto-apply settings at account takeover and turn off anything that changes budgets, targets or keywords without approval.
- Editor/API changes obey the same policies; automated mass account creation or ad cloning can trigger suspension (see circumvention caution, section 8).

## 12. Cases
**Situation: Ad disapproved (policy).**
**Do:** read the exact reason in Policy manager; fix ad text, page or feed; save to resubmit; appeal in batches only if you believe it is an error; wait 24 h between appeals; edit minimally to force re-crawl.
**Avoid:** mass duplicates, blind rewording, appealing the same ad 3 times with identical text, hiding the offending content with redirects.

**Situation: Account suspended.**
**Do:** identify the policy (misrepresentation, payment, other) from the notice; fix root cause on site and in ads; submit the appeal form with honest, complete facts; prepare business documents; complete advertiser verification if asked.
**Avoid:** opening a new account to continue advertising (egregious-violation accounts may not advertise again; circumvention risk), submitting false info, repeated identical appeals.

**Situation: Spend with no conversions.**
**Do:** first prove tracking (conversion diagnostics, test conversion, tag fires once, value present); check search terms for intent mismatch; check landing page speed and form/WhatsApp link; tighten match types and negatives; if tracking is fine and spend is above 2-3x target CPA with 0 conversions, pause the worst segment (heuristic).
**Avoid:** switching bid strategy daily; blaming Smart Bidding before verifying data.

**Situation: CPA doubled suddenly.**
**Do:** check recency (conversion lag makes recent days look worse), tracking/consent changes, landing page or stock change, budget or target change in the last 7 days (change history), competitor/seasonal effect, the 2026-08-17 target-delivery change for budget-limited tCPA/tROAS campaigns. Roll back the single most recent change if it fits.
**Avoid:** several simultaneous fixes; resetting learning.

**Situation: "Learning" / limited data.**
**Do:** wait 1-2 conversion cycles; consolidate campaigns to concentrate conversions; use a micro-conversion (add to cart, lead) as primary only if it correlates with revenue; Max Conversions before tCPA.
**Avoid:** adding/removing keywords or ad groups during the period; tCPA far below history (Demand Gen guidance).

**Situation: Creative/asset fatigue.**
**Do:** add new RSA headlines/PMax assets; refresh Demand Gen creative; wait 2-3 weeks before replacing low-rated PMax assets.
**Avoid:** deleting the best assets; pinning too many headlines (cuts combinations, lowers Ad Strength).

**Situation: Google Ads vs GA4/CRM mismatch.**
**Do:** compare using the same window and date basis; check consent mode loss, enhanced conversions, duplicate tags, imported GA4 key events vs native tag; use CRM as the revenue truth for leads and import offline conversions.
**Avoid:** bidding on one number and reporting another without noting it.

**Situation: Tiny budget (for example below the budget needed for 15 conversions a month).**
**Do:** single Search campaign, exact/phrase keywords, tight location, Maximize Clicks with a CPC cap or Maximize Conversions; use a lead-quality micro-conversion; run during business hours.
**Avoid:** PMax, Demand Gen with tCPA (needs 10x tCPA/day budget), broad match without negatives and conversion data.

**Situation: Local lead gen / WhatsApp-click campaign (Egypt).**
**Do:** Search + call assets (local verified number) + location targeting by city/radius; track WhatsApp button click as a conversion event on the page; import real sales/qualified-lead status via offline conversion upload or enhanced conversions for leads; add Arabic and Latin-script keywords; use ad schedule matching staffed hours.
**Avoid:** optimizing for raw WhatsApp clicks forever (low quality leads); virtual/premium phone numbers (disallowed in assets); sending users to a page that hides the offering (destination mismatch).

**Situation: Scaling too fast.**
**Do:** increase budget 20% per step every 3-7 days; verify the campaign is budget-limited and CPA/ROAS is inside target; review after 1-2 conversion cycles.
**Avoid:** doubling budgets; changing tCPA and budget the same day.

**Situation: Seasonal peak (Ramadan, Black Friday, White Friday).**
**Do:** raise budgets before the peak so Smart Bidding sees volume; prepare creative and offers; ensure feed prices/availability are current (Merchant Center mismatches disapprove products); plan the target change you want after the peak. Google offers Smart Bidding seasonality adjustments; details `unverified` in this pass.
**Avoid:** large target changes the first day of the peak; launching new campaigns during the peak with no learning time; making tCPA/tROAS tighter than your peak-season CPA.

## 13. Pre-launch checklist
1. Is billing active, with a backup payment method, and (for Egypt addresses) are the TRN and UIN entered or VAT accepted?
2. Is advertiser verification complete or not requested?
3. Does the business have the licenses/qualifications for the product (restricted categories checked)?
4. Does the final URL return 200 to AdsBot, load fast on mobile and show the offer in the ad?
5. Is the Google tag firing once per conversion with a test conversion visible?
6. Are conversion values set (for tROAS) and is the conversion window correct (default 30/3/1)?
7. Is enhanced conversions on (if consent allows) and consent mode v2 correct for EEA traffic?
8. Is the primary conversion action the real business outcome, not a page view?
9. Are location (Presence) and language settings correct for Egypt/MENA targeting?
10. Are negative keyword lists loaded (including Arabic/Latin variants)?
11. Are there at least 2 RSAs per ad group with 8+ unique headlines, 4 descriptions, no unreliable claims?
12. Is brand search separated from non-brand?
13. Is the bid strategy matched to data (section 5 thresholds) and the budget at least 10x target CPA/day where tCPA is used?
14. Is auto-apply recommendations disabled for budget/target/keyword changes?
15. Is PMax/Demand Gen creative complete in every required ratio with Arabic text inside safe areas?
16. If Shopping/PMax feed: GTINs valid, no promo text in titles, images at least 500x500?
17. Are alerts in place for billing failure, disapprovals, and spend anomalies?
18. Is there a written change log and rollback owner?

## 14. Sources
- Smart Bidding: https://support.google.com/google-ads/answer/10970825
- Target CPA: https://support.google.com/google-ads/answer/6268632
- Target ROAS: https://support.google.com/google-ads/answer/6268637
- Bidding change 2026-08-17: https://support.google.com/google-ads/answer/17061251
- Learning period: https://support.google.com/google-ads/answer/13020501 and https://support.google.com/google-ads/answer/12563349
- Data-driven attribution: https://support.google.com/adwords/answer/7003150
- Conversion windows: https://support.google.com/google-ads/answer/3123169 ; store visits https://support.google.com/google-ads/answer/9462121
- Enhanced conversions: https://support.google.com/google-ads/answer/9888656 ; https://support.google.com/google-ads/answer/15712870
- Consent mode: https://support.google.com/google-ads/answer/13695607 ; https://developers.google.com/tag-platform/security/concepts/consent-mode
- Budgets: https://support.google.com/google-ads/answer/1704424 ; https://support.google.com/google-ads/answer/16913225
- Payments and billing: https://support.google.com/google-ads/answer/2375433 ; https://support.google.com/google-ads/answer/1704418 ; https://support.google.com/google-ads/answer/2393016
- Taxes (Egypt VAT): https://support.google.com/google-ads/answer/2375370
- Advertiser verification: https://support.google.com/adspolicy/answer/9703665 ; https://support.google.com/adspolicy/answer/9870201
- Account access: https://support.google.com/google-ads/answer/6372672
- Match types: https://support.google.com/google-ads/answer/7478529 ; negatives https://support.google.com/google-ads/answer/2453972
- Quality Score: https://support.google.com/google-ads/answer/6167118 ; Ad Rank https://support.google.com/google-ads/answer/1722122
- RSA: https://support.google.com/google-ads/answer/7684791
- Performance Max: https://support.google.com/google-ads/answer/11605187 ; asset groups https://support.google.com/google-ads/answer/14528220 ; https://developers.google.com/google-ads/api/performance-max/asset-requirements
- Demand Gen: https://support.google.com/google-ads/answer/13695777 ; specs https://support.google.com/google-ads/answer/13704860 ; https://support.google.com/google-ads/answer/17140672 ; FAQ https://support.google.com/google-ads/answer/14509385
- Display to Demand Gen (secondary): https://www.searchenginejournal.com/google-is-retiring-standalone-display-campaigns-in-favor-of-demand-gen/575889/
- App campaigns: https://support.google.com/google-ads/answer/6247380
- Merchant Center: https://support.google.com/merchants/answer/7052112 ; languages/currencies https://support.google.com/merchants/answer/160637
- Policies: https://support.google.com/adspolicy/answer/6316 ; misrepresentation https://support.google.com/adspolicy/answer/6020955 ; https://support.google.com/adspolicy/answer/14599564 ; https://support.google.com/adspolicy/answer/14092889 ; unreliable claims https://support.google.com/adspolicy/answer/15936857 ; destination https://support.google.com/adspolicy/answer/6368661 ; appeals https://support.google.com/adspolicy/answer/9338593
- API: https://developers.google.com/google-ads/api/docs/api-policy/access-levels ; https://developers.google.com/google-ads/api/docs/best-practices/quotas ; scripts https://developers.google.com/google-ads/scripts/docs/limits
- Third-party (caution): https://www.spendfigo.com/guides/google-ads/egypt (card declines claim, unverified)

Unverified summary: Egypt prepay availability, EGP billing currency for advertisers, access-level definitions, financial/healthcare rules for MENA, circumvention policy text, before/after rule, AI Max details, GA4 vs Ads discrepancy page, iOS ATT, language-targeting and location "Presence" option text, Smart Bidding seasonality adjustments, auto-apply list, Egypt data-protection law, Egypt/MENA benchmarks.
