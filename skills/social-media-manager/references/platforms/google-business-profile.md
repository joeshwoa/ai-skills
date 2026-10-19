# Google Business Profile — rules and playbook
Last verified: 2026-10-19

Scope: Google Business Profile (GBP) as a local and social-style channel: posts, photos and videos, reviews and replies, verification, suspension, and the Business Profile APIs. It shows on Google Search and Maps. It is not a feed people follow; it is a storefront that is judged by accuracy, reviews and policy compliance. `unverified` means no official page confirmed it on 2026-10-19. Items marked "secondary source" come from trade press, not Google.

## 1. Snapshot
- A GBP is the business card people see in Search and Maps: name, category, address or service area, hours, phone, website, photos, posts, services/products, menu, reviews and review replies. Posts show on mobile in "Updates" or "Overview" tabs and in the "From the owner" section on desktop (support.google.com/business/answer/7662907).
- Best for: any business that meets customers in person or travels to them: restaurants, clinics, shops, salons, schools, repair services, hotels, agencies with a staffed office.
- Not eligible: online-only brands, organizations and artists; lead-generation agents; virtual offices; remote mailboxes/P.O. boxes; rental or for-sale properties (but sales/leasing offices are eligible) (answer/13763036).
- Egypt: Egypt is listed on Google's "Supported countries/regions" page (answer/6270107). Reviews are available only in certain countries or regions and categories and may change (answer/3474050), so check each listing.
- Ranking basics from Google: local results are mainly based on relevance, distance and prominence (answer/7091). Verified, complete, accurate profiles with photos and replied reviews are more likely to appear.
- For a social media manager: GBP is where reputation is won or lost (reviews), where phone, direction and website clicks happen, and where fake-review or impersonation problems hit hardest.

## 2. Content formats and specs

| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Update post | photo or video optional; no official ratio found (square or 4:3 is a practitioner convention, `unverified`) | description limit `unverified` (practitioner observation: 1,500 chars) | same as photo/video rules below | Optional action button with link (book, order, learn more) |
| Offer post | same | needs title, dates, times; "View Offer" button added automatically | same | Optional coupon code, link, terms. Hotels cannot post offers |
| Event post | same | title, start and end date and time; if times omitted, shows as 24 h | same | Archived after the end date |
| Photo | 720x720 px recommended; 250x250 px minimum | n/a | JPG or PNG; 10 KB to 5 MB | In focus, well lit, no heavy filters; must represent reality. Appears only after verification |
| Logo / cover photo | same photo rules | n/a | same | Logo highlighted when basic info exists; cover not guaranteed to show first |
| Video | 720p or higher | up to 30 s | up to 75 MB | Appears only after verification |
| Customer photo updates | n/a | n/a | n/a | Do not affect rating; you can reply |
| Reviews | text + star rating from customers | n/a | n/a | Reply as the business; owner replies appear without personal name |
| Q&A | discontinued (see section 8) | | | Do not plan content around it |
| Messages / chat | discontinued (see section 8) | | | Use phone, website, WhatsApp or SMS links |
| Story / Live / status | not offered | | | |
| Product posts | cannot be created through the API | | | Use the Products editor in the UI where eligible |

- Posts older than 6 months are archived unless a date range is set (answer/7662907). Posts can be scheduled and set to repeat (weekly, monthly, custom) in the UI. You can post to several profiles at once.
- Post status: Live (public), Pending (processing or unverified profile), Not approved (policy violation).
- Featured posts (auto-surface from your social channels) are limited to English-language, single-location food and drink businesses in the US, UK, Canada, Australia and New Zealand, so Egypt is not covered.
- If you have 10 or more locations, photos can be bulk-uploaded through a spreadsheet.

## 3. Text limits
- Post description: `unverified` on official pages read. Practitioner observation, not an official rule: 1,500 characters; also 1,500 appears widely for API `summary`. Keep the first 100 characters self-contained because truncation is common (`unverified`).
- Post title: required for Offer and Event posts; limit `unverified`.
- Business name: must match real-world signage; no taglines, store codes, ® signs, all-caps words, hours, phone numbers or URLs, special characters or legal suffixes (LLC, Ltd) unless proven on signage, no service or location keywords (answer/3038177).
- Business description: no links of any type, no promotions or prices ("-50%"), no gibberish. Length limit `unverified` (practitioner: 750 chars).
- Review reply: reviewed by Google, usually within 10 minutes but up to 30 days; character limit `unverified` (practitioner: 4,096).
- Hashtags and mentions: no official support or guidance found; do not use as a tactic.
- Links: action buttons (book, order, learn more, sign up, call now) carry the link. Descriptions cannot contain links. In posts, links to unrelated websites, emails, phone numbers and social handles not tied to your business are prohibited (contribution policy, Advertising and solicitation). Phone numbers in a post may be rejected if they cannot be tied to the business; use a "Call now" button instead.
- Arabic and RTL: Arabic business names and posts are possible; consistency rules still apply (see section 11).

## 4. Posting and cadence
- Official guidance on frequency: none found. Google says to keep info accurate and up to date. All of the following is heuristic (practitioner observation, not an official rule): 1-3 posts a week; Offers and Events need valid dates; reuse best photos.
- Because posts older than 6 months are archived, schedule evergreen "Update" posts for refresh every few months or give offers an end date.
- Timing: no official best time. Schedule to publish before opening hours or before known demand peaks (Cairo local time).
- Funnel mapping:
  - Awareness: photos and videos of storefront, products, team; seasonal updates; Updates tied to local events.
  - Consideration: Offers, menu or service updates, FAQ-style updates (since Q&A is gone), customer photo replies.
  - Conversion: action buttons (Call, Book, Order), WhatsApp/text link attribute, accurate hours and holiday hours.
  - Retention: replies to every review, review request link/QR, event posts.
- Review requests: Google allows asking customers via a Google review link or QR code (answer/3474122). It forbids incentives or gating (section 6).

## 5. Distribution and ranking signals
Official:
- Relevance (how well the profile matches the search), distance (from searcher), prominence/popularity. Verified status, complete and accurate information, reviews and replies, photos and videos are listed as improvement levers (answer/7091).
- Posts, photos and reviews can show to people in Search and Maps; Google reviews posts for policy and shows status.
- Impressions are counted once per user per day per surface (Performance API reference).
Practitioner observation, not an official rule:
- Review count, rating, recency, and keywords in reviews seem to correlate with local-pack rank.
- Primary category and accurate category choice are widely treated as the strongest controllable factor. Google's own guideline is to choose the fewest categories that describe the core business.
- Posts are not a confirmed ranking factor; they mainly influence conversion.

## 6. Community rules and policy hot spots
Sources: Guidelines for representing your business (3038177), Maps contribution policy (contributionpolicy/7400114), posts content policy (7213077), suspension help (4569145).
- Fake engagement and spam: fake, paid, incentivized or conflict-of-interest reviews are removed; reviews posted from multiple accounts by or for one person, emulator or device tampering, unusual patterns of review volume are prohibited. Competitor sabotage is prohibited.
- Review incentives: merchants must not offer payment, discounts or free goods or services for posting reviews, changing reviews or removing negative ones.
- Review gating: merchants must not "discourage or prohibit negative reviews, or selectively solicit positive reviews". They must not pressure customers to leave reviews on the premises, ask for specific content, or require staff to solicit a number of reviews or reviews naming a staff member. Asking all customers for honest reviews with no incentive is allowed.
- Impersonation and misrepresentation: do not misrepresent business name, address, category or affiliation; name stuffing risks suspension. One profile per business. Do not create a new profile for a suspended business.
- Copyright and music: photos and videos must be your own or licensed; music in videos should be cleared (general content policy; specific clause `unverified`).
- Regulated goods: posts must not carry calls to action, links, phone numbers or promotional offers for regulated products (alcohol, tobacco, pharmaceuticals, gambling, weapons, financial services among them). Incidental depictions such as a menu photo are allowed.
- Health, finance, politics: prohibited and restricted content policy covers misleading and dangerous content; GBP is not a venue for political persuasion or medical claims (details `unverified`).
- Hotels: cannot post Offer posts or mention deals or discounts.
- Minors: general Maps content policies apply; do not post identifiable minors without consent (`unverified` clause).
- Giveaways and contests: no GBP-specific contest policy found; do not tie a giveaway to leaving a review (that is a prohibited incentive).
- Automation and bots: the API policy allows only managing listings you own or are authorized to manage; Google may deactivate your project. Using bots to post reviews is fake engagement.
- Buying followers: not applicable; buying reviews is prohibited (above).
- Suspension and ownership: Google may suspend or disable profiles that break guidelines; owners can appeal once per decision via the appeals tool with evidence (business registration, licence, tax certificate, utility bill with matching name and address). An account-level restriction suspends all profiles you manage and blocks creating or claiming new ones. Ownership can be revoked for inactivity or when the business says you are no longer authorized.
- Triggers named or implied in the guidelines: ineligible business type or virtual office, remote mailbox address, name stuffing, service-area abuse, duplicate profiles, inaccurate information, policy-violating content, hijack or ownership conflicts.

## 7. Branded content, ads disclosure and legal
Not legal advice.
- GBP has no paid-partnership label; commercial content is the business's own. Offers and promotional posts are allowed in posts. They are not allowed in the business description or in the profile listing itself (time-bound promotions, pricing, direct calls to action).
- Sponsored or paid reviews are banned. A business that pays for reviews breaks Google's policy and, in many markets, consumer law.
- Consumer law, high level: undisclosed paid reviews and fake reviews are treated as unfair or deceptive practices in the EU, US (FTC rule on fake reviews) and under Egypt's Consumer Protection Law 181 of 2018 (details `unverified`).
- Respond to reviews without offering deals (Google advises to be conversational, not promotional).
- Privacy: do not share a reviewer's private information; Google bans soliciting personal or confidential information.
- If a review is defamatory or threatens, use Google's report tool first; legal removal notices are outside this file.

## 8. API and automation
- Official APIs: Google Business Profile APIs (developers.google.com/my-business). They are a family: Account Management, Business Information, Performance, Verifications, Lodging, Place Actions, Notifications, plus the legacy v4 My Business API still used for posts (`accounts.locations.localPosts`), reviews (`accounts.locations.reviews`) and media.
- Can: list and read reviews (including review media, reply state, policy violation status as added in 2026), reply to a review and delete a reply; create, edit and delete posts (Update, Event, Offer) with call-to-action buttons and recurrence (RecurrenceInfo added 2026-04-07); upload media; read daily performance metrics; manage locations, hours, attributes (including WhatsApp and text URL attributes), services, food menus, admins, verification and notifications.
- Cannot or no longer: Product posts cannot be created via the API; Q&A API was discontinued on 3 November 2025 (secondary source ppc.land, announced 17 September 2025; confirm against Google's developer notices); the chat/messages feature was removed (2024 per secondary source ppc.land) and the `BUSINESS_CONVERSATIONS` metric is marked deprecated in the official Performance API reference. There is no API to remove or report others' reviews; use the Reviews Management Tool (UI). An API to send replies to private messages: none.
- Auth: OAuth 2.0 (Google Account that manages the profile).
- Access: not open. Requirements: a Google Cloud project, an Organization account, a verified and active GBP of 60+ days (own or a client's), a website on that profile; submit the "Application for Basic API Access" via the GBP API contact form using an email that is owner or manager on the profile. A quota of 0 QPM means not approved; 300 QPM means approved (developers.google.com/my-business/content/prereqs).
- Rate limits (developers.google.com/my-business/content/limits): default 300 QPM for most APIs; Create Location 300 QPD; SearchGoogleLocation 300 QPD; Update Location 10,000 QPD; location edits 10 per minute per profile (cannot be increased). 429 on excess; pace evenly and back off with jitter.
- Policies: use only for listings you own or are authorized to manage; agencies must follow the third-party policies; Google may deactivate the project.
- Scheduling options: native in the UI (schedule and recurring posts); API-side scheduling of a future publish time: `unverified`, only recurrence info confirmed.
- Forbidden: bots posting reviews, review gating tools that filter who is asked, scraping profiles or review pages, bulk spam posts, bulk profile creation for ineligible businesses.
- n8n guidance: build a queue with a human-approved reply draft; never auto-post replies that quote private data; log `ReviewReplyState` and `PolicyViolation`; respect 300 QPM with a Wait node; use the Notifications API (Pub/Sub) for new reviews if available to your project rather than polling (`unverified` for review notification types); store OAuth credentials in n8n credentials.

## 9. Analytics
Where: the profile's Performance view in Search/Maps or Business Profile manager, and the Performance API. Definitions from the official DailyMetric reference:
- Business impressions on Google Maps and on Google Search, split desktop and mobile; multiple impressions by one user in a day count once.
- Direction requests (BUSINESS_DIRECTION_REQUESTS), call clicks, website clicks, messaging clicks (for example WhatsApp), bookings (Reserve with Google), food menu clicks (unique per user per day). Food orders and conversations are deprecated.
- Search keywords report exists in the UI/API (`unverified` on definition used here).
- Reviews: count, average rating, reply state; photo views (`unverified` in this file).
- Which metric answers which question: Is the profile found? Impressions. Are people choosing us? Call, website and direction clicks divided by impressions. Is a post worth it? Compare clicks before and after (post-level analytics beyond status: `unverified`). Is reputation healthy? Rating trend and unanswered reviews.

## 10. Cases
**Situation:** Calls and direction requests suddenly drop.
**Do:** Check the profile for suspension or "needs verification" notices; confirm hours, holiday hours, category and phone were not changed by suggested edits; check for a duplicate listing or hijack (look at owners/managers list); review recent photos and reviews.
**Avoid:** Re-creating the profile, buying reviews, changing the business name with keywords.

**Situation:** Profile suspended or disabled.
**Do:** Read the decision and violated policy in the appeals tool; fix the cause (name, address, ineligible content); submit one appeal with evidence whose name and address match the profile (registration, licence, tax certificate, utility bill); if the account is restricted appeal the account first from My accounts.
**Avoid:** Creating a new profile for the same business (Google says not to), submitting multiple appeals (only one per decision).

**Situation:** Negative review wave (real customers).
**Do:** Reply to each concisely and politely with an offer to continue by phone or email; fix the operational problem; encourage honest reviews from all satisfied customers with the review link or QR code; flag only reviews that violate policy.
**Avoid:** Arguing, revealing customer details, reporting reviews just because you disagree, offering money or discounts to remove or change a review.

**Situation:** Suspected fake or competitor reviews.
**Do:** Gather evidence (reviewer profile, timing, no matching customer); report each through the Reviews Management Tool and track status (can take several days); respond once publicly if it stays up.
**Avoid:** Posting fake positives to compensate; retaliating on the competitor's profile (prohibited).

**Situation:** Review gating or incentive temptation ("5 stars for a discount").
**Do:** Ask every customer the same way with the Google link or QR; train staff not to pressure or script content; send private feedback forms only as an additional option, not as a filter before the Google link.
**Avoid:** Routing only happy customers to Google, staff quotas, review-for-discount or review-for-removal deals.

**Situation:** Fake or duplicate listing or impersonator using the brand (or a "Google support" phone scam).
**Do:** Claim every location; use "Suggest an edit"/report on the duplicate; remove unknown owners and managers; keep ownership with a company-controlled account; ignore calls that offer paid help claiming to be Google (Google does not charge for this).
**Avoid:** Approving unknown manager requests, sharing verification codes by phone.

**Situation:** Cross-posting from Facebook or Instagram to GBP.
**Do:** Rewrite for GBP: remove hashtags and links to social handles, keep one clear action button, check the offer has dates, use a photo 720 px or larger, keep Arabic text short.
**Avoid:** Copying captions with phone numbers, unrelated links or social handles.

**Situation:** A post is wrong, outdated or rejected.
**Do:** Edit or delete it in Posts; for "Not approved" read the policy reference and resubmit a compliant version; remove phone numbers and use a Call button.
**Avoid:** Resubmitting the same text repeatedly.

**Situation:** Crisis (closure, safety incident, viral complaint).
**Do:** Update hours and add a short Update post; set temporary closure; keep the description free of promotions; reply to reviews factually; align with PR.
**Avoid:** Deleting profile, hiding behind generic replies, offering compensation in review replies.

**Situation:** Handing over access to an agency.
**Do:** Add the agency as manager (not owner), use an email alias for the owner, keep at least one company-held owner, remove ex-employee access, review access quarterly; for API access use an authorized third-party that follows Google's agency policy.
**Avoid:** Sharing the owner Google password, adding unknown requesters, letting an agency claim the profile in its own name.

## 11. Arabic and Egypt notes
- Business name: must match signage; for bilingual signage, using exactly what the sign shows is the rule. Whether to write Arabic only, English only or both in the name field: `unverified` beyond "match real-world signage"; do not add keywords, tagline or area names.
- Reviews and replies: reply in the reviewer's language (Arabic reply to Arabic review); keep it short, no promotions. Egyptian dialect is fine; avoid slang that could read as dismissive. Review translation behaviour: `unverified`.
- Address: use a precise address or service area; P.O. boxes and remote mailboxes are not accepted. Egypt-specific address formatting and landmark rules: `unverified`.
- Verification: methods are chosen by Google and cannot be changed; phone or text codes cannot be received by IVR systems, so use a number a person or SMS-capable device answers; live video is only within business hours; available options depend on region and business type. Video verification is recommended when offered.
- Hours: remember Friday and Eid/holiday hours; use special hours for holidays.
- WhatsApp is widely used by customers in Egypt (`unverified` as a statistic); GBP lets you add WhatsApp and text URL attributes via the API (and UI); use these instead of the removed chat (`unverified` for UI path in Egypt).
- Photos: show storefront signage in Arabic so customers can recognise the place; follow quality rules (no heavy filters).
- Payments for ads or Google Ads location links: `unverified`.

## 12. Pre-publish checklist
1. Is the post an Update, Offer or Event with the right type and dates?
2. Is the photo JPG or PNG, 10 KB to 5 MB, at least 250 px (720 px recommended), unfiltered and genuine?
3. Is any video up to 30 s, 75 MB, 720p or higher?
4. Is there one clear action button instead of a phone number, email or social handle in the text?
5. Are all links related to the business and safe?
6. Is the copy free of regulated-product offers (alcohol, tobacco, medicines, gambling, financial services)?
7. For hotels: does it avoid deals, discounts and offer posts?
8. Does the text avoid asking for reviews in exchange for anything and avoid review gating language?
9. Do business details (hours, holiday hours, address, category, name) match the real world and signage?
10. If it is a review reply: is it polite, short, free of private data and free of promotions?
11. Is the language the same as the audience (Arabic or English) and checked for typos?
12. Does a human approve any automated reply to a 1-3 star review?

## 13. Sources
- https://support.google.com/business/answer/7662907 (create and manage posts)
- https://support.google.com/business/answer/7213077 (photos, videos and posts content policy)
- https://support.google.com/business/answer/6103862 (photos and videos)
- https://support.google.com/business/answer/3038177 (guidelines for representing your business)
- https://support.google.com/business/answer/13763036 (eligibility and ownership)
- https://support.google.com/business/answer/4569145 (suspended or disabled profiles)
- https://support.google.com/business/answer/7107242 (verification)
- https://support.google.com/business/answer/3474050 (manage reviews)
- https://support.google.com/business/answer/3474122 (tips to get more reviews, reply tips)
- https://support.google.com/business/answer/4596773 (report reviews)
- https://support.google.com/business/answer/7091 (local ranking)
- https://support.google.com/business/answer/6270107 (supported countries)
- https://support.google.com/business/answer/14509283 (protect your profile)
- https://support.google.com/contributionpolicy/answer/7400114 (Maps prohibited and restricted content)
- https://developers.google.com/my-business/content/prereqs
- https://developers.google.com/my-business/content/limits
- https://developers.google.com/my-business/content/policies
- https://developers.google.com/my-business/content/latest-updates
- https://developers.google.com/my-business/content/posts-data
- https://developers.google.com/my-business/content/review-data
- https://developers.google.com/my-business/content/whatsapp-text
- https://developers.google.com/my-business/reference/performance/rest/v1/DailyMetric
- https://ppc.land/google-discontinues-business-profile-q-a-api-effective-november-3/ (secondary source, Q&A API)
- https://ppc.land/google-quietly-kills-q-a-for-an-ai-button-most-wont-use/ (secondary source, Q&A UI replaced)
