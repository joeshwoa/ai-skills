#!/usr/bin/env bash
# premium-spreadsheets self-test: build every example (+ recalculation check when LibreOffice exists) and the presets.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="bash $S/../../premium-design-kit/scripts/run.sh"
T="$(mktemp -d)"; fail=0
for f in "$S"/../examples/*.json; do n="$(basename "$f" .json)"
  if out="$($R "$S/build_sheet.py" "$f" "$T/$n.xlsx" 2>&1)"; then echo "PASS  $n"; else echo "FAIL  $n"; echo "$out" | tail -5; fail=1; fi
done
if $R -c "
import sys, json; sys.path.insert(0, '$S')
from presets import gradebook, attendance, question_bank, tracker, schedule
specs = [gradebook(['A','B'], [{'name':'Q1','max':10,'weight':1}]), attendance(['A'], ['W1','W2']),
         question_bank([{'q':'2+2?','options':['3','4'],'answer':1}]), tracker([{'task':'x','due':'2026-01-01'}]),
         schedule([{'title':'Intro','hours':1.5}])]
for i, s in enumerate(specs): json.dump(s, open('$T/p%d.json' % i, 'w'))
"; then pf=0; for i in 0 1 2 3 4; do $R "$S/build_sheet.py" "$T/p$i.json" "$T/p$i.xlsx" >/dev/null 2>&1 || { echo "FAIL  preset $i"; pf=1; fail=1; }; done; [ $pf = 0 ] && echo "PASS  presets"; else echo "FAIL  presets (python)"; fail=1; fi
echo "outputs: $T"; exit $fail
