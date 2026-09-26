#!/usr/bin/env bash
# Clone (or update) and build the real devuniverse-mcp server into a local cache so
# scripts/call.sh can run its tools with no MCP client registration.
# Safe to re-run: it updates in place and rebuilds.
#   bash bootstrap.sh            # install / update
#   bash bootstrap.sh --check    # only report what is installed and what is missing
set -euo pipefail
NAME="devuniverse-mcp"
REPO_URL="${AI_SKILLS_DEVUNIVERSE_REPO:-https://github.com/joeshwoa/devuniverse-mcp.git}"
NODE_MIN=20
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/$NAME"
CHECK_ONLY=0; WITH_RENDER=0
for a in "$@"; do
  case "$a" in
    --check) CHECK_ONLY=1 ;;
    --with-render) WITH_RENDER=1 ;;
    *) echo "unknown option $a" >&2; exit 2 ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1; }
if ! have node || ! have npm || ! have git; then
  echo "Missing requirement: node, npm and git must be on PATH (Node >= $NODE_MIN)." >&2; exit 1
fi
if ! node -e 'const [a,b]=process.versions.node.split(".").map(Number);process.exit(a>20||(a===20&&b>=10)?0:1)'; then
  echo "Node $(node -v) is too old — $NAME needs Node >= 20.10." >&2; exit 1
fi

report_tools() {
  echo "--- optional tools on this machine ---"
  for t in "$@"; do
    if have "$t"; then echo "  ok       $t"; else echo "  missing  $t"; fi
  done
}

if [ "$CHECK_ONLY" = 1 ]; then
  if [ -f "$CACHE_DIR/dist/index.js" ]; then
    echo "$NAME installed at $CACHE_DIR ($(git -C "$CACHE_DIR" log -1 --format='%h %cs %s'))"
  else
    echo "$NAME not installed — run: bash $(dirname "$0")/bootstrap.sh"
  fi
  report_tools flutter dart docker psql ffmpeg
  exit 0
fi

if [ -d "$CACHE_DIR/.git" ]; then
  echo "Updating $CACHE_DIR"
  git -C "$CACHE_DIR" fetch --quiet origin
  git -C "$CACHE_DIR" merge --ff-only --quiet "@{u}" || {
    echo "Local changes in $CACHE_DIR block the update (git status there). Not touching them." >&2; exit 1; }
else
  echo "Cloning $REPO_URL -> $CACHE_DIR"
  mkdir -p "$(dirname "$CACHE_DIR")"
  git clone --quiet "$REPO_URL" "$CACHE_DIR"
fi

cd "$CACHE_DIR"
if [ -f package-lock.json ]; then npm ci --no-audit --no-fund --loglevel=error; else npm install --no-audit --no-fund --loglevel=error; fi
if ! npm run build --silent; then
  echo "Build failed — see the compiler output above. The checkout is at $CACHE_DIR." >&2; exit 1
fi
[ -f dist/index.js ] || { echo "Build finished but dist/index.js is missing." >&2; exit 1; }
echo "$NAME ready: $(git log -1 --format='%h %cs %s')"
report_tools flutter dart docker psql ffmpeg
