# Connecting "any app" — decision card

For every app ask in this order: (1) n8n node? (2) public API / webhooks? (3) export/email/RSS? (4) hidden JSON? (5) browser. Verify with `nx nodes <name>` and `nx probe <url>`; docs change, never rely on memory for limits/prices.

| Kind of app | Usual best route | Notes |
|---|---|---|
| Google (Sheets, Drive, Gmail, Calendar) | native nodes, OAuth credential | user creates the Google Cloud OAuth client — steps in `automation-studio/references/credentials.md` |
| Microsoft 365, Slack, Notion, Airtable, HubSpot, Stripe, Shopify, WooCommerce, Telegram | native nodes | |
| WhatsApp | WhatsApp Business Cloud API node (official). Personal WhatsApp Web automation violates ToS/ban risk → don't; offer Telegram/Business API | |
| Facebook/Instagram/TikTok/LinkedIn | official APIs are limited; posting via Graph API/partner tools; scraping is against ToS → export, official API, or a human step | |
| Local ERPs (Odoo etc.) | their JSON-RPC/REST API | self-hosted ones usually have API even if the UI is the only thing the user knows |
| Banks / payment portals | **do not automate logins or money movement.** Use statements by email/export or an open-banking/PSP API; human approves anything that moves money | |
| Government/utility portals, supplier portals, courier tracking pages | recipe (login once by human) or their export; respect captcha → human-in-loop | |
| Web dashboards of SaaS without API | hidden JSON → recipe | |
| Legacy desktop software | its CLI/DB/files first; export folder watcher (Local File Trigger) ; then computer-use | |
| Email-only systems | IMAP trigger + parse (Code / AI extraction) | very robust |
| Spreadsheets/CSV on disk | Local File Trigger / Read Binary Files + Spreadsheet File | local n8n only |
| Anything with MCP server | MCP Client Tool | check what authority it gets |

## Pairing an app with an *agent*
Expose each app capability as a tool with a narrow description (`get_order(id)`, `create_draft_reply(thread,text)`) via sub-workflows; the agent chooses tools, the sub-workflow validates & logs. Read tools free; write tools behind approval.
