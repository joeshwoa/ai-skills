#!/usr/bin/env bash
# One-time setup on the Mac. After this, every commit in the ai-skills repo is
# pushed to GitHub automatically, right after the commit happens. Safe to re-run.
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
  <key>WatchPaths</key>
  <array>
    <string>$REPO/.git/refs/heads</string>
    <string>$REPO/.git/logs/HEAD</string>
  </array>
  <key>ThrottleInterval</key><integer>30</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/ai-skills-autopush.out</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/ai-skills-autopush.out</string>
</dict>
</plist>
PLIST_EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Auto-push installed: it runs only when a commit lands in the repo."
bash "$REPO/tools/autopush.sh" || true
echo "Log: $HOME/Library/Logs/ai-skills-autopush.log"
tail -3 "$HOME/Library/Logs/ai-skills-autopush.log" 2>/dev/null || true

# Self-check: macOS blocks background jobs from reading an external drive (like the SSD) unless
# /bin/bash has Full Disk Access. Run the job the way launchd does and report what happened.
OUT="$HOME/Library/Logs/ai-skills-autopush.out"
: > "$OUT"
launchctl kickstart -k "gui/$(id -u)/$LABEL" 2>/dev/null || true
sleep 4
if grep -q "Operation not permitted" "$OUT" 2>/dev/null; then
  cat <<'MSG'

!! Background pushes are BLOCKED by macOS (Operation not permitted on the SSD).
   One-time fix, 30 seconds:
   System Settings > Privacy & Security > Full Disk Access > click "+"
   > press Cmd+Shift+G, type /bin/bash, Open > make sure the switch is ON.
   Then run this installer again. It will say OK when the job can read the repo.
MSG
  exit 1
fi
echo "OK: the background job can read the repo and will push every new commit by itself."
