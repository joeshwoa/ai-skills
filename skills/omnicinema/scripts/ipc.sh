#!/usr/bin/env bash
# Run omnicinema's localhost asset API as a background service, so other
# tools (devuniverse's generate_media_asset) can request assets from it.
# (The MCP tools ipc_start/ipc_stop only live for one call through call.sh —
# use this script instead.)
#   ipc.sh start [port]   (default 8787)
#   ipc.sh status
#   ipc.sh stop
# The bearer token lives in $CINEMA_ROOT/data/ipc-token.txt (0600) — never
# print it into chat. devuniverse finds it through the same CINEMA_ROOT.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="omnicinema-mcp"
CACHE_DIR="${AI_SKILLS_CACHE_DIR:-$HOME/.cache/ai-skills}/$NAME"
# shellcheck source=/dev/null
. "$SCRIPT_DIR/root.sh"
DATA="$CINEMA_ROOT/data"
mkdir -p "$DATA"
PIDFILE="$DATA/ipc.pid"; PORTFILE="$DATA/ipc.port"; LOG="$DATA/ipc.log"

alive() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }
healthy() { curl -fsS --max-time 2 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }
saved_port() { cat "$PORTFILE" 2>/dev/null || echo "${OMNICINEMA_IPC_PORT:-8787}"; }

case "${1:-status}" in
  start)
    PORT="${2:-${OMNICINEMA_IPC_PORT:-8787}}"
    [ -f "$CACHE_DIR/dist/ipc-main.js" ] || { echo "omnicinema is missing or too old — run bootstrap.sh" >&2; exit 2; }
    if alive; then echo "already running (pid $(cat "$PIDFILE"), port $(saved_port))"; exit 0; fi
    if healthy "$PORT"; then
      echo "something else already answers on port $PORT (another omnicinema? different CINEMA_ROOT?)." >&2
      echo "stop it, or start on another port: ipc.sh start 8788" >&2; exit 1
    fi
    cd "$CACHE_DIR"
    OMNICINEMA_IPC_PORT="$PORT" nohup node dist/ipc-main.js >"$LOG" 2>&1 &
    echo $! >"$PIDFILE"; echo "$PORT" >"$PORTFILE"
    for _ in $(seq 1 30); do
      if ! alive; then echo "the service exited — see $LOG:" >&2; tail -20 "$LOG" >&2; rm -f "$PIDFILE"; exit 1; fi
      if healthy "$PORT"; then
        echo "omnicinema IPC up: http://127.0.0.1:$PORT (pid $(cat "$PIDFILE"))"
        echo "token file: $DATA/ipc-token.txt"
        echo "for devuniverse, in the same shell:"
        echo "  export CINEMA_ROOT=\"$CINEMA_ROOT\" OMNICINEMA_PATHS=\"$CACHE_DIR\" OMNICINEMA_API_URL=http://127.0.0.1:$PORT"
        exit 0
      fi
      sleep 0.5
    done
    echo "did not become healthy — see $LOG" >&2; tail -20 "$LOG" >&2; exit 1 ;;
  status)
    PORT="$(saved_port)"
    if alive && healthy "$PORT"; then echo "running (pid $(cat "$PIDFILE")) on http://127.0.0.1:$PORT"
    elif alive; then echo "process $(cat "$PIDFILE") alive but not answering on $PORT — see $LOG"; exit 1
    else echo "not running"; exit 1; fi ;;
  stop)
    if alive; then
      pid="$(cat "$PIDFILE")"; kill "$pid"
      for _ in $(seq 1 20); do kill -0 "$pid" 2>/dev/null || break; sleep 0.25; done
      kill -0 "$pid" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
      echo "stopped"
    else echo "not running"; fi
    rm -f "$PIDFILE" "$PORTFILE" ;;
  *) echo "usage: ipc.sh start [port] | status | stop" >&2; exit 2 ;;
esac
