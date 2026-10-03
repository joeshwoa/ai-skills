#!/usr/bin/env bash
# reels-studio setup — safe to re-run.
#   bash scripts/setup.sh            # check + install python-docx if missing (into a private venv)
#   bash scripts/setup.sh --fonts    # also copy Cairo into your user font folder (so the DOCX shows
#                                    # the house font in Word/LibreOffice; the PDF embeds it anyway)
#   bash scripts/setup.sh --check    # report only, change nothing
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"
CONF="$HOME/.config/ai-skills"
VENV="$HOME/.cache/ai-skills/reels-studio/venv"
CHECK=0; FONTS=0
for a in "$@"; do case "$a" in --check) CHECK=1;; --fonts) FONTS=1;; esac; done

PY="$(command -v python3 || true)"
[ -z "$PY" ] && { echo "✗ python3 not found (macOS: brew install python)"; exit 1; }
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' || { echo "✗ python3 ≥ 3.8 needed"; exit 1; }
echo "✓ python3: $("$PY" --version 2>&1)"

if "$PY" -c 'import docx' 2>/dev/null; then
  echo "✓ python-docx (system python)"; USE_PY="$PY"
elif [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c 'import docx' 2>/dev/null; then
  echo "✓ python-docx (venv $VENV)"; USE_PY="$VENV/bin/python"
elif [ "$CHECK" = 1 ]; then
  echo "✗ python-docx missing — run: bash scripts/setup.sh"; USE_PY="$PY"
else
  echo "… installing python-docx into $VENV"
  mkdir -p "$(dirname "$VENV")" && "$PY" -m venv "$VENV" && "$VENV/bin/python" -m pip install -q python-docx \
    && echo "✓ python-docx installed" && USE_PY="$VENV/bin/python" || { echo "✗ install failed"; USE_PY="$PY"; }
fi
if [ "$CHECK" = 0 ]; then mkdir -p "$CONF" && echo "$USE_PY" > "$CONF/reels-studio.python"; fi

# PDF engines (any one is enough; Chromium-based is preferred for Arabic)
found=""
"$USE_PY" -c 'import playwright' 2>/dev/null && found="$found playwright"
for c in "/Applications/Google Chrome.app" "/Applications/Chromium.app" "/Applications/Microsoft Edge.app" "/Applications/Brave Browser.app"; do
  [ -e "$c" ] && found="$found $(basename "$c" .app | tr ' ' '-')"
done
for n in google-chrome chromium chromium-browser microsoft-edge; do command -v "$n" >/dev/null 2>&1 && found="$found $n"; done
{ [ -e "/Applications/LibreOffice.app" ] || command -v soffice >/dev/null 2>&1; } && found="$found libreoffice"
if [ -n "$found" ]; then echo "✓ PDF engine(s):$found"; else
  echo "✗ no PDF engine — install Google Chrome (or: pip install playwright && playwright install chromium, or LibreOffice). DOCX/HTML still work."; fi

if [ "$FONTS" = 1 ] && [ "$CHECK" = 0 ]; then
  case "$(uname)" in Darwin) FD="$HOME/Library/Fonts";; *) FD="$HOME/.local/share/fonts";; esac
  mkdir -p "$FD" && cp "$SKILL"/assets/fonts/Cairo-*.ttf "$FD"/ && echo "✓ Cairo fonts → $FD"
  command -v fc-cache >/dev/null 2>&1 && fc-cache -f "$FD" >/dev/null 2>&1
fi
echo "done."
