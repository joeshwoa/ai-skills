#!/usr/bin/env bash
# End-to-end proof, no accounts needed: mock "portal with no API" → browserd (headless Chrome) → real n8n engine.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; K="$(dirname "$S")"; AUTO="$K/../automation-studio/scripts/auto.sh"
T="$(mktemp -d)"; PY="$(command -v python3)"; PASS=0; FAIL=0; PIDS=()
cleanup(){ for p in "${PIDS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null; done; rm -rf "$T"; }; trap cleanup EXIT
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }; bad(){ echo "  ✗ $1"; FAIL=$((FAIL+1)); }
chk(){ if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }
export NX_SECRET_MOCK_USER=demo NX_SECRET_MOCK_PASS=demo-pass NX_HOME="$T/home"

echo "== static"
chk "browserd.py parses" "$PY -c 'import ast;ast.parse(open(\"$S/browserd.py\").read())'"
chk "recipes validate" "$PY $S/browserd.py validate $K/recipes/orders-scrape.json"
chk "bad recipe is rejected" "! $PY $S/browserd.py validate <(echo '{\"steps\":[{\"nope\":1}]}')"
chk "ladder: captcha => human in the loop first" "$PY $S/ladder.py --probe <(echo '{\"protection\":[\"recaptcha\"],\"signals\":[]}') --json | $PY -c 'import json,sys;r=json.load(sys.stdin);sys.exit(0 if r[0][\"rung\"]==\"human_in_loop\" else 1)'"
chk "ladder: official node wins" "$PY $S/ladder.py --has-node --json | $PY -c 'import json,sys;sys.exit(0 if json.load(sys.stdin)[0][\"rung\"]==\"native_node\" else 1)'"
chk "ladder: ToS forbids => no scraping rung first" "$PY $S/ladder.py --forbidden --json | $PY -c 'import json,sys;r=json.load(sys.stdin);sys.exit(0 if r[0][\"rung\"] not in (\"browser_recipe\",\"browser_agent\",\"hidden_json\",\"browser_attach\") else 1)'"

echo "== live: mock site + browserd"
$PY "$S/mock/mocksite.py" 7799 >/dev/null 2>&1 & PIDS+=($!)
$PY "$S/browserd.py" serve --allow 127.0.0.1 --allow-private --port 7788 --session-dir "$T/sess" >"$T/bd.log" 2>&1 & PIDS+=($!)
for i in $(seq 1 40); do curl -s localhost:7788/health >/dev/null && break; sleep 0.5; done
post(){ curl -s -X POST localhost:7788$1 -H 'Content-Type: application/json' -d "$2"; }
R=$(post /run '{"recipe_name":"orders-scrape","vars":{"base":"http://127.0.0.1:7799"},"session":"t"}')
chk "login + 3 pages => 25 rows" "echo '$R' | $PY -c 'import json,sys;d=json.load(sys.stdin);sys.exit(0 if d[\"ok\"] and len(d[\"data\"][\"orders\"])==25 else 1)'"
chk "secret never appears in the response" "! echo '$R' | grep -q demo-pass"
chk "domain allow-list blocks other hosts" "post /run '{\"steps\":[{\"goto\":\"https://example.org\"}],\"session\":\"t\"}' | grep -q 'not in --allow'"
chk "captcha => needs_human + screenshot" "post /run '{\"recipe_name\":\"captcha-demo\",\"vars\":{\"base\":\"http://127.0.0.1:7799\"},\"session\":\"t\"}' | grep -q needs_human"
chk "eval step is off by default" "post /run '{\"steps\":[{\"goto\":\"http://127.0.0.1:7799/orders\"},{\"eval\":\"1+1\"}],\"session\":\"t\"}' | grep -q disabled"
O=$(post /observe '{"session":"t","url":"http://127.0.0.1:7799/order/1005"}')
chk "observe marks page text as untrusted data" "echo '$O' | grep -q untrusted"
chk "act: click by ref moves the browser" "post /act '{\"session\":\"t\",\"action\":{\"type\":\"goto\",\"url\":\"http://127.0.0.1:7799/orders\"}}' | grep -q '\"ok\": true'"

echo "== n8n engine (real), flows from patterns"
DOC=$(bash "$AUTO" doctor 2>/dev/null || true)
if [ -f "$AUTO" ] && echo "$DOC" | grep -q "n8n *: *[0-9]"; then
  for p in "01-browser-recipe:orders-scrape" "02-agent-browser-tools:x" "03-mcp-bridge:x"; do
    d="${p%%:*}"; r="${p##*:}"; mkdir -p "$T/$d"
    sed -e "s#__RECIPE__#$r#g" -e 's#__PATH__#web-run#' -e 's#__BROWSERD__#http://127.0.0.1:7788#g' -e 's#__SESSION__#shop#' "$K/patterns/$d/workflow.ts" > "$T/$d/workflow.ts"
    chk "$d builds + validates" "bash $AUTO build $T/$d/workflow.ts -o $T/$d/flow.json"
    [ -f "$K/patterns/$d/cases.json" ] && chk "$d test cases pass" "bash $AUTO test $T/$d/flow.json $K/patterns/$d/cases.json"
  done
else
  echo "  (n8n not set up — skipping engine tests; run: bash ../automation-studio/scripts/setup_n8n.sh --yes)"
fi
echo "---- $PASS passed, $FAIL failed"; [ "$FAIL" = 0 ]
