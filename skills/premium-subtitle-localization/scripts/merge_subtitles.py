#!/usr/bin/env python3
"""
merge_subtitles.py — mux a translated SRT into the video.

Two modes:

  softsub (default) — a real subtitle track, toggle-able on/off in the
  player, selectable alongside other language tracks. Video and audio are
  STREAM-COPIED (-c:v copy -c:a copy): no re-encode, so this takes seconds
  regardless of movie length and there is zero quality loss. Output
  container must support the subtitle codec used:
    .mkv -> subtitle copied as-is (SRT codec, universally supported in mkv)
    .mp4 -> subtitle converted to mov_text (mp4's native text-subtitle
            codec; still not a video/audio re-encode, just the tiny text
            stream gets repackaged)

  hardsub (--burn-in) — subtitles painted directly into the video frames.
  Use this only when the target platform/player can't do soft subtitle
  tracks at all (e.g. some short-form social platforms). This DOES
  re-encode the video (libx264) because burning text into pixels has no
  copy-only path — slower, and re-encoding always costs a little quality,
  so it's opt-in, never the default.

Usage:
    python3 merge_subtitles.py movie.mp4 ru.srt movie.ru.mkv
    python3 merge_subtitles.py movie.mp4 ru.srt movie.ru.mp4
    python3 merge_subtitles.py movie.mp4 ru.srt movie.ru.burned.mp4 --burn-in
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys


def run(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-3000:]}")


def softsub_merge(video_path: str, srt_path: str, output_path: str, lang_code: str | None) -> None:
    ext = os.path.splitext(output_path)[1].lower()
    sub_codec = "mov_text" if ext == ".mp4" else "srt"
    if ext not in (".mp4", ".mkv"):
        print(f"Warning: output extension {ext!r} is unusual for soft subs; "
              f"defaulting to the {sub_codec} subtitle codec (mkv-style). "
              f"Use .mkv or .mp4 if the player complains.", file=sys.stderr)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", srt_path,
        "-map", "0:v", "-map", "0:a", "-map", "1:s",
        "-c:v", "copy", "-c:a", "copy", "-c:s", sub_codec,
        "-disposition:s:0", "default",
    ]
    if lang_code:
        cmd += ["-metadata:s:s:0", f"language={lang_code}"]
    cmd.append(output_path)
    run(cmd)


def hardsub_merge(video_path: str, srt_path: str, output_path: str) -> None:
    # ffmpeg's subtitles filter needs a path with no characters that upset
    # its internal filter-graph parser (colons, backslashes) — safest to
    # always pass an absolute path and let ffmpeg handle escaping via the
    # filename= form.
    srt_abs = os.path.abspath(srt_path)
    vf = f"subtitles=filename='{srt_abs}'"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "copy",
        output_path,
    ]
    run(cmd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_path")
    ap.add_argument("srt_path")
    ap.add_argument("output_path")
    ap.add_argument("--burn-in", action="store_true", help="hardsub: re-encode video with subtitles painted in")
    ap.add_argument("--lang", default=None, help="ISO 639 language code to tag the subtitle track with, e.g. ru")
    args = ap.parse_args()

    if args.burn_in:
        print("Hard-sub mode: this WILL re-encode the video (slower, one generation of quality loss).")
        hardsub_merge(args.video_path, args.srt_path, args.output_path)
    else:
        print("Soft-sub mode: video/audio stream-copied, no re-encode.")
        softsub_merge(args.video_path, args.srt_path, args.output_path, args.lang)

    print(f"-> {args.output_path}")
    print(f"Next: python3 verify_output.py {args.video_path!r} {args.output_path!r}")


if __name__ == "__main__":
    main()
