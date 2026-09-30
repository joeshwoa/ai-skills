#!/usr/bin/env bash
# Install or update studio-mcp (github.com/joeshwoa/studio-mcp) into its own Python environment.
# Safe to re-run: it upgrades in place.
#   bash bootstrap.sh                 install / update (Python packages + headless Chromium, ~1.5 GB)
#   bash bootstrap.sh --check         only report what is installed
#   bash bootstrap.sh --venv DIR      put the environment somewhere else
#   bash bootstrap.sh --lite          only the core (design, brand, vector, motion; no audio/photo AI models)
# Desktop apps (GIMP, Inkscape, Kdenlive, Audacity…) and AI models are NOT installed here — the studio
# lists them with sizes (studio_doctor / studio_install / comfyui_setup) and installs only after the user agrees.
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${AI_SKILLS_STUDIO_REPO:-https://github.com/joeshwoa/studio-mcp}"
REF="${AI_SKILLS_STUDIO_REF:-main}"
CHECK=0; LITE=0; VENV=""
while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK=1 ;;
    --lite) LITE=1 ;;
    --venv) shift; VENV="$1" ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac; shift
done
VFILE="$HOME/.config/ai-skills/creative-studio.venv"
if [ -z "$VENV" ]; then
  if [ -f "$VFILE" ]; then VENV="$(cat "$VFILE")"
  elif [ -d /Volumes/PortableSSD ]; then VENV="/Volumes/PortableSSD/creative-studio/.venv"
  else VENV="$HOME/.cache/ai-skills/creative-studio/venv"; fi
fi

if [ "$CHECK" = 1 ]; then
  if [ -x "$VENV/bin/studio" ]; then
    echo "studio-mcp installed in $VENV ($("$VENV/bin/pip" show studio-mcp 2>/dev/null | sed -n 's/^Version: //p'))"
    PLAYWRIGHT_BROWSERS_PATH="$VENV/ms-playwright" "$VENV/bin/studio" doctor || true
  else
    echo "studio-mcp not installed — run: bash $S/bootstrap.sh"
  fi
  exit 0
fi

PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "Python ≥ 3.10 is required (macOS: brew install python@3.12)." >&2; exit 1
fi
command -v git >/dev/null || { echo "git is required." >&2; exit 1; }

if [ ! -x "$VENV/bin/python" ]; then
  echo "Creating the studio environment in $VENV (with $($PY --version))"
  mkdir -p "$(dirname "$VENV")"
  "$PY" -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --quiet --upgrade pip
EXTRAS="all"; [ "$LITE" = 1 ] && EXTRAS="design,vector,motion"
if [ "$(uname -s)" = Darwin ] && [ "$(uname -m)" = arm64 ] && [ "$LITE" = 0 ]; then EXTRAS="$EXTRAS,mac"; fi
echo "Installing studio-mcp[$EXTRAS] from $REPO@$REF"
"$VENV/bin/pip" install --quiet --upgrade "studio-mcp[$EXTRAS] @ git+$REPO@$REF"
export PLAYWRIGHT_BROWSERS_PATH="$VENV/ms-playwright"
echo "Installing headless Chromium for layouts and motion graphics"
"$VENV/bin/python" -m playwright install chromium >/dev/null
mkdir -p "$(dirname "$VFILE")" && printf '%s\n' "$VENV" > "$VFILE"
echo
echo "Done. Environment: $VENV (remembered in $VFILE)"
echo "MCP server command: $VENV/bin/studio-mcp  (env PLAYWRIGHT_BROWSERS_PATH=$VENV/ms-playwright)"
echo "Next: bash $S/call.sh studio_doctor   — what else can be installed (apps, models), with sizes"
