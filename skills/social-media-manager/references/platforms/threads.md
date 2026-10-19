# Threads — rules and playbook
Last verified: 2026-10-19

Labels: `official` = Meta developer docs or Meta newsroom/help page read on 2026-10-19; `secondary` = third party; `unverified` = not confirmed. Threads help pages on help.instagram.com returned only short metadata, so consumer-app rules are thinly sourced; the API docs are the strongest source.

## 1. Snapshot
- What it is: Meta's text-first social app (launched July 2023, tied to Instagram). Best for conversational brand voice, creator and community building, quick opinions, real-time reactions, and recycling Instagram audiences. Posts can also be shared to the fediverse (Mastodon and other ActivityPub servers).
- Egypt: Threads ad reach 3.15 million in late 2025 (2.7% of the population); no growth figure given. For comparison X is 4.64M and LinkedIn 15.0M in Egypt. Ad reach is not active users. Source DataReportal Digital 2026 Egypt https://datareportal.com/reports/digital-2026-egypt
- Arab world: no other sourced figures. `unverified`
- Surfaces: posts, replies, reposts, quotes, polls, topic tags, ghost posts (24 h), text attachments (long text), fediverse sharing, Community Notes (US-first).

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Text post | n/a | 500 characters | emojis count by UTF-8 bytes (API docs) | `official` https://developers.facebook.com/documentation/threads/posts |
| Text attachment (long text) | n/a | up to 10,000 characters plus one link | text-only posts, not with polls | Bold, italic, highlight, underline, strikethrough styling via API. Announced Sept 2025. Rollout regions not stated. |
| Image | ratio up to 10:1; width 320-1440 px (scaled) | n/a | JPEG or PNG, 8 MB, sRGB | `official` API docs |
| Video | 9:16 recommended; allowed 0.01:1 to 10:1; max width 1920 px | up to 300 seconds (5 min) | MOV or MP4, up to 1 GB; H.264 or HEVC, AAC audio, 23-60 fps, up to 100 Mbps | `official` API docs |
| Carousel | per item rules above | 2 to 20 items (images, videos or mixed) | per item | Counts as one post toward API limits. |
| Poll | n/a | duration not stated in API page | 2 to 4 options, 1 to 25 characters each (API) | Text-only posts. Not shared to the fediverse. |
| GIF | n/a | n/a | GIPHY only; text-only posts via API | No numeric limit stated. |
| Topic tag | n/a | 1 to 50 characters; no periods or ampersands | one per post | See section 3. |
| Ghost post | n/a | auto-archived after 24 hours | text only via API; cannot reply; only text spoilers | Replies go to messages; only the author sees likes and repliers. `official` Meta newsroom Oct 2025. |
| Spoiler | n/a | n/a | n/a | Supported (text spoilers via API). |
| Story/status, Live, channel | not available | n/a | n/a | No equivalent verified. Instagram link-sharing to Stories exists via API (`share-to-ig-stories` doc, not read). |

## 3. Text limits
- Post: 500 characters; emojis count by UTF-8 bytes (API docs). Arabic character and RTL counting behaviour `unverified`; test with a real Arabic draft before bulk scheduling.
- Text attachment: 10,000 characters plus one link.
- Caption: n/a (the text is the post). Title: none. Bio and username limits: `unverified`. Replies: assumed same as posts; `unverified`.
- Hashtags / topic tags: one topic per post ("up to 1 topic per post", Threads Help https://help.instagram.com/1356090605000312). API topic_tag 1-50 chars; in-text tags start with `#`, only the first valid tag is used, and tags end at space, tab, newline, period, ampersand, @, !, ?, comma, semicolon, colon; plain numbers like #1 are not converted. Treat `#` as a topic tag, not a classic multi-hashtag system.
- Mentions: `@username` works; mentions API lists public posts that tag your account. Maximum per post `unverified`.
- Links: clickable. Link attachments only on text-only posts; at most 5 unique links per post (API fails with THREADS_API__LINK_LIMIT_EXCEEDED since 2025-12-22); if no `link_attachment` is set the first link becomes the preview.
- Reply controls (API `reply_control`): everyone, accounts_you_follow, mentioned_only, parent_post_author_only, followers_only. Reply approvals can hold replies until approved.

## 4. Posting and cadence
Heuristic (not official):
- Brand accounts: 1 to 3 posts a day is a workable range; replies to your own thread and to others are the main growth action. Do not exceed the API limits below (250 posts per 24 h); real accounts should stay far below.
- Timing: no official data. For Egypt, test mornings (08:00-10:00) and evenings (20:00-23:00) Cairo time, then follow your analytics.
- Funnel:
  - Awareness: one-idea text posts, opinions, short vertical video, polls, topic-tagged posts.
  - Consideration: carousels explaining how a product works, text attachments for long takes, Q&A replies.
  - Conversion: a single link post (limit of 5 links), a pinned reply with the offer.
  - Retention: replying to every thoughtful comment within hours, community prompts, behind-the-scenes.
- Drafts: up to 100 drafts (Meta announcement, Aug 2024). Native scheduling was announced as a test in Aug 2024; current availability `unverified`.

## 5. Distribution and ranking signals
Official: Meta has not published a ranking formula for Threads in the sources read. `unverified`
- Reply controls and approvals give you moderation control. Ghost posts are not publicly distributed beyond the 24-hour window.
- Community Notes: US-first rollout across Facebook, Instagram and Threads starting April 2025; notes need cross-viewpoint agreement; notes do not reduce distribution; contributors must be 18+ with an account over six months old.

Practitioner lore (practitioner observation, not an official rule): replies and conversations are weighted over likes; topic tags help discovery; Instagram followers seed early reach; early replies within the first hour help; posting several unrelated posts in a burst splits attention. None of these is confirmed by Meta in the sources read.

## 6. Community rules and policy hot spots
- Rulebook: Threads is reported to apply Instagram's Community Guidelines (statement from a Meta AI post on Threads, `secondary`); the guideline text was not read. Assume the usual categories: spam and fake engagement, hate and harassment, nudity, dangerous organizations, regulated goods, misinformation, impersonation, intellectual property.
- Spam / engagement bait / buying followers: treat as prohibited; exact Threads wording `unverified`.
- Copyright and music: use only licensed audio; no Meta music library for Threads verified. `unverified`
- Impersonation: report the profile; verified-badge programs `unverified` for Threads.
- Health, finance, political claims: Meta's misinformation policies apply in general; Community Notes in the US. Add disclosure and avoid unsubstantiated claims. Details `unverified`.
- Minors: Meta sets a minimum age; the Threads-specific minimum `unverified`; never target minors with advertising-like content.
- Giveaways/contests: Meta has contest rules for Instagram and Facebook; whether they bind Threads `unverified`. Use clear terms and avoid mandatory tagging and spam mechanics.
- Automation and bots: publish through the official Threads API only. Scraping and automated logins are not permitted by Meta's terms in general; Threads-specific terms `unverified`. Do not auto-reply in bulk or use bots to follow/unfollow.
- Fediverse: only top-level posts and self-replies are shared; polls and posts with reply controls are not (TechCrunch, 2024). Fediverse sharing is for adults with public profiles and was not available in the European region at the June 2025 announcement.

## 7. Branded content, ads disclosure and legal
- Meta branded content tools exist on Instagram and Facebook; their application to Threads posts `unverified` in the sources read. Always disclose in plain words in the post text ("Ad", "Sponsored", "Paid partnership with X"), in the same language as the post.
- US FTC: disclose any material connection, place disclosure with the endorsement, use plain words, the influencer and brand are both responsible https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- EU: ads must be identifiable as ads. Egypt: Consumer Protection Law No. 181/2018 (misleading advertising) and Personal Data Protection Law No. 151/2020 (marketing data); Law 180/2018 was reported in 2018 to treat social accounts with 5,000+ followers as media outlets. Not legal advice; consult local counsel.

## 8. API and automation
Official: Threads API, `graph.threads.net` or `graph.threads.com`. Docs https://developers.facebook.com/documentation/threads/overview
- What it can do: publish text, image, video, carousel; text attachments, polls, ghost posts, spoilers; quote and repost; reply (create replies); read the user's own posts and replies; hide replies, reply controls, approve pending replies; insights; mentions; keyword and topic-tag search; delete posts; webhooks; oEmbed; profile lookup.
- What it cannot do (not present in the documentation index): DMs; scheduling (no scheduled-publish parameter documented - hold and publish from your own scheduler); edit a published post (no edit endpoint listed). `unverified` for edit.
- Auth: OAuth user tokens. Short-lived token 1 hour; long-lived 60 days via server-side exchange (`th_exchange_token`); refresh with `th_refresh_token` once the token is at least 24 hours old and not expired, giving another 60 days; an unrefreshed token expires after 60 days. Private-profile permissions valid for 90 days.
- Permissions: `threads_basic` (all calls), `threads_content_publish`, `threads_read_replies`, `threads_manage_replies`, `threads_manage_insights`, `threads_manage_mentions`, `threads_keyword_search`, `threads_delete`, `threads_location_tagging`.
- Access gates: without Advanced Access you can post only for Threads testers on your app; after App Review you can post for any user who authorizes. Keyword search covers only your own posts until `threads_keyword_search` is approved. Mentions return only testers' mentions until `threads_manage_mentions` has advanced access. Webhooks require advanced access, a published app and a verified business. Publishing the app needs an icon, privacy policy URL, data-deletion URL, and DPO contact if you do business in the EU.
- Limits per 24-hour moving window (official overview page): 250 API-published posts (carousel = 1); 1,000 replies; 100 deletions; 500 location searches. Check usage with `GET /{threads-user-id}/threads_publishing_limit`. Your app should enforce these itself, especially for scheduled posts. General call limit: 4,800 x impressions calls per 24 h (impressions minimum 10), plus CPU-time limits. Keyword search: 2,200 queries per user per rolling 24 h across all apps; empty results do not count; sensitive keywords return empty.
- Fediverse: eligible posts made through the API are also shared to the fediverse for users who enabled sharing (since 2024-08-28).
- n8n: use an HTTP Request node with the container-then-publish pattern (`POST /{user-id}/threads` then publish). Store the long-lived token in a credential, refresh it monthly, and check `threads_publishing_limit` before bulk runs. Wait for media container processing before publishing (exact wait time `unverified`).
- Forbidden: spam, fake accounts, bulk unsolicited replies, reselling data. Meta Platform Terms apply; Threads-specific automation clause `unverified`.
- Official scheduling options in the product: drafts (up to 100); native scheduling status `unverified`.

## 9. Analytics
- Post insights (API): views, likes, replies, reposts, quotes, shares (views and shares marked "in development" in docs); nested replies not counted.
- User insights: views (time series), likes, replies, reposts, quotes, clicks (by link URL), followers_count, follower_demographics (country, city, age or gender; needs 100+ followers; one breakdown per call). Requires `threads_manage_insights`. `since` timestamps before 2024-04-13 are rejected; default window is 2 days.
- Native app insights exist (views, replies, reposts, quotes, follower growth and demographics announced Aug 2024).
- Which metric answers what: reach/interest = views; conversation = replies and quotes; share of voice = reposts; click intent = clicks per URL; audience fit = follower demographics.

## 10. Cases
**Situation:** Reach or replies fall sharply.
**Do:** Check insights views and replies per post by format; look for a burst of near-identical posts; review whether recent posts used heavy links (only 5 allowed) or off-topic tags; test text posts with a question and a topic tag; wait for a week of data.
**Avoid:** Posting more of the same, mass tagging, buying engagement.

**Situation:** Account restricted or content removed.
**Do:** Read the in-app notice (Threads follows Instagram Community Guidelines reportedly); pause scheduled posts; use the in-app appeal or review request; check linked Instagram account status; document which posts were flagged.
**Avoid:** Creating a new account to continue, or appealing repeatedly with copy-pasted text.

**Situation:** Copyright or music claim on a video.
**Do:** Take down the post, replace audio with licensed or original audio, keep proof of license; re-upload as a new post.
**Avoid:** Re-uploading the identical file, using trending audio from other apps.

**Situation:** Negative reply wave.
**Do:** Set `reply_control` (or the in-app reply controls) to followers only or mentioned only, turn on reply approvals for the next post, hide abusive replies (`manage_reply`), report threats, answer legitimate complaints once with a support route.
**Avoid:** Deleting the whole post, replying to trolls, arguing in the thread.

**Situation:** Impersonator or scam account copying the brand.
**Do:** Screenshot, report the profile, post a pinned notice of official accounts (and the same on Instagram), alert customer support and followers.
**Avoid:** Sharing the impostor's handle in posts, replying to it.

**Situation:** Planning a giveaway.
**Do:** Write rules (eligibility, dates, prize, how winners are chosen, data use) on a page; ask for one simple action such as replying with an answer; disclose any sponsor; check Meta contest rules for Instagram/Facebook, as Threads-specific rules are `unverified`; follow local contest law.
**Avoid:** Requiring tagging of friends, automated entry collection, over-collecting personal data.

**Situation:** Cross-posting from Instagram or X.
**Do:** Rewrite in conversational tone under 500 characters; reupload native media (9:16 video up to 5 min, images up to 8 MB); use one topic tag; avoid pasted tweet screenshots; if sharing from Instagram, make sure the link and aspect ratio fit.
**Avoid:** Copy-pasting 280-character threads, "link in bio", multiple hashtags in a row.

**Situation:** A post must be corrected or deleted.
**Do:** Edit via the app's edit feature if available (window `unverified`); otherwise reply with a correction or delete and repost; delete via API with `threads_delete` (100 deletions per 24 h).
**Avoid:** Mass deleting posts (the quota is 100/24 h and looks suspicious).

**Situation:** Crisis or brand-safety event.
**Do:** Pause scheduled/auto posts; prepare one statement; use reply controls and approvals; assign a human to read replies; keep a log.
**Avoid:** Ghost posts for official statements (they vanish after 24 hours), auto-replies.

**Situation:** Handing over account access.
**Do:** Use the company Instagram/Threads account with 2FA owned by the business; for API access, register a company Meta developer app, add the agency as an app role (tester/developer) and use Advanced Access only after App Review.
**Avoid:** Sharing a personal Instagram password or long-lived tokens in chat.

## 11. Arabic and Egypt notes
- Threads supports Arabic text; RTL and mixed-language rendering, plus byte vs character counting for Arabic, are `unverified`. Emojis count by UTF-8 bytes in the API docs, so emoji-heavy Arabic posts near 500 characters may be rejected; test.
- Topic tags: one per post; Arabic topic tags work as plain words (single token, no spaces); no punctuation. Use one clear topic rather than many hashtags.
- Etiquette: conversational, short; Masri dialect works for brand voice; avoid political and religious controversy; respect holidays.
- Reach: 3.15 million ad reach in Egypt, so audience is smaller than LinkedIn and X in Egypt; tie Threads to your Instagram audience.
- Fediverse: sharing was not available in the European region at the June 2025 announcement; Egypt is outside that exclusion but availability `unverified`.
- Verification and payments: Threads has no payment features for brands here; Meta Verified availability in Egypt `unverified`.

## 12. Pre-publish checklist
1. Is the text 500 characters or less (including emoji bytes), or is the long text in a text attachment (up to 10,000 characters)?
2. Is there at most one topic tag, 1-50 characters, without periods or ampersands?
3. Are links at most 5 unique URLs, and is the intended link the first one (for the preview)?
4. Is media within limits (image 8 MB JPEG/PNG; video 5 min, 1 GB, MP4/MOV; carousel 2-20 items)?
5. Is vertical video 9:16 where possible?
6. Is paid or gifted content disclosed in plain words?
7. Is the reply control set correctly (everyone vs followers vs mentioned) and approvals on for risky topics?
8. Is the post not a duplicate of another recent post or a bulk-reply pattern?
9. Is the Arabic text preview correct (direction, punctuation, emoji count)?
10. Is publishing through the official API with a valid (not expired) token, and is `threads_publishing_limit` under quota?
11. Is the post free of claims that need substantiation (health, finance, legal)?

## 13. Sources
- https://developers.facebook.com/documentation/threads/overview
- https://developers.facebook.com/documentation/threads/posts
- https://developers.facebook.com/documentation/threads/create-posts.md
- https://developers.facebook.com/documentation/threads/create-posts/text-attachments.md
- https://developers.facebook.com/documentation/threads/create-posts/polls.md
- https://developers.facebook.com/documentation/threads/create-posts/ghost-posts.md
- https://developers.facebook.com/documentation/threads/posts/reposts.md
- https://developers.facebook.com/documentation/threads/insights.md
- https://developers.facebook.com/documentation/threads/reply-management.md
- https://developers.facebook.com/documentation/threads/keyword-search.md
- https://developers.facebook.com/documentation/threads/threads-mentions.md
- https://developers.facebook.com/documentation/threads/webhooks.md
- https://developers.facebook.com/documentation/threads/get-started/long-lived-tokens.md
- https://developers.facebook.com/documentation/threads/get-started/get-access-tokens-and-permissions.md
- https://developers.facebook.com/documentation/threads/get-started/create-an-app.md
- https://developers.facebook.com/documentation/threads/llms.txt
- https://help.instagram.com/1356090605000312 (topic tags)
- https://about.fb.com/news/2024/08/new-threads-features-for-creators-and-businesses/
- https://about.fb.com/news/2025/09/attach-text-threads-posts-share-longer-perspectives/ (via socialsamosa summary)
- https://www.socialsamosa.com/news-2/threads-rolls-out-long-form-text-option-9986486 (secondary)
- https://about.fb.com/news/2025/10/introducing-disappearing-posts-on-threads/
- https://about.fb.com/news/2025/03/testing-begins-community-notes-facebook-instagram-threads/
- https://techcrunch.com/2024/06/25/all-threads-users-can-now-share-to-the-open-social-web-aka-the-fediverse (secondary)
- https://www.elevenforum.com/t/now-easier-to-see-more-fediverse-content-on-threads.37129/latest (copy of Meta newsroom post, secondary)
- https://datareportal.com/reports/digital-2026-egypt
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
