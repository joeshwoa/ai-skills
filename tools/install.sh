#!/usr/bin/env bash
# Installs every skill in skills/ into the local AI tools this script can
# find on THIS machine, by copying/symlinking files — no tool has a public
# API for "install a skill," so this works by dropping files where each
# tool already knows to look for project/agent rules.
#
# Verified against each tool's own docs (2026-09) — earlier versions of
# this script guessed at some paths; corrected below:
#   - Cursor:      project rules are `.cursor/rules/*.mdc` in the PROJECT
#                   root — Cursor has NO global filesystem rules directory.
#                   Global "User Rules" only exist as UI-entered text in
#                   Cursor's own Settings -> Customize -> Rules; there is
#                   nothing on disk to copy for that, see the printed text
#                   block below and paste it in once, by hand.
#   - Antigravity: reads plain `AGENTS.md` at a project's root (already
#                   the generic convention this repo uses), and globally
#                   from `~/.gemini/AGENTS.md` (GEMINI.md there takes
#                   priority if both exist). `.antigravity/rules/` is NOT
#                   a real Antigravity discovery path — ignore any older
#                   note in this repo that said otherwise.
#
# Run this in a real terminal on your machine (not inside a sandboxed
# session) from the repo root:
#   bash tools/install.sh                 # sets up THIS repo as a Cursor/Antigravity project + global Antigravity
#   bash tools/install.sh /path/to/project # + installs project-level rules into another project too
set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_PROJECT="${1:-}"

echo "Repo: $REPO_DIR"

# Keep skills/manifest.json (the skill-router dispatcher's index) current.
if command -v python3 >/dev/null 2>&1; then
  python3 "$REPO_DIR/skills/skill-router/scripts/build_manifest.py" "$REPO_DIR"
else
  echo "• python3 not found — skipping skills/manifest.json refresh (skill-router needs this; install python3 and re-run)"
fi

install_project_rules() {
  local dir="$1"
  local label="$2"
  mkdir -p "$dir/.cursor/rules"
  cp "$REPO_DIR/adapters/cursor/"*.mdc "$dir/.cursor/rules/"
  echo "✓ Cursor project rules -> $dir/.cursor/rules ($label) — pick up automatically next time you open this folder in Cursor"

  cp "$REPO_DIR/adapters/generic/AGENTS.md" "$dir/AGENTS.md"
  echo "✓ AGENTS.md -> $dir/AGENTS.md ($label) — read automatically by Antigravity and other AGENTS.md-aware tools"
}

# This repo itself is a valid Cursor/Antigravity project — always set it up
# so opening Cursor/Antigravity directly on this folder works immediately.
install_project_rules "$REPO_DIR" "this repo"

# Antigravity global rules (the one real global, file-based mechanism)
if [ -d "$HOME/.gemini" ]; then
  if [ -f "$HOME/.gemini/AGENTS.md" ] && ! grep -q "premium-subtitle-localization\|premium-presentations\|premium-3d-models" "$HOME/.gemini/AGENTS.md" 2>/dev/null; then
    echo "" >> "$HOME/.gemini/AGENTS.md"
    echo "---" >> "$HOME/.gemini/AGENTS.md"
    cat "$REPO_DIR/adapters/generic/AGENTS.md" >> "$HOME/.gemini/AGENTS.md"
    echo "✓ Appended skills section -> ~/.gemini/AGENTS.md (global Antigravity, kept your existing content)"
  elif [ ! -f "$HOME/.gemini/AGENTS.md" ]; then
    cp "$REPO_DIR/adapters/generic/AGENTS.md" "$HOME/.gemini/AGENTS.md"
    echo "✓ AGENTS.md -> ~/.gemini/AGENTS.md (global Antigravity — applies to every project)"
  else
    echo "• ~/.gemini/AGENTS.md already mentions these skills — left as-is"
  fi
else
  echo "• ~/.gemini not found — skipping global Antigravity install (per-project AGENTS.md still works everywhere)"
fi

# Optional: also install + copy the skills/ folder into a specific OTHER project
if [ -n "$TARGET_PROJECT" ]; then
  mkdir -p "$TARGET_PROJECT"
  cp -r "$REPO_DIR/skills" "$TARGET_PROJECT/"
  install_project_rules "$TARGET_PROJECT" "project: $TARGET_PROJECT"
  echo "✓ skills/ copied into $TARGET_PROJECT/skills"
fi

echo ""
echo "Claude Code: copy every skill under skills/ to ~/.claude/skills/"
echo "  mkdir -p ~/.claude/skills && cp -r \"$REPO_DIR\"/skills/*/ ~/.claude/skills/"
echo ""
echo "ChatGPT: no file-based install exists — paste adapters/chatgpt/custom_instructions.md"
echo "  into Settings > Personalization > Custom instructions (or a custom GPT's instructions)."
echo ""
echo "Cursor GLOBAL (applies in every project, not just this repo) — Cursor has no file for"
echo "this, paste the block below into Cursor Settings -> Customize -> Rules -> User Rules, ONCE:"
echo "-----------------------------------------------------------------------------------"
echo "Read skills/skill-router/SKILL.md FIRST, always — it auto-selects a matching"
echo "installed skill from skills/manifest.json, and if nothing matches, searches for or"
echo "builds a new one and installs it automatically. The list below is what it dispatches to:"
echo "- Slide deck / presentation / pitch deck / PowerPoint request -> if this project has"
echo "  a premium-presentations skill (skills/premium-presentations/SKILL.md) or an AGENTS.md"
echo "  pointing at one, read it before building the deck."
echo "- 3D model / .glb / .stl / mechanical part / Blender asset request -> same, look for"
echo "  skills/premium-3d-models/SKILL.md or its AGENTS.md pointer."
echo "- Subtitle / translate / localize a video request -> same, look for"
echo "  skills/premium-subtitle-localization/SKILL.md or its AGENTS.md pointer."
echo "- Cinematic video / design asset / voiceover / music / SFX via OmniCinema -> same, look for"
echo "  skills/omnicinema/SKILL.md or its AGENTS.md pointer."
echo "- Scaffold a new app / Flutter project / 3D spatial canvas module -> same, look for"
echo "  skills/devuniverse/SKILL.md or its AGENTS.md pointer."
echo "- Make / plan / prompt / fix / check an AI video, reel, ad or animated series, or"
echo "  choose a Google Flow model / estimate credits -> skills/flow-studio-director/SKILL.md."
echo "- A skill just failed, or a request to enhance/audit/improve a skill -> look for"
echo "  skills/skill-enhancer/SKILL.md or its AGENTS.md pointer."
echo "If none of these skill folders exist in the current project, proceed normally."
echo "-----------------------------------------------------------------------------------"
