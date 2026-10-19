# Media buying in Egypt and the Arab world
Last verified: 2026-10-19

Scope: practical notes for agents planning, launching and reporting paid media for Egyptian and Arab-world advertisers. Labels: `unverified` means no official or reliable source was read; `practitioner observation` means common field knowledge, not an official rule. Nothing here is legal or tax advice; tell the client to confirm with an accountant or lawyer. Per-platform detail lives in `platforms/*.md`.

## 1. Payment and billing realities
Verified platform facts (read this session):
| Platform | What is documented | Source |
|---|---|---|
| TikTok | Egypt: pre-pay in EGP by bank card or Fawry, or in USD by card or PayPal; autopay in EGP by card; credit line (monthly invoicing) in EGP by card or Fawry. KSA: SAR by card, USD by card or PayPal. UAE: AED by card, USD by card or PayPal. Kuwait: KWD; Morocco: MAD, no autopay | https://ads.tiktok.com/help/article/europe-middle-east-and-africa-emea-supported-payment-methods |
| LinkedIn | Billing currencies include EGP, SAR, AED, USD, EUR, GBP; KWD, QAR, MAD are not listed | https://learn.microsoft.com/en-us/linkedin/shared/references/v2/ads/supported-currencies |
| X | Egypt, Saudi Arabia and UAE are charged in USD; EGP, SAR, AED not supported; cards only (Visa, Mastercard, American Express and others) | https://help.x.com/en/business-and-advertising/ads-currency and billing-basics |
| Telegram | Official page says ads are paid with Gram, a cryptocurrency; no fiat method described | https://ads.telegram.org/ |
| Meta | Payment table for Egypt could not be read (robots); EGP billing and local methods `unverified`; see platforms/meta-ads.md | https://www.facebook.com/business/help/212763688755026 (not fetchable) |
| Google | Not confirmed here; see platforms/google-ads.md (EGP billing `unverified`; Egypt VAT rule recorded there) | |
- Cards: Egyptian-issued cards are often reported to fail on international ad payments because of foreign-currency limits or bank rules; this is practitioner observation, not an official rule, and bank policies change. Operational rules: keep a second valid payment method, set billing-failure alerts, tell the client's bank the advertising merchants (Meta, Google, TikTok) in advance, and never run a campaign that cannot survive one declined charge.
- Currency: the ad account currency is fixed at creation on most platforms (X requires a new linked account to change; confirmed above). Choose currency and time zone before the first dollar. Report in the client's reporting currency and state the FX rate and date used. EGP devaluation periods distort CPA targets set in USD: refresh targets monthly when the exchange rate moves materially.
- Local entities: opening the ad account under a UAE or KSA entity can unlock local currency billing (for example AED or SAR) and local VAT invoices, but this changes tax, ownership and platform-verification treatment. Whether it is worth it is a business decision: `unverified`; do not recommend without legal advice.
- Vouchers and credits: X's advertising page advertises a USD 500 credit for new advertisers who spend USD 500 with terms (https://business.x.com/en/advertising). Other platforms' welcome credits and agency coupons exist but terms differ by country: `unverified`; never plan a budget around a credit before it is visibly applied.
- Agency billing: agencies commonly pay on the client's behalf and re-invoice with a service fee or run ads from their own account. Risks: client loses ownership of audiences and pixels, platform invoices go to the agency, and local tax documents may not match the client's legal name. Preferred setup: client owns the ad account and pixel; agency has partner or admin access; payment instrument and invoices stay in the client's name. A monthly-invoicing credit line (TikTok) is an alternative where approved.
- Tax at a high level (secondary sources; confirm with an accountant):
  - Egypt standard VAT is 14%. For services bought from non-resident providers, the recipient business generally accounts for VAT under reverse charge; non-resident B2C providers must register. Same PwC summary notes that, under Law 157 of 2025, advertising services are subject to 14% VAT. Source: https://taxsummaries.pwc.com/egypt/corporate/other-taxes
  - Withholding tax on services paid to non-residents is stated at 20% unless a treaty applies (PwC). Whether this is charged on payments to Meta, Google or TikTok (which are billed by foreign entities, often Irish) is `unverified`: ask the accountant. Source: https://taxsummaries.pwc.com/egypt/corporate/withholding-taxes
  - E-invoicing: PwC states only e-invoices are recognized by the Egyptian Tax Authority as support for deductible expenses. Whether a foreign platform's invoice satisfies this: `unverified`; accountants often ask for local documentation of ad spend. Related practical notes are in platforms/meta-ads.md and platforms/google-ads.md (including Google's Egypt TRN/UIN VAT-exemption path).
  - UAE: X (billing entity X International Company, Ireland) charges UAE VAT on personal-use accounts and allows a VAT ID for business use; no VAT is added for non-EU billing addresses elsewhere. Source: https://help.x.com/en/business-and-advertising/value-added-tax-vat-information . Other UAE and KSA VAT mechanics for ad platforms: `unverified`.

## 2. Account and identity verification quirks
- Name consistency matters: legal business name, payment-card holder name, billing address and the website's company details should match; mismatches are a common trigger for payment holds and verification requests (practitioner observation).
- Google advertiser verification is rolling out gradually with possible re-verification after payment profile or legal name changes; details in platforms/google-ads.md. A Google reactivation help page mentions a verification review of up to 48 hours for reactivation; general timelines vary.
- Meta: business verification and domain verification are needed for several features; Egypt-specific documents: `unverified`. Keep admin on the client's Business Manager with two or more admins to avoid lock-out.
- X: country and time zone chosen at account creation set the currency permanently; fixing it needs a support ticket and a new linked account (confirmed).
- Telegram: the account is a phone number; use a company-controlled number.
- LinkedIn: needs a Company Page; role setup determines who can pay and publish (see platforms/linkedin-ads.md).
- Restricted verticals (finance, health, crypto, gambling, political) need advertiser verification or certification in many countries; Egypt, KSA and UAE specifics were not retrieved: `unverified` per platform file.
- Personal vs business accounts: running paid ads from a founder's personal profile or personal ad account creates continuity risk; use a business account.

## 3. Which platforms matter by country
Late-2025 platform-reported ad reach from DataReportal (not monthly active users; estimates may be revised and exceed 100% of a population share):
| Platform | Egypt | Saudi Arabia | UAE |
|---|---|---|---|
| Facebook | 51.6M | 17.7M | 9.70M |
| Instagram | 21.7M | 18.2M | 8.05M |
| TikTok (18+ only) | 48.8M | 38.6M | 12.5M |
| Snapchat | 20.6M | 25.3M | 5.13M |
| LinkedIn (registered members) | 15.0M | 12.0M | 10.0M |
| X | 4.64M | 15.0M | 2.85M |
Sources: https://datareportal.com/reports/digital-2026-egypt , https://datareportal.com/reports/digital-2026-saudi-arabia , https://datareportal.com/reports/digital-2026-united-arab-emirates . Egypt had 98.2M internet users (82.7%) and 51.6M social media user identities in October 2025 per the same report.
- Reading: Egypt is Facebook- and TikTok-led with large mass-market reach and price sensitivity; Saudi Arabia is TikTok- and Snapchat-heavy with strong Instagram and a large X audience; the UAE has a small, high-income, expatriate-heavy population where LinkedIn and Instagram are comparatively strong relative to population.
- Missing from these figures: YouTube, WhatsApp, Telegram, Google Search volume, Pinterest. Treat their country reach as `unverified`; YouTube and WhatsApp are widely used regionally (practitioner observation).
- Other Arab countries (Iraq, Jordan, Kuwait, Qatar, Morocco, Algeria, Lebanon and others): no data was gathered here. `unverified`. Note TikTok billing support for Kuwait (KWD) and Morocco (MAD, no autopay) from the payment page above, and that LinkedIn does not list KWD, QAR or MAD billing.
- Selection heuristics (judgment): mass-market Egypt consumer goods start with Meta and TikTok plus Google Search for high intent; Gulf consumer brands add Snapchat and X depending on audience; B2B and recruitment use LinkedIn, especially for UAE, KSA and Egyptian tech exports; Telegram is a niche, hard-to-measure channel (see platforms/telegram-ads.md). Always check the client's own analytics for where customers actually come from.

## 4. Arabic ad copy and RTL creative issues
- Dialect: use the audience's dialect for consumer ads (Egyptian Arabic for Egypt, Khaleeji for Gulf) and Modern Standard Arabic for formal, financial, government, medical or multi-country copy; keep one dialect per ad (practitioner convention; also noted in platforms/meta-ads.md).
- Numbers and currency: write prices with a consistent numeral system (Western or Arabic-Indic) and a clear currency token (EGP, ج.م, SAR, ر.س, AED, د.إ). Never mix systems in one ad. Prices in the ad must match the landing page (policy risk on several platforms).
- Bidi (mixed direction) problems: Arabic with Latin brand names, hashtags, URLs, @handles and numbers can reorder or flip punctuation. Preview every placement on iOS, Android and desktop. Put Latin terms at sentence ends or isolate them; avoid trailing punctuation after a Latin token.
- Character limits count characters, not words; check after proofreading. Arabic diacritics may count as characters on some platforms: `unverified`.
- Programmatic text rendering (automation): many image and video libraries draw Arabic as disconnected or reversed letters unless text shaping and bidi are applied (for example using a shaping engine such as HarfBuzz/Raqm or an Arabic reshaping plus bidi step). Always inspect rendered output; do not ship auto-rendered Arabic without a native review. Burn captions with a font that supports full Arabic shaping and keep safe margins at the top and bottom (UI overlays).
- Layout: mirror arrows and carousels for RTL where the platform does not; in video, check reading order of on-screen text and animation direction.
- Keywords and search: Arabic spelling varies (hamza forms, ta marbuta vs ha, dialect spellings, Arabizi/Latin). Add variants, review the search terms report in Arabic and Latin script, and add negatives per variant (see platforms/google-ads.md).
- Review: have a native speaker review translated copy; machine translation tends to read as formal MSA, misgender, or produce unintended meaning.
- Cultural fit: avoid religious references used for selling; keep Ramadan and Eid content respectful; check imagery and dress norms by country (more conservative in KSA than in UAE or Egypt; practitioner observation).

## 5. WhatsApp-first conversion paths
- Behavior: in Egypt and the Gulf, many buyers prefer to chat before buying; click-to-WhatsApp ads and WhatsApp buttons on pages often outperform forms on lead quality or speed (practitioner observation; no sourced benchmark).
- Official pricing facts (read this session): since July 1, 2025 the WhatsApp Business Platform charges per delivered business-to-user message by category (marketing, utility, authentication; service and Meta Business Agent for non-template). User-to-business messages are not charged. When a user messages from a click-to-WhatsApp ad, a free entry point window can last up to 7 days, with marketing, utility, authentication and service messages free during it. Egypt (+20) has its own rate card; lower utility and authentication rates took effect October 1, 2025 and lower marketing rates January 1, 2026 per Meta's page. Messaging account currency is chosen at creation and cannot be changed. Source: https://developers.facebook.com/docs/whatsapp/pricing
- Setup rules: use the WhatsApp Business app or API with a company-owned number; keep the ad's promise and the first reply consistent; show business hours; use quick replies and a first message that qualifies (product, city, budget).
- Lead handling speed: define an SLA (for example first reply within minutes during business hours) and measure it; speed to first reply strongly affects conversion (practitioner observation; no sourced figure here). Assign owners, a fallback rota, and an auto-reply outside hours. Record the first-reply time per lead.
- Measurement: platform conversion counts "conversations started" or leads, not sales. Pass qualified or purchase events back to the platform where supported (Meta Conversions API for messaging events: `unverified` details; see platforms/meta-ads.md) and tag the conversation with source, campaign and creative (use a unique click ID or a message prefix; `unverified` mechanisms per platform).
- Compliance: send marketing messages only to people who opted in; follow WhatsApp commerce and business policies (`unverified` here); keep unsubscribe handling.
- Avoid: sending all leads to one phone number with no capacity; judging campaigns on "conversations" without a sales-stage report; using personal numbers.

## 6. Cash-on-delivery (COD) dynamics
No reliable public statistics on COD share, refusal or return rates in Egypt or the Gulf were found in the sources read; do not quote any. The mechanism is the issue:
- Platforms count a purchase when the order is placed (or the thank-you page loads), not when the courier collects cash. Refused, unreachable, duplicate and fake orders inflate reported conversions, ROAS and CPA.
- Reports show gross numbers that look better than the business reality. COD orders also bias optimization: the algorithm learns from fake or low-intent orders if events fire at checkout.
- Reporting fix: report three layers: platform-reported (orders placed), confirmed (after call or WhatsApp confirmation) and delivered or collected (after courier settlement). Compute:
  - Net ROAS = delivered revenue / ad spend.
  - Effective CPA = ad spend / delivered orders.
  - Allowable CPA = contribution margin per delivered order (after product cost, shipping both ways for refused parcels, COD fees and packaging) x delivery rate, then compare to effective CPA.
  - Use cohort tables with a lag (orders settle over days to weeks), and compare cohorts by order date, not by delivery date.
- Optimization fix: send a server-side conversion event only for confirmed or delivered orders (or send a separate "Confirmed Order" event and optimize on it once it has enough volume); add friction against fakes (phone verification, address validation, duplicate-number checks); incentivize prepaid or wallet payment; track cost per confirmed order.
- Operational notes: courier cities and delivery zones affect refusal rates; fix targeting to serviceable areas; align ad promises (delivery time, price including shipping) with reality because returns kill COD economics.
- Pitfalls: scaling on platform ROAS alone; ignoring returned-parcel costs; letting agencies be paid on platform ROAS without delivered-revenue reconciliation.

## 7. Seasonality: Ramadan, Eid, White Friday
- Ramadan 2027 is expected from about 8 February to 8 March 2027 (Umm al-Qura calendar; local moon sighting can shift by about a day). Ramadan 2026 ran about 18 February to 19 March 2026. Eid al-Fitr 2027 should fall about 9 March 2027 (inferred, moon dependent). Eid al-Adha 2027: about mid-May 2027 (approximate, `unverified`). Source for Ramadan dates: https://en.wikipedia.org/wiki/Ramadan
- White Friday: the regional name for the late-November sale event; in 2026 it aligns with Black Friday on Friday 27 November 2026 (day after US Thanksgiving, 26 November). Regional retailers often run multi-day or week-long campaigns around it: practitioner observation, not an official calendar. Other events: 11.11 (11 November), Back-to-school (Egypt, late summer), Saudi Founding Day (22 February), Saudi National Day (23 September), UAE National Day (2 December), Coptic Christmas (7 January). Verify dates annually.
- Typical patterns (practitioner observation, no sourced numbers): TV and online viewing shifts to evenings and late nights during Ramadan; consumer spend rises on food, gifts, fashion, electronics; competition raises auction costs; the weeks right after Eid can be softer. Check the account's own prior-year data; do not assume a CPM uplift.
- Planning timeline for a Ramadan campaign: 8 to 10 weeks out lock offer, budget and creative strategy; 6 weeks out produce creative and landing pages; 3 to 4 weeks out launch pre-Ramadan awareness and build retargeting audiences; 1 week out soft-launch with the main creatives to pass learning and review; during Ramadan shift dayparting toward post-iftar and late evening and refresh creatives weekly; run Eid gift/sale burst; reserve a post-Eid reactivation plan.
- Platform hygiene during peaks: submit ads early (review queues grow; LinkedIn review aims for 24 hours, others vary), keep spare creatives, avoid launching new ad sets on peak days, do not change conversion events during the peak, and raise budgets gradually (see platform files).
- Content rules of thumb: respectful tone, avoid mixing religious messaging with hard sell, avoid daytime food-and-drink imagery aimed at fasting audiences (judgment), and watch regulatory limits on religious content in the Telegram and LinkedIn policies (religious promotion is banned on Telegram Ads).

## 8. Regulatory and advertising-law basics (not legal advice)
- Data protection: Egypt has a personal data protection law (Law 151 of 2020) and the Gulf states have their own laws; whether and how they apply to ad pixels, custom audience uploads and lead forms: `unverified`; ask counsel. Rule of thumb: collect consent for marketing messages, keep opt-out, and do not upload customer lists without a lawful basis.
- Egypt media regulation: a secondary source reports that the Supreme Council for Media Regulation (SCMR) law of 2018 allows supervision of social accounts with more than 5,000 followers; implications for influencers and advertisers: `unverified` (https://en.wikipedia.org/wiki/Media_of_Egypt).
- Saudi Arabia: the General Authority for Media Regulation lists a service for licensing advertising content through social media platforms (Mawthooq). Eligibility, fees and penalties were not retrievable: `unverified`. Source: https://gmedia.gov.sa/en . Ask Saudi-based influencers for their license number before booking.
- UAE: a media or advertiser permit regime for influencers and social advertisers exists (widely reported): `unverified`; the UAE media regulator site could not be read by the research tool.
- Sector rules: finance (forex, crypto, investments), health and pharma, real estate off-plan sales, education, alcohol and gambling each have specific restrictions in the three countries, and platform policies add their own: `unverified` for Egypt, KSA and UAE specifics; see platform policy sections.
- Consumer protection: price accuracy, delivery promises, return and warranty claims must be truthful; Egypt has a consumer protection law (Law 181 of 2018, `unverified` here). Comparative or competitor claims: platform rules require accuracy (LinkedIn, Telegram); local law varies.
- Disclosure: label paid partnerships clearly in Arabic and English (for example "إعلان" or "إعلان مدفوع" and #ad); platform branded-content tools exist (Meta partnership ads, TikTok Spark Ads) and require creator authorization; local rules may demand more.
- Taxes and invoices: see section 1.

## 9. Influencer and creator buying norms
- Pricing: usually per deliverable (story, reel, post, video, live) or package; rates vary widely by country, category and audience. No reliable public rate benchmark for Egypt or MENA was found; do not quote one. Request rate cards and compare cost per thousand views and cost per click from past work.
- Agencies and talent managers: many creators work through managers or agencies that take a commission; negotiate directly or through them, but contract with the party that is paid.
- Vetting: audit audience country split, engagement rate, view-to-follower ratio, comment quality, growth spikes (fake followers), prior brand work, and brand-safety history; ask for native analytics screenshots (reach, audience location, saves) rather than third-party estimates.
- Contract terms: deliverables and dates, number of revisions, approval rights, usage rights and duration (organic reposts vs paid usage), whitelisting or partnership-ad access, exclusivity, disclosure language, payment schedule, cancellation, and metrics reporting. In KSA check the creator's license (Mawthooq); in UAE check the permit; in Egypt check the creator's registration or business status: all `unverified` in detail.
- Paid amplification: use platform partnership tools (Meta partnership ads, TikTok Spark Ads) so ads run from the creator's handle; requires the creator's authorization code or permission; see platform files. Creator content often outperforms brand-made creative for trust (practitioner observation).
- Measurement: unique codes, tracked links with UTMs, WhatsApp click IDs or message prefixes, dedicated landing pages, and post-purchase "how did you hear about us" surveys. Attribute influencer sales conservatively; do not double count with paid media.
- Payment: bank transfer or local payment is typical; keep invoices or receipts. For foreign creators tax and withholding may apply: `unverified`.
- Risk controls: pay a deposit with the balance on delivery, require content approval before posting, and have a takedown clause for brand-safety incidents.

## 10. Sources
- https://ads.tiktok.com/help/article/europe-middle-east-and-africa-emea-supported-payment-methods
- https://learn.microsoft.com/en-us/linkedin/shared/references/v2/ads/supported-currencies
- https://help.x.com/en/business-and-advertising/ads-currency
- https://help.x.com/en/business-and-advertising/billing-basics
- https://help.x.com/en/business-and-advertising/value-added-tax-vat-information
- https://ads.telegram.org/
- https://business.x.com/en/advertising
- https://developers.facebook.com/docs/whatsapp/pricing
- https://taxsummaries.pwc.com/egypt/corporate/other-taxes
- https://taxsummaries.pwc.com/egypt/corporate/withholding-taxes
- https://datareportal.com/reports/digital-2026-egypt
- https://datareportal.com/reports/digital-2026-saudi-arabia
- https://datareportal.com/reports/digital-2026-united-arab-emirates
- https://en.wikipedia.org/wiki/Ramadan
- https://en.wikipedia.org/wiki/Media_of_Egypt
- https://gmedia.gov.sa/en
- Cross-references: platforms/meta-ads.md, platforms/google-ads.md, platforms/tiktok-ads.md, platforms/linkedin-ads.md, platforms/x-ads.md, platforms/telegram-ads.md
- Not readable by the research tool (blocked): Meta payment help pages, UAE National Media Council, Saudi Mawthooq details, Google payment-by-country pages.
