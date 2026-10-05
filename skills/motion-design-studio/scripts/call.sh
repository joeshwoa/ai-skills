#!/usr/bin/env bash
# Run one studio-mcp tool (same server as the creative-studio skill) and print its report.
#   call.sh <tool> '<json args>'  |  call.sh <tool> @args.json  |  call.sh --json <tool> …
#   call.sh list [dept]  |  call.sh help <tool>
# The environment is installed once by creative-studio:  bash ../creative-studio/scripts/bootstrap.sh
set -euo pipefail
VFILE="$HOME/.config/ai-skills/creative-studio.venv"
VENV="${CREATIVE_STUDIO_VENV:-}"
[ -z "$VENV" ] && [ -f "$VFILE" ] && VENV="$(cat "$VFILE")"
if [ -z "$VENV" ] || [ ! -x "$VENV/bin/studio" ]; then
  S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  echo "studio-mcp is not installed (or its drive is not mounted)." >&2
  echo "Install/update it once with: bash $S/../../creative-studio/scripts/bootstrap.sh" >&2
  exit 2
fi
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$VENV/ms-playwright}"
[ $# -eq 0 ] && set -- --help
exec "$VENV/bin/studio" "$@"
