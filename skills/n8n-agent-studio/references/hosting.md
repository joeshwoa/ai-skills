# Where things run — local, published, or both

Three parts: **n8n** (the brain), **browserd** (the hands, needs a real/headless Chrome + saved logins), **the sinks** (Sheets, DB, Slack…). n8n must be able to reach browserd.

| Setup | n8n | browserd | Good for | Catch |
|---|---|---|---|---|
| **A · All local** (Mac) | `setup_n8n.sh --start` (localhost:5678) | `nx start --allow …` (127.0.0.1:7788) | personal automations, logins done in your own window, free | runs only while the Mac is awake; webhooks from the internet need a tunnel |
| **B · All on one server** | docker compose (deploy/) | container beside n8n | always-on, team, schedules | logins must be done *on the server* (VNC/`--headed` via X, or attach mode through an SSH tunnel to your Chrome); captcha sites → human-in-loop |
| **C · n8n Cloud/VPS + browserd on your Mac** | cloud | local, reachable via authenticated tunnel (Cloudflare Tunnel / Tailscale funnel) with `--token` | you want cloud schedules but your own logged-in Chrome | Mac must be on; tunnel = attack surface → token + allow-list + IP rules |
| **D · local n8n + published bits** | local | local | develop & test locally, publish only the webhook endpoint (tunnel) | keep production off dev laptop |
| **E · Flow published, browser step by API** | cloud | a hosted browser service (Browserbase/Browserless-type) | no server of your own | third party sees the sessions — only for non-sensitive sites; check ToS |

Decision hints: needs the user's personal logged-in session → A or C (attach). Always-on + shared → B. Sensitive accounts → keep sessions on a machine you control (A/B), not a third party (E).

## Local (A)
```bash
bash ../automation-studio/scripts/setup_n8n.sh --yes && bash ../automation-studio/scripts/setup_n8n.sh --start     # n8n on :5678
pip install playwright && python3 -m playwright install chromium                                                 # once
bash scripts/nx.sh start --allow supplier-portal.com                                                             # browserd on :7788
bash scripts/nx.sh login https://supplier-portal.com/login --session supplier                                    # you sign in, close window
```
Make it survive reboots: macOS `launchd` plist (RunAtLoad) running `nx.sh start …`; Linux systemd user unit. n8n flow URL: `http://127.0.0.1:7788/run`.

## Docker (B) — `deploy/docker-compose.yml`
`cp deploy/.env.example deploy/.env` → edit → `docker compose -f deploy/docker-compose.yml up -d`. n8n reaches `http://browserd:7788` (add a Header Auth credential `Authorization: Bearer $NX_TOKEN` to the HTTP Request node).
(YAML validated; the images were not run in this sandbox — test with `docker compose config` then a dry run.) HTTPS: Caddy/Cloudflare Tunnel in front of 5678. Backups: Postgres dump + `n8n` volume + `bd` volume.
First login on a server: run `docker compose run --rm -e DISPLAY… browserd` headed over X forwarding/VNC, or use attach mode (SSH `-R 9222:127.0.0.1:9222` to your own Chrome) — then keep the session volume.

## Tunnel for C (sketch)
`cloudflared tunnel --url http://127.0.0.1:7788` (or a named tunnel + Access policy). browserd needs `--token` when not loopback; add the token as an n8n credential. Rotate it if the URL leaks.

## Deploying flows
`bash scripts/nx.sh deploy flow/flow.json --target local --activate` (automation-studio engine; targets `local`, self-hosted URL, or `cloud`; API keys in `automation-secrets.json`). In published n8n change the HTTP node URL via an environment variable or a *Set* config node, not by editing code.

## Schedules & reliability
Schedule Trigger → browserd call → IF ok → … ; *Retry on fail* 2× with wait; error workflow → alert with screenshot; keep recipes idempotent; jitter times (don't hit at :00 exactly); keep run history 30 days; one Chrome profile = one run at a time.
