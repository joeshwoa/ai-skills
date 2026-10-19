# Telegram — rules and playbook
Last verified: 2026-10-19

Scope: organic use of channels, groups, bots, the Bot API and Stories. Telegram Ads is only touched where it affects organic rules. Figures that Telegram changes often carry a source URL. Items I could not confirm are marked `unverified`.

## 1. Snapshot
- What it is: a messaging app with three publishing surfaces. A **channel** is one-to-many broadcast with no subscriber cap. A **supergroup** is a group chat with up to 200,000 members. A **bot** is an automated account driven by the Bot API. Source: https://core.telegram.org/api/channel
- Best for: owned-audience broadcasting (news, offers, drops, courses), community chat, support and ordering through bots, and delivering files up to 2 GB (4 GB with Premium) to subscribers. Source: https://telegram.org/faq
- What it is not: a discovery feed. A public channel is found by search, t.me links, forwards and recommendations, so growth depends on cross-promotion from other platforms. (practitioner observation, not an official rule)
- Egypt / Arab world: the DataReportal Digital 2026 Egypt page does not list Telegram, so I have **no sourced Telegram user count for Egypt** (`unverified`). It does give ad-reach for Facebook 51.6M, YouTube 49.3M, TikTok 48.8M (18+), Instagram 21.7M, which shows where the mass audience is. Source: https://datareportal.com/reports/digital-2026-egypt
- Latest Bot API at verification time: **Bot API 10.3, released 2026-08-24**. Source: https://core.telegram.org/bots/api

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Text post (channel/group/bot) | n/a | 1 to 4096 chars after entity parsing (Bot API) | n/a | Source: https://docs.aiogram.dev/en/latest/api/methods/send_message.html (mirrors Bot API) |
| Photo | Width + height at most 10,000 px; width/height ratio at most 20 | n/a | Bot API: 10 MB | Telegram recompresses photos; send as document to keep the original. Limits: https://docs.aiogram.dev/en/latest/api/methods/send_photo.html |
| Album (media group) | per item | 2 to 10 items | per item type limits | Documents and audio can only be grouped with the same type. Source: https://docs.aiogram.dev/en/latest/api/methods/send_media_group.html |
| Video / file / document | no fixed ratio documented in pages read (`unverified` for recommended px) | no duration cap documented | Bot API upload 50 MB, download via getFile 20 MB; local Bot API server upload 2000 MB; user clients 2 GB (4 GB Premium) | Source: https://core.telegram.org/bots/faq and https://telegram.org/faq |
| Live Photo | n/a | n/a | n/a | New type in Bot API 10.0 (2026-05-08), sendable and editable, also as paid media. Source: https://core.telegram.org/bots/api-changelog |
| Poll / quiz | n/a | question 1 to 300 chars; 1 to 12 options (1 to 100 chars each); quiz explanation 0 to 200 chars; description 0 to 1024 chars; open_period 5 to 2,628,000 s | n/a | Min options lowered from 2 to 1 in Bot API 10.0. Source: https://docs.aiogram.dev/en/latest/api/methods/send_poll.html |
| Checklist | n/a | n/a | n/a | Introduced in Bot API 9.1 for business accounts. Source: https://core.telegram.org/bots/api-changelog |
| Story (channel) | vertical media, exact px `unverified` | active 24 h by default on the client; other durations `unverified` for client | n/a | Posted by an admin with Premium and the `post_stories` right; channel needs boosts. Sources: https://telegram.org/blog/channel-stories , https://core.telegram.org/constructor/chatAdminRights |
| Story (via Bot API) | photo or video content | active_period 21,600 / 43,200 / 86,400 / 172,800 s (6/12/24/48 h); caption 0 to 2048 chars | n/a | Only for a managed **business account**; needs the `can_manage_stories` right. Source: https://docs.aiogram.dev/en/latest/api/methods/post_story.html |
| Live stream / video chat | n/a | channel owners can stream to unlimited viewers; group calls up to 200 participants | n/a | Source: https://telegram.org/faq |
| Paid media | n/a | n/a | n/a | Priced in Stars; max price 25,000 Stars since Bot API 9.3. Source: https://core.telegram.org/bots/api-changelog |
| Channel direct messages / suggested posts | n/a | n/a | n/a | Bot API 9.2: bots can send into a channel's direct-messages chat, approve or decline suggested posts. Paid posts must not be deleted for 24 h. Source: https://core.telegram.org/bots/api-changelog |
| Scheduled post | n/a | at least 10 s in the future (shorter sends immediately) | n/a | Native client feature; see section 4 and 8. Source: https://core.telegram.org/api/scheduled-messages |

Native-client story and caption limits by tier (from the live config page, values change): caption 1024 free / 4096 Premium; story caption 200 free / 2048 Premium; stories sent per week 3 / 700; per month 10 / 3000; active stories 1 / 100. Source: https://core.telegram.org/api/config

## 3. Text limits
| Item | Limit | Source / status |
|---|---|---|
| Message text | 1 to 4096 chars after entities parsing (Bot API) | https://docs.aiogram.dev/en/latest/api/methods/send_message.html |
| Caption (Bot API photo/video/document) | 0 to 1024 chars after entities parsing | https://docs.aiogram.dev/en/latest/api/methods/send_photo.html |
| Caption (user client, Premium) | 1024 default, 4096 Premium | https://core.telegram.org/api/config |
| Story caption | 200 free / 2048 Premium (client); 2048 via Bot API postStory | config page and post_story page above |
| Channel/group title | no number stated in official pages read; commonly cited 128 | `unverified` |
| Channel/group description | no number stated in official pages read; commonly cited 255 | `unverified` |
| User bio | 70 default, 140 Premium | https://core.telegram.org/api/config |
| Bot username | 5 to 32 chars, Latin letters, digits, underscore, must end in "bot"; cannot be changed later | https://core.telegram.org/bots/features |
| Comment (group message) | same 4096 as any message | assumption from message limit, `unverified` as a comment-specific rule |
| Hashtags | no count limit documented; hashtags are text entities and searchable within Telegram | no cap found, `unverified` |
| Mentions | @username mentions notify the user; no mention cap documented | `unverified` |
| Links | Clickable in posts; links render as previews unless disabled; inline buttons (URL buttons) are also clickable | https://core.telegram.org/bots/features |
| Formatting | bold, italic, underline, strikethrough, spoiler, blockquote, expandable blockquote, code, pre, text_link, custom_emoji; entity offsets are in UTF-16 code units | https://core.telegram.org/bots/api |
| Custom emoji | in bot messages only if the bot owner has Premium (Bot API 9.4) | https://core.telegram.org/bots/api-changelog |
| Arabic / RTL | Telegram clients render RTL per paragraph; no official RTL rule found | `unverified` |

Entity length warning for agents: when you compute entity offsets for Arabic text or emoji, count UTF-16 code units, not Python characters. A wrong offset shifts or drops the bold/link.

## 4. Posting and cadence
Telegram publishes no official cadence guidance, so everything below is heuristic.
- Frequency (heuristic): news or deal channels 1 to 5 posts/day; brand or educational channels 3 to 7 posts/week. Every post can trigger a push notification, so volume is the main unsubscribe driver. Use silent sending for low-priority posts (client feature; Bot API `disable_notification`).
- Timing (heuristic): use the channel's own "top hours" graph in Statistics (see section 9) rather than any generic best-time claim. Source for the graph: https://core.telegram.org/api/stats
- Native scheduling: a scheduled message needs a timestamp at least 10 s ahead; each chat has its own queue; Premium users can make repeating scheduled messages (daily to yearly). Source: https://core.telegram.org/api/scheduled-messages . No maximum horizon or queue size is stated there (`unverified`).
- Edit and delete: owners and admins with rights can delete any message and it disappears for all subscribers. Source: https://telegram.org/faq_channels . Paid posts (suggested-post flow) must stay at least 24 h. Source: https://core.telegram.org/bots/api-changelog
- Funnel plan:
  - Awareness: forwardable posts (a short insight, a poll, a file or template). Cross-post teasers on Instagram/TikTok/YouTube pointing to the t.me link.
  - Consideration: albums, long posts with proof (case results, how-it-works), pinned "start here" post, polls and quizzes for feedback.
  - Conversion: pinned offer with a URL button, a bot for ordering/booking, paid media or Stars for digital goods.
  - Retention: weekly digest, comments via a linked discussion group, Q&A in the group, exclusive files.
- Reminder from the platform: new subscribers can see the entire channel history, so pinned and early posts must stay accurate. Source: https://telegram.org/faq_channels

## 5. Distribution and ranking signals
Official:
- There is no algorithmic feed for subscribed channels: subscribers see posts in order. Reach equals subscribers plus forwards. View counters include views of forwarded copies, are approximate, and Telegram forgets a view after about 4 days. Source: https://telegram.org/faq_channels
- Public channels with a username appear in Telegram search and via t.me links. Source: https://telegram.org/faq_channels
- Channels can be recommended as "similar channels" (client limit of recommended similar channels is 10 free / 100 Premium for a user's own view). Source: https://core.telegram.org/api/config . How Telegram chooses recommendations is not documented (`unverified`).
- Boosts: users give boosts to a channel; each boost level unlocks perks (extra daily stories, wallpapers, emoji status, autotranslation). Exact boost counts per level are in the live config, not on the doc page. Source: https://core.telegram.org/api/boost
- Premium gives each user 4 boosts to assign to channels. Source: https://telegram.org/blog/channel-stories

Practitioner observation, not an official rule:
- Growth comes mostly from other channels (shoutouts, folders, Telegram Ads), cross-platform links and forwards. Posts that are forwarded earn extra views.
- Pinning a post and using a clear first line improves the preview shown in forwards.

## 6. Community rules and policy hot spots
| Topic | What the rules say | Source |
|---|---|---|
| Spam and scams | Terms forbid using Telegram to send spam or scam users. Violations can lead to a temporary or permanent ban, and loss of Premium benefits without compensation. | https://telegram.org/tos |
| Spam limits on accounts | Reported accounts can only message saved contacts or reply to people who wrote first. A first limit usually lasts a few days; repeats last longer; early release is not possible. Appeal through @SpamBot. Unsolicited ads, invite links and links to strangers are the typical trigger. | https://telegram.org/faq_spam |
| Violence and illegal content | Promoting violence on publicly viewable channels and bots, and illegal pornography on public channels, are banned. | https://telegram.org/tos |
| Copyright | Telegram handles copyright complaints only for public content (not private chats or groups). Complaints go to dmca@telegram.org. | https://telegram.org/faq |
| Impersonation and fraud reports | Telegram points users to @NoToScam for scams; impersonators can be reported in-app. | https://telegram.org/faq |
| Scraping | Data scraping is prohibited under Telegram's Content Licensing and AI Scraping Terms. | https://telegram.org/tos |
| Minors | Users in the EU, UK and Australia must be 18 or older to sign up. | https://telegram.org/tos |
| Bots: spam | Bots must not harass or spam users with unsolicited messages; bypassing rate limits is banned. | https://telegram.org/tos/bot-developers |
| Bots: fake engagement | "Social growth manipulation" and impersonating Telegram or others is banned. | https://telegram.org/tos/bot-developers |
| Bots: user data | Collect only what is needed, get explicit revocable consent, delete on request, have a privacy policy (the Standard Policy applies if you give none). | https://telegram.org/tos/bot-developers |
| Bots: bans | A violation can ban the bot, the linked account and affiliated channels or communities. | https://telegram.org/tos/bot-developers |
| Giveaways | Telegram has a native channel giveaway tool: Premium subscriptions as prizes, winners drawn at random by Telegram, entry limited to new or all subscribers, optional required channels, optional country limits. Pre-paid. | https://telegram.org/blog/giveaways |
| Health, finance, political claims | Telegram's organic rules do not list category-specific bans beyond illegal content. Telegram **Ads** forbid political promotion, gambling, unverified medical or supplement claims and get-rich-quick schemes; do not mirror such content in ad-like posts. | https://ads.telegram.org/guidelines |
| Buying followers | Social growth manipulation is banned for bots; no organic-account equivalent was found in pages read, but treat purchased members as a ban risk. | bot terms above; the rest `unverified` |

## 7. Branded content, ads disclosure and legal
- Telegram has **no paid-partnership label** in the sources I read (`unverified`). Disclose sponsorship in the post text yourself ("#ad", "إعلان" or "برعاية").
- Telegram Ads (ads.telegram.org) shows sponsored messages with a "sponsored" marker; ad text is capped at 160 characters plus one button, and ads must not bypass the rules in section 6. Source: https://ads.telegram.org/guidelines . Organic channels only need to follow these rules if the creative is run as an ad.
- Channel owners can share 50% of Telegram Ads revenue earned in their bot's chat (bot feature); channel ad revenue sharing terms were not researched (`unverified`). Source: https://core.telegram.org/bots/features
- Consumer-law basics (not legal advice): in the EU, the US (FTC) and Egypt, undisclosed paid endorsements and misleading claims are risky; disclose material connections clearly in the post. Egyptian Consumer Protection Law No. 181 of 2018 requires accurate advertising information (named from general knowledge, `unverified` in this run).
- Bot privacy: keep a privacy policy; the Bot Developer Terms require consent and deletion on request. Source: https://telegram.org/tos/bot-developers

## 8. API and automation
- **Bot API** (HTTPS, token from @BotFather). Version 10.3 as of 2026-08-24. Source: https://core.telegram.org/bots/api
- Auth: bot token only (secret). Webhook secret_token header option, 1 to 256 chars `A-Z a-z 0-9 _ -`. No app review is needed to create a bot; featured Mini Apps and some business features have their own requirements.
- Receiving: `getUpdates` (limit 1 to 100, updates kept 24 h, unusable while a webhook is set) or `setWebhook` (ports 443, 80, 88, 8443; max_connections 1 to 100, default 40; HTTPS with valid certificate). Source: https://core.telegram.org/bots/api and https://core.telegram.org/bots/faq
- Can do: send text, media, albums, polls, checklists; edit and delete its own messages; moderate groups (ban, restrict, approve join requests) when admin; post to a channel where the bot is an admin with `post_messages`; reply in comment threads of the discussion group; send into channel direct-messages chats; approve/decline suggested posts; paid media; Stars payments. Sources: https://core.telegram.org/bots/features , https://core.telegram.org/bots/api-changelog
- Stories: only through a **managed business account** with `can_manage_stories` (postStory, active_period 6/12/24/48 h, caption up to 2048). There is **no Bot API method to post a story as a channel**; channel stories are posted manually by a Premium admin with the `post_stories` right. Sources: https://docs.aiogram.dev/en/latest/api/methods/post_story.html , https://telegram.org/blog/channel-stories
- Scheduling: native client scheduling exists (MTProto `schedule_date`). The Bot API pages I read show no scheduling parameter for sendMessage, only a note that a scheduled message has message_id 0 until sent; treat Bot API scheduling as unavailable and schedule in your own tool (n8n Cron or Wait node calling sendMessage) (`unverified` whether a newer parameter exists).
- Cannot: read a channel's full history or reactions analytics through the Bot API (`unverified` in this run), see messages from other bots, or use long polling and a webhook together. With privacy mode on, a group bot only sees commands addressed to it, replies, and a few other messages; admin bots or bots with privacy off see all messages except from other bots. Source: https://core.telegram.org/bots/faq
- Analytics: channel statistics are exposed through MTProto `stats.getBroadcastStats` (user-account API), not the Bot API pages I read (`unverified`). Source: https://core.telegram.org/api/stats
- Rate limits (documented, not guaranteed): about 1 message/s to one chat, 20 messages/minute in one group, about 30 messages/s across chats in bulk. Above that you get HTTP 429 with `retry_after`. Paid broadcasts allow up to 1000 msg/s at 0.1 Star per message beyond the free 30/s, and require at least 100,000 Stars balance and 100,000 monthly active users. File limits: 50 MB upload, 20 MB getFile download on the public API; local Bot API server: 2000 MB upload, no download limit. Source: https://core.telegram.org/bots/faq
- Forbidden automation: spam or harassing bots, circumventing limits, scraping public channel contents to build datasets or AI products, social growth manipulation, impersonation, phishing for OTP or passwords. Source: https://telegram.org/tos/bot-developers
- Automation pattern for n8n: Telegram node or HTTP Request to `https://api.telegram.org/bot<TOKEN>/sendMessage`. Store the token in credentials, never in the workflow JSON or a repo. Put a delay between sends (at least 1 s per chat, 40 ms between chats) and honour `retry_after`.
- Official scheduling options: client "Schedule message" (channels, groups, private chats), Premium repeating schedule. There is no official third-party scheduler.

## 9. Analytics
- Where: Channel info > Statistics in the app, once the channel meets a server-side size threshold (the exact number is a server config flag `can_view_stats`; not published). Source: https://core.telegram.org/api/stats
- Channel metrics: followers (vs previous period), average views per post, average shares per post, reactions per post, story views/shares/reactions, percentage of subscribers with notifications enabled. Graphs: growth, followers, mute, top hours, interactions, views by source, new followers by source, languages, reactions by emotion.
- Supergroup metrics: members, messages, viewers, posters; top posters, top admins, top inviters; growth and new members by source; top hours and weekdays.
- Which metric answers which question:
  - Is the content good? average views per post divided by subscribers, and shares per post.
  - Will people see announcements? share of subscribers with notifications enabled.
  - When to post? top-hours graph.
  - Where do followers come from? new followers by source (links, search, forwards, similar channels).
  - Is a post being re-shared? public forwards list for the message.
- Limit: view counters are approximate and a view can be counted again after about 4 days. Source: https://telegram.org/faq_channels

## 10. Cases
1. **Situation:** Views on recent posts drop sharply.
   **Do:** Check Statistics: did the share of subscribers with notifications enabled fall, did followers drop (mute and unsubscribe graphs), did posting frequency or time change? Compare views per post to the previous period, then test fewer posts, silent mode for low-value posts and a stronger first line.
   **Avoid:** Buying members or views to "fix" the number; views are approximate and purchases risk bans (section 6).
2. **Situation:** The account cannot message people or add them to groups ("limited").
   **Do:** Open @SpamBot to see the limit and appeal if wrong. Stop cold outreach, remove invite links from private messages, wait out the limit (a few days on a first offense).
   **Avoid:** Creating new accounts to continue the same outreach; repeated offenses lengthen the limit and can become permanent.
3. **Situation:** A copyright or illegal-content complaint on a public channel.
   **Do:** Remove or replace the post, keep the original licence or permission, and answer through the contact in Telegram's notice. Rights holders contact dmca@telegram.org; appeals for banned channels or bots go to abuse@telegram.org. Source: https://telegram.org/faq
   **Avoid:** Re-posting the same file under a new channel after a ban.
4. **Situation:** A wave of insults or raids in the discussion group.
   **Do:** Turn on join-to-send, set slow mode, restrict new members, ban offenders with an admin or moderation bot, keep a pinned rules post, and report scam accounts. Admins need `ban_users` and `delete_messages` rights. Source: https://core.telegram.org/api/discussion , https://core.telegram.org/constructor/chatAdminRights
   **Avoid:** Auto-banning by keyword alone without a review list; Arabic dialect words cause false positives.
5. **Situation:** A fake channel or bot copies the brand name.
   **Do:** Collect usernames and screenshots, report the account or channel in-app, post a pinned notice with the real t.me link, and add the official link to every bot welcome message. Telegram lists @NoToScam for scam reporting. Source: https://telegram.org/faq
   **Avoid:** Replying to the impersonator's DMs or sending money or OTPs.
6. **Situation:** Running a subscriber giveaway.
   **Do:** Use the native channel giveaway (Telegram draws winners at random and sends gift-code links), state the end date, countries and required channels in the post, and pay for the prizes up front. Source: https://telegram.org/blog/giveaways
   **Avoid:** Picking winners by hand, requiring users to add contacts, or sending unsolicited DMs to entrants.
7. **Situation:** Cross-posting from Instagram, TikTok or YouTube.
   **Do:** Re-write the caption for Telegram (4096-char text, link as clickable text), upload the file natively (up to 50 MB through a bot) or link to the video, and remove other platforms' watermarks if they would look like ads for a competitor.
   **Avoid:** Pasting the same hashtag block; Telegram hashtags are only in-app search tags.
8. **Situation:** A post contains a wrong price or false claim.
   **Do:** Edit the post (add "تحديث" / "Updated" in the text), and delete only if it is harmful or illegal; deletion removes it for all subscribers. If the post was a paid post in the suggested-post flow it must stay for 24 h. Sources: https://telegram.org/faq_channels , https://core.telegram.org/bots/api-changelog
   **Avoid:** Silent edits that change commitments (price, dates) without notice.
9. **Situation:** A crisis (leaked data, harmful reply by the bot).
   **Do:** Pause the n8n workflow, revoke the bot token in @BotFather (this changes it), delete bad messages, post one factual update in the channel, and review the bot's privacy policy duties (deletion on request). Source: https://telegram.org/tos/bot-developers
   **Avoid:** Leaving the old token in workflows, logs or repos.
10. **Situation:** Handing over channel access to an agency.
    **Do:** Add them as admins with minimal rights (for example `post_messages`, `edit_messages`; no `add_admins`), never share the owner's phone login code or 2-step password, and remove the admin at the end. Rights list: https://core.telegram.org/constructor/chatAdminRights
    **Avoid:** Transferring ownership as a "trial".
11. **Situation:** Telegram bot floods users with 429 errors during a broadcast.
    **Do:** Send at most about 30 messages/s overall and 1/s per chat, honour `retry_after`, queue and spread the broadcast (the FAQ suggests 8 to 12 hours for very large lists), and consider paid broadcasts only if you meet the Stars and MAU thresholds. Source: https://core.telegram.org/bots/faq
    **Avoid:** Retrying instantly in a loop; it extends the flood wait.

## 11. Arabic and Egypt notes
- Telegram clients render RTL per paragraph and support Arabic in names, titles and messages. No official RTL spec was found, so put one language per paragraph and test the preview (`unverified`).
- Entity offsets use UTF-16 code units; Arabic letters are 1 unit, but emoji with joiners and surrogate pairs count more. Source: https://core.telegram.org/bots/api
- Channel usernames and bot usernames allow only Latin letters, digits and underscore (bot username rule), so Arabic brand names need a Latin handle. Source: https://core.telegram.org/bots/features
- Payments: Digital goods in bots must use Telegram Stars (XTR). Local card payment support in Egypt via Bot payments was not verified (`unverified`).
- Hashtag habits: Arabic hashtags work as in-app search text; no official count rule found.
- Verification and bans: Telegram has no public Egypt-specific posting rule in the sources read; follow section 6 and local law.
- Age: the 18+ signup rule applies to the EU, UK and Australia only; other regions are not stated in the page. Source: https://telegram.org/tos

## 12. Pre-publish checklist
1. Is the text 4096 characters or fewer (or the caption 1024 or fewer for a bot post)?
2. Are entity offsets computed in UTF-16 units and formatting tested on a preview?
3. Is every file under the limit for the sending method (bot upload 50 MB; photo 10 MB; album 2 to 10 items)?
4. Is the post in the right chat (channel vs discussion group) and sent silently if low priority?
5. Does it avoid unsolicited private outreach, mass invite links and scam wording?
6. Are sponsorship, affiliate or gift relationships disclosed in the text?
7. Are price, date and claim figures verified, with no health, finance or political promises?
8. Is third-party media licensed (no copyright risk on a public channel)?
9. Are links valid, not shorteners that hide the destination, and does the URL button work?
10. Is the posting rate within bot limits (1/s per chat, about 30/s bulk, 20/min per group)?
11. Is the bot token kept in credentials, not in the post, logs or workflow export?
12. Is there a rollback plan (who can edit or delete, and that deletion hits all subscribers)?

## 13. Sources
- https://core.telegram.org/bots/api
- https://core.telegram.org/bots/api-changelog
- https://core.telegram.org/bots/faq
- https://core.telegram.org/bots/features
- https://core.telegram.org/api/channel
- https://core.telegram.org/api/config
- https://core.telegram.org/api/boost
- https://core.telegram.org/api/stats
- https://core.telegram.org/api/discussion
- https://core.telegram.org/api/scheduled-messages
- https://core.telegram.org/constructor/chatAdminRights
- https://core.telegram.org/method/channels.createChannel
- https://telegram.org/faq
- https://telegram.org/faq_channels
- https://telegram.org/faq_spam
- https://telegram.org/tos
- https://telegram.org/tos/bot-developers
- https://telegram.org/blog/channel-stories
- https://telegram.org/blog/giveaways
- https://ads.telegram.org/guidelines
- https://docs.aiogram.dev/en/latest/api/methods/send_message.html (mirror of Bot API method docs)
- https://docs.aiogram.dev/en/latest/api/methods/send_photo.html
- https://docs.aiogram.dev/en/latest/api/methods/send_media_group.html
- https://docs.aiogram.dev/en/latest/api/methods/send_poll.html
- https://docs.aiogram.dev/en/latest/api/methods/post_story.html
- https://datareportal.com/reports/digital-2026-egypt
