#!/usr/bin/env bash
# course-studio self-test (offline): validate the example course, build session 1 (slides, docs) and the workbooks.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="bash $S/../../premium-design-kit/scripts/run.sh"
T="$(mktemp -d)"; export PDK_OFFLINE=1; fail=0
$R "$S/validate_course.py" "$S/../examples/python_school_ar.json" >/dev/null && echo "PASS  validate" || { echo "FAIL  validate"; fail=1; }
FLAGS="--offline"; $R -c "from playwright.sync_api import sync_playwright as p; b=p().start().chromium.launch(); b.close()" >/dev/null 2>&1 || FLAGS="--offline --no-pdf"
if out="$($R "$S/build_course.py" "$S/../examples/python_school_ar.json" "$T/course" $FLAGS 2>&1)"; then
  n=$(find "$T/course" -name "*.pptx" | wc -l); d=$(find "$T/course" -name "*.docx" | wc -l); x=$(find "$T/course" -name "*.xlsx" | wc -l)
  [ "$n" -ge 2 ] && [ "$d" -ge 10 ] && [ "$x" -ge 3 ] && echo "PASS  build ($n decks, $d docx, $x xlsx)" || { echo "FAIL  build counts $n/$d/$x"; fail=1; }
else echo "FAIL  build"; echo "$out" | tail -8; fail=1; fi
echo "outputs: $T"; exit $fail
