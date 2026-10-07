#!/usr/bin/env bash
# premium-documents self-test (offline): every example → docx (+ pdf when Chromium exists) + validator.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="bash $S/../../premium-design-kit/scripts/run.sh"
T="$(mktemp -d)"; export PDK_OFFLINE=1; fail=0
PDF=1; $R -c "from playwright.sync_api import sync_playwright as p; b=p().start().chromium.launch(); b.close()" >/dev/null 2>&1 || { PDF=0; echo "NOTE  Chromium missing — DOCX only (run premium-design-kit/scripts/setup.sh)"; }
for f in "$S"/../examples/*.json; do
  n="$(basename "$f" .json)"
  if [ $PDF = 1 ]; then flags="--offline"; files="$T/$n.pdf $T/$n.docx"; else flags="--offline --docx-only"; files="$T/$n.docx"; fi
  if $R "$S/build_doc.py" "$f" "$T/$n" $flags >/dev/null 2>&1 && $R "$S/validate_doc.py" $files >/dev/null 2>&1; then echo "PASS  $n"; else echo "FAIL  $n"; fail=1; fi
done
echo "outputs: $T"; exit $fail
