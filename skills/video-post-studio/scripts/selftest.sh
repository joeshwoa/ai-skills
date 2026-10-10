#!/usr/bin/env bash
# Prove the editing tools work here on synthetic media (temporary STUDIO_HOME, no network needed).
set -uo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; FAIL=0
ok() { echo "PASS  $1"; }; bad() { echo "FAIL  $1"; FAIL=1; }
C() { bash "$S/call.sh" --json "$@"; }
J() { python3 -c "import sys,json; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }
command -v ffmpeg >/dev/null || { echo "FAIL  ffmpeg missing (brew install ffmpeg)"; exit 1; }
export STUDIO_HOME="$(mktemp -d)"; T="$STUDIO_HOME/media"; mkdir -p "$T"
ffmpeg -v error -y -f lavfi -i testsrc2=s=640x360:r=30:d=3 -f lavfi -i smptebars=s=640x360:r=30:d=3 -f lavfi -i "color=c=red:s=640x360:r=30:d=3" \
  -filter_complex "[0][1][2]concat=n=3:v=1:a=0" -c:v libx264 -pix_fmt yuv420p "$T/shots.mp4"
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.6*sin(2*PI*1000*t)*lt(mod(t\\,0.5)\\,0.03)':s=44100:d=8" "$T/click120.wav"
n=$(C video_scene_detect "{\"path\":\"$T/shots.mp4\"}" | J "len(d['data'].get('shots',[]))")
[ "${n:-0}" -eq 3 ] && ok "scene detection (3 shots)" || bad "scene detection ($n)"
b=$(C video_beats "{\"path\":\"$T/click120.wav\"}" | J "round(d['data'].get('tempo',0))")
[ "${b:-0}" -ge 118 ] && [ "${b:-0}" -le 122 ] && ok "beat detection ($b BPM)" || bad "beats ($b)"
C video_edit "{\"timeline\":{\"size\":\"640x360\",\"clips\":[{\"src\":\"$T/shots.mp4\",\"in\":0,\"out\":3},{\"src\":\"$T/shots.mp4\",\"in\":3.5,\"out\":6,\"transition\":\"dissolve\"}]},\"name\":\"st\"}" | J "any(f.endswith('.kdenlive') for f in d['files'])" | grep -q True && ok "timeline edit → MP4 + .kdenlive" || bad "video_edit"
C video_edit "{\"timeline\":{\"size\":\"640x360\",\"clips\":[{\"src\":\"$T/shots.mp4\",\"in\":0,\"out\":3},{\"src\":\"$T/shots.mp4\",\"in\":3.5,\"out\":6,\"transition\":\"dissolve\",\"grade\":\"teal_orange\"}]},\"name\":\"pkg\"}" | J "all(v == [] for v in d['data']['project_package']['checks'].values())" | grep -q True && ok "project package: Premiere, After Effects, Resolve, Final Cut, CapCut, Avid, Kdenlive, OTIO, EDL — all checks pass" || bad "project package"
mp4=$(ls -t "$STUDIO_HOME"/projects/*/video/st*.mp4 2>/dev/null | head -1)
[ -n "$mp4" ] && { C video_qc "{\"path\":\"$mp4\"}" | J "d['ok']" | grep -q True && ok "QC report" || bad "video_qc"; }
C video_export_interchange "{\"timeline\":{\"size\":\"640x360\",\"clips\":[{\"src\":\"$T/shots.mp4\",\"in\":0,\"out\":3}]},\"format\":\"all\"}" | J "d['ok']" | grep -q True && ok "FCPXML/OTIO/EDL export" || bad "interchange"
echo "(temp home: $STUDIO_HOME)"; exit $FAIL
