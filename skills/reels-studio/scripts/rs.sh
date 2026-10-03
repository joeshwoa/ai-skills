#!/usr/bin/env bash
# One entry point that uses the python setup.sh chose.
#   bash scripts/rs.sh new --template talking_head --language ar-EG --brand neoai --out p/spec.json
#   bash scripts/rs.sh validate p/spec.json [--strict]
#   bash scripts/rs.sh render   p/spec.json --out p/out [--formats pdf,docx,teleprompter,srt]
#   bash scripts/rs.sh score    p/ideas.json [--md p/ideas.md]
#   bash scripts/rs.sh selftest
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(cat "$HOME/.config/ai-skills/reels-studio.python" 2>/dev/null || true)"
[ -x "${PY:-}" ] || PY="$(command -v python3)"
cmd="${1:-}"; shift || true
case "$cmd" in
  new)      exec "$PY" "$HERE/new_spec.py" "$@";;
  validate) exec "$PY" "$HERE/validate_script.py" "$@";;
  render)   exec "$PY" "$HERE/render_script.py" "$@";;
  score)    exec "$PY" "$HERE/score_ideas.py" "$@";;
  selftest) exec bash "$HERE/selftest.sh" "$@";;
  *) sed -n '2,8p' "$0"; exit 2;;
esac
