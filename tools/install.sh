#!/usr/bin/env bash
# Installs every skill in skills/ into the local AI tools this script can
# find on THIS machine, by copying/symlinking files — no tool has a public
# API for "install a skill," so this works by dropping files where each
# tool already knows to look for project/agent rules.
#
# Run this in a real terminal on your machine (not inside a sandboxed
# session) from the repo root:
#   bash tools/install.sh                 # installs into ~ (global, where supported)
#   bash tools/install.sh /path/to/project # also installs project-level rules there
set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_PROJECT="${1:-}"

echo "Repo: $REPO_DIR"

install_into() {
  local dir="$1"
  local label="$2"
  [ -d "$dir" ] || return 0
  mkdir -p "$dir/.cursor/rules" 2>/dev/null || true
  if [ -d "$dir/.cursor" ]; then
    cp "$REPO_DIR/adapters/cursor/"*.mdc "$dir/.cursor/rules/" 2>/dev/null && \
      echo "✓ Cursor rules -> $dir/.cursor/rules ($label)"
  fi
  if [ -d "$dir/.antigravity" ]; then
    mkdir -p "$dir/.antigravity/rules"
    cp "$REPO_DIR/adapters/antigravity/"*.md "$dir/.antigravity/rules/" 2>/dev/null && \
      echo "✓ Antigravity rules -> $dir/.antigravity/rules ($label)"
  fi
  # AGENTS.md convention (Cursor, Copilot, Codex CLI, and others read this
  # automatically from a project root)
  if [ -n "$TARGET_PROJECT" ] && [ "$dir" = "$TARGET_PROJECT" ]; then
    cp "$REPO_DIR/adapters/generic/AGENTS.md" "$dir/AGENTS.md"
    echo "✓ AGENTS.md -> $dir/AGENTS.md ($label)"
  fi
}

# Global home-directory install (covers tools with a single global rules dir)
install_into "$HOME" "global"

# Optional: also install + copy the skills/ folder into a specific project
if [ -n "$TARGET_PROJECT" ]; then
  mkdir -p "$TARGET_PROJECT"
  cp -r "$REPO_DIR/skills" "$TARGET_PROJECT/"
  install_into "$TARGET_PROJECT" "project: $TARGET_PROJECT"
  echo "✓ skills/ copied into $TARGET_PROJECT/skills"
fi

echo ""
echo "Claude Code: copy every skill under skills/ to ~/.claude/skills/"
echo "  mkdir -p ~/.claude/skills && cp -r \"$REPO_DIR\"/skills/*/ ~/.claude/skills/"
echo ""
echo "ChatGPT: no file-based install exists — paste adapters/chatgpt/custom_instructions.md"
echo "  into Settings > Personalization > Custom instructions (or a custom GPT's instructions)."
echo ""
echo "Antigravity: verify its current rules-file location in its docs — this script's guess"
echo "  (.antigravity/rules/) may need adjusting; adapters/antigravity/ has the content either way."
