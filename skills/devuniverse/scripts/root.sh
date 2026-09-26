# Sourced by the other scripts: resolves $DEVUNIVERSE_ROOT, the folder where devuniverse writes
# its output. Order: the environment variable if set; else the folder chosen
# on first use (remembered in ~/.config/ai-skills/devuniverse.root) so outputs, quota
# counters and tokens never split between two places; first use picks
# /Volumes/PortableSSD/devuniverse-mcp when that drive is mounted, else $HOME/AI-Projects/devuniverse.
# To move it: export DEVUNIVERSE_ROOT=/new/path (one call) or edit the .root file.
_ai_root_file="$HOME/.config/ai-skills/devuniverse.root"
if [ -z "${DEVUNIVERSE_ROOT:-}" ]; then
  if [ -f "$_ai_root_file" ]; then
    DEVUNIVERSE_ROOT="$(cat "$_ai_root_file")"
    if [ ! -d "$(dirname "$DEVUNIVERSE_ROOT")" ]; then
      echo "Output folder $DEVUNIVERSE_ROOT is not available (external drive not mounted?)." >&2
      echo "Mount it, or set DEVUNIVERSE_ROOT=/another/folder, or edit $_ai_root_file." >&2
      exit 2
    fi
  else
    if [ -d "/Volumes/PortableSSD" ]; then DEVUNIVERSE_ROOT="/Volumes/PortableSSD/devuniverse-mcp"; else DEVUNIVERSE_ROOT="$HOME/AI-Projects/devuniverse"; fi
    mkdir -p "$(dirname "$_ai_root_file")" && printf '%s\n' "$DEVUNIVERSE_ROOT" > "$_ai_root_file"
    echo "(devuniverse output folder: $DEVUNIVERSE_ROOT — remembered in $_ai_root_file)" >&2
  fi
fi
export DEVUNIVERSE_ROOT
mkdir -p "$DEVUNIVERSE_ROOT"
