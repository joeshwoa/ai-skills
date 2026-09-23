#!/usr/bin/env python3
"""
qc_clip.py — the mechanical half of checking a generated clip.

A generated clip can look fine in a thumbnail and still be unusable:
wrong length, wrong aspect ratio, no audio, dialogue that never happens,
a frozen second in the middle, a black flash, audio clipping. None of
those need judgment — they need measuring. This script measures them, and
extracts frames so the agent can do the half that DOES need judgment
(identity, wardrobe, anatomy, physics, continuity) by actually looking.

It never replaces looking. It makes sure looking starts from facts.

USAGE
    python3 qc_clip.py clip.mp4 --duration 8 --ratio 9:16
    python3 qc_clip.py clip.mp4 --duration 8 --ratio 9:16 --expect-speech \
        --dialogue '[{"start":1.0,"end":3.6},{"start":4.4,"end":7.0}]'
    python3 qc_clip.py clip.mp4 --out qc/S02_take1      # where frames go

OUTPUTS (in --out, default: <clip>_qc/)
    contact_sheet.png   5 frames across the clip, for visual QC
    first.png / last.png  first and last frames (last.png = next shot's start
                          keyframe when chaining)
    report.json         every measurement + a technical verdict

VERDICTS
    PASS   technically sound — proceed to visual QC
    CHECK  something is off but may be acceptable; look before accepting
    FAIL   technically broken — regenerate or fix in post, do not accept
EXIT CODES: 0 PASS, 3 CHECK, 4 FAIL, 1 could not read the file
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: str) -> dict:
    r = run(["ffprobe", "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", path])
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[-800:])
    return json.loads(r.stdout)


def parse_ratio(s: str) -> float:
    a, b = s.split(":")
    return float(a) / float(b)


def detect(path: str, vf: str | None, af: str | None, dur: float) -> str:
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", path]
    if vf:
        cmd += ["-vf", vf]
    else:
        cmd += ["-vn"]
    if af:
        cmd += ["-af", af]
    else:
        cmd += ["-an"]
    cmd += ["-f", "null", "-"]
    return run(cmd).stderr


def intervals(log: str, start_key: str, end_key: str) -> list[tuple[float, float]]:
    starts = [float(x) for x in re.findall(rf"{start_key}:\s*([-\d.]+)", log)]
    ends = [float(x) for x in re.findall(rf"{end_key}:\s*([-\d.]+)", log)]
    out = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else None
        out.append((s, e))
    return out


def voiced_intervals(silences: list[tuple[float, float | None]], dur: float) -> list[tuple[float, float]]:
    """Invert silence intervals into sound intervals."""
    cur = 0.0
    out = []
    for s, e in sorted(silences):
        if s > cur + 0.05:
            out.append((round(cur, 2), round(s, 2)))
        cur = e if e is not None else dur
    if cur < dur - 0.05:
        out.append((round(cur, 2), round(dur, 2)))
    return out


def overlap(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def extract_frames(path: str, dur: float, out: str) -> dict:
    os.makedirs(out, exist_ok=True)
    first = os.path.join(out, "first.png")
    last = os.path.join(out, "last.png")
    sheet = os.path.join(out, "contact_sheet.png")
    run(["ffmpeg", "-y", "-v", "error", "-ss", "0", "-i", path, "-frames:v", "1", first])
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.08", "-i", path, "-frames:v", "1", "-update", "1", last])
    # 5 evenly spaced frames tiled horizontally, scaled to a readable height.
    times = [dur * f for f in (0.02, 0.25, 0.5, 0.75, 0.97)]
    tmp = []
    for i, t in enumerate(times):
        p = os.path.join(out, f".f{i}.png")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", path,
             "-frames:v", "1", "-vf", "scale=-2:360", p])
        if os.path.exists(p):
            tmp.append(p)
    if tmp:
        inputs = []
        for p in tmp:
            inputs += ["-i", p]
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
             f"hstack=inputs={len(tmp)}" if len(tmp) > 1 else "null", sheet])
        for p in tmp:
            os.remove(p)
    return {"first": first, "last": last, "contact_sheet": sheet if os.path.exists(sheet) else None,
            "contact_sheet_times": [round(t, 2) for t in times]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Technical QC for a generated video clip.")
    ap.add_argument("clip")
    ap.add_argument("--duration", type=float, help="expected seconds")
    ap.add_argument("--ratio", help="expected aspect ratio, e.g. 9:16")
    ap.add_argument("--expect-audio", action="store_true", help="clip must have an audio track")
    ap.add_argument("--expect-speech", action="store_true",
                    help="dialogue is scripted; audio must not be mostly silent")
    ap.add_argument("--dialogue", help="JSON list of {start,end} windows where speech is scripted")
    ap.add_argument("--out", help="output folder (default <clip>_qc)")
    args = ap.parse_args()

    out = args.out or os.path.splitext(args.clip)[0] + "_qc"
    try:
        info = probe(args.clip)
    except Exception as e:
        print(f"FAIL: cannot read {args.clip}: {e}")
        return 1

    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"].get("duration") or 0)
    fails, checks, notes = [], [], []

    if not v:
        fails.append("no video stream")
        w = h = 0
        fps = 0.0
    else:
        w, h = int(v["width"]), int(v["height"])
        num, den = (v.get("avg_frame_rate") or "0/1").split("/")
        fps = float(num) / float(den) if float(den) else 0.0

    # --- length ---------------------------------------------------------
    if args.duration:
        diff = abs(dur - args.duration)
        if diff > 1.0:
            fails.append(f"duration {dur:.2f}s vs expected {args.duration}s")
        elif diff > 0.3:
            checks.append(f"duration {dur:.2f}s vs expected {args.duration}s")

    # --- aspect ratio ---------------------------------------------------
    if args.ratio and w and h:
        want = parse_ratio(args.ratio)
        got = w / h
        if abs(got - want) / want > 0.03:
            fails.append(f"aspect {w}x{h} ({got:.3f}) is not {args.ratio} ({want:.3f})")

    # --- black frames / freezes ----------------------------------------
    if v:
        blog = detect(args.clip, "blackdetect=d=0.25:pix_th=0.10", None, dur)
        blacks = intervals(blog, "black_start", "black_end")
        mid_blacks = [b for b in blacks if b[0] > 0.3 and (b[1] or dur) < dur - 0.3]
        if mid_blacks:
            fails.append(f"black frames mid-clip at {[(round(s,2), round(e or dur,2)) for s, e in mid_blacks]}")
        elif blacks:
            notes.append(f"black at clip edge {[(round(s,2), round(e or dur,2)) for s, e in blacks]} (trim in post)")

        flog = detect(args.clip, "freezedetect=n=0.003:d=0.8", None, dur)
        freezes = intervals(flog, "freeze_start", "freeze_end")
        long_mid = [f for f in freezes if f[0] > 0.2 and ((f[1] or dur) - f[0]) > 1.2 and (f[1] or dur) < dur - 0.2]
        if long_mid:
            checks.append(f"frozen picture mid-clip at {[(round(s,2), round(e or dur,2)) for s, e in long_mid]} "
                          f"— a stall, or an intentional hold?")
        tail = [f for f in freezes if (f[1] is None or f[1] >= dur - 0.2)]
        ends_still = bool(tail) and (dur - tail[-1][0]) >= 0.5
    else:
        ends_still = False

    # --- audio ----------------------------------------------------------
    audio_report = {}
    if not a:
        if args.expect_audio or args.expect_speech:
            fails.append("no audio track, but audio/dialogue was expected")
    else:
        vlog = detect(args.clip, None, "volumedetect", dur)
        mv = re.search(r"max_volume:\s*([-\d.]+) dB", vlog)
        mean = re.search(r"mean_volume:\s*([-\d.]+) dB", vlog)
        audio_report["max_db"] = float(mv.group(1)) if mv else None
        audio_report["mean_db"] = float(mean.group(1)) if mean else None
        if audio_report["max_db"] is not None and audio_report["max_db"] >= -0.1:
            checks.append(f"audio peaks at {audio_report['max_db']} dB — possible clipping")
        if audio_report["mean_db"] is not None and audio_report["mean_db"] < -55:
            (fails if args.expect_speech else checks).append(
                f"audio is near-silent (mean {audio_report['mean_db']} dB)")

        slog = detect(args.clip, None, "silencedetect=n=-38dB:d=0.35", dur)
        sil = intervals(slog, "silence_start", "silence_end")
        voiced = voiced_intervals(sil, dur)
        audio_report["sound_intervals"] = voiced
        sound_total = sum(e - s for s, e in voiced)
        audio_report["sound_seconds"] = round(sound_total, 2)

        if args.expect_speech and sound_total < 0.8:
            fails.append("dialogue was scripted but the clip has almost no sound")

        if args.dialogue:
            try:
                wins = json.loads(args.dialogue)
            except json.JSONDecodeError as e:
                print(f"bad --dialogue JSON: {e}")
                return 1
            cover = []
            for wi in wins:
                span = (float(wi["start"]), float(wi["end"]))
                got = sum(overlap(span, iv) for iv in voiced)
                frac = got / max(0.01, span[1] - span[0])
                cover.append(round(frac, 2))
                if frac < 0.35:
                    checks.append(f"scripted line {span} has little sound under it ({frac:.0%}) "
                                  f"— line skipped, moved, or cut short?")
            audio_report["dialogue_window_coverage"] = cover
            # Sound where no line is scripted — could be SFX, could be an extra voice.
            scripted = [(float(x["start"]), float(x["end"])) for x in wins]
            stray = sum(max(0.0, (e - s) - sum(overlap((s, e), sc) for sc in scripted)) for s, e in voiced)
            audio_report["sound_outside_dialogue_seconds"] = round(stray, 2)

    frames = extract_frames(args.clip, dur, out) if v else {}

    verdict = "FAIL" if fails else ("CHECK" if checks else "PASS")
    report = {
        "clip": os.path.abspath(args.clip),
        "verdict": verdict,
        "measured": {"duration": round(dur, 3), "width": w, "height": h,
                     "fps": round(fps, 3), "has_audio": bool(a), "ends_on_stillness": ends_still,
                     **audio_report},
        "fails": fails, "checks": checks, "notes": notes,
        "frames": frames,
        "next": ("Open contact_sheet.png and run the visual checklist in references/qc.md "
                 "(identity, wardrobe, anatomy, physics, continuity, camera, lip-sync). "
                 "A technical PASS is not an accept."),
    }
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print(f"{verdict}  {os.path.basename(args.clip)}  {dur:.2f}s  {w}x{h}  "
          f"audio={'yes' if a else 'no'}  ends_on_stillness={ends_still}")
    for x in fails:
        print(f"  X {x}")
    for x in checks:
        print(f"  ? {x}")
    for x in notes:
        print(f"  . {x}")
    if frames.get("contact_sheet"):
        print(f"  contact sheet -> {frames['contact_sheet']}")
    print(f"  report -> {os.path.join(out, 'report.json')}")
    return {"PASS": 0, "CHECK": 3, "FAIL": 4}[verdict]


if __name__ == "__main__":
    sys.exit(main())
