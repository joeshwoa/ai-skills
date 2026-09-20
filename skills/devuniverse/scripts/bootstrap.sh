#!/usr/bin/env bash
# Clones (or updates) and builds the real devuniverse-mcp server into a
# local cache, so scripts/call.sh can run its tools with no MCP client
# registration needed. Safe to re-run — it just updates in place.
set -euo pipefail

REPO_URL="https://github.com/joeshwoa/devuniverse-mcp.git"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/devuniverse-mcp"

if [ -d "$CACHE_DIR/.git" ]; then
  echo "Updating existing checkout at $CACHE_DIR"
  git -C "$CACHE_DIR" pull --ff-only
else
  echo "Cloning $REPO_URL -> $CACHE_DIR"
  mkdir -p "$(dirname "$CACHE_DIR")"
  git clone "$REPO_URL" "$CACHE_DIR"
fi

cd "$CACHE_DIR"
npm install --no-audit --no-fund
npm run build

if [ ! -f "$CACHE_DIR/dist/index.js" ]; then
  echo "Build finished but dist/index.js is missing — check the build output above." >&2
  exit 1
fi

echo "devuniverse-mcp ready at $CACHE_DIR/dist/index.js"
