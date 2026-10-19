# Funnel and channels

Purpose: model how customers move from stranger to repeat buyer, score channels honestly, split budget by evidence, and know the Egypt channel realities.
Last updated: 2026-10-19

Pairs with `templates/channel-scorecard.md`. Execution lives in `social-media-manager` (organic), `media-buying` (paid), `reels-studio` (video scripts), `creative-studio` (visuals) and `automation-studio` / `n8n-agent-studio` (workflows).

## 1. Funnel models: pick the simplest one that fits
| Model | Stages | Use when |
|---|---|---|
| Simple 4-stage | Awareness, consideration, conversion, retention | Default for small businesses and most plans |
| AARRR ("pirate") | Acquisition, activation, retention, referral, revenue | Apps, subscriptions, SaaS, anything with an in-product "aha" moment |
| Flywheel | Attract, engage, delight; customers feed growth through reviews, referrals, content | Service/local/community businesses where word of mouth is the main engine |
| Sales pipeline | Lead, qualified lead, meeting, proposal, win | B2B and high-ticket services |
Notes:
- A funnel is a model, not reality. People loop, jump and ask friends on WhatsApp; use it to find the weakest step, not to describe every path.
- Define each stage by an observable event you can count (for example: awareness = reached/visited; consideration = viewed product, started chat; conversion = paid/confirmed/delivered; retention = second purchase in N days).
- Find the **bottleneck stage** first (largest drop vs. what you can fix). Fixing conversion before buying more traffic is usually cheaper (heuristic). In COD businesses add "confirmed" and "delivered" as stages (see `measurement.md`, section 3).

## 2. What each stage needs
| Stage | Customer question | Best-fit assets | Typical channels | Main metric |
|---|---|---|---|---|
| Awareness | "Does this exist / is it for me?" | Short video, problem-led posts, search content, creators | Social video, SEO, partnerships | Qualified reach, branded searches |
| Consideration | "Is it good, is it trustworthy, how does it compare?" | Reviews, comparisons, FAQ, demos, WhatsApp chat | GBP, site, social proof, retargeting | Chats started, product page depth |
| Conversion | "What do I do and what if it goes wrong?" | Clear offer, price, delivery, risk reversal, fast reply | WhatsApp, site, marketplace listing, search ads | Confirmed orders/bookings, conversion rate |
| Retention | "Was it worth it, what next?" | Onboarding/aftercare, reorder prompts, referrals, community | WhatsApp (opt-in), email, loyalty | Repeat rate, referral rate |

## 3. Channel scorecard
Score each candidate channel 1 to 5 on seven criteria (details and sheet in `templates/channel-scorecard.md`). Weight criteria to the goal (a launch weights speed; a mature brand weights control).
| Criterion | Question | Evidence source |
|---|---|---|
| Audience fit | Is our primary segment there in volume, in the language we use? | Customer interviews, platform audience tools, `competitor-research.md` |
| Intent | Are people ready to buy or just browsing? | Search vs. feed; chat starts |
| Cost | Cash cost per useful outcome we can afford against allowable CPA | Own history, small test |
| Speed | Time to first signal | Test duration |
| Control | Do we own the audience and rules (email list vs. platform reach)? | Policy, algorithm dependence |
| Measurability | Can we count outcomes down to delivered revenue? | Tracking setup |
| Team skill | Can we produce and operate it well weekly? | Hours and skills |
Decision rule (heuristic): choose channels with weighted score at or above your threshold, cap at three active channels per quarter, and keep any with a fatal 1 (for example no way to measure, or no capacity) on the "not now" list.

## 4. Owned, earned, paid mix
- **Owned**: website, blog, email list, WhatsApp opt-in contacts, Google Business Profile, product pages, packaging. Slow to build, cheapest long term, you control it.
- **Earned**: reviews, word of mouth, press, creator mentions, communities, referrals. Cannot be bought honestly; can be encouraged by being worth mentioning and by asking all customers in a compliant way (GBP bans review incentives and selective solicitation: see `../../social-media-manager/references/platforms/google-business-profile.md`, section 6).
- **Paid**: ads, sponsored creators, marketplaces' sponsored listings. Fast, scalable, stops when you stop paying.
Mix heuristics (labelled as such):
- New business with no demand: lean on paid for speed plus owned for capture; set up WhatsApp and GBP first so paid traffic has somewhere to land.
- Local business with existing intent: owned and earned first (GBP, reviews, WhatsApp), paid for gaps.
- Established brand: invest in owned (email/WhatsApp, content) so reach is not rented.
- Never let one paid platform be the only source of customers; a single account restriction should not stop the business.

## 5. Budget allocation heuristics (not benchmarks)
These are starting rules; replace with your own data after 4 to 8 weeks.
1. Compute allowable CPA from margin (and delivery rate for COD) before assigning media budget (`measurement.md`, section 7; `media-buying` break-even tools).
2. Fund operations first (reply speed, content production, tracking), then media.
3. Test budget: 10 to 20 percent of total in the first quarter for channels with no history; reserve some for creative refresh.
4. After the test, shift budget toward channels with delivered-revenue payback inside your time limit and away from channels that miss the threshold twice.
5. Retention (email/WhatsApp, aftercare) is often cheaper per sale than acquisition; give it a visible slice once there are repeat-eligible customers.
6. Cap spend growth steps (see `media-buying` optimization playbook) and avoid changing several variables at once.
7. Seasonal peaks (Ramadan, White Friday): plan 8 to 10 weeks ahead per `../../media-buying/references/mena-and-egypt-notes.md`, section 7.

## 6. Channel playbooks (one paragraph each, then hand off)
- **Organic social**: build recognisable pillars, consistent formats and a reply routine; use it for trust and demand creation, not for guaranteed sales. Hand off to `social-media-manager` (platform rules, calendar, replies).
- **Paid social/search**: use when the offer converts organically or when you must create volume; require verified tracking and allowable CPA first. Hand off to `media-buying`.
- **Search/SEO**: captures existing demand and compounds; slow; see `content-and-seo.md`.
- **Google Business Profile**: the storefront in Search and Maps for any business customers visit or that serves an area; see `content-and-seo.md`, section 6, and the `social-media-manager` GBP file.
- **WhatsApp**: the conversion and service channel in Egypt; consent-based marketing, templates, fast replies; see `email-and-whatsapp.md`.
- **Email**: owned retention and nurture channel; deliverability rules in `email-and-whatsapp.md`.
- **Creators/influencers**: borrowed trust; vet audience and disclosure; see `../../media-buying/references/mena-and-egypt-notes.md`, section 9.
- **Partnerships/referrals**: cross-promotions with complementary businesses; track with codes; cheapest honest earned growth for local businesses.
- **Marketplaces**: demand and trust you rent; fees and rules apply; good for discovery and for products with comparison shopping; weak on brand control and customer data.
- **Events/offline**: shop signage, QR codes, flyers, sampling; connect every offline touch to a trackable action (WhatsApp link, QR with source tag).

## 7. Egypt channel realities (sourced facts only)
Facts (DataReportal Digital 2026: Egypt, reports Kepios analysis of platform ad-reach data, not monthly active users; numbers may be revised):
- 98.2 million internet users in October 2025 (82.7 percent of the population); 51.6 million social media user identities (43.4 percent); 121 million cellular mobile connections (102 percent).
- Platform ad reach, late 2025: Facebook 51.6M, YouTube 49.3M, TikTok 48.8M (18+ only), Messenger 37.0M, Instagram 21.7M. Source: https://datareportal.com/reports/digital-2026-egypt
- DataReportal's Egypt table did not list WhatsApp. A vendor guide claims about 52 million WhatsApp monthly users in Egypt; that is third-party and unsourced, so treat WhatsApp reach as indicative only (see `../../social-media-manager/references/platforms/whatsapp.md`, section 1).
- Marketplaces: Jumia lists Egypt among its first expansion countries after Nigeria (Wikipedia, Jumia); Souq.com Egypt was rebranded as Amazon.eg on 1 September 2021 (Wikipedia, Souq). Seller terms, fees and current market share were not verified: check each marketplace's seller page.
- TikTok Ads for Egypt accepts EGP payments by bank card or Fawry (TikTok help page, via `../../media-buying/references/mena-and-egypt-notes.md`, section 1). Meta and Google local payment methods for Egypt are `unverified` there.
- Egypt Personal Data Protection Law No. 151 of 2020 requires explicit consent for direct electronic marketing, an easy opt-out and consent records (DLA Piper summary, recorded in the WhatsApp file, section 7). Not legal advice.
Practitioner observations (not sourced numbers):
- **WhatsApp**: many buyers prefer to chat before buying; plan it as the checkout. Measure first-reply time and confirmation rate.
- **Facebook**: broad mass-market reach, Pages, Groups and Messenger remain important for local commerce and older audiences.
- **Instagram**: product discovery and brand building for fashion, food, beauty, lifestyle; smaller reach than Facebook in the table above.
- **TikTok**: large reach and entertainment-led discovery; short video capacity required; ads support local payment options for billing.
- **Google Business Profile and Search**: intent-rich for local services (clinics, restaurants, repairs, schools); see `content-and-seo.md`.
- **Marketplaces**: price comparison is easy; compete on delivery reliability, reviews and bundles; keep your own WhatsApp/site path for repeat customers where the marketplace rules allow.
- **Cash on delivery**: report confirmed and delivered revenue; see `../../media-buying/references/mena-and-egypt-notes.md`, section 6.
- Friday is the weekly day off and Ramadan changes evening activity; plan post times from the account's own insights.

## 8. Channel decision output
Produce a table: channel, role in funnel, score, monthly budget (money and hours), owner, KPI, review date, and the next test. Add the "not now" list with revisit dates. Hand each chosen channel a brief using the intake checklist in the target skill so nothing is re-asked.

## Sources (accessed 2026-10-19)
- https://datareportal.com/reports/digital-2026-egypt
- https://en.wikipedia.org/wiki/Jumia
- https://en.wikipedia.org/wiki/Souq_(company)
- https://ads.tiktok.com/help/article/europe-middle-east-and-africa-emea-supported-payment-methods (as recorded in the media-buying Egypt notes)
- https://www.dlapiperdataprotection.com/index.html?t=law&c=EG (as recorded in the WhatsApp file)
- Internal: `../../media-buying/references/mena-and-egypt-notes.md`, `../../social-media-manager/references/platforms/whatsapp.md`, `../../social-media-manager/references/platforms/google-business-profile.md`
