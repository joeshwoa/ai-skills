# Sourced by the other scripts: resolves $CINEMA_ROOT, the folder where omnicinema writes
# its output. Order: the environment variable if set; else the folder chosen
# on first use (remembered in ~/.config/ai-skills/omnicinema.root) so outputs, quota
# counters and tokens never split between two places; first use picks
# /Volumes/PortableSSD/omnicinema-mcp when that drive is mounted, else $HOME/AI-Projects/omnicinema.
# To move it: export CINEMA_ROOT=/new/path (one call) or edit the .root file.
_ai_root_file="$HOME/.config/ai-skills/omnicinema.root"
if [ -z "${CINEMA_ROOT:-}" ]; then
  if [ -f "$_ai_root_file" ]; then
    CINEMA_ROOT="$(cat "$_ai_root_file")"
    if [ ! -d "$(dirname "$CINEMA_ROOT")" ]; then
      echo "Output folder $CINEMA_ROOT is not available (external drive not mounted?)." >&2
      echo "Mount it, or set CINEMA_ROOT=/another/folder, or edit $_ai_root_file." >&2
      exit 2
    fi
  else
    if [ -d "/Volumes/PortableSSD" ]; then CINEMA_ROOT="/Volumes/PortableSSD/omnicinema-mcp"; else CINEMA_ROOT="$HOME/AI-Projects/omnicinema"; fi
    mkdir -p "$(dirname "$_ai_root_file")" && printf '%s\n' "$CINEMA_ROOT" > "$_ai_root_file"
    echo "(omnicinema output folder: $CINEMA_ROOT — remembered in $_ai_root_file)" >&2
  fi
fi
export CINEMA_ROOT
mkdir -p "$CINEMA_ROOT"
