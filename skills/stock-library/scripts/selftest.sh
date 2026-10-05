#!/usr/bin/env bash
# Prove the stock tools work here (temporary STUDIO_HOME; uses only keyless providers).
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
C() { bash "$S/call.sh" --json "$@"; }
J() { python3 -c "import sys,json; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }
export STUDIO_HOME="$(mktemp -d)"
C stock_sources '{}' | J "d['ok']" | grep -q True && ok "stock_sources (keys.json template written)" || bad "stock_sources"
n=$(C stock_search '{"query":"coffee","kind":"photo","count":4,"providers":"openverse","project":"st"}' | J "len(d['data'].get('results',[]))")
[ "${n:-0}" -ge 1 ] && ok "search Openverse photos ($n)" || bad "search (network?)"
C stock_download '{"ids":["1"],"quality":"sd","project":"st"}' | J "len(d['data'].get('downloaded',[]))" | grep -q 1 && ok "download + licence sidecar" || bad "download"
C stock_credits '{"project":"st"}' | J "d['ok']" | grep -q True && ok "credits" || bad "credits"
C stock_icon '{"query":"mdi:coffee","project":"st"}' | J "d['ok']" | grep -q True && ok "icon (Iconify)" || bad "icon"
echo "(temp home: $STUDIO_HOME)"; exit $FAIL
