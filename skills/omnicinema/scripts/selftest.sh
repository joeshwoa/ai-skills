#!/usr/bin/env bash
# Prove the skill works on this machine (offline, free, ~1 min; --video adds a short render).
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
bash "$S/bootstrap.sh" --check
export CINEMA_ROOT="$(mktemp -d)"
n=$(bash "$S/call.sh" --list 2>/dev/null | grep -c '^[a-z_]*(' || true)
[ "$n" -ge 15 ] && ok "server starts, $n tools" || bad "tool list ($n tools)"
bash "$S/call.sh" generate_image '{"assetKind":"logo","subject":"Selftest","style":"#0f766e #f59e0b"}' >/dev/null 2>&1 && ok "logo generated" || bad "logo"
bash "$S/call.sh" generate_sfx '{"subject":"soft UI click"}' >/dev/null 2>&1 && ok "sfx generated" || bad "sfx"
bash "$S/call.sh" generate_soundtrack '{"subject":"calm focus","style":"lo-fi","durationSeconds":8}' >/dev/null 2>&1 && ok "soundtrack generated" || bad "soundtrack"
if [ "${1-}" = "--video" ]; then
  bash "$S/call.sh" run_cinema_pipeline '{"prompt":"a lighthouse keeper watching a storm at night","sceneCount":2,"shotsPerScene":1,"shotDurationSeconds":2,"width":640,"height":360,"stock":false}' >/dev/null 2>&1 && ok "video rendered" || bad "video"
fi
shopt -s nullglob
files=("$CINEMA_ROOT"/assets/*.svg "$CINEMA_ROOT"/assets/*.wav "$CINEMA_ROOT"/output/*.mp4)
if [ ${#files[@]} -eq 0 ]; then bad "no output files were produced"
else bash "$S/check_media.sh" "${files[@]}" && ok "outputs pass check_media" || bad "check_media flagged something (see above)"; fi
echo "(outputs in $CINEMA_ROOT)"
exit $FAIL
