#!/usr/bin/env python3
"""
find_subtitles.py — look for a subtitle file that already ships next to
the movie, before spending time/compute transcribing from audio.

Usage:
    python3 find_subtitles.py /path/to/movie.mp4
"""
from __future__ import annotations

import argparse
import os

from srt_utils import find_subtitle_candidates, parse_srt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_path")
    args = ap.parse_args()

    candidates = find_subtitle_candidates(args.video_path)
    if not candidates:
        print("No .srt/.vtt/.ass/.ssa files found next to the video.")
        print("-> proceed to transcribe.py to generate a source-language SRT.")
        return

    print(f"Found {len(candidates)} subtitle file(s) next to the video:")
    for path in candidates:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".srt":
            try:
                n = len(parse_srt(path))
                print(f"  {path}  ({n} cues)")
            except Exception as e:
                print(f"  {path}  (found but failed to parse: {e})")
        else:
            print(f"  {path}  ({ext[1:].upper()} — convert to SRT before using with this skill's scripts)")

    print(
        "\nCheck the filename/content for which language(s) these are "
        "(e.g. *.ar.srt vs *.en.srt) before deciding whether you still need "
        "to transcribe."
    )


if __name__ == "__main__":
    main()
