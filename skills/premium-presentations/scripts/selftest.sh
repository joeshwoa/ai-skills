#!/usr/bin/env bash
# premium-presentations self-test (offline): build + validate the three example decks, render previews.
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; R="bash $S/../../premium-design-kit/scripts/run.sh"
T="$(mktemp -d)"; export PDK_OFFLINE=1; fail=0
for ex in full_types_deck_spec v2_types_deck_spec lesson_deck_ar; do
  if $R "$S/build_deck.py" "$S/../examples/$ex.json" "$T/$ex.pptx" --offline >/dev/null 2>&1 && $R "$S/validate_deck.py" "$T/$ex.pptx" >/dev/null 2>&1 \
     && $R "$S/render_preview.py" "$S/../examples/$ex.json" "$T/$ex.html" --offline >/dev/null 2>&1; then echo "PASS  $ex"; else echo "FAIL  $ex"; fail=1; fi
done
echo "outputs: $T"; exit $fail
