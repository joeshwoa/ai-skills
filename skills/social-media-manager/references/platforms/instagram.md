# Instagram — rules and playbook
Last verified: 2026-10-19

Scope: Feed posts, carousels, Reels, Stories, Broadcast channels, comments, and DMs including automation. Labels: **official** = Meta developer docs, Instagram blog or creator blog fetched on 2026-10-19; **third-party** = secondary reporting or tool-vendor article; **practitioner observation, not an official rule**; **unverified** = not confirmed from a source this session. Instagram's Help Center and Meta's Transparency Center pages are JavaScript-rendered and could not be read, so help-center rules (promotions, monetization, spam wording) are mostly unverified.

## 1. Snapshot
- Egypt: DataReportal (Digital 2026: Egypt, 2025-11-08) lists Instagram ad reach at 21.7M in Oct 2025, up 13.9% year on year, against Facebook 51.6M, TikTok 48.8M (18+), Snapchat 20.6M. Ad reach is not monthly active users. Source: https://datareportal.com/reports/digital-2026-egypt
- Best for: visual brand building, Reels discovery, creator partnerships, Stories for daily contact, DMs for sales conversations, younger urban audiences in Egypt (age split: unverified).
- Account type needed for any API use: Instagram professional account (business or creator).
- Meta's current emphasis: Reels, original content, Trial Reels, collaborations, DMs/Broadcast channels, fewer but more targeted hashtags.

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Feed single image | 4:5 to 1.91:1 accepted by API; width 320 to 1440 px (scaled) | n/a | JPEG only, 8 MB, sRGB | MPO and JPS not supported. `alt_text` up to 1,000 chars (API, image posts only). |
| Carousel | all items cropped to first item's ratio, default 1:1 | video items allowed | each item same rules as image/video | API: up to 10 items, mixed image and video, counts as one post. App: up to 20 items reported by TechRadar (headline, date unconfirmed) so the in-app limit is higher than the API limit. Reels cannot be carousel children. |
| Feed video | unverified | unverified | unverified | API publishes feed videos as Reels (`media_type=REELS`); separate feed-video spec: unverified. |
| Reels | 9:16 recommended (API accepts 0.01:1 to 10:1) | API: 3 s to 15 min. App editor: 3 min announced 2025-01-21 for US creators (before: 90 s); other regions and any later change: unverified | MOV or MP4, 300 MB max via API; H.264 or HEVC, 23 to 60 fps, max width 1920 px, VBR up to 25 Mbps; AAC up to 48 kHz | Cover JPEG 8 MB, 9:16 (non-9:16 is center-cropped). Reels up to 3 min can reach non-followers in the Reels tab and Explore (creators.instagram.com, 2025-01-21); whether longer Reels are recommended: unverified. `share_to_feed` sets eligibility only. |
| Trial Reel | same as Reel | same | same | Shown first to non-followers; `graduation_strategy` `MANUAL` or `SS_PERFORMANCE` (API). |
| Story, image | 9:16 recommended | 24 h life | JPEG, 8 MB, sRGB | API cannot publish link, poll or location stickers; mentions without stickers work. |
| Story, video | 9:16 recommended (0.1:1 to 10:1 accepted) | API 3 to 60 s | MOV or MP4, 100 MB max; H.264/HEVC; 23 to 60 fps | `media_type=STORIES`; captions not supported by API. |
| Live | unverified | unverified | n/a | Live cannot be created by API (no endpoint found). Live comments can be answered only by private reply (API). |
| Broadcast channel | text, photo, video, voice note | n/a | unverified | One-way: only the creator sends; followers react and vote in polls. Channels are public. No member cap stated. Source: about.instagram.com blog (2023-02-16). |
| DM media | n/a | n/a | audio 25 MB (aac, m4a, wav, mp4); image 8 MB (png, jpeg); video 25 MB (mp4, ogg, avi, mov, webm); pdf 25 MB | Official, Messaging API. |
| Cover/profile grid crop | unverified | n/a | n/a | Reports of a 3:4 profile grid in 2025 were not verified. Keep key content centered. |

## 3. Text limits
| Item | Limit | Status |
|---|---|---|
| Caption | 2,200 chars | official (API) |
| Hashtags in a caption | 5 per Reel or post, rolling out gradually from Dec 2025 (was 30). The Instagram API docs I read still say 30 | Instagram statement as reported by Social Media Today (https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/); API text conflicts: treat 5 as the operating limit |
| @mentions in a caption | 20 | official (API) |
| Collaborators on a post or Reel | up to 3 (API) | official |
| Username | 30 chars | third-party (bitly.com) |
| Bio | 150 chars | third-party (bitly.com) |
| Display name | no figure found | unverified |
| Comment | 2,200 chars and a hashtag cap of 30 per third-party; comment-rate spam filters exist | third-party; unverified |
| Alt text | 1,000 chars | official (API) |
| Poll option (feed poll via API) | 1 to 25 chars each, 2 to 4 options | official |
| DM text | 1,000 bytes max, UTF-8 | official (Messaging API) |
| Links | not clickable in captions or comments; clickable in bio, Story link stickers, and ads | practitioner/third-party and long-standing behavior; not re-verified from Meta this session |
| Emoji / Arabic / RTL | UTF-8 supported; mixed RTL and LTR lines can reorder punctuation. Keep hashtags on their own line | emoji and Arabic accepted: practical; reorder detail: practitioner |

## 4. Posting and cadence
- Official: Meta's creator blog says to post original content consistently and gives no numeric frequency (creators.instagram.com, 2025-01-21).
- Rate caps if you automate: 100 API-published posts per rolling 24 h per account (a second place on the same page says 50, so use 50 as the safe ceiling), 400 containers per 24 h, containers expire after 24 h (official).
- Heuristic (practitioner observation, not an official rule): 3 to 5 Reels per week, 2 to 4 feed posts, daily Stories for an active brand; fewer but better beats daily low-effort posts. Use the account's own Insights for timing; Egypt evenings and non-Friday days are a starting hypothesis only.
- Funnel mapping:
  - Awareness: Reels, Trial Reels (reach non-followers first), collaborator posts, remix-friendly audio.
  - Consideration: carousels (education, comparisons), Stories Q&A and polls, Highlights, Broadcast channel for early updates.
  - Conversion: Story link stickers (app only), "DM us" calls to action with a keyword, product tags (not publishable via API), profile link, click-to-DM ads.
  - Retention: Close friends or Broadcast channel for loyal followers, customer UGC, replies to comments and DMs within the 24 h window.

## 5. Distribution and ranking signals
Official:
- Instagram's ranking explainer (Adam Mosseri, 2021, so dated) lists signals by surface. Feed: your activity, information about the post (popularity, speed of engagement, time, location), information about the poster, your history with the poster. Stories: viewing history, engagement history, closeness. Explore: post popularity (likes, comments, shares, saves, speed) most important, your Explore activity, history with poster, poster information. Reels: your activity, history with poster, the reel's audio, visuals and popularity, poster information (follower count, engagement). Source: https://about.instagram.com/blog/announcements/instagram-ranking-explained
- Jan 2025 creators post: Reels recommendation was updated in 2024 so creators of all sizes have an equal chance; Reels up to 3 min (previously 90 s) can be recommended to non-followers; Trial Reels let a Reel go to non-followers first; audio added to photos and carousels can appear in the Reels tab; each unique audio mix is credited to its creator.
- Hashtags: Instagram says fewer, targeted hashtags (up to 5) help; Mosseri said in Feb and May 2025 that hashtags do not increase reach and only help show what a post is about (as reported by Social Media Today).
- Originality: Instagram's "About original content" help page exists (https://help.instagram.com/1800814370401535/) but its text was not readable; Facebook's parallel 2025 policy penalizes reposted and watermarked content (see facebook.md). Treat reposted or watermarked content on Instagram as at risk of reduced recommendation: unverified wording.

Practitioner lore (practitioner observation, not an official rule):
- Shares by DM, saves and watch time matter more than likes for Reels.
- First-3-seconds hook and a loop-friendly ending help retention.
- Watermarks from other apps reduce recommendation.
- Posting several Reels in one hour cannibalizes each one.

## 6. Community rules and policy hot spots
- Community Guidelines (official FAQ page, https://about.instagram.com/blog/announcements/instagram-community-guidelines-faqs): nudity is not allowed with named exceptions (post-mastectomy scarring, active breastfeeding, art such as paintings and sculptures); spam is prohibited including unwanted commercial comments, messages and likes; users must have rights to what they post; Instagram may remove content and disable entire accounts. That page does not cover strikes, appeals or minors: those details are unverified.
- Spam and fake engagement: buying followers, likes, comments, or using engagement pods and mass follow/unfollow tools is a restriction risk. Exact Terms wording not readable: unverified. Meta's Spam and Inauthentic Behavior policy pages exist (section 13).
- Copyright and music: Business-account music licensing limits in the Instagram music library are unverified. API: music tagging works only with original audio (official), `audio_name` can be renamed once.
- Impersonation: an account pretending to be a brand or person is removable; reporting flow wording unverified. Meta Verified and professional-account category help; details unverified.
- Health, finance and political claims: Meta Misinformation and Fraud policies and ad policies apply; exact rules unverified. Never promise returns, cures or "guaranteed results".
- Minors: Instagram's minimum age is 13 (consistent with Meta API `age_min` floor of 13 in the Reels API); teen-account restrictions on DMs and tagging: unverified. Do not feature or DM minors for promotions without a guardian and a lawful basis.
- Giveaways: Instagram Promotion Guidelines page is not readable: unverified. Apply the conservative rules in section 10 (official rules, no false tagging, no required Likes of unrelated pages, Meta-not-sponsor statement, local law).
- Automation and bots: official rules are in the Messaging API and Messenger policy: the user must message first, 24 h window, human handoff, automation disclosure where required by law (California and Germany named), and a recommendation to disclose even when not required. Automation of likes, follows, comments or scraping through unofficial tools is against the Instagram Terms (page not readable): unverified wording, high account-risk in practice.
- Branded content: partnership labels are mandatory in practice when a brand pays or gifts; see section 7.
- Account status: Instagram publishes an "Understanding Instagram outages and account status" page (https://about.instagram.com/blog/announcements/instagram-outages-and-account-status); content unread.

## 7. Branded content, ads disclosure and legal
Not legal advice.
- Tools: paid partnership label and partnership ads. Via API (Facebook Login only): `is_paid_partnership` and `branded_content_sponsor_ids` (max 2 sponsors per post); not allowed on close-friends-only posts or remixed media; errors `INSTAGRAM_PLATFORM_API__PERMISSION` (creator not eligible for branded content) and `INSTAGRAM_PLATFORM_API__INVALID_PARAM` (sponsor cannot be tagged, more than 2 sponsors, or creator tagged themselves).
- Eligibility page for partnership ads: https://help.instagram.com/1372533836927082 (not readable: unverified).
- US FTC: disclose any material connection including free products; put it clearly and early, in plain words ("ad", "sponsored", "paid partnership"); in Stories overlay long enough to read; in video put it in the video not only in the caption; hashtags such as #ad are optional extras and must not be buried; platform label alone is not enough; the influencer carries responsibility. Source: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- EU: hidden advertising is generally prohibited under consumer-protection law and national rules differ: unverified here.
- Egypt: sending marketing to people without consent falls under Law 151/2020 and Law 175/2018 article 25 (DLA Piper summary). Influencer licensing and ad-disclosure rules: unverified.
- AI content: the API exposes `is_ai_generated` (carousel container only; not on children). Set it honestly when media is AI-generated or edited.

## 8. API and automation
- Two official routes: **Instagram API with Instagram Login** (host `graph.instagram.com`, permissions `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_insights`, `instagram_business_manage_messages`, no Facebook Page required) and **Instagram API with Facebook Login** (host `graph.facebook.com`, permissions `instagram_basic`, `instagram_content_publish`, `instagram_manage_insights`, `instagram_manage_comments`, `pages_read_engagement`, `pages_show_list`; needed for hashtag search, product tagging and partnership ads). Messaging also runs through the Messenger Platform for Facebook-linked accounts.
- Auth: OAuth. Authorization code valid 1 h, short-lived token 1 h, long-lived token 60 days and refreshable. Standard Access for accounts you own or manage; Advanced Access for other people's accounts requires App Review and Business Verification.
- Publish: image (JPEG), carousel, Reels, Trial Reels, Stories via container then `media_publish`. Media must be at a public URL when you publish. Poll container `status_code` about once per minute for at most 5 minutes (`IN_PROGRESS`, `FINISHED`, `PUBLISHED`, `ERROR`, `EXPIRED`). If the connected Page requires Page Publishing Authorization (PPA), publishing is blocked until it is done.
- Cannot publish via API: shopping tags, filters, link/poll/location stickers on Stories, captions on Stories, alt text on Reels and Stories, Reels in carousels, Live. Collaborators up to 3 are supported.
- Scheduling: no `scheduled_publish_time` parameter appears in the publishing docs read. Scheduling = your own queue calling `media_publish` at the time (rate-limit aware), or Instagram app / Meta Business Suite scheduling (UI limits unverified).
- Comments: create a top-level comment with `POST /{ig-media-id}/comments`; reply with `POST /{ig-comment-id}/replies` (top-level comments only, not hidden comments, not live-video comments). Hide and delete endpoints exist under `instagram_manage_comments` (not read: unverified).
- Insights: metrics listed in section 9; webhook `story_insights` is not supported under Instagram Login.
- Messaging (DMs): the user must message your professional account first; window 24 h, up to 7 days after a Click-to-Direct ad; `HUMAN_AGENT` tag gives 7 days for a human reply; Private Replies: one message per comment within 7 days; can send text, images, video, audio, pdf, your own posts, reactions, stickers, links, templates; no group messaging; requests-folder conversations inactive 30 days are not returned; Marketing, Sponsored and One-Time Notification options are Messenger-only. Rate limits: Conversations API 2 calls/s, Send API 300 calls/s text and 10 calls/s audio/video, Private Replies 750 calls/hour for post and Reel comments, 100 calls/s for Live comments; above 72,000 sent and received messages the Inbox stops showing new messages until volume drops (official, Messenger rate-limit page).
- Platform rate limits: most endpoints use Business Use Case limits, calls per rolling 24 h = 4800 x impressions; hashtag search and business discovery use platform limits. Publishing: 100 posts per 24 h (page also states 50; use 50 to be safe), 400 containers per 24 h; check `GET /<IG_ID>/content_publishing_limit`.
- Forbidden automation: unofficial bots that like, follow, comment, DM cold, or scrape; reselling accounts; bypassing the 24 h window with tags for promotion. Official: tags may not carry promotional content (Messenger policy).
- n8n pattern (safe): schedule trigger, upload to public storage, create container, wait and poll, publish, log result; read comments by webhook; reply with a human-approved template; hand over DMs to a human after the first automated answer.
- No API: Instagram Live creation, Notes, Edits-app features and Broadcast channel posting (no endpoints found in the docs read; Broadcast channel API status is unverified).

## 9. Analytics
- Where: Instagram app Professional Dashboard / Insights, Meta Business Suite, Insights API.
- Media metrics (official): `reach` (unique accounts, estimated); `views` (times the media was played or shown; replaces `impressions` and `plays`); `likes`, `comments`, `saved`, `shares`; `total_interactions` (likes, saves, comments, shares minus unlikes, unsaves and deleted comments); Reels: `ig_reels_avg_watch_time`, `ig_reels_video_view_total_time`, `reels_skip_rate`; `follows`, `profile_visits` for feed and Stories; Stories: `navigation` (total actions taken from a story, with a `story_navigation_action_type` breakdown), `replies` (returns 0 for stories by users in Europe from 2020-12-01 and Japan from 2021-04-14).
- Rules: `impressions` is deprecated for media created after 2024-07-02; insights can lag up to 48 h; media metrics retained up to 2 years; user-level metrics up to 90 days; missing data returns an empty set, not 0; no insights for media inside an album; Story metrics available for 24 hours (capture them early); values below 5 return error code 10; some account metrics are unavailable below 100 followers; `likes`, `comments`, `views`, `total_interactions` are organic only.
- Question to metric: Are new people seeing it? Reels `reach` and `views`. Is the hook working? `ig_reels_avg_watch_time` and `reels_skip_rate`. Is it worth sharing? `shares` and `saved`. Does it bring followers or profile traffic? `follows`, `profile_visits`. Are Stories sticky? `navigation` exits vs forwards, `replies`. Is the DM funnel working? count of conversations opened versus replies within 24 h (from your own logs).

## 10. Cases
**Situation 1: Reach suddenly drops.**
**Do:** Compare `reach` and `views` of the last 10 Reels against the previous 10; check whether the account has a warning, restriction or "not eligible for recommendations" notice in Account Status (path: unverified); look for reposted, watermarked or off-topic content; return to original Reels with a strong first 3 seconds; try Trial Reels to test non-follower reception.
**Avoid:** Posting 10 Reels a day, changing niche overnight, buying followers, blaming a "shadowban" without checking account status and Insights.

**Situation 2: Account restricted, flagged or action-blocked.**
**Do:** Stop all automation immediately; revoke third-party app access and unknown logins; change the password and enable two-factor on the owner; follow the in-app appeal; note the date and the reason shown; inform the client.
**Avoid:** Running more bot or scheduler tools, creating a second account to bypass the block, sharing passwords with freelancers.

**Situation 3: Copyright or music claim on a Reel.**
**Do:** Replace the audio with licensed or original audio, keep licence proof, use the in-app dispute when the claim is wrong; for business accounts use only audio you can prove rights to (library limits: unverified).
**Avoid:** Re-uploading the same file repeatedly, using commercial songs in paid partnership posts without clearance.

**Situation 4: Negative comment wave.**
**Do:** Reply once publicly and calmly to genuine complaints, move details to DM, hide abusive or spam comments, use Restrict for repeat offenders, keep a screenshot log, brief the client; the API can reply to top-level comments (not to hidden comments).
**Avoid:** Deleting every critical comment, auto-replying with canned text to everyone, arguing in captions.

**Situation 5: Fake or scam impersonator account.**
**Do:** Screenshot the profile and URL; report via the profile menu (Report > impersonation, wording unverified); pin a Story highlight "Our only official account"; warn followers that the brand never asks for payment by DM; reply to the scammer's victims through DM with the official contact.
**Avoid:** Engaging with the fake account, sharing its link as a clickable item, public accusations without proof.

**Situation 6: Giveaway planning.**
**Do:** Written rules (eligibility, dates, prize, how a winner is picked, data use), entry by comment or form, a statement that Instagram/Meta does not sponsor or endorse the promotion, delivery proof, client legal check (Instagram promotion guidelines page not readable: unverified). In Egypt keep entrant data only as needed and with consent (Law 151/2020).
**Avoid:** Requiring entrants to tag unrelated accounts, to post a specific hashtag from personal pages for extra entries at scale, to buy anything, or to follow ten sponsor accounts.

**Situation 7: Cross-posting from TikTok or YouTube Shorts.**
**Do:** Export without the other platform's watermark; recompose safe areas for Reels (9:16, 1080x1920); rewrite the caption; use at most 5 hashtags; keep Reel under 3 min; add the brand's own audio or captions in Arabic.
**Avoid:** Re-posting the watermarked file, copying a 30-hashtag block, using audio that is licensed only for the source platform.

**Situation 8: A published post must be edited or deleted.**
**Do:** Edit the caption in the app for typos (API publishes only); if a claim is wrong or harmful, delete and replace with a corrected post, and archive the original text and time in the client log; use Archive instead of Delete when the post is only off-brand.
**Avoid:** Silent deletion of a post with many comments on a crisis topic, editing a caption so the comments lose context.

**Situation 9: Crisis (product harm, viral complaint, outage).**
**Do:** Pause scheduled posts and ads, post one Story and one feed statement, turn on comment filters, send DMs through a human using the 24 h window or `HUMAN_AGENT` 7 days, appoint one approver, give updates at fixed times.
**Avoid:** Cheerful pre-scheduled content, automated DM replies that deny the problem, deleting reports.

**Situation 10: DM automation (comment-to-DM keyword flows).**
**Do:** Use Private Replies (one message, within 7 days of the comment, 750 calls/hour limit), give a clear automated-service disclosure at the start of the thread, offer "talk to a human", respond within the 24 h window, log consent for marketing.
**Avoid:** Cold DMs, sending promotions with message tags, ignoring the 24 h rule, running unofficial DM bots.

**Situation 11: Handing over account access safely.**
**Do:** Convert to a professional account, connect it to a Meta Business portfolio and Page, add the agency as partner with limited tasks, use Meta Business Suite, keep the owner as admin, keep two-factor on the owner login, remove access on exit.
**Avoid:** Sharing a username and password in chat, leaving the account tied to a personal Facebook profile only, letting an agency become the sole owner.

## 11. Arabic and Egypt notes
- Arabic captions: Instagram accepts UTF-8 Arabic and emoji; paragraphs follow the first strong direction, so start with Arabic for Arabic posts and put English brand names or numbers inside the sentence carefully; check the preview of mixed lines in the app (reorder behavior: practitioner observation).
- Hashtags: the effective cap is now 5. Use one brand tag, one Arabic topic tag, one English topic tag, one city tag (for example Cairo) and one campaign tag. Arabic hashtags work but diacritics and ta marbuta vs ha variants split the tag: choose one spelling and keep it (practitioner observation, not an official rule).
- Dialect: Egyptian dialect for Reels voice and captions, Modern Standard Arabic for formal announcements; keep burned-in captions legible, 2 lines maximum, safe area above the bottom UI.
- Etiquette: avoid religious jokes, politically loaded content, and imagery unsuitable for conservative audiences; Ramadan and Eid need dedicated calendars (practitioner observation).
- Audience reach: Instagram ad reach 21.7M versus Facebook 51.6M in Egypt: do not drop Facebook for Instagram-only plans.
- Data law: Law 151/2020 requires explicit consent for direct electronic marketing and keeps consent records for 3 years; Centre licence required for electronic marketing activities (DLA Piper, modified 2026-02-13). Applies to DM and contest data.
- Payments and verification: Meta Verified and ad billing availability or local payment methods in Egypt: unverified. Egyptian influencer-licensing rules: unverified.

## 12. Pre-publish checklist
1. Is the media original, without another app's watermark, and with rights to music and people shown?
2. Reel: 9:16, 1080x1920, 3 s or more, under 3 min, MP4 or MOV, under 300 MB (API)?
3. Feed image: JPEG, ratio between 4:5 and 1.91:1, under 8 MB?
4. Caption under 2,200 characters with at most 5 hashtags and at most 20 mentions?
5. First 125 characters carry the hook (the rest may be cut in feed)?
6. Is alt text added for accessibility (up to 1,000 chars)?
7. If sponsored: paid partnership label set, "Ad" visible in the first lines or on the video, and a maximum of 2 sponsors tagged?
8. Do claims (health, finance, results) have approval and proof?
9. Any minors, ID documents, license plates or phone numbers visible?
10. Is `is_ai_generated` set when AI content is used?
11. Is the publish time within the daily cap (50 to 100 posts, 400 containers) and is the container used within 24 h?
12. Is a human assigned to answer comments and DMs within 24 h of publishing?

## 13. Sources
- https://datareportal.com/reports/digital-2026-egypt
- https://developers.facebook.com/documentation/instagram-platform/content-publishing
- https://developers.facebook.com/documentation/instagram-platform/content-publishing.md
- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
- https://developers.facebook.com/docs/instagram-platform/overview/
- https://developers.facebook.com/docs/instagram-platform
- https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/messaging-api
- https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-comment/replies
- https://developers.facebook.com/documentation/instagram-platform/reference/instagram-media/insights
- https://developers.facebook.com/documentation/instagram-platform/insights
- https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy
- https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview/rate-limiting
- https://creators.instagram.com/blog/the-latest-with-instagram
- https://about.instagram.com/blog/announcements/instagram-ranking-explained
- https://about.instagram.com/blog/announcements/introducing-broadcast-channels/
- https://about.instagram.com/blog/announcements/instagram-community-guidelines-faqs
- https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/ (third-party reporting of Instagram statement)
- https://techbuild.africa/instagram-posts-and-reels-to-five-hashtags/ (third-party)
- https://bitly.com/blog/instagram-character-limit/ (third-party; bio and username limits)
- https://www.techradar.com/computing/instagram/instagram-will-now-let-you-post-up-to-20-photos-or-videos-in-a-gallery-your-friends-should-be-thrilled (headline only, not opened)
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.dlapiperdataprotection.com/index.html?t=law&c=EG
- Not readable this session: https://help.instagram.com/1038071743007909 , https://help.instagram.com/1800814370401535/ , https://help.instagram.com/1372533836927082 , https://help.instagram.com/581066165581870 , https://transparency.meta.com/features/explaining-ranking/ig-feed-recommendations/
