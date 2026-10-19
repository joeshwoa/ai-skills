# X (Twitter) — rules and playbook
Last verified: 2026-10-19

Labels: `official` = X Help Center or docs.x.com page read on 2026-10-19; `secondary` = third party; `unverified` = not confirmed. X changes pricing and limits often; docs.x.com and the Developer Console are authoritative.

## 1. Snapshot
- What it is: public, real-time conversation platform; best for news, live events, customer support in public, tech and media communities, launches, and reactive brand voice.
- Egypt: X ad reach 4.64 million in late 2025, down 846 thousand (-15.4%) year on year; 8th by ad reach in Egypt, well behind Facebook (51.6M), YouTube, TikTok, Instagram, LinkedIn (15.0M). Ad reach is not active users, and X's demographic data is inferred. Source: DataReportal Digital 2026 Egypt https://datareportal.com/reports/digital-2026-egypt
- Arab world: no further sourced figures gathered. `unverified`
- Surfaces: posts, replies, quotes, reposts, long posts and Articles (Premium), polls, Communities, Spaces (audio), DMs, Lists, X Live/video.

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Post (text) | n/a | 280 characters standard (implied by X's Premium page); 25,000 characters for Premium subscribers | n/a | Everyone can read long posts; only Premium can write them. `official` https://help.x.com/en/using-x/x-premium |
| Images | recommended ratios `unverified` | up to 4 photos per post | 5 MB per image (API `tweet_image`) | Alt text supported. Formats `unverified`. |
| GIF | `unverified` | 1 per post | 15 MB (API `tweet_gif`) | Cannot mix with photos or video. |
| Video (standard account) | `unverified` | up to 140 seconds | 512 MB | Help Center https://help.x.com/en/using-x/x-videos |
| Video (Premium) | 1080p; 720p mentioned above 2 hours | under 4 hours (help) | 16 GB | Help Center says under 4 h; Premium page says about 3 hours / 8 GB on web and iOS only. |
| Video via API | n/a | default account 20 min; Premium or verified 125 min | 8 GB default; 16 GB Premium | docs.x.com media upload; exceeding returns 403. **Conflicts with Help Center 140 s / 512 MB for standard accounts: unresolved, test with a real account.** |
| Poll | n/a | duration 5 to 10,080 minutes (API) | 2 to 4 options, 1 to 25 characters each (API) | `official` docs.x.com Create Post. |
| Thread | n/a | chain of replies to your own post | n/a | No separate format; post sequentially. |
| Article | n/a | n/a | n/a | Premium and Premium+ only; limits not stated on the page. |
| Community post | n/a | 280 / Premium limit | n/a | Posts in a Community show to anyone on X; only members can engage fully. |
| Space (audio live) | n/a | duration cap not stated | up to 13 speakers including host and 2 co-hosts | Start only on iOS/Android; web can listen. |
| Story/Status | not available | n/a | n/a | No equivalent. |
| DM | n/a | n/a | image 5 MB, GIF 15 MB, video 140 s / 512 MB (Premium 10 min / 1 GB) | API `dm_*` categories. |

## 3. Text limits
- Post: 280 characters (standard); 25,000 (Premium). Counting rules for URLs, emoji and Arabic characters `unverified` (do not assume 23-character link wrapping; test in the composer).
- Display name: up to 50 characters. Username (handle): up to 15 characters, letters A-Z, digits and underscore only; names containing "X" or "Admin" cannot be claimed except by official accounts. `official` https://help.x.com/en/managing-your-account/x-username-rules
- Bio: commonly cited as 160 characters; `unverified` here.
- Hashtags: no hard limit; X recommends no more than 2 per post. Hashtags must have no spaces or punctuation. `official` https://help.x.com/en/using-x/how-to-use-hashtags . Excessive or unrelated hashtags and hashtag hijacking violate the spam policy.
- Mentions: no fixed count found; bulk or aggressive unsolicited mentions violate the spam policy. API allows tagging up to 10 users on media.
- Cashtags: self-serve API allows one cashtag per post.
- Links: clickable. Link-heavy accounts: links shared without commentary must not be most of an account's activity (spam policy). API posts containing a URL cost more (see section 8).
- Edits: allowed within 1 hour with a limited number of changes (all tiers; number not stated). Edits that substantially change content to keep engagement are a policy violation.
- Arabic/RTL: Arabic text and display names work; handles must be Latin letters/digits. See section 11.

## 4. Posting and cadence
Heuristic (not official):
- Brand accounts: 1 to 3 posts per day plus replies is a sustainable range; reactive accounts post more. Quality of replies and quotes matter more than volume.
- Timing: X is real-time; post when your audience is active and during live events. For Egypt, test 12:00-15:00 and 20:00-24:00 Cairo time (heuristic); evenings and match nights are commonly busy.
- Do not post more than a few times per hour in an automated way: identical/near-identical posts and posting then deleting the same text are prohibited.
- Funnel:
  - Awareness: timely commentary, short video, data points, threads that teach one thing.
  - Consideration: product demos, FAQs in replies, polls, Spaces/AMAs, Community discussions.
  - Conversion: pinned offer post, launch posts with one link, replies to buying-intent questions (manually).
  - Retention: support replies, changelogs, customer shout-outs with permission.
- Threads: put the full value in the first post; later posts add depth. Do not rely on thread-only reach.

## 5. Distribution and ranking signals
Official (open-source For You feed code, xai-org/x-algorithm, released Jan 2026 per press, repo updated Aug 2026): https://github.com/xai-org/x-algorithm
- Candidates come from in-network posts (accounts the viewer follows) and out-of-network retrieval (embedding similarity, engagement clusters).
- A model predicts probabilities of actions: favorite, reply, repost, quote, share, share via DM, link/profile/photo/video clicks, dwell, follow author; and negative actions: not interested, mute, block, report. Final score is a weighted sum; negative actions carry negative weights. The weight values are NOT published, so relative importance cannot be stated.
- Adjustments: author-diversity decay (repeat posts from one author rank lower), an out-of-network discount, and a boost for authors with few impressions.
- Filters before scoring include posts older than 48 hours, duplicates, blocked or muted authors and muted keywords; visibility filtering (policy labels) can drop posts.
- Takeaways supported by the code: avoid anything that provokes mutes/blocks/reports; do not post bursts from one account; replies and reposts from followed accounts are discounted vs original posts.

Practitioner lore (practitioner observation, not an official rule): early replies and dwell time matter; native video outperforms link posts; external links lower reach; Premium subscribers get a reach boost. The repository does not confirm the Premium boost or link penalty; treat them as unconfirmed.

## 6. Community rules and policy hot spots
- Platform manipulation and spam (official https://help.x.com/en/rules-and-policies/platform-manipulation): bulk, aggressive or deceptive activity; buying or selling followers, likes, reposts, votes; follow trains and repost-for-repost schemes; duplicate or near-duplicate posts, including across accounts; posting then deleting the same content; bulk unsolicited replies, mentions, DMs; follow/unfollow churn; hashtag hijacking and unrelated hashtags; editing posts to keep engagement while changing meaning; malicious or deceptive links; selling accounts/usernames.
  - Up to 10 accounts allowed if each has a different, non-duplicative purpose. Social media managers may manage client accounts within the rules.
  - Enforcement: anti-spam challenges (phone/reCAPTCHA), post deletion or temporary lock, reduced reach, feature limits, link denylisting, permanent suspension for severe or repeat cases (including replacement accounts for suspended ones).
- Automation (official https://help.x.com/en/rules-and-policies/x-automation and https://docs.x.com/developer-guidelines.md):
  - Allowed: automated posts that share useful information (RSS, weather, alerts) if you are authorized to publish them; auto-replies and automated DMs only to users who opted in (replying to you or messaging you; following is not enough), one automated reply per interaction, clear opt-out honored immediately.
  - AI reply bots require prior written approval from X. Brand/advertiser auto-response campaigns need approval.
  - Prohibited: non-API automation (scripting the website, scraping), automated likes, automated hiding of replies, keyword-search-based auto-replies, automated posts about trending topics or meant to influence them, unsolicited bulk DMs, circumventing rate limits, multiple apps for the same use case to dodge limits.
  - Automated accounts must turn on the "Automated" profile label, state the operator in the bio, and link to a responsible human account (developer guidelines).
- Impersonation and parody: parody accounts must be clearly labeled; exact policy text `unverified` (not fetched).
- Copyright and music: DMCA and copyright reports apply; music use in videos `unverified`. Do not upload full songs or ripped videos.
- Health, finance, political claims: X rules on misleading media, election integrity and synthetic media exist; details `unverified`. Add disclosures for finance and health claims per local law.
- Minors: no targeting of minors; minimum age rules `unverified`.
- Giveaways/contests: follow-and-repost contests risk spam enforcement (repost-for-repost and mass-follow behaviors); run them with clear rules, one entry method, and limits per user; policy page `unverified`.
- Buying followers or using apps that promise followers: prohibited.
- AI training: using X API data to train AI models is prohibited except for Grok (developer guidelines).

## 7. Branded content, ads disclosure and legal
- Paid Partnership policy (official https://help.twitter.com/rules-and-policies/paid-partnerships): organic posts count as paid partnerships if the poster received money, gifts, free product loans or other rewards, has a commercial relationship (e.g. brand ambassador), or includes an affiliate link or discount code. Disclose clearly and prominently, e.g. #ad, #paidpartnership, #sponsored. Failure can lead to enforcement. Follow local law (FTC guides in the US; CAP/CMA in the UK).
- API: set `paid_partnership: true` on create post to label; `made_with_ai: true` discloses AI-generated media.
- Promoted posts carry a "Promoted" label and must follow X Ads Policies.
- Wider law (not legal advice): FTC Disclosures 101 (clear, unavoidable, in the video itself for video, plain words) https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers ; EU rules require ads to be identifiable; Egypt Consumer Protection Law No. 181/2018 covers misleading advertising and Personal Data Protection Law No. 151/2020 covers marketing data. Law 180/2018 was reported in 2018 to classify social accounts with 5,000+ followers as media outlets (africanews). Seek local counsel.

## 8. API and automation
Official API: X API v2 (`api.x.com/2`), console at console.x.com, docs https://docs.x.com .
- Pricing model (official https://docs.x.com/x-api/getting-started/pricing): pay-per-usage, credits bought in advance, no subscription or minimum spend; spending limit per billing cycle can be set; a resource requested twice in 24 h UTC is billed once (soft guarantee). New developers can earn $20 in credits after saving a card and a first purchase. Approximate unit prices read on 2026-10-19 (re-check, they change):
  - Reads: $0.005 per post, list, space, community returned; $0.010 per user, DM event, follower/following record; $0.001 per like, mute, block record. "Owned reads" (your own posts, mentions, bookmarks, followers) $0.001 per resource.
  - Writes: create post $0.015; create post containing a URL $0.200; "summoned" post create $0.010; DM interaction create $0.015.
  - Webhook events billed per delivered event, $0.001 to $0.010.
  - Pay-per-use is capped at 3 million post reads per month; above that needs Enterprise.
- Legacy Basic and Pro subscription tiers: reported (secondary, OpenTweet, checked 2026-10-10) as deprecated, with Basic holders moving to pay-per-use after 2026-06-01 and Pro after 2026-09-01. The official pricing page lists only pay-per-use and Enterprise. A free tier for posting is not listed on the pricing page; the developer guidelines still say a free tier is non-commercial only, so treat free-tier availability as `unverified`.
- Auth: OAuth 2.0 Authorization Code with PKCE or OAuth 1.0a (user context) for posting; Bearer token for app-only reads. An approved developer account, Project and App are required.
- Create post (`POST /2/tweets`): up to 4 photos, 1 GIF or 1 video; media uploaded first via chunked upload (`/2/media/upload/initialize`, `append` chunks of at most 5 MB (server max 8 MB), `finalize`, `STATUS`); poll with 2-4 options; `reply_settings` (following, mentionedUsers, subscribers, verified); `community_id`; `quote_tweet_id`; `nullcast`; `paid_partnership`; `made_with_ai`; `edit_options.previous_post_id` to edit; `for_super_followers_only`. Text-length limit not stated in the spec.
- Self-serve restrictions in the spec: replying is allowed only if the original author @mentioned or quoted your account; quote-posting requires Enterprise; one cashtag per post. This breaks "auto-reply to anyone" workflows by design.
- Rate limits (official https://docs.x.com/x-api/fundamentals/rate-limits): create post 100 per 15 minutes per user and 10,000 per 24 hours per app; delete 50 per 15 minutes per user; likes 50 per 15 min and 1,000 per 24 h per user; retweets 50 per 15 min; media upload about 500 per 15 min per user. 429 on exceed; read `x-rate-limit-remaining` and `x-rate-limit-reset`. Enterprise has custom limits.
- Scheduling: no scheduled-post endpoint found in the docs read. Schedule in your own tool (n8n Schedule trigger then API call). Native scheduling in the X composer/Media Studio exists in the product but was not verified here. `unverified`
- Comments/replies: read via search or conversation lookups (billed per resource); replying subject to the self-serve restriction above.
- DMs: API available (read DM events, create DM interaction; webhooks `dm.received`). Automated DMs only to users who opted in; bulk unsolicited DMs are banned.
- Insights: see section 9; non-public metrics only for the owner, last 30 days.
- Spaces and Communities: Spaces read ($0.005/resource) and webhooks exist; creating or hosting a Space by API `unverified`; posting into a Community via `community_id` is supported; creating/administering Communities by API `unverified` (listed under enterprise docs).
- Forbidden (developer guidelines https://docs.x.com/developer-guidelines.md): non-API automation and scraping; auto-likes; spam and trend manipulation; unsolicited bulk replies or DMs; deceptive bots; using X data to train AI except Grok; iframes for displaying X content; matching X data to off-platform identifiers without opt-in; creating multiple apps to bypass limits; redistribution above 1.5M Post IDs per 30 days. Delete X content within 24 hours of a removal signal.
- Commercial note: the free tier was non-commercial only (developer guidelines); paid use is commercial.

## 9. Analytics
- API fields: `public_metrics` (reposts, quotes, likes, replies, impressions, bookmarks, video views) readable by anyone; `non_public_metrics` (URL link clicks, profile clicks, engagements, video playback at 0/25/50/75/100%) and `organic_metrics` for the owner only, posts from the last 30 days; `promoted_metrics` for ads. Official https://docs.x.com/x-api/fundamentals/metrics
- Native analytics in the X web UI: metric names and definitions `unverified` (page not read). Do not invent definitions; use the API field names above in reports.
- Which metric answers what: reach = impressions; interest = engagements and profile clicks; click intent = URL link clicks; video hook = playback 0% vs 25%; sentiment = replies/quote text read manually; negative-feedback proxy = sharp drop in impressions after posting a topic (blocks and mutes are not exposed).
- Billing: each API read is priced per resource; schedule analytics pulls daily, not per minute.

## 10. Cases
**Situation:** Impressions drop suddenly on a brand account.
**Do:** Check for a spam-policy trigger (duplicate posts, many identical replies, link-only streams, bursty automation); review the last 7 days of posts; check for an anti-spam challenge or locked state; reduce frequency; post original content with commentary; test again for a week.
**Avoid:** Re-posting the same content to "fix" it, buying engagement, or deleting and re-posting repeatedly.

**Situation:** Account locked or suspended.
**Do:** Complete the in-app challenge (phone/reCAPTCHA) if shown; read the violation notice; delete the flagged post if asked; submit one clear appeal; meanwhile pause all automation and scheduled posts.
**Avoid:** Creating a replacement account (grounds for permanent suspension), multiple appeals, or posting from another of your accounts about the suspension.

**Situation:** Copyright or music complaint on a video.
**Do:** Remove the clip, check you own or license the audio and footage, replace with licensed audio, file a counter-notice only with proof of rights.
**Avoid:** Re-uploading the same file, or claiming "fair use" without a legal check.

**Situation:** Negative reply wave or pile-on.
**Do:** Do not respond to bait; post one clear statement if there is a real issue; use "limit who can reply" (`reply_settings`) on the post if abuse spikes; mute/block abusive accounts, report threats; escalate to a human lead.
**Avoid:** Quote-posting critics, auto-replies, deleting the post (screenshots persist) unless it contains an error.

**Situation:** Impersonator or scam account uses the brand name.
**Do:** Screenshot and report the account (impersonation) and posts (spam/scam); pin a post listing official handles; notify followers and support; use verified or gold/affiliate labels if the brand has them (availability `unverified`).
**Avoid:** Engaging the impersonator or tagging them in warnings.

**Situation:** Planning a giveaway.
**Do:** Publish rules, one entry method (reply with a comment or quote), eligibility, region, end date, winner draw method; check for duplicate entries by hand; disclose sponsors with #ad where relevant; follow local contest/lottery law.
**Avoid:** "Follow + repost + tag 3 friends" mass mechanics that trigger spam rules, rewarding repost-for-repost.

**Situation:** Cross-posting from LinkedIn or Instagram.
**Do:** Shorten to the first line, remove platform-specific hashtags, upload the native file, add alt text; check that the length fits 280 characters (or use a long post only if the account has Premium).
**Avoid:** Pasting a link-only post, Instagram watermarked reels, "link in bio" text, identical posts across several accounts.

**Situation:** A post must be deleted or corrected.
**Do:** Typos: edit within the 1-hour window (limited edits); wrong info: edit plus reply, or delete and post a correction; legal/safety: delete immediately and log it.
**Avoid:** Editing a post after it went viral to change its meaning or link (policy violation).

**Situation:** Crisis or brand-safety issue (offensive trend, tragic news).
**Do:** Pause scheduled posts and any automated posting; check hashtags and trending topics before any reactive post; get approval for statements; unpause only after checking the queue.
**Avoid:** Auto-posting on trending topics (prohibited for automation) or humorous posts on sensitive days.

**Situation:** Handing account access to an agency or agent.
**Do:** Use X's delegate/teams access features where available (`unverified` here) or a shared company-controlled login with 2FA; for automation, create an app under the company developer account, spend-limit the credits, and store tokens in a secret manager.
**Avoid:** Sharing passwords in chat, or running the automation under a personal developer account.

## 11. Arabic and Egypt notes
- Handles are Latin letters, digits and underscore only (15 characters); display names (50 characters) can be Arabic.
- Arabic and mixed Arabic/English posts display RTL; hashtags mixing scripts can break at punctuation. Keep hashtags to a single script, no spaces or punctuation (official hashtag rules). Preview before posting.
- Hashtag habits: Multi-word Arabic hashtags are usually joined with underscores (common practice, not an official rule); many Arabic users join trending Arabic hashtags. Automated posting about trending topics is prohibited; manual participation only, and only if relevant.
- Egyptian Arabic (Masri) is widely understood; keep a consistent voice (Masri for casual brand voice, Modern Standard for formal announcements). Dialect effect on reach `unverified`.
- Etiquette: avoid political and religious controversy, respect Ramadan and public-holiday timing, be careful with tragedy-related content.
- Payments: X Premium and API credit purchases are card-based; availability and local-currency billing for Egypt `unverified`.
- Regulatory: Law 180/2018 reported to classify accounts with 5,000+ followers as media outlets (2018 press report); take local legal advice for large accounts.

## 12. Pre-publish checklist
1. Is the post within the account's limit (280, or 25,000 only if the account has Premium)?
2. Is it at most 2 hashtags, all relevant, single script?
3. Is the content not identical or near-identical to a recent post on any account you run?
4. Is any link purposeful and accompanied by commentary (not link-only)?
5. Is media within limits (images 5 MB, GIF 15 MB, video within the account's cap) and has alt text?
6. Is paid or gifted content labeled with #ad/#paidpartnership and `paid_partnership` where posting via API?
7. Is AI-generated media disclosed (`made_with_ai`) where applicable?
8. If it is an automated reply or DM, did the recipient opt in, is it one reply per interaction, and is an opt-out provided?
9. Does the automation use the API (no scripting of the website, no auto-likes, no trend-hijack posts)?
10. Is the "Automated" label on and the human operator named in the bio for bot accounts?
11. Is the time free of crisis, tragedy or sensitive-trend collisions?

## 13. Sources
- https://help.x.com/en/using-x/x-premium
- https://help.x.com/en/using-x/x-videos
- https://help.x.com/en/using-x/communities
- https://help.x.com/en/using-x/spaces
- https://help.x.com/en/using-x/how-to-use-hashtags
- https://help.x.com/en/managing-your-account/x-username-rules
- https://help.x.com/en/rules-and-policies/x-automation
- https://help.x.com/en/rules-and-policies/platform-manipulation
- https://help.twitter.com/rules-and-policies/paid-partnerships
- https://docs.x.com/x-api/getting-started/pricing
- https://docs.x.com/x-api/getting-started/about-x-api
- https://docs.x.com/x-api/fundamentals/rate-limits
- https://docs.x.com/x-api/fundamentals/metrics
- https://docs.x.com/x-api/posts/create-post
- https://docs.x.com/x-api/posts/manage-tweets/introduction
- https://docs.x.com/x-api/media/quickstart/media-upload-chunked
- https://docs.x.com/developer-guidelines.md
- https://github.com/xai-org/x-algorithm
- https://ppc.land/xs-algorithm-source-code-drops-what-it-reveals-about-the-platforms-feed-mechanics/ (secondary)
- https://opentweet.io/x-api-pricing (secondary, legacy tier dates)
- https://datareportal.com/reports/digital-2026-egypt
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.africanews.com/amp/2018/07/19/egyptians-with-5000-followers-on-twitter-to-be-supervised-as-media-outlets/
