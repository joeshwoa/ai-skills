#!/usr/bin/env bash
# Run one studio tool (no MCP client needed) and print its report.
#   call.sh <tool> '<json args>'     e.g. call.sh brand_create '{"name":"Qahwa House","sector":"coffee"}'
#   call.sh <tool> @args.json        arguments from a file (long briefs, Arabic, quotes)
#   call.sh --json <tool> …          machine-readable result (files, previews, warnings, data)
#   call.sh list [dept]              tool catalogue;  call.sh help <tool>   full arguments
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$S/env.sh"
if [ -z "${CREATIVE_STUDIO_VENV:-}" ]; then
  echo "studio-mcp is not installed yet — run: bash $S/bootstrap.sh" >&2; exit 2
fi
[ $# -eq 0 ] && set -- --help
exec "$CREATIVE_STUDIO_VENV/bin/studio" "$@"
