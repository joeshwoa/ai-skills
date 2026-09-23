#!/usr/bin/env python3
"""
assemble.py — turn approved clips into a finished, delivery-ready video.

Clips from different models (Omni vs Veo) and different takes rarely
share exact resolution, frame rate, or loudness. Concatenating them
naively gives jumps in size, stutter, and volume lurches between cuts.
This conforms every clip to one spec, cuts them in order with their
native audio, lays off-screen narration on top, ducks music under the
narration, and normalizes the whole mix to the delivery platform's
loudness target.

USAGE
    python3 assemble.py edit.json
    python3 assemble.py edit.json --dry-run     # print the ffmpeg command

edit.json:
{
  "output": "final/hana_teaser_9x16.mp4",
  "ratio": "9:16",                  # 9:16 -> 1080x1920, 16:9 -> 1920x1080, 1:1, 4:5
  "fps": 24,
  "platform": "reels",              # sets loudness: reels/tiktok/shorts -14, youtube -14, broadcast -23
  "clips": [
    {"file": "takes/S01.mp4", "in": 0.0, "out": 6.0},
    {"file": "takes/S02.mp4", "in": 0.2, "out": 8.0, "gain_db": 0}
  ],
  "voiceover": [{"file": "vo/N01.wav", "at": 1.5, "gain_db": 0}],
  "music": {"file": "music/bed.mp3", "gain_db": -16, "duck_under_voiceover": true},
  "fade_out": 0.6
}
Only "output" and "clips" are required.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
LUFS = {"reels": -14, "tiktok": -14, "shorts": -14, "youtube": -14, "facebook": -14,
        "linkedin": -14, "web": -16, "broadcast": -23}


def has_audio(path: str) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "stream=index", "-of", "csv=p=0", path], capture_output=True, text=True)
    return bool(r.stdout.strip())


def probe_duration(path: str) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def integrated_lufs(path: str) -> float | None:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True)
    import re as _re
    m = _re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def build(edit: dict) -> tuple[list[str], float]:
    W, H = SIZES[edit.get("ratio", "16:9")]
    fps = edit.get("fps", 24)
    target = LUFS.get(edit.get("platform", "youtube"), -14)
    clips = edit["clips"]
    inputs, filters = [], []
    idx = 0
    seg_labels = []
    total = 0.0

    for i, c in enumerate(clips):
        f = c["file"]
        if not os.path.exists(f):
            raise SystemExit(f"missing clip: {f}")
        t_in = float(c.get("in", 0.0))
        t_out = float(c.get("out", probe_duration(f)))
        d = t_out - t_in
        if d <= 0:
            raise SystemExit(f"clip {f}: out must be after in")
        inputs += ["-i", f]
        # Conform picture: fit inside the frame, pad the rest (never stretch).
        filters.append(
            f"[{idx}:v]trim={t_in}:{t_out},setpts=PTS-STARTPTS,fps={fps},"
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}]")
        g = float(c.get("gain_db", 0))
        if has_audio(f):
            filters.append(
                f"[{idx}:a]atrim={t_in}:{t_out},asetpts=PTS-STARTPTS,"
                f"aresample=48000,aformat=channel_layouts=stereo,volume={g}dB[a{i}]")
        else:  # silent clip: keep the timeline in sync with generated silence
            filters.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d}[a{i}]")
        seg_labels.append(f"[v{i}][a{i}]")
        idx += 1
        total += d

    filters.append(f"{''.join(seg_labels)}concat=n={len(clips)}:v=1:a=1[vcat][acat]")
    mix_inputs = ["[acat]"]

    # Narration, positioned on the timeline.
    vo_labels = []
    for j, vo in enumerate(edit.get("voiceover") or []):
        if not os.path.exists(vo["file"]):
            raise SystemExit(f"missing voiceover: {vo['file']}")
        inputs += ["-i", vo["file"]]
        ms = int(float(vo.get("at", 0)) * 1000)
        filters.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                       f"volume={float(vo.get('gain_db', 0))}dB,adelay={ms}|{ms}[vo{j}]")
        vo_labels.append(f"[vo{j}]")
        idx += 1
    if vo_labels:
        if len(vo_labels) > 1:
            filters.append(f"{''.join(vo_labels)}amix=inputs={len(vo_labels)}:normalize=0[voall]")
        else:
            filters.append(f"{vo_labels[0]}anull[voall]")

    music = edit.get("music")
    if music:
        if not os.path.exists(music["file"]):
            raise SystemExit(f"missing music: {music['file']}")
        inputs += ["-stream_loop", "-1", "-i", music["file"]]
        filters.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                       f"volume={float(music.get('gain_db', -16))}dB,atrim=0:{total}[mus]")
        idx += 1
        if vo_labels and music.get("duck_under_voiceover", True):
            filters.append("[voall]asplit=2[voA][voK]")
            filters.append("[mus][voK]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[musd]")
            mix_inputs += ["[voA]", "[musd]"]
        else:
            if vo_labels:
                mix_inputs.append("[voall]")
            mix_inputs.append("[mus]")
    elif vo_labels:
        mix_inputs.append("[voall]")

    fo = float(edit.get("fade_out", 0))
    fade = f",afade=t=out:st={max(0, total - fo)}:d={fo}" if fo else ""
    vfade = f",fade=t=out:st={max(0, total - fo)}:d={fo}" if fo else ""
    if len(mix_inputs) > 1:
        filters.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:normalize=0:duration=first[amix]")
        last_a = "[amix]"
    else:
        last_a = "[acat]"
    filters.append(f"{last_a}loudnorm=I={target}:TP=-1.5:LRA=11{fade}[aout]")
    filters.append(f"[vcat]null{vfade}[vout]")

    out = edit["output"]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
           "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-t", f"{total:.3f}", out]
    return cmd, total


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble approved clips into a delivery file.")
    ap.add_argument("edit")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with open(args.edit, encoding="utf-8") as f:
        edit = json.load(f)
    if edit.get("ratio", "16:9") not in SIZES:
        raise SystemExit(f"ratio must be one of {sorted(SIZES)}")
    cmd, total = build(edit)
    if args.dry_run:
        print(" ".join(cmd))
        return 0
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    # Single-pass loudnorm drifts on short clips; measure and correct.
    target = LUFS.get(edit.get("platform", "youtube"), -14)
    measured = integrated_lufs(edit["output"])
    if measured is not None and abs(measured - target) > 0.7:
        fixed = edit["output"] + ".tmp.mp4"
        gain = target - measured
        r2 = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", edit["output"], "-c:v", "copy",
                             "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac",
                             "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", fixed],
                            capture_output=True, text=True)
        if r2.returncode == 0:
            os.replace(fixed, edit["output"])
            measured = integrated_lufs(edit["output"])
    got = probe_duration(edit["output"])
    print(f"{edit['output']}  {got:.2f}s (timeline {total:.2f}s)  "
          f"loudness {measured} LUFS (target {target})")
    if abs(got - total) > 0.25:
        print("  X output length differs from the timeline — check the clip in/out points")
        return 1
    print("Run qc_clip.py on the output before delivering it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
