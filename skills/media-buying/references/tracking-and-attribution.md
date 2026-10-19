# Tracking and attribution
Purpose: define what must be measured before spend, how to keep the numbers trustworthy, and how to debug them when they disagree.
Last updated: 2026-10-19

Per-platform tag, server API, deduplication, windows and consent details are in `platforms/*.md` section 7; this file links to them instead of repeating values. Window lengths and rules change often: read the platform file's Last verified date and confirm in the live account. Nothing here is legal advice.

## 1. No spend until these are true (hard gate)
1. **One primary conversion defined** per campaign goal, with a business value (see `funnel-and-objectives.md` s1). Secondary events (view content, add to cart) are for observation and fallback optimization.
2. **Event fires once, at the right moment**: purchase on a confirmed order page (not on page reload), lead on successful submit (not on button click), message events on the chat start. Test with the platform's own tester (Meta Test Events, TikTok Pixel Helper, Google Tag Assistant / conversion diagnostics; names in each platform file s7).
3. **Value and currency passed** with purchase events; currency matches the account.
4. **Browser tag and server API both present** where the platform offers one (Meta Conversions API, TikTok Events API, Google enhanced conversions / Data Manager API, Snap and Pinterest Conversions APIs: see each file s7). Browser alone loses events to blockers, in-app browsers and consent choices.
5. **Deduplication configured**: the same event name plus the same event ID sent from browser and server. Rules and windows per platform in `meta-ads.md` s7 and `tiktok-ads.md` s7.
6. **Domain and ownership verified** in each platform (ownership of the domain/dataset), because several features and restrictions depend on it (`meta-ads.md` s2, s7; `policy-and-account-health.md` s5).
7. **Consent handled** for the audiences you serve: consent banner and consent signals where required (for example Google consent mode for EEA traffic in `google-ads.md` s7). A server API does not remove the consent requirement (`meta-ads.md` s7). Egypt and Gulf data-protection application to tags and uploads is `unverified`: ask the client's counsel (`mena-and-egypt-notes.md` s8).
8. **UTMs on every ad URL** (section 3) and consistent naming (`scripts/naming.py`).
9. **A CRM or sheet receives every lead/order** with source, campaign and timestamp, so the platform number can be reconciled (section 5, 6).
10. **Test conversion** performed end to end by a human: real click on a test ad link or tagged URL, then conversion, then check the event in the platform, GA4 and the CRM.

If any of 1, 2, 5 or 8 fails, the campaign does not launch (SKILL.md workflow step 3). If 4 or 7 cannot be done, launch only with the client's written acceptance of the measurement gap and a plan to close it.

## 2. Event design
| Funnel point | Typical event (names vary by platform; see s7 of each platform file) | Pass |
|---|---|---|
| Product/landing view | view content | content id, value |
| Interest | add to cart, initiate checkout | value, currency, items |
| Purchase | purchase | value, currency, order id |
| Lead | lead / submit form | lead id, value if modeled |
| Messaging | conversation started, qualified lead, order created/delivered | click ID, stage |
| Downstream quality | qualified, sale closed, delivered | same user keys, original click ID |

Rules:
- **Value for leads**: assign a modeled value (average sale value x close rate) per lead so value-based bidding becomes possible; label it as modeled in reports.
- **Order ID** as the dedup/reconciliation key on purchases and as the join key to the shop/ERP.
- **Match keys** (email, phone, click IDs): send what the platform accepts, normalized and hashed as its documentation says (hash rules per platform: `meta-ads.md` s7, `google-ads.md` s7). Never send raw personal data in URLs. Collect only with a lawful basis and a privacy policy on the page.
- **Do not change the optimization event during a peak** (Ramadan, White Friday): learning resets and comparisons break (`mena-and-egypt-notes.md` s7).
- Version the tracking plan: a one-page list of events, triggers, parameters and owner (`templates/launch-checklist.md` check 4).

## 3. UTM scheme
Use `scripts/utm_builder.py`; it lowercases, rejects non-ASCII (transliterate Arabic names), replaces spaces and underscores with hyphens, keeps existing query parameters.
```
python3 scripts/utm_builder.py https://shop.example.com/p --source facebook --medium paid-social --campaign ramadan-2027 --content reel-03 [--term broad] [--id adset-12]
```
| Parameter | Value rule | Example |
|---|---|---|
| utm_source | the platform | `facebook`, `instagram`, `tiktok`, `snapchat`, `google`, `youtube`, `linkedin`, `x`, `pinterest`, `telegram` |
| utm_medium | channel type, fixed list | `paid-social`, `cpc` (search), `paid-video`, `influencer`, `whatsapp-click` |
| utm_campaign | campaign slug matching the naming convention (campaign segment of `naming.py`, ASCII) | `ramadan-2027` |
| utm_content | ad/concept ID (concept_format_version) | `ugc-hook3-9x16-v2` |
| utm_term | ad set / audience (search: keyword) | `broad` |

- Existing platform files suggest `paid_social` with an underscore; `utm_builder.py` normalizes underscores to hyphens. Pick the hyphen form everywhere (the script's output) and keep the GA4 channel grouping rules in line with it. Whatever you choose, change nothing mid-campaign: one spelling per medium, because reports group on the exact string.
- Google Ads: keep auto-tagging (gclid) on; add UTMs only for non-Google reporting (`google-ads.md` s7).
- Prefer dynamic parameters where the platform supports them (Meta `{{campaign.name}}`, `{{ad.name}}`; TikTok macros; Google ValueTrack) so names match reports. Exact macro names are in the platform files and some are `unverified`: test one URL before applying to all ads.
- Never put personal data in a UTM. Never reuse a campaign slug for a different offer.
- Influencers, QR codes and WhatsApp: use a unique tagged link or code per creator/placement (`mena-and-egypt-notes.md` s9).

## 4. Attribution windows and why numbers disagree
The same sale appears with different counts in the ad platform, GA4 (or other analytics), the shop and the CRM. This is expected; the job is to know the gap and keep it stable.

| Source of difference | Mechanism | What to do |
|---|---|---|
| Window length | Platforms default to click windows of several days to 30 days, plus view-through/engaged-view (per-platform values in each file s7: `meta-ads.md` s7 attribution note, `google-ads.md` s7, `tiktok-ads.md` s7) | Compare at the same window; record the window in every report |
| View-through credit | Meta, TikTok and Google count some conversions after views or engagement without a click; analytics does not | Report click-only and total side by side |
| Attribution model | Platforms credit themselves (self-reporting); analytics uses its own model (GA4 default and lookback details `unverified` here: check the property settings) | Do not mix platform ROAS and analytics ROAS in one number |
| Counting date | Platform may date a conversion to the click/impression day, analytics to the conversion day | Align date basis before comparing periods; allow 3-7 days of lag |
| Sessions and consent | Analytics needs a session and consent; in-app browsers lose cookies; ad blockers drop tags | Server events, first-party IDs; accept analytics under-count |
| Cross-device/cross-platform | Platforms know logged-in users across devices; analytics often does not | Expect platform > analytics for social |
| Offline/COD events | Order placed vs cash collected | Three layers (section 6) |
| Duplicates | Double-fired events, missing dedup, thank-you page reloads | Section 8 |
| Modeled conversions | Platforms fill gaps for consent/privacy with modeling | Know the share; ask the platform report column definitions |

Reading rule (heuristic): platform-reported numbers are for optimization inside the platform; the business source of truth (shop/ERP/CRM delivered orders, bank) is for decisions about money; analytics is the cross-channel referee for click-based traffic. When the ratio platform/CRM stays stable week to week, the platform is directionally usable; when it jumps, suspect tracking before suspecting performance.

Track a **reconciliation ratio** weekly: CRM (confirmed) orders attributable to paid / platform-reported conversions. Keep it in the weekly report (`templates/weekly-report.md`).

## 5. Lead quality loop (offline conversion import / CRM feedback)
Goal: teach the platform which leads become customers, so it finds more of them.
1. Capture the **click ID** at submit time (gclid, `fbc`/`fbclid`, `ttclid`, `ctwa_clid`, `lead_id`, etc.; names per platform file s7) in a hidden form field or the chat metadata and store it in the CRM.
2. Define lead stages: new, contacted, qualified, proposal/quote, won, lost (with a reason). Agree on "qualified" in writing with sales.
3. Send stage events back: Google offline conversion import by click ID or enhanced conversions for leads (the Data Manager API is the route for new Google integrations: `google-ads.md` s7); Meta via the Conversions API with the lead or click ID (messaging variant in `meta-ads.md` s7); TikTok Events API offline; others per file.
4. Delay and batch: send within the platform's allowed age for events (Meta allows events up to 7 days old; see `meta-ads.md` s7), daily or hourly. Late events outside the window are rejected.
5. Optimize on the qualified event only when it has enough volume; until then optimize on lead and report qualified rate by campaign and creative as a manual quality check.
6. Close the loop in reporting: cost per qualified lead and cost per sale by campaign/creative/audience (`reporting.md`).
- WhatsApp: the same idea with message stages (`meta-ads.md` s7 and s12, `mena-and-egypt-notes.md` s5). Meta does not deduplicate messaging events, so send each stage once.
- Privacy: send only what the platform documents, hashed where required, with consent and a privacy policy; check local law for customer-list uploads (`mena-and-egypt-notes.md` s8).

## 6. COD and delivered-order reconciliation
Platforms count orders when placed. Money arrives at delivery. Build three layers (`mena-and-egypt-notes.md` s6):
| Layer | Source | Use |
|---|---|---|
| Placed | pixel/API | platform optimization, platform CPA |
| Confirmed | call/WhatsApp confirmation in CRM | quality check, optimization event once volume allows |
| Delivered/collected | courier settlement | profit, break-even comparison |
- Math: `ads_math.py cod --orders N --delivered-rate R --aov V --spend S` for real ROAS and CPA per delivered order; `ads_math.py breakeven --cod-delivery-rate R --return-rate X` for the target. Use order-date cohorts with a lag (settlement takes days to weeks); never compare a fresh cohort's delivered rate with an old one.
- Keep returned-parcel shipping cost in `--other-var` or adjust the delivery rate down; the script does not model it separately.
- Send confirmed/delivered orders as the server event when volume allows (a separate event, optimized once it has enough volume).
- Reconcile weekly: platform orders vs shop orders vs confirmed vs delivered; log gaps and causes (fake orders, duplicates, unreachable numbers).

## 7. Privacy constraints (high level)
- Consent: collect before firing marketing tags where law or platform policy requires; honor opt-outs; store consent state (EEA/UK consent mode in `google-ads.md` s7; EU/UK pixel consent in `meta-ads.md` s7).
- Data minimization: no health, financial or ID data in events, URLs or lead forms unless the platform explicitly allows it (TikTok lead-form restriction in `tiktok-ads.md` s8; Meta personal-attribute rule in `meta-ads.md` s8).
- Hashing and PII: hash identifiers as documented; never log raw emails/phones in analytics or chat; keep API tokens in a secret manager, never in prompts or repos (`meta-ads.md` s11).
- Egypt personal data protection law (Law 151 of 2020) and Gulf laws: application to pixels and uploads `unverified`; recommend counsel review (`mena-and-egypt-notes.md` s8).
- Platform restrictions: some categories (health, finance) have limited optimization events and audience features; check the platform policy sections (`policy-and-account-health.md`).

## 8. QA checklist (before spend, and after any site change)
- [ ] Each primary event fires once per conversion (reload the thank-you page: still once).
- [ ] Event value/currency correct; order ID present.
- [ ] Browser and server events deduplicate (event count in the platform is not double the browser count; the "deduplicated" or match-quality indicator is healthy in the platform file's tester).
- [ ] Test event code or test mode removed from production calls (`meta-ads.md` s7).
- [ ] Click ID captured to the CRM.
- [ ] UTMs resolve, survive redirects and the checkout, and appear in analytics.
- [ ] Consent banner behavior tested with consent granted and denied.
- [ ] Mobile and in-app browser path tested (Instagram, TikTok, Facebook in-app browsers).
- [ ] Platform vs shop vs CRM counts for a test day within the expected gap.
- [ ] Owner, date and tracking plan stored.

## 9. Debugging tree
**A. Conversions not tracked (platform shows zero or far too few)**
1. Is the tag/pixel present on the conversion page? (tag helper/tester)
2. Does the event fire at all? If not: trigger wrong (button vs success), tag manager not published, consent blocking, ad blocker, checkout on another domain/iframe.
3. Fires but not received: wrong dataset/pixel ID, server API errors (batch rejected for one bad event, timestamp too old; see `meta-ads.md` s7), blocked by the CMP, test event code left on.
4. Received but not attributed: no click/ID match, window too short, event outside the attribution window, ad click traffic opening in an in-app browser that drops cookies, user converted on another device.
5. Attributed but invisible in the report column: wrong attribution setting selected, reporting delay (Google conversion lag, X spend lag in `x-ads.md` s5), wrong date range or column.
6. Fix, retest end to end, log in the change log.

**B. Conversions double counted (platform > shop)**
1. Pixel installed twice (theme plus tag manager plus app).
2. Browser + server without a shared event ID or with different event names.
3. Thank-you page reload/back button/refresh; fire once per order ID.
4. Two conversion actions both set as primary for the same sale (Google); duplicate primary goals.
5. Platform counts view-through; shop counts clicks only: compare click-only.
6. Test orders and internal traffic not excluded.

**C. Conversions dropped (sudden fall)**
1. Compare the platform's event count to the shop's orders for the last 14 days: did the drop start the same day on both? If shop is stable and platform dropped, it's tracking.
2. What changed on that day: site release, theme/plugin update, checkout change, new consent banner, CDN, domain, payment gateway redirect.
3. Server API: token expired, endpoint version unsupported, rate limit or schema error (`meta-ads.md` s11).
4. Platform side: pixel/dataset permissions removed, domain verification lost, policy action.
5. If shop also dropped: this is demand, price, stock or delivery, not tracking; go to `optimization-playbook.md`.
6. If only the paid-attributed share dropped: attribution setting or window changed (Meta changed attribution in March 2026 per `meta-ads.md` s7); do not compare across the change.

**D. Platform and analytics differ by a stable ratio**: normal; document the ratio. **Differ by a changing ratio**: go to A/B/C.

## 10. Operating rules
- One person owns the tracking plan; changes go through the change log (`optimization-playbook.md` s7).
- Re-run section 8 after every theme, checkout, consent-tool or domain change, and before every seasonal peak.
- Never "fix" a bad number by editing the report; fix the source or label the number as estimated.
- Do not request or paste access tokens or passwords in chat; use partner/role access and a secret manager (`policy-and-account-health.md` s6).

## Sources
- Platform files (each carries its own dated sources): `platforms/meta-ads.md` s7, `platforms/google-ads.md` s7, `platforms/tiktok-ads.md` s7 and the tracking sections of the other platform files.
- `mena-and-egypt-notes.md` s5, s6, s8.
- GA4 lookback windows, attribution defaults and reporting-column definitions were not verified in this pass (web search unavailable on 2026-10-19). Check the property's Admin > Attribution settings and Google's current help pages before stating any GA4 number.
