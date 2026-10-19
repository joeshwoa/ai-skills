# TikTok — rules and playbook
Last verified: 2026-10-19

Scope: organic posting (videos, photo mode, LIVE), Business vs Personal accounts, Commercial Music Library, branded-content toggle, the TikTok for Developers APIs and community rules. TikTok Shop is mentioned only briefly. TikTok's own help pages and community-guideline subpages are partly blocked to automated fetching, so several app-side figures are marked `unverified`. Official figures carry a URL.

## 1. Snapshot
- What it is: a short-video and photo-carousel platform driven by a recommendation feed (For You feed, FYF). Reach is mostly from recommendation, not follower count. Source for the FYF concept: https://www.tiktok.com/community-guidelines/en
- Best for: top-of-funnel discovery, product demos, educational snippets, trend participation, creator-led proof, LIVE selling.
- Egypt: DataReportal (Digital 2026: Egypt, data as of late 2025) lists TikTok ad reach of 48.8 million users aged 18+, up 25.2% year on year (+9.81M), against Facebook 51.6M, YouTube 49.3M, Instagram 21.7M. Ad reach is an advertising estimate, not monthly active users. Source: https://datareportal.com/reports/digital-2026-egypt
- Age: minimum age is 13 (higher in some regions); FYF eligibility requires users to be 16 or older. Source: https://www.tiktok.com/community-guidelines/en/youth-safety
- Not documented in sources I could reach: official TikTok user counts for the Arab world (`unverified`).

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Video (feed / FYF) | 9:16 vertical, 1080x1920 is the common target (practitioner convention, official recommendation `unverified`) | API Upload endpoint: up to 10 minutes; each creator has their own `max_video_post_duration_sec` (example value 300). App upload of up to 60 minutes is reported by news outlets as a 2024 rollout, not confirmed on a TikTok page I could open (`unverified`) | API: up to 4 GB; MP4 recommended, also MOV and WebM; H.264 recommended, also H.265, VP8, VP9; 23 to 60 fps; 360 to 4096 px height and width | Source: https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide and https://developers.tiktok.com/doc/content-posting-api-reference-query-creator-info |
| Photo mode (carousel) | not documented (`unverified`) | n/a | API: up to 35 images, PULL_FROM_URL only; formats and size not stated | Title up to 90 and description up to 4000 UTF-16 runes; `auto_add_music` available; only the Comment interaction applies to photo posts. Sources: https://developers.tiktok.com/doc/content-posting-api-reference-photo-post and https://developers.tiktok.com/doc/content-sharing-guidelines |
| Draft / inbox upload (API) | same as video | same as video | up to 5 pending shares per 24 h per app/user (photo doc) | The creator finishes the post in the TikTok app. Source: https://developers.tiktok.com/products/content-posting-api/ |
| Scheduled post | same as video | scheduled posts: 15 minutes to 10 days ahead per TikTok's scheduler announcement; newer limits `unverified` | cannot be edited after scheduling; delete and re-upload to change | Business accounts and creators; web upload page. Source: https://ads.tiktok.com/business/en-US/blog/introducing-video-scheduler-now-you-can-plan-tiktoks-in-advance |
| LIVE | vertical or landscape `unverified` | no documented duration cap in pages read | n/a | Eligibility (age 18, follower minimum) not confirmed on an accessible TikTok page (`unverified`). The disclosure toggle can be used when going LIVE. Source: https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service |
| Story-style / ephemeral | not researched | n/a | n/a | `unverified` whether TikTok Stories are active in Egypt |
| Text-only post | not researched | n/a | n/a | `unverified` |
| Channel / broadcast | none documented | n/a | n/a | TikTok has DMs and LIVE; no broadcast channel was found in sources read (`unverified`). |
| TikTok Shop | n/a | n/a | n/a | Commerce feature with its own seller policies; not researched here (`unverified`). |

## 3. Text limits
| Item | Limit | Source / status |
|---|---|---|
| Video caption (API title) | 2200 UTF-16 runes; hashtags and mentions inside are parsed | https://developers.tiktok.com/doc/content-posting-api-reference-direct-post |
| Video caption (in-app) | 4000 characters is widely reported since 2023; TikTok's own page was blocked to me | `unverified`; stay under 2200 to be safe |
| Photo post title / description | 90 / 4000 UTF-16 runes | https://developers.tiktok.com/doc/content-posting-api-reference-photo-post |
| Bio | not found on an accessible official page (commonly 80 characters) | `unverified` |
| Display name / @username | not found | `unverified` |
| Comment | not found | `unverified` |
| Hashtags | no official count cap found; they count toward the caption limit | `unverified` as a rule |
| Mentions | parsed in the caption; no official cap found | `unverified` |
| Links | not clickable in captions; website link in bio depends on account type and eligibility | `unverified` (not confirmed on an accessible TikTok page) |
| Emoji / Arabic / RTL | the API counts UTF-16 runes, so emoji and some Arabic compounds use more than one unit; RTL display is handled by the app | counting rule from the API doc; RTL behavior `unverified` |

## 4. Posting and cadence
No official cadence or best-time guidance was reachable, so everything here is heuristic.
- API cap: a creator account typically can publish around 15 posts per day through Direct Post; hitting it returns `spam_risk_too_many_posts`. Source: https://developers.tiktok.com/doc/content-sharing-guidelines
- Frequency (heuristic): 3 to 5 videos per week is a sustainable floor for a brand; 1 per day for creator-led accounts. Test, do not assume.
- Timing (heuristic): use the account's own analytics (Followers tab, most active times) and Egypt evening hours as a hypothesis, then A/B test by posting the same format at two slots.
- Processing: content can take a few minutes to appear after posting, which agents should not treat as a failure. Source: https://developers.tiktok.com/doc/content-sharing-guidelines
- Funnel plan:
  - Awareness: hook-first short videos (under about 30 s is practitioner advice), trend sounds from the Commercial Music Library when the account is a business, photo-mode carousels.
  - Consideration: demos, comparisons, FAQ answers in comments (video replies), longer videos over 1 minute if the account is in the Creator Rewards Program (section 5).
  - Conversion: pinned video with the offer, link in bio, TikTok Shop or LIVE offers, clear CTA in the caption.
  - Retention: LIVE sessions, series with a repeating title, replies to comments.

## 5. Distribution and ranking signals
Official:
- Moderation has four pillars: removal, age restriction, FYF eligibility and community empowerment tools. Recommendation is not guaranteed; content not appropriate for a broad audience is ineligible for the FYF. Source: https://www.tiktok.com/community-guidelines/en
- Content disclosed incorrectly or undisclosed marketing is FYF-ineligible. Source: https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities
- Content that manipulates engagement (like-for-like, false incentives to engage) is FYF-ineligible; conspiracy theories and unverified emergency information are FYF-ineligible. Source: https://www.tiktok.com/community-guidelines/en/integrity-authenticity
- Turning on the commercial disclosure setting does not affect feed distribution. Source: https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service
- Creator Rewards, as described by a secondary source summarizing TikTok's newsroom post, rewards originality, play duration, search value and audience engagement. Source: https://www.makeinfluence.com/en/academy/tiktok-creator-rewards-program-how-organic-monetization-works-in-2026 (secondary source)

Practitioner observation, not an official rule: strong first-second hook, watch-through and rewatch rate, shares and saves, searchable keywords in captions, on-screen text and spoken words, consistent niche. TikTok does not publish the weights.

Creator Rewards eligibility per a secondary source: age 18+, 10,000 followers, 100,000 views in the last 30 days, a personal (not Business) account, original videos longer than 1 minute, and availability in the creator's country. Egypt availability is not confirmed (`unverified`). Source: https://www.makeinfluence.com/en/academy/tiktok-creator-rewards-program-how-organic-monetization-works-in-2026

## 6. Community rules and policy hot spots
| Topic | What the rules say | Source |
|---|---|---|
| Fake engagement / buying followers | Trading services that inflate engagement (selling followers or likes) and instructions to boost engagement artificially are banned; inauthentic followers and likes are removed. | https://www.tiktok.com/community-guidelines/en/integrity-authenticity |
| Engagement bait / giveaways | Like-for-like arrangements and false incentives are FYF-ineligible. The page does not mention general giveaways. Giving away banned goods counts as trade and is banned. | integrity page above; https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities |
| Impersonation | Posing as a real person or entity is banned; parody or fan accounts are allowed if disclosed in the account name (not only the @username). | integrity page above |
| Misinformation | Banned when likely to cause significant harm: crisis, medical, climate-denial, civic and election misinformation. Edited media that misleads about real events is banned. | integrity page above |
| AI-generated content | Realistic synthetic or altered media must be clearly labeled (sticker or caption). Synthetic media of private individuals or minors is banned; so are adult public figures in political or commercial endorsements. The API has an `is_aigc` flag for the label. | integrity page above; https://developers.tiktok.com/doc/content-posting-api-reference-direct-post |
| Health, finance, political | Paid political marketing is banned. Gambling promotion is banned (approved advertisers may run paid ads). Alcohol, tobacco, drugs, weapons trading are banned. Weight-loss, cosmetic surgery without risk warnings and gambling content are age-restricted. Fraud and scams are banned. | https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities and youth-safety page |
| Minors | Users under 13 are banned where identified; content risking harm to minors is banned; teen accounts get restrictive defaults. FYF needs age 16+. | https://www.tiktok.com/community-guidelines/en/youth-safety |
| Copyright and music | Business accounts must use the Commercial Music Library (CML) for branded content; the General Music Library is not cleared for businesses. | https://ads.tiktok.com/business/tr/blog/audio-library-royalty-free-music |
| Automation and bots | Via API only (section 8). Unaudited apps can only post privately; do not add watermarks, logos or promotional text on behalf of users. | https://developers.tiktok.com/doc/content-sharing-guidelines |
| Strikes | The community-guidelines strike system (counts and durations) could not be fetched. | `unverified` |

## 7. Branded content, ads disclosure and legal
- Tool: the **content disclosure** setting (Content disclosure and ads). Two options: **Your brand** (label "Promotional content") for your own business, and **Branded content** (label "Paid partnership") for a third party paid or incentivized. You can tag a Brand Partner. Once a post or LIVE is published, the label cannot be changed; remove and repost. Source: https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service
- Branded content cannot be private (visibility must be public/non-private). API apps must show both checkboxes and consent links. Source: https://developers.tiktok.com/doc/content-sharing-guidelines
- Branded Content Policy: the promoted product must be clear from the video itself (speech or caption); creators must follow applicable law, avoid false claims, protect minors. Prohibited categories include adult products, alcohol, tobacco and vapes, drugs including CBD, financial products (loans, credit cards, crypto, multi-level marketing), gambling, pharmaceuticals and health supplements, political advertising, professional services (accounting, legal, immigration), weapons, weight-loss products, counterfeit goods. Source: https://www.tiktok.com/legal/page/global/bc-policy/en
- TikTok may keep certain branded content in its Commercial Content Library where legally required, even after deletion. Same source.
- Practical rule: when a video was paid, gifted, affiliate-linked or made for your own brand, switch the disclosure on and also say "إعلان" or "#ad" in the caption (practitioner habit). This is not legal advice. In the EU, the US (FTC endorsement guidance) and Egypt (consumer protection law), undisclosed paid endorsements and misleading claims create exposure; check a lawyer for specifics. The Egyptian statute name and article numbers were not researched (`unverified`).

## 8. API and automation
TikTok for Developers (https://developers.tiktok.com) offers several products:
- **Login Kit**: OAuth sign-in. **Display API**: `/v2/user/info/` (open_id, avatar, display_name, profile link, bio) and `/v2/video/list/`, `/v2/video/query/` (public video metadata); scopes `user.info.basic`, `video.list`. Rate limit 600 per minute sliding window per endpoint; higher limits by request to TikTok support. Sources: https://developers.tiktok.com/doc/display-api-overview and https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit . The Display API pages do not list analytics or comments.
- **Content Posting API**: Direct Post (`video.publish` scope, app must be approved) publishes video or photos; Upload (`video.upload`) sends a draft to the creator's inbox. Source: https://developers.tiktok.com/doc/content-posting-api-get-started
  - Unaudited apps: all content is private (`SELF_ONLY`); at most 5 users posting per 24 h and the posting accounts must be private. An audit is needed for public posting. Source: https://developers.tiktok.com/doc/content-sharing-guidelines
  - Rate limits: 6 requests per minute per user token for the video init call; query creator info 20 per minute per token. Source: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post and https://developers.tiktok.com/doc/content-posting-api-reference-query-creator-info
  - Mandatory UX: call creator info on each render, show the nickname, no default privacy, no default interactions, disclosure toggle off by default, music-usage consent before publish, no watermark or promotional text added. Source: https://developers.tiktok.com/doc/content-sharing-guidelines
  - Scheduling: no scheduling parameter was found in the API docs I read (`unverified`); schedule in your own tool or use TikTok's own scheduler.
- **Research API**: comment queries (video_id or comment_id, up to 100 per page) under the `research.data.basic` scope; eligibility (research use) was not stated on the page, `unverified`. Source: https://developers.tiktok.com/doc/research-api-specs-query-video-comments
- **TikTok API for Business**: Marketing API for ads and an **Organic API** (Accounts, Mentions, TikTok One, Discovery, Spark Ads Recommendation) plus a **Business Messaging API** (DMs, automated and welcome replies). Eligibility and approval steps are not on the help page. Source: https://ads.tiktok.com/help/article/marketing-api?lang=en
- Auth: OAuth 2.0 access tokens per creator; keep client secrets and tokens in secure credential storage, never in prompts or repos.
- What has **no public API in the sources read**: replying to comments for personal/creator accounts through the Display API, reading personal-account analytics through the Display API, LIVE control, following/unfollowing, and bulk DMs for non-business accounts (`unverified` for each).
- Forbidden: scraping to build datasets or bots, buying followers or engagement, automation that circumvents limits (platform terms page not fetchable; derived from community guidelines and developer rules above).
- Official scheduling options: TikTok's web scheduler (Business and creator accounts), Content Posting API draft/inbox flow, and third-party tools that use the Content Posting API.

## 9. Analytics
Metric definitions were not available on an accessible TikTok page (`unverified` for exact definitions). Native tools: Analytics inside TikTok Studio on web/app (Overview, Content, Viewers, Followers, LIVE). Commonly used metrics and the question each answers (practitioner mapping):
- Video views and traffic source (FYF vs Following vs Search vs Profile): where reach comes from.
- Average watch time and watched-full-video rate: whether the hook and pacing work.
- Likes, comments, shares, saves: depth of interest; saves and shares signal utility and virality.
- Followers growth and follower activity by hour: when to post.
- Profile views and link clicks: conversion toward the website.
- Search queries that led to the video: keyword opportunities.
The Display API exposes video metadata and public counts only as described in its docs; check the Video Object doc before building dashboards (`unverified`).

## 10. Cases
1. **Situation:** Reach suddenly drops on all videos.
   **Do:** Check Analytics traffic sources and recent posts for FYF-ineligible triggers: undisclosed promotion, engagement bait ("like for like"), unlabeled AI content, misleading edits, re-uploaded watermarked content. Fix the pattern, then post normal content for a week. Source for triggers: https://www.tiktok.com/community-guidelines/en/integrity-authenticity
   **Avoid:** Deleting many videos at once or buying views; deletion does not reset a ban and fake engagement is banned.
2. **Situation:** Account restricted, or a video removed.
   **Do:** Read the in-app notice, appeal inside the app, remove similar videos that break the same rule, and keep screenshots. Severe or repeated violations can lead to an account ban (strike counts are `unverified`). Source: https://www.tiktok.com/community-guidelines/en
   **Avoid:** Opening a second account to keep posting the same content; ban-evasion risk.
3. **Situation:** A trending song is unavailable or muted on a business account.
   **Do:** Switch to a track from the Commercial Music Library, or upload a licensed or original sound. The General Music Library is not cleared for businesses. Source: https://ads.tiktok.com/business/tr/blog/audio-library-royalty-free-music
   **Avoid:** Using a personal account to promote a business just to get the trend sound; TikTok warns of copyright risk.
4. **Situation:** A wave of negative or hateful comments.
   **Do:** Use comment filters and keyword filters (community empowerment tools), pin a calm factual reply, report abusive comments, and respond to genuine complaints with a video reply or a DM. Source for tools: https://www.tiktok.com/community-guidelines/en
   **Avoid:** Arguing in comments or mass-deleting valid criticism; it fuels the story.
5. **Situation:** A fake account impersonates the brand.
   **Do:** Report it as impersonation, post a pinned video with the real @handle, and add the official handle to the bio. Impersonation is banned except disclosed parody. Source: https://www.tiktok.com/community-guidelines/en/integrity-authenticity
   **Avoid:** Contacting the impersonator or paying "recovery" services.
6. **Situation:** Planning a giveaway.
   **Do:** Choose a prize outside the banned categories (alcohol, tobacco, drugs, weapons, counterfeit goods), state rules, dates and winner selection in the caption, make it clear who sponsors, and turn on the disclosure toggle when a partner sponsors the prize. Source: https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities
   **Avoid:** "Like-for-like", mass tagging or mandatory re-posting requirements; false incentives to engage are FYF-ineligible. Local contest and lottery law in Egypt was not researched (`unverified`).
7. **Situation:** Cross-posting a Reel or Short.
   **Do:** Export a clean file without the other app's watermark, check the safe zones for TikTok's UI, rewrite the hook and caption natively, and use TikTok's own captions.
   **Avoid:** Leaving a visible watermark or logo of another platform; practitioners report reduced reach (practitioner observation, not an official rule).
8. **Situation:** A published video has a wrong disclosure label or a claim error.
   **Do:** The disclosure label cannot be changed after publishing, so delete and repost with the correct selection. For caption typos use the in-app edit options (feature availability `unverified`). Source: https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service
   **Avoid:** Leaving an undisclosed paid post up; it can be removed or restricted.
9. **Situation:** An n8n workflow posts via the Content Posting API and gets `unaudited_client_can_only_post_to_private_accounts`.
   **Do:** Get the app audited; meanwhile test with a private account and `SELF_ONLY`. Respect 6 requests per minute and the daily cap error `spam_risk_too_many_posts`. Source: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
   **Avoid:** Passing default privacy values or forcing public visibility without showing the user a choice; this breaks the content-sharing guidelines.
10. **Situation:** Crisis (product complaint going viral).
    **Do:** Pause scheduled posts, publish one factual response video or pinned comment, keep paid-partner posts consistent with the response, and document everything. 
    **Avoid:** Deleting critical comments in bulk or posting jokes.
11. **Situation:** Handing the account to an agency.
    **Do:** Use TikTok Business Center or authorized app access where available (`unverified` for exact roles), give least privilege, enable 2-step verification, and revoke at the end.
    **Avoid:** Sharing the password or SMS codes.

## 11. Arabic and Egypt notes
- TikTok's reach in Egypt is large (48.8M ad reach for ages 18+; +25.2% year on year). Source: https://datareportal.com/reports/digital-2026-egypt
- Caption length counting uses UTF-16 runes in the API; Arabic letters usually count as one, emoji can count as two. Source: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- Mixed Arabic and Latin hashtags: keep one language per hashtag and test the line break; RTL rendering rules are not documented in sources read (`unverified`).
- Dialect: no official rule; Egyptian Arabic captions and on-screen text are practitioner standard for local reach. Search value increases when the spoken language and the caption language match (practitioner observation).
- Branded content prohibited categories matter in Egypt: financial products, crypto, multi-level marketing, health supplements, weight loss, professional services cannot use the branded-content toggle. Source: https://www.tiktok.com/legal/page/global/bc-policy/en
- Creator Rewards availability in Egypt, TikTok Shop availability in Egypt, payout and verification methods in Egypt: not confirmed (`unverified`). Check the in-app Creator tools menu.
- Cultural caution: religious, political and sensitive-event content is risky for both brand reputation and platform rules (paid political marketing is banned). Source: https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities

## 12. Pre-publish checklist
1. Is the video 9:16, between 360 and 4096 px per side, 23 to 60 fps, MP4/MOV/WebM, and within the creator's max duration?
2. Is the caption at most 2200 characters (hashtags included)?
3. Is every sound licensed, from the Commercial Music Library if the account is a Business account?
4. Is there a hook in the first 1 to 2 seconds and on-screen text that works muted?
5. Is any sponsorship, gifted product, affiliate link or own-brand promotion declared in the disclosure setting?
6. Is the product category outside the branded-content prohibited list?
7. Is realistic AI-generated or altered media labeled (`is_aigc` or sticker/caption)?
8. Does the post avoid engagement bait, false incentives and misleading edits?
9. Does it avoid minors in unsafe or promotional situations and age-restricted topics?
10. Are claims (health, finance, results) supportable and in line with local law?
11. Is the watermark of other platforms removed and are third-party faces and brands cleared?
12. Is the posting account correct, and is the daily post cap and 6-per-minute API rate respected?

## 13. Sources
- https://developers.tiktok.com/doc/content-posting-api-get-started
- https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- https://developers.tiktok.com/doc/content-posting-api-reference-photo-post
- https://developers.tiktok.com/doc/content-posting-api-reference-query-creator-info
- https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide
- https://developers.tiktok.com/doc/content-sharing-guidelines
- https://developers.tiktok.com/doc/display-api-overview
- https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit
- https://developers.tiktok.com/doc/research-api-specs-query-video-comments
- https://developers.tiktok.com/products/ and https://developers.tiktok.com/products/content-posting-api/
- https://developers.tiktok.com/doc/overview
- https://www.tiktok.com/community-guidelines/en
- https://www.tiktok.com/community-guidelines/en/integrity-authenticity
- https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities
- https://www.tiktok.com/community-guidelines/en/youth-safety
- https://www.tiktok.com/legal/page/global/bc-policy/en
- https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service
- https://ads.tiktok.com/business/tr/blog/audio-library-royalty-free-music
- https://ads.tiktok.com/business/en-US/blog/introducing-video-scheduler-now-you-can-plan-tiktoks-in-advance
- https://ads.tiktok.com/help/article/marketing-api?lang=en
- https://datareportal.com/reports/digital-2026-egypt
- https://www.makeinfluence.com/en/academy/tiktok-creator-rewards-program-how-organic-monetization-works-in-2026 (secondary)
- https://www.socialmediatoday.com/news/tiktok-changes-rules-on-music-usage-by-businesses/577734/ (secondary, 2020 background)
