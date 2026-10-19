# Telegram Ads — rules and playbook
Last verified: 2026-10-19

Read this first: Telegram's official advertising pages are short. Many things a media buyer expects (pixel, conversion events, audiences, demographic targeting, an advertiser API, published minimum budget) are not documented in official sources and must be treated as not available unless a human confirms them inside the logged-in Ad Platform. Items marked `unverified` come either from the logged-in product (not readable without a Telegram account) or from memory. Do not invent numbers for this platform.

## 1. When to use it
- What it is: Telegram's own self-serve ad platform ("Telegram Ad Platform", ads.telegram.org). Ads are short text sponsored messages shown in public one-to-many channels with 1,000+ subscribers; per the API docs, sponsored posts also appear below a channel's last post, as an ad bar above bot chats, as text ads over channel fullscreen video, and as sponsored peers in global search. Premium subscribers do not see Telegram-displayed sponsored messages. Sources: https://ads.telegram.org/ , https://core.telegram.org/api/sponsored-messages , https://telegram.org/tos/ad-platform
- Official reach claim (self-reported, not independently verified): 1 billion users generating 1 trillion views per month in public broadcast channels. Source: https://ads.telegram.org/
- Strengths: attention inside channels where the audience chose to follow a topic (news, jobs, education, crypto, deals, local communities), channel-level contextual targeting, a simple text format (no creative production), strong for promoting a Telegram channel, bot or mini app (the destination is native to Telegram), no use of private chat content or contacts for targeting (stated by Telegram).
- Weaknesses: no pixel or conversion API, no audience or retargeting building, no documented demographic targeting, thin reporting (needs verification), text-only format with a 160-character limit, strict policy on finance, health, gambling and political content, payment in cryptocurrency per the official page, and country availability of sponsored messages is limited to "certain countries" without a list.
- Best objectives: grow a Telegram channel (subscribers), start a bot, drive traffic to a landing page or mini app, awareness among niche channel audiences. Poor for direct-response e-commerce that needs measured purchases.
- Relevance in Egypt / MENA: Telegram is widely used in the Arab world for education, news and deal channels (qualitative; no official per-country usage figure was found, so do not quote one). Whether sponsored messages are shown in Egypt, KSA, UAE and other MENA countries, and whether advertisers from Egypt can pay: `unverified` (the terms say only "certain countries"). Test with a small budget and check delivery statistics by country if the platform gives them. Alternative route: buy posts directly from channel admins; Telegram says admin-posted third-party promotions are not part of its ad platform, so platform policies and tools do not apply (see section 3). See ../mena-and-egypt-notes.md.

## 2. Account, billing and access
- Access: log in at ads.telegram.org with a phone number in international format; Telegram sends a confirmation message to your Telegram account. The page says anyone can post ads through the platform. Sources: https://ads.telegram.org/
- Account structure: advertiser account tied to a Telegram identity (phone number). Multi-user or agency access, business verification, and permission roles: `unverified` (not documented in readable pages). Practical rule: create the account under a company-controlled number and document who holds it; do not use a personal number you may lose.
- Payment: the official page says ads are paid for with Gram, a cryptocurrency (speed and low commissions). No fiat card, bank transfer, EGP/SAR/AED or invoice option is described on the readable pages. Which currencies or fiat top-up methods exist in the logged-in product, minimum top-up, and whether the token is TON: `unverified`. Egyptian advertisers: crypto purchase and use by companies may have legal and accounting implications locally; get advice. See ../mena-and-egypt-notes.md.
- Minimum budget, minimum CPM, minimum top-up: not stated on the readable pages. `unverified`. Read them in the platform before quoting any figure.
- Tax/VAT: the Telegram terms say users in certain regions may owe local taxes and charges are generally nonrefundable. Whether Telegram issues invoices or VAT receipts to advertisers: `unverified`. Sources: https://telegram.org/tos/ad-platform
- Refunds: terms state purchases are generally nonrefundable (the quoted text covers Premium; whether it applies to ad balance: `unverified`). Treat any top-up as spent.
- Age and eligibility: sign-up requires agreeing not to spam, scam, promote violence or illegal activity; users in the EU, UK and Australia must be 18+.

## 3. Campaign structure
- There is no documented campaign > ad set > ad hierarchy or objective selector in the official pages. Each ad has: ad text (up to 160 characters including spaces) and a button that opens a link to the promoted product. You also choose where it appears. Source: https://ads.telegram.org/guidelines
- Targeting objects named in sources: specific channels you pick (stated on the main page); search queries (the guidelines refer to "search keywords", which implies search placements); language of the targeted channel must match the language of the ad and destination. Topics and bots as targeting options: not on the readable pages (`unverified`).
- Buying type: auction in the platform with a price per 1,000 views (CPM) is commonly described, but the readable pages do not state the pricing model. `unverified`. Check in the ad form whether the price is CPM or other.
- Recommended structures (judgment, since platform features are unverified):
  - Small: one ad text, one destination, a hand-picked list of 10 to 30 relevant channels in the target language, one test budget. Tag the destination for tracking (section 7).
  - Medium: 3 to 5 ad texts across 2 or 3 channel clusters (by topic). One variable per test.
  - Large: add direct-from-admin buys (third-party channel promotion) for specific premium channels, tracked with named invite links; keep the official platform for scale.
- Direct buys from channel admins (not Telegram Ads): posts, pinned posts, forwards and story-style placements arranged privately or through marketplaces. Telegram states these are not part of its ad platform. Risks: fake subscribers or views, no policy review by Telegram, payment risk. Mitigate with named invite links, escrow, trial post, check channel statistics (views per post vs subscribers) and screenshots of admin stats. Practitioner observation, not an official rule.

## 4. Targeting and audiences
- Contextual by channel: you select the channels. Channels must be public one-to-many with 1,000+ subscribers to carry Telegram sponsored messages. Source: https://ads.telegram.org/
- Language: policy requires the targeted channel's language to match the ad and destination language. Arabic channels need Arabic ads; Egyptian dialect vs Modern Standard Arabic is not a targeting option (`unverified` whether any dialect option exists). Source: https://ads.telegram.org/guidelines
- Search keywords: the guidelines imply search-query targeting but forbid keywords that exploit harmful, prohibited or sensitive topics.
- Prohibited in ads and targeting: ads may not highlight personal characteristics such as ethnicity, religion, location or financial status.
- Privacy: Telegram says it does not use private chat contents or contacts for ad targeting. There is no documented way to upload customer lists, build retargeting audiences, or build lookalike audiences. Treat these as not available. Demographic targeting (age, gender, country, interest profiles): not documented (`unverified`); country-level targeting of delivery: `unverified`.
- Premium users do not see Telegram-displayed sponsored messages, so reach excludes them.
- Arabic notes: channel names and bios are often Arabic and mixed with English; pick channels by reading recent posts, not by name. Use channels whose audience matches the offer country (Egyptian dialect and local currency mentions matter). Verify channel authenticity (views per post relative to subscriber count; sudden subscriber spikes).

## 5. Bidding, budget and delivery
- Bid strategies, budget types, daily vs total budget, pacing, frequency caps and learning phase: none documented on the readable official pages. `unverified` for all.
- Practical approach (judgment): start with a small fixed test budget; keep the same ad text and a single destination per test; compare channel groups; do not change price and text at the same time; allow a few days and enough views before judging (no official threshold).
- Revenue share: 50% of ad revenue goes to the owners of the channels where ads run. This does not change what the advertiser pays. Source: https://ads.telegram.org/
- Sensitive events: ads tied to ongoing sensitive events or topics may be suspended temporarily (guidelines). Plan for pauses during crises.

## 6. Creative specs and requirements
Source: https://ads.telegram.org/guidelines (re-check before production).
| Placement / format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Sponsored message (channel) | none (text only) | no image upload documented | n/a | n/a | 160 characters including spaces | One button opening the promoted link; optional single @link or t.me/link in text, same destination as the URL field |
| Fullscreen video overlay ad | none | small text box | n/a | n/a | text only | Per API docs; same ad object |
| Search placement | none | n/a | n/a | n/a | same 160 | `unverified` format details |
| Bot ad bar | none | n/a | n/a | n/a | same 160 | Shown above chat in bots |
- Editorial rules: standard grammar and punctuation. Forbidden: profanity (including disguised), unclear or repetitive wording, gimmicky capitals, bold, letter spacing, symbol art, excessive emoji, line breaks, bullet points, numbered lists.
- Link rules: main link in the URL field; one optional link in the text; both must reach the same destination; bot start parameters allowed; no more than one link in text, no URL shorteners, no IP addresses.
- Destination rules: promoted channels, bots and accounts need a profile image and a full about/description; destinations must be functional (no under-construction pages, errors, paywalls, login walls, geo-blocked sites); must match the ad text; no mock data-collection pages, redirect-only pages, bots or automatic redirects; no spoofing of other brands; channels must have a post within two weeks before review; no empty or abandoned channels.
- External links: ads that lead outside Telegram's trusted domains show a confirmation prompt before opening (API docs), which adds friction to website traffic. Telegram links open in app.
- Arabic / RTL cautions: Arabic text and Latin text (brand names, numbers, URLs, usernames) mix and can reorder; keep the line short, avoid punctuation next to Latin handles, test display in Telegram on iOS and Android and desktop. Because line breaks and emoji are restricted, rely on simple sentences. The 160-character limit is counted in characters, and Arabic diacritics may count; count after final proofreading. Use plain Arabic that matches the audience (Egyptian vs Gulf vs MSA) and match the channel language exactly.

## 7. Tracking and measurement
Not available (as far as documented): Pixel, tags, JavaScript snippet, server-side Conversions API, attribution windows, conversion events, audience building, view-through, SKAdNetwork-style reporting. No official GA4 integration. Do not promise conversion tracking from the platform.
What you can do:
- Website destination: append UTMs (`utm_source=telegram`, `utm_medium=paid-social` or `cpm`, `utm_campaign`, `utm_content=ad-id-or-channel-cluster`) to the URL-field link; read them in GA4 or your analytics. Whether the platform keeps query strings intact: verify with a test click (`unverified`). Remember that Telegram's in-app browser can strip or isolate cookies; GA4 sessions will likely be fewer than platform clicks (no sourced ratio).
- Bot destination: use a deep-link start parameter as the source tag. Format `https://t.me/<bot>?start=<param>`; allowed characters A-Z a-z 0-9 _ and -, up to 64 characters (base64url recommended for other content). Parse the `/start` payload in the bot and log source, ad id and channel cluster. Source: https://core.telegram.org/bots/features
- Channel destination: create named invite links for the channel (multiple links with a title; each link has usage counts; joins via a link can be inspected; links can have expiry, usage limits and join-request approval). Use a different link per ad or channel cluster to count joins by source. Source: https://core.telegram.org/api/invites . Whether the ad button can use a custom invite link, or only the public t.me link: `unverified`.
- Mini app destination: use start parameters for Mini Apps (guide not read; `unverified`).
- Platform statistics: the Ad Platform shows statistics inside the logged-in product; fields (views, clicks, cost, joins, CTR) are `unverified`. Export them manually to your sheet daily.
- Offline and CRM matching: ask for the Telegram username or phone and the "source" in the first bot message or form; store the source tag with the lead.
- Consent/privacy: Telegram does not give you user-level data; any data you collect is via your bot, site or form and must follow local privacy law. Do not use scraping tools on Telegram data: Telegram prohibits data scraping under its Content Licensing and AI Scraping Terms. Source: https://telegram.org/tos/ad-platform

## 8. Policies and restricted content
Source: https://ads.telegram.org/guidelines and https://telegram.org/tos/ad-platform
- Review process: not described in detail. Ads and destinations are reviewed; violators may be suspended without notice. Review time and appeal route: `unverified`. Plan for rejections without a clear reason; keep a backup ad text.
- Prohibited content (summary of the guidelines): graphic, shocking or sexual content; hate, violence, harassment, discrimination; third-party rights violations (copyright, trademark, impersonation); deceptive, misleading or predatory advertising (clickbait, absolute claims, fear tactics, exploiting tragedies); political campaigns, candidates, parties and religious promotion; gambling (betting, lotteries, tips and odds); deceptive financial products (payday loans, get-rich-quick, multilevel marketing, hidden fees); unlicensed medical products or services, supplements with unverified health claims, prescription medication; alcohol, tobacco, recreational drugs and paraphernalia; weapons and ammunition; spam, malware, fake engagement or follower services, automated clicks, phishing; products of questionable legality (forgeries, stolen data, counterfeit goods).
- Implications for MENA: religious promotion and political content are banned; alcohol and gambling banned; crypto and trading offers are not named but "deceptive financial products" and "get-rich-quick" are; investment, forex and trading-signal offers need extra caution (whether regulated forex or crypto is allowed: `unverified`).
- Account rules: the Telegram ToS bans spam and scam use, violence promotion on public channels, public illegal pornography, and activities illegal in most countries. Giveaways are regulated by local law and organizers are responsible; channels using misleading giveaways can be terminated or labeled as scams. Source: https://telegram.org/tos/ad-platform
- Destination requirements: see section 6 (functional destination, same destination for text link and URL, no login walls, no shorteners, channel active in the last two weeks).
- Claims rules: no absolute claims, no unsupported health claims, no clickbait. Prices and offers must match the landing page (principle from "must match the ad text").
- Impersonation: do not imitate other brands, bots or channels; Telegram suspends this quickly.
- Top rejection causes to expect (judgment from the rules; no ranking published): emoji or line breaks, shortened or mismatched links, destination bot not responding, new or inactive channel, finance or health claims, language mismatch between ad and channel.

## 9. Optimization playbook
Because the platform exposes little, optimization is about channel selection, message and tracking discipline.
1. Before spending: build the tracking (UTM, bot start parameter, named invite link), test the destination from a fresh device and check it responds in under a few seconds (judgment). A broken destination is a rejection cause and a waste of money.
2. Start small and uniform: one text, one destination, 10 to 30 channels in the target language; avoid mixing languages. Record the cost and views per channel cluster if the platform reports it (`unverified`).
3. Judge on your own data, not on the platform: cost per click or join, cost per bot start, cost per qualified lead or sale, measured with your tracking. The platform has no conversion data.
4. Wait: do not edit the ad text while a test is running; allow enough views to compare (judgment: at least a few thousand views per cluster, or whatever gives you about 50 clicks per variant).
5. Cut: pause a channel cluster whose cost per qualified result is 2 to 3 times the best cluster after the same number of views; pause an ad text with a weak click rate relative to siblings (judgment).
6. Scale: only widen by adding similar channels (same topic and language) after tracking shows acceptable cost per qualified lead; raise spend gradually (judgment: 20% steps).
7. Fatigue: channel audiences see ads repeatedly; expect declining response when the same text runs for weeks. Rotate copy every 1 to 2 weeks (judgment). Frequency is not controllable in documented features.
8. Quality: track retention, not just joins. For channel growth, check how many new subscribers remain after 7 and 30 days, and whether they engage with posts. Remove channels that bring subscribers that leave quickly.
9. Fraud checks for direct admin buys: compare views per post with subscriber count, check post history, ask for admin screenshots, and use a tracked invite link with join counts; never prepay a large amount.
10. Do not touch during a test: destination, language, channel list, and text together. Change one.
11. Test budget reasoning: because the minimum budget is unknown, set the test budget so you can reach at least 100 tracked clicks, 100 bot starts or 20 qualified leads (judgment), using the first 24 hours of CPM and click rate to estimate cost.

## 10. Metrics and definitions
The platform's metric names were not readable without login. Map generic terms to what you can measure yourself.
| Standard term | Telegram Ad Platform | Your own measurement |
|---|---|---|
| Impressions / views | views of the sponsored message (`unverified` name) | n/a |
| CPM | price per 1,000 views (`unverified` pricing model) | spend / views x 1000 |
| Clicks | clicks on ad button (`unverified`) | UTM sessions, bot starts, invite-link joins |
| CTR | clicks / views | tracked clicks / views |
| CPC | spend / clicks | spend / tracked clicks |
| Joins / subscribers | channel joins (`unverified` availability) | `usage` count on a named invite link |
| CPA / CPL | not provided | spend / qualified leads from your CRM |
| CVR | not provided | leads or orders / tracked clicks |
| ROAS | not provided | revenue attributed by source tag / spend |
| Frequency | not provided | not available |
- Currency: spend is in the platform's payment token per official page; convert to USD/EGP using a fixed rate and date in every report (`unverified` how the platform displays cost).
- Always label Telegram numbers "platform-reported, no conversion tracking" in reports.

## 11. API and automation
- Advertiser API: none documented. The Telegram API docs for sponsored messages describe only client-side calls (fetching, viewing, clicking and reporting ads inside Telegram clients) and link to ads.telegram.org for advertiser information. Source: https://core.telegram.org/api/sponsored-messages . So creating, pausing or reporting on campaigns by API: not available. Automation of the Ad Platform UI through scraping or browser bots would violate Telegram's scraping prohibition and risk the account; do not do it. (Telegram prohibits data scraping under its Content Licensing and AI Scraping Terms.)
- Can automate around it: your own bot (Bot API) to log `/start` parameters, route leads to a CRM or WhatsApp, send a welcome message, and compute cost per start by source; reading channel invite link usage via the Telegram API for channels you administer (https://core.telegram.org/api/invites); sheet or dashboard updates from manually exported platform stats.
- Rate limits for these are those of the Bot API and Telegram API: not researched here (`unverified`).
- Rules for automated changes: none apply to the Ad Platform since no API exists; all changes are manual and should be logged in the plan with timestamp, ad id and reason.

## 12. Cases
**Situation** Advertiser wants to run Telegram Ads to drive online purchases and see ROAS in the platform.
**Do** Explain that there is no pixel or conversion tracking; set up UTM links and a tracked checkout or a bot flow, count orders by source tag, and judge Telegram on cost per tracked order from your own data.
**Avoid** Promising platform-reported ROAS, or comparing Telegram cost per click to Meta's conversion-optimized results as if they were the same measure.

**Situation** Ad is rejected with no clear reason.
**Do** Check the 160-character limit, remove emoji, line breaks, caps, bold and extra links, confirm the text link and URL field match, make sure the destination channel or bot has a profile picture, a description and a recent post, and resubmit a plainer version.
**Avoid** Using URL shorteners, redirect pages, login walls or under-construction pages; creating many near-identical ads to find which passes.

**Situation** Promoting an Egyptian Arabic education channel to grow subscribers.
**Do** Select Arabic channels about study, exams or careers, write the ad in plain Arabic that matches those channels, use a named invite link per channel cluster, and track joins and 7-day retention.
**Avoid** Choosing channels by name only; mixing English and Arabic ad text on Arabic-only channels (the policy requires language match).

**Situation** A channel admin offers a "guaranteed 20,000 views" post for a flat fee.
**Do** Ask for admin screenshots of statistics, compare views per recent post with subscriber count, run a small trial with a tracked link, and use escrow or pay after delivery.
**Avoid** Prepaying the full amount; treating it as Telegram Ads (it is outside Telegram's platform and policy review).

**Situation** Selling investment, forex or crypto signals via Telegram Ads.
**Do** Check the financial policy: "deceptive financial products", "get-rich-quick", gambling-like tips and odds are banned. Confirm with the platform support route before spending and avoid performance promises.
**Avoid** Return guarantees, signal screenshots implying profit, or hidden fees.

**Situation** Promoting a bot and leads arrive without a source.
**Do** Add `?start=` parameters per ad (letters, digits, underscore, hyphen, up to 64 characters), store the parameter on the first message, and report cost per start by ad.
**Avoid** Spaces or Arabic characters in the start parameter (not allowed); reusing one link for all ads.

**Situation** Website click volume looks high but GA4 sessions are far lower.
**Do** Check that UTMs survive the link, test in Telegram's in-app browser, accept some loss from the browser confirmation prompt for external links, and measure on landing-page events or a bot step instead of clicks.
**Avoid** Blaming GA4 first; adding multiple links or shorteners to the ad.

**Situation** Platform is not available or the payment method is not accepted for an Egyptian company.
**Do** Document the exact message, check the terms ("certain countries" for sponsored messages), ask Telegram through the platform's support route, and plan an alternative: direct admin buys with tracked links, or other platforms.
**Avoid** Using personal crypto wallets or third-party resellers without a written agreement and invoice, or violating local financial rules.

**Situation** A political or sensitive news event breaks while a campaign runs.
**Do** Expect temporary suspension of ads tied to sensitive topics, pause copy that references the event, and keep neutral backup ad text.
**Avoid** Trending-topic hooks or fear messaging (banned as deceptive or exploiting tragedies).

## 13. Pre-launch checklist
1. Is the platform available to the account (login works, sponsored messages allowed for the target country)?
2. Is the payment method confirmed and the minimum top-up known, with the legal and accounting route approved?
3. Is the ad text 160 characters or fewer including spaces, with no emoji spam, line breaks, bullets or caps?
4. Is there only one link in the text, matching the URL field destination?
5. Is the URL free of shorteners and IP addresses?
6. Does the destination work on mobile and desktop and not require login or payment first?
7. Does the promoted channel or bot have a profile image, full description and a post within the last two weeks?
8. Is the ad language the same as the targeted channels' language and the destination language?
9. Is the content outside the prohibited list (finance, health, gambling, alcohol, political, religious)?
10. Is each target channel verified as real (views per post vs subscribers, history)?
11. Are UTMs added and tested to reach analytics?
12. Is a bot `start` parameter or a named invite link set per ad or cluster?
13. Is the destination able to capture the source tag in the lead record or CRM?
14. Is the test budget sized to reach a decision (clicks or leads) and is the review date set?
15. Is there a plain-language backup ad text in case of rejection?
16. Does the report template state "no platform conversion tracking" and show your own measured results?

## 14. Sources
- https://ads.telegram.org/ (main page; reach claim, 160 characters, Gram, 50% revenue share, login)
- https://ads.telegram.org/faq
- https://ads.telegram.org/guidelines (ad guidelines)
- https://ads.telegram.org/terms
- https://telegram.org/tos/ad-platform (Telegram Terms of Service, sponsored messages, taxes, refunds, scraping)
- https://core.telegram.org/api/sponsored-messages (placements and absence of an advertiser API)
- https://core.telegram.org/api/revenue (50% revenue share)
- https://core.telegram.org/bots/features (deep link start parameter)
- https://core.telegram.org/api/invites (invite links and usage counts)
- https://telegram.org/faq_channels (channel view counting)
- Not found in official sources: minimum budget, CPM, supported countries, payment methods beyond Gram, review time, targeting by topic or demographics, statistics fields.
