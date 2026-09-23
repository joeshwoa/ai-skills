#!/usr/bin/env python3
"""
animatic.py — the whole film as a timed storyboard, before any video credit.

Keyframe images cost nothing (Nano Banana on Flow Pro), video costs
credits. So the client sees and approves the entire piece — every shot's
composition, the cast, the order, the timing, the transitions, the lines —
as an animatic built from the keyframes, and only then does anything get
spent on motion. This is the single biggest reason a client project comes
out right the first time: disagreements happen on free pictures, not on
paid clips.

For each shot in plan.json:
  * start keyframe only  -> slow push-in over the shot's length
  * start + end frames   -> push on the start, cross-dissolve to the end frame
  * no keyframe yet      -> a dark placeholder card (so gaps are obvious)
Then every shot is cut together with the plan's transitions, with:
  * top label   "S03 · 8s · Veo 3.1 Fast · frames" (+ beat)
  * captions    the scripted dialogue, timed to each shot's dialogue windows
  * sound       scratch audio per shot if present (scratch/<SHOT>.wav — e.g.
                a TTS read of the lines), otherwise silence

USAGE
    python3 animatic.py --plan plan.json --keyframes keyframes/ \
        [--scratch scratch/] --out review/animatic.mp4 [--no-labels]
Keyframe files: <SHOT>_start.png|jpg and optional <SHOT>_end.png|jpg
                (or <SHOT>.png as the start frame).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble   # noqa: E402
import captions   # noqa: E402

FPS = 24
EXTS = (".png", ".jpg", ".jpeg", ".webp")
MODEL_LABEL = {"omni-1.1-flash": "Omni 1.1 Flash", "veo-3.1-lite": "Veo 3.1 Lite",
               "veo-3.1-fast": "Veo 3.1 Fast", "veo-3.1-quality": "Veo 3.1 Quality"}


def find(folder: str, shot: str, which: str) -> str | None:
    names = [f"{shot}_{which}"] + ([shot] if which == "start" else [])
    for n in names:
        for e in EXTS:
            p = os.path.join(folder, n + e)
            if os.path.exists(p):
                return p
    return None


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed:\n" + r.stderr[-1500:])


def still_clip(img: str, secs: float, W: int, H: int, out: str, zoom_to: float = 1.06) -> None:
    frames = max(2, int(round(secs * FPS)))
    step = (zoom_to - 1.0) / frames
    run(["ffmpeg", "-v", "error", "-y", "-i", img, "-vf",
         f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
         f"zoompan=z='min(zoom+{step:.6f},{zoom_to})':d={frames}:x='iw/2-(iw/zoom/2)':"
         f"y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},format=yuv420p",
         "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", out])


def segment(shot: dict, kf: str, scratch: str | None, W: int, H: int, tmp: str) -> str:
    sid, d = shot["id"], float(shot.get("duration") or 4)
    start, end = find(kf, sid, "start"), find(kf, sid, "end")
    pic = os.path.join(tmp, f"{sid}_pic.mp4")
    if start and end:
        a, b = os.path.join(tmp, f"{sid}_a.mp4"), os.path.join(tmp, f"{sid}_b.mp4")
        still_clip(start, d * 0.6, W, H, a)
        still_clip(end, d * 0.6, W, H, b, zoom_to=1.03)
        run(["ffmpeg", "-v", "error", "-y", "-i", a, "-i", b, "-filter_complex",
             f"[0:v][1:v]xfade=transition=fade:duration={d * 0.2:.3f}:offset={d * 0.4:.3f},format=yuv420p",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", pic])
    elif start:
        still_clip(start, d, W, H, pic)
    else:
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x1c1c22:s={W}x{H}:r={FPS}:d={d}",
             "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", pic])
    out = os.path.join(tmp, f"{sid}.mp4")
    snd = os.path.join(scratch, f"{sid}.wav") if scratch else None
    if snd and os.path.exists(snd):
        run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", snd, "-filter_complex",
             f"[1:a]aresample=48000,apad,atrim=0:{d}[a]", "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-t", f"{d}", out])
    else:
        run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-f", "lavfi", "-i",
             f"anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-t", f"{d}", out])
    return out, bool(start), bool(end)


def label_ass(plan: dict, tl: list[dict], ratio: str, font: str, dialogue: list[dict],
              with_labels: bool, path: str) -> None:
    rx, ry, size, mv = captions.STYLE[ratio]
    lsize = max(28, int(size * 0.55))
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {rx}
PlayResY: {ry}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,{max(3, size // 16)},1,2,60,60,{mv},1
Style: Label,{font},{lsize},&H0000E5FF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,3,2,0,8,40,40,40,1
Style: Missing,{font},{int(size * 0.8)},&H006E6EFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    shots = {s["id"]: s for s in plan["shots"]}
    lines = []
    for c in tl:
        s = shots[c["shot"]]
        a, b = captions.ts_ass(c["start"]), captions.ts_ass(c["end"])
        if with_labels:
            mode = s.get("mode", "")
            lab = (f"{s['id']} · {float(s.get('duration') or 0):g}s · "
                   f"{MODEL_LABEL.get(s.get('model'), s.get('model'))} · {mode}")
            beat = (s.get("beat") or "")[:70].replace("{", "(").replace("}", ")")
            lines.append(f"Dialogue: 1,{a},{b},Label,,0,0,0,,{lab}\\N{beat}")
        if not c.get("has_start"):
            lines.append(f"Dialogue: 1,{a},{b},Missing,,0,0,0,,NO KEYFRAME YET\\N{s['id']}")
    for q in dialogue:
        txt = q["text"].replace("\n", "\\N").replace("{", "(").replace("}", ")")
        lines.append(f"Dialogue: 0,{captions.ts_ass(q['start'])},{captions.ts_ass(q['end'])},Default,,0,0,0,,{txt}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a storyboard animatic from keyframes.")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--keyframes", required=True)
    ap.add_argument("--scratch")
    ap.add_argument("--out", default="review/animatic.mp4")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--no-labels", action="store_true", help="clean version for the client")
    args = ap.parse_args()
    plan = json.load(open(args.plan, encoding="utf-8"))
    ratio = plan.get("aspect_ratio", "16:9")
    W, H = assemble.SIZES[ratio]
    W, H = W // 2 // 2 * 2, H // 2 // 2 * 2  # review resolution

    tmp = tempfile.mkdtemp(prefix="animatic_")
    clips, flags = [], {}
    for s in plan["shots"]:
        if s.get("mode") == "extend":
            continue
        f, hs, he = segment(s, args.keyframes, args.scratch, W, H, tmp)
        flags[s["id"]] = hs
        tr = s.get("transition_in") or {"type": "cut"}
        if isinstance(tr, dict) and tr.get("type") in assemble.XFADE or \
                (isinstance(tr, dict) and tr.get("type") in ("cut", "j_cut", "l_cut", "match_cut", "morph")):
            pass
        clips.append({"shot": s["id"], "file": f, "transition_in": tr})

    tl = assemble.plan_timeline(clips)
    timeline = {"ratio": ratio, "clips": [{"shot": x["shot"], "in": x["in"], "out": x["out"],
                                           "speed": x["speed"], "start": x["start"],
                                           "end": round(x["start"] + x["length"], 3),
                                           "has_start": flags[x["shot"]]} for x in tl]}
    cues, warns = captions.collect(plan, timeline, None, measure=False)
    maxc = 40 if any(captions.AR.search(c["text"]) for c in cues) else 42
    caps, _ = captions.build(cues, maxc, "ar" if maxc == 40 else "en")
    ass = os.path.join(tmp, "animatic.ass")
    label_ass(plan, timeline["clips"], ratio, args.font, caps, not args.no_labels, ass)

    edit = {"output": args.out, "ratio": ratio, "fps": FPS, "platform": "web", "clips": clips,
            "captions": {"file": ass, "burn": True}}
    cmd, _, total, out = assemble.build(edit, preview=False)
    # animatic is already at review size: rebuild at that size, not full resolution
    cmd = [c.replace(f"scale={assemble.SIZES[ratio][0]}:{assemble.SIZES[ratio][1]}", f"scale={W}:{H}")
            .replace(f"pad={assemble.SIZES[ratio][0]}:{assemble.SIZES[ratio][1]}", f"pad={W}:{H}")
           for c in cmd]
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    missing = [s for s, ok in flags.items() if not ok]
    print(f"{out}  {total:.1f}s  {len(clips)} shots  ({W}x{H}, review quality)")
    if missing:
        print(f"  ! no keyframe yet for: {missing} (shown as placeholder cards)")
    for w in warns:
        print(f"  ! {w}")
    print("Show this to the client for the storyboard sign-off: `project_state.py gate storyboard approve --by user --note '<client words>'`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
