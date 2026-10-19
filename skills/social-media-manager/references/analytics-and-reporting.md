# Analytics and reporting
Purpose: choose KPIs per goal, define metrics consistently, report weekly and monthly, test ideas fairly, track links, and write insight instead of description.
Last updated: 2026-10-19

Metric names, availability and retention change often and differ per platform: always read section 9 of `platforms/<slug>.md` before building a dashboard, and say which definition you used in the report. Do not invent metric definitions; if a platform file marks one `unverified`, report the metric name as the platform shows it and flag it.

## 1. KPI tree by goal
Primary KPI first, then drivers, then diagnostics. Report the primary KPI in every report.
| Goal | Primary KPI | Drivers (what moves it) | Diagnostics (why) |
|---|---|---|---|
| Awareness | reach or views from non-followers | posting volume of discovery formats, shares, collaborations | hook retention, watch time, skip rate, share rate |
| Engagement | engagements per 1,000 reach (comments + shares + saves weighted over likes) | question posts, series, UGC, replies | comment quality (manual sample), return commenters |
| Traffic | tracked clicks and landing sessions from social | link placement, CTA clarity, audience fit | click-through per reach, bounce, page speed |
| Leads | leads (form fills, DM conversations opened, WhatsApp starts) | offer, CTA, response time | qualified rate, time to first reply |
| Sales | orders and revenue attributed (with attribution caveats, section 5) | proof, offers, remarketing handled elsewhere | conversion rate on landing page, average order value |
| Support | first-reply time and resolved rate | staffing, templates, FAQ posts | repeat contacts, sentiment, review rating |
Keep to 3 to 5 KPIs per account per month (SKILL.md report format).

## 2. Metric definitions (common)
Use these definitions in reports; note platform differences in section 3.
| Metric | Common definition | Watch out |
|---|---|---|
| Reach | unique accounts that saw the content | estimated; some platforms count only organic; platform-specific |
| Impressions/views | times content was shown or played | platforms renamed these (see section 3); not comparable across platforms |
| Engagement | sum of reactions, comments, shares, saves (define the list) | do not mix with clicks unless stated |
| Engagement rate | engagements / reach (preferred) or / followers | state the denominator; reach-based is comparable across audience sizes |
| Video view | platform-defined play threshold | thresholds differ and have changed (`platforms/youtube.md` section 1) |
| Watch time / average view duration | total or mean time played | compare to video length: retention % |
| Retention | share of viewers remaining at points in the video | needs enough views |
| Click-through rate | clicks / impressions (or reach) | state denominator |
| Follower growth | net follows in the period | separate organic growth from campaign spikes |
| Saves, shares | strong intent signals | shares by DM may be invisible in public counts |
| Response time | time from customer message to first human reply | business hours only; use medians |
| Conversion | defined action / sessions or / clicks | define the action once |
Use medians for per-post metrics (a viral post distorts averages) and show percentiles when comparing.

## 3. Where platforms differ (read section 9 of each file)
| Platform | Notable differences |
|---|---|
| Instagram | `views` replaces `impressions` for media created after 2024-07-02; Story metrics available only 24 h; insights lag up to 48 h (`platforms/instagram.md` section 9) |
| Facebook | impressions metrics were migrated to `*_media_view` and follows metrics changed in 2025 (`platforms/facebook.md` section 9) |
| TikTok | definitions not readable; use TikTok Studio names and flag them (`platforms/tiktok.md` section 9) |
| YouTube | view counting rules changed in 2025 and 2026; Shorts "engaged views" vs views (`platforms/youtube.md` sections 1 and 9) |
| LinkedIn | impressions vs unique impressions; engagement formula in the API; 12-month window (`platforms/linkedin.md` section 9) |
| X | public vs non-public vs organic metrics, owner metrics only last 30 days; each API read costs money (`platforms/x-twitter.md` section 9) |
| Threads | views and shares marked in development; demographics need 100+ followers (`platforms/threads.md` section 9) |
| WhatsApp | delivered/read counts and template quality; cost per delivered message (`platforms/whatsapp.md` section 9) |
| Telegram | channel stats only above a server threshold; MTProto not Bot API (`platforms/telegram.md` section 9) |
| Pinterest | saves, outbound clicks; real-time numbers are estimates (`platforms/pinterest.md` section 9) |
| Snapchat | UI and API numbers may differ until synced (`platforms/snapchat.md` section 9) |
| Reddit | score, comments, views; karma is not a KPI (`platforms/reddit.md` section 9) |
| Google Business Profile | impressions by Search/Maps, call/website/direction clicks (`platforms/google-business-profile.md` section 9) |
Rule: never add numbers from two platforms into one "total reach"; show them side by side.

## 4. Report structure
**Weekly (15 minutes, internal, 1 page)**
1. Headline: one sentence (up or down, why in a phrase).
2. Primary KPI vs last week and vs target.
3. Top 3 posts and bottom 3 posts with the hypothesis for each.
4. Community: first-reply time median, unresolved items, top 3 recurring questions.
5. Risks and incidents (moderation actions, platform notices, API errors from `automation-recipes.md`).
6. Next 3 actions with owners.
**Monthly (client or leadership, 2 pages + appendix)** use `../templates/monthly-report.md`
1. Executive summary: result vs goal in 3 lines.
2. KPI table (3 to 5 KPIs): this month, last month, target, trend, note.
3. What worked and why (evidence), what failed and why (hypothesis, confidence).
4. Content and format analysis by pillar and platform.
5. Audience and community (growth, sentiment, support metrics).
6. Experiments run and results (section 7).
7. Next month: keep, stop, start (max 3 each); calendar summary.
8. Appendix: data definitions, platform file dates, anomalies.
Quarterly: add pillar mix, platform ROI by time spent, and the review in `strategy-and-planning.md` section 8.

## 5. Attribution limits for organic
- Many social apps open links in in-app browsers and strip or change referrers; some clicks arrive as "direct".
- Dark social (WhatsApp, Telegram, DMs, copy-paste) is invisible to analytics; shares by DM often lack tracking.
- Instagram captions and comments do not carry clickable links (`platforms/instagram.md` section 3), so conversions start from the bio, Stories or DMs.
- Cross-device and offline actions (store visits, phone orders, cash on delivery) are mostly unmeasured on social.
- Platform conversions are modelled or deduplicated in different ways; do not compare them with your own sales system without reconciling.
- Organic and paid overlap: paid boosts change organic reach; separate them by label and time (media-buying handles paid).
Practical mix of evidence (heuristic): UTM sessions, promo codes per platform, a "How did you hear about us?" field, branded search trend, DM keyword counts, and call/WhatsApp counts at the same hours as posts. Report these as signals, not proof; state confidence (low/medium/high).

## 6. UTM conventions
Use `scripts/utm.py` so values are consistent: `python3 scripts/utm.py https://example.com/offer --source instagram --medium social --campaign white-friday --content reel-03`.
- Lower-case, ASCII, hyphens not spaces; the script rejects Arabic (transliterate campaign names, for example `ramadan-sale`).
- `utm_source`: platform slug (`instagram`, `facebook`, `tiktok`, `youtube`, `linkedin`, `x-twitter`, `telegram`, `whatsapp`, `gbp`).
- `utm_medium`: `social` for organic posts; use a different value (for example `influencer`, `paid-social`) for other types and keep the list in one table.
- `utm_campaign`: `<theme>-<yyyy-mm>` (for example `white-friday-2026-11`).
- `utm_content`: format plus sequence (`reel-03`, `carousel-12`, `story-sticker`, `bio-link`).
- `utm_term`: optional keyword (ads or search); leave empty for organic.
- `--id`: optional post id to match the calendar row.
- Never put personal data, names, emails or phone numbers in UTM values; URLs are logged in many places.
- One short link per campaign in bios; test every link on mobile; avoid chained redirects. Shorteners: some platforms block known shorteners (`platforms/pinterest.md` section 7); prefer your own domain.
- Keep a UTM register sheet (campaign, owner, date range, final URLs) tied to calendar rows (`../templates/content-calendar.md`).
Analytics tools usually treat `social` as an organic-social medium in default channel groupings; check your tool's grouping rules (unverified here).

## 7. Experiment design for organic
What can be tested: hook wording, first 3 seconds, video length, format (carousel vs Reel), cover/thumbnail, caption length, CTA wording, posting window, topic angle, language/dialect (Egyptian vs MSA), hashtag set size within caps, first-comment link.
Rules:
1. One variable per test; state hypothesis, metric and decision rule before posting ("Hook B wins if median 3-second hold is 5 points higher across 6 posts").
2. Comparable posts: same pillar, same format, similar topic strength; alternate A and B on similar days/times.
3. Sample: at least 6 posts per variant where cadence allows; with fewer, label the result as a hint. Organic reach is noisy (algorithm, news cycle, size of audience). One viral or dead post is not a result.
4. Noise check (heuristic): compute the median and the spread (interquartile range) of the last 20 posts; call a difference real only if the variant medians differ by more than the spread, and re-test once.
5. Platform tools: Instagram Trial Reels show a Reel to non-followers first (`platforms/instagram.md` section 2); other native test features were not verified in the platform files, so check the app.
6. Do not run tests that harm the audience (misleading hooks, fake urgency) or break platform rules (duplicate spam).
7. Record every test in a log: hypothesis, variants, dates, result, decision, confidence; roll winners into the playbook.
8. Posting-time tests need 4 weeks of stable cadence; use the account's insights, not generic charts (`egypt-mena-playbook.md` section 6).

## 8. Dashboards
- Source: official exports and APIs only (platform files section 9 and 8); no scraping or unofficial tools. API access is gated on several platforms (LinkedIn, Snapchat, GBP, TikTok): where there is no API, export by hand weekly and paste into the data sheet.
- Structure: a raw data tab (one row per post per day: date, platform, post id, format, pillar, metrics), a metrics tab (calculated rates), a goals tab (targets), a notes tab (campaigns, incidents).
- Tools: Google Sheets or Looker Studio, Notion, Airtable, or n8n/Make writing to a sheet (`automation-recipes.md` recipe 4). The `data-visualization` skills can chart exports.
- Keep one page per audience: operator (daily), manager (weekly), client (monthly). Show target lines and the date of the last data refresh. Mark platform metric changes with annotations.
- Retention: save monthly snapshots; platforms keep limited history (Instagram user metrics 90 days, X owner metrics 30 days, per their platform files).
- Access: view-only for clients; credentials never in the sheet.

## 9. Writing insight, not description
Formula: **Observation, comparison, reason (hypothesis), action, confidence.**
- Description (weak): "Reel A got 12,000 views and 340 likes."
- Insight (useful): "Reel A reached 3.2x our median non-follower views; the first 2 seconds show the finished product before the process, and the 3 other Reels with this hook are also above median (n=4). Next: apply the hook to the next 4 product Reels and compare median 3-second hold. Confidence: medium."
Arabic version for client reports: "الريل ده وصل لناس جداد أكتر من المتوسط بـ ٣ أضعاف تقريبًا، والسبب المرجح إن أول ثانيتين بيوروا المنتج النهائي. هنجرب نفس البداية في ٤ ريلز جاية. درجة الثقة: متوسطة."
Checklist: every chart has a "so what" line; each insight has an action and an owner; correlation is not stated as cause; small samples are labelled; failures are reported with the same detail as wins; benchmarks come from the account's own history unless a sourced benchmark is cited with date.

## 10. Sources
- Platform files section 9 and section 8 (each with sources and dates).
- UTM script: `scripts/utm.py` in this skill.
- Thresholds in sections 4 and 7 (6 posts, IQR check, 4 weeks) are heuristics, not sourced standards.
