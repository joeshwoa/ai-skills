#!/usr/bin/env bash
# Call one devuniverse-mcp tool, no MCP client/registration needed.
# Usage: call.sh <tool_name> ['<json-args>']
# Example: call.sh get_agency_roster '{}'
#          call.sh init_dev_universe '{"project_type":"flutter_spatial_app","description":"a meditation app with a 3D deep-scroll journey"}'
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/devuniverse-mcp"
ENTRY="$CACHE_DIR/dist/index.js"

if [ ! -f "$ENTRY" ]; then
  echo "devuniverse-mcp isn't installed yet. Run: bash $SCRIPT_DIR/bootstrap.sh" >&2
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

cd "$CACHE_DIR"
exec node "$SCRIPT_DIR/mcp_cli.mjs" node "$ENTRY" -- "$TOOL" "$ARGS"
