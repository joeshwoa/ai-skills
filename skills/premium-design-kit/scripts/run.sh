#!/usr/bin/env bash
# Run a Python script of any premium document skill with the right interpreter + the shared kit on
# PYTHONPATH.   run.sh <script.py> [args…]
# Interpreter: $PDK_PYTHON, else the venv made by setup.sh, else python3.
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PDK_PYTHON:-}"
VF="$HOME/.config/ai-skills/docs.venv"
if [ -z "$PY" ] && [ -f "$VF" ] && [ -x "$(cat "$VF")/bin/python" ]; then PY="$(cat "$VF")/bin/python"; fi
[ -z "$PY" ] && PY="$(command -v python3)"
export PYTHONPATH="$KIT/lib${PYTHONPATH:+:$PYTHONPATH}"
# share Chromium with creative-studio when it is installed (no second download)
if [ -z "${PLAYWRIGHT_BROWSERS_PATH:-}" ] && [ -f "$HOME/.config/ai-skills/creative-studio.venv" ]; then
  MP="$(cat "$HOME/.config/ai-skills/creative-studio.venv")/ms-playwright"; [ -d "$MP" ] && export PLAYWRIGHT_BROWSERS_PATH="$MP"
fi
exec "$PY" "$@"
