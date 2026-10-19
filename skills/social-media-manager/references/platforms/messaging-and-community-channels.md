# Messaging and community channels — rules and playbook
Last verified: 2026-10-19

Scope: Discord (servers, bots, community rules) and the private-messaging channels a community manager hands conversations between: Facebook Messenger, Instagram DMs, WhatsApp (Business Platform), Telegram (bots, channels, groups). Cross-platform handoff patterns are in sections 4 and 10. `unverified` means no official page confirmed it on 2026-10-19. Meta pages are tagged by URL in section 13.

## 1. Snapshot
- Discord: community chat organized in servers with channels and roles; strong for product communities, creators, learning groups and support. Bots are first-class. Each account must belong to a human; no self-bots.
- Messenger and Instagram DM: conversational inboxes tied to a Facebook Page or Instagram professional account. Business messaging is time-windowed (24 hours after the user's last action, with longer windows only in defined cases).
- WhatsApp Business Platform: the template-and-window model. Business-initiated conversations need approved templates and opt-in; free-form replies only inside the 24-hour customer service window.
- Telegram: bots, channels (broadcast, unlimited subscribers) and groups (up to 200,000 members per Telegram FAQ). A bot cannot start a conversation; the user starts it.
- Egypt / Arab world: the claim that WhatsApp and Messenger dominate Egyptian customer service is widespread but `unverified` here (no official statistic read). Telegram's own pages list Arabic among its languages.
- Rule of thumb: public channel for community and visibility, DM for personal help, WhatsApp for transactional follow-up with opt-in, human for anything sensitive.

## 2. Content formats and specs
Limits for messages, not for posts.

| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Discord message | n/a | content up to 2000 characters | n/a | Up to 10 embeds per message; total 6000 characters across embed title, description, field name/value, footer, author (docs.discord.com) |
| Discord attachment / media | `unverified` | `unverified` | upload size limit `unverified` (varies by server boost and plan) | Not confirmed on pages read |
| Messenger text | n/a | limit not stated on page read (`unverified`) | up to 30 images in one `attachments` array | Keep short; send several messages rather than one long one (Meta advice) |
| Instagram DM text | n/a | up to 1,000 bytes UTF-8 per message (about 500 Arabic characters, since Arabic letters take 2 bytes) | images png/jpeg 8 MB (up to 10 images per message); audio aac/m4a/wav/mp4 25 MB; video mp4/ogg/avi/mov/webm 25 MB; pdf 25 MB | Also supports heart sticker, reactions, shared posts (`MEDIA_SHARE`), replies to a message |
| WhatsApp text message | n/a | body up to 4096 characters | media size limits `unverified` (separate Supported Media Types page not read) | Interactive body 1024, footer 60, header text 60; reply buttons up to 3 with 20-char titles; list up to 10 rows, row title 24, description 72 |
| WhatsApp template | per category | header text parameter 60; body 1024 characters if other components present (32,768 if body only) | document headers must be PDF | Up to 10 buttons; approval by WhatsApp; categories marketing, utility, authentication |
| WhatsApp sticker | 512x512 px | n/a | static up to 100 KB; animated up to 500 KB | |
| Telegram text | n/a | 1-4096 characters after entity parsing | n/a | Bot API 10.3 (24 Aug 2026) |
| Telegram media caption | n/a | 0-1024 characters | bots can send files up to 50 MB; getFile downloads up to 20 MB | |
| Telegram channel post / live | n/a | n/a | n/a | Channels have unlimited subscribers; channel owners can host live streams with unlimited viewers (Telegram FAQ) |
| Channel/broadcast on WhatsApp (Channels) and broadcast lists | n/a | `unverified` | `unverified` | Official FAQ pages could not be fetched; do not hard-code limits |

## 3. Text limits
- Discord: message 2000 characters; embeds as above. Username, nickname, channel name, topic limits: `unverified`.
- Messenger: no stated limit on page read. Hashtags: not applicable in DMs. Links are allowed; promotional content is allowed only inside the window (section 5).
- Instagram DM: 1,000 bytes (not characters). Plan Arabic replies at about 500 characters, emoji count 4 bytes each. Links must be validly formatted URLs.
- WhatsApp: 4096 characters in a text body; button and list titles are short (20 to 24 characters). The limit is stated in characters; how emoji and Arabic are counted: `unverified`.
- Telegram: 4096 characters per message, 1024 per caption; channel description limits `unverified`.
- Arabic and RTL: all five channels render Arabic RTL natively in clients; mixed Arabic and Latin can reorder punctuation and numbers, so put URLs and order numbers on their own line.
- Emoji: use sparingly in templates; WhatsApp flow CTA text cannot contain emoji.

## 4. Posting and cadence
- Community cadence (heuristic, practitioner observation, not an official rule): Discord needs a visible rhythm (weekly event, daily prompt, weekly recap); Telegram channels typically 1 to 3 posts a day; avoid daily mass broadcast on WhatsApp.
- Timing: no official best time on any of these; respect local quiet hours (Cairo) for outbound templates.
- Funnel use:
  - Awareness: public posts and ads that open conversations (Click-to-Messenger, Click-to-Instagram Direct, Click-to-WhatsApp), Telegram channel, Discord server invite.
  - Consideration: answer product questions in DMs, FAQ pinned channel, replies to comments.
  - Conversion: order confirmation, appointment reminders (utility templates), payment links (do not collect card numbers in chat).
  - Retention: Discord community, Telegram channel updates, WhatsApp utility messages, support follow-up.
- Handoff patterns (cross-platform):
  1. Public comment to DM: Facebook and Instagram "private replies" allow one message to a commenter within 7 days of the comment (Instagram Live: only while the broadcast runs). Further messages need the user to reply, which opens the 24-hour window.
  2. DM to WhatsApp: only with explicit opt-in. Offer a click-to-chat link or QR and let the user start the WhatsApp conversation; this creates the service window. Do not message a number you scraped.
  3. Bot to human: Messenger Handover Protocol: primary receiver (bot) passes thread control to a secondary receiver (agent app) or to the Page inbox; only the primary can take control back; other apps receive `standby` events. Tag every conversation with owner, status and language in your CRM.
  4. Community to private: Discord bots must not DM people unsolicited; invite members to open a ticket channel or `/support` command instead.
  5. Telegram: put a "Start" deep link (t.me/bot?start=...) in posts so the user initiates.
  6. Handoff packet (what an agent sees): channel, user id, language, last 5 messages, intent tag, order or ticket id, consent status (opt-in source and time), SLA clock.
- Response-time heuristics: Messenger automated bots must respond to any input within 30 seconds (official); human first reply target 1 hour in business hours (heuristic); WhatsApp inside the 24-hour window.

## 5. Distribution and ranking signals
Official:
- Messenger and Instagram: standard window 24 hours for most user actions; up to 7 days from the first message after a Click-to-Messenger or Click-to-Instagram Direct ad; the Human Agent tag adds a separate 7-day window for manual human replies. Promotional content is allowed inside the window, outside it requires a permitted path such as a message tag use case or Sponsored Messages. One-Time Notification (beta) lets a Page send one message after a user requests it; token expires within 1 year; not available for Instagram.
- WhatsApp: quality rating is based on the past 7 days of messages, weighted by recency, from blocks, reports, mutes, archives and block reasons. Messaging limit applies to unique users messaged outside a service window in a moving 24 hours, per business portfolio. New portfolios start at 250; the first scale-up target is 2,000; after that the limit rises one level when quality is high and at least half the current limit was used in the last 7 days (effective within 6 hours).
- Discord: no ranking; server discovery requires Community enabled and more than 1,000 members, or Partnered/Verified status (support.discord.com).
- Telegram: no ranking guidance found. Channel search penalties exist for scams (section 6).
Practitioner observation, not an official rule: faster replies and fewer blocks protect WhatsApp quality; Discord communities grow through onboarding, roles and events, not through bot spam.

## 6. Community rules and policy hot spots
Sources: Discord Community Guidelines and Developer Policy; Meta Messenger and WhatsApp policies; Telegram Terms.
- Spam and unsolicited messages:
  - Discord: no unsolicited bulk messages; bots must not contact users without explicit permission or send frequent unsolicited DMs; no ads unrelated to the app; do not contact users off-platform using API data.
  - WhatsApp: contact only people who gave you their number and opted in; honor opt-outs everywhere (including removing them from your contacts); do not "spam, or surprise people".
  - Telegram: forbids using the service to send spam or scam users.
- Fake engagement and buying followers: Discord prohibits artificially inflating server membership and fake engagement, and bots must not send automated messages just to keep a server looking active. Telegram can remove subscribers acquired through misleading giveaways and label scam channels.
- Automation and bots:
  - Discord: no self-bots or user-bots; each account is a human. Apps must not circumvent API limits, must not ask for passwords or tokens, must not use message content to train AI models without permission.
  - Messenger: automated bots must answer every input within 30 seconds; if non-compliant, 7 days to fix before sending may be limited; disclose automation where required by law (California and Germany named).
  - WhatsApp: automation is allowed inside the window but must offer prompt escalation (human agent, phone, email, web, store). AI-provider clause: providers whose primary offering is AI technology are prohibited from using the WhatsApp Business Solution (terms last modified 6 March 2026); a customer-support bot as an incidental feature is not named either way, so ask Meta. Do not use business data to train AI models.
  - Telegram: bots cannot message users first; bots do not see other bots' messages; data scraping is prohibited by Telegram's content licensing and AI scraping terms.
- Impersonation: banned on Discord (fake profiles, impersonating groups or organizations), WhatsApp (misrepresenting affiliation) and Telegram bot terms.
- Copyright and music: no channel-specific rule read; general IP rules apply (`unverified`). Do not rehost copyrighted media in bot messages.
- Health, finance, politics: Discord prohibits harmful misinformation and financial scams; WhatsApp restricts firearms, alcohol, tobacco, drugs, medical and healthcare products, adult products, dating, multi-level marketing, payday loans and debt collection, and allows regulated verticals only in listed countries.
- Minors: Discord prohibits any sexualization of minors and removes dating spaces for teens; apps must not target under 13. WhatsApp regulated verticals not to under 18.
- Giveaways: Telegram punishes misleading giveaways (refunded-through-third-party scheme). Discord: engagement manipulation rules apply. Meta/WhatsApp: opt-in is required before any prize messages. Local contest law applies.
- Privacy: WhatsApp forbids sharing one customer's chat with another and requesting full payment card numbers or financial account numbers.
- Enforcement: WhatsApp can limit or remove access for negative feedback or violations; Meta Page Support Inbox response is 3 business days; Discord and Telegram appeals: `unverified` paths.

## 7. Branded content, ads disclosure and legal
Not legal advice.
- Click-to-message ads: the first user message after a Click-to-Messenger or Click-to-Instagram Direct ad can open a window up to 7 days; a Click-to-WhatsApp ad can open a free entry point window (WhatsApp pricing page says up to 7 days) during which all message categories are not charged. Ads follow Meta advertising policies; Sponsored Messages carry a "Sponsored" label.
- WhatsApp costs: per-message pricing since 1 July 2025; charged when a message is delivered; categories: marketing, utility, authentication (templates) and service (non-template, inside the window). Each business phone number gets 1,000 free service messages per month. Per the pricing page, from 1 October 2026 service messages beyond the free tier and utility messages sent inside an open window became chargeable, and businesses without a payment method on file by 30 September 2026 may have service messages stopped. Rate depends on category and the recipient's country calling code (Egypt +20 rate: `unverified`). Meta can change pricing only on 1 Jan, 1 Apr, 1 Jul or 1 Oct. A "Meta Business Agent" non-template category (added 1 July 2026) is billed per token.
- Sponsorship disclosure in public posts or server announcements: label sponsored content with the platform tool where it exists (Meta branded content tools on Facebook and Instagram) and a plain word in Arabic or English such as "إعلان" or "ad". Discord and Telegram have no dedicated sponsorship label found; disclose in text.
- Consent and data: opt-in must be explicit, recorded and revocable; Meta requires automation disclosure where law requires; WhatsApp requires opt-out handling. High-level frameworks: GDPR (EU), CCPA (California), Egypt's Personal Data Protection Law 151 of 2020 (details `unverified`). Telegram bots need an accessible privacy policy (Bot Developer Terms).
- Giveaways in chat: publish rules, avoid requiring chat messages or tagging as entry, do not collect sensitive data; local lottery rules apply.
- Payments: do not request full card numbers, financial account numbers or other sensitive identifiers in WhatsApp (policy).

## 8. API and automation
- Discord: Discord API/Gateway (docs.discord.com). Bot token (OAuth2 app). Can (general API surface; only rate limits, intents and policies were verified line by line): send, edit and delete messages in channels and DMs the bot can reach, slash commands and interactions, moderation actions, roles, threads, webhooks. Cannot: act as a user (self-bots forbidden), read message content without the privileged MESSAGE_CONTENT intent, DM users who have not interacted without permission (policy). Privileged intents (GUILD_MEMBERS, GUILD_PRESENCES, MESSAGE_CONTENT) must be enabled in the portal; apps in 100 or more servers must be verified and approved for them; above 10,000 unique users an access review is required. Without the intent, message content fields are empty except for messages the app sends and DMs with the app. Rate limits: 50 requests per second global per bot; per-route buckets with `X-RateLimit-*` headers; 429 includes `retry_after`; invalid requests (401, 403, 429) above 10,000 per 10 minutes per IP cause a temporary restriction; interaction endpoints are not bound by the global limit. Scheduling: none native for messages (use scheduled events or your own scheduler). Premium Apps requirement for paid features from 7 October 2024 in supported regions.
- Messenger Platform (Meta Graph API): Page access token, `pages_messaging` permission; Send API, webhooks, handover protocol, private replies, persistent menu; app review and Advanced Access needed to serve accounts you do not own or manage (Standard Access works for roles on the app). Rate limits per Page: Send API 300 calls/s for text, links, reactions and stickers; 10/s for audio and video; Conversations API 2/s; Private Replies 750/hour for Instagram post and reel comments; Business Use Case limit 200 x Engaged Users per rolling 24 hours (error 80006). "Your app may be rate limited if too many messages are being sent to a single thread."
- Instagram Messaging API: Instagram professional account; Instagram User access token; permissions `instagram_business_basic` and `instagram_business_manage_messages`; need the Instagram-scoped ID (IGSID) from a webhook; Advanced Access for accounts you do not own. Rate limits per account: Send API 100 calls/s for text (one Meta table says 300 for the Messenger API for Instagram; confirm which applies to your product), 10/s for media, Conversations 2/s, private replies to Live comments 100/s, private replies to post or reel comments 750/hour. Private replies: one message per commenter, within 7 days; Live only during the broadcast. No One-Time Notification on Instagram. There is no API to send a first DM to a person who has not messaged you or commented.
- WhatsApp Business Platform (Cloud API): Meta app, WhatsApp Business Account, permanent system-user token (store in a secret manager, never in a workflow). Needs business verification for higher limits (details `unverified`). Free-form messages only inside the 24-hour customer service window; outside it, only approved templates and only to opted-in users. Message types inside the window include text, image, audio, video, document, location, contacts, sticker, reaction, interactive buttons, lists, CTA URL buttons, Flows. Messaging limits are per business portfolio (250 initial, 2,000 after scaling). Template review can pause or reject templates at any time. The WhatsApp Business app (non-API), broadcast lists and Channels: API coverage and limits `unverified`.
- Telegram Bot API (core.telegram.org/bots/api, version 10.3 on 24 Aug 2026): bot token from @BotFather; long polling (`getUpdates` returns the earliest 100 unconfirmed updates) or webhooks (ports 443, 80, 88, 8443; valid certificate; polling does not work while a webhook is set). Limits: about 1 message per second in a chat, 20 messages per minute in a group, about 30 messages per second for bulk notifications; paid broadcasts raise this to 1,000 per second at 0.1 Stars per message above the free 30/s (requires a Stars balance, FAQ states at least 100,000 Stars). Spread broadcasts over 8 to 12 hours to avoid 429. Bots cannot start conversations and cannot see other bots. Business bots (`business_connection`) exist for Telegram Business chat automation.
- n8n and Make guidance: use official nodes or HTTP Request; one workflow per channel; central queue with per-channel rate limiting (Telegram 30/s, Discord 50/s, Meta per-Page limits); idempotency key from message id; separate "inbound classification" from "outbound send"; log opt-in proof; always include a human-handoff branch; never auto-reply in WhatsApp outside the window (it will fail).

## 9. Analytics
- Discord: Server Insights is available for Community servers (retention, activation, communication); metric definitions `unverified`. Track: new members, retention after 7 days, active posters, tickets resolved.
- Messenger and Instagram DM: Meta Business Suite inbox metrics: response rate, response time (definitions `unverified` here). Track conversations started from ads, first response time, resolution time, thread ownership.
- WhatsApp: quality rating and messaging limit tier in WhatsApp Manager (Account tools > Phone numbers; Messaging limits); `GET /<BUSINESS_PHONE_NUMBER_ID>` with `whatsapp_business_manager_messaging_limit` returns the tier (for example TIER_250); `business_capability_update` and `account_alerts` webhooks signal changes. Template quality and delivered counts for billing.
- Telegram: channel statistics in the app (views per post, followers, notifications); API analytics for bots: none official (`unverified`).
- Which metric answers which question: Are we reachable? First response time. Are we annoying people? Block rate and quality rating on WhatsApp, unsubscribe on Telegram. Does DM drive revenue? Orders per conversation by source tag. Is the community alive? Weekly active posters and 7-day retention on Discord.

## 10. Cases
**Situation:** WhatsApp quality drops or messaging limit gets stuck at 250.
**Do:** Check WhatsApp Manager quality rating and recent blocks and reports; pause marketing templates; send only to recently engaged opted-in users; improve template content and opt-in wording; wait for automatic scaling (needs high quality and at least half the limit used in the last 7 days) or complete a scaling path.
**Avoid:** Blasting purchased lists, resending to non-responders, creating extra numbers to bypass a limit (limits are per portfolio).

**Situation:** Customer writes on Instagram DM after more than 24 hours and the reply is blocked.
**Do:** If it needs a human reply, use the Human Agent tag within 7 days; otherwise ask them to message again or move to a channel they opted into; reply from the Instagram app inbox manually where allowed.
**Avoid:** Misusing tags for promotions (can restrict messaging), spamming "are you there" messages.

**Situation:** Negative comment wave turning into DM threats or abuse.
**Do:** Document and escalate; reply publicly once with a contact route; use a private reply only once per commenter; hide or report abuse; assign a senior agent; do not trade personal data in public.
**Avoid:** Auto-replying to every angry comment with a template (30-second bot rule applies to automated bots and loops can annoy users).

**Situation:** Fake or impersonator account contacts customers on WhatsApp, Instagram or Telegram.
**Do:** Report in-app, collect screenshots, warn customers with your verified handle and a rule ("we never ask for card numbers or OTP codes in chat"), request verification where available, secure real accounts with two-step verification.
**Avoid:** Sharing the impostor's link in public posts, answering the impostor.

**Situation:** Discord raid or spam wave in the server.
**Do:** Raise the server verification level, enable the explicit media filter, lock channels temporarily, ban and report, announce calmly in the rules or announcements channel, review AutoMod rules (`unverified` for exact settings).
**Avoid:** Using a self-bot or user-token automation to ban or message people (prohibited), mass-DMing members.

**Situation:** Planning a giveaway across Discord and Telegram.
**Do:** Publish rules, eligibility, dates and winner selection; require no purchase; collect minimal data; disclose sponsors; on Telegram avoid schemes where prizes are refunded through third parties; on Discord do not inflate membership with bots.
**Avoid:** Entry by inviting friends in bulk, fake accounts, prizes in restricted categories.

**Situation:** Cross-posting the same announcement to Telegram channel, Discord and a WhatsApp broadcast.
**Do:** Adapt per channel: Telegram 4096 chars or 1024 caption; Discord 2000 chars or an embed; WhatsApp broadcast only to opted-in contacts using an approved template; single source of truth in your content calendar.
**Avoid:** Copying Markdown formatting that breaks (Discord Markdown differs from WhatsApp bold with asterisks), pushing marketing to users who opted in only for order updates.

**Situation:** A wrong or harmful message went out (wrong price, wrong link, sensitive info).
**Do:** Delete where possible (Telegram channel delete removes for all subscribers; Discord delete), send a corrected message immediately, log the incident, notify affected users where personal data was exposed.
**Avoid:** Silent deletion of a message that made a promise; resending the correction to everyone if only a small segment saw it.

**Situation:** Crisis (outage, product recall) during which DMs spike.
**Do:** Pin an announcement in the Discord announcement channel and Telegram channel; set an automatic away or greeting message where the channel offers one (availability per channel `unverified`) with a link to the status page; use utility templates for WhatsApp updates to affected opted-in customers; add human agents; maintain the handoff packet.
**Avoid:** Promotional templates during the crisis, claiming a fix before it is confirmed.

**Situation:** Handing over community or inbox access to an agency.
**Do:** Use Meta Business Manager roles and system users, Discord roles and a dedicated bot application owned by the company team, Telegram bot tokens stored in a secret manager and rotated at exit, WhatsApp Manager roles; document owners, escalation contacts and offboarding steps.
**Avoid:** Sharing personal logins, putting tokens in chats or workflow JSON, letting an agency own the WhatsApp Business Account or Discord server.

## 11. Arabic and Egypt notes
- Instagram DM text limit is 1,000 bytes of UTF-8. Arabic letters are 2 bytes each in UTF-8, so a reply is about 500 Arabic characters, fewer with emoji (usually 4 bytes). Split long answers into several messages or send a link.
- WhatsApp templates in Arabic are submitted per language; approval time and Arabic-specific rejection reasons: `unverified`. Keep variables at the end of a sentence to avoid RTL reordering, and put English product names and numbers on separate lines.
- Dialect: Egyptian colloquial is natural in DMs and Discord; keep templates and legal or billing messages in simple Modern Standard Arabic or neutral Egyptian to avoid misreading. Provide an English option where the audience is mixed.
- Discord: Arabic server names and channel names are allowed (`unverified` for restrictions); use clear English or transliterated names for channels that bots reference by name.
- Telegram: Arabic is available in Telegram's interface (language list on telegram.org). RTL text works in channel posts and captions.
- Phone numbers: use international format with +20 for Egyptian mobile numbers when registering opt-ins and calling the WhatsApp API; pricing is by country calling code (Egypt rate `unverified`).
- Payments: WhatsApp requires a payment method on file for chargeable messages (per pricing page); accepted Egyptian payment methods and local currency billing: `unverified`. Telegram paid broadcasts use Stars; Discord Premium Apps availability in Egypt: `unverified`.
- Verification quirks: Meta Business verification may request a commercial register or tax card in Egypt (`unverified`; do not assume).
- Local etiquette (heuristic, `unverified`, not an official rule): greet in Arabic, avoid late-night promotional sends, avoid generic holiday-greeting broadcasts that carry a sales pitch, and test send times around Friday midday.
- Hashtag habits: not relevant inside DMs; on Telegram and Discord public posts use a few Arabic hashtags; counts `unverified`.

## 12. Pre-publish checklist
1. Does the recipient have explicit, recorded opt-in for this channel and this message category?
2. Is the message inside the 24-hour window (or 7-day Human Agent / ad window), or is an approved template used?
3. Is the length within the channel limit (Discord 2000; Instagram 1,000 bytes; WhatsApp 4096; Telegram 4096 or caption 1024)?
4. For Arabic text on Instagram, did you count bytes, not characters?
5. Is the message free of full card numbers, OTP codes, passwords or other sensitive identifiers?
6. Is sponsored or promotional content labeled, and is it allowed outside the window on this channel?
7. Does the message offer an opt-out or a path to a human?
8. For a bot message on Messenger, will it answer within 30 seconds, and does it disclose automation where required?
9. For Discord, does the bot avoid unsolicited DMs and avoid reading message content without the intent?
10. Is the rate within limits (Telegram 30/s bulk and 20/min in groups; Discord 50/s; Meta per-Page limits; WhatsApp tier)?
11. Is the handoff packet attached (language, intent, ids, consent) if a human takes over?
12. Is there a safe way to delete or correct the message if it is wrong?

## 13. Sources
- https://docs.discord.com/developers/topics/rate-limits
- https://docs.discord.com/developers/resources/message
- https://docs.discord.com/developers/events/gateway
- https://docs.discord.com/llms.txt
- https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy
- https://discord.com/guidelines
- https://support.discord.com/hc/en-us/articles/360047132851-Enabling-Your-Community-Server
- https://developers.facebook.com/docs/messenger-platform/policy/policy-overview
- https://developers.facebook.com/docs/messenger-platform/handover-protocol
- https://developers.facebook.com/docs/messenger-platform/discovery/private-replies
- https://developers.facebook.com/docs/messenger-platform/instagram/features/private-replies
- https://developers.facebook.com/docs/messenger-platform/send-messages
- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api
- https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages
- https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages
- https://developers.facebook.com/docs/whatsapp/messaging-limits
- https://developers.facebook.com/docs/whatsapp/pricing
- https://whatsappbusiness.com/policy/
- https://www.whatsapp.com/legal/business-solution-terms
- https://core.telegram.org/bots/api
- https://core.telegram.org/bots/faq
- https://core.telegram.org/bots
- https://telegram.org/tos
- https://telegram.org/tos/bot-developers
- https://telegram.org/faq_channels
- https://telegram.org/faq
