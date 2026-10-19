# WhatsApp — rules and playbook
Last verified: 2026-10-19

Scope: WhatsApp Business app, WhatsApp Business Platform (Cloud API), Channels, Communities, Status. WhatsApp is a messaging channel, not a feed: success is consent, template quality, and reply speed. Labels: **official** = Meta developer docs, WhatsApp Business policy/terms, WhatsApp blog or business site fetched on 2026-10-19; **third-party** = vendor or press article; **practitioner observation, not an official rule**; **unverified** = not confirmed this session. Prices and limits change on fixed dates; re-read the pricing page before quoting costs to a client. WhatsApp help-center (faq.whatsapp.com) pages are partly blocked to crawlers, so some Business app, Status and Communities facts are unverified.

## 1. Snapshot
- Egypt: a vendor guide (chatdaddy.tech, 2026-03-24, third-party and mostly unsourced) claims about 52 million WhatsApp monthly users in Egypt and that 76% of smartphone users have WhatsApp. DataReportal's Digital 2026: Egypt table did not list WhatsApp, so use these as indicative only. Facebook reaches 51.6M and Messenger 37.0M (DataReportal, ad reach, Oct 2025).
- Best for: customer service, order and booking updates, lead follow-up after Click-to-WhatsApp ads, one-to-many news through Channels, community groups.
- Three product families: **WhatsApp Business app** (free, phone, manual and small automation), **WhatsApp Business Platform** (Cloud API for automation at scale, per-message pricing), and **public surfaces** in the Updates tab (Channels, Status, Communities). WhatsApp says the Updates tab (Channels and Status) is used by 1.5 billion people a day (WhatsApp blog, 2025-06-16).
- Product rule that drives everything: a business may only message people who gave their number and opted in, and outside a 24-hour window only approved templates may be sent.

## 2. Content formats and specs
| Format | Aspect ratio / size | Length or duration | File limits | Notes |
|---|---|---|---|---|
| Service (free-form) message | n/a | text length: unverified | n/a | Only within the 24-hour customer service window; any user message or call resets it to 24 h (official). |
| Template: marketing | header image/video/document/GIF | body 1,024 chars | media via Resumable Upload | Business-initiated, any time to opted-in users. GIF headers only via Marketing Messages API (mp4, 3.5 MB). |
| Template: utility | same as above, location header allowed | same | same | Non-promotional, tied to a user action or request. |
| Template: authentication | text only | one-time passcode | no URLs, media or emoji; parameters max 15 chars | Must use authentication template library with OTP button. |
| Image | JPEG or PNG, 8-bit RGB/RGBA | n/a | 5 MB | Official media page. |
| Video | MP4 or 3GP, H.264 video and AAC audio | unverified | 16 MB | Single or no audio stream. |
| Audio | AAC, AMR, MP3, M4A, OGG (OPUS, mono) | unverified | 16 MB | Official. |
| Document | PDF, TXT, Word, Excel, PowerPoint | n/a | 100 MB | Official. |
| Sticker | WebP | n/a | static 100 KB, animated 500 KB | Official. |
| Interactive (buttons, lists, catalog) | n/a | unverified | unverified | Exist in Cloud API; per-type limits not read: unverified. |
| Broadcast list (Business app) | n/a | n/a | up to 256 contacts per list | Recipients must have your number saved; not available on Windows, Mac or Web. Official help page. |
| Business Broadcast (Business app) | n/a | n/a | n/a | Reaches people who have not saved your number; scheduling, action buttons and insights; "available to eligible users in select countries". Egypt availability: unverified. |
| Channel update | text, photo, video, sticker, link, audio, poll | n/a | unverified | One-way. Followers cannot reply; they can react or vote in polls. Channel history stored up to 30 days (2023 blog, may have changed). |
| Status | unverified | 24 h life: unverified | unverified | Not supported on Cloud API or coexistence (official coexistence page); ads can run in Status (2025-06-16 blog). |
| Community announcement | n/a | n/a | n/a | Only admins post; announcement group holds all members; the page read says 2,000 members max per community: re-check. Admin roles: up to 20 (setup page). |
| Group (Cloud API) | n/a | n/a | up to 8 participants per group, 10,000 groups per number | Only for businesses with an Official Business Account; not for Business-app numbers. Official Groups API page. |

Media retention: uploaded media kept 30 days; API media IDs expire after 30 days (7 days in incoming webhooks); media download URLs expire after 5 minutes.

## 3. Text limits
| Item | Limit | Status |
|---|---|---|
| Template name | up to 512 chars, lowercase letters, numbers, underscores | official |
| Template body | 1,024 chars | official |
| Template header (text) | 60 chars, 1 variable | official |
| Template footer | 60 chars, text only | official |
| Buttons | up to 10 per template; quick reply 25 chars (up to 10); phone 1 (25 chars); URL up to 2 (25 chars label, URL up to 2,000 chars, 1 variable at the end) | official |
| Variables | positional `{{1}}` or named `{{name}}`; each needs a sample at creation | official |
| Free-form text message | no figure read (commonly cited as 4,096): unverified | unverified |
| Media caption | unverified | unverified |
| Business profile About / description | unverified | unverified |
| Hashtags | not a feature | n/a |
| Mentions | not applicable to business messages | n/a |
| Links | URLs in message text are clickable; in templates use URL buttons; authentication templates cannot contain URLs | official for templates; clickable text: practical |
| Emoji / Arabic / RTL | emoji not allowed in authentication templates; Arabic template text is accepted and renders RTL in practice (third-party claim, no source): unverified | partly unverified |
| Broadcast list | 256 contacts | official |

## 4. Posting and cadence
- No posting schedule: cadence is set by consent and limits. Marketing messages count against a per-user limit that adapts to each person's recent read rate and inbox volume; Meta does not publish the number (official).
- If a marketing template fails with error 131049 (per-user limit or repeated resend), wait at least 24 hours before retrying; excessive retries can block further attempts to that user for up to 24 hours.
- WhatsApp does not currently deliver marketing templates to users with US phone numbers (+1 US area codes); the API returns an error (official).
- Heuristic (practitioner observation, not an official rule): at most 2 to 4 marketing templates per opted-in user per month, one clear action per message, and always an opt-out path. Egypt timing: after work and after iftar during Ramadan (7 to 11 pm, third-party), Friday is the weekly day off in Egypt (third-party).
- Funnel mapping:
  - Awareness: Click-to-WhatsApp ads, Channels with promotion, ads in Status, QR codes and wa.me links, Community.
  - Consideration: replies in the 24 h window with catalog, price and FAQs; Business app catalog and labels.
  - Conversion: cart and order flows, utility templates for confirmations, payment links, appointment booking.
  - Retention: utility updates (shipping, appointment), authentication codes, opt-in service updates, Channel for news, templated win-back with strict opt-out handling.

## 5. Distribution and ranking signals
There is no feed ranking. Deliverability and reach depend on these official signals:
- Opt-in and user feedback: people can block or report a business, or stop marketing messages from it; reports affect messaging limits (policy page, last updated 2026-09-23).
- Template quality: GREEN (high), YELLOW (medium), RED (low), UNKNOWN (new); driven by user feedback and read rate; low quality risks pausing or disabling; status other than APPROVED cannot be sent. Templates inactive 12 months are archived and then deleted after 28 days.
- Messaging limits (section 8): 250 for new portfolios, 2,000 after scaling path, then 10,000, 100,000, unlimited, auto-scaled when quality is high and at least half the limit was used in the last 7 days.
- Per-user marketing limit and read rate (section 4).
- Channels discovery: directory search and browsing, invite links and QR codes, in-app sharing by followers; admins can pay to promote channels in the directory and run ads in Status (WhatsApp blog, 2025-06-16). Channel subscriptions are available to some creators.
- Practitioner lore (practitioner observation, not an official rule): short templates with a clear name and one button get higher read rates; sending right after the user opted in improves engagement; heavy sending to cold lists is the fastest route to a RED rating.

## 6. Community rules and policy hot spots
- Opt-in: businesses may only contact people who gave their mobile number and agreed to receive messages from that business; the opt-in must say the person is agreeing to messages and name the business; separate opt-ins by category are recommended; opt-outs must be honored whether made in or off WhatsApp (official policy and opt-in pages). Methods named: SMS, website forms, IVR, in-person or paper sign-up. Bought or scraped lists are not opt-in.
- Spam and bulk: start conversations only with approved templates; free-form replies only inside the 24 h window; no deceiving, misleading, defrauding or surprising people; Meta may limit volume based on user feedback and remove access for unauthorized scale messaging (official).
- Prohibited goods and services (official policy): firearms, alcohol and tobacco, drugs, medical products, endangered wildlife, hazardous materials, currency and ICOs, body parts or fluids, adult products, dating services, multi-level marketing, payday loans and debt collection (with limited exceptions); real-money gambling restricted and never to under 18; sexual or nude content and discrimination prohibited; political parties, candidates and campaigns, law enforcement, military and intelligence agencies prohibited; news publishers must register as a News Page. Some regulated verticals are allowed only in listed countries and only on the Platform, not the Business app.
- Automation and AI: automated replies are allowed in the 24 h window but must offer a clear path to a human (policy page). The Business Solution Terms (last modified 2026-03-06) bar AI providers (large language models, general-purpose assistants) from using the Business Solution to offer those tools when they are the primary functionality; exception for tools offered only to users with EEA or Brazil phone numbers. A normal business bot for its own customers is allowed (it is incidental to the business). Using Business Solution Data to train AI models is not allowed; fine-tuning a model for the business's own exclusive use is.
- Template categorization: marketing includes anything promotional or unclear (for example only "{{1}}" or "Congratulations!"); utility must be non-promotional and tied to a user action or request or essential and critical; authentication is OTP-only. Misuse escalates: warning, rate limiting of utility messages (min 7 days), utility restriction where all approved utility templates become marketing (7 days, 30 for repeat), portfolio-level restriction (30 days). Since 2025-04-09 a utility template that should be marketing is approved as marketing; since 2025-04-16 warned businesses get no 24-hour notice.
- Account enforcement ladder (official): warning; 1- or 3-day block on templates and adding numbers; 5-, 7- or 30-day block on all messages; account lock until appeal; permanent disablement. Severe harm (scams, child exploitation, terrorism, illegal drugs) can mean immediate offboarding. Appeals through Business Support Home usually take 24 to 48 hours; not all spam violations can be appealed.
- Copyright and music: not a platform-specific feature; use only media you have rights to. Impersonation of other businesses is prohibited (policy). Minors: gambling messages never to under 18; consent for minors under Egypt's data law is sensitive (section 11).
- Giveaways: no WhatsApp-specific promotion rules found: unverified. Do not use WhatsApp numbers collected for a contest for later marketing without a separate opt-in.
- Buying followers: no Channel-specific rule read (Channels Guidelines page not readable: unverified); do not buy followers. Buying or renting contact lists breaks the opt-in rule.

## 7. Branded content, ads disclosure and legal
Not legal advice.
- WhatsApp has no paid-partnership label. Influencer or sponsored content published in Channels or Status still needs plain disclosure ("Ad", "Sponsored"). US FTC guidance: disclose material connections clearly and early, in plain words, in the same language as the endorsement; platform tools alone are not enough; responsibility sits with the endorser. https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Ads that lead to WhatsApp (Click-to-WhatsApp, ads in Status) follow Meta ad rules (not read: unverified).
- Egypt: Personal Data Protection Law No. 151 of 2020 requires explicit consent for direct electronic marketing, sender identity and a valid contact address, a clear marketing label, an easy opt-out, and consent records kept 3 years after the last message; a licence or permit from the Personal Data Protection Centre is required for electronic marketing; breaches reportable within 72 hours; fines up to EGP 5,000,000 and imprisonment possible; children's data is sensitive; cross-border transfers need adequate protection and licence (DLA Piper summary, modified 2026-02-13). Anti-Cybercrime Law 175/2018 article 25 covers privacy violations including unsolicited marketing emails. WhatsApp's own rule is similar: the business is solely responsible for the opt-in method and legal notices.
- EU and US: GDPR/ePrivacy and TCPA-style consent rules apply to marketing messages; not read this session: unverified.
- Record keeping: store opt-in source, timestamp, wording shown, and category consent for every contact.

## 8. API and automation
- Official products: WhatsApp Business Platform with **Cloud API** (messaging, rich media, interactive, calling, group conversations), **Business Management API** (accounts, numbers, templates, billing, analytics), **Marketing Messages API** (quality-based delivery, automated creative optimization, benchmarks, conversion metrics; businesses can set a max price in 2026), **Webhooks**, and **Meta Business Agent** (AI agents; billed per token from 2026-07-01). The older on-premises API is not described in the docs read: unverified.
- Auth: OAuth access tokens sent as `Authorization: Bearer`. Token types: system user tokens (long-lived, recommended for automation), Business Integration System User tokens (partners via Embedded Signup), user tokens (testing only; expire in hours). Assign `business_management`, `whatsapp_business_management`, `whatsapp_business_messaging`; use least privilege; never log tokens. App Review and Advanced Access requirements for the WhatsApp permissions: not read: unverified.
- Onboarding: via App Dashboard, WhatsApp Manager, Meta Business Suite or Embedded Signup (Solution Partner or Tech Provider). Numbers need an owned phone number with country code that can receive SMS or voice; no short codes; a display name is required; two-step verification PIN required. A new portfolio can register 2 numbers, rising to 20 after business verification or a 2,000 messaging limit.
- Official Business Account (blue check): needs 30 days on the Platform, passed Business Verification, two-step verification, approved display name, policy compliance; not for Business-app numbers.
- Coexistence (Business app plus Cloud API on one number): requires Business app version 2.24.17 or higher and a Solution Partner or Tech Provider; throughput fixed at 20 messages per second; history sync up to 180 days within 24 hours of onboarding; groups, disappearing and view-once messages, live location, broadcast lists, catalog, orders, status and channels are not available through it; primary device disconnects after about 14 days of inactivity. App messages stay free.
- Messaging rules: customer service window of 24 h from the user's last message or call; free-form replies only inside it; outside it only approved templates. Free entry point window: replying inside the window to a Click-to-WhatsApp ad conversation may keep a window open up to 7 days (official pricing page; older sources said 72 hours).
- Messaging limits (official, portfolio-level since 2025-10): new portfolio 250 unique users per rolling 24 h outside windows; 2,000 after a scaling path (business verification, partner verification, or 2,000 delivered template messages to unique users in 30 days with high quality); then 10,000, 100,000, unlimited by automatic scaling (within 6 hours when quality is high and at least half the limit was used in the last 7 days). The Flagged state was removed and a quality drop no longer lowers the limit. Field `messaging_limit_tier` is deprecated; use `whatsapp_business_manager_messaging_limit`.
- Throughput: 80 messages per second per number by default; automatic upgrade to 1,000 mps for unlimited portfolios that message 100K+ unique users in 24 h with quality Medium or higher; upgrade takes up to 1 minute (error 131057 during it). Pair rate limit exists but no number found: unverified. Error 130429 = throughput exceeded.
- Templates: 250 per Messaging account (unverified portfolio) or 6,000 (verified with an approved display name); creation up to 100 per hour; review up to 24 hours (usually automatic); statuses include In Review, Rejected, Active (quality pending/high/medium/low), Paused, Disabled; pacing and pausing apply to poor-quality templates.
- Pricing (official, https://developers.facebook.com/docs/whatsapp/pricing): per delivered message since 2025-07-01; categories marketing, utility, authentication and service; marketing has no volume tiers; utility and authentication have volume tiers; rate-card changes happen only on Jan 1, Apr 1, Jul 1, Oct 1. As read on 2026-10-19: from 2026-10-01 service messages are free only for the first 1,000 delivered per business number per month (no rollover) and charged after that; utility templates sent inside an open customer service window became charged on 2026-10-01 (they were free from 2025-07-01 to 2026-09-30); free entry point window messages stay free; Meta Business Agent replies are billed per token. Egypt rates: unverified amounts (Egypt marketing rate fell 2026-01-01; utility and authentication fell 2025-10-01; see the rate card). Vendor figures such as $0.0972 marketing in Egypt are unsourced and may be outdated: unverified.
- Webhooks: `messages`, `account_update`, `account_alerts`, `business_capability_update`, `message_template_status_update`, `message_template_quality_update`, `phone_number_quality_update`, `template_category_update`, `smb_message_echoes` and more; subscribe to `account_update` to catch warnings and restrictions early.
- BSUID and usernames (official): since April 2026 webhooks include a business-scoped user ID (format like `US.1349...`); from 2026-06-29 businesses can reserve usernames; from July 2026 APIs can send to BSUIDs; a user's phone number can be missing from webhooks when they use a username and no recent contact exists (30 days). Store BSUIDs, handle missing phone numbers, handle `user_changed_number` and `user_changed_user_id` system messages. One-tap, zero-tap and copy-code authentication need phone numbers (error 131062 for BSUID sends).
- Scheduling: Cloud API has no native scheduler: queue on your side and send within limits. Business app supports scheduled Business Broadcasts where available.
- Forbidden automation: messaging non-opted-in numbers, using templates in the wrong category, bots that give no human path, selling or sharing Business Solution Data, AI-provider chatbot as primary product (section 6), unofficial WhatsApp Web or multi-device bots that automate personal accounts (the Terms page not read for this: unverified; widely known to cause bans).
- No API found (practitioner and docs index): creating or posting to Channels (the docs index has no Channels section), Status posts, Communities, Business app Broadcast lists, labels. Treat these as manual or app-only.

## 9. Analytics
- Where: WhatsApp Manager (analytics, template metrics, messaging limit, quality), Business Management API, webhooks (`pricing` object on each status), Marketing Messages API metrics (conversions, click events), Business app Insights (counts of messages sent, delivered, read: unverified), Channel Insights.
- Channel Insights (official FAQ, last 30 days): accounts reached, top regions, follows and unfollows, total followers; per update: reactions (number and type) and poll results; admins can see which followers are also contacts.
- Delivery states: sent, delivered, read, failed (error codes). Cost is charged on delivered messages.
- Question to metric: Is the audience reachable? delivered vs sent and error 131049 rate. Is it wanted? read rate, block and report signals via template quality rating. Do templates convert? Marketing Messages API conversion metrics or click events on tracked links. Are we near limits? `whatsapp_business_manager_messaging_limit` and the 7-day usage versus half of the limit. Is the account safe? `account_update` and `phone_number_quality_update` webhooks. Is the Channel growing? follows minus unfollows and reach in Insights.

## 10. Cases
**Situation 1: Template messages fail with error 131049 or delivery suddenly drops.**
**Do:** Treat 131049 as the per-user marketing limit; wait at least 24 hours before resending to that user; reduce marketing frequency; check read rate and the template quality rating (GREEN, YELLOW, RED); remove users who never read; make sure the number is not a US +1 number (marketing templates are not delivered there).
**Avoid:** Retrying in a loop, re-sending to everyone each day, creating clone templates to bypass pausing.

**Situation 2: Template paused, disabled or recategorized from utility to marketing.**
**Do:** Read the `message_template_status_update` or `template_category_update` webhook; fix wording (remove promotion from utility copy); appeal within 60 days or request a category review; rewrite as marketing and accept marketing price; keep utility templates strictly transactional.
**Avoid:** Adding discount codes to order-status templates, using vague bodies such as only "{{1}}" (treated as marketing), asking for authentication content in a utility template.

**Situation 3: Number restricted, locked or warned.**
**Do:** Open Business Support Home, read the violation and restriction length (1/3 days block templates; 5/7/30 days block all messages); stop campaigns; request review (24 to 48 hours typically); fix the opt-in source; confirm admin contact emails and `account_update` webhook are active.
**Avoid:** Switching to a new number to continue the same campaign, appealing without changing behavior, ignoring a warning.

**Situation 4: Complaint wave, many blocks and reports.**
**Do:** Pause the campaign, check which template and audience triggered it, shorten and clarify the opt-in message, offer a clear "reply STOP" or opt-out button, honor opt-outs immediately, brief the client.
**Avoid:** Pushing another message to explain, sending to people who never opted in, deleting evidence of opt-in.

**Situation 5: Fake WhatsApp number impersonating the brand (scam payment requests).**
**Do:** Post the official number on the website, Facebook and Instagram bio; apply for an Official Business Account (blue check) when eligible (30 days on Platform, Business Verification, two-step verification, approved display name); report the number in WhatsApp; warn customers that the brand never asks for payment through unknown numbers.
**Avoid:** Responding to the scammer, sharing the fake number as a clickable link, using a personal number as the brand's only contact.

**Situation 6: Giveaway or contest through WhatsApp.**
**Do:** Collect entries by form with a separate, clear consent for later marketing; publish rules; use utility-type confirmation only for the entry itself; delete entrants' data when the contest closes unless they opted in (Law 151/2020).
**Avoid:** Messaging entrants with promotions without separate opt-in, asking people to forward a message to 10 contacts, using purchased lists.

**Situation 7: Cross-posting from Instagram or Facebook to a Channel or Broadcast.**
**Do:** Re-write for one-way updates (short text, image or video, optional poll); no link spam; for Channels use the app or Business app (no API found); keep one clear call to action; use polls and reactions to measure response.
**Avoid:** Pasting a 30-hashtag caption, sending the same post to a Broadcast list of non-opted-in contacts, expecting replies on Channels (followers cannot reply).

**Situation 8: A sent message is wrong.**
**Do:** Inside the 24 h window send a short correction; outside it use an approved utility template if the correction is about an existing order or appointment; Business app and coexistence support editing and revoking of messages after onboarding (official coexistence page); log the correction.
**Avoid:** Sending a promotional template as an apology, deleting the evidence, sending a second marketing message to explain.

**Situation 9: Customer writes after the 24-hour window closed.**
**Do:** Any new user message or call reopens a 24 h window; reply with free-form content; if you must reach them first, send an approved utility template (if related to their request) or a marketing template (if they opted in).
**Avoid:** Using a utility template for promotion, using the "HUMAN_AGENT" tag (that is Messenger/Instagram, not WhatsApp).

**Situation 10: Chatbot design and AI.**
**Do:** Let the bot answer inside the 24 h window, offer "talk to an agent" at every step, disclose that the user is talking to an automated assistant, keep it a business-specific assistant for your own customers (permitted) rather than a general-purpose AI product (prohibited for AI providers whose primary functionality it is).
**Avoid:** Training models on Business Solution Data from third parties, bots with no human escalation, general chatbots offered as a public service.

**Situation 11: Handing over access safely.**
**Do:** Use a Meta Business portfolio, give the agency partial access to the WhatsApp account, create a system user with least privilege for automation, rotate tokens on exit, keep the two-step verification PIN in a password manager, keep two admins.
**Avoid:** Sharing the SIM or the personal phone, giving full portfolio control to a freelancer, pasting tokens in chat tools.

**Situation 12: Webhook arrives without a phone number.**
**Do:** Use the BSUID (`user_id`) as identifier, send replies to the BSUID, store both identifiers, handle `user_changed_number` and `user_changed_user_id`.
**Avoid:** Using phone number as the only key, dropping the event.

## 11. Arabic and Egypt notes
- Arabic templates: the body supports Arabic text and variables; variables inside Arabic sentences can break word order, so keep a variable at the end of a clause and test rendering on Android and iOS (practitioner observation). Egyptian dialect is accepted by users and by template review according to a vendor guide (third-party, no source: unverified); use Modern Standard Arabic for formal notices.
- Numbers: Egyptian mobile numbers are written with country code 20 and no leading 0 (for example 201xxxxxxxxx); normalize before sending and store in E.164 format (practitioner).
- Language and category: provide template translations per language; each language version counts against the template limit (official).
- Rhythm: Friday is the weekly day off; Ramadan activity peaks after iftar (third-party).
- Payments and verification: a vendor guide lists documents for Business Verification in Egypt (commercial register extract, tax card, Facebook Business Page and website) and local payment tools (Fawry, InstaPay, mobile wallets); these are third-party and unverified. Meta billing currency and local card acceptance for Egyptian businesses: unverified.
- Rates: Egypt-specific amounts not confirmed this session; use the official rate card in WhatsApp Manager or https://developers.facebook.com/docs/whatsapp/pricing before quoting.
- Law: Law 151/2020 explicit consent, clear marketing label, opt-out, consent records 3 years, licence for electronic marketing; Anti-Cybercrime Law 175/2018 article 25 for unsolicited marketing (DLA Piper summary). Not legal advice.
- Local etiquette: greet in dialect, avoid sending at night (10 pm to 8 am Cairo time is a practitioner suggestion), never message about religion or politics for marketing, make opt-out visible.

## 12. Pre-publish checklist
1. Does every recipient have documented opt-in naming this business, for this message category?
2. Is the message inside the 24 h window, or is it an approved template?
3. Is the template category honest (promotion = marketing; utility has no offer; authentication = OTP only, no URL, media or emoji)?
4. Template limits: body at most 1,024 chars, header at most 60, footer at most 60, button labels at most 25?
5. Are media files within limits (image 5 MB JPEG/PNG, video 16 MB MP4 H.264, audio 16 MB, document 100 MB)?
6. Is the send within the portfolio's messaging limit and the 7-day usage plan, and is the per-user marketing risk (131049) acceptable?
7. Are US +1 recipients excluded from marketing templates?
8. Is an opt-out path present and does the system honor it immediately?
9. Is there a human escalation path, and is the bot disclosed as automated?
10. Does the copy avoid prohibited goods, regulated claims and sensitive categories?
11. Are variables filled, Arabic text checked for RTL order, links on URL buttons?
12. If a Channel update: is it one-way content with a single call to action, and are Insights tracked after 24 hours?

## 13. Sources
- https://developers.facebook.com/docs/whatsapp/pricing
- https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform
- https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/upcoming-messaging-limits-changes.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement
- https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers
- https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media
- https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids
- https://developers.facebook.com/documentation/business-messaging/whatsapp/changelog
- https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/groups.md
- https://developers.facebook.com/documentation/business-messaging/whatsapp/llms.txt
- https://whatsappbusiness.com/policy/ (WhatsApp Business Messaging Policy, last updated 2026-09-23)
- https://www.whatsapp.com/legal/business-solution-terms (last modified 2026-03-06)
- https://whatsappbusiness.com/products/business-app-features/
- https://faq.whatsapp.com/861663048350950/?cms_platform=android (broadcast lists)
- https://faq.whatsapp.com/265055289421317 (Channels)
- https://faq.whatsapp.com/582420703681043 (community announcements)
- https://www.whatsapp.com/communities/learning/settingupyourcommunity
- https://www.whatsapp.com/channels
- https://blog.whatsapp.com/introducing-whatsapp-channels-a-private-way-to-follow-what-matters
- https://blog.whatsapp.com/helping-you-find-more-channels-and-businesses-on-whatsapp
- https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- https://www.dlapiperdataprotection.com/index.html?t=law&c=EG
- https://chatdaddy.tech/blog/whatsapp-business-api-egypt (third-party)
- https://datareportal.com/reports/digital-2026-egypt
- Not readable this session: faq.whatsapp.com pages for Business-app communities, Business Broadcasts and creating a Channel (robots-blocked); the Meta rate card (login-gated).
