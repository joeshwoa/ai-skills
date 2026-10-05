#!/usr/bin/env bash
# Prove the motion engines work here (temporary STUDIO_HOME). --full also renders a template video and 3D.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
C() { bash "$S/call.sh" --json "$@"; }
J() { python3 -c "import sys,json; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }
export STUDIO_HOME="$(mktemp -d)"
C motion_plan '{"brief":"Arabic kinetic hook for a reel","size":"9:16","arabic":true}' | J "d['ok']" | grep -q True && ok "router (motion_plan)" || bad "motion_plan"
C motion_compose '{"template":"kinetic_quote","size":"540x960","fields":{"quote":"مش محتاج|أغلى *موديل*"},"preview":true}' | J "d['ok']" | grep -q True && ok "compose preview (Arabic kinetic)" || bad "compose preview (needs internet once for GSAP)"
C motion_title_card '{"title":"Selftest","duration":2,"size":"640x360","fps":24}' | J "d['ok']" | grep -q True && ok "built-in template render" || bad "motion_title_card"
if [ "${1-}" = "--full" ]; then
  C motion_compose '{"template":"stat_reveal","size":"640x360","fields":{"value":97,"suffix":"%","label":"Selftest"}}' | J "d['ok']" | grep -q True && ok "compose video render" || bad "compose render"
  C motion_3d '{"preset":"title","text":"3D","duration":1,"size":"480x270","fps":12}' | J "d['ok']" | grep -q True && ok "three.js 3D" || bad "motion_3d"
fi
echo "(temp home: $STUDIO_HOME)"; exit $FAIL
