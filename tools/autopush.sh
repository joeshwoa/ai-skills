#!/usr/bin/env bash
# autopush — pushes every local commit of the ai-skills repo to GitHub.
# Runs every 5 minutes on the Mac through a LaunchAgent (installed once by
# tools/install-autopush.sh). Pushes ONLY commits; never rewrites history,
# never force-pushes, never touches files. If the remote has commits we don't
# have, it stops and logs instead of guessing.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"
REPO="${AI_SKILLS_REPO:-$HOME/.cursor/ai-skills}"
LOG="$HOME/Library/Logs/ai-skills-autopush.log"
mkdir -p "$(dirname "$LOG")"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

cd "$REPO" 2>/dev/null || { log "repo not found: $REPO"; exit 1; }
# Another git process is running right now: try again on the next tick.
if pgrep -x git >/dev/null 2>&1; then exit 0; fi

if ! git fetch --quiet origin main >>"$LOG" 2>&1; then log "fetch failed (offline or auth)"; exit 1; fi
AHEAD=$(git rev-list --count origin/main..HEAD)
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ "$BEHIND" -gt 0 ]; then log "remote has $BEHIND commit(s) we don't have; not pushing"; exit 1; fi
[ "$AHEAD" -eq 0 ] && exit 0
if git push --quiet origin main >>"$LOG" 2>&1; then
  log "pushed $AHEAD commit(s) to origin/main"
else
  log "push failed (see lines above)"; exit 1
fi
