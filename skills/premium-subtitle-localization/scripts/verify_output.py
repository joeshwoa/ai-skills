#!/usr/bin/env python3
"""
verify_output.py — the final "did this actually work" check, before
telling the user the video is ready.

Confirms, via ffprobe (never just "the command exited 0"):
  - the output file exists and is playable (ffprobe can read it)
  - it has a video stream and an audio stream
  - its duration matches the original within a small tolerance (a merge
    that silently truncated the video is a real failure mode worth
    catching)
  - it has at least one subtitle stream (soft-sub mode) — burned-in mode
    obviously won't have one, so that check is skipped with --burned-in

Usage:
    python3 verify_output.py original.mp4 output.mkv
    python3 verify_output.py original.mp4 output.burned.mp4 --burned-in
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def ffprobe(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe could not read {path!r}:\n{result.stderr[-2000:]}")
    return json.loads(result.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original_video")
    ap.add_argument("output_video")
    ap.add_argument("--burned-in", action="store_true", help="skip the subtitle-stream check")
    ap.add_argument("--duration-tolerance", type=float, default=1.0, help="seconds")
    args = ap.parse_args()

    errors = []

    try:
        orig = ffprobe(args.original_video)
    except Exception as e:
        raise SystemExit(f"Could not read the ORIGINAL video: {e}")

    try:
        out = ffprobe(args.output_video)
    except Exception as e:
        raise SystemExit(f"Could not read the OUTPUT video — merge likely failed: {e}")

    out_kinds = {s["codec_type"] for s in out["streams"]}
    if "video" not in out_kinds:
        errors.append("Output has no video stream.")
    if "audio" not in out_kinds:
        errors.append("Output has no audio stream.")
    if not args.burned_in and "subtitle" not in out_kinds:
        errors.append("Output has no subtitle stream (expected in soft-sub mode).")

    orig_dur = float(orig["format"].get("duration", 0))
    out_dur = float(out["format"].get("duration", 0))
    if orig_dur and abs(orig_dur - out_dur) > args.duration_tolerance:
        errors.append(
            f"Duration mismatch: original {orig_dur:.2f}s vs output {out_dur:.2f}s "
            f"(tolerance {args.duration_tolerance}s) — the merge may have truncated the file."
        )

    print(f"Original: {orig_dur:.2f}s, streams: "
          f"{[s['codec_type'] for s in orig['streams']]}")
    print(f"Output:   {out_dur:.2f}s, streams: "
          f"{[s['codec_type'] for s in out['streams']]}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  X {e}")
        sys.exit(1)

    print("\nPASSED — output file is playable, streams intact, duration matches.")


if __name__ == "__main__":
    main()
