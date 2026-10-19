# YouTube Ads — rules and playbook
Last verified: 2026-10-19

Scope: video ads bought through Google Ads (Video campaigns, Demand Gen, PMax video) and reservation products. For account, billing, tracking, API and general Google policy rules, read `google-ads.md` first; this file adds only what is specific to YouTube. Items marked `unverified` were not confirmed in an official source in this pass. "Practitioner observation" means lore, not an official rule.

## 1. When to use it
- Use YouTube for reach, consideration and demand creation with video, and for action goals through Demand Gen (YouTube, Shorts, Discover, Gmail, Display in one campaign).
- Strengths: video storytelling at scale, Shorts and connected-TV reach, audience targeting from Google signals, brand-lift measurement (Brand Lift recommended for reach campaigns, help 12400225).
- Weaknesses: cost per conversion usually higher than Search for direct response; view metrics are not conversions; creative quality dominates results; fewer brand-safety controls on some surfaces (see section 4).
- Best objectives:
  - Awareness: Video reach (Efficient reach, Non-skippable reach, Target frequency) with bumper, skippable in-stream, in-feed, Shorts.
  - Consideration: Video views (cost per TrueView view), Demand Gen with Max Clicks.
  - Action: Demand Gen (replaced Video action campaigns) or Video campaigns with goals Sales, Leads, Website traffic using Max conversions or tCPA.
- Video action campaigns were phased out: new ones could not be created from April 2025, automatic upgrades to Demand Gen ran July 2025 to April 2026 (help 15110871). Do not plan new work on VAC.
- Egypt / MENA relevance: no sourced figures were collected in this pass (YouTube reach by country, Arabic-language viewing share, CPM/CPV/view-rate benchmarks for Egypt/MENA: `unverified`). Do not quote benchmarks. Build the baseline from the account's first 2-4 weeks. The only benchmark Google's help page gives is an average in-stream view rate of roughly 10-15% (global, undated, "varies widely"; help 2375431).

## 2. Account, billing and access
- YouTube ads run inside a Google Ads account; billing, verification, VAT (Egypt 14% unless TRN + UIN) and access rules are the same as `google-ads.md` section 2.
- Link the YouTube channel to the Google Ads account to use channel audiences (viewers, subscribers, interactions) and to count earned actions (views, subscribers on the linked channel within 7 days; help 2375431). Linking steps: not fetched; `unverified`.
- Video ads are built from videos on YouTube (the exact hosting/visibility rule was not on the fetched pages; `unverified`). Policy says videos must be publicly available (help 176114). Keep the video up after launch.
- Masthead and reservation products (Premier reach, Standard reach): sold through a Google sales representative; fixed CPM or cost-per-hour (help 2375464). Not available self-serve.
- Egypt/MENA reservation availability and minimums: `unverified`.

## 3. Campaign structure
- Video campaigns (Google Ads) in five steps: objective, budget and bidding, targeting, ad groups, ads (help 2375425).
  - Sales / Leads / Website traffic: needs conversion tracking; subtype Drive conversions; Max conversions or tCPA; tROAS and Max conversion value unlock after enough conversions.
  - YouTube reach, views and engagements (no conversion tracking needed):
    - Video views: bid cost per TrueView view (CPV). Target CPV (tCPV) in multi-format video view campaigns.
    - Video reach: Efficient reach (bumper + skippable in-stream; multi-format adds in-feed and Shorts), Non-skippable reach (15 s, 30 s mainly CTV, or mix of 6 s bumpers and 15 s ads in beta), Target frequency; all bid Target CPM (help 10581234).
    - Ad sequence, YouTube subscriptions and engagements (tCPA), Audio reach (tCPM).
  - Reservation: fixed CPM (Premier reach, Masthead, Standard reach).
- Manual CPC and Maximize clicks are not available for video campaigns (help 2375425). Demand Gen offers Maximize Clicks.
- Demand Gen (the action-oriented route): YouTube + Shorts + Discover + Gmail + GDN; image, video, carousel; billing by surface (YouTube video and image CPM; Gmail teaser click; Discover image CPC; GDN CPM) (help 14509385). Frequency cannot be controlled. Video action campaigns' shared budgets, lead-form ads (beta), seasonal-event targeting, new-customer-acquisition goals and frequency caps were removed in the upgrade (help 15110871).
- Performance Max can also serve video (YouTube inventory); see `google-ads.md`.
- Recommended structure (heuristic):
  - Small budget: one Demand Gen or Video views campaign, 2-3 creatives, one audience, Max Clicks or tCPV; no multi-campaign splits.
  - Medium: separate prospecting (Video reach or Demand Gen with lookalikes) and retargeting (site visitors, YouTube viewers) so retargeting frequency is controlled by audience size.
  - Large: Video reach with Target frequency + Brand Lift; Demand Gen for action; experiments on creative; reservation Masthead/Premier reach for launches.
- Buying types: auction (self-serve) and reservation (fixed CPM via rep). Target frequency supports auction and reservation (non-mixed formats), not Google video partners.

## 4. Targeting and audiences
- Audience (who) options for video campaigns (help 2454017): demographics (age, gender, parental status, household income), detailed demographics, interests (affinity, custom affinity, life events, in-market, custom segments), your data (viewers of your videos/ads/channel, site/app visitors), Customer Match.
- Content (where): placements (YouTube channels/videos, GDN sites/apps), topics, keywords, devices (computers, phones, TV screens).
- Location targeting is an intersection with other targeting. Multiple content types: ads can show on content matching any of them.
- Conversion-driving video campaigns can no longer add content targeting; the page says it was removed from them in early 2023 (help 2454017). Use Demand Gen audiences or placement exclusions instead.
- Demand Gen: lookalike segments (purchasers, site visitors, YouTube channel viewers), custom segments (10-15 keywords suggested), audience insights. Sensitive-category campaigns must use predefined Google audiences.
- Target frequency: respects age/gender targeting; no contextual/topic/keyword/placement targeting; one ad group per campaign; no shared budgets; only for new campaigns.
- Inventory types (content suitability, help 12764663): Maximum (all inventory except highly sensitive), Moderate (excludes strong profanity, dramatized violence, sexually suggestive themes), Limited (also excludes moderate profanity and suggestive themes; may reduce reach). Names in older docs ("Expanded/Standard/Limited") differ; use the current names above.
  - Exclusions: content types, topics, keywords (exact match only, up to 1,000 at account level), placements (up to 65,000), content labels (Display only; YouTube stopped using them as of September 2024). Always-on automatic exclusions apply regardless (e.g. terrorism, nudity).
  - Coverage gap: YouTube Shorts, Home feed and Subscription feed have limited or no support for several exclusion types; Home and Subscription feeds do not support content-type, keyword, placement or theme exclusions.
  - Brand-safety rule: choose the inventory type BEFORE launch; for regulated or kid-adjacent brands use Limited and a placement exclusion list; review the placement report in week 1.
- Restrictions: sensitive categories and personalized-ads restrictions follow the Google Ads policies (see `google-ads.md` section 8); health, financial and political targeting rules per country: `unverified`.
- Arabic / regional notes:
  - Target by location and language (Arabic and/or English). How YouTube language targeting maps to viewer language: `unverified` in this pass.
  - Add Arabic keywords for custom segments and content keywords in both Arabic script and Latin transliteration. Practitioner observation.
  - Check exclusions for dialect content: category-level exclusions are language-dependent in classifier quality; verify with the placements report. `unverified` for Arabic classifier accuracy.

## 5. Bidding, budget and delivery
- Bid strategies by campaign type (help 2375425, 2472735, 10581234):
  - Video views: CPV (target CPV in multi-format). You pay for TrueView views, not impressions.
  - Video reach, Ad sequence, Audio reach: Target CPM (tCPM). Non-skippable and bumper are impression-bought.
  - Sales/Leads/Traffic video: Maximize conversions, Target CPA; tROAS/Maximize conversion value after enough conversions.
  - Demand Gen: Maximize Clicks, Maximize Conversions, Target CPA, value-based (help 13695777).
- CPV: you pay when a viewer watches 30 s (or the full ad if shorter) or interacts, for in-stream; in-feed counts a click to watch or autoplay of at least 10 s; Shorts counts 10 s, a CTA click, or like/comment/share (help 2375431, 2472735). Bumper and non-skippable are not TrueView views.
- Minimum bid/budget: not documented on the pages fetched (`unverified`). Follow the in-product bid suggestion; Target frequency explicitly says follow the in-built bid suggestion. Demand Gen Max Clicks has no minimum budget; tCPA needs daily budget of at least 10x the target CPA (help 13695777). A bid set too low limits the campaign's ability to compete (help 2472735).
- Delivery and learning:
  - Target frequency campaigns: run at least 7 days, ideally 2-4 weeks; have at least as many creatives as the frequency target; avoid mid-flight changes (removing audiences, late budget swings, pause/resume) (help 12400225).
  - Smart Bidding learning rules from `google-ads.md` section 5 apply to tCPA/Max conversions in Demand Gen (switch to tCPA only after at least 50 conversions per the Demand Gen FAQ).
  - Mid-flight changes to bid strategy or composition trigger a new learning period (help 13020501).
- Frequency:
  - Video reach Target frequency (2-7 per week or 4-12 per month in multi-format; 2-4 per week or 4-8 per month for non-skippable or skippable+bumper in-stream). It is a target, not a cap; some users exceed it (help 12400225).
  - Demand Gen: no frequency control; review unique reach and impressions per user.
  - Video action campaign frequency caps no longer exist after the upgrade.
- 2026-08-17 bidding change (budget-limited tCPA/tROAS deliver closer to target) excludes Video reach and Video view campaigns (help 17061251); it does apply to Demand Gen.

## 6. Creative specs and requirements
Source: help 13547298 (video ad specs), 13704860 (Demand Gen), 10581234, 2375464. Re-check before bulk production.

| Format | Ratio | Size / resolution | Length | File size | Text limits | Notes |
|---|---|---|---|---|---|---|
| Skippable in-stream | 16:9 recommended (also 9:16, 1:1, 4:5, 2:3, 4:3 accepted) | rec 1920x1080; min 1280x720 (SD 640x480 not advised) | No max; under 3 min suggested; at least 7 s; skippable after 5 s | up to 256 GB | Video campaign headline and description up to 90 chars each; display URL up to 255; Google recommends a 40-char headline and 90-char description | Charged per view (30 s or interaction) in Video views; tCPM/tCPA/Max conversions on impressions in other goals |
| Non-skippable in-stream | 16:9 | same as above | Policy page: up to 30 s in auction, 60 s in reservation; format page says 15 to 60 s by subtype; Video reach options: 15 s (30 s mainly CTV); 7 to 15 s | 256 GB | as above | Conflicting pages; check campaign UI. Impression-bought (tCPM) |
| Bumper | 16:9 | same | 6 s | 256 GB | as above | Not skippable; tCPM; no TrueView view |
| In-feed video | horizontal recommended (help 12400225) | rec 1280x720 thumbnail 16:9 (min 1280x640) | No max | 256 GB | Headline up to 90 and description (as video campaigns) | Click to watch; shows in Search, Watch Next, Home, Subscriptions feeds |
| YouTube Shorts ad | 9:16 vertical recommended | rec 1080x1920 | at least 5 s; under 60 s recommended | 256 GB | as above | Skippable by swiping; TrueView view at 10 s; Shorts spec page not found, `unverified` |
| Demand Gen video | 16:9, 1:1, 4:5, 9:16 | rec 1920x1080, 1080x1080, 1080x1350, 1080x1920 | min 5 s; under 10 s cannot serve in YouTube in-stream | 256 GB | headline 40, description 90, business name 25 | Format MPG (MPEG-2/4) |
| Demand Gen image | 1:1, 1.91:1, 4:5, 9:16 | min 300x300 to 600x1067; rec 1200x1200, 1200x628, 960x1200, 1080x1920 | n/a | 5 MB | as above | 9:16 image recommended for Shorts; safe zones like 9:16 video |
| Companion banner (desktop) | 300x60 | 300x60 | n/a | 150 KB | n/a | jpg/gif/png |
| Thumbnail (in-feed) | 16:9 | rec 1280x720, min 1280x640 | n/a | under 2 MB (video) | n/a | jpg/gif/png |
| Masthead | n/a | n/a | over 10 s recommended | n/a | n/a | Reservation only (CPM or cost per hour) |

- Accepted resolutions: recommended 1080p (1920x1080, 1080x1920, 1080x1080); accepted 720p minimum (1280x720, 720x1280, 480x480); audio-only files not accepted. Recommended container MPG; also MP4, MOV, WMV, AVI, FLV, WebM, ProRes, HEVC and others.
- Safe zones: keep logos, products and text inside the safe area in Google's overlay templates; buttons and overlays cover edges in some placements.
- Tracking pixels in video ads (policy 176114): SSL only; allowed only on impression, view and skip events (not midpoint/complete); max 3 pixels per event; no JavaScript data collection; third-party click redirects allowed.
- Google AI can create 9:16 versions of videos in Video reach campaigns (on by default for new campaigns; can be turned off).
- AI-generated content may require an AI label (EU, India, New York rules; video specs page).
- Creative rules for the first 5 seconds:
  - Official mechanics: skippable in-stream can be skipped after 5 s; Shorts can be swiped immediately; bumper is 6 s. So the first 5 s (in-stream) or first 1-2 s (Shorts) must carry brand/product and the hook. Google's own creative guidance (ABCD framework) was not fetched; `unverified`.
  - Practitioner rules: show the brand or product in the first 3 s; lead with the benefit or a question, not a logo animation; add captions (many views are muted); keep Arabic captions inside safe areas; for Shorts shoot native vertical, not a cropped 16:9.
  - Provide one video per ratio when possible (16:9, 1:1/4:5, 9:16) so Demand Gen does not crop.
- Arabic/RTL cautions: burned-in Arabic subtitles must sit above the Shorts/in-stream UI overlay; check right-to-left alignment in every ratio; write captions in the same dialect as the voice-over, word for word, and avoid mixed RTL/LTR punctuation glitches; for voice-over in Arabic, do not rely on auto-captions without review. Practitioner observations.

## 7. Tracking and measurement
- Tag, enhanced conversions, consent mode v2, conversion windows and attribution follow `google-ads.md` section 7. YouTube-specific points below.
- View-based conversion windows (help 3123169): engaged-view default 3 days, view-through default 1 day, click-through 30 days. Overall range 1-90 days. Smart Bidding optimizes for the window you pick.
- Engaged-view conversion (EVC; help 2375431): the viewer did not click, but watched at least 10 s of a skippable ad (skippable after 5 s) and converted within the engaged-view window. For Shorts the trigger is 5 s watched or a CTA click.
- View-through conversion: viewer saw an impression and converted within the view-through window without clicking.
- Rule: report EVC and view-through separately from click conversions; do not let them inflate CPA/ROAS for bidding decisions without checking incrementality. Practitioner rule; Google counts them per account settings.
- Data-driven attribution supports YouTube, Search/Shopping, Display and Demand Gen; recommended at least 200 conversions and 2,000 interactions in 30 days (help 7003150).
- Brand Lift: recommended for Video reach/target-frequency (help 12400225). Eligibility and minimum spend: `unverified`.
- Earned actions (help 2375431): a view on your ad followed within 7 days by an action on the linked channel is an "earned view"; not billed; repeat views by the same person count once.
- UTM: add utm_source=youtube, utm_medium=video (or cpv) and utm_campaign naming; keep autotagging. Convention, not an official rule. GA4 will not credit view-through conversions as Google Ads does, so numbers differ; compare with the same window and note it.
- Privacy: EEA consent mode v2 signals apply the same as Search; without consent, YouTube remarketing lists for EEA users are limited (see `google-ads.md`).

## 8. Policies and restricted content
- General Google Ads policies apply (see `google-ads.md` section 8).
- Video ad requirements (help 176114): videos publicly available; name or logo clearly identifying advertiser/product; meet video quality standards; sexual content restricted; advertiser must own copyright or be authorized; third-party tracking per section 6.
- Length rules in policy: non-skippable in-stream up to 30 s in auction campaigns, 60 s in reservation; skippable has no limit.
- Approval: typically within a day (help 2375425). Migrated Video action ads were treated as new and needed re-approval (help 15110871).
- Content restrictions: YouTube and Google video partners have always-on exclusions; sensitive categories are mostly limited to YouTube in Demand Gen; gambling, alcohol and political content cannot run on Discover (help 13695777). Country-level rules for MENA: `unverified`.
- Claims: unreliable-claims policy (miracle cures, unrealistic weight loss, guaranteed returns) applies to video voice-over and on-screen text, not only text assets. Warning of at least 7 days before account suspension for that policy (help 15936857).
- Kids/children: policy for made-for-kids content and personalized ads: not fetched; `unverified`. Avoid targeting or featuring minors for regulated products.
- Appeals: edit and resubmit, or appeal in Policy manager (see `google-ads.md`). Re-uploading a video starts a fresh review (help 9338593).
- While rejected: swap in a compliant cut of the video, keep other ads live, and do not re-upload the same video repeatedly.

## 9. Optimization playbook
1. Decide the job before the format: reach (tCPM/Target frequency), views (CPV), action (Demand Gen / Max conversions). Never judge a reach campaign on CPA.
2. First look at day 3-7: delivery (impressions, spend vs budget), view rate (TrueView views / impressions), average CPV or CPM, placements (YouTube vs Google video partners), search-term-like placement report for junk.
3. View rate: Google's help page cites roughly 10-15% for in-stream averages, varying widely (undated, global). Use only as a rough sanity range; compare ads against each other, not against the cited range. For Egypt/MENA no benchmark found.
4. Hook test: run 3 openings (first 5 s) of the same body; keep the one with the best view rate or CTR; budget so each variant gets at least about 1,000 views/impressions-for-CPM before judging (heuristic: enough events for a stable rate; for CPA tests use the 10x tCPA per variant per week rule from `google-ads.md`).
5. Fatigue signals: falling view rate or CTR for 7+ days with rising frequency, rising CPM/CPV with flat targeting. Rotate or add a creative; for Target frequency, creatives should be at least as many as the frequency target (help 12400225).
6. Scale: raise budget about 20% per step every 3-7 days only if CPA/CPV is stable; for Target frequency avoid late budget swings; for Demand Gen with tCPA keep budget at least 10x tCPA per day.
7. Cut: pause placements with high spend and near-zero view rate or conversions after a full week; exclude channels/videos via account or campaign placement exclusions; do not cut for CPA before 1-2 conversion cycles.
8. What NOT to touch during learning: bid strategy, audiences in Target frequency, creative swaps all at once, budget doubling, pausing and resuming.
9. Retargeting: cap by audience size; Demand Gen has no frequency control, so use small audiences with sequenced creative and exclude converters.
10. Sequence rule (practitioner): prospecting video, then a shorter retargeting cut with offer and CTA to site visitors/viewers.
11. Measure incrementality for high spend: Brand Lift or geo-split test; platform view-through numbers are not proof of causality.
12. Shorts: test native vertical creative separately; do not assume in-stream creative cropped to 9:16 will work.

## 10. Metrics and definitions
| Google Ads name | Standard | Definition |
|---|---|---|
| Impr. | Impressions | Ad served. Shorts viewable impression for tCPM = 50% on screen for 2 continuous seconds (help 2375464) |
| TrueView views (renamed from "Views" Oct 2025) | Paid views | Billing unit for CPV; thresholds in section 5 (help 2375431) |
| View rate | VTR | TrueView views / impressions (formerly "view-through rate"); format-specific columns exist |
| Avg. CPV | Cost per view | Cost / TrueView views; the page gave no definition (`unverified`) |
| Avg. CPM | CPM | Cost per 1,000 impressions; billing unit for tCPM |
| Interactions (engagements) | Engagement | Videos under 10 s: full watch or click; over 10 s: watch over 10 s or click; bumper/non-skippable count only clicks |
| Clicks, CTR | Link clicks / CTR | Standard |
| Conversions, Cost/conv. | CVR, CPA | See `google-ads.md` |
| Engaged-view conv. | EVC | Watched at least 10 s then converted in window (5 s for Shorts) |
| View-through conv. | VTC | Impression then conversion within window |
| Earned views / earned actions | Earned | Actions on the linked channel within 7 days; not billed |
| Unique reach, Avg. impr. frequency | Reach / frequency | In Video reach and Demand Gen reports |
| Thumb-stop / hook rate | Hook rate | Not a Google Ads metric. Proxy: view rate (in-feed/Shorts) or 25%-watched in video reports; the exact quartile columns: `unverified` |

## 11. API and automation
- Same API and access rules as `google-ads.md` section 11. Video campaigns, ad groups, video ads, assets and reports are manageable through the Google Ads API; the exact resource names and which video subtypes are writable in the current API version: `unverified` in this pass.
- Reporting: pull view rate, CPV, impressions, frequency/unique reach, placements, EVC. Alert on spend with zero views and on disapproved video ads.
- Do not automate creative swaps without a policy check; new video assets go through review (typically within a day).
- Video action campaigns no longer exist; scripts or API integrations that target them should be migrated to Demand Gen (help 15110871).
- Automated bidding changes on Video reach/view are outside the 2026-08-17 target-delivery change.

## 12. Cases
**Situation: Video ad disapproved.**
**Do:** read the policy reason; check claims in voice-over and on-screen text, brand/logo clarity, copyright music, destination page; edit, re-upload a compliant version, resubmit; appeal if it is clearly an error.
**Avoid:** re-uploading the identical file repeatedly; hiding claims in a slate.

**Situation: Account suspended after video ads.**
**Do:** follow `google-ads.md` appeal steps; check misrepresentation (fake endorsements, impersonation) and payment/verification status.
**Avoid:** using celebrity likeness or implied endorsements (egregious, no-warning suspension).

**Situation: Spend with no conversions.**
**Do:** confirm the objective and conversion tracking; check whether the campaign is a reach/views campaign (no conversion goal); check placements; move to Demand Gen with a lightweight conversion (add to cart, lead) and Max Conversions; give it a conversion cycle.
**Avoid:** judging CPA on a CPV campaign; setting tCPA far below history.

**Situation: CPA doubled suddenly.**
**Do:** check engaged-view/view-through settings change, creative fatigue (frequency), tracking, budget change, 2026-08-17 target behavior (Demand Gen), seasonality.
**Avoid:** changing five settings at once.

**Situation: Learning limited / too few conversions.**
**Do:** use Max Clicks (no minimum budget) or Max Conversions with a lightweight event; consolidate audiences; wait; move to tCPA after at least 50 conversions (Demand Gen FAQ).
**Avoid:** tCPA at launch; many small ad groups.

**Situation: Creative fatigue.**
**Do:** refresh the first 5 s, add formats (Shorts vertical), rotate at least as many creatives as the frequency target.
**Avoid:** replacing all creatives simultaneously (resets what you learned about winners).

**Situation: Tracking mismatch (Ads vs GA4 vs CRM).**
**Do:** separate click vs EVC/view-through; compare same window; use CRM as truth; apply enhanced conversions where consented.
**Avoid:** reporting EVC-inflated ROAS to a client without labeling it.

**Situation: Tiny budget.**
**Do:** one Demand Gen campaign with Max Clicks (no min budget) or Video views with 2 creatives; narrow Egypt geography; review placements at day 3.
**Avoid:** Target frequency or reach campaigns (need reach budget and 7+ days), splitting budget across formats.

**Situation: Local lead gen / WhatsApp (Egypt).**
**Do:** short vertical video with the offer and a visible CTA; Demand Gen to site/WhatsApp landing page; track WhatsApp click as an event; follow up leads in CRM and import offline conversions.
**Avoid:** counting views as leads; sending to a generic homepage.

**Situation: Scaling too fast.**
**Do:** about 20% budget steps per 3-7 days; add creative before budget; keep frequency in check.
**Avoid:** doubling budget mid-flight on Target frequency campaigns.

**Situation: Seasonal peak (Ramadan, White Friday).**
**Do:** prepare Arabic creative variants (greeting + offer), bumpers for reach, retargeting video for cart abandoners; start earlier to build audiences; plan budget at least a week before.
**Avoid:** launching untested creative on peak day; relying on view-through conversions to judge peak ROAS.

## 13. Pre-launch checklist
1. Is the YouTube channel linked and the video public with correct title/thumbnail?
2. Does the video identify the advertiser (name or logo) and avoid unreliable claims?
3. Do you own rights to music, footage, and any faces/voices?
4. Is the objective right (reach, views, action) with the matching bid strategy?
5. Is conversion tracking verified for action goals (tag, test conversion, enhanced conversions)?
6. Are engaged-view and view-through windows set deliberately (defaults 3/1 days)?
7. Is the inventory type chosen (Maximum, Moderate, Limited) and exclusions loaded?
8. Are location and language set for Egypt/MENA and the right audiences loaded?
9. Are there creatives in 16:9, 1:1/4:5 and 9:16 with safe zones respected?
10. Are the first 5 seconds (first 2 s for Shorts) carrying hook, product and brand?
11. Are Arabic captions reviewed and inside safe areas?
12. For Target frequency: at least as many creatives as the frequency target, and 7+ days of runway?
13. For tCPA: daily budget at least 10x target CPA and at least 50 prior conversions (or start with Max Conversions)?
14. Is a Brand Lift or incrementality plan set for reach spend?
15. Are billing, VAT and verification complete (see `google-ads.md`)?
16. Are alerts in place for disapprovals and for spend with zero views?

## 14. Sources
- Video ad formats: https://support.google.com/google-ads/answer/2375464
- Video ad requirements (policy): https://support.google.com/adwordspolicy/answer/176114
- Video ad specs: https://support.google.com/google-ads/answer/13547298
- YouTube ads and view metrics: https://support.google.com/google-ads/answer/2375431
- CPV bidding: https://support.google.com/google-ads/answer/2472735
- Create a video campaign: https://support.google.com/google-ads/answer/2375425
- Video reach campaigns: https://support.google.com/google-ads/answer/10581234
- Target frequency: https://support.google.com/google-ads/answer/12400225
- Targeting for video campaigns: https://support.google.com/google-ads/answer/2454017
- Content suitability: https://support.google.com/google-ads/answer/12764663
- Demand Gen: https://support.google.com/google-ads/answer/13695777 ; specs https://support.google.com/google-ads/answer/13704860 ; FAQ https://support.google.com/google-ads/answer/14509385
- Video action campaign upgrade: https://support.google.com/google-ads/answer/15110871
- Conversion windows: https://support.google.com/google-ads/answer/3123169
- Data-driven attribution: https://support.google.com/adwords/answer/7003150
- Bidding change 2026-08-17: https://support.google.com/google-ads/answer/17061251
- Unreliable claims: https://support.google.com/adspolicy/answer/15936857
- Appeals: https://support.google.com/adspolicy/answer/9338593
- Learning period: https://support.google.com/google-ads/answer/13020501

Unverified summary: Egypt/MENA reach and benchmarks, channel-link steps, YouTube hosting/visibility rule, reservation availability and minimums, Shorts ad spec page, Google's own creative guidance (ABCD), Brand Lift eligibility, quartile/hook-rate columns, kids/made-for-kids policy, MENA sensitive-category rules, API resource names for video subtypes, Arabic classifier accuracy for exclusions.
