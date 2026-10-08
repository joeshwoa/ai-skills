# Credentials — what the USER does, step by step

The AI never creates accounts, signs in with passwords, or generates/reads keys on websites. It tells the
user exactly what to click, then the user either:
- **A. connects the credential in the n8n editor** (open the node → Credential → Create new → paste/sign in), or
- **B. pastes the values into `~/.config/ai-skills/automation-secrets.json`** and the AI runs
  `auto.sh creds flow.json --apply --target T` (creates the credential through the API and wires it into the
  nodes; values are never printed). OAuth2 apps (Google, Microsoft, Slack OAuth) must use **A** — the browser
  consent can't be done from a file.

Secrets file (chmod 600, never committed, never shown in chat):
```json
{"n8n_api_keys": {"local": "<n8n API key>", "cloud": ""},
 "credentials": {
   "Telegram bot": {"type": "telegramApi", "data": {"accessToken": "123456:ABC…"}},
   "OpenAI":       {"type": "openAiApi",   "data": {"apiKey": "sk-…"}},
   "Shop DB":      {"type": "postgres",    "data": {"host": "…", "port": 5432, "database": "…", "user": "…", "password": "…", "ssl": "require"}}
 }}
```
Field names of any type: `auto.sh creds --schema <type> --target local` (`*` = required). Verified fields:
telegramApi `accessToken*` · openAiApi `apiKey*` · anthropicApi `apiKey*` · googlePalmApi (Gemini) `apiKey*` ·
slackApi `accessToken*` (+ `signatureSecret`) · httpHeaderAuth `name`, `value` · notionApi `apiKey*` ·
airtableTokenApi `accessToken` · postgres `host, database, user, password, port, ssl` · whatsAppApi
`accessToken*, businessAccountId*` · smtp `user, password, host, port, secure` · hubspotAppToken `appToken` ·
discordBotApi `botToken*` · stripeApi `secretKey` (+ `signatureSecret`) · supabaseApi `host, serviceRole`.

n8n shows each credential's own docs link (ⓘ in the credential window) and the **OAuth Redirect URL** to paste
into the provider — local: `http://localhost:5678/rest/oauth2-credential/callback`.

## Google (Sheets, Gmail, Drive, Calendar, Docs) — OAuth2 (method A)
1. console.cloud.google.com → top bar project picker → **New project** (e.g. "n8n").
2. **APIs & Services → Library** → enable each API you need (Google Sheets API, Gmail API, Google Drive API, Google Calendar API).
3. **Google Auth Platform / OAuth consent screen** → Get started → app name, support email → Audience
   **External** → contact email → Create. Under **Audience → Test users** add your own Gmail.
4. **Clients → Create client** → type **Web application** → Authorized redirect URIs → paste n8n's OAuth
   Redirect URL (local: `http://localhost:5678/rest/oauth2-credential/callback`) → Create → copy **Client ID**
   and **Client secret**.
5. In n8n: credential "Google Sheets OAuth2 API" (or Gmail OAuth2…) → paste ID + secret → **Sign in with
   Google** → choose the account → allow (the "unverified app" warning is expected for your own app: Advanced → continue).
Tip: one OAuth client works for all Google credentials. Server-to-server alternative: Service Account (JSON key)
+ share the sheet with the service-account email (credential type `googleApi`).

## Telegram bot
1. In Telegram open **@BotFather** → `/newbot` → name → username ending in `bot` → copy the **token**.
2. Chat id: send any message to your bot, then open `https://api.telegram.org/bot<TOKEN>/getUpdates` in the
   browser and read `message.chat.id` (groups: add the bot, send a message, id starts with `-`).
3. Token → credential `telegramApi.accessToken`; chat id → workflow (env `TELEGRAM_CHAT_ID` or the node field).

## Slack
1. api.slack.com/apps → **Create New App → From scratch** → name + workspace.
2. **OAuth & Permissions → Bot Token Scopes**: `chat:write` (+ `channels:read`, `chat:write.public`,
   `files:write`, `users:read` as needed) → **Install to Workspace** → Allow → copy **Bot User OAuth Token** (`xoxb-…`).
3. In Slack invite the bot to the channel: `/invite @YourApp`.
4. Credential `slackApi.accessToken` = the xoxb token. Slack Trigger also needs the **Signing Secret** (Basic Information).

## OpenAI / Anthropic / Google Gemini / local models
- OpenAI: platform.openai.com → Settings → **Billing** (add credit) → **API keys → Create new secret key** → copy once.
- Anthropic: console.anthropic.com → **API Keys → Create Key** (needs credit in Billing).
- Gemini: aistudio.google.com → **Get API key → Create API key** (free tier available) → credential "Google Gemini(PaLM) API".
- Free/local: Ollama on the Mac (`ollama pull llama3.1`) → n8n "Ollama" credential, base URL `http://localhost:11434`.
Set a monthly spend limit in the provider's billing page.

## WhatsApp (Cloud API, Meta)
1. developers.facebook.com → **My Apps → Create app** → type Business → add product **WhatsApp**.
2. **WhatsApp → API Setup**: note **Phone number ID** and **WhatsApp Business Account ID**; add your phone as a test recipient.
3. Permanent token: business.facebook.com → **Settings → Users → System users** → Add (admin) → **Generate
   token** for the app with `whatsapp_business_messaging`, `whatsapp_business_management` → copy.
4. Credential `whatsAppApi`: accessToken + businessAccountId. The WhatsApp Trigger uses a separate OAuth
   credential (App ID + App Secret from App settings → Basic) and needs a public HTTPS n8n URL.

## Notion
notion.so/profile/integrations → **New integration** → Internal → workspace → copy the **Internal Integration
Secret** → open the target page/database → ⋯ → **Connections → Add** your integration. Credential `notionApi.apiKey`.

## Airtable
airtable.com/create/tokens → **Create token** → scopes `data.records:read`, `data.records:write`,
`schema.bases:read` → add the bases → Create → copy. Credential `airtableTokenApi.accessToken`.

## HubSpot
Settings → Integrations → **Private Apps → Create** → scopes (crm.objects.contacts.read/write …) → Create →
copy the access token → credential `hubspotAppToken.appToken`.

## Postgres / Supabase / MySQL
Host, port, database, user, password (Supabase: Project Settings → Database → Connection string → use the
pooler host/port; or the Supabase node with Project URL + service_role key — server side only). Create a
dedicated DB user with only the needed tables.

## Email
- Gmail node → Google OAuth (above). Plain SMTP with Gmail: Google Account → Security → 2-Step Verification on →
  **App passwords** → create → SMTP `smtp.gmail.com:465` secure, user = address, password = the app password.
- Outlook/Microsoft 365: Microsoft OAuth (Azure portal → App registrations → New → redirect URL from n8n →
  Certificates & secrets → new client secret; API permissions Mail.Send, etc.).

## Stripe / payment webhooks
Dashboard → Developers → **API keys** → create a **restricted key** with only what the flow needs → credential
`stripeApi.secretKey`. Webhooks: Developers → Webhooks → add endpoint (production n8n URL) → copy the
**signing secret** → verify signatures in the flow; idempotency on `event.id` (pattern 08).

## Discord
discord.com/developers/applications → New Application → **Bot → Reset Token** → copy → invite with OAuth2 URL
Generator (scope `bot`, permissions Send Messages). Simple alternative: channel Settings → Integrations →
**Webhooks** → New → copy URL (use HTTP Request, no credential needed; keep the URL secret).

## Webhook authentication for your own n8n webhooks
Create credential **Header Auth** (`name`: `X-API-Key`, `value`: a long random string the user generates,
e.g. `openssl rand -hex 24`) → select it in the Webhook node (Authentication: Header Auth) → give the sender the header.

## Make / Zapier / others
Each platform stores its own connections; the user connects apps inside that platform's editor. The AI
provides the module list and mappings (`platforms.md`) and never handles those passwords.
