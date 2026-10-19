# Automation recipes
Purpose: what can and cannot be automated safely per platform, the architecture for a daily multi-platform rotation with approval, and six recipes written node by node for n8n and Make.
Last updated: 2026-10-19

This file is a specification. The `n8n-agent-studio` skill (n8n workflows, browser recipes, agents) and the `automation-studio` skill build the actual workflows; hand them these recipes and the platform files named below. Node and module names are descriptive: confirm exact names in your n8n or Make version. API limits move: re-read section 8 of each platform file before building (check `Last verified`).

## 1. What can and cannot be automated (by platform)
Safe = official API or official scheduler, with logging and an approval gate. Details and numbers: section 8 of each platform file.
| Platform | Automate (official route) | Do not / cannot | File |
|---|---|---|---|
| Instagram | publish via container flow, read comments by webhook, reply to top-level comments, Private Replies, insights | Live, shopping tags, link/poll stickers in Stories, cold DMs, unofficial bots; no scheduling parameter documented: use your own queue | `platforms/instagram.md` |
| Facebook | Page publishing and scheduling via Pages API, comment moderation, Messenger inside the window | posting to Groups (unconfirmed), personal profiles, messaging people outside the window except via approved options | `platforms/facebook.md` |
| WhatsApp | Cloud API replies inside the 24 h window, approved templates to opted-in contacts, webhooks | messaging non-opted-in numbers, Channels/Status posting (no API found), unofficial WhatsApp Web bots | `platforms/whatsapp.md` |
| Telegram | Bot API posts to channels where the bot is admin, group moderation, replies | read full channel history/analytics via Bot API, scraping, spam bots; Bot API scheduling unavailable: schedule in your tool | `platforms/telegram.md` |
| TikTok | Content Posting API (needs app audit for public posts; unaudited = private), drafts to inbox | comment replies and analytics for personal accounts via public APIs, scraping, LIVE | `platforms/tiktok.md` |
| YouTube | uploads with `publishAt`, metadata, comment moderation, within quota | community Posts and DMs via API, automating views/likes | `platforms/youtube.md` |
| LinkedIn | Posts API (self-serve member posting or approved Community Management API), comments | DMs, scraping, headless accounts, one profile managing many clients | `platforms/linkedin.md` |
| X | create posts via API (paid usage), reads, DMs to opted-in users | auto-reply to anyone (self-serve restriction), bulk DMs, auto-likes, near-duplicate posts | `platforms/x-twitter.md` |
| Threads | publish via container flow, replies, insights, keyword search (after approval) | DMs, scheduling endpoint, edit | `platforms/threads.md` |
| Pinterest | Pins via API v5 (Standard access needed for public), analytics | scheduling field, comments/DMs; each Pin must be chosen by the user, so keep a human-approved queue | `platforms/pinterest.md` |
| Snapchat | Public Profile API only if allowlisted (Stories, Spotlight) | comments, chats, scheduling endpoints | `platforms/snapchat.md` |
| Reddit | monitoring and drafting with approved API access | automated posting/commenting/voting, scraping | `platforms/reddit.md` |
| Google Business Profile | posts and review replies after API approval | removing others' reviews, review gating, bulk spam | `platforms/google-business-profile.md` |
| Discord / DMs | bot moderation and replies with a bot token | self-bots, DMing users who did not opt in | `platforms/messaging-and-community-channels.md` |
Where there is no official route, the manual path is the answer: native scheduler in the platform app, or a person posting.

## 2. Architecture: daily multi-platform rotation
```
Calendar source -> Daily trigger -> Select due rows -> Generator (LLM) -> limits_check
   -> Human approval gate -> Router by platform -> Publisher (official API / scheduler)
   -> Log + status update -> Alerts (failure, limits, no-approval) -> Daily heartbeat
Kill switch checked at trigger AND before every publish
```
1. **Calendar source**: Google Sheet, Notion database or Airtable with the columns in `../templates/content-calendar.md` (date, time, platform, pillar, format, copy, asset, link/UTM, status, owner, approvals) plus `post_id`. Status flow: planned, generated, checked, approved, scheduled, published, failed, paused. A separate `config` tab holds `automation_enabled`, timezone (Africa/Cairo) and per-platform daily caps.
2. **Trigger**: schedule trigger each morning (for example 08:00 Cairo) selecting rows with `date = tomorrow` and `status = planned`; a second trigger fires at each row's publish time for status `approved`.
3. **Generator**: LLM step receives pillar, brief, brand voice, facts sheet and platform file limits (not secrets, not customer data). Output must be strict JSON: `text`, `alt_text`, `hashtags`, `first_comment`, `cta`, `link`, `needs_proof` flag. Drafts follow `content-craft.md`. The LLM never publishes.
4. **limits_check**: run `python3 scripts/limits_check.py <platform> --field caption --file draft.txt` (n8n self-hosted Execute Command node, or a small private HTTP wrapper that Make can call; Make cannot run local scripts). Exit code 1 means hard error: set `status = needs-fix`, alert, stop that row. Warnings go to the approver.
5. **Approval gate**: send the final text, media, time, link and checks to the approver (Slack, email or Telegram) and wait. Only `approved` rows continue. Approval expires after a set time (for example 12 h): expired rows are not published. The approver is a person, not the LLM.
6. **Publisher**: Switch on `platform`, then official route only (table above). Where the API has no scheduler (Instagram, Threads, LinkedIn, X, Telegram, TikTok), the workflow itself runs at publish time or sleeps until then. Where a platform needs a human per item (Pinterest, Reddit), the workflow prepares a ready-to-post pack and notifies a person.
7. **Logging**: append one row per attempt: `post_id`, platform, attempt time, request id, platform object id, status, error code, duration. Never log tokens or personal data.
8. **Failure alerts**: an error workflow sends a message with post id, platform, error code and next step (section 8). A daily heartbeat message lists published, failed and waiting rows so silence is visible.
9. **Rate-limit handling**: per-platform queue with delays; read counters before batches (Instagram `content_publishing_limit`, Threads `threads_publishing_limit`, Meta usage headers, X `x-rate-limit-*`, YouTube quota); stop at 80% of a cap; back off on 429/5xx with jitter (`platforms/instagram.md`, `platforms/threads.md`, `platforms/facebook.md`, `platforms/x-twitter.md`, `platforms/youtube.md` section 8).
10. **Cadence guard**: refuse to publish if the platform already has a post in the last N minutes or the daily plan cap is reached (duplicate and burst posts risk spam enforcement, `platforms/x-twitter.md` section 6).

## 3. Kill switch, approval and safety controls
- Kill switch: one cell (`automation_enabled`) or n8n/Make variable. Every workflow reads it at start and again immediately before any outbound call. Also provide a webhook or button that sets it to false and a documented manual step: deactivate the scenario/workflow and revoke credentials.
- Who can flip it: the owner and the approver; crisis procedure sets it first (`crisis-playbook.md` section 2).
- Approval states are audit logged: who approved, when, which version of the text (hash).
- Dry-run mode: `mode = dry` writes the would-be request to the log and sends nothing; use it for every new workflow and after changes.
- Content guards: block words list, banned topics, link domain allow-list, no raw customer data in generated posts, `needs_proof` forces human review (`compliance-and-ethics.md` section 11).
- Never auto-reply to `sensitive` or `escalate` items (`community-management.md` section 2).
- Never run bulk unsolicited DMs or WhatsApp messages; never message numbers without recorded opt-in.

## 4. Recipes
Common to all: dry-run first, kill switch read first, secrets only in the tool's credential store, every outbound call logged, humans approve outbound text.

### Recipe 1: Daily multi-platform rotation (publish)
**n8n (two workflows: Prepare, Publish)**
Prepare:
1. Schedule Trigger (daily, Africa/Cairo).
2. Google Sheets (Get rows from `config`): stop if `automation_enabled` is not true (IF node).
3. Google Sheets (Get rows from calendar) with a filter `date = tomorrow`, `status = planned`.
4. Loop Over Items (Split in Batches), one row at a time.
5. LLM node (Basic LLM Chain or HTTP Request to the model API) with a JSON-only prompt; Structured Output Parser.
6. Code node: assemble `draft.txt`; Execute Command node: `scripts/limits_check.py`; IF exit code 1: Sheets update `needs-fix` and alert; else continue.
7. Sheets update: `status = checked` plus draft fields.
8. Slack/Gmail/Telegram "Send and Wait for Response" (approval message with the final post). On approve: Sheets update `approved` with approver and timestamp; on reject or timeout: `rejected` or `expired`.
Publish:
1. Schedule Trigger (every 15 minutes) or Wait node until the row's time.
2. Config check (kill switch) then Sheets get rows `status = approved`, `time <= now`.
3. Filter: not already published (idempotency, section 5).
4. Switch by platform: HTTP Request nodes per official API (Instagram container, poll status, publish; Facebook Page post; YouTube `publishAt`; X create post; Threads container; Telegram `sendMessage`; LinkedIn `/rest/posts`; GBP `localPosts`). Pinterest/Reddit/Snapchat/TikTok (unaudited): create a ready pack and notify a person.
5. IF success: Sheets update `published` with platform id; log row. On error: Error Workflow (section 8).
**Make (two scenarios)**
Scenario A (Prepare): Scheduler (daily) > Data store/Sheets "Get config" > Filter `automation_enabled = true` > Google Sheets "Search Rows" (date = tomorrow, status = planned) > Iterator > LLM module (OpenAI or Anthropic Claude app, or HTTP) > JSON "Parse JSON" > HTTP "Make a request" to your private limits-check endpoint > Router (fail: update `needs-fix` + alert; pass: update `checked`) > Slack/Email "Create a message" containing the draft and a link. The approver sets `status = approved` in the sheet (or clicks a link that calls a Custom Webhook scenario that sets it).
Scenario B (Publish): Scheduler (every 15 minutes) > config filter > Sheets "Search Rows" (approved, due) > Iterator > Router by platform > Facebook Pages / Instagram for Business / YouTube / LinkedIn / Telegram Bot modules or HTTP "Make a request" with OAuth connection > Sheets "Update a Row" > error handler route (Break/Resume with incomplete executions enabled, then alert).
Do not: skip the approval step; publish from a stale draft (hash check); post the same text to several platforms unchanged.

### Recipe 2: Comment triage with draft replies for approval
Platforms: Instagram and Facebook comments (webhooks), YouTube comments (polling), X replies only where the API allows (`platforms/x-twitter.md` section 8).
**n8n**
1. Webhook node (Meta verification handshake plus signature check) or Schedule Trigger + HTTP (YouTube `commentThreads.list`).
2. Respond to Webhook 200 immediately; continue asynchronously.
3. Edit Fields: extract `comment_id`, text, author handle, post id, time.
4. Dedupe: Data Table/Sheets lookup by `comment_id`; stop if seen.
5. LLM classification with JSON: `tag` (ok, sensitive, escalate), `language`, `intent`, `draft_reply` using the reply library (`../templates/reply-library.md`).
6. Switch on `tag`: ok: write draft to the queue and send Slack message with Approve/Edit; sensitive: notify the owner with the comment (no draft sent); escalate: immediate alert (`community-management.md` section 9).
7. On approval (Send and Wait): HTTP POST reply (Instagram `/{comment-id}/replies`, Facebook comments, YouTube `comments.insert`); optional hide via the platform's moderation endpoint after approval.
8. Log result and time to first reply.
**Make**
Custom Webhook (or Facebook Pages "Watch Comments") > Data store "Check record" (dedupe) > LLM module > Router on tag > Slack "Create a message" with a link to an approval webhook > Webhook scenario "Approve" > HTTP/Instagram/Facebook "Create a Reply" > Data store update.
Do not: auto-post replies; reply to hidden comments through the API (not supported, `platforms/instagram.md` section 8); log customer names beyond handle.

### Recipe 3: WhatsApp or Messenger lead capture to CRM
**n8n**
1. WhatsApp Trigger (or Webhook for the WhatsApp Cloud API / Messenger `messages` events; verify signature).
2. IF message is from a new contact: check opt-in proof (the user messaged first = service conversation; marketing follow-ups need explicit opt-in recorded).
3. CRM node (HubSpot, Airtable, Google Sheets): upsert contact with `contact_id` (store the business-scoped user ID where provided; the phone number may be missing, `platforms/whatsapp.md` section 8), source, time, consent text, language.
4. Reply inside the window: acknowledgement with "talk to a human" option (free-form is allowed inside the 24 h window); if outside the window use only an approved template to an opted-in contact.
5. Create CRM task for sales with due time; notify Slack/Telegram.
6. If keyword = STOP/opt-out: set `consent = false`, confirm, stop all flows.
7. Log. No card numbers, passwords or codes requested.
Instagram comment-to-DM variant: Webhook (comment containing keyword) > Private Reply once within the allowed period > log consent and disclosure text (`platforms/instagram.md` case 10).
**Make**
Custom Webhook (WhatsApp Business Cloud or Facebook Messenger/Instagram app module) > Router (new/existing contact) > CRM module "Search/Create a Record" > WhatsApp "Send a Message" (inside window) or Template message > Slack "Create a message" > Data store (consent log).
Do not: message people who did not opt in; bulk-broadcast without templates and consent; ignore the window.

### Recipe 4: Weekly report to email or Slack
**n8n**
1. Schedule Trigger (Monday morning).
2. Per platform: HTTP Request or native node to the official analytics source (platform file section 9); where no API exists, read the manual export sheet.
3. Merge and Code node: compute week-over-week, medians, top and bottom posts, reply-time median.
4. LLM node: write insights with the formula in `analytics-and-reporting.md` section 9; pass numbers only, not customer data.
5. Gmail/Slack node: send the draft to the owner (not the client) first, with data table attached.
6. Sheets append: archive the week.
**Make**
Scheduler > Sheets "Search Rows" (data tabs) > Array aggregator > Tools "Set variables" (calculations) > LLM module > Gmail/Slack "Send a message" > Sheets "Add a row".
Do not: send LLM text to clients unread; mix platform totals.

### Recipe 5: Evergreen recycler
**n8n**
1. Schedule Trigger (weekly).
2. Sheets: published posts with `evergreen = true`, last posted over 90 days ago, performance above the median (heuristic).
3. Code: pick top N, exclude time-sensitive claims (price, date, offer) via a `needs_update` flag.
4. LLM: rewrite hook and CTA, keep facts, mark claims needing recheck.
5. limits_check; create new calendar rows with `status = planned` (not published).
6. Notify the owner with the list; the normal daily rotation and approval apply.
**Make**
Scheduler > Sheets "Search Rows" > Filter > Sorter/Iterator > LLM module > Sheets "Add a Row" (planned) > Slack message.
Do not: recycle outdated pricing or policies; recycle the same text verbatim; run recycled posts through any path that skips approval.

### Recipe 6: Mention and keyword monitor (official sources only)
Sources: official APIs you have access to (Threads keyword search after approval, X search billed per read, YouTube comments, Google Business Profile reviews via API if approved), Reddit Pro keyword tracking in its app or approved API access (`platforms/reddit.md` section 8), RSS/email alerts from official alerting products (for example Google Alerts feeds), Meta webhooks for tags and mentions on your own accounts. No scraping, no logged-in crawlers, no unofficial APIs.
**n8n**
1. Schedule Trigger (hourly or daily) or RSS Feed Read Trigger.
2. HTTP Request nodes to each permitted source; respect cost and rate limits (X is paid per read: daily, not per minute).
3. Dedupe by URL/id.
4. LLM node: classify topic, sentiment, risk (ok, sensitive, escalate), language; summarise in one line.
5. Switch: escalate: instant alert to owner; others: append to a digest sheet.
6. Daily Slack/email digest (top mentions, counts, sentiment trend).
**Make**
RSS "Watch RSS feed items" / HTTP "Make a request" > Data store dedupe > LLM module > Router > Slack/Email modules > Sheets row.
Do not: reply automatically; join conversations as a bot; store personal data beyond handle and link; use results for profiling individuals.

## 5. Idempotency and duplicates
- Key: `post_id = YYYYMMDD-platform-slot`. Before any publish call, look up the log: if status is `published` or `in-flight` stop.
- Write `in-flight` with a timestamp before calling the API; write `published` with the platform object id after. A row stuck `in-flight` over 15 minutes goes to a human, not an automatic retry (the post may exist).
- Multi-step publishes (Instagram/Threads container then publish, YouTube resumable upload): store the container or upload id so a retry resumes instead of creating a second object. Instagram containers expire after 24 h (`platforms/instagram.md` section 8).
- Webhook events repeat: dedupe by event or comment id (Recipes 2 and 3).
- Duplicate or near-duplicate posts risk spam enforcement (`platforms/x-twitter.md` section 6); the cadence guard in section 2 prevents bursts.
- Content hash: store a hash of the approved text; publish only if the hash equals the current row (stops publishing edited or stale text).

## 6. Rate limits and queues
- Treat the numbers in each platform file as ceilings to stay well under; read live counters where offered; stop at about 80%.
- One queue per platform and account; sequence calls with Wait nodes (n8n) or sleep modules (Make); spread bulk jobs over time.
- On 429 or quota errors: honour `retry_after` or reset headers, then exponential backoff with jitter, maximum 3 attempts, then alert.
- Never rotate apps or tokens to bypass limits (`platforms/x-twitter.md` section 8, `platforms/pinterest.md` section 8).

## 7. Secrets handling
- Store tokens, client secrets, webhook secrets and API keys only in n8n credentials, Make connections or a secret manager. Never in prompts, LLM inputs, workflow JSON exports, sheets, Notion pages, chat messages, screenshots or Git repos.
- Export workflows without credentials; scan exports before sharing; keep a `.gitignore` for env files.
- Least privilege: request only the permissions needed (platform files section 8 list them); separate test and production apps and accounts.
- Token lifetimes: Meta long-lived tokens 60 days and refreshable, LinkedIn tokens 60 days without partner refresh tokens, Threads tokens refreshed monthly (`platforms/instagram.md`, `platforms/linkedin.md`, `platforms/threads.md` section 8). Put expiry reminders in the calendar and alert on auth errors.
- Rotate secrets after staff changes or any incident (`crisis-playbook.md` section 5, hacked account).
- Redact logs: no tokens, no phone numbers, no message bodies where not needed.
- LLM calls: send only the brief, brand facts and public data; no customer messages beyond what a triage step needs, and use a provider and plan whose data terms you accepted (`compliance-and-ethics.md` section 6).

## 8. Error handling and alerts
| Error class | Example | Action |
|---|---|---|
| Auth | expired token, revoked permission | stop that platform, alert owner, re-authorise manually |
| Rate/quota | 429, quota exceeded, publishing cap | wait and retry per section 6; push remaining rows to next slot |
| Validation | caption too long, wrong ratio, unsupported media | mark `needs-fix`, alert, no retry |
| Media processing | container `ERROR` or `EXPIRED` | recreate once, then alert |
| Policy | restriction notice, flagged post | set kill switch, follow platform case in `crisis-playbook.md` section 6 |
| Network/5xx | timeout | retry max 3 with backoff; check whether the post exists before retrying |
| Logic | LLM returns invalid JSON | retry once with stricter prompt, then `needs-fix` |
Alert content: post id, platform, error code and text (no secrets), what was or was not published, who acts, link to the execution. Channels: Slack, Telegram or email to at least two people. Use the n8n Error Trigger workflow or Make error handler routes plus a daily heartbeat so a silent failure is noticed. Review the failure log weekly; fix causes, not symptoms.

## 9. When to stop automating
Stop (or do not start) when:
- the platform has no official route or forbids it (section 1); manual or native scheduling is the answer;
- every item needs a human decision anyway (Pinterest per-Pin choice, Reddit, sensitive replies);
- volume is low (a few posts a week): a calendar and manual posting is cheaper than maintaining workflows;
- the account has a warning, restriction or open crisis: stop all automation first (platform cases, `crisis-playbook.md`);
- failure rate stays high or the workflow changes meaning (hallucinated facts, wrong language);
- maintenance cost exceeds time saved, or API cost per task is higher than a person (X per-use fees, `platforms/x-twitter.md` section 8).
Review each workflow quarterly: still needed, still compliant, still within limits.

## 10. Related skills and hand-offs
- `n8n-agent-studio`: builds n8n workflows, browser recipes and agents from these specs; `automation-studio`: builds automations in other tools. Give them: recipe, platform files, limits, approval and kill-switch requirements.
- `media-buying`: paid promotion; `marketing-studio`: strategy, SEO, email.
- `scripts/calendar_gen.py` produces the calendar CSV the rotation reads; `scripts/limits_check.py` and `scripts/utm.py` are the two helper steps.

## 11. Sources
- Platform files section 8 and 6 (each lists its official sources and `Last verified`); no new facts were added here.
- Node and module names are descriptive and must be checked in the tool version used.
