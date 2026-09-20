#!/usr/bin/env bash
# Call one omnicinema-mcp tool, no MCP client/registration needed.
# Usage: call.sh <tool_name> ['<json-args>']
# Example: call.sh list_providers '{}'
#          call.sh generate_image '{"assetKind":"logo","subject":"a fox reading a book"}'
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/omnicinema-mcp"
ENTRY="$CACHE_DIR/dist/index.js"

if [ ! -f "$ENTRY" ]; then
  echo "omnicinema-mcp isn't installed yet. Run: bash $SCRIPT_DIR/bootstrap.sh" >&2
  exit 2
fi

TOOL="${1:?Usage: call.sh <tool_name> ['<json-args>']}"
# NOTE: deliberately not `${2:-{}}` — bash's brace matching inside a
# parameter expansion's default value gets confused by a literal `{}`
# there (it was appending a stray extra `}` when $2 was itself "{}",
# producing invalid JSON). Spelling it out avoids that pitfall.
ARGS="${2-}"
if [ -z "$ARGS" ]; then
  ARGS='{}'
fi

# Run from the cache dir so the server's relative paths (tools-registry.json,
# data/, .env) resolve the same way they do for a normal `npm start` there.
cd "$CACHE_DIR"
exec node "$SCRIPT_DIR/mcp_cli.mjs" node "$ENTRY" -- "$TOOL" "$ARGS"
