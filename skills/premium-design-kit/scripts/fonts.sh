#!/usr/bin/env bash
# Install the free (SIL OFL) fonts the themes use — Arabic: Cairo, Tajawal, IBM Plex Sans Arabic,
# Amiri, El Messiri, Noto Naskh Arabic; Latin: Inter, Poppins — from github.com/google/fonts into the
# user font folder (macOS ~/Library/Fonts, Linux ~/.local/share/fonts). Downloads ~6 MB; run only
# when the user agrees. Office files never embed fonts: the person OPENING a .docx/.pptx also needs
# them (or Word substitutes) — designed PDFs embed them, so PDFs always look right.
set -euo pipefail
B=https://raw.githubusercontent.com/google/fonts/main/ofl
if [ "$(uname)" = "Darwin" ]; then D="$HOME/Library/Fonts"; else D="$HOME/.local/share/fonts"; fi
mkdir -p "$D"
F=( "cairo/Cairo%5Bslnt%2Cwght%5D.ttf" "tajawal/Tajawal-Regular.ttf" "tajawal/Tajawal-Medium.ttf"
    "tajawal/Tajawal-Bold.ttf" "tajawal/Tajawal-ExtraBold.ttf" "ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf"
    "ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf" "ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf"
    "amiri/Amiri-Regular.ttf" "amiri/Amiri-Bold.ttf" "elmessiri/ElMessiri%5Bwght%5D.ttf"
    "notonaskharabic/NotoNaskhArabic%5Bwght%5D.ttf" "inter/Inter%5Bopsz%2Cwght%5D.ttf"
    "poppins/Poppins-Regular.ttf" "poppins/Poppins-SemiBold.ttf" "poppins/Poppins-Bold.ttf" )
n=0
for f in "${F[@]}"; do
  name="$(basename "$f" | sed 's/%5B/[/g; s/%5D/]/g; s/%2C/,/g')"
  [ -f "$D/$name" ] && continue
  curl -fsSL "$B/$f" -o "$D/$name" && n=$((n+1))
done
command -v fc-cache >/dev/null && fc-cache -f "$D" >/dev/null 2>&1 || true
rm -f "$HOME/.cache/matplotlib/fontlist-"*.json "$HOME/.matplotlib/fontlist-"*.json 2>/dev/null || true
echo "fonts: $n new file(s) in $D"
