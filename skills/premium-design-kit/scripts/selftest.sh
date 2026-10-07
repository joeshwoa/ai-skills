#!/usr/bin/env bash
# premium-design-kit self-test (offline): tokens, chart, art, and one build per document skill.
#   bash selftest.sh [--keep]     → PASS/FAIL per check; outputs in a temp folder (kept with --keep)
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SK="$(cd "$S/../.." && pwd)"
R="bash $S/run.sh"
T="$(mktemp -d)"; export PDK_OFFLINE=1
pass=0; fail=0
ok(){ echo "PASS  $1"; pass=$((pass+1)); }; ko(){ echo "FAIL  $1"; echo "$2" | tail -5 | sed 's/^/      /'; fail=$((fail+1)); }
check(){ local name="$1"; shift; out="$("$@" 2>&1)" && ok "$name" || ko "$name" "$out"; }
check "python deps"   $R -c "import pptx, docx, openpyxl, matplotlib, arabic_reshaper, bidi, PIL; print('ok')"
check "themes"        $R -c "from pdk.themes import THEMES, tokens; assert len(THEMES) >= 24; [tokens(t) for t in THEMES]"
check "arabic tokens" $R -c "from pdk.themes import get_theme, tokens; t=tokens(get_theme('plain-pro'), arabic=True); assert t['dir']=='rtl'"
check "chart"         $R "$S/kit.py" chart "$SK/premium-design-kit/examples/chart.json" "$T/chart.png"
check "art"           $R "$S/kit.py" art geo "$T/art.jpg" --w 800 --h 450
check "deck (pptx)"   $R "$SK/premium-presentations/scripts/build_deck.py" "$SK/premium-presentations/examples/v2_types_deck_spec.json" "$T/deck.pptx" --offline
check "deck valid"    $R "$SK/premium-presentations/scripts/validate_deck.py" "$T/deck.pptx"
check "doc (docx)"    $R "$SK/premium-documents/scripts/build_doc.py" "$SK/premium-documents/examples/report_en.json" "$T/report" --offline --docx-only
if $R -c "from playwright.sync_api import sync_playwright as p; b=p().start().chromium.launch(); b.close()" >/dev/null 2>&1; then
  check "doc (pdf)"   $R "$SK/premium-documents/scripts/build_doc.py" "$SK/premium-documents/examples/worksheet_ar.json" "$T/ws" --offline --pdf-only
else echo "SKIP  doc (pdf) — Chromium not installed (bash setup.sh)"; fi
check "sheet (xlsx)"  $R "$SK/premium-spreadsheets/scripts/build_sheet.py" "$SK/premium-spreadsheets/examples/budget_en.json" "$T/budget.xlsx"
check "course spec"   $R "$SK/course-studio/scripts/validate_course.py" "$SK/course-studio/examples/python_school_ar.json"
echo "---- $pass passed, $fail failed  (outputs: $T)"
[ "${1:-}" = "--keep" ] || { [ $fail -eq 0 ] && rm -rf "$T"; }
[ $fail -eq 0 ]
