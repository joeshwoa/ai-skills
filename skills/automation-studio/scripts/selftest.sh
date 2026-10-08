#!/usr/bin/env bash
# automation-studio self-test: proves the toolkit works on this machine.
#   bash scripts/selftest.sh            full (patterns' live cases call public APIs)
#   AUTOKIT_OFFLINE=1 bash scripts/selftest.sh   no network
#   bash scripts/selftest.sh 08         only patterns matching "08"
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; SKILL="$(dirname "$HERE")"
A="bash $HERE/auto.sh"
ONLY="${1:-}"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
pass=0; fail=0
ok()  { echo "  ✓ $*"; pass=$((pass+1)); }
bad() { echo "  ✗ $*"; fail=$((fail+1)); }

echo "== python modules compile"
python3 -m py_compile "$HERE"/*.py && ok "scripts compile" || bad "compile error"
rm -rf "$HERE/__pycache__"

echo "== doctor"
$A doctor > "$WORK/doctor.txt" 2>&1 && ok "$(grep -m1 '^n8n  *: ' "$WORK/doctor.txt" | tr -s ' ')" || { bad "doctor failed (run setup_n8n.sh)"; cat "$WORK/doctor.txt"; exit 1; }

for d in "$SKILL"/patterns/*/; do
  n=$(basename "$d"); [ -n "$ONLY" ] && [[ "$n" != *"$ONLY"* ]] && continue
  echo "== $n"
  for ts in "$d"workflow.ts "$d"sub-workflow.ts; do
    [ -f "$ts" ] || continue
    base=$(basename "$ts" .ts); out="$WORK/$n-$base.json"
    $A build "$ts" -o "$out" > "$WORK/b.txt" 2>&1 && grep -q "✅" "$WORK/b.txt" && ok "build+validate $base" || { bad "build $base"; tail -5 "$WORK/b.txt"; continue; }
    cases="$d$( [ "$base" = workflow ] && echo cases.json || echo "$base.cases.json")"
    [ -f "$cases" ] || continue
    $A test "$out" "$cases" > "$WORK/t.txt" 2>&1 && ok "$(tail -1 "$WORK/t.txt" | sed 's/^---- //') ($base)" || { bad "tests $base"; grep -E "❌|✗" "$WORK/t.txt" | head -8; }
  done
  for t in node-red make zapier power-automate pipedream activepieces; do
    $A convert "$WORK/$n-workflow.json" --to "$t" -o "$WORK/conv-$n-$t" > /dev/null 2>&1 || { bad "convert $t"; continue; }
  done
  ok "converted to 6 platforms"
done

echo "== diagram"
first=$(ls "$WORK"/*-workflow.json 2>/dev/null | head -1)
if [ -n "$first" ]; then
  $A diagram "$first" -o "$WORK/diag" --formats svg,html,mmd,excalidraw > /dev/null 2>&1 && ls "$WORK/diag"/*.svg >/dev/null 2>&1 && ok "diagram svg/html/mmd/excalidraw" || bad "diagram"
fi
echo
echo "selftest: $pass passed, $fail failed"
[ "$fail" = 0 ]
