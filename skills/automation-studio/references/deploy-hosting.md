# Where n8n runs — local, Docker, self-hosted server, n8n Cloud

All four expose the same editor and the same public REST API (`/api/v1`, header `X-N8N-API-KEY`), so
`auto.sh deploy/list/trigger/executions` work with any of them — only the target URL + key differ.

| Option | Cost | Good for | API for deploy |
|---|---|---|---|
| Local on the Mac (`setup_n8n.sh`) | free | building, testing, personal automations while the Mac is on | yes |
| Docker on the Mac/PC | free | same, isolated; easy upgrades | yes |
| Self-hosted VPS (Docker + HTTPS) | server ~$5–20/mo | 24/7 production, webhooks from the internet, full control | yes |
| n8n Cloud | paid plans (Starter/Pro/Enterprise; priced per executions/month) | 24/7 with zero ops | **paid plans only — not in the free trial** |

The user currently has no n8n subscription → default: **local on the Mac**; production later on a VPS or Cloud.
Webhooks from internet services need a public HTTPS URL → VPS/Cloud, or a tunnel for development
(`cloudflared tunnel --url http://localhost:5678`, then set `WEBHOOK_URL` to the tunnel URL).

## Local on the Mac (no sudo, no Docker)
```
bash scripts/setup_n8n.sh          # asks, then: Node 24 (checksum-verified) + n8n → ~/.local/share/ai-skills/n8n
bash scripts/setup_n8n.sh --start  # http://localhost:5678 (data in …/n8n/data, logs …/n8n/n8n.log)
bash scripts/setup_n8n.sh --stop | --status | --logs | --update
```
Then the user (not the AI): opens the URL → creates the owner account → Settings → n8n API → Create an API
key → pastes it into `~/.config/ai-skills/automation-secrets.json` → `"n8n_api_keys": {"local": "…"}` →
`auto.sh doctor` shows the target. Start at login (optional): System Settings → General → Login Items → add a
small script that runs `setup_n8n.sh --start`, or use the Docker option with `--restart unless-stopped`.

## Docker (Mac/PC/server)
```
docker volume create n8n_data
docker run -d --name n8n -p 5678:5678 -e GENERIC_TIMEZONE=Africa/Cairo -e TZ=Africa/Cairo \
  -v n8n_data:/home/node/.n8n --restart unless-stopped docker.n8n.io/n8nio/n8n
```
(`setup_n8n.sh --docker` runs this after asking.) Upgrade: `docker pull docker.n8n.io/n8nio/n8n && docker rm -f n8n` and run again (data stays in the volume).

## Self-hosted production (VPS) — docker compose + Postgres + automatic HTTPS
```yaml
# docker-compose.yml   (domain: n8n.example.com → A record to the server IP)
services:
  caddy:
    image: caddy:2
    ports: ["80:80", "443:443"]
    volumes: ["./Caddyfile:/etc/caddy/Caddyfile", "caddy_data:/data"]
    restart: unless-stopped
  postgres:
    image: postgres:16
    environment: { POSTGRES_USER: n8n, POSTGRES_PASSWORD: ${PG_PASSWORD}, POSTGRES_DB: n8n }
    volumes: ["pg_data:/var/lib/postgresql/data"]
    restart: unless-stopped
  n8n:
    image: docker.n8n.io/n8nio/n8n
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: ${PG_PASSWORD}
      DB_POSTGRESDB_DATABASE: n8n
      N8N_HOST: n8n.example.com
      N8N_PROTOCOL: https
      WEBHOOK_URL: https://n8n.example.com/
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}      # back this up — without it credentials can't be decrypted
      GENERIC_TIMEZONE: Africa/Cairo
      EXECUTIONS_DATA_PRUNE: "true"
      EXECUTIONS_DATA_MAX_AGE: "336"                 # hours (14 days)
      N8N_DEFAULT_BINARY_DATA_MODE: filesystem
      N8N_RUNNERS_ENABLED: "true"
    volumes: ["n8n_data:/home/node/.n8n"]
    depends_on: [postgres]
    restart: unless-stopped
volumes: { caddy_data: {}, pg_data: {}, n8n_data: {} }
```
`Caddyfile`: `n8n.example.com { reverse_proxy n8n:5678 }`. Secrets in a `.env` next to the compose file
(the user generates them: `openssl rand -hex 32`). The AI can prepare these files; the user (or the AI with
explicit permission, via the user's SSH) runs them on the server.

### Scaling: queue mode
For high volume: `EXECUTIONS_MODE=queue`, add Redis (`QUEUE_BULL_REDIS_HOST`), run extra `n8n worker`
containers (same image, `command: worker`, same env + encryption key), optionally webhook processors
(`n8n webhook`). Postgres required. Workers scale horizontally.

## n8n Cloud
User signs up at n8n.io (the AI never does). Instance URL `https://<name>.app.n8n.cloud`. API keys only on
paid plans. `$env` is blocked on Cloud — use Variables (`$vars`, Pro+) or credentials. Target:
`{"targets": {"cloud": {"url": "https://<name>.app.n8n.cloud"}}}` + `n8n_api_keys.cloud` in the secrets file.

## Deploying with the toolkit
```
auto.sh deploy flow.json --target local                 # create, or update the workflow with the same name
auto.sh deploy flow.json --target cloud --activate      # ask the user before activating production
auto.sh list --target cloud · auto.sh pull --target cloud --id ID -o flow.json
```
- Activation fails with a clear message when a node has no credential or a trigger needs setup — fix in the UI or `creds --apply`.
- Sub-workflow references `name:<workflow name>` are resolved to ids at deploy (deploy children first).
- `deploy` writes `<flow>.deployed.json` (target, id, URL) next to the file.
- Versioning: keep `flow.ts`, `flow.json`, `cases.json` in git; deploy from git; `pull` before editing in the UI
  to avoid overwriting UI changes.

## Backups & migration
- Workflows: `n8n export:workflow --all --output=backups/ --separate` (or `auto.sh pull` each).
- Credentials: `n8n export:credentials --all --output=creds.json` (encrypted with the instance key); move the
  `N8N_ENCRYPTION_KEY` with them. Never commit credentials or the key.
- Move local → server: export on the Mac, `n8n import:workflow --separate --input=backups/` on the server,
  recreate or import credentials, re-activate.

## Security checklist (production)
HTTPS only · strong owner password + 2FA · webhook authentication on anything that writes · least-privilege
app scopes · separate test/prod credentials · prune execution data with PII · keep n8n updated
(`setup_n8n.sh --update` / `docker pull`) · encryption key backed up offline · restrict who can create
Code/Execute Command nodes (`NODES_EXCLUDE` to disable risky nodes).
