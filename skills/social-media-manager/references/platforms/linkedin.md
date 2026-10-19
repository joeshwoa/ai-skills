# LinkedIn — rules and playbook
Last verified: 2026-10-19

Source note: LinkedIn Help Center pages (linkedin.com/help) block automated fetching, so consumer-UI limits below come from secondary sources and are marked `secondary`. Anything from learn.microsoft.com (LinkedIn API docs) is marked `official-API-doc`. Re-check `secondary` items in the LinkedIn UI before relying on them.

## 1. Snapshot
- What it is: professional network; best for B2B, employer brand, recruiting, thought leadership, partnerships, services and consultants. Weak for impulse consumer retail.
- Scale: about 1.20 billion registered members in LinkedIn's own ad tools (Jan 2025; registered accounts, not active users) per DataReportal https://datareportal.com/essential-linkedin-stats
- Egypt: 15.0 million member ad reach in late 2025, up 3.0 million (+25%) year on year, 7th among platforms by ad reach in Egypt (behind Facebook, YouTube, TikTok, Messenger, Instagram, Snapchat) per DataReportal Digital 2026 Egypt https://datareportal.com/reports/digital-2026-egypt . "Members" are registered accounts, not monthly users.
- Other Arab countries: no sourced figure gathered. `unverified`.
- Surfaces: personal profiles (people are the main reach engine), Company Pages (brand home, jobs, employee advocacy), Showcase pages, Newsletters and Articles, Events, Live (application based), Groups.

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Text post | n/a | 3,000 characters (`secondary`) | n/a | Feed cuts after roughly the first 140-210 characters on mobile (`secondary`, LinkedIn publishes no exact cut). Put the hook first. |
| Single image | 1080x1080 or 1080x1350 recommended (`secondary`); ratio range reported 3:1 to 4:5 (`secondary`) | n/a | JPG, PNG, GIF (GIF up to 250 frames); fewer than 36,152,320 pixels (`official-API-doc`, Images API). No hard MB cap published; 3 MB appears in Page-image guidance (`secondary`) | Image URN must exist before post creation via API. |
| Multi-image | same as single image | up to 20 images (`secondary`) | as above | Organic only; API content type `MultiImage`. First image drives layout. |
| Document / "carousel" PDF | 1080x1080 or 1080x1350 pages (`secondary`) | up to 300 pages (`official-API-doc`) | 100 MB; PDF, PPT, PPTX, DOC, DOCX (`official-API-doc`, Documents API) | Best-performing educational format by practitioner lore. Keep body text 14 pt+ (`secondary`). Document can be reused across posts and ads. |
| Native video | 1:1, 4:5, 9:16, 16:9 work; supported ratio 1:2.4 to 2.4:1 (`secondary`) | 3 s to 30 min (`official-API-doc`, Videos API); UI organic cap reported 10-15 min (`secondary`) | MP4; 75 KB to 500 MB per the spec table, API field maximum 5 GB (`official-API-doc`) | Captions via API: one SRT file per video, English only. Thumbnail upload optional. |
| Link post (Article type in API) | preview image 1.91:1, 1200x627 (`secondary`) | n/a | n/a | Preview comes from Open Graph tags in the UI. Via API you must supply title, description and thumbnail yourself (no URL scraping). |
| Poll | n/a | n/a | n/a | Organic only via API (`Poll` content type). Option count and duration limits `unverified`. |
| LinkedIn Article (long-form) | n/a | title about 150 chars, body about 110,000 chars (`secondary`, single source) | n/a | No publishing API found in the docs reviewed. `unverified` whether API supports it. |
| Newsletter | n/a | n/a | n/a | Built on Articles. Rules, limits, API: `unverified`. |
| LinkedIn Live | 16:9, max 1080p, 30 fps | max 4 hours | H.264 + AAC, video up to 6 Mbps, audio 128 kbps/48 kHz, keyframe every 2 s (`official-API-doc`, Live Events APIs) | Application-based access (beta). Needs RTMP(S) encoder; preferred partners include Restream, Socialive, StreamYard, Switcher Studio (LinkedIn business page). |
| Event | n/a | n/a | n/a | Events Management API is self-serve on request (Increasing Access page). |
| Story / status / channel | not available | n/a | n/a | No equivalent verified. Treat as not available. |

## 3. Text limits
- Post body: 3,000 characters including spaces, line breaks, hashtags, mentions (`secondary`: eden.so, contentin.io; the Posts API only returns `400 FIELD_LENGTH_TOO_LONG` without a number).
- Comment: about 1,250 characters (`secondary`, single source) - the Comments API page states no limit. Treat as `unverified`.
- Headline 220, About 2,600, connection note 300, DM 8,000, article title 150 (`secondary`, single source, "observed values"). All `unverified`.
- Company Page tagline / description limits: `unverified`.
- Hashtags: no official maximum found. 3 to 5 is common marketing advice, not a LinkedIn rule (`secondary`). Hashtag following was reported removed, so hashtags act as topic signals (`secondary`).
- Mentions: via API, organization mention text must match the full organization name, case-sensitive; member mentions need to match only one name (`official-API-doc`).
- Links: clickable in posts. Practitioner lore says external links in the body depress reach; LinkedIn has not confirmed it. Common workaround is link in first comment (lore; weigh against Page-comment visibility).
- Arabic / RTL: LinkedIn renders Arabic text; exact RTL alignment and mixed-direction behaviour in posts `unverified`. Test a draft in app and desktop before scheduling.

## 4. Posting and cadence
Heuristic, not official (`practitioner observation, not an official rule`):
- Company Page: 3 to 5 posts a week is a sustainable range; personal profiles of founders and employees usually out-reach the Page. Page posts alone rarely drive reach.
- Timing: Tuesday to Thursday business hours in the audience time zone is the common heuristic. For Egypt audiences, test 09:00-11:00 and 19:00-21:00 Cairo time; measure, do not assume. Egypt week is commonly Sunday-Thursday; Friday and Saturday engagement is typically lower (heuristic).
- Funnel mapping:
  - Awareness: document carousels, short native video with captions, industry-insight text posts, founder takes.
  - Consideration: case studies, how-it-works documents, webinars/Live, newsletter issues, employee stories.
  - Conversion: demo or event invites, job posts, lead-gen via ads (not organic), comment-to-DM only manually.
  - Retention / advocacy: customer wins with permission, product updates, employee advocacy posts.
- Scheduling: Company Pages have native scheduled posts in the UI (help article exists, limits not read: `unverified`). Third-party schedulers hold your post and publish at time through the API.

## 5. Distribution and ranking signals
Official:
- LinkedIn does not publish ranking weights. Its engineering blog describes a feed that ranks by predicted relevance to each member (engineering.linkedin.com/blog, FollowFeed and "Community-focused Feed optimization" posts). Those pages could not be fetched here, so no specific official claim is made. `unverified`
- Page and member analytics expose impressions, unique impressions, clicks, reactions, comments, shares (see section 9). Those are outcomes, not documented ranking inputs.

Practitioner lore (practitioner observation, not an official rule):
- Early comments, saves and meaningful replies in the first hour help; one-word "great post" comments and engagement pods are discounted or risky.
- Document and multi-image posts earn long dwell time; text-only with a strong first line also performs.
- Posts from a person's profile usually out-reach the same text from a Company Page.
- Topical consistency (posting about one expertise area) is said to help relevance. Reported shift to "expertise and relevance" ranking is commentary, not an official spec.

## 6. Community rules and policy hot spots
- Automation and scraping: LinkedIn's "Prohibited software and extensions" help page says members using prohibited software risk having accounts restricted or shut down (quoted via contentin.io; page itself blocked to bots). The User Agreement (s. 8.2) prohibits using scripts or robots to scrape or copy the Services, including profiles and other data (quoted via secondary). Treat these as hard lines:
  - No browser extensions or bots that send connection requests, messages, likes or comments, or that scrape profiles or search results.
  - No driving a logged-in session (li_at cookie) from n8n, Puppeteer, Phantombuster-style tools, or MCP servers that wrap a session cookie.
  - Safe path: official OAuth apps through the Community Management API / Share on LinkedIn, with a human deciding each post.
- Engagement pods and fake engagement, mass templated comments, buying followers or likes: expect restriction; exact policy wording `unverified` (Professional Community Policies page blocked).
- Spam: repeated identical posts, tag-spam, unsolicited bulk messaging. Enforcement follows volume and inauthenticity (secondary reading).
- Impersonation / fake profiles: report via Help; personal profiles are expected to be real people (policy wording `unverified`). For brand impersonation see case 5.
- Health, finance, political claims: LinkedIn Professional Community Policies prohibit misinformation and harmful content (details `unverified`); finance-service promotion also falls under local law (section 7).
- Copyright and music: use licensed audio only in video; no LinkedIn music library for organic posts verified. `unverified`
- Minors: LinkedIn is a professional network with age minimums by country; do not target minors. Specific minimum `unverified`.
- Giveaways/contests: no LinkedIn organic-contest policy was readable. Ask the platform's rules before running one; do not require "like + comment + tag" mechanics that look like engagement bait. `unverified`
- API data restrictions (binding on any automation, see section 8): no social-feed widgets from API data, no sales/recruiting/ads use of member data, no combining with other data, no export.

## 7. Branded content, ads disclosure and legal
- LinkedIn has a "Label post as brand partnership" tool (help article exists; content not readable here). Use it for paid or gifted creator posts and still add plain-word disclosure ("Sponsored", "Paid partnership with X") in the text. `unverified` for exact eligibility.
- US FTC "Disclosures 101": disclose any financial, employment or family tie, including free product; place the disclosure with the endorsement, not in a bio or hashtag pile; use plain words ("ad", "sponsored"); same language as the endorsement; platform tools alone may not be enough; the influencer is responsible https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- EU: unfair-commercial-practices rules require ads to be identifiable as ads; national regulators publish influencer guidance. UK: CAP/CMA guidance (referenced by X's policy page).
- Egypt (high level, not legal advice): Consumer Protection Law No. 181 of 2018 covers misleading advertising; Personal Data Protection Law No. 151 of 2020 affects marketing messages and lead data; Law 180 of 2018 was reported in 2018 to treat accounts with 5,000+ followers as media outlets under Supreme Council for Media Regulation oversight (africanews, 2018). Confirm current application with Egyptian counsel before running influencer campaigns. This is not legal advice.
- Lead and data handling: LinkedIn API member data storage limits apply (section 8).

## 8. API and automation
Official APIs (learn.microsoft.com/en-us/linkedin):
- Share on LinkedIn (self-serve): `w_member_social`, post text, article, image or video as a member via `ugcPosts`. Limits: 150 requests per member per day, 100,000 per app per day (UTC; page last updated Feb 2025). No approval step described.
- Community Management API (Posts, Comments, Social Metadata/Reactions, Images, Videos, Documents, Page and member analytics, Social Action notifications, People Typeahead): approval required.
  - Eligibility: registered legal organization, commercial use case, verified business email, legal name, address, website, privacy policy, verification by a super admin of the associated Page; app must not use LinkedIn or Microsoft branding. Personal email fails vetting.
  - Development tier: 500 calls per app and 100 per member per 24 h, no BATCH_GET, Social Actions webhooks disabled, 12 months to finish testing.
  - Standard tier: no restrictions; needs screen recording of each use case, company/product overview, test credentials, data-storage compliance. Reviewed for compliance; LinkedIn may decline. A rejected app cannot reapply; create a new app. No stated review time.
  - Scopes: `w_organization_social` (post as Page; needs ADMINISTRATOR, DIRECT_SPONSORED_CONTENT_POSTER or CONTENT_ADMIN), `r_organization_social`, `w_member_social`, `rw_organization_admin` (analytics). `r_member_social` is closed; no new requests accepted.
- Posts API: `POST /rest/posts` with headers `Linkedin-Version: YYYYMM` and `X-Restli-Protocol-Version: 2.0.0`. Types: text, image, MultiImage, video, document, article, poll, celebration (organic); carousel is sponsored-only. Edit only `commentary`, CTA fields, `lifecycleState`. Delete is idempotent; no batch delete. Batch get supported (not on dev tier). Targeted organic posts need audience over 300 members.
- Scheduling: not documented in the Posts API (states DRAFT, PUBLISH_REQUESTED, PUBLISHED, PUBLISH_FAILED; only PUBLISHED accepted at creation). Do the timing in your own scheduler (n8n cron) and call the API at the publish time, or use the native Page scheduler by hand.
- Comments: read, create, edit, delete as person or organization; org actions pass `actor`. 429 if a member comments too fast (one-minute short-term limit). Comment length limit not documented.
- Messaging/DMs: not part of the Community Management API as documented. Treat as no API. `unverified`
- Analytics: see section 9.
- Live Events API: beta; apply; scopes `w_member_live` or `w_organization_live`; Development tier about 100 requests/day per Live API; Standard needs certification video.
- Tokens: 3-legged OAuth, access token 60 days; refresh tokens only for a limited set of partners; otherwise re-authorize before expiry. Redirect URI must be HTTPS and exact; authorization code valid 30 minutes.
- Rate limits: daily, reset at midnight UTC, per application and per member; limits vary by endpoint and are not published; read them in Developer Portal > app > Analytics. 429 on exceed. Email alert at 75% of an app-level quota.
- API versions: versioned monthly. 202510 sunsets 2026-10-15 and 202511 sunsets 2026-11-16. Use the newest version.
- Forbidden: member data in social feeds or intranet widgets; advertising, sales, recruiting or lead use; export or transfer of member data; combining with other data; storing member social activity more than 48 hours or most profile data more than 24 hours; fake or headless accounts; one individual profile managing many customers' accounts. Scraping and bots are separately prohibited by the User Agreement.
- n8n: use the official LinkedIn credentials / OAuth app; set Schedule trigger plus HTTP Request for `/rest/posts` after approval. Never store cookies.

## 9. Analytics
- Organic share statistics (`organizationalEntityShareStatistics`, 12-month rolling window, `rw_organization_admin`, ADMINISTRATOR only): impressionCount, uniqueImpressionsCount, clickCount, likeCount, commentCount, shareCount, engagement = (clicks + likes + comments + shares) / impressions. Smallest granularity is 1 day. Sponsored data goes through Ad Analytics.
- Page statistics: allPageViews, uniquePageViews, desktop/mobile splits, careers/jobs views, breakdowns by country, function, industry, seniority, staff count range.
- Follower and video analytics (watch time, views, viewers) exist in the Community Management API.
- Which metric answers what: reach = unique impressions; resonance = engagement rate; interest in the offer = clickCount; audience fit = page and follower breakdowns by function and seniority; video hook strength = views vs watch time.
- For counts that match the feed exactly, read socialActions/Social Metadata rather than statistics.

## 10. Cases
**Situation:** Reach on Company Page posts drops sharply for two weeks.
**Do:** Check Page analytics for a format or topic change; compare unique impressions vs impressions; check that no admin used a third-party extension or logged in from odd locations; test a document post and a personal-profile repost by an exec; wait one full week of data before changing strategy.
**Avoid:** Posting more of the same, buying engagement, or blaming "the algorithm" without data. Never add engagement pods.

**Situation:** Account or profile restricted ("unusual activity") after using an automation tool.
**Do:** Stop the tool immediately, remove browser extensions, change password and sign out all sessions, follow the in-app restriction/appeal flow with a calm, factual message, and wait; document what ran and when.
**Avoid:** Opening new accounts to continue, re-running the tool, mass appeals, or promising LinkedIn the tool is "official" when it is not.

**Situation:** Negative comment wave on a Page post (customers or competitors).
**Do:** Reply once, factually, from the Page; move detailed support to a named contact; hide or delete only comments that break the Professional Community Policies (abuse, spam, doxxing) and keep a screenshot log; brief the team before replying at scale.
**Avoid:** Deleting legitimate criticism, arguing in threads, or auto-replying with a template to every comment.

**Situation:** A fake Page or profile impersonates the brand and DMs job-seekers or customers.
**Do:** Collect URLs and screenshots, report the profile/Page as impersonation via LinkedIn's report flow, post a short warning from the real Page listing official channels (domain, careers URL), alert HR and customer support; consider a legal notice if money is involved.
**Avoid:** Sharing the fake's link in a way that boosts it; engaging the impersonator.

**Situation:** Planning a giveaway or lead contest.
**Do:** Publish clear terms (eligibility, dates, prize, winner selection, data use) on a landing page; use form or event registration rather than "like + comment + tag"; check LinkedIn's current rules in the Help Center first (`unverified` here); comply with Egyptian/EU/US contest and data rules.
**Avoid:** Engagement-bait mechanics, requiring tags of friends, collecting data without consent.

**Situation:** Cross-posting a post from X or Instagram.
**Do:** Rewrite to LinkedIn's format: stronger first line, professional framing, native upload of video/images (not a pasted link), remove @handles and hashtags that do not exist on LinkedIn, add captions.
**Avoid:** Pasting text with "RT", screenshots of tweets, watermarked TikTok videos, link-only posts.

**Situation:** A published post contains an error or must be removed.
**Do:** Typo or small fix: edit the post (API `PARTIAL_UPDATE` allows `commentary` edits). Wrong facts: edit plus a pinned correction comment. Serious (legal, confidential, harmful): delete (idempotent in API), record why, notify stakeholders.
**Avoid:** Silent deletion of a post that already caused public debate, with no follow-up.

**Situation:** Crisis (layoffs, data breach, controversial exec post).
**Do:** Pause all scheduled posts across Page and exec profiles; publish one approved statement from the Page; switch comment handling to a human with a briefing doc; resume the calendar only after sign-off.
**Avoid:** Scheduled "celebration" posts going out on top of bad news.

**Situation:** Handing over Page access to an agency or agent.
**Do:** Add the agency member as a Page admin with the least role needed (Content admin for posting; Analyst for reports) from a super admin account; keep at least two super admins in the company; for API use, have the company register the Community Management app under its own legal entity.
**Avoid:** Sharing a password or session cookie, using one individual profile to manage several clients, or letting the agent become the only super admin.

**Situation:** An n8n workflow should "auto-post and auto-comment" for engagement.
**Do:** Automate drafting, scheduling and reporting via official API; require a human approve step for comments, replies and DMs.
**Avoid:** Auto-commenting on other people's posts, auto-connecting, scraping search results.

## 11. Arabic and Egypt notes
- Egypt member base: 15.0 million (late 2025, DataReportal). Egyptian professionals commonly post in English, Arabic or mixed; the best language depends on the audience (corporate/tech in English, SMEs and local services in Arabic). Test, do not assume.
- RTL: Arabic paragraphs display right-to-left; mixed Arabic/English lines and hashtags can render with odd ordering. Keep the first line fully Arabic or fully English; avoid starting with an English word followed by Arabic. Behaviour in LinkedIn specifically `unverified`; check on mobile and desktop.
- Hashtags: use a few, in the language of the post; Arabic hashtags without spaces or diacritics. Count and ranking effect `unverified`.
- Tone: formal and respectful for B2B; the "Hello Egypt" or "Ramadan Kareem" seasonal posts are common; avoid political and religious controversy.
- Week and holidays: working week is typically Sunday to Thursday; plan around Ramadan hours and public holidays (heuristic).
- Payments/verification: LinkedIn Ads payment options and ID verification availability for Egyptian entities `unverified`.
- Regulatory: see section 7 for the Law 180/2018 reporting; check with counsel for influencer campaigns.

## 12. Pre-publish checklist
1. Is the hook visible in the first two lines (about 140 characters)?
2. Is the post within 3,000 characters and free of broken mentions or hashtags?
3. Does every claim, number and customer name have a source or permission?
4. Is paid/gifted content labeled in plain words and with the brand-partnership tool where available?
5. Is native media attached (not a link-only or watermarked repost), with captions on video?
6. Is the document/PDF within 100 MB and 300 pages, text legible on mobile?
7. Is the author correct (Page vs person) and is the link/UTM correct and working?
8. Is the Arabic or mixed-direction text rendered correctly in a preview?
9. Is the publishing route official (API with approved app, or native scheduler) and free of cookies/scrapers?
10. Is a human approver recorded for any comment, reply or DM that will be sent?
11. Is the time not colliding with a crisis, holiday or other scheduled post?

## 13. Sources
- https://datareportal.com/reports/digital-2026-egypt
- https://datareportal.com/essential-linkedin-stats
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/documents-api?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2023-11
- https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access?view=li-lms-2025-10
- https://learn.microsoft.com/en-us/linkedin/marketing/restricted-use-cases?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/share-statistics?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/page-statistics?view=li-lms-2026-10
- https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits
- https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow
- https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access
- https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin
- https://learn.microsoft.com/en-us/linkedin/consumer/integrations/live-video/
- https://developer.linkedin.com/product-catalog/marketing/community-management-api
- https://business.linkedin.com/marketing-solutions/linkedin-events/getting-started
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.africanews.com/amp/2018/07/19/egyptians-with-5000-followers-on-twitter-to-be-supervised-as-media-outlets/
- Secondary (UI limits): https://eden.so/blog/linkedin-character-limits/ , https://contentin.io/blog/linkedin-post-specs/ , https://contentin.io/blog/linkedin-mcp-terms-of-service/
- Not fetchable (robots): LinkedIn Help pages "Prohibited software and extensions" (a1341387), "Automated activity on LinkedIn" (90586), User Agreement, Professional Community Policies.
