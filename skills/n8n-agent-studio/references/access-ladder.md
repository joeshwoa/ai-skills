# The access ladder — how to automate something that "has no API"

Rule: **take the highest rung that works.** Each rung down is slower, costlier and breaks more often.

## 1 · Native n8n node (570 node types) — `nx nodes <app>` (alias of auto.sh nodes)
Search before anything else; also check `n8n-nodes-*` community nodes and the app's own "n8n" integration page.

## 2 · Official API / webhooks
"No API" is often wrong: look for **Developers / API / Integrations / Webhooks** in the app's settings and footer, `/api`, `/graphql`, `/openapi.json`
(`nx probe` tries these). Many apps hide API access on a higher plan — ask the user whether upgrading beats maintaining a scraper.

## 3 · The app pushes to you
Scheduled report emails (n8n *Email Trigger (IMAP)* parses attachments), CSV/Excel export + schedule, RSS/Atom, calendar `.ics`, Zapier-style "outgoing webhook" in settings,
"forward to address" inboxes, Google Sheets sync, Slack/Teams notifications → n8n triggers.

## 4 · The site's own JSON API ("hidden API") — the sweet spot
The front-end of every SPA calls a JSON API. Replaying it is 100× lighter than a browser.
How to find it:
- **With Claude in Chrome:** open the site in the user's browser, do the task by hand once, then `read_network_requests` (filter XHR/fetch) and `read_page` / `javascript_tool` for the request headers & bodies.
- **By hand:** DevTools → Network → Fetch/XHR → do the action → right-click request → *Copy as cURL* → paste → n8n *HTTP Request → Import cURL*.
Check: auth (cookie? `Authorization: Bearer`? CSRF header/cookie pair?), pagination (`page`, `cursor`, `limit`), rate limits, whether the token expires (refresh call?).
Get the session cookie/token **without handling the password**: `nx login URL --session s`, then a recipe step `cookies`/`eval`-free: easier is to let browserd do the call: recipe with `goto` the API URL
and `text`/`extract` on the JSON, or run the whole thing in the page context. If the token is short-lived, keep browserd in the loop (recipe refreshes it).
Be polite: same rate as a human, cache, no parallel hammering. Stay inside what the user is allowed to access.

## 5 · JSON embedded in the HTML
`__NEXT_DATA__`, `window.__INITIAL_STATE__`, `application/ld+json`: HTTP Request (HTML) → Code node `JSON.parse`. `nx probe` lists which exist.

## 6 · Browser recipe (browserd) — deterministic, cheap
Use when you must click: logins, wizards, downloads, uploads, content only built by JS. Detailed in `browser-recipes.md`.

## 7 · Attach to the user's real Chrome (CDP)
When the user's own logged-in state matters (SSO, device-bound cookies, extension). Dedicated Chrome profile with `--remote-debugging-port` (`nx chrome` prints the command).
Treat the port as full control of that browser: loopback only.

## 8 · LLM browser agent (observe → act)
For unknown/changing UIs and one-off research. Costs tokens, can wander, can be prompt-injected → allow-list + step cap + approvals + freeze to a recipe when it works.

## 9 · Desktop / screen automation
Only for apps with no web surface. Needs the user's machine and supervision; not for unattended production.

## 10 · Human in the loop
The machine does everything up to the step a human must do (captcha, SMS, bank confirmation, "are you sure?"), n8n *Wait* (resume URL) / Telegram-Slack approve button, then continues with the saved session.

## Scoring factors `nx ladder` uses
API/OpenAPI found (+), feeds/exports (+), embedded JSON (+), SPA (hidden JSON ↑), login (recipe/attach ↑), high frequency (agent ↓), large volume (browser ↓),
captcha/WAF (all browser routes ↓↓, human ↑↑), ToS/robots forbid (all scraping ↓↓↓). Always read its "why" lines to the user.
