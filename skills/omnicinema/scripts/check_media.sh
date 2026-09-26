#!/usr/bin/env bash
# Check what omnicinema produced before showing it to the user.
#   check_media.sh <file> [file ...]
# Images (svg/png/jpg): opens/parses, size; SVGs are rendered with rsvg-convert
#   to <file>.check.png so you can LOOK at it (Read the PNG) before presenting.
# Audio (wav/mp3/ogg): duration, integrated loudness (LUFS), true peak,
#   share of silence — flags silent, clipped or far-too-quiet files.
# Video (mp4/webm/mov): duration, resolution, fps, audio present, loudness,
#   black-frame share; writes <file>.contact.png (a frame every ~2 s) to LOOK at.
# Exit 0 all OK · 1 at least one file needs attention · 2 usage/tooling error.
set -uo pipefail
[ $# -ge 1 ] || { echo "usage: check_media.sh <file> [file ...]" >&2; exit 2; }
have() { command -v "$1" >/dev/null 2>&1; }
have ffprobe || { echo "ffprobe (ffmpeg) is required for audio/video checks" >&2; }
BAD=0

loudness() { # prints "I=<lufs> TP=<dbtp>"
  ffmpeg -hide_banner -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 |
    awk '/Integrated loudness:/{f=1} f&&/I:/{i=$2} f&&/Peak:/{p=$2} END{printf "I=%s TP=%s", i, p}'
}
silence_share() { # percent of the file below -50 dB for >=0.5 s
  local dur="$1" f="$2"
  ffmpeg -hide_banner -nostats -i "$f" -af silencedetect=n=-50dB:d=0.5 -f null - 2>&1 |
    awk -v d="$dur" '/silence_duration/{s+=$NF} END{ if (d>0) printf "%.0f", 100*s/d; else print 0 }'
}

for f in "$@"; do
  if [ ! -s "$f" ]; then echo "FAIL  $f — missing or empty"; BAD=1; continue; fi
  ext="$(echo "${f##*.}" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in
    svg)
      if ! python3 -c "import sys,xml.dom.minidom as m; m.parse(sys.argv[1])" "$f" 2>/dev/null; then
        echo "FAIL  $f — not valid XML/SVG"; BAD=1; continue; fi
      if have rsvg-convert; then
        bg=()
        case "$f" in *-reversed*) bg=(-b "#111827") ;; esac   # reversed logos are light-on-dark
        if rsvg-convert -w 1024 ${bg[@]+"${bg[@]}"} "$f" -o "$f.check.png" 2>/dev/null; then
          echo "OK    $f — valid SVG; preview $f.check.png (look at it)"
        else echo "FAIL  $f — rsvg-convert could not render it"; BAD=1; fi
      else echo "OK    $f — valid XML (install librsvg / rsvg-convert to render a preview)"; fi ;;
    png|jpg|jpeg|webp)
      dims="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f" 2>/dev/null)"
      if [ -n "$dims" ]; then echo "OK    $f — image ${dims}"; else echo "FAIL  $f — unreadable image"; BAD=1; fi ;;
    wav|mp3|ogg|m4a|flac)
      dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)"
      [ -n "$dur" ] || { echo "FAIL  $f — unreadable audio"; BAD=1; continue; }
      l="$(loudness "$f")"; i="${l#I=}"; i="${i%% *}"; tp="${l##*TP=}"
      sil="$(silence_share "$dur" "$f")"
      note=""
      if awk -v d="$dur" 'BEGIN{exit !(d+0 < 0.5)}'; then
        # LUFS needs >= 400 ms of audio; judge very short effects by their peak.
        pk="$(ffmpeg -hide_banner -nostats -i "$f" -af volumedetect -f null - 2>&1 | awk '/max_volume/{print $5}')"
        i="n/a (short)"; tp="${pk:-?}"
        awk -v p="$pk" 'BEGIN{exit !(p=="" || p+0 < -30)}' && note="$note too quiet/silent;"
      else
        awk -v i="$i" 'BEGIN{exit !(i=="" || i+0 < -30)}' && note="$note too quiet/silent;"
      fi
      awk -v p="$tp" 'BEGIN{exit !(p+0 > -0.5)}' && note="$note peaks near 0 dBTP (clipping risk);"
      [ "${sil:-0}" -gt 60 ] && note="$note ${sil}% silence;"
      printf '%-5s %s — %.1fs, %s LUFS, peak %s dBTP, %s%% silence%s\n' \
        "$([ -n "$note" ] && echo WARN || echo OK)" "$f" "$dur" "$i" "$tp" "$sil" "${note:+ — $note}"
      [ -n "$note" ] && BAD=1 ;;
    mp4|webm|mov|mkv)
      info="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$f" 2>/dev/null)"
      dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)"
      [ -n "$info" ] && [ -n "$dur" ] || { echo "FAIL  $f — unreadable video"; BAD=1; continue; }
      IFS=, read -r w h fr <<<"$info"
      fps="$(awk -v r="$fr" 'BEGIN{split(r,a,"/"); printf "%.2f", (a[2]?a[1]/a[2]:a[1])}')"
      has_audio="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" 2>/dev/null | head -1)"
      black="$(ffmpeg -hide_banner -nostats -i "$f" -vf blackdetect=d=0.5:pix_th=0.10 -an -f null - 2>&1 |
        awk -v d="$dur" '/black_duration/{split($NF,a,":"); s+=a[2]} END{ if (d>0) printf "%.0f", 100*s/d; else print 0 }')"
      step="$(awk -v d="$dur" 'BEGIN{s=d/12; if (s<1) s=1; printf "%.2f", s}')"
      ffmpeg -hide_banner -loglevel error -y -i "$f" -vf "fps=1/$step,scale=320:-1,tile=4x3" -frames:v 1 "$f.contact.png" 2>/dev/null
      note=""
      [ -z "$has_audio" ] && note="$note no audio track;"
      [ "${black:-0}" -gt 20 ] && note="$note ${black}% black frames;"
      aud=""
      if [ -n "$has_audio" ]; then
        l="$(loudness "$f")"; li="${l#I=}"; li="${li%% *}"
        if awk -v i="$li" 'BEGIN{exit !(i=="" || i+0 <= -69)}'; then aud=", audio track is SILENT (fine only if no sound was asked for)"
        else aud=", audio ${li} LUFS, peak ${l##*TP=} dBTP"; fi
      fi
      printf '%-5s %s — %.1fs, %sx%s @ %s fps%s, %s%% black; contact sheet %s.contact.png (look at it)%s\n' \
        "$([ -n "$note" ] && echo WARN || echo OK)" "$f" "$dur" "$w" "$h" "$fps" "$aud" "$black" "$f" "${note:+ — $note}"
      [ -n "$note" ] && BAD=1 ;;
    mid|midi)
      if head -c 4 "$f" | grep -q "MThd"; then echo "OK    $f — Standard MIDI file"; else echo "FAIL  $f — not a MIDI file"; BAD=1; fi ;;
    *) echo "SKIP  $f — unknown type" ;;
  esac
done
exit "$BAD"
