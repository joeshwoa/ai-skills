#!/usr/bin/env bash
# Clone (or update) and build the real omnicinema-mcp server into a local cache so
# scripts/call.sh can run its tools with no MCP client registration.
# Safe to re-run: it updates in place and rebuilds.
#   bash bootstrap.sh            # install / update
#   bash bootstrap.sh --check    # only report what is installed and what is missing
set -euo pipefail
NAME="omnicinema-mcp"
REPO_URL="${AI_SKILLS_OMNICINEMA_REPO:-https://github.com/joeshwoa/omnicinema-mcp.git}"
NODE_MIN=18
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
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt "$NODE_MIN" ]; then
  echo "Node $(node -v) is too old — $NAME needs Node >= $NODE_MIN." >&2; exit 1
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
  report_tools ffmpeg ffprobe rsvg-convert espeak-ng say
  ffmpeg -hide_banner -filters 2>/dev/null | grep -q ' flite ' && echo "  ok       flite (inside ffmpeg)" || echo "  missing  flite (ffmpeg built without it; fine if say/espeak-ng exist)"
  [ -d "$CACHE_DIR/node_modules/remotion" ] && echo "  ok       remotion (installed)" || echo "  missing  remotion (optional: bootstrap.sh --with-render; ffmpeg renders without it)"
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
if [ "$WITH_RENDER" = 1 ]; then
  echo "Installing the optional Remotion renderer (a few hundred MB)…"
  npm run setup:render --silent
fi
if ! npm run build --silent; then
  echo "Build failed — see the compiler output above. The checkout is at $CACHE_DIR." >&2; exit 1
fi
[ -f dist/index.js ] || { echo "Build finished but dist/index.js is missing." >&2; exit 1; }
echo "$NAME ready: $(git log -1 --format='%h %cs %s')"
report_tools ffmpeg ffprobe rsvg-convert espeak-ng say
  ffmpeg -hide_banner -filters 2>/dev/null | grep -q ' flite ' && echo "  ok       flite (inside ffmpeg)" || echo "  missing  flite (ffmpeg built without it; fine if say/espeak-ng exist)"
