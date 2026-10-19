#!/usr/bin/env bash
# autopush — pushes new local commits of the ai-skills repo to GitHub.
# Started by a LaunchAgent that watches the repo's git refs, so it runs only
# when a commit actually happens (no polling). Pushes commits only; never
# force-pushes; stops and logs if the remote has commits we don't have.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"
REPO="${AI_SKILLS_REPO:-$HOME/.cursor/ai-skills}"
LOG="$HOME/Library/Logs/ai-skills-autopush.log"
mkdir -p "$(dirname "$LOG")"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

cd "$REPO" 2>/dev/null || { log "repo not found: $REPO"; exit 1; }
# Local check only (no network): nothing to do unless we are ahead of origin.
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
[ "$AHEAD" -eq 0 ] && exit 0
# Only now touch the network: make sure the remote has not moved ahead.
if ! git fetch --quiet origin main >>"$LOG" 2>&1; then log "fetch failed (offline or auth)"; exit 1; fi
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ "$BEHIND" -gt 0 ]; then log "remote has $BEHIND commit(s) we don't have; not pushing"; exit 1; fi
if git push --quiet origin main >>"$LOG" 2>&1; then
  log "pushed $AHEAD commit(s) to origin/main"
else
  log "push failed (see lines above)"; exit 1
fi
