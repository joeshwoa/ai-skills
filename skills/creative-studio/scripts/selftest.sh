#!/usr/bin/env bash
# Prove the studio works on this machine (writes only into a temporary STUDIO_HOME).
#   selftest.sh          quick: tools listed, palette, a designed post, a motion title, a JSON-timeline edit
#   selftest.sh --full   + brand kit with logo suite, voiceover (online voices), captions (Whisper, downloads a model)
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
C() { bash "$S/call.sh" --json "$@"; }
field() { python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$1') if not isinstance(d.get('$1'),list) else '\n'.join(map(str,d.get('$1'))))"; }
TMP="$(mktemp -d)"; export STUDIO_HOME="$TMP"
n=$(bash "$S/call.sh" list 2>/dev/null | grep -c '^[a-z]' || true)
[ "$n" -ge 100 ] && ok "studio starts, $((n - 1)) tools" || bad "tool list ($n)"
C brand_palette '{"brief":"organic juice bar, fresh"}' | field ok | grep -q True && ok "palette" || bad "palette"
out=$(C design_create '{"template":"headline","size":"ig_square","style":"nile","content":{"eyebrow":"جديد","headline":"قهوة *مختصة* كل يوم","cta":"اطلب دلوقتي"}}')
echo "$out" | field ok | grep -q True && [ -f "$(echo "$out" | field previews | head -1)" ] && ok "Arabic social post + preview" || bad "design_create"
out=$(C motion_title_card '{"title":"Selftest","duration":2,"size":"640x360","fps":24}')
echo "$out" | field ok | grep -q True && ok "motion title (Chromium frames → MP4)" || bad "motion_title_card"
mp4=$(echo "$out" | field files | grep '\.mp4$' | head -1)
if [ -n "$mp4" ]; then
  out=$(C video_edit "{\"timeline\":{\"size\":\"640x360\",\"clips\":[{\"src\":\"$mp4\"},{\"color\":\"#224466\",\"duration\":1,\"transition\":\"dissolve\"}]},\"name\":\"selftest\"}")
  echo "$out" | field files | grep -q '\.kdenlive$' && ok "video edit → MP4 + .kdenlive" || bad "video_edit"
fi
if [ "${1-}" = "--full" ]; then
  C brand_create '{"name":"Selftest Café","sector":"coffee","name_ar":"كافيه تجربة","concepts":3}' | field ok | grep -q True && ok "brand kit + logo suite" || bad "brand_create"
  out=$(C audio_voiceover '{"text":"أهلاً بيكم، ده اختبار صوت.","voice":"auto"}')
  wav=$(echo "$out" | field files | grep '\.wav$' | head -1)
  [ -n "$wav" ] && ok "Egyptian voiceover" || bad "audio_voiceover (needs internet)"
  [ -n "$wav" ] && { C audio_transcribe "{\"path\":\"$wav\",\"language\":\"ar\",\"speed\":\"fast\",\"allow_download\":true}" | field ok | grep -q True && ok "transcription" || bad "audio_transcribe"; }
fi
bash "$S/call.sh" studio_doctor | sed -n '1,2p;/Departments ready/p'
echo "(temp home: $TMP)"
exit $FAIL
