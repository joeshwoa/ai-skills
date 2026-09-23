#!/usr/bin/env python3
"""
captions.py — captions from the SCRIPT, timed to the final edit.

Captions are never transcribed from the finished audio. Speech recognition
on dialect is unreliable and invents words (see premium-subtitle-
localization's asr_accuracy_guide.md); the script already holds the exact
words. This maps every scripted line — each shot's dialogue windows and
the narration placed in the edit — through the assembled timeline (trims,
speed changes, transitions) to its final time, then writes:

  captions.srt   for platforms that take a caption file (YouTube, Facebook)
  captions.ass   styled for burning in (assemble.py "captions": {...}),
                 safe-zone aware per ratio, Arabic shaped correctly by libass

Timing comes from the ACTUAL clips, not the plan: each clip in the timeline
(the approved take, or its edit_clip.py fix — whatever the edit really
uses) is measured for speech (band-limited silence detection), and the
scripted lines of that shot are aligned to the measured speech in order.
The plan's windows are only the fallback, and every fallback is reported.
J/L cuts are respected: a line may run over the next picture when its
sound does.

Rules: ≤2 lines per caption; ≤40 characters per line for Arabic and ≤42 for
English (configurable); long lines split into several captions at natural
breaks with time shared by length; a caption is never shown for less than
~1 s; reading speed is checked.

USAGE
    python3 captions.py --plan plan.json --timeline final/out.mp4.timeline.json \
        [--edit edit.json] --out final/captions [--max-chars 40] [--font "Arial"] \
        [--planned-timing]   (skip measuring; use the plan's windows)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

AR = re.compile(r"[؀-ۿ]")
STYLE = {  # PlayRes, font size, bottom margin (keeps clear of platform UI)
    "9:16": (1080, 1920, 64, 420),
    "16:9": (1920, 1080, 54, 70),
    "1:1": (1080, 1080, 52, 90),
    "4:5": (1080, 1350, 54, 140),
}
MIN_DUR, GAP = 1.0, 0.08
MAX_CPS = {"ar": 15, "en": 20}


def ts_srt(t: float) -> str:
    t = max(0.0, t)
    h, rem = divmod(int(round(t * 1000)), 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ts_ass(t: float) -> str:
    t = max(0.0, t)
    cs = int(round(t * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, c = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def wrap(text: str, maxc: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def chunk(text: str, maxc: int) -> list[str]:
    """Split text into balanced caption-sized pieces (≤2 lines each).

    Pieces are sized evenly — never a long caption followed by a one-word
    orphan — and each break is pulled to the nearest punctuation mark when
    one is close to the ideal split point."""
    words = text.split()
    if len(wrap(text, maxc)) <= 2:
        return ["\n".join(wrap(text, maxc))]
    k = 2
    while True:
        total = len(text)
        cuts, pos, acc = [], 0, 0
        bounds = []
        for i, w in enumerate(words):
            acc += len(w) + 1
            bounds.append((acc, i + 1, bool(re.search(r"[.!?؟،,؛;…:]$", w))))
        for j in range(1, k):
            target = total * j / k
            window = total / k * 0.3
            near = [b for b in bounds if abs(b[0] - target) <= window and b[2]]
            pick = min(near or bounds, key=lambda b: abs(b[0] - target))
            if not cuts or pick[1] > cuts[-1]:
                cuts.append(pick[1])
        pieces, prev = [], 0
        for c in cuts + [len(words)]:
            if c > prev:
                pieces.append(" ".join(words[prev:c]))
            prev = c
        if all(len(wrap(p, maxc)) <= 2 for p in pieces) or k > len(words):
            return ["\n".join(wrap(p, maxc)) for p in pieces]
        k += 1


def measure_speech(path: str, a: float, b: float) -> list[tuple[float, float]] | None:
    """Speech-band sound intervals of path between source times a..b."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", path,
                        "-vn", "-af", "highpass=f=180,lowpass=f=3800,silencedetect=n=-32dB:d=0.22",
                        "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode != 0 or "Audio" not in r.stderr:
        return None
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", r.stderr)]
    length = b - a
    sil = [(max(0.0, st), ends[i] if i < len(ends) else length) for i, st in enumerate(starts)]
    voiced, t = [], 0.0
    for st, en in sorted(sil):
        if st - t > 0.12:
            voiced.append((t, st))
        t = max(t, en)
    if length - t > 0.12:
        voiced.append((t, length))
    return [(a + x, a + y) for x, y in voiced]


def align(lines: list[dict], iv: list[tuple[float, float]]) -> tuple[list[tuple[float, float]] | None, str]:
    """Map scripted lines (in order) onto measured speech intervals."""
    if not lines:
        return [], "none"
    merged: list[list[float]] = []
    for a, b in iv:
        if merged and a - merged[-1][1] < 0.3:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    merged = [m for m in merged if m[1] - m[0] >= 0.15]
    if not merged:
        return None, "no speech measured"
    planned = sum(float(l["end"]) - float(l["start"]) for l in lines)
    measured = sum(b - a for a, b in merged)
    if not 0.4 * planned <= measured <= 2.5 * planned + 1.0:
        return None, f"measured speech {measured:.1f}s vs planned {planned:.1f}s — implausible (music/ambience?)"
    while len(merged) > len(lines):                       # join the closest neighbours
        gaps = [merged[i + 1][0] - merged[i][1] for i in range(len(merged) - 1)]
        i = gaps.index(min(gaps))
        merged[i][1] = merged[i + 1][1]
        del merged[i + 1]
    if len(merged) == len(lines):
        return [(a, b) for a, b in merged], "measured"
    # fewer sound blocks than lines (lines run together): share each block by length
    words = [max(1, len(l["text"].split())) for l in lines]
    span_a, span_b = merged[0][0], merged[-1][1]
    speech = sum(b - a for a, b in merged)
    out, acc, total = [], 0.0, sum(words)
    def at(x):                                            # x seconds of speech -> source time
        for a, b in merged:
            if x <= b - a:
                return a + x
            x -= b - a
        return span_b
    for w in words:
        a = at(acc)
        acc += speech * w / total
        out.append((a, at(acc)))
    return out, "measured (lines shared a sound block)"


def collect(plan: dict, timeline: dict, edit: dict | None, measure: bool = True) -> tuple[list[dict], list[str]]:
    shots = {s["id"]: s for s in plan.get("shots", [])}
    cues, warns = [], []
    for c in timeline["clips"]:
        s = shots.get(c.get("shot"))
        if not s:
            continue
        sp = float(c.get("speed", 1.0))
        au = c.get("audio") or {"src_in": c["in"], "src_out": c["out"], "start": c["start"], "end": c["end"]}
        lines = s.get("dialogue") or []
        if not lines:
            continue
        times, how = None, "planned (--planned-timing)"
        if measure and c.get("file") and os.path.exists(c["file"]):
            iv = measure_speech(c["file"], au["src_in"], au["src_out"])
            times, how = align(lines, iv) if iv is not None else (None, "clip has no audio")
        if times is None:
            if measure:
                warns.append(f"{s['id']}: caption timing from the PLAN ({how}) — check it against the picture")
            times = [(float(l["start"]), float(l["end"])) for l in lines]
        elif how != "measured":
            warns.append(f"{s['id']}: {how} — check the split points")
        for ln, (sa, sb) in zip(lines, times):
            a = c["start"] + (sa - c["in"]) / sp
            b = c["start"] + (sb - c["in"]) / sp
            lo, hi = min(c["start"], au["start"]), max(c["end"], au["end"])
            if b <= lo or a >= hi:
                warns.append(f"{s['id']}: line \"{ln['text'][:30]}\" is outside the kept part of the clip "
                             f"(trimmed away) — the edit dropped scripted dialogue")
                continue
            if a < lo - 0.05 or b > hi + 0.05:
                warns.append(f"{s['id']}: line \"{ln['text'][:30]}\" is partly cut by the trim")
            cues.append({"start": max(a, lo), "end": min(b, hi), "text": ln["text"],
                         "who": ln.get("character"), "src": s["id"]})
    measured_vo = {(v["file"], round(v["at"], 2)): v for v in timeline.get("voiceover") or []}
    for vo in (edit or {}).get("voiceover") or []:
        if vo.get("text"):
            m = measured_vo.get((os.path.abspath(vo["file"]), round(float(vo.get("at", 0)), 2))) \
                if vo.get("file") else None
            dur = float(vo.get("seconds") or 0) or (m["seconds"] if m else 0) or \
                max(1.2, len(vo["text"].split()) / 2.3)
            cues.append({"start": float(vo.get("at", 0)), "end": float(vo.get("at", 0)) + dur,
                         "text": vo["text"], "who": "VO", "src": "VO"})
    cues.sort(key=lambda x: x["start"])
    return cues, warns


def build(cues: list[dict], maxc: int, lang: str) -> tuple[list[dict], list[str]]:
    out, warns = [], []
    for q in cues:
        parts = chunk(q["text"], maxc)
        total = sum(len(p) for p in parts) or 1
        t = q["start"]
        span = q["end"] - q["start"]
        for p in parts:
            d = span * len(p) / total
            out.append({"start": t, "end": t + d, "text": p, "src": q["src"]})
            t += d
    # minimum duration / no overlaps
    for i, c in enumerate(out):
        if c["end"] - c["start"] < MIN_DUR:
            nxt = out[i + 1]["start"] - GAP if i + 1 < len(out) else c["start"] + MIN_DUR
            c["end"] = max(c["end"], min(c["start"] + MIN_DUR, nxt))
        if i + 1 < len(out) and c["end"] > out[i + 1]["start"] - GAP:
            c["end"] = max(c["start"] + 0.3, out[i + 1]["start"] - GAP)
        cps = len(c["text"].replace("\n", "")) / max(0.1, c["end"] - c["start"])
        if cps > MAX_CPS.get(lang, 18):
            warns.append(f"{ts_srt(c['start'])} \"{c['text'][:30]}…\" reads at {cps:.0f} chars/s "
                         f"(>{MAX_CPS.get(lang, 18)}) — hard to read; shorten the line or give it more time")
    return out, warns


def write_srt(caps: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(caps, 1):
            f.write(f"{i}\n{ts_srt(c['start'])} --> {ts_srt(c['end'])}\n{c['text']}\n\n")


def write_ass(caps: list[dict], path: str, ratio: str, font: str) -> None:
    rx, ry, size, mv = STYLE[ratio]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {rx}
PlayResY: {ry}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,{max(3, size // 16)},1,2,60,60,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(head)
        for c in caps:
            txt = c["text"].replace("\n", "\\N").replace("{", "(").replace("}", ")")
            f.write(f"Dialogue: 0,{ts_ass(c['start'])},{ts_ass(c['end'])},Default,,0,0,0,,{txt}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Captions from the script, timed to the final edit.")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--edit", help="edit.json — for narration lines that carry 'text'")
    ap.add_argument("--out", default="captions")
    ap.add_argument("--max-chars", type=int)
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--planned-timing", action="store_true", help="don't measure the clips; use plan windows")
    args = ap.parse_args()
    plan = json.load(open(args.plan, encoding="utf-8"))
    tl = json.load(open(args.timeline, encoding="utf-8"))
    edit = json.load(open(args.edit, encoding="utf-8")) if args.edit else None
    cues, w1 = collect(plan, tl, edit, measure=not args.planned_timing)
    if not cues:
        print("no scripted dialogue or narration text to caption")
        return 1
    lang = "ar" if any(AR.search(c["text"]) for c in cues) else "en"
    maxc = args.max_chars or (40 if lang == "ar" else 42)
    caps, w2 = build(cues, maxc, lang)
    os.makedirs(os.path.dirname(os.path.abspath(args.out + ".srt")), exist_ok=True)
    write_srt(caps, args.out + ".srt")
    write_ass(caps, args.out + ".ass", tl.get("ratio", "16:9"), args.font)
    print(f"{len(caps)} captions ({lang}, ≤{maxc} chars/line) -> {args.out}.srt / {args.out}.ass")
    for w in w1 + w2:
        print(f"  ! {w}")
    return 3 if (w1 or w2) else 0


if __name__ == "__main__":
    sys.exit(main())
