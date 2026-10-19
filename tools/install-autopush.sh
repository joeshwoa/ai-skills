#!/usr/bin/env bash
# One-time setup on the Mac. After this, every commit in the ai-skills repo is
# pushed to GitHub automatically within 5 minutes. Safe to re-run.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LABEL=com.joshua.ai-skills-autopush
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
chmod +x "$REPO/tools/autopush.sh"

cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$REPO/tools/autopush.sh</string></array>
  <key>EnvironmentVariables</key>
  <dict><key>AI_SKILLS_REPO</key><string>$REPO</string></dict>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/ai-skills-autopush.out</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/ai-skills-autopush.out</string>
</dict>
</plist>
PLIST_EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Auto-push installed. Running the first push now..."
bash "$REPO/tools/autopush.sh" || true
echo "Done. Log: $HOME/Library/Logs/ai-skills-autopush.log"
tail -3 "$HOME/Library/Logs/ai-skills-autopush.log" 2>/dev/null || true
