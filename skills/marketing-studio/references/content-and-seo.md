# Content and SEO

Purpose: build a content system that serves the strategy, and cover the SEO basics that stay stable, including local SEO in Egypt and Arabic-specific points.
Last updated: 2026-10-19

Platform execution (captions, posting, replies, limits) belongs to `social-media-manager`. Video scripts: `reels-studio`. Visuals: `creative-studio`. Voice: `brand-voice.md`.

## 1. Content system
**Pillars (3 to 5)**: recurring topics that connect audience needs to your offer. Each pillar serves a funnel stage (awareness, consideration, conversion, retention; see `funnel-and-channels.md`, section 2) and a pillar in the messaging house. Example pillars for a bag maker: craftsmanship, styling for work, care and repair, customer stories, offers.
**Formats**: choose by job.
| Job | Formats |
|---|---|
| Be found (search) | Guides, comparison pages, FAQ, service/location pages, GBP posts |
| Be noticed (feeds) | Short video, carousels, stories, live Q&A |
| Build trust | Case studies, reviews, behind-the-scenes, expert explainers |
| Convert | Product/service pages, offer pages, WhatsApp scripts, demo videos |
| Retain | How-to, onboarding, newsletters, community |
**Calendar**: a monthly view with date, pillar, format, channel, owner, status, call to action and metric. Use the `social-media-manager` calendar template for social and keep a separate editorial calendar for long-form content. Build around real dates (Ramadan, Eid, back to school, White Friday, see `../../media-buying/references/mena-and-egypt-notes.md`, section 7) and around product/stock calendar.
**Repurposing**: one hub asset becomes many pieces. Example: a 20-minute interview or workshop session becomes one article, 5 short clips, 3 quote cards, one email, 10 FAQ answers for WhatsApp. Adapt per platform; never paste the same file everywhere unchanged.
**Editorial workflow** (small team): brief (audience, intent, claim, source list, CTA) -> draft -> fact and claim check -> voice check (`brand-voice.md`, section 6) -> design -> approval -> publish -> measure at 7 and 30 days -> update or retire. Each step has one named owner and a status. Nothing is published without approval from the owner of the account.
**Capacity rule**: plan only what the team can produce for 12 weeks at normal pace; consistency beats bursts. Keep a bank of evergreen pieces for slow weeks.

## 2. SEO basics that are stable
Source for principles: Google Search Central (see Sources). Details change; core ideas have been stable.
- **Search intent**: classify each target query as informational, navigational, commercial investigation or transactional (or local). Make the page type match the intent: guides for questions, comparison for "best/vs", product/service pages for buying, location pages for "near me" style queries. Look at what currently ranks to infer intent.
- **Topic clusters**: one pillar page covering a topic well, plus supporting pages for specific questions, all linked to each other with descriptive anchor text. Plan clusters around your offer, not around volume alone.
- **On-page**: one clear topic per page; descriptive title and heading that match the query and the content (no exaggeration); helpful first paragraph; scannable structure; original images with descriptive alt text; clear CTA; visible author/business info; no keyword stuffing.
- **Technical checklist**: pages crawlable and indexable (robots.txt and noindex reviewed); HTTPS; mobile friendly; fast on real devices; XML sitemap submitted in Search Console; canonical tags on duplicate or parameter URLs; clean URLs; no broken links or redirect chains; structured data only where it matches visible content and validates; hreflang for multi-language (section 7).
- **Core Web Vitals** (web.dev thresholds, measured at the 75th percentile of page loads): LCP within 2.5 seconds, INP 200 milliseconds or less, CLS 0.1 or less.
- **Internal links**: every important page reachable in a few clicks from home and from related pages; use descriptive anchors; link new content from existing high-traffic pages; fix orphan pages.
- **Trust signals (E-E-A-T style)**: show real experience and expertise: author or business page, credentials where relevant, sourcing, first-hand photos and results, clear contact info, policies (returns, privacy), reviews, and a consistent business identity. Google's guidance asks content to show first-hand expertise and to be reliable and people-first; E-E-A-T is a framework for quality evaluation, not a switch you can turn on. Do not fake credentials.
- **Measurement**: Search Console (queries, pages, indexing), analytics, and conversions (calls, WhatsApp clicks, form submits). See `measurement.md`.
- **Expectations**: SEO is slow and uncertain; set review points at 90 and 180 days and judge by qualified traffic and conversions, not rank of one keyword. Avoid "guaranteed first page" promises from vendors.

## 3. Keyword and topic research workflow
1. List seed topics from customer questions (WhatsApp chats, calls, reviews, competitor FAQs).
2. Expand with autocomplete, related searches, "people also ask", Search Console queries, and keyword tools; record volume as a rough signal only, since tool volumes are estimates and Arabic coverage varies by tool.
3. Group by intent and by page; one primary query per page, plus close variants.
4. Prioritise by business value x ease x fit with a page you can make better than what ranks (use the competitor gap method in `competitor-research.md`, section 7).
5. Brief the writer with intent, outline, sources, internal links, CTA and the evidence required.

## 4. Content measurement
- Leading: publish rate, indexing, impressions and clicks (Search Console), watch time/saves/shares for social, replies/DM/WhatsApp starts.
- Lagging: leads, orders, calls, direction requests (GBP), revenue by source, assisted conversions.
- Quality: return visits, scroll/read depth, branded search growth.
- Content-level decisions at 30/90 days: keep, update, merge, redirect or remove. Record the change and the hypothesis.
- Tag all links with UTM (the `social-media-manager` has `scripts/utm.py`) and use WhatsApp source tags so social and content show up in reports.

## 5. AI-generated content risks and quality control
Google's published guidance (Search Central) says generative AI can help research and structure, but using it to generate many pages without adding value for users may violate its spam policy on scaled content abuse; creators should fact-check AI output, including titles, meta descriptions, structured data and alt text, and consider telling readers how content was created. Merchant Center has its own AI-content policies for product data and images.
Quality-control rules:
1. Human subject-matter owner for every published claim; AI never sole author on health, legal, finance or safety topics.
2. Fact-check numbers, names, prices, dates and quotes against a source; keep the source list with the draft.
3. Add original value: your data, photos, processes, examples, expert comments; if a page could be written by anyone, it will rank like it.
4. Voice and dialect check by a native speaker (`brand-voice.md`); machine Arabic often drifts to formal MSA or odd phrasing.
5. No fake reviews, testimonials, experts or case studies generated by AI.
6. Disclose AI use where the platform or law requires it (see `social-media-manager` compliance file) and for AI-generated images in product feeds per Merchant Center metadata rules.
7. Limit throughput: publishing volume should follow review capacity, not model speed.
8. Keep an audit sample: review 10 percent of published AI-assisted pieces each month for errors and sameness.

## 6. Local SEO for Egypt (Google Business Profile first)
For businesses with a place or a service area, the profile is the storefront in Search and Maps. Rules below come from the `social-media-manager` GBP file (sourced to Google help pages); read it for details.
- **Eligibility and identity**: real address or service area; no P.O. boxes or remote mailboxes; one profile per business; business name must match real-world signage (no keywords, taglines or locations added).
- **Verification**: Google chooses the method (phone, text, video); use a number a person or SMS-capable device answers; video verification only in business hours.
- **Ranking levers named by Google**: relevance, distance and prominence; complete and accurate information, verified status, reviews with replies, photos and videos. Primary category choice and review recency are widely treated as strong signals (practitioner observation, not an official rule).
- **Completeness**: categories (fewest that describe the core business), hours including Friday and Eid/holiday special hours, services/products, photos of the storefront with Arabic signage, phone, website, appointment/order links, WhatsApp link via supported attributes (`unverified` for the Egypt UI path).
- **Reviews**: ask every customer for honest reviews with no incentive and no selection; reply to all in the reviewer's language, short, no promotions; Google prohibits paying or discounting for reviews, review gating and fake reviews.
- **Posts**: offers, events and updates; they influence conversion more than rank (practitioner observation).
- **Consistency**: same name, address, phone across site, Facebook, Instagram and directories; add local landmarks in the page copy for clarity, not in the GBP name.
- **Site support**: location/service pages with unique content, embedded map, local phone and WhatsApp, local business structured data that matches the visible information.
- **Measure**: calls, direction requests, website clicks, messages, and review count and rating (Google's Performance data in the profile).

## 7. Arabic SEO specifics
- **Dialect vs MSA**: people often search in a mix. Egyptian users may type dialect spellings, MSA terms, English or Arabizi (Arabic written in Latin letters). Do research in each variety and build one page per intent, written in the register of the audience: dialect or plain MSA for consumer pages, MSA for formal and technical pages. Check the Search Console query report and the Google Ads search terms report for the real variants (`unverified` tool coverage; verify in the tool).
- **Spelling normalisation**: variants such as ة/ه, أ/إ/ا, ى/ي are common in queries; include natural variants in headings and body, but do not stuff.
- **Hreflang** (Google Search Central): use it to tell Google which language/region version a page has. Each version must list itself and all other versions; return links are required or tags are ignored; use fully-qualified URLs; codes are ISO 639-1 language plus optional ISO 3166-1 alpha-2 region, such as `ar-EG` and `en-EG`; add `x-default` as a fallback. Google does not use hreflang or the HTML lang attribute to detect language. Use only one method (HTML tags, HTTP headers or sitemap).
- **RTL**: set `dir="rtl"` and `lang="ar"` on Arabic pages; mirror layout; test mixed-direction text (Latin brand names, numbers, URLs); check fonts render connected letters; keep URLs clean (Latin slugs or percent-encoded Arabic are both possible; pick one and stay consistent, `unverified` effect on ranking).
- **Titles and snippets**: Arabic title length displays differently; preview in Search Console and on mobile.
- **Duplicate and thin pages**: do not auto-translate whole sites; machine-translated, unreviewed pages risk quality and scaled-content problems.
- **Local intent**: include city and district names that people actually use (for example Nasr City, Maadi, 6th of October) in service pages where truthful.

## 8. Handoffs
Social publishing and platform rules: `social-media-manager`. Reels and ad video scripts: `reels-studio`. Blog or landing visuals: `creative-studio`. Paid search: `media-buying` (Google Ads). Automating briefs or reports: `automation-studio` / `n8n-agent-studio`. Always pass: audience, intent, pillar, claim, proof, CTA, tracking link, deadline, approver.

## 9. Tools: content brief and 30-minute SEO check
**Content brief fields**: working title; audience and the job; search intent and primary query (plus variants in Arabic, English, Arabizi if relevant); funnel stage; one-sentence claim; outline (H2/H3); evidence and sources required; original asset to include (photo, data, quote); internal links to add and from where; CTA and tracked link; word and tone guide (`brand-voice.md`); reviewer; publish and review dates.
**30-minute SEO check for a small site**
1. Search `site:yourdomain.com` and confirm the important pages are indexed; open Search Console and read the Pages report for exclusions and errors.
2. Check each key page has one clear topic, a descriptive title and heading, and that titles are not duplicated.
3. Test mobile speed on a real mid-range phone and the Core Web Vitals report; fix the biggest image or script first.
4. Confirm the site uses HTTPS, has no broken links on key paths, and has a sitemap submitted.
5. Search the 10 queries customers use (Arabic and English) from the target city: who ranks, what format, is there a map pack.
6. Open the Google Business Profile: category, hours, photos, reviews and replies, links, WhatsApp/booking link.
7. Check the contact, about, shipping and returns pages exist and match across channels.
8. Write the top 3 fixes with owners and dates; re-check in 30 days.

## Sources (accessed 2026-10-19)
- https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://web.dev/articles/vitals (Core Web Vitals thresholds)
- Google Business Profile help pages as recorded in `../../social-media-manager/references/platforms/google-business-profile.md` (answer/7091, 3038177, 7107242, 3474050)
- Not verified this session: tool-specific Arabic keyword volume coverage; WhatsApp attribute availability in Egypt.
