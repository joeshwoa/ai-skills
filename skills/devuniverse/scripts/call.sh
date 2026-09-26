#!/usr/bin/env bash
# Call one devuniverse-mcp tool — no MCP client or registration needed.
#   call.sh <tool> ['<json-args>' | @args.json]     human-readable result
#   call.sh --json <tool> [...]                      raw MCP result (structured data)
#   call.sh --list                                   every tool + its arguments
# Output location: $DEVUNIVERSE_ROOT — see root.sh (default: /Volumes/PortableSSD/devuniverse-mcp when that drive is
# mounted, else $HOME/AI-Projects/devuniverse). Set it to put work somewhere else.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="devuniverse-mcp"
# shellcheck source=/dev/null
. "$SCRIPT_DIR/root.sh"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/$NAME"
ENTRY="$CACHE_DIR/dist/index.js"
[ -f "$ENTRY" ] || { echo "$NAME isn't installed yet. Run: bash $SCRIPT_DIR/bootstrap.sh" >&2; exit 2; }

FLAG=()
if [ "${1-}" = "--json" ]; then FLAG=(--json); shift; fi
TOOL="${1:?Usage: call.sh [--json] <tool_name> ['<json-args>'|@file] | --list}"
# Spelled out rather than ${2:-{}} — bash brace matching appends a stray "}".
ARGS="${2-}"
[ -n "$ARGS" ] || ARGS='{}'
case "$ARGS" in @*) ARGS="@$(cd "$(dirname "${ARGS#@}")" && pwd)/$(basename "${ARGS#@}")";; esac

cd "$CACHE_DIR"
exec node "$SCRIPT_DIR/mcp_cli.mjs" ${FLAG[@]+"${FLAG[@]}"} node "$ENTRY" -- "$TOOL" "$ARGS"
