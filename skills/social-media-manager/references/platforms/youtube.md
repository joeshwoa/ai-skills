# YouTube — rules and playbook
Last verified: 2026-10-19

Scope: long-form videos, Shorts, Live, Posts (community), playlists, YouTube Partner Program (YPP), strikes, disclosures and the YouTube Data API v3. Quota numbers changed in 2025 and 2026 (see section 8); always re-read the quota page before building on them.

## 1. Snapshot
- What it is: a search-and-recommendation video platform. Long-form builds evergreen search traffic; Shorts feeds fast discovery; Live adds real-time community. Sources for surfaces: https://www.youtube.com/howyoutubeworks/product-features/recommendations/ and https://support.google.com/youtube/answer/10059070
- Best for: tutorials and explainers, product education, series, Q&A and live events, and Shorts as a top-of-funnel feeder.
- Egypt: DataReportal (Digital 2026: Egypt, data to late 2025) gives YouTube ad reach of 49.3 million (41.5% of the population), down 1.40M (-2.8%) from end-2024. Compared with TikTok 48.8M (18+) and Facebook 51.6M. It is an ad-reach estimate, not monthly active users. Source: https://datareportal.com/reports/digital-2026-egypt
- View counting changed twice: since 2025-03-31 a Short counts a view on every start or replay with no minimum watch time (the older metric is called "Engaged views"), and the API revision history says that from 2026-08-27 public view counting starts when playback begins for long-form, Live and Shorts, with monetization metrics unchanged. Sources: https://support.google.com/youtube/answer/10059070 and https://developers.google.com/youtube/v3/revision_history

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Long-form video | 16:9 standard; vertical 9:16 and square 1:1 are accepted and adapt automatically. Resolutions 360p to 8K | 15 minutes for unverified accounts; verified accounts up to 12 hours | 256 GB or 12 hours, whichever is less | Recommended encode: MP4, H.264 High Profile, AAC-LC or Opus audio, 48 kHz, record frame rate kept. SDR 1080p at 24-30 fps about 8 Mbps; 4K 35-45 Mbps. Sources: https://support.google.com/youtube/answer/71673 and https://support.google.com/youtube/answer/1722171 |
| Short | vertical; uploads up to 1080p | up to 3 minutes | covered by the general upload limits | Vertical video up to 3 min. Shorts can be monetized through the Shorts feed revenue share. Source: https://support.google.com/youtube/answer/10059070 |
| Thumbnail (video) | recommended 3840x2160, 16:9; minimum 640 px width | n/a | JPG or PNG; desktop up to 50 MB; mobile 2 MB for video thumbnails | Requires a verified account. API `thumbnails.set` max size raised from 2 MB to 50 MB on 2026-09-14. Sources: https://support.google.com/youtube/answer/72431 and https://developers.google.com/youtube/v3/revision_history |
| Thumbnail (Short) | 2160x3840, 9:16; minimum 640 px height | n/a | desktop 50 MB | Only in YouTube Studio on a computer, verified account. Same support page |
| Live stream | not stated on page read | no stream length cap found on the page read (`unverified`) | n/a | Needs a verified channel, no live restrictions in the last 90 days, minimum age 16. Mobile streaming has separate requirements (subscriber minimum not stated here, `unverified`). Source: https://support.google.com/youtube/answer/2474026 |
| Posts (community: text, image, poll, quiz) | not researched | not researched | not researched | Spec and eligibility `unverified`; the Data API resource list does not include posts. Spam policy mentions polls and Image Posts. Sources: https://developers.google.com/youtube/v3/getting-started |
| Playlist | n/a | n/a | max items not confirmed (commonly 5,000) | `unverified`. Public playlist creation has a daily cap shared across app, YouTube Music and API; Shorts-only playlists cannot be reordered. Source: https://support.google.com/youtube/answer/57792 |
| Premiere / scheduled video | as long-form | n/a | n/a | Scheduling in the API uses `status.publishAt`; the video must be private and never published. Source: https://developers.google.com/youtube/v3/docs/videos |
| Podcast thumbnail | n/a | n/a | desktop 50 MB, mobile 10 MB | Source: https://support.google.com/youtube/answer/72431 |
| Channel/broadcast (WhatsApp-style) | none | n/a | n/a | No broadcast channel product found in sources read. |

## 3. Text limits
| Item | Limit | Source / status |
|---|---|---|
| Video title | 100 characters; `<` and `>` not allowed | https://developers.google.com/youtube/v3/docs/videos |
| Video description | 5,000 **bytes** (API), not characters | same source. UTF-8 Arabic letters use 2 bytes each, so about 2,500 Arabic characters fit. Whether the Studio UI counts characters or bytes was not confirmed (`unverified`) |
| Tags | 500 characters in total, commas count, a tag with a space counts as quoted (+2) | same source |
| Hashtags | no spaces; more than 60 on a video or playlist and every hashtag is ignored; up to 3 of the most engaging show above the title | https://support.google.com/youtube/answer/6390658 |
| Channel name | 30 characters per the API channel resource (`brandingSettings.channel.title`); Studio may differ (`unverified`) | https://developers.google.com/youtube/v3/docs/channels |
| Channel description | 1,000 characters; channel keywords 500 characters | same source |
| Handle | 3 to 30 characters; letters, numbers, underscore, hyphen, period; not case sensitive; LTR and RTL scripts cannot be mixed (digits may be appended) | https://support.google.com/youtube/answer/11585688 |
| Comment | maximum length not stated in the API reference (commonly cited 10,000, `unverified`) | https://developers.google.com/youtube/v3/docs/comments |
| Playlist title / description | not specified in the API reference | https://developers.google.com/youtube/v3/docs/playlists |
| Mentions | @handle mentions are supported in comments and descriptions; caps `unverified` | n/a |
| Links in description | clickable in the description; link rules for new channels `unverified` | n/a |
| Emoji / Arabic / RTL | handles cannot mix scripts; API strings are UTF-8, so bytes matter for descriptions | see rows above |

## 4. Posting and cadence
No official cadence or timing guidance was reachable. All below is heuristic.
- Frequency (heuristic): one strong long-form video per week or fortnight plus 3 to 7 Shorts per week; consistency matters more than volume. YouTube may turn off monetization for channels with no uploads or Posts-tab activity for six months or more. Source: https://support.google.com/youtube/answer/72851
- Timing (heuristic): check Audience > "When your viewers are on YouTube" in Studio (`unverified` as an exact name) and publish 1 to 2 hours before the peak. Use scheduling (Studio or `publishAt`).
- Funnel plan:
  - Awareness: Shorts with a clear hook, search-led titles for questions people actually type.
  - Consideration: long-form how-to, comparison and case-study videos; playlists that chain related videos.
  - Conversion: pinned comment and description with one primary link, end screens (not available on made-for-kids), Live Q&A.
  - Retention: series, memberships (when eligible), Posts and Live.
- Chapters, a clear title and a readable thumbnail help but are practitioner advice, not a documented ranking rule.

## 5. Distribution and ranking signals
Official (YouTube's "how YouTube works" page): recommendations use a viewer's behavior, likes, dislikes, subscriptions and feedback including satisfaction surveys; channel reputation and quality shape how, when and to whom content is surfaced; Search ranks by relevance, engagement and quality with weights varying by query; news and health shelves favor high-quality sources. The page does not mention click-through rate or watch time as stated inputs. Source: https://www.youtube.com/howyoutubeworks/product-features/recommendations/
- Official CTR benchmark: half of channels and videos have an impressions CTR between 2% and 10%, with a wider spread for videos under a week old or under 100 views. Source: https://support.google.com/youtube/answer/7628154
- Disclosure labels (altered or synthetic content, paid promotion) do not by themselves restrict reach or monetization eligibility (AI label page). Source: https://support.google.com/youtube/answer/14328491
Practitioner observation, not an official rule:
- Click-through rate and average view duration together drive Home and Suggested; strong retention in the first 30 seconds matters; consistent topic clusters help recommendations.
- Shorts and long-form audiences overlap less than expected; do not assume Shorts views convert to long-form watch time.

## 6. Community rules and policy hot spots
| Topic | What the rules say | Source |
|---|---|---|
| Strikes | First violation is usually a warning (optional training lets it expire after 90 days). Strike 1: one week without uploads, Live, Premieres, thumbnails, posts and playlist edits; scheduled public videos become private. Strike 2 within 90 days: two weeks. Strike 3 within 90 days: channel may be terminated. Each strike expires after 90 days; deleting content does not remove it. Severe abuse can cause termination without warning. Creating another channel to evade a restriction is circumvention. | https://support.google.com/youtube/answer/2802032 |
| Spam, deceptive practices and scams | Bans engagement manipulation (sub-for-sub, bots, rewards), repetitive prompts in polls or Image Posts, comment spam, link spam, speeding or mirroring to evade detection, automated mass-produced near-identical content, scraped content, get-rich-quick scams, fake support, malicious clickbait. Asking viewers to like, comment, subscribe is allowed. | https://support.google.com/youtube/answer/2801973 |
| Copyright strikes | Different from Community Guidelines strikes and from claims. 3 copyright strikes in 90 days can terminate the account and its channels. Copyright School (4 questions, once) lets a strike expire after 90 days. Resolve by retraction, counter notification, or waiting. A removed live stream means a 7-day Live restriction (14 days on the second). | https://support.google.com/youtube/answer/2814000 |
| Content ID claims | Matches against owners' reference files; owner chooses block, monetize or track, per country. A claim normally causes no strike. Disputing without a valid reason can lead the owner to file a removal request and a strike. | https://support.google.com/youtube/answer/2797370 |
| Dispute timeline | Claimant has 30 days to respond to a dispute; after a rejected dispute you may appeal and the claimant has 7 days. Monetization is restored when all claims are released. Not valid reasons: giving credit, owning a copy, not monetizing. | https://support.google.com/youtube/answer/2797454 |
| Impersonation | Banned: copying another channel's branding or name, adding "Real", "Official" or "Backup", AI voice or likeness to imply ownership or endorsement. Fan channels must say so in the name or handle. | https://support.google.com/youtube/answer/2801947 |
| Medical misinformation | Content contradicting local health authorities on prevention or treatment can be removed; first-time violations usually get a warning. | https://support.google.com/youtube/answer/13813322 |
| Minors and Made for Kids | See section 7 on Made for Kids. Live needs age 16; live chat may be disabled for 13-15 year olds without a visible adult. | https://support.google.com/youtube/answer/2474026 |
| Altered or synthetic content | Disclose realistic AI-made or altered content (real person saying or doing something they did not, altered real events or places, realistic scenes that never happened). Not needed for clearly unrealistic content or minor aesthetic edits. | https://support.google.com/youtube/answer/14328491 |
| Giveaways and contests | The pages I could read do not set contest rules. The API terms forbid paying users for subscribing, liking or watching and forbid requiring a like or subscription to keep watching. Treat sub-gating a prize as risky. | https://developers.google.com/youtube/terms/developer-policies ; contest policy `unverified` |
| Buying subscribers / views | Bots, rewards and sub-for-sub schemes are banned engagement manipulation. | spam policy above |
| Political, finance claims | Rules not fetched in this run (`unverified`). Get-rich-quick scams are covered by the spam and scams policy. | n/a |

**YouTube Partner Program (YPP) eligibility** (all also need: public follow of monetization policies, YPP available in your country, no active Community Guidelines strikes, 2-Step Verification, advanced features access, one active AdSense for YouTube account). Source: https://support.google.com/youtube/answer/72851
- Ad revenue: 1,000 subscribers plus either 4,000 qualified long-form public watch hours in the last 12 months or 10 million qualified Shorts views in the last 90 days. Age 18+ or a guardian handling AdSense. Review takes about one month; after rejection appeal within 21 days or reapply after 30 days (90 days for repeat rejections).
- Channel memberships: 500 subscribers, 3 public uploads in 90 days, and either 3,000 watch hours in 365 days or 3 million Shorts views in 90 days; not Made for Kids. Super Chat, Super Thanks and Shopping have their own conditions. Source: https://support.google.com/youtube/answer/72857
- Unlisted, private, deleted, ad-campaign and Shorts-feed watch hours do not count toward the 4,000-hour route. Meeting thresholds does not guarantee acceptance.

## 7. Branded content, ads disclosure and legal
- **Paid promotion toggle**: required for branded content, sponsorships, endorsements and other commercial relationships. In Studio upload: Show more > Paid promotion > "Yes, my video includes branded content". It adds a disclosure label at the start of the video. You can set default and country-specific minimum ages for branded content. Branded content must also follow Community Guidelines and Google Ads policies. Source: https://support.google.com/youtube/answer/154235
- API: `status.paidProductPlacementDetails.hasPaidProductPlacement` (default false); a `brandPartner` part (Creator Initiated Brand Partner Access) was added to `videos.insert`, `update`, `list` on 2026-07-07. Sources: https://developers.google.com/youtube/v3/docs/videos and https://developers.google.com/youtube/v3/revision_history
- Altered or synthetic content label is separate (section 6); the API field is `status.containsSyntheticMedia`.
- **Made for Kids**: set at channel, video or live level in Studio. Required by COPPA and other laws regardless of location. Made-for-kids videos lose comments, notification bell, end-screen and card autoplay, live chat and Super Chat, memberships, merch, personalized ads, save to playlist and more; wrong settings can lead to regulator and account action. The help page says the API does not support it, while the API reference has `selfDeclaredMadeForKids`; verify before automating. Sources: https://support.google.com/youtube/answer/9527654 and https://developers.google.com/youtube/v3/docs/videos
- Legal (not legal advice): creators and brands are responsible for local ad law. YouTube points to the FTC (US), ASA (UK), DGCCRF (France), Medienanstalten (Germany) and KFTC (Korea). Egyptian consumer-protection and advertising rules were not researched (`unverified`). Also say "إعلان" or "برعاية" in the video and description. Source: https://support.google.com/youtube/answer/154235

## 8. API and automation
- **YouTube Data API v3** (REST). Auth: API key for public reads; OAuth 2.0 for insert, update and delete and for private data. Source: https://developers.google.com/youtube/v3/getting-started
- **Quota (documented 2026-10-08):** each project has 100 `search.list` calls per day, 100 `videos.insert` calls per day, and 10,000 units per day shared by all other methods. Quotas reset at midnight Pacific Time. Every request costs at least 1 unit. Quota moved to granular buckets on 2026-06-01; the documented upload cost fell from about 1,600 units to about 100 on 2025-12-04. Sources: https://developers.google.com/youtube/v3/determine_quota_cost and https://developers.google.com/youtube/v3/revision_history
- Unit costs (same quota page): reads such as `videos.list`, `channels.list`, `playlistItems.list`, `comments.list`, `commentThreads.list` cost 1. Writes cost 50: `commentThreads.insert`, `comments.insert`, `comments.update`, `comments.setModerationStatus`, `comments.delete`, `videos.update`, `videos.delete`, `videos.rate`, `thumbnails.set`, `playlists.insert`, `playlistItems.insert`, `subscriptions.insert`, `channels.update`. Captions: list 50, insert 400, update 450, delete 50. Live: `liveBroadcasts.*` and `liveStreams.*` 1; `liveChatMessages.list` 5, insert/delete 20; `liveChatBans` and `liveChatModerators` insert/delete 200. New `videos.batchGetStats` (2026-06-03): 1 unit in its own bucket of 10,000/day.
- Quota increase: needs the quota extension request and an API Compliance Audit; inactive projects (90 days) can lose quota. Source: https://developers.google.com/youtube/terms/developer-policies
- Can do: upload (resumable, 256 GB), schedule with `publishAt` (private, never published; a past time publishes immediately), set title/description/tags/category, privacy, made-for-kids self declaration, `containsSyntheticMedia`, paid placement flag, thumbnails, playlists, captions, read and post comments and replies, moderate comments (`heldForReview`, `published`, `rejected`; `banAuthor` only with rejected; scope `youtube.force-ssl`), run Live broadcasts and chat moderation. Sources: https://developers.google.com/youtube/v3/docs/videos , https://developers.google.com/youtube/v3/docs/comments/setModerationStatus
- Cannot / not found: Posts (community) are not in the resource list; DMs and Shorts-feed placement are not exposed; there is no documented "is Short" flag (Shorts are vertical videos of up to 3 minutes) (`unverified` for each). Comments' image attachments (`snippet.imageUrl`, signed link valid 6 hours) are rolling out from November 2026.
- Unverified API projects: the revision pages conflict (one summary says uploads from unverified projects are restricted; the `privacyStatus` text says they are not). Test with a throwaway private video before relying on public publishing. Source: https://developers.google.com/youtube/v3/docs/videos/insert
- **YouTube Analytics API** (targeted real-time queries) and **Reporting API** (bulk reports); groups up to 500 items. Scopes and latency not confirmed on the pages read (`unverified`). Source: https://developers.google.com/youtube/analytics
- Developer policy highlights: no automating views, likes, comments or uploads without the user's express consent; no rewards for engagement; no scraping; delete data within 7 days of a deletion request; refresh or delete most stored API data within 30 days; show YouTube branding where content is displayed. Source: https://developers.google.com/youtube/terms/developer-policies
- Official scheduling: YouTube Studio scheduled publish and Premieres; the API `publishAt`. n8n pattern: HTTP Request with OAuth2 credentials to `videos.insert` (resumable) then set `publishAt`; budget 100 uploads per day per project.

## 9. Analytics
Where: YouTube Studio > Analytics (Overview, Content, Audience, Revenue).
- **Views**: number of plays; Shorts count a view on start or replay since 2025-03-31, and "Engaged views" is the older Shorts metric. Source: https://support.google.com/youtube/answer/10059070
- **Impressions CTR**: how often viewers watched after a registered impression; impressions on external sites and end screens are excluded; 2% to 10% is the range for half of all videos. Answers: "does the title and thumbnail earn the click?" Source: https://support.google.com/youtube/answer/7628154
- **Audience retention and key moments**: shown at video level; key moments need a video of at least 60 seconds and 100 views; data takes 1 to 2 days to process. Answers: "where do viewers leave?" Source: https://support.google.com/youtube/answer/9314415
- **Ad revenue metrics**: RPM is per 1,000 engaged views for Shorts; estimated monetized playbacks, ad impressions. Source: https://support.google.com/youtube/answer/9314357
- Definitions of watch time, average view duration, unique viewers, traffic source, subscribers gained were not on pages I could read; use them as standard Studio metrics (`unverified` definitions).
- Which metric answers which question: thumbnail/title test = impressions CTR; hook = retention in the first 30 seconds (practitioner); topic fit = audience and returning viewers; revenue = estimated revenue and RPM; Shorts feeder = views and subscribers gained from Shorts.

## 10. Cases
1. **Situation:** Views suddenly drop on long-form and Shorts.
   **Do:** Check Studio traffic sources and impressions CTR; compare against the 2% to 10% range; look for a new Community Guidelines or Content ID notice in Studio; review the last 5 uploads for misleading thumbnails or titles. Also remember the view-counting changes (2025-03-31 Shorts, 2026-08-27 all formats): a step change in reported views can be definitional. Sources: https://support.google.com/youtube/answer/7628154 , https://developers.google.com/youtube/v3/revision_history
   **Avoid:** Re-uploading the same video or buying views; both are spam-policy risks.
2. **Situation:** A Community Guidelines strike arrives.
   **Do:** Read the policy named in the email, appeal in Studio if you believe it is wrong, complete the optional policy training only when the notice is a warning, and pause scheduled videos (they turn private under strike 1). Source: https://support.google.com/youtube/answer/2802032
   **Avoid:** Making a new channel to keep posting; circumvention can terminate linked channels.
3. **Situation:** A Content ID claim on a video with music.
   **Do:** Open Content > Claims in Studio. If the claim only monetizes or tracks and you agree, do nothing; if you hold rights or fair use applies, dispute (the claimant has 30 days). Replace or mute the track if you do not have rights. Source: https://support.google.com/youtube/answer/2797454
   **Avoid:** Disputing with invalid reasons ("I gave credit", "I bought the song"); a failed dispute can trigger a removal request and a copyright strike. Source: https://support.google.com/youtube/answer/2814000
4. **Situation:** A copyright strike (legal removal request).
   **Do:** Choose one route: ask the claimant to retract, file a counter notification if mistaken or an exception applies, or complete Copyright School and wait 90 days. Source: https://support.google.com/youtube/answer/2814000
   **Avoid:** Treating it as a Content ID claim; deleting the video does not remove the strike.
5. **Situation:** A wave of abusive or spam comments, or a raid on a Live chat.
   **Do:** Turn on held-for-review for comments, hold or reject spam with `comments.setModerationStatus` (50 units per call; rejected plus `banAuthor` blocks the author), and add moderators and blocked words for Live. Sources: https://developers.google.com/youtube/v3/docs/comments/setModerationStatus
   **Avoid:** Bulk-calling moderation in a loop without budgeting quota (10,000 units/day shared).
6. **Situation:** An impersonator copies the channel (name, avatar, "Official" added).
   **Do:** Collect URLs, report via the impersonation form, pin a comment with the real handle, and warn the audience that YouTube staff never ask for payment in comments. Source: https://support.google.com/youtube/answer/2801947
   **Avoid:** Replying to the fake account or following its links.
7. **Situation:** Planning a giveaway.
   **Do:** Make the entry rule a comment or form that is not conditional on subscribing; state dates and eligibility; disclose sponsors with the paid promotion toggle; keep legal advice for local lottery or contest law (Egypt not researched). 
   **Avoid:** Requiring sub-for-sub, rewarding watch or like actions, or promising prizes to viewers who subscribe (see API terms on rewards). Source: https://developers.google.com/youtube/terms/developer-policies
8. **Situation:** Cross-posting a TikTok or Reel as a Short.
   **Do:** Export without another app's watermark, keep it vertical and 3 minutes or less, write a new title (keywords) and description, and add the AI-use disclosure if it includes realistic synthetic media. Sources: https://support.google.com/youtube/answer/10059070 , https://support.google.com/youtube/answer/14328491
   **Avoid:** Re-uploading unchanged third-party clips (reposted content with no commentary is a spam and impersonation risk). Source: https://support.google.com/youtube/answer/2801973
9. **Situation:** A published video needs a fix (wrong claim, wrong disclosure).
   **Do:** Edit title, description, thumbnail or tags in Studio (or `videos.update`, 50 units); trim or blur parts with the editor; add the paid-promotion toggle if missed (Content > video > branded content box). Source: https://support.google.com/youtube/answer/154235
   **Avoid:** Deleting a video that is under a strike or claim to "make it go away".
10. **Situation:** Crisis or brand-safety problem (an ad shows next to unsuitable content, a viral complaint).
    **Do:** Unlist or hold the affected video, post a single factual Community post or pinned comment, tighten comment moderation, and review advertiser-friendly guidelines for demonetization (YPP ad eligibility requires content meeting them). Source: https://support.google.com/youtube/answer/72857
    **Avoid:** Editing the video title to hide the issue after reports.
11. **Situation:** Handing over the channel to an agency.
    **Do:** Use Studio permissions (manager roles) rather than sharing the Google password; keep 2-Step Verification on (it is a YPP requirement); revoke OAuth tokens and permissions at handover end. Source: https://support.google.com/youtube/answer/72851
    **Avoid:** Sending verification codes or giving AdSense owner access.
12. **Situation:** n8n upload workflow hits quota errors.
    **Do:** Remember `videos.insert` has its own bucket of 100 calls per day and uses 10,000 shared units for the rest; cache `videos.list` data, avoid `search.list` (100 per day), and request an extension through the audit path. Source: https://developers.google.com/youtube/v3/determine_quota_cost
    **Avoid:** Polling comments every minute with 1-unit calls plus 50-unit replies from many channels under one project.

## 11. Arabic and Egypt notes
- Descriptions are limited in **bytes** by the API (5,000), and Arabic letters take 2 UTF-8 bytes, so a full Arabic description is about 2,500 characters. Source: https://developers.google.com/youtube/v3/docs/videos
- Handles cannot mix left-to-right and right-to-left scripts (digits may be added at the end), so an Arabic handle cannot include Latin letters. Source: https://support.google.com/youtube/answer/11585688
- Hashtags: no spaces; more than 60 and all are ignored; keep three strong Arabic/English tags for the title area. Source: https://support.google.com/youtube/answer/6390658
- Localization: the channel resource accepts localized titles and descriptions keyed by BCP-47 codes (for example `ar`), but whether it improves Arabic search was not confirmed (`unverified`). Source: https://developers.google.com/youtube/v3/docs/channels
- YPP eligibility depends on the country; the list of eligible countries (including Egypt) was not on the page I could read (`unverified`). Requirements that are known: 2-Step Verification, one active AdSense for YouTube account, advanced features access, no active strikes. Payment and tax setup in Egypt were not researched (`unverified`). Source: https://support.google.com/youtube/answer/72851
- Updated YPP terms take effect 2027-02-01 and must be accepted in Studio by 2027-01-31. Source: https://support.google.com/youtube/answer/72851
- Dialect: no platform rule; Egyptian Arabic titles with MSA keywords for search is practitioner advice (practitioner observation, not an official rule).
- Sensitive topics (political and religious content, health claims) carry both platform and local-law risk; medical misinformation rules apply to comments and descriptions too. Source: https://support.google.com/youtube/answer/13813322

## 12. Pre-publish checklist
1. Is the title 100 characters or fewer and is the main keyword near the start?
2. Is the description under 5,000 bytes (about 2,500 Arabic characters) with the primary link in the first lines?
3. Are tags under 500 characters and hashtags under 60 (best 3)?
4. Is the format right: Short is vertical and 3 minutes or less; long-form is 16:9 (or accepted 9:16/1:1)?
5. Is the thumbnail 16:9 (or 9:16 for Shorts), under the size limit, readable at small size, and honest to the content?
6. Is the audience setting (made for kids or not) correct?
7. Is realistic synthetic or altered content disclosed with the AI-use question?
8. Is paid promotion (sponsor, gifted, affiliate, own paid deal) declared with the toggle and also in words?
9. Is all music, footage and imagery licensed or original (no Content ID risk)?
10. Are claims (health, finance, results) supportable and within the medical and scam policies?
11. Does the description and title avoid engagement bait and misleading metadata?
12. Is publishAt set correctly (private, never published) and the project quota enough for the day?

## 13. Sources
- https://developers.google.com/youtube/v3/determine_quota_cost
- https://developers.google.com/youtube/v3/getting-started
- https://developers.google.com/youtube/v3/revision_history
- https://developers.google.com/youtube/v3/docs/videos
- https://developers.google.com/youtube/v3/docs/videos/insert
- https://developers.google.com/youtube/v3/docs/channels
- https://developers.google.com/youtube/v3/docs/playlists
- https://developers.google.com/youtube/v3/docs/comments
- https://developers.google.com/youtube/v3/docs/comments/setModerationStatus
- https://developers.google.com/youtube/analytics
- https://developers.google.com/youtube/terms/developer-policies
- https://www.youtube.com/howyoutubeworks/product-features/recommendations/
- https://support.google.com/youtube/answer/72851
- https://support.google.com/youtube/answer/72857
- https://support.google.com/youtube/answer/71673
- https://support.google.com/youtube/answer/1722171
- https://support.google.com/youtube/answer/72431
- https://support.google.com/youtube/answer/10059070
- https://support.google.com/youtube/answer/2474026
- https://support.google.com/youtube/answer/2801973
- https://support.google.com/youtube/answer/2802032
- https://support.google.com/youtube/answer/2814000
- https://support.google.com/youtube/answer/2797370
- https://support.google.com/youtube/answer/2797454
- https://support.google.com/youtube/answer/2801947
- https://support.google.com/youtube/answer/13813322
- https://support.google.com/youtube/answer/14328491
- https://support.google.com/youtube/answer/154235
- https://support.google.com/youtube/answer/9527654
- https://support.google.com/youtube/answer/6390658
- https://support.google.com/youtube/answer/11585688
- https://support.google.com/youtube/answer/57792
- https://support.google.com/youtube/answer/7628154
- https://support.google.com/youtube/answer/9314415
- https://support.google.com/youtube/answer/9314357
- https://datareportal.com/reports/digital-2026-egypt
