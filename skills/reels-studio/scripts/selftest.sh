#!/usr/bin/env bash
# Proves reels-studio works on this machine. Writes only to a temp folder.
#   bash scripts/selftest.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"
PY="$(cat "$HOME/.config/ai-skills/reels-studio.python" 2>/dev/null || true)"
[ -x "${PY:-}" ] || PY="$(command -v python3)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
pass=0; fail=0; skip=0
ok()   { echo "  ✓ $1"; pass=$((pass+1)); }
bad()  { echo "  ✗ $1"; fail=$((fail+1)); }
skp()  { echo "  – $1 (skipped)"; skip=$((skip+1)); }
TODAY=2026-10-03

echo "reels-studio selftest ($PY)"

# 1. good examples validate clean
for ex in "$SKILL"/examples/*.json; do
  if "$PY" "$HERE/validate_script.py" "$ex" --today "$TODAY" --strict >"$T/v.txt" 2>&1; then ok "valid: $(basename "$ex")"
  else bad "should validate: $(basename "$ex")"; cat "$T/v.txt"; fi
done

# 2. the broken fixture is rejected, for the right reasons
"$PY" "$HERE/validate_script.py" "$SKILL/examples/tests/broken_spec.json" --today "$TODAY" --json >"$T/b.json" 2>&1
rc=$?
[ $rc -eq 1 ] && ok "broken fixture rejected (exit 1)" || bad "broken fixture exit $rc (want 1)"
"$PY" - "$T/b.json" <<'PYEOF' && ok "broken fixture: every planted fault reported" || bad "broken fixture: a planted fault was missed"
import json, sys
r = json.load(open(sys.argv[1]))
msgs = " | ".join(i["where"] + ": " + i["msg"] for i in r["errors"] + r["warnings"])
need = ["brief.audience", "hook must land", "placeholder", "laser_show", "no CTA", "MSA word 'سوف'",
        "claim needs proof", "engagement bait", "checked 63 days", "business account", "no 'checked' date",
        "7 hashtags", "estimated 25s"]
missing = [n for n in need if n not in msgs]
if missing:
    print("    missing:", missing); sys.exit(1)
PYEOF

# 2b. ads and long-form rules
"$PY" "$HERE/validate_script.py" "$SKILL/examples/tests/broken_ad.json" --today "$TODAY" --json >"$T/ba.json" 2>&1
"$PY" - "$T/ba.json" <<'PYEOF' && ok "ad fixture: slot overrun, bumper limit, bad cutdowns, no CTA, late brand, personal attribute" || bad "ad fixture: a planted fault was missed"
import json, sys
r = json.load(open(sys.argv[1]))
msgs = " | ".join(i["msg"] for i in r["errors"] + r["warnings"])
need = ["ad slot is 15s", "runs ~14.0s for a 6s slot", "scene 9 doesn't exist", "no cutdown with placement 'youtube_bumper' fits", "youtube_bumper allows at most 6s",
        "an ad needs a CTA", "isn't seen or heard in the first 5 s", "personal attribute", "cuts headlines around 40"]
missing = [n for n in need if n not in msgs]
if missing:
    print("    missing:", missing); sys.exit(1)
PYEOF
"$PY" "$HERE/validate_script.py" "$SKILL/examples/tests/broken_long.json" --today "$TODAY" --json >"$T/bl.json" 2>&1
"$PY" - "$T/bl.json" <<'PYEOF' && ok "long-form fixture: late hook, greeting, 230 s scene, <3 chapters, title >100" || bad "long-form fixture: a planted fault was missed"
import json, sys
r = json.load(open(sys.argv[1]))
msgs = " | ".join(i["msg"] for i in r["errors"] + r["warnings"])
need = ["first 10 s", "opens with a greeting", "one scene runs ~230s", "YouTube needs at least 3", "> YouTube's 100", "thumbnail"]
missing = [n for n in need if n not in msgs]
if missing:
    print("    missing:", missing); sys.exit(1)
PYEOF

# 3. templates: every one renders, and every one is refused by the validator until filled
for tp in "$SKILL"/templates/*.json; do
  n="$(basename "$tp" .json)"
  if "$PY" "$HERE/validate_script.py" "$tp" --today "$TODAY" >/dev/null 2>&1; then bad "template $n passed validation while still blank"
  else ok "template $n blocked until filled"; fi
  "$PY" "$HERE/render_script.py" "$tp" --out "$T/tpl" --formats html --name "$n" >/dev/null 2>&1 && ok "template $n renders" || bad "template $n failed to render"
done

# 4. new_spec scaffolds and refuses to overwrite
"$PY" "$HERE/new_spec.py" --template talking_head --language ar-EG --brand neoai --out "$T/p/spec.json" >/dev/null && ok "new_spec writes a spec" || bad "new_spec failed"
"$PY" "$HERE/new_spec.py" --template talking_head --language ar-EG --out "$T/p/spec.json" >/dev/null 2>&1 && bad "new_spec overwrote a file" || ok "new_spec refuses to overwrite"

# 5. render the Neo AI example: DOCX, teleprompter, SRT, and PDF if an engine exists
EX="$SKILL/examples/neoai_expensive_model_ar-EG.json"
if "$PY" -c 'import docx' 2>/dev/null; then
  "$PY" "$HERE/render_script.py" "$EX" --out "$T/out" --formats docx,teleprompter,srt --name ex >/dev/null 2>&1 && ok "docx/teleprompter/srt rendered" || bad "docx render failed"
  "$PY" - "$T/out/ex.docx" <<'PYEOF' && ok "docx: RTL paragraphs, Cairo, editor blue + talent red" || bad "docx content check failed"
import sys, zipfile
x = zipfile.ZipFile(sys.argv[1]).read("word/document.xml").decode()
assert "<w:bidi/>" in x, "no bidi paragraphs"
assert 'w:cs="Cairo' in x, "Cairo not set for complex script"
assert "1D55A3" in x and "8A1538" in x, "house colours missing"
assert "<w:bCs" in x and "<w:szCs" in x, "complex-script size/bold missing"
PYEOF
  grep -q -- "-->" "$T/out/ex_captions_ESTIMATED.srt" && ok "srt has cues" || bad "srt empty"
  "$PY" -c 'import sys; L=[l.rstrip("\n") for l in open(sys.argv[1], encoding="utf-8")]; sys.exit(any(len(l) > 42 for l in L if l and "-->" not in l and not l.isdigit()))' "$T/out/ex_captions_ESTIMATED.srt" && ok "srt lines ≤ 40–42 chars" || bad "srt line too long"
else
  skp "python-docx not installed — run bash scripts/setup.sh"
fi
if "$PY" "$HERE/render_script.py" "$EX" --out "$T/pdf" --formats pdf --name ex >"$T/pdf.log" 2>&1; then
  ok "pdf rendered ($(grep 'pdf engine' "$T/pdf.log" | cut -d: -f2 | tr -d ' '))"
  if command -v pdffonts >/dev/null 2>&1; then
    pdffonts "$T/pdf/ex.pdf" | grep -q Cairo && ok "pdf embeds Cairo" || bad "pdf does not embed Cairo"
  else skp "pdffonts not installed — font embedding not checked"; fi
else
  skp "no PDF engine on this machine — $(tail -1 "$T/pdf.log")"
fi

# 5b. long-form timecodes/chapters and ad cutdowns reach the document
LF="$SKILL/examples/neoai_model_myth_youtube_ar-EG.json"; AD="$SKILL/examples/neoai_diploma_ad_ar-EG.json"
"$PY" "$HERE/render_script.py" "$LF" --out "$T/lf" --formats html --name lf >/dev/null 2>&1 \
  && grep -q "00:00 المقدمة" "$T/lf/lf.html" && grep -q "(≈ 01:" "$T/lf/lf.html" \
  && ok "long-form: scene timecodes + YouTube chapters starting 00:00" || bad "long-form timecodes/chapters missing"
"$PY" "$HERE/render_script.py" "$AD" --out "$T/ad" --formats html,production --name ad >/dev/null 2>&1 \
  && grep -q "CUTDOWNS" "$T/ad/ad.html" && grep -q "6s bumper — 6 s target" "$T/ad/ad.html" && grep -q "Note: cutdown 15s = scenes 1, 3, 5" "$T/ad/ad_for_production.txt" \
  && ok "ad: cutdowns in the script and the production file" || bad "ad cutdowns missing"

# 6. loose spec shapes, awkward paths, malformed input, stale output
E="$SKILL/examples/tests/edge_spec.json"; OD="$T/out dir #1"
"$PY" "$HERE/render_script.py" "$E" --out "$OD" --formats html,teleprompter,srt,production --name edge >/dev/null 2>&1 \
  && ok "loose shapes (meta dict, string lists, arz) render into a path with spaces/#" || bad "edge spec failed to render"
grep -q 'dir="rtl"' "$OD/edge.html" 2>/dev/null && ok "arz renders right-to-left" || bad "arz not RTL"
printf '{"language":"ar-EG","title":"x","brief":{"trend_refs":["s"]},"scenes":[{"blocks":[{"type":"dialogue","lines":[{"bad":1}]}]}, 7]}' > "$T/mal.json"
"$PY" "$HERE/validate_script.py" "$T/mal.json" --json > "$T/mal.out" 2>&1; rc=$?
{ [ $rc -eq 1 ] && ! grep -q Traceback "$T/mal.out"; } && ok "malformed spec → errors, no traceback" || bad "malformed spec crashed the validator (rc=$rc)"
mkdir -p "$T/stale" && echo junk > "$T/stale/ex.pdf"
CHROME_PATH=/usr/bin/true "$PY" "$HERE/render_script.py" "$EX" --out "$T/stale" --formats pdf --pdf-engine chrome --name ex >/dev/null 2>&1 \
  && bad "a leftover PDF was reported as a fresh render" || ok "stale PDF is never reported as success"

# 7. idea scoring ranks and applies floors
cat > "$T/ideas.json" <<'J'
{"brief":"t","ideas":[
 {"title":"weak fit","scores":{"hook":5,"audience_fit":1,"trend_timing":5,"shareability":5,"feasibility":5,"brand_fit":5,"originality":5}},
 {"title":"solid","scores":{"hook":4,"audience_fit":4,"trend_timing":3,"shareability":4,"feasibility":4,"brand_fit":4,"originality":3}},
 {"title":"meh","scores":{"hook":2,"audience_fit":3,"trend_timing":2,"shareability":2,"feasibility":3,"brand_fit":3,"originality":2}}]}
J
"$PY" "$HERE/score_ideas.py" "$T/ideas.json" > "$T/board.md" 2>&1
"$PY" - "$T/board.md" <<'PYEOF' && ok "idea board ranks and sinks floor failures" || bad "idea board order wrong"
import sys
rows = [l for l in open(sys.argv[1]) if l.startswith("| ") and l[2].isdigit()]
order = [r.split("|")[3].strip() for r in rows]
assert order == ["solid", "meh", "weak fit"], order
PYEOF

echo "$pass passed, $fail failed, $skip skipped"
[ $fail -eq 0 ]
