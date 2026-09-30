# Sourced by the other scripts: finds the studio's Python environment.
# Order: $CREATIVE_STUDIO_VENV; else the venv remembered in ~/.config/ai-skills/creative-studio.venv
# (written by bootstrap.sh); else nothing (callers tell the user to run bootstrap.sh).
# Outputs, brand kits and AI models live in STUDIO_HOME, which the studio itself resolves:
# $STUDIO_HOME, else ~/.config/ai-skills/creative-studio.root, else (first run)
# /Volumes/PortableSSD/creative-studio when that drive is mounted, else ~/AI-Projects/creative-studio.
_cs_venv_file="$HOME/.config/ai-skills/creative-studio.venv"
if [ -z "${CREATIVE_STUDIO_VENV:-}" ] && [ -f "$_cs_venv_file" ]; then
  CREATIVE_STUDIO_VENV="$(cat "$_cs_venv_file")"
fi
if [ -n "${CREATIVE_STUDIO_VENV:-}" ] && [ ! -x "$CREATIVE_STUDIO_VENV/bin/studio" ]; then
  echo "The studio environment $CREATIVE_STUDIO_VENV is not available (external drive not mounted?)." >&2
  echo "Mount the drive, or run bootstrap.sh again (it can install elsewhere with --venv DIR)." >&2
  exit 2
fi
export CREATIVE_STUDIO_VENV
# Playwright keeps its Chromium next to the venv so the SSD holds everything big
[ -n "${CREATIVE_STUDIO_VENV:-}" ] && export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$CREATIVE_STUDIO_VENV/ms-playwright}"
