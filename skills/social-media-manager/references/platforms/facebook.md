# Facebook — rules and playbook
Last verified: 2026-10-19

Scope: Facebook Pages (main focus), Groups, Meta Business Suite, and Messenger as it relates to Pages. Labels used below: **official** = Meta developer docs or Meta blogs fetched on 2026-10-19; **third-party** = secondary site, not a Meta rule; **practitioner observation, not an official rule**; **unverified** = could not be confirmed from a source this session. Meta's help center, Transparency Center and Pages policy pages are rendered by JavaScript or block crawlers, so most policy-page text could not be read directly; those items are marked.

## 1. Snapshot
- Egypt reach: DataReportal (Digital 2026: Egypt, published 2025-11-08) reports Facebook ad reach of 51.6M, Messenger 37.0M and Instagram 21.7M in Oct 2025. These are advertising-tool reach figures, not monthly active users, and Meta revised its reporting method. Source: https://datareportal.com/reports/digital-2026-egypt
- Best for: local-business discovery, customer service via Messenger, community building in Groups, events, longer-form video and older or broader age groups. Age-mix claims for Egypt: unverified.
- Meta frames Facebook as one place for Reels, feed video, Stories, Groups and Pages; Reels and original content are the formats Meta is pushing (see section 5).
- A Page is the brand surface. Personal profiles cannot be used to run a brand through the API. All Page API publishing acts "in the voice of the Page" (official).

## 2. Content formats and specs
| Format | Aspect ratio / size | Length / duration | File limits | Notes |
|---|---|---|---|---|
| Text-only post | n/a | see section 3 | n/a | Publish via `/{page-id}/feed` with `message`. Either `message` or `link` is required (official). |
| Single photo | no official ratio found: unverified | n/a | no official size found: unverified | API: `/{page-id}/photos` with a public `url`. |
| Multi-photo post | unverified | n/a | unverified | Pages API posts page does not describe multi-photo posts. |
| Link post | link preview thumbnail jpg/jpeg/gif/png | n/a | n/a | Custom title/thumbnail only if the Page owns and has verified the domain. Post fails if the link URL cannot be seen by the viewer or app (official). |
| Feed video (non-Reel) | no official ratio found: unverified | max duration unverified | API upload accepts `video/mp4` only; resumable upload for large files | Max file size and max length not stated in the Video API pages read: unverified. |
| Reels | 9:16; 1080x1920 recommended, minimum 540x960 | 3 to 90 s in the Page Reels API | file size not stated | mp4 recommended; H.264/H.265 (VP9, AV1 also supported); 24 to 60 fps fixed, progressive; AAC-LC 48 kHz stereo, 128 kbps or more. Public only. Max 30 published posts per Page per rolling 24 h via API (official). |
| Page Story, photo | 9:16 implied by Stories format | 24 h life (unverified here) | up to 10 MB; JPEG, BMP, PNG, GIF, TIFF | A photo or video already used in a published post cannot be reused as a story (official). |
| Page Story, video | 9:16, 1080x1920 recommended, min 540x960 | 3 to 90 s generally, but a Page story cannot exceed 60 s | same codec specs as Reels | Use `/{page-id}/video_stories`; `is_ai_generated` flag available (official). |
| Live video | unverified | max duration unverified | n/a | Live is publishable via API with the `publish_video` permission (official: Pages API posts page). |
| Group post | unverified | n/a | n/a | No official API for posting to Groups confirmed: see section 8. |
| Event | n/a | description limit see section 3 | n/a | Cover specs unverified. |
| Messenger broadcast | n/a | n/a | n/a | Not a feed format. Only Marketing Messages or Sponsored Messages outside the 24 h window (section 8). |

Facts to remember: scheduled-post lead time is documented three different ways: 10 minutes to 30 days (Pages API Posts guide), 10 minutes to 75 days (Feed edge reference) and more than 10 minutes to less than 29 days (Reels guide). Treat 10 minutes to 29 days as the safe window for automation; Business Suite UI window: unverified.

## 3. Text limits
| Item | Limit | Status |
|---|---|---|
| Post text | 63,206 chars | third-party (typecount.com); not found in Meta docs |
| Visible before "See more" | about 125 chars mobile, about 477 desktop | third-party; heuristic |
| Comment | 8,000 chars | third-party |
| Messenger text message | 20,000 chars per third-party; Meta says only "keep it short" | unverified |
| Page name | 75 chars | third-party |
| Page short description | 155 chars | third-party, article is internally inconsistent: treat as unverified |
| Event description | 8,000 chars | third-party |
| Hashtags | no official cap found; Meta's creator guidance says use no more than five | official guidance (creators.facebook.com, 2025-07-14) |
| Mentions | `@[page-id]` in `message`; person mentions need `@[PSID]`, only people who commented on or created the post, and the Page must allow tagging | official (Pages API) |
| Links | clickable in posts and comments; Meta guidance says keep links out of captions on Reels/video to avoid penalties | official guidance |
| Emoji / Arabic / RTL | UTF-8; Reels `description` and `title` support emoji (official). RTL rendering is automatic per text direction in practice; mixed-direction rendering rules: unverified | partly unverified |

## 4. Posting and cadence
- Official numeric guidance on frequency: none found. Meta says post mainly original content and avoid very short videos (creators.facebook.com/blog/combating-unoriginal-content).
- Hard automation cap: 30 published Reels per Page per rolling 24 h (official, Reels guide). Meta recommends enforcing the cap in your own scheduler.
- Heuristic (practitioner observation, not an official rule): 3 to 7 feed posts per week plus 2 to 4 Reels per week is a sustainable range for a small business; consistency beats volume.
- Timing (heuristic, practitioner observation): in Egypt evenings after work (roughly 8 to 11 pm Cairo time) and Thursday to Saturday often perform better; Friday is the weekly day off; Ramadan shifts activity to after iftar (third-party claim from chatdaddy.tech, WhatsApp context). Always confirm with the Page's own Insights.
- Funnel mapping:
  - Awareness: Reels, original short video, shareable photo or text posts, Page-run events. Goal metric: views and reach.
  - Consideration: carousel-style multi-photo, product explainers, long video, Live Q&A, Group threads, link posts to a landing page.
  - Conversion: posts with a call-to-action button (Message, WhatsApp, Shop), pinned offer post, Messenger or WhatsApp click-to-chat ads, event reminders.
  - Retention: Group community posts, comment replies within the day, Messenger utility updates, polls.

## 5. Distribution and ranking signals
Official:
- Originality: on 2025-07-14 Facebook announced it penalizes accounts that repeatedly reuse others' videos, photos or text without crediting them. Consequences listed: temporary loss of monetization access, reduced distribution of everything the account shares, reduced distribution for duplicate copies. Visible third-party watermarks, recycled content from other apps, and simple clip stitching do not count as meaningful enhancement. Reaction videos, commentary, trends with a unique take, and approved content with real editing are allowed. Rollout was gradual. Source: https://creators.facebook.com/blog/combating-unoriginal-content
- Meta's stated best practices in that post: mainly original content, tell a story, avoid very short videos, avoid watermarks, relevant captions with no links, minimal capitalization, at most five hashtags.
- Tools: post-level insights in the Professional Dashboard show why a post may not be distributed; a Support home screen shows whether a Page is at risk of recommendation or monetization penalties.
- Engagement bait, spam and low-quality repetition each have a Meta Transparency Center page (URLs in section 13); their text could not be retrieved, so exact definitions are unverified.
- Insights vocabulary has moved from "impressions" to "views" (see section 9), which signals Meta now optimizes and reports on media views.

Practitioner lore (practitioner observation, not an official rule):
- Early engagement (first 30 to 60 minutes) helps a post.
- Native uploads outperform links to other sites; Reels from other apps with watermarks do worse (the watermark part is consistent with the official statement above).
- Replying to comments quickly can extend a post's life.
- Posting the same asset on several Pages is treated as duplicate content (the duplicate-copy penalty is official; the multi-Page tactic detail is practitioner).

## 6. Community rules and policy hot spots
Page text of Meta's Community Standards could not be read this session (JavaScript-rendered). What is stated below is either from fetched official pages or flagged unverified.
- Unoriginal content: see section 5 (official, 2025-07-14). Repeat offenders lose monetization access for a period and see reduced distribution.
- Spam, inauthentic behavior, fraud and scams, engagement bait, misinformation: each exists as a Transparency Center policy page (URLs in section 13). Specific wording: unverified. Safe operating rule: never ask people to react, share, tag or comment in exchange for a prize or to "boost" reach, and never buy followers, likes or comments.
- Buying followers or engagement: unverified in wording, but the Spam and Inauthentic Behavior pages exist and Meta lists fake engagement under unoriginal-content penalties ("spammy behavior and fake engagement"). Treat as a restriction risk.
- Impersonation: Meta lists impersonating creators or large content producers under unoriginal-content penalties (official). Reporting flow: unverified.
- Copyright and music: Page Reels API returns copyright check results after upload (official, "may take a few minutes"). Using commercial music on a business Page: music library licensing terms for business accounts are unverified; use the in-app licensed library or owned audio.
- Health, finance, political claims: Meta Misinformation and Fraud policies apply; details unverified. Ads on social issues, elections or politics need authorization and a disclaimer (Meta ad policy, details unverified here).
- Minors: API targeting `age_min` must be 13 or higher (official, Reels API reference). Minimum account age is 13 (consistent with that; the Terms page was not readable: unverified). Do not target or collect data from minors without a lawful basis; Egypt's data law treats all children's data as sensitive (DLA Piper summary, section 11).
- Giveaways and contests: Facebook's Pages, Groups and Events Policies contain promotion rules, but the page could not be fetched (robots blocked). Verified specifics: none. Conservative rules to apply: official rules posted, free entry, no "share to win" or "tag friends to win" mechanics, a statement that Meta is not a sponsor, local-law compliance. Mark each as unverified in client documents.
- Automation and bots: messaging bots must follow the Messenger Platform policy (section 8). Automated Page posting is allowed through the API with a Page token. Scraping and fake accounts are not allowed (Terms page not readable: unverified).
- Reduced reach without notice: Meta lowers distribution for unoriginal, duplicate and low-quality repetitive content. Check the Professional Dashboard and the Page Integrity API for violations or restrictions.
- Restriction states available through the API: `ok`, `warning`, `restricted`, `suspended`, with restriction features `page_publish`, `page_read_only`, `page_messaging`, `page_messaging_api` (official, Page Integrity API).

## 7. Branded content, ads disclosure and legal
Not legal advice. Check local counsel for campaigns.
- Meta tools: Meta has a branded content / paid partnership label and partnership ads flow on Facebook and Instagram; eligibility rules page exists (help.instagram.com/1372533836927082, not readable here). Via the Instagram API: `is_paid_partnership` and `branded_content_sponsor_ids` (max 2 sponsors), partnership ads only through Instagram API with Facebook Login. Facebook-side Pages API fields for the label: unverified.
- US (FTC): disclose any financial, employment, personal or family tie; place it where people will notice, in plain words ("ad", "sponsored", "paid partnership"), in the same language as the endorsement; in video put it in the video itself; platform label alone is not enough; the influencer is responsible. Source: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- EU: hidden advertising is generally prohibited under consumer-protection law; member-state rules vary. Details not fetched: unverified.
- Egypt: unsolicited electronic marketing and personal-data use fall under Law 151/2020 and Anti-Cybercrime Law 175/2018 (section 11). Specific Egyptian rules for influencer licensing and ad disclosure: unverified; confirm with Egyptian counsel before running paid-partnership campaigns.
- Practical rule for agents: always put the word "Ad" or "Paid partnership" (Arabic: "إعلان" or "برعاية") at the start of sponsored copy and also use the Meta label when available.

## 8. API and automation
- Official API: Graph API with the Pages API (Pages use case). Meta current version in docs: v26.0 (reference pages show v25.0/v26.0).
- Auth: OAuth. Use a Page access token (obtained through a user token of a person who can perform the Page task). System user tokens are recommended to avoid rate limits for Page Public Content Access. Page task needed to publish: `CREATE_CONTENT`; to moderate comments: `MODERATE`. Tokens: never log them.
- Permissions (official): `pages_show_list`, `pages_read_engagement`, `pages_manage_posts` (publish and schedule), `pages_manage_engagement` (moderate comments, delete), `pages_read_user_content`, `pages_manage_metadata`, `pages_messaging`, `pages_manage_ads`, `pages_manage_cta`, `business_management`; add `publish_video` for live video. Extended permissions need App Review; screencast and use-case explanation are required. Business verification may also be required for Advanced Access: unverified for Pages API.
- What the API can do: publish text, link, photo, video, Reels (`/video_reels`, start-upload-finish), photo and video Stories; schedule; edit and delete posts (only the creating app can edit a post it made); read comments, reply as the Page, mention people; read insights; send and receive Messenger messages; webhooks for `feed`, `videos`, `messages`, `business_integrity`.
- What it cannot do or is not confirmed: hide-comment endpoint details (`pages_manage_engagement` is described as allowing comment moderation and post deletion, but the endpoint was not read: unverified); publish to Groups (no confirmation found; Groups API status: unverified); start a Messenger conversation with a person who never messaged you; multi-photo post details (unverified).
- Rate limits (official): Pages API with Page or system-user tokens uses Business Use Case limits of 4800 x engaged users per rolling 24 h; user or app tokens use platform limits (200 x users per hour per app). Errors: 4, 17, 32, 613, BUC 80001. Read the `X-Business-Use-Case-Usage` header; stop on limit; do not retry in a tight loop. Reels: 30 published per Page per 24 h; collaborator invites 10 per Page per 24 h.
- Scheduling options: API with `published=false` and `scheduled_publish_time`; Reels with `video_state=SCHEDULED`; Meta Business Suite planner in the UI (limits unverified). A third-party scheduler must call the same API.
- Messenger Platform policy (official): 24 h standard window from the user's action (up to 7 days after a Click-to-Messenger ad); promotional content is allowed inside the window; `HUMAN_AGENT` tag gives a 7 day manual reply window; tags `CONFIRMED_EVENT_UPDATE`, `ACCOUNT_UPDATE`, `POST_PURCHASE_UPDATE` stopped working (error 100) from 2026-04-27; outside the window use Sponsored Messages, One-Time Notifications (one follow-up with permission), Marketing Messages (opt-in) or Utility Messages; Private Replies: one message within 7 days of a comment. Bots must answer every input within 30 seconds; disclose automation where law requires (California, Germany named); a flagged violation must be fixed within 7 days or sending can be limited.
- Messenger rate limits (official): 200 x engaged users per Page per 24 h; Send API 300 calls/s for text, 10/s for audio or video; Conversations API 2/s; above 40 messages/s sustained, new messages stop appearing in Page Inbox.
- Page publishing authorization (PPA): the Instagram docs say publishing is blocked if the connected Page requires PPA; complete it ahead of time.
- No API: Facebook Group posting by apps (unconfirmed), personal-profile posting, Business Suite-only tools (inbox automations built in the UI, stars and labels), Page Quality ("Page Status") appeals except via links from the Integrity API.

## 9. Analytics
- Where: Meta Business Suite Insights, Professional Dashboard (post-level), Page Insights API (`/{page-id}/insights`), `page_status` for integrity.
- Metric changes (official): on 2025-06-15 a block of `*_impressions_unique` and related metrics stopped working; on 2025-11-15 `page_impressions`, `post_impressions` and variants moved to `page_media_view` and `post_media_view` (ads vs organic via `is_from_ads`, followers via `is_from_followers` breakdowns), `page_fans*` moved to `page_follows*`; about 70 older engagement and click metrics were retired on 2024-03-14 with no replacement. Calls to deprecated metrics return an invalid-metric error. Unique-reach replacement: `page_total_media_view_unique`, `post_total_media_view_unique`. Never build reports on `impressions` or `fans`.
- Data retention for public Pages insights: 2 years; periods `day`, `week`, `days_28`, `lifetime` (official).
- Definitions: `views` count media plays or displays (Meta describes views as the replacement for impressions; exact definition text: unverified). Total reach (legacy `page_impressions_unique`) was "people who had any content from or about the Page on screen".
- Question to metric: Are we being seen? `page_media_view`, `post_media_view`. How many different people? `page_total_media_view_unique`. Is audience growing? `page_follows`. Is paid driving it? media views broken down by `is_from_ads`. Is the content resonating? reactions, comments, shares per post. Are we penalized? Professional Dashboard post-level distribution status and `page_status`.

## 10. Cases
**Situation 1: Reach suddenly drops on a Page.**
**Do:** Check `page_status` / Page Status and the Professional Dashboard post-level distribution view for violations or restrictions; compare `post_media_view` for the last 10 posts against the previous 10; look for reposted, watermarked or duplicate media; remove or replace clearly unoriginal posts; return to original content for 2 to 4 weeks.
**Avoid:** Posting more of the same, buying engagement, deleting and reposting the same asset, blaming "the algorithm" without checking integrity status.

**Situation 2: Page restricted or flagged.**
**Do:** Read the violation type, `expiration_time` and recommended action in Business Support Home or via the Integrity API; file the appeal through the provided link; stop scheduled posts that may repeat the violation; tell the client the restriction scope (`page_publish`, `page_read_only`, `page_messaging`).
**Avoid:** Creating a replacement Page to dodge restriction, appealing repeatedly with the same text, sending the admin password to anyone.

**Situation 3: Copyright or music claim on a Reel.**
**Do:** Read the copyright check result returned after upload; swap to licensed or owned audio; keep the licence proof; for a wrong claim use the dispute option in Business Support Home or Rights Manager (flow: unverified).
**Avoid:** Re-uploading the same video hoping the check passes, using trending commercial audio on a business Page without confirmed rights.

**Situation 4: Negative comment wave on a post.**
**Do:** Pin one calm factual reply, answer genuine questions publicly and move details to Messenger, hide or delete only abusive, spammy or hateful comments per a written moderation rule, log the incident, brief the client. Keep a response template in Arabic and English.
**Avoid:** Deleting all criticism, arguing, using auto-replies that look evasive, turning off comments without telling the client.

**Situation 5: Fake or scam impersonator Page copying the brand.**
**Do:** Collect URLs and screenshots; report the Page via the Facebook "Report Page" flow for impersonation or scam (flow wording unverified); warn followers with a pinned post saying the only official Page is X and Meta never asks for payment by DM; check the brand's verified status if eligible.
**Avoid:** Engaging with the scammer, naming and shaming individuals, sharing the fake link as a clickable URL.

**Situation 6: Giveaway planning.**
**Do:** Write official rules (eligibility, dates, prize, winner selection, data use, Meta-not-sponsor statement), use comment or form entry only, get the client's legal sign-off, announce the winner publicly with proof of random selection. Treat Meta-specific promotion rules as unverified until read from the Pages, Groups and Events Policies page.
**Avoid:** "Share to win", "tag three friends", requiring likes of other Pages, collecting extra personal data without consent (Law 151/2020).

**Situation 7: Cross-posting from Instagram or TikTok.**
**Do:** Export a clean file without any other app's watermark; re-cut hooks for Facebook's 9:16 Reels spec (1080x1920, 3 to 90 s); write a fresh caption without links and with at most five hashtags; use Instagram's Facebook-share setting or Meta Business Suite cross-post rather than re-downloading.
**Avoid:** Uploading the TikTok-watermarked file, copy-pasting 20 Instagram hashtags, posting the same Reel on several Pages.

**Situation 8: A published post must be corrected or deleted.**
**Do:** If only the text is wrong, edit it (API edit works only for posts created by the same app; otherwise edit in the UI); if the facts are harmful, delete and post a short correction; keep a log with time, reason and approver.
**Avoid:** Silent deletion of a post that already got many comments on a crisis topic, editing a post to change its meaning after people reacted.

**Situation 9: Crisis (product harm, viral complaint, outage).**
**Do:** Pause scheduled posts and ads, post one holding statement, route DMs to a human via the `HUMAN_AGENT` 7-day window, set one approver, update at fixed times.
**Avoid:** Cheerful scheduled content, automated replies that deny the issue, deleting reports of the problem.

**Situation 10: Handing over Page access safely.**
**Do:** Add people as Page admins or assign tasks (`CREATE_CONTENT`, `MODERATE`, `ANALYZE`) through Meta Business Suite and a Business portfolio; use a system user for automation; remove access on exit; keep two admins.
**Avoid:** Sharing a personal Facebook password, using a personal account as the sole admin, leaving a former freelancer with full control.

## 11. Arabic and Egypt notes
- Text direction: Facebook posts accept UTF-8 Arabic; in practice the direction of a paragraph follows its first strong character. Keep a line of Latin text separate from Arabic lines, put numbers and links on their own line. Rendering in preview vs live is unverified for edge cases.
- Dialect: write Egyptian dialect for engagement posts and customer replies; Modern Standard Arabic for announcements, legal and official statements (third-party suggestion from chatdaddy.tech for WhatsApp; apply as a style guideline, not a platform rule).
- Hashtags: Arabic hashtags work; keep to at most five and mix one Arabic with one English (practitioner observation, not an official rule).
- Rhythm: Friday is the weekly day off in Egypt; Ramadan changes the daily rhythm (activity moves after iftar, third-party). Eid and national holidays need dedicated calendars.
- Reach context: ad reach in Egypt is 51.6M for Facebook and 37.0M for Messenger (DataReportal 2025). Messenger and WhatsApp are the usual conversion channels; Egyptian audiences often ask price in comments: answer in DM with a link to the order channel and reply in the comment thread to confirm you did.
- Data law: Personal Data Protection Law No. 151 of 2020 requires explicit consent for processing and for direct electronic marketing, a clear marketing label, sender identity, easy opt-out, and consent records kept 3 years after the last message; a licence or permit from the Personal Data Protection Centre is required for electronic marketing activities (DLA Piper summary, page modified 2026-02-13). Anti-Cybercrime Law 175/2018 article 25 covers unsolicited marketing messages. Not legal advice.
- Payment and verification quirks for Meta ads and Business verification in Egypt (local cards, EGP billing, document requirements): unverified.
- Egyptian media-regulation rules for large social accounts and influencers (Law 180/2018): unverified here; check before paid campaigns.

## 12. Pre-publish checklist
1. Is the media original, free of other apps' watermarks, and either owned or licensed (including music)?
2. Does the Reel meet 9:16, at least 540x960 (1080x1920 preferred), 3 to 90 s, mp4?
3. Is the caption free of links (for Reels/video), with at most five hashtags and no engagement bait ("share to win", "tag a friend")?
4. If sponsored, does the copy start with "Ad" or "Paid partnership" and is the Meta label applied?
5. Are claims (health, finance, prices, political) sourced and approved by the client?
6. Is any personal data of customers or minors visible (faces of children, phone numbers, ID cards)?
7. Is the scheduled time within the safe window (10 minutes to 29 days ahead) and inside the 30-Reels-per-24-hours cap?
8. Is the Arabic text proofread, with numbers and links on their own lines and no broken RTL ordering?
9. Does the post have a clear next step (message, WhatsApp, link) and is someone assigned to reply within the same day?
10. Is it a duplicate of a post already live on this or another Page?
11. Is a crisis or sensitive event happening that makes the scheduled tone wrong?
12. Is the post logged (owner, approver, time) for later audit?

## 13. Sources
- https://datareportal.com/reports/digital-2026-egypt
- https://creators.facebook.com/blog/combating-unoriginal-content
- https://developers.facebook.com/documentation/video-api/guides/publishing
- https://developers.facebook.com/docs/video-api/guides/reels-publishing
- https://developers.facebook.com/docs/graph-api/reference/page/video_reels
- https://developers.facebook.com/docs/graph-api/reference/page/feed/
- https://developers.facebook.com/docs/page-stories-api/
- https://developers.facebook.com/documentation/pages-api
- https://developers.facebook.com/documentation/pages-api/posts
- https://developers.facebook.com/documentation/pages-api/comments-mentions
- https://developers.facebook.com/documentation/pages-api/integrity-webhook
- https://developers.facebook.com/documentation/pages-api/platforminsights/page
- https://developers.facebook.com/documentation/pages-api/platforminsights/page/deprecated-metrics.md
- https://developers.facebook.com/blog/post/2025/08/15/page-insights-api-updates/
- https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy
- https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages
- https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview/rate-limiting
- https://developers.facebook.com/documentation/instagram-platform/content-publishing (Page Publishing Authorization note)
- https://typecount.com/blog/facebook-post-character-limit-2026 (third-party)
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.dlapiperdataprotection.com/index.html?t=law&c=EG
- https://chatdaddy.tech/blog/whatsapp-business-api-egypt (third-party, Egypt notes)
- Not readable this session, listed for the next verification pass: https://transparency.meta.com/policies/community-standards/spam/ , https://transparency.meta.com/policies/community-standards/inauthentic-behavior/ , https://transparency.meta.com/en-gb/features/approach-to-ranking/content-distribution-guidelines/engagement-bait , https://www.facebook.com/business/help/169845596919485 , https://www.facebook.com/policies_center/pages_groups_events
