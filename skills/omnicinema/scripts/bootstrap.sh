#!/usr/bin/env bash
# Clones (or updates) and builds the real omnicinema-mcp server into a local
# cache, so scripts/call.sh can run its tools with no MCP client
# registration needed. Safe to re-run — it just updates in place.
set -euo pipefail

REPO_URL="https://github.com/joeshwoa/omnicinema-mcp.git"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/omnicinema-mcp"

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
set +e
npm run build
BUILD_STATUS=$?
set -e

if [ ! -f "$CACHE_DIR/dist/index.js" ]; then
  cat <<'EOF' >&2

============================================================
BUILD FAILED — known issue in the omnicinema-mcp repo itself
============================================================
This is NOT a problem with this skill. As of the last check, a fresh clone
of joeshwoa/omnicinema-mcp fails to build with errors like:

  Cannot find module '../assets/stockManager.js'
  Cannot find module '../assets/stock/pexels.js'
  ...

Root cause: the repo's .gitignore has a bare `assets/` rule (no leading
slash), which matches at every depth — so it silently excludes
`src/assets/` (real source code: stockManager.ts, pexels.ts, pixabay.ts,
unsplash.ts, vector.ts) from git, not just the intended top-level runtime
`assets/` output folder. `git log --all -- src/assets` shows nothing was
ever committed there, on any branch.

Fix (in the omnicinema-mcp repo, one line):
  Change the .gitignore rule from `assets/` to `/assets/` (anchor it to
  the repo root) and `!assets/.gitkeep` to `!/assets/.gitkeep`, then
  `git add -f src/assets && git commit && git push` the previously-
  untracked source files.

Once that's fixed upstream, re-run this bootstrap script — no change
needed here.
============================================================
EOF
  exit 1
fi

echo "omnicinema-mcp ready at $CACHE_DIR/dist/index.js"
