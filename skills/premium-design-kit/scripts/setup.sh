#!/usr/bin/env bash
# One-time setup for premium-presentations / premium-documents / premium-spreadsheets / course-studio.
# Creates a small venv (python-pptx, python-docx, openpyxl, matplotlib, Arabic shaping, PyMuPDF,
# Playwright) and remembers it in ~/.config/ai-skills/docs.venv.  Safe to re-run (upgrades).
#   bash setup.sh            # venv in ~/.local/share/ai-skills/docs-venv
#   bash setup.sh <dir>      # venv somewhere else (e.g. on the SSD)
# Chromium (for designed PDFs): reused from creative-studio when present; otherwise this asks before
# downloading it (~150 MB).  LibreOffice (optional, for previews of .pptx/.docx/.xlsx) is NOT installed
# automatically:  brew install --cask libreoffice
set -euo pipefail
DIR="${1:-$HOME/.local/share/ai-skills/docs-venv}"
PYBIN="$(command -v python3.12 || command -v python3.11 || command -v python3)"
"$PYBIN" -c 'import sys; assert sys.version_info >= (3, 9), "Python 3.9+ needed"'
[ -x "$DIR/bin/python" ] || "$PYBIN" -m venv "$DIR"
"$DIR/bin/python" -m pip install -q --upgrade pip
"$DIR/bin/python" -m pip install -q --upgrade "python-pptx>=1.0" "python-docx>=1.1" "openpyxl>=3.1" \
  "matplotlib>=3.8" numpy pillow arabic-reshaper python-bidi pymupdf "playwright>=1.42" pygments
mkdir -p "$HOME/.config/ai-skills"
echo "$DIR" > "$HOME/.config/ai-skills/docs.venv"
CS="$HOME/.config/ai-skills/creative-studio.venv"
if [ -f "$CS" ] && [ -d "$(cat "$CS")/ms-playwright" ]; then
  echo "Chromium: shared with creative-studio ($(cat "$CS")/ms-playwright)"
elif [ -d "$HOME/Library/Caches/ms-playwright" ] || [ -d "$HOME/.cache/ms-playwright" ]; then
  echo "Chromium: already installed for Playwright"
else
  read -r -p "Download Chromium for designed PDFs (~150 MB)? [y/N] " a
  if [[ "$a" =~ ^[Yy] ]]; then "$DIR/bin/python" -m playwright install chromium; else echo "skipped — PDFs from HTML will not work until you run: $DIR/bin/python -m playwright install chromium"; fi
fi
command -v soffice >/dev/null || [ -d /Applications/LibreOffice.app ] || echo "Tip: brew install --cask libreoffice  (lets the skills preview and check .pptx/.docx/.xlsx pages)"
echo "OK — docs venv: $DIR"
