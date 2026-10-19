#!/bin/bash
# One-time setup on the Mac. After this, every agent reads skills from a local GitHub clone that
# refreshes itself, so nothing depends on the SSD and nothing needs a manual push or copy.
set -euo pipefail
HUB="$HOME/.local/share/ai-skills-hub"
REPO_URL="https://github.com/joeshwoa/ai-skills.git"
SERVER="$HUB/tools/ai-skills-mcp/server.py"

mkdir -p "$(dirname "$HUB")"
if [ -d "$HUB/.git" ]; then
  git -C "$HUB" fetch -q origin
  git -C "$HUB" reset -q --hard origin/main
else
  git clone -q "$REPO_URL" "$HUB"
fi
echo "GitHub clone ready: $HUB"

python3 - "$SERVER" <<'PY'
import json, os, shutil, sys
server = sys.argv[1]
entry = {"command": "python3", "args": [server]}
targets = [
    "~/.cursor/mcp.json",
    "~/Library/Application Support/Claude/claude_desktop_config.json",
    "~/.claude.json",
    "~/.codeium/windsurf/mcp_config.json",
    "~/.gemini/settings.json",
    "~/.gemini/mcp_config.json",
]
for path in targets:
    p = os.path.expanduser(path)
    if not os.path.exists(p):
        continue
    shutil.copy(p, p + ".bak")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    d.setdefault("mcpServers", {})["ai-skills"] = entry
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print("pointed to GitHub clone:", p)
PY

# Cursor skill folders: relink symlinks to the GitHub clone (real folders are left alone).
mkdir -p "$HOME/.cursor/skills"
for d in "$HUB"/skills/*/; do
  n=$(basename "$d")
  [ -f "$d/SKILL.md" ] || continue
  t="$HOME/.cursor/skills/$n"
  if [ -L "$t" ] || [ ! -e "$t" ]; then ln -sfn "${d%/}" "$t"; fi
done
echo "Cursor skill links now point to the GitHub clone."
echo "Restart Cursor, Claude Desktop, Windsurf; start a new Gemini CLI / Claude Code session."
