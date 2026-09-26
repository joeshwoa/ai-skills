#!/usr/bin/env bash
# Prove the skill works on this machine.
#   selftest.sh          quick: server starts, tools listed, dry run plans a project
#   selftest.sh --full   + generates a real project in a temp root and runs verify_project.sh
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
bash "$S/bootstrap.sh" --check
n=$(bash "$S/call.sh" --list 2>/dev/null | grep -c '^[a-z_]*(' || true)
[ "$n" -ge 13 ] && ok "server starts, $n tools" || bad "tool list ($n tools)"
TMP="$(mktemp -d)"; export DEVUNIVERSE_ROOT="$TMP"
out=$(bash "$S/call.sh" init_dev_universe '{"project_type":"flutter_app","name":"Selftest","description":"A notes app with sign in and offline mode.","dry_run":true}' 2>&1)
echo "$out" | grep -q "dry run" && [ ! -d "$TMP/projects/selftest" ] && ok "dry run plans without writing" || bad "dry run"
if [ "${1-}" = "--full" ]; then
  bash "$S/call.sh" init_dev_universe '{"project_type":"flutter_app","name":"Selftest","description":"A notes app with sign in and offline mode."}' >/dev/null 2>&1 \
    && ok "project generated" || bad "project generation"
  bash "$S/verify_project.sh" "$TMP/projects/selftest" && ok "generated project verified" || bad "verify_project"
fi
echo "(temp root: $TMP)"
exit $FAIL
