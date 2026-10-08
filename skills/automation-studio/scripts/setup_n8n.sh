#!/usr/bin/env bash
# automation-studio · install / run a private local n8n (macOS or Linux) — no account, no subscription.
#
#   bash setup_n8n.sh            install portable Node 24 + n8n into ~/.local/share/ai-skills/n8n (asks first)
#   bash setup_n8n.sh --start    start the local n8n server  → http://localhost:5678   (--stop, --status, --logs)
#   bash setup_n8n.sh --docker   run n8n in Docker instead (needs Docker Desktop)
#   bash setup_n8n.sh --update   update n8n to the latest version (keeps your data)
#   flags: --yes (don't ask), --version X.Y.Z (pin n8n), --port 5678
#
# Nothing is installed system-wide and nothing needs sudo. Your workflows/credentials live in
# ~/.local/share/ai-skills/n8n/data (back it up). The AI never creates the owner account or API keys:
# after --start YOU open the editor, create the owner, then Settings → n8n API → Create API key and
# paste it into ~/.config/ai-skills/automation-secrets.json under n8n_api_keys.local.
set -euo pipefail

DIR="${AUTOKIT_N8N_DIR:-$HOME/.local/share/ai-skills/n8n}"
CFG_DIR="$HOME/.config/ai-skills"
CFG="$CFG_DIR/automation.json"
PORT=5678; PORT_SET=0; YES=0; ACTION=install; N8N_VERSION="latest"
while [ $# -gt 0 ]; do
  case "$1" in
    --yes|-y) YES=1;; --start) ACTION=start;; --stop) ACTION=stop;; --status) ACTION=status;; --logs) ACTION=logs;;
    --docker) ACTION=docker;; --update) ACTION=update;; --port) PORT="$2"; PORT_SET=1; shift;; --version) N8N_VERSION="$2"; shift;;
    -h|--help) sed -n 2,16p "$0"; exit 0;;
    *) echo "unknown option $1"; exit 2;;
  esac; shift
done
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ "$PORT_SET" = 0 ] && [ -f "$CFG" ]; then   # reuse the port saved at install time
  PORT=$(python3 -c 'import json,sys,re; u=json.load(open(sys.argv[1])).get("targets",{}).get("local",{}).get("url",""); m=re.search(r":(\d+)$",u); print(m.group(1) if m else 5678)' "$CFG")
fi
say() { printf '\033[1m%s\033[0m\n' "$*"; }
ask() { [ "$YES" = 1 ] && return 0; read -r -p "$1 [y/N] " a; [[ "$a" =~ ^[Yy] ]]; }
NODE="$DIR/node/bin/node"; NPM="$DIR/node/bin/npm"
export PATH="$DIR/node/bin:$PATH"

write_config() {
  mkdir -p "$CFG_DIR"
  python3 - "$CFG" "$DIR" "$NODE" "$PORT" <<'EOF'
import json, sys, os
p, d, node, port = sys.argv[1:]
c = json.load(open(p)) if os.path.exists(p) else {}
c["n8n_dir"], c["node"] = d, node
c.setdefault("targets", {}).setdefault("local", {})["url"] = f"http://localhost:{port}"
json.dump(c, open(p, "w"), indent=2)
print("config →", p)
EOF
  python3 "$HERE/autokit.py" doctor >/dev/null 2>&1 || true   # also creates the secrets template (chmod 600)
}

install_node() {
  [ -x "$NODE" ] && "$NODE" -e 'process.exit(+process.versions.node.split(".")[0] >= 24 ? 0 : 1)' && { say "Node $("$NODE" -v) already installed"; return; }
  local os arch plat ver tmp
  os=$(uname -s); arch=$(uname -m)
  case "$os-$arch" in
    Darwin-arm64) plat=darwin-arm64;; Darwin-x86_64) plat=darwin-x64;;
    Linux-x86_64) plat=linux-x64;; Linux-aarch64|Linux-arm64) plat=linux-arm64;;
    *) echo "unsupported platform $os-$arch — install Node 24 yourself and set AUTOKIT_NODE"; exit 1;;
  esac
  ver=$(curl -fsSL https://nodejs.org/dist/index.json | python3 -c 'import json,sys; print(next(r["version"] for r in json.load(sys.stdin) if r["version"].startswith("v24.")))')
  tmp=$(mktemp -d)
  say "Downloading Node $ver ($plat) …"
  curl -fL --progress-bar -o "$tmp/node.tar.gz" "https://nodejs.org/dist/$ver/node-$ver-$plat.tar.gz"
  curl -fsSL -o "$tmp/SHASUMS256.txt" "https://nodejs.org/dist/$ver/SHASUMS256.txt"
  local want got
  want=$(grep " node-$ver-$plat.tar.gz\$" "$tmp/SHASUMS256.txt" | awk '{print $1}')
  got=$( (command -v shasum >/dev/null && shasum -a 256 "$tmp/node.tar.gz" || sha256sum "$tmp/node.tar.gz") | awk '{print $1}')
  [ "$want" = "$got" ] || { echo "checksum mismatch — aborting"; exit 1; }
  mkdir -p "$DIR/node"; tar -xzf "$tmp/node.tar.gz" -C "$DIR/node" --strip-components=1; rm -rf "$tmp"
  say "Node $("$NODE" -v) ✓ (checksum verified)"
}

install_n8n() {
  mkdir -p "$DIR"; cd "$DIR"
  [ -f package.json ] || echo '{"name":"ai-skills-n8n","private":true}' > package.json
  say "Installing n8n@$N8N_VERSION (a few minutes the first time) …"
  "$NPM" install "n8n@$N8N_VERSION" --no-audit --no-fund --loglevel=error
  say "n8n $("$NODE" node_modules/n8n/bin/n8n --version 2>/dev/null | tail -1) ✓"
}

pidfile="$DIR/n8n.pid"; logfile="$DIR/n8n.log"
running() { [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; }

case "$ACTION" in
  install|update)
    say "This installs a private copy of Node 24 + n8n into $DIR (~600 MB, no sudo, nothing system-wide)."
    ask "Continue?" || { echo "cancelled"; exit 0; }
    install_node; install_n8n; write_config
    say "Done. Next:  bash $0 --start"
    ;;
  start)
    [ -x "$NODE" ] && [ -d "$DIR/node_modules/n8n" ] || { echo "not installed — run: bash $0"; exit 1; }
    if running; then say "already running (pid $(cat "$pidfile")) → http://localhost:$PORT"; exit 0; fi
    mkdir -p "$DIR/data"
    N8N_USER_FOLDER="$DIR/data" N8N_PORT="$PORT" N8N_DIAGNOSTICS_ENABLED=false N8N_PERSONALIZATION_ENABLED=false \
    N8N_LISTEN_ADDRESS="${N8N_LISTEN_ADDRESS:-127.0.0.1}" N8N_RUNNERS_BROKER_PORT=$((PORT + 1)) \
    N8N_RUNNERS_ENABLED=true N8N_SECURE_COOKIE=false GENERIC_TIMEZONE="${TZ:-Africa/Cairo}" \
      nohup "$NODE" "$DIR/node_modules/n8n/bin/n8n" start >"$logfile" 2>&1 &
    echo $! > "$pidfile"
    for _ in $(seq 1 60); do curl -fs "http://localhost:$PORT/healthz" >/dev/null 2>&1 && break; sleep 2; done
    if curl -fs "http://localhost:$PORT/healthz" >/dev/null 2>&1; then
      say "n8n is running → http://localhost:$PORT   (logs: $logfile)"
      cat <<EOF

First time only — do these yourself in the browser (the AI does not create accounts or keys):
  1. Open http://localhost:$PORT and create the owner account (email + password, stays on this Mac).
  2. Settings (bottom-left) → n8n API → Create an API key → label "ai-skills", no expiry → copy it.
  3. Open ~/.config/ai-skills/automation-secrets.json and paste it:
       "n8n_api_keys": { "local": "PASTE-HERE" }
  4. Check:  bash $HERE/auto.sh doctor     (shows local ✓)
EOF
      [ "$(uname -s)" = Darwin ] && open "http://localhost:$PORT" 2>/dev/null || true
    else
      echo "n8n did not come up — last log lines:"; tail -20 "$logfile"; exit 1
    fi
    ;;
  stop)   running && kill "$(cat "$pidfile")" && rm -f "$pidfile" && say "stopped" || say "not running";;
  status) running && say "running (pid $(cat "$pidfile")) → http://localhost:$PORT" || say "not running";;
  logs)   tail -n 80 "$logfile";;
  docker)
    command -v docker >/dev/null || { echo "Docker not found — install Docker Desktop, or use the default install (no Docker needed)"; exit 1; }
    say "Will run: docker run -d --name n8n -p $PORT:5678 -v n8n_data:/home/node/.n8n --restart unless-stopped docker.n8n.io/n8nio/n8n"
    ask "Start the n8n container?" || exit 0
    docker volume create n8n_data >/dev/null
    docker run -d --name n8n -p "$PORT:5678" -e GENERIC_TIMEZONE="${TZ:-Africa/Cairo}" -e N8N_SECURE_COOKIE=false \
      -v n8n_data:/home/node/.n8n --restart unless-stopped docker.n8n.io/n8nio/n8n
    say "→ http://localhost:$PORT  (then create the owner + API key as in --start)"
    say "Tests/validation still need the local copy:  bash $0   (or: AUTOKIT_N8N_DIR pointing at any n8n install)"
    ;;
esac
