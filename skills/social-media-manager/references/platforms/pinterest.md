# Pinterest — rules and playbook
Last verified: 2026-10-19

Scope: organic Pinterest for a business or creator: Pins (image and video), boards, claimed websites, Rich Pins, the Pinterest API v5 organic endpoints, content and spam policy. Paid ads are mentioned only where they change organic behaviour. `unverified` means no official page confirmed it on the verification date.

## 1. Snapshot
- Pinterest is a visual search and planning engine. People save Pins to boards, so content keeps resurfacing; Pinterest says there is no set engagement window and a Pin can gain engagement hours, days, months or years after publishing (help.pinterest.com "Pin performance and distribution").
- Best for: evergreen visual content, how-to, recipes, home, fashion, beauty, travel, weddings, education, product discovery, and sending traffic to a website or shop.
- Scale: Pinterest ads reached 340 million users in January 2025 (DataReportal, from Pinterest's own tools; ad reach is not the same as monthly active users).
- Egypt / Arab world: Arabic is among the languages of Pinterest's policy pages, and Pinterest appointed DMS as sales representative across MENA (communicateonline.me headline; date `unverified`). Egypt-specific user numbers: `unverified`.
- Organic Pinterest is mostly a "link-out" channel: Pins link to a destination URL, so a claimed website and fast, relevant landing pages matter more than on most social platforms.
- Formats were simplified: organic content is now image Pins or video Pins. The old Idea Pin product is no longer a separate organic format (developers.pinterest.com "Create boards and Pins": "simplified our organic Pin formats to image or video Pins").

## 2. Content formats and specs

| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Image Pin | 2:3 recommended, 1000x1500 px (taller than 2:3 may be cropped in feeds) | n/a | BMP, JPEG, PNG, TIFF, WEBP; 20 MB on web; mobile apps 1 GB recommended | Title 100 chars, description 800, alt text 500. Safe zone px: top 270, left 65, right 195, bottom 790 |
| Video Pin | 9:16 (1080x1920) recommended for full-bleed; 1:2, 2:3, 3:4, 4:5, 1:1 also accepted | 4 s minimum, 5 min maximum (organic Pin specs). Pinterest recommends 15-60 s | Web MP4, M4V; apps MP4, MOV, M4V; H.264 or H.265. Organic file-size cap: `unverified` | Needs a cover image. Ad spec page lists 15 min and 2 GB for ads; do not use those for organic |
| Multi-image / multi-video Pin | per item | per item | Web creates one Pin per image (up to 10 files per upload); combining images and videos into one video Pin is app-only | API multiple_image_urls takes 2-5 images |
| Carousel Pin (image carousel) | 1:1 or 2:3 | n/a | 2-5 images, 20 MB each (ad spec page; organic carousel creation UI `unverified`) | Ad carousels with sales objective allow 2-10 |
| Collections / shop-the-look Pin | hero 1:1 or 2:3, hero image max 10 MB | secondary 3-24 items (3 min recommended) | Per ad spec page | Primarily a shopping format |
| Rich Pin (article, recipe, product) | same as image/video | n/a | Needs page meta tags | Syncs data from your site (see "Claimed website and Rich Pins" in section 5) |
| Product Pin / product tag | image/video | n/a | Up to 5 product tags per Pin | Product Pins need catalog or product rich Pin |
| Story / Live / status | not offered | | | Pinterest has no ephemeral stories product; `unverified` for any pilot |
| Text-only | not a format | | | Every Pin needs an image or video |
| Idea ad source Pin | image or video | | set `is_standard` false when creating via API | Only if you intend to promote as an Idea ad |

Limits on objects (developers.pinterest.com): up to 2,000 boards per account (including group boards); up to 200,000 Pins for personal accounts. Each user can schedule up to 10 Pins up to 30 days ahead (section 4).

## 3. Text limits
- Pin title: 100 chars. Description: 800 chars (not shown in home or search feed, only close-up). Text box on image Pins: 250 chars. Alt text: 500 chars. Link: 2048 chars (API schema).
- Profile bio: 500 chars. Username: the profile page lists "three to 30 characters" (appears to refer to the username; confirm in UI). Business display name limit: `unverified`. Board name and description limits: `unverified`.
- Comments: up to 500 chars; you can only add links to Pinterest in comments; up to 5 @mentions per comment; commenters accept the Comment Code once; creators can turn comments off.
- Hashtags: hashtags in the Pin description link to a feed of Pins with that tag (Pinterest newsroom, September 2017). Current importance and a recommended count: `unverified`. Pinterest's present guidance is to add up to 10 "related topics" tags when creating a Pin and use keywords in title, description, board titles and board descriptions.
- Links in Pins: the Pin's destination link is the clickable element. Links in descriptions: `unverified`. Redirect-heavy links and abused URL shorteners may be blocked.
- Titles are truncated in feeds: the first 40 characters (30 for double-byte languages including Arabic) per the ad specs page (it covers organic and paid image and video), so put the key words first.
- Emoji and Arabic: Arabic text is supported; RTL rendering inside Pin text overlays depends on the editing tool. Test the exported image.

## 4. Posting and cadence
- Official: "Aim to create original content weekly"; create "frequently and consistently". Scheduling: help.pinterest.com "Schedule Pins" says business accounts can schedule one Pin at a time, up to 10 Pins in the queue, up to 30 days ahead; the "Pin performance and distribution" page says two weeks. The two pages disagree; use 14 days as the safe window and confirm in the UI.
- After scheduling you can change publish date, title, board, description and link; you cannot change the image or video. After publishing you also cannot change image, video or audio, only descriptive fields; to change the creative you must publish a new Pin.
- Heuristic (practitioner observation, not an official rule): a steady 3-15 fresh Pins per week works better than bursts; freshness (new image or new video, not re-uploaded duplicates) matters more than volume. Pinterest warns that repeatedly saving the same Pins or uploading content that already exists may be flagged as spam and temporarily block Pin creation.
- Timing: no official best time. Pins are discovered via search over weeks and seasons, so publish 30-45 days before a season or holiday (practitioner heuristic). Use Pinterest Trends to pick topics.
- Funnel:
  - Awareness: keyword-rich image/video Pins for broad topics, trend-led Pins.
  - Consideration: how-to, comparison, checklists, rich article Pins linking to guides.
  - Conversion: product Pins and product tags, catalog Pins, landing pages that match the Pin.
  - Retention: boards by theme, follow CTA, fresh variants of the best Pins.

## 5. Distribution and ranking signals
Official (help.pinterest.com "Pin performance and distribution"):
- Distribution relies on how people search, save and engage; engagement is affected by language, location, season, holidays, formats and trends.
- Troubleshooting levers: let Pinterestbot reach your site, no broken links, descriptions and image text match the landing page, landing pages that add related content, a domain that loads in under 4 seconds, a safe spam-free domain, claimed website, original Pins, regular creation, no duplicates.
- Quality: strong lighting, framing, high resolution, vertical format, text on image; call-to-action to save and follow; answering comments.
- Language: Pins are distributed by language and location; match the Pin language to the target audience.
- Merchants: correct catalog metadata, in-stock info and Google product category influence distribution; Verified Merchant Program lets Pins appear on shopping surfaces.
Practitioner observation, not an official rule:
- Saves and outbound clicks are widely treated as the strongest signals.
- Fresh Pins to the same URL with new images outperform re-saving old Pins; fewer, better boards with keyword names help.

Claimed website and Rich Pins (help.pinterest.com "Claim your website", "Create rich Pins"):
- Claiming requires owning the domain, subdomain or subpath and being able to edit its code; you cannot claim most marketplace stores (Etsy, eBay, Amazon). A website can be claimed by only one Pinterest account. Methods: Google Merchant Center (some accounts), HTML tag, HTML file or DNS TXT record.
- Claiming gives analytics on Pins from your site, shows your profile photo and follow option on Pins saved from your site, and unlocks logo features.
- Rich Pins sync data from page meta tags: article (headline, description, author), recipe (title, servings, cook time, ratings, ingredients; Schema.org or h-recipe markup), product (price, availability; only if merchant guidelines are met and the item is in stock). Sync can take up to 24 hours. Opt a page out with `<meta name="pinterest-rich-pin" content="false" />`. A manual edit to a rich Pin overwrites the synced metadata.

## 6. Community rules and policy hot spots
Source: policy.pinterest.com Community Guidelines (page says updated guidelines take effect 12 November 2026, so re-read them after that date), Spam section, Account deactivation help.
- Spam and automation: "Don't use automation that hasn't been explicitly approved by Pinterest", including unauthorized services that perform actions on your behalf. Do not create accounts en masse, post repetitive, deceptive or irrelevant content to make money, link to unsafe or unoriginal sites, buy or sell engagement, stuff irrelevant keywords, redirect existing Pins to new destinations, or evade anti-spam systems. Buying followers or engagement is spam.
- Rate-limit blocks: repeating the same action many times in a short period (fast commenting, many follows, saving many Pins from one website) can trigger a temporary block; most are lifted within 24 hours.
- Engagement bait: pay-for-saves is forbidden (Paid Partnership guidelines). Contest guidance in section 7.
- Copyright and music: Do not infringe IP; use the content claiming portal for content uploaded by others. Pinterest has a copyright policy and repeat-infringer enforcement (details `unverified`).
- Impersonation: accounts impersonating or misrepresenting affiliation are deactivated; fan, parody or commentary accounts are allowed only if clearly not official.
- Health, finance, politics: medically unsupported health claims that risk public health, public-health-emergency misinformation, civic and climate misinformation, and exploitative financial practices (get-rich-quick, online gambling and lotteries) are prohibited.
- Regulated goods: restrictions on alcohol and supplement sellers without authorization, tobacco, marijuana, weapons, prescription drugs.
- Minors: zero tolerance for sexualization of minors, minors in underwear, grooming; accounts that save otherwise benign content in ways suggesting sexualization are deactivated.
- Account security: do not share your password, let others access the account, or buy/sell account access.
- Deactivation: single or repeat violations in safety, security (impersonation), spam and IP can lead to deactivation; appeal via Help Center; copyright appeals follow the copyright policy.
- Synthetic content: community guidelines apply to AI-generated content; Pinterest shows an AI label on image Pin close-ups when the owner marks content as AI-modified or when detection flags it. The Pin creation form has an "AI-Modified" toggle; API has `ai_disclosures`.

## 7. Branded content, ads disclosure and legal
Not legal advice.
- Paid partnerships: any sponsored or branded content for an exchange of value must disclose. Use the paid partnership label tool or a clear marker such as #ad. Follow advertising guidelines, post relevant content to relevant boards, and do not pay people per save or follow.
- EEA: commercial content must carry a clear disclosure using functionality Pinterest provides (a hashtag or label) and must not be deceptive or target minors' inexperience (commercial and branded content guidelines).
- Affiliate: keep one authentic account, original content, be transparent about links, do not use fake accounts or quid-pro-quo saves, avoid repetitive large-volume affiliate Pins; some URL shorteners are blocked.
- Contests: do not require saving a specific image, allow only one entry per person, do not imply Pinterest sponsorship, follow local law.
- Commercial content cannot promote tobacco, marijuana, firearms or prescription-only treatments, or encourage excessive alcohol use.
- Consumer law at a high level: EU rules on identifiable advertising, US FTC endorsement guidance, Egypt Consumer Protection Law 181 of 2018 on misleading advertising (details `unverified`; get legal advice for contests, lotteries and health claims).

## 8. API and automation
- Official API: Pinterest API v5 (developers.pinterest.com). OAuth 2.0 (and client credentials for some flows). Scopes for publishing: boards:read, boards:write, pins:read, pins:write.
- Can: create, read, update, delete boards, board sections and Pins (`POST /v5/pins`), save a Pin to a board, upload video via `/v5/media` then create a Pin with a cover image, product tags, user and Pin analytics, top Pins, trends, verify and list websites, catalogs, ads endpoints, search Pins or boards (limited), AI disclosure on Pins.
- Pin create body: title up to 100, description up to 800, alt text up to 500, link up to 2048; media sources: image URL, image base64, video_id, multiple image URLs (2-5) or base64, pin_url (beta). Video Pins may report an incorrect `creative_type` for a few seconds while processing.
- No endpoint found in the v5 OpenAPI file for: comment reading or replying, DMs or messages, scheduled publish time (Create Pin has no schedule field). Treat these as having NO API. Use native scheduling or a partner tool that complies with developer guidelines.
- Access tiers (developers.pinterest.com "access tiers"): Trial is default; Pins and boards created with Trial access are visible only to their creator as Sandbox entities. Standard access requires a demo video showing the OAuth flow, privacy policy and use case, then review. Apps registered on or after 14 September 2026 may get HTTP 403 `PINNER_DATA_ACCESS_DENIED` for non-business users without Pinterest's authorization.
- Rate limits (developers.pinterest.com "rate limits", subject to change): Trial 1,000 requests per day for all requests, with `org_write` (Pins, boards) 300 per day; Standard up to 100 requests per second per user per app overall, with `org_write` 100 per minute, `org_read` 1,000 per minute, `org_analytics` 60 per minute, `trends_read` 60 per minute.
- Developer guidelines forbid: acting for users without their knowledge, features that auto-initiate actions without each action being chosen (a scheduler must let the end user choose each Pin), scraping, storing API-accessed data except campaign analytics, using API data to train AI models, requiring or incentivizing saves, testing rate limits. Credentials must never be solicited (OAuth only).
- Native scheduling: business accounts only, one at a time, up to 10 queued, 30 days ahead (section 4). Bulk upload for video Pins and catalogs exist (`unverified` specifics).
- n8n guidance: use OAuth credentials, log HTTP 429 and back off, keep a human-approved queue, never loop over many Pins from the same domain quickly, avoid duplicate-image uploads.

## 9. Analytics
Where: business account > Analytics (Overview, Conversion insights, Audience insights) and per-Pin "Pin stats". Real-time overview metrics are estimates and may decrease (help.pinterest.com "Pinterest Analytics").
- Impressions: times your Pins or ads were on screen.
- Saves: times people saved your Pin to a board.
- Pin clicks: total taps on a Pin or ad that lead to a destination on or off Pinterest.
- Outbound clicks: total clicks to the destination URL.
- Profile visits and follows: visits and followers gained after viewing a Pin.
- Video views: 2 s continuous playback while 50% in view; 10-second plays; played at 95%; average and total play time.
- Product tag impressions, clicks, saves, outbound clicks.
- Analytics shows published Pins by default; check "Include saved Pins" to add saved ones. Claim your website to see analytics for Pins others create from your site.
- Which metric answers which question: Is content discoverable? Impressions. Is it useful enough to keep? Saves. Does it drive traffic? Outbound clicks per impression. Is the video hook working? 10-second plays / video views, play time. Does it sell? Conversion insights and product-tag clicks.

## 10. Cases
**Situation:** Impressions fall week over week.
**Do:** Check Include saved Pins filter and date range first; confirm Pinterestbot can fetch your site and links are not broken; check landing page speed (under 4 s per Pinterest guidance); publish fresh Pins with new creative; review whether Pins are in the right language for the audience.
**Avoid:** Re-uploading identical images (spam flag and temporary block on Pin creation) and mass-deleting old Pins that still earn saves.

**Situation:** Account flagged, Pin creation blocked, or deactivated.
**Do:** For a temporary rate-limit block wait; most clear within 24 hours. For deactivation, read the notice category (spam, security, IP, safety), remove the offending content and appeal through the Help Center once with facts.
**Avoid:** Opening a new account to bypass enforcement (prohibited and treated as spam), buying a "recovery" service.

**Situation:** Copyright claim or someone uploaded your content.
**Do:** If your content was uploaded by others, use the Content Claiming Portal; if you are the one claimed against, remove the Pin, check you own the image and any music, and file a counter-notice only with proof.
**Avoid:** Re-saving the same copyrighted image from another source, or using stock images beyond their licence.

**Situation:** Negative comment wave on a Pin.
**Do:** Reply once helpfully, report harassment, remove spam comments, or turn comments off for that Pin; fix the underlying problem if it is a link or product issue.
**Avoid:** Mass deleting valid complaints or commenting repetitively from the brand account (rate-limit risk).

**Situation:** Impersonator account using your brand.
**Do:** Report through the impersonation form with proof of identity; make sure your own account is business-verified and your website is claimed so the real profile is attached to saved content.
**Avoid:** Replying from brand accounts to the impostor or sharing the link widely.

**Situation:** Planning a giveaway.
**Do:** Follow Contest Guidelines: do not require people to save a specific image, allow one entry per person, do not imply Pinterest sponsorship, state rules and local law; allow entries based on a board of the entrant's own choosing.
**Avoid:** "Save this Pin to enter" or paying people per save or follow.

**Situation:** Cross-posting from Instagram Reels or TikTok.
**Do:** Re-export without watermarks in 9:16, 4 s or longer, add a keyword title, description and destination link, pick a cover image, choose the board, mark AI-modified content.
**Avoid:** Posting the same video to many boards as separate uploads, and leaving the Pin without a link.

**Situation:** A published Pin has a wrong image or must be corrected.
**Do:** Edit title, description, link or board; for wrong creative publish a new Pin and delete the old one if it is misleading (deleted Pins cannot be recovered; check saves first).
**Avoid:** Trying to replace media on an existing Pin (not possible).

**Situation:** Crisis (product safety or scandal).
**Do:** Pause the scheduled queue, remove affected Pins or point links to a statement page, update product Pins and catalog availability, use comments-off for sensitive Pins.
**Avoid:** Continuing to promote the affected product via ads or scheduled Pins.

**Situation:** Giving an agency or tool access to the account.
**Do:** Use Business Manager roles and OAuth with minimum scopes; keep the tool on Pinterest's approved partner list when possible; revoke tokens at exit.
**Avoid:** Sharing the password (forbidden by Pinterest) or using cookie-based or credential-collecting tools.

## 11. Arabic and Egypt notes
- Arabic is in Pinterest's supported language list on policy pages; whether Arabic Pin search is as mature as English is `unverified`.
- Titles in double-byte languages including Arabic show about 30 characters in feeds against 40 for Latin text (ad specs page): lead with the keyword.
- Pins are distributed by language and location; write the Pin in the audience's language and avoid mixing scripts in the title.
- Text on image in Arabic: export from a design tool and check letter joining and RTL order; alt text can also be written in Arabic (500 chars).
- Dialect keyword research: Pinterest search favors the words people type; Egyptian-colloquial versus Modern Standard Arabic keyword performance is `unverified`; test both in titles and descriptions.
- Hashtag habits in Arabic: `unverified`.
- Verification and payment: Egypt is not among the regions where the Community Guidelines page says business accounts are unavailable (Crimea, Cuba, Donetsk, Iran, Luhansk, North Korea, Syria); that is not a statement that every feature is available in Egypt. Egyptian payment methods for ads and Verified Merchant Program availability in Egypt: `unverified`.
- Claim your site: needs access to HTML, DNS or Google Merchant Center; local web agencies must give you the code access.

## 12. Pre-publish checklist
1. Is the image 2:3 (1000x1500) or the video 9:16, at least 4 s, within 5 min?
2. Is the file within limits (20 MB for web image upload, supported format)?
3. Is the title 100 chars or fewer with the keyword in the first 40 chars?
4. Is the description 800 chars or fewer, keyword-led, written in the target language?
5. Is alt text (500 chars or fewer) filled in?
6. Does the link work, load in under 4 s, match the Pin, and avoid redirects or abused shorteners?
7. Is it a fresh creative, not a duplicate of an existing Pin?
8. Is it saved to the right, keyword-named board (and section)?
9. Is a paid partnership label or #ad applied when sponsored or affiliate?
10. Is AI-modified content toggled correctly?
11. Are text overlays inside the safe zone (top 270, left 65, right 195, bottom 790 px)?
12. Is the destination domain claimed and, for articles, recipes or products, do rich meta tags validate?

## 13. Sources
- https://help.pinterest.com/en/article/review-pin-specs
- https://help.pinterest.com/en/business/article/pinterest-product-specs
- https://help.pinterest.com/en/business/article/pin-performance-and-distribution
- https://help.pinterest.com/en/business/article/schedule-pins
- https://help.pinterest.com/en/article/create-a-pin-from-an-image-or-video
- https://help.pinterest.com/en/article/create-idea-pins
- https://help.pinterest.com/en/article/types-of-pins-on-pinterest
- https://help.pinterest.com/en/business/article/pin-stats
- https://help.pinterest.com/en/business/article/pinterest-analytics
- https://help.pinterest.com/en/business/article/rich-pins
- https://help.pinterest.com/en/business/article/claim-your-website
- https://help.pinterest.com/en/article/comment-on-a-pin
- https://help.pinterest.com/en/article/edit-your-profile
- https://help.pinterest.com/en-gb/node/2461
- https://help.pinterest.com/en/article/edit-or-delete-a-pin
- https://help.pinterest.com/en/article/account-suspension
- https://help.pinterest.com/en/article/rate-limit-blocks
- https://help.pinterest.com/en/article/ai-at-pinterest
- https://policy.pinterest.com/en/community-guidelines
- https://policy.pinterest.com/en/commercial-and-branded-content-guidelines
- https://policy.pinterest.com/en/developer-guidelines
- https://developers.pinterest.com/docs/key-concepts/access-tiers/
- https://developers.pinterest.com/docs/reference/rate-limits.md
- https://developers.pinterest.com/docs/api/v5/pins-create/
- https://developers.pinterest.com/docs/api-features/creating-boards-and-pins/
- https://raw.githubusercontent.com/pinterest/api-description/main/v5/openapi.yaml
- https://newsroom.pinterest.com/en-gb/post/now-hashtags-work-on-pinterest
- https://datareportal.com/essential-pinterest-stats (ad reach, January 2025)
