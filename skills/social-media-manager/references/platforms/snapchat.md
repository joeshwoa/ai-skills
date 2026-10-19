# Snapchat — rules and playbook
Last verified: 2026-10-19

Scope: Snapchat as an organic channel for a business or creator (Public Profile, Stories, Spotlight, Saved Stories). Paid Snap Ads and the ads Marketing API are out of scope except where they touch organic. Where a fact comes from an official page it is tagged with its URL in section 13. Anything marked `unverified` could not be confirmed on an official page on the verification date.

## 1. Snapshot
- Snapchat is a camera-first, mobile-first app. A person has a private profile (friends only) and, from age 16 in most countries, can opt into a Public Profile visible to anyone (help.snapchat.com "What is a Public Profile", "Who is eligible").
- Businesses create and manage Public Profiles in Ads Manager; Snapchat does not create them automatically. One email/username can hold only one Public Profile; one organization can run several profiles with separate roles (forbusiness.snapchat.com/en-US/public-profiles).
- Content surfaces: Stories (visible up to 24 hours), Saved Stories (stay on the profile), Spotlight (permanent short videos distributed to a wider audience), Lenses (AR) (developers.snap.com Public Profile API intro).
- Best for: younger mobile audiences, behind-the-scenes and casual short video, AR/Lens campaigns, local discovery through Snap Map.
- Egypt / Arab world: DataReportal (Snap's own ad tools, January 2025, page updated 12 March 2025) lists ad reach of 24.7 M in Saudi Arabia, 19.7 M in Egypt and 18.5 M in Iraq. DataReportal says ad reach is not a direct proxy for active users. Newer Egypt figures: `unverified`.
- Not a link-driving channel for organic posts in the way Pinterest or Google Business Profile are; treat it as attention and community, and measure with Insights (section 9).

## 2. Content formats and specs
Figures below for Story/Spotlight/Saved Story come from the Public Profile API asset-management documentation. They are the ingest limits for API uploads; the app itself may accept other inputs (`unverified` for in-app limits).

| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Public Story (video) | portrait; minimum 540x960 px (ratio not stated; 9:16 is the practical choice) | 5-60 s per API upload | .mp4; upload up to 1 GB via multipart (32 MB chunks, parts 1-35) | API: uploaded media object must be used within 24 h of creation. Story is visible up to 24 h unless saved |
| Public Story (image) | `unverified` for API; 1080x1920 (9:16) is the common app canvas (`unverified`, practitioner convention) | n/a | `unverified` | App lets you add photos from camera roll |
| Spotlight | portrait; minimum 540x960 px | 6-60 s per API upload | .mp4; same multipart limits | Description up to 160 chars, hashtags allowed. Monetization needs 30 s or longer (section 6) |
| Saved Story (Highlight) | follows source snaps | combined duration max 5 min via API | built from Spotlight, a public-story snap, or uploaded media | Title up to 45 chars (API). Only proactively saved content stays on the profile |
| Lens (AR) | built in Lens Studio | n/a | n/a | Lens publishing is outside this file; list a Lens on the profile through Lens Studio (`unverified` details) |
| Live / group live | none documented for Public Profiles | n/a | n/a | `unverified`: no official spec found |
| Text-only post | not a format | n/a | n/a | Snapchat has no text-only organic post |
| Link attachment | full http:// or https:// URL in `link` parameter (API) | n/a | n/a | In-app, link/swipe-up behaviour on Stories is `unverified` for this date |

Quality rules that affect distribution (values.snap.com recommendation guidelines, Quality): blurry or pixelated video, wrong orientation, letterboxed video and missing audio are not eligible for recommendation.

## 3. Text limits
- Spotlight description: 160 chars including hashtags (API). Spotlight title in app: `unverified`.
- Saved Story title: 45 chars (API). Story caption: no posting limit stated; in-app caption limit `unverified`.
- Public Profile bio, display name, username limits: `unverified` (Snapchat help pages that list them did not load). Do not hard-code a number.
- Comments: Spotlight has comments (insights list "comments"); comment length `unverified`.
- Hashtags: allowed in Spotlight description; maximum count `unverified`.
- Mentions: `unverified` for count limit.
- Links: no clickable link in a Spotlight description is documented. Stories/Spotlights accept a `link` field through the API (must be a full URL). Off-platform links to social, messaging or cloud-storage services make content ineligible for recommendation, except limited surfaces for vetted creators (values.snap.com Quality).
- Arabic/RTL: Snapchat has Arabic UI; text behaviour of captions with mixed Arabic/English: `unverified`. Always test an Arabic caption on a device before scheduling at scale.

## 4. Posting and cadence
- Official posting-frequency guidance: none found. Everything below is a heuristic.
- Heuristic: Stories are daily, informal, low-production; Spotlight is 2-5 polished vertical videos per week; Saved Stories are evergreen (menu, FAQ, location, offers, how to order).
- Timing: no official best time. Use Insights audience and past Story view curves (section 9). Evenings in Cairo (local time, UTC+2/+3 depending on daylight saving) are a starting hypothesis to test, not a rule.
- Funnel:
  - Awareness: Spotlight with a strong first 2 seconds, Lenses, trending sounds you have rights to.
  - Consideration: Stories sequence (product demo, staff Q&A, before/after), Saved Stories "How it works".
  - Conversion: Story with link attachment (check current availability), Saved Story with price/location/how to order, business profile link to site or catalog.
  - Retention: subscriber-only tone in daily Stories, polls (do not ask sensitive-personal-information polls, see section 6).
- Snap Map: content can be tagged with locations to appear on Snap Map (creators.snapchat.com/getting-started).

## 5. Distribution and ranking signals
Official:
- Content is recommended beyond friends/subscribers only if it meets the Content Guidelines for Recommendation Eligibility (help.snapchat.com Spotlight Guidelines).
- Snap says it may restrict recommendations based on moderation history, user feedback, engagement signals or editorial discretion.
- Ads on Spotlight and Stories are served mainly according to how long people watch (help.snapchat.com monetization page), which indicates watch time matters commercially.
- Ineligible for recommendation (values.snap.com Quality): unoriginal reposts, low-effort reaction content as a pretext to repost, repeated near-identical posts, promotion of other accounts via usernames paired with another app's name or logo, flashes/strobes without warning, AI-generated content created outside Snapchat is ranked lower than human-made even with disclosure.
- Sensitive content may be limited to narrower audiences, not removed; repeat violators can lose reach.

Practitioner observation, not an official rule:
- Completion rate and replays on Spotlight appear to matter most; hook in the first seconds.
- Watermarked TikTok/Reels reposts underperform; consistent with the unoriginal-content rule above.

## 6. Community rules and policy hot spots
Sources: Community Guidelines, Recommendation Eligibility guidelines, Moderation page, Commercial Content Policy, Monetization page.
- Spam: paid follower promotions, follower-growth schemes, spam apps, MLM/pyramid schemes are banned. Buying followers = spam (Community Guidelines).
- Engagement bait: the Quality page does not mention engagement bait or clickbait by name; do not assume they are allowed, as it lists related repetitive/unoriginal patterns.
- Copyright and music: for Spotlight you confirm you created the Snap yourself and hold all rights, including music master/sync/performance rights (Spotlight terms, snap.com/terms/spotlight-terms). Commercial accounts should use only rights-cleared audio. Which in-app sounds are cleared for business accounts: `unverified`; check "Music on Snapchat Guidelines".
- Impersonation: banned when used to pretend to be a person, celebrity, public figure or brand for harmful purposes; satire excluded.
- Health, finance, politics: unsubstantiated medical claims and harmful misinformation are banned. Commercial content: election content and most advocacy/issue content prohibited; diet and fitness cannot target minors or make false food/nutrition claims; financial products (including crypto) must be age-restricted; get-rich-quick and predatory offers are prohibited (Commercial Content Policy).
- Minors: sexualization of minors, grooming and sextortion are zero-tolerance and reported to authorities. Content and products promoted must suit users aged 13+. Users 16-17 have extra safeguards on Public Profiles (help.snapchat.com).
- Regulated goods: restrictions on tobacco, alcohol, vapes, loans/financial products, gambling, weapons, drugs.
- Giveaways/contests: no dedicated organic contest policy found. `unverified`. Treat as commercial content: disclose, follow local law, do not require sensitive data.
- Automation/bots: Community Guidelines do not explicitly address automation but ban inauthentic activity that manipulates the platform. Only use the allowlisted API for publishing (section 8).
- Enforcement: violating content is removed, the account gets a strike, too many strikes within a period typically disable the account; severe harms disable immediately. Strike duration and thresholds are not published. Appeals go through Snap Support; repeated unfounded appeals can lead to a suspension of appeal review for up to a year (values.snap.com moderation).
- Monetization eligibility (invitation only, help.snapchat.com "About Snapchat's Monetization Program"): 50,000 followers; 15,000 view-hours in 28 days with at least 3,000 from Spotlight; age 18 or majority; Snap Star verification; residence in an eligible country; original, advertiser-friendly content. Spotlight must be at least 30 s to earn. From 7 May 2026, at least 100 hours of Total Spotlight View Time in 28 days for maximum Creator Rewards. Cash-out minimum 100 USD. Snap says it never charges for invitations. The eligible-country list was not on the page; whether Egypt is eligible: `unverified`.
- The older Spotlight Rewards programme (qualifying snaps, 1,000 followers) ended 31 January 2025 (snap.com/terms/spotlight-terms). Ignore articles that quote its thresholds.

## 7. Branded content, ads disclosure and legal
Not legal advice. Check local rules before running paid collaborations.
- Snap Commercial Content Policy applies to non-Snap-served content that promotes any brand, product or service, including your own, and to content you are paid or gifted to post.
- Use Snap's paid partnership tool to label commercial content. The label is generally required when you are paid or receive something of value, such as free products. It is not required if you bought the product yourself and no brand compensates you.
- Disclosure must be clear and conspicuous on every relevant Snap. If only the first of several commercial Snaps is disclosed, only that first Snap can be amplified beyond the Public Profile.
- Do not imply Snap endorsement, misuse Snap trademarks or Bitmoji, or use someone's name, likeness or voice without consent.
- If you collect personal data (lead forms, contests), say it is you collecting it and link a privacy policy. Do not collect sensitive data (ethnicity, politics, religion, health, sex life).
- Prohibited commercial content: deceptive claims, counterfeits, fake celebrity endorsements, bait-and-switch links, cloaking, adult content, graphic violence, illegal activity.
- High-level consumer law: advertising must be identifiable as such and not misleading in the EU (Unfair Commercial Practices Directive), the US (FTC Endorsement Guides) and Egypt (Consumer Protection Law 181 of 2018 prohibits misleading advertising; details `unverified`, confirm with counsel). Use a platform label plus a plain-language word such as "ad" or "paid partnership" (in Arabic: "إعلان" or "شراكة مدفوعة").

## 8. API and automation
- Official API for organic: Snap Public Profile API (developers.snap.com/api/marketing-api/Public-Profile-API). It sits inside the Snap Marketing API documentation but is separate from the ads endpoints.
- Capabilities documented: post a Story (`POST /v1/public_profiles/{profile_id}/stories`), post a Spotlight (`POST .../spotlights`), create Saved Stories, upload media with multipart upload, read metrics and creator discovery data, brand-to-creator collaboration messaging (TEXT only; needs a separate allowlist).
- Not documented as supported: reading or replying to public comments, replying to Story replies or friend chats, publishing text-only posts, scheduling endpoints. Treat these as having NO API.
- Access: allowlist only. Create a business account and an OAuth app in Ads Manager (the Developer Portal client ID does not work for this API), then email your Snap contact the client ID and intended use. Never send the client secret.
- Auth: OAuth 2.0 with scope `snapchat-profile-api`; `Authorization: Bearer <token>`. Public endpoints (`/public/v1/...`) need no owner authorization and return only public data; owner endpoints need the profile owner's OAuth consent or opt-in data sharing.
- Rate limits: not stated in the pages read. Treat as `unverified`; implement exponential backoff and a conservative queue.
- Scheduling: no official native scheduling confirmed for Stories or Spotlight (`unverified`). Third-party tools exist; verify they use the allowlisted API rather than credentials or scraping.
- Forbidden: sharing credentials with unapproved tools, automating through the app UI or scraping, inauthentic activity and bought followers (Community Guidelines).
- n8n guidance: use HTTP Request nodes only if the app has been allowlisted; store the token in n8n credentials, never in workflow JSON; log `request_status`; stop on repeated errors rather than retrying blindly.

## 9. Analytics
Where: Insights in the app (Profile > Insights) and Public Profile Insights in the web profile manager. Definitions live in the Snap Insights Glossary (help.snapchat.com/hc/articles/7012336424980). Definitions below paraphrase the Insights help article; unlisted ones are `unverified`.
- Public Stories: viewers and Snap count per Story; per Snap: views, viewers, screenshots, swipe-ups, Story replies, interactions; Snap Views, Average View Time, Total View Time as comparison filters.
- Spotlight: views, favorites, shares, unique viewers, followers gained, reposts, comments, clicks, screenshots; Average View Time, Total View Time, Average View Rate over 7, 28 or 90 days. Favorite counts show only if "Show Favorite Counts" is enabled.
- Audience: follower count; gender and age breakdown appear only above 200 followers.
- UI and API numbers can differ and usually sync after 24 hours (Public Profile API FAQ).
- Which metric answers which question:
  - Is the hook working? Average View Rate and Average View Time on Spotlight.
  - Is the Story sequence too long? Drop in viewers across successive Snaps.
  - Is content being shared? Shares, reposts, screenshots.
  - Is it growing the base? Followers gained per post, subscriber growth.
  - Does it qualify for rewards? Total Spotlight View Time (28 days) under "Daily Rewards Eligibility" in Insights.

## 10. Cases
**Situation:** Views drop sharply after steady Spotlight reach.
**Do:** Check the Insights glossary metrics for the date; compare hook retention; look for notices about strikes or limited distribution; remove recent reposted or watermarked content; check audio was present and orientation vertical; post an original, native video.
**Avoid:** Deleting the whole library, re-uploading the same clip repeatedly (repeated near-identical content is ineligible for recommendation), buying views.

**Situation:** The account is locked or disabled.
**Do:** Use the in-app/Support appeal once, with a factual explanation and the business verification data; record the notice text; check Community Guidelines categories named in the notice.
**Avoid:** Repeated appeals about the same case (can lead to suspended appeal review for up to a year), making a replacement account to bypass the lock.

**Situation:** Music or copyright claim on a Spotlight.
**Do:** Remove or replace the audio with rights-cleared music; keep licence proof; for brands, use commissioned or library tracks with sync rights.
**Avoid:** Assuming popular sounds are cleared for commercial accounts; the Spotlight terms put rights responsibility on you.

**Situation:** Negative comment wave on a Spotlight.
**Do:** Reply once with facts and a support route; remove or report harassment and hate; turn off or limit interaction features if the profile offers them (`unverified` per option); escalate real complaints to support channels.
**Avoid:** Arguing in public, deleting legitimate criticism en masse, using fake accounts to counter.

**Situation:** A fake profile uses the brand name.
**Do:** Report impersonation in-app; collect URL, screenshots and evidence of trademark/business registration; apply for the verified badge route if the business is authentic and notable; warn followers in a Story with your real username.
**Avoid:** Engaging the impersonator, sharing the fake's link widely.

**Situation:** Planning a giveaway.
**Do:** Treat as commercial content: disclose, publish rules (eligibility, dates, prize, winner selection, data use), check local contest/lottery rules, do not collect sensitive data, avoid requiring paid entry.
**Avoid:** "Follow + share to enter" mechanics that look like follower-growth schemes; prizes in regulated categories (alcohol, vapes, gambling).

**Situation:** Cross-posting a Reel or TikTok to Spotlight.
**Do:** Export the original without watermark in 9:16, at least 540x960, with audio; adapt the first seconds and caption (160 chars); re-check music rights.
**Avoid:** Uploading the platform watermark, or letterboxed video, which are not recommended content.

**Situation:** A Story or Spotlight needs correction or removal.
**Do:** Delete it in the app/profile manager, republish the corrected version, keep a note of what changed; for Saved Stories remove the snap from the Story and review the title.
**Avoid:** Silent deletion of a post that made a public promise; edit-by-repost loops that create near-duplicates.

**Situation:** Crisis (product harm, viral complaint).
**Do:** Pause scheduled posts across channels, post a short factual Story, pin a Saved Story with updates, route DMs/complaints to a monitored channel, brief leadership.
**Avoid:** Humor or promotional posting during the crisis, deleting the profile.

**Situation:** Handing over account access to an agency or freelancer.
**Do:** Use Ads Manager roles (contributor/manager/admin) on the Public Profile instead of sharing passwords; enable two-factor authentication (recommended on creators.snapchat.com); document who has access and revoke on exit.
**Avoid:** Sharing the personal Snapchat login, which also controls the person's private chats.

## 11. Arabic and Egypt notes
- Spotlight/Story overlay text in Arabic: RTL rendering inside the Snapchat camera text tool is `unverified`; test on iOS and Android because overlays are baked into the video.
- Dialect: Egyptian Arabic voiceover and captions suit the audience; burn captions into the video because auto-caption reliability for dialect is `unverified`.
- Hashtag habits in Arabic: `unverified`; test with a short list.
- Monetization: Egypt eligibility for the Monetization Program is not stated on the page read; payouts are in USD with a 100 USD minimum cash-out. Payment method availability in Egypt: `unverified`.
- Age: Public Profiles start at 16 in most countries; local law may differ.
- Verified badge (Snap Star / Official Business) is assigned manually after authenticity and notability review; it cannot be bought.

## 12. Pre-publish checklist
1. Is the video vertical, at least 540x960, with sound and no letterboxing?
2. Is the Spotlight 6-60 s (30 s or longer if monetization matters)?
3. Is the description 160 chars or fewer and does it avoid off-platform links to social, messaging or cloud services?
4. Are all music, images, faces and brands cleared for commercial use?
5. Is it original content, with no other platform's watermark or username overlay?
6. If sponsored or gifted, is the paid partnership label applied on every relevant Snap?
7. Are health, finance and political claims removed or substantiated?
8. Is the content suitable for 13+ and not aimed at minors if the category is regulated?
9. Does the first 2 seconds hook, and do flashes or strobes carry a warning?
10. If AI-generated, was it created in Snapchat tools or disclosed, accepting lower ranking otherwise?
11. Is there a plan for replies to comments or messages in the first hour?
12. If using automation, is the app allowlisted and the token stored securely?

## 13. Sources
- https://developers.snap.com/api/marketing-api/Public-Profile-API/Introduction
- https://developers.snap.com/api/marketing-api/Public-Profile-API/ProfileAssetManagement
- https://developers.snap.com/api/marketing-api/Public-Profile-API/GetStarted
- https://developers.snap.com/api/marketing-api/Public-Profile-API/FAQ
- https://developers.snap.com/api/marketing-api/Public-Profile-API/Messaging
- https://help.snapchat.com/hc/en-us/articles/14669003687444-About-Snapchat-s-Monetization-Program
- https://help.snapchat.com/hc/en-us/articles/7012287256596-Spotlight-Guidelines
- https://help.snapchat.com/hc/en-us/articles/7012347065876-What-is-a-Public-Profile-on-Snapchat
- https://help.snapchat.com/hc/en-us/articles/7012390139284-Who-is-eligible-for-a-Public-Profile-
- https://help.snapchat.com/hc/en-us/articles/38529745974036-Why-don-t-I-have-a-Public-Profile
- https://help.snapchat.com/hc/en-us/articles/7012342583188-How-can-I-get-Creator-features-on-Snapchat
- https://help.snapchat.com/hc/en-us/articles/24892451593108-Viewing-and-Understanding-Analytics
- https://help.snapchat.com/hc/en-gb/articles/7012381865236-How-do-I-add-a-Story-to-my-Public-Profile
- https://values.snap.com/policy/policy-community-guidelines
- https://values.snap.com/policy/content-guidelines-recommendation-eligibility
- https://values.snap.com/policy/content-guidelines-recommendation-eligibility/recommendation-eligibility/quality
- https://values.snap.com/privacy/transparency/community-guidelines/moderation
- https://www.snap.com/terms/spotlight-terms
- https://snap.com/terms/commercial-content
- https://forbusiness.snapchat.com/en-US/public-profiles
- https://creators.snapchat.com/getting-started?lang=en-GB
- https://datareportal.com/essential-snapchat-stats (ad reach, January 2025)
