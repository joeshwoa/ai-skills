#!/usr/bin/env python3
"""
assemble.py — the montage: approved clips in, finished video out.

Does the editor's job on a timeline:
  * conforms clips from different models/takes (size, fps, timebase, audio)
  * trims each clip (in/out) and optionally changes its speed
  * joins them with the transition planned for each cut:
      cut · dissolve · fade_black · fade_white · wipe_* · slide_* · zoom_in ·
      circle_open/close · pixelize · radial · whip (blur assist)
      j_cut / l_cut  — sound leads / trails the picture across a cut
      match_cut / morph / whip_pan — designed into the shots themselves;
      here they are hard cuts (whip_pan gets a 0.25 s blur assist)
  * crossfades the audio under every visual transition
  * lays off-screen narration on the timeline, ducks music under it
  * burns captions (.ass/.srt — Arabic shaped correctly via libass) and a logo
  * normalises loudness to the platform target and verifies it
  * writes <output>.timeline.json — where every clip landed — which
    captions.py uses to time captions from the SCRIPT (never from ASR)

USAGE
    python3 assemble.py edit.json                # full quality
    python3 assemble.py edit.json --preview      # fast low-res rough cut for review
    python3 assemble.py edit.json --dry-run      # print the ffmpeg command

edit.json
{
  "output": "final/coffee_9x16.mp4",
  "ratio": "9:16", "fps": 24, "platform": "reels",
  "clips": [
    {"shot": "S01", "file": "takes/S01_t1.mp4", "in": 0.3, "out": 5.8,
     "transition_in": {"type": "fade_black", "duration": 0.6}},
    {"shot": "S02", "file": "takes/S02_t2.mp4", "in": 0.2, "out": 7.6, "speed": 1.0,
     "transition_in": {"type": "j_cut", "audio_offset": 0.4}},
    {"shot": "S03", "file": "takes/S03_t1.mp4", "transition_in": {"type": "dissolve", "duration": 0.5}}
  ],
  "voiceover": [{"file": "vo/N01.wav", "at": 1.5, "gain_db": 0}],
  "music": {"file": "music/bed.mp3", "gain_db": -18, "duck_under_voiceover": true, "fade_in": 1.0},
  "captions": {"file": "final/captions.ass", "burn": true},
  "logo": {"file": "brand/logo.png", "position": "top_right", "scale": 0.14, "margin": 48, "opacity": 0.9},
  "fade_out": 0.6
}
Only "output" and "clips" are required.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
LUFS = {"reels": -14, "tiktok": -14, "shorts": -14, "youtube": -14, "facebook": -14,
        "linkedin": -14, "web": -16, "broadcast": -23}
XFADE = {
    "dissolve": "fade", "crossfade": "fade", "fade_black": "fadeblack", "fade_white": "fadewhite",
    "wipe": "wipeleft", "wipe_left": "wipeleft", "wipe_right": "wiperight", "wipe_up": "wipeup",
    "wipe_down": "wipedown", "slide": "slideleft", "slide_left": "slideleft",
    "slide_right": "slideright", "slide_up": "slideup", "slide_down": "slidedown",
    "zoom_in": "zoomin", "circle_open": "circleopen", "circle_close": "circleclose",
    "whip": "hblur", "whip_pan": "hblur", "pixelize": "pixelize", "radial": "radial",
}
HARD = {"cut", "match_cut", "morph", "j_cut", "l_cut"}
EDGE = 0.04  # tiny audio fade on every segment edge, kills clicks at hard cuts


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def has_audio(path: str) -> bool:
    return bool(run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                     "stream=index", "-of", "csv=p=0", path]).stdout.strip())


def probe_duration(path: str) -> float:
    try:
        return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path]).stdout.strip())
    except ValueError:
        return 0.0


def integrated_lufs(path: str) -> float | None:
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=framelog=quiet",
             "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def fpath(p: str) -> str:
    """Escape a path for use inside a filtergraph option."""
    return p.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,")


def atempo_chain(speed: float) -> str:
    parts, s = [], speed
    while s > 2.0:
        parts.append("atempo=2.0"); s /= 2.0
    while s < 0.5:
        parts.append("atempo=0.5"); s /= 0.5
    parts.append(f"atempo={s:.4f}")
    return ",".join(parts)


def tr_of(c: dict) -> tuple[str, float, float]:
    t = c.get("transition_in") or {}
    if isinstance(t, str):
        t = {"type": t}
    typ = t.get("type", "cut")
    dur = float(t.get("duration", 0.25 if typ == "whip_pan" else 0.5))
    off = float(t.get("audio_offset", 0.5))
    return typ, dur, off


def plan_timeline(clips: list[dict]) -> list[dict]:
    tl, t = [], 0.0
    for i, c in enumerate(clips):
        f = c["file"]
        if not os.path.exists(f):
            raise SystemExit(f"missing clip: {f}")
        src = probe_duration(f)
        t_in = float(c.get("in", 0.0))
        t_out = float(c.get("out", src))
        if t_out > src + 0.05:
            raise SystemExit(f"{f}: out {t_out}s is past the clip's end ({src:.2f}s)")
        speed = float(c.get("speed", 1.0))
        if not 0.25 <= speed <= 4.0:
            raise SystemExit(f"{f}: speed must be 0.25–4.0")
        length = (t_out - t_in) / speed
        if length <= 0.2:
            raise SystemExit(f"{f}: in/out leaves {length:.2f}s")
        typ, tdur, aoff = tr_of(c)
        overlap = 0.0
        if i > 0 and typ == "whip_pan":          # hard cut + short smear assist
            overlap = min(0.25, length / 3, tl[-1]["length"] / 3)
        elif i > 0 and typ in XFADE:
            overlap = min(tdur, length / 2, tl[-1]["length"] / 2)
        start = 0.0 if i == 0 else tl[-1]["start"] + tl[-1]["length"] - overlap
        tl.append({"i": i, "shot": c.get("shot"), "file": f, "src_len": src, "in": t_in,
                   "out": t_out, "speed": speed, "length": length, "start": round(start, 4),
                   "type": typ, "tdur": tdur, "overlap": overlap, "aoff": aoff,
                   "gain": float(c.get("gain_db", 0)), "audio": has_audio(f)})
    audio_plan(tl)
    return tl


WARNINGS: list[str] = []


def audio_plan(tl: list[dict]) -> None:
    """Where each clip's SOUND sits. A J-cut starts clip k's sound `lead`
    seconds before its picture and ends clip k-1's sound at that moment; an
    L-cut runs clip k-1's sound `tail` seconds over clip k's picture and
    starts clip k's own sound only then — so two takes never talk at once."""
    for seg in tl:
        seg.update({"a_lead": 0.0, "a_tail": 0.0, "cut_head": 0.0, "cut_tail": 0.0})
    for k, seg in enumerate(tl):
        if k == 0 or seg["type"] not in ("j_cut", "l_cut"):
            continue
        prev = tl[k - 1]
        want = seg["aoff"]
        if seg["type"] == "j_cut":
            spare = seg["in"] / seg["speed"]              # sound available before the in-point
            lead = min(want, spare, prev["length"] - 0.3, seg["length"] - 0.3)
            lead = max(0.0, lead)
            if lead < want - 0.05:
                WARNINGS.append(f"{seg['shot'] or seg['file']}: J-cut wanted {want:.2f}s of lead-in sound, "
                                f"only {lead:.2f}s available — trim this clip's in-point later "
                                f"(\"in\") to give the sound room" + (" (J-cut has NO effect)" if lead < 0.05 else ""))
            seg["a_lead"], prev["cut_tail"] = lead, lead
        else:
            spare = (prev["src_len"] - prev["out"]) / prev["speed"]   # sound left after prev's out-point
            tail = min(want, spare, seg["length"] - 0.3)
            tail = max(0.0, tail)
            if tail < want - 0.05:
                WARNINGS.append(f"{seg['shot'] or seg['file']}: L-cut wanted {want:.2f}s of the previous "
                                f"clip's sound, only {tail:.2f}s exists after its out-point — set the "
                                f"previous clip's \"out\" earlier" + (" (L-cut has NO effect)" if tail < 0.05 else ""))
            prev["a_tail"], seg["cut_head"] = tail, tail
    for seg in tl:
        sp = seg["speed"]
        seg["a_src_in"] = seg["in"] + (seg["cut_head"] - seg["a_lead"]) * sp
        seg["a_src_out"] = seg["out"] + (seg["a_tail"] - seg["cut_tail"]) * sp
        seg["a_start"] = seg["start"] - seg["a_lead"] + seg["cut_head"]
        seg["a_end"] = seg["a_start"] + (seg["a_src_out"] - seg["a_src_in"]) / sp


def build(edit: dict, preview: bool) -> tuple[list[str], list[dict], float, str]:
    W, H = SIZES[edit.get("ratio", "16:9")]
    if preview:
        W, H = (W // 2) // 2 * 2, (H // 2) // 2 * 2
    fps = edit.get("fps", 24)
    target = LUFS.get(edit.get("platform", "youtube"), -14)
    tl = plan_timeline(edit["clips"])
    total = tl[-1]["start"] + tl[-1]["length"]
    inputs, F = [], []
    n = 0

    # ---- picture ---------------------------------------------------------
    for seg in tl:
        inputs += ["-i", seg["file"]]
        seg["idx"] = n
        F.append(f"[{n}:v]trim={seg['in']}:{seg['out']},setpts=(PTS-STARTPTS)/{seg['speed']},"
                 f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=decrease,"
                 f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,settb=AVTB[v{seg['i']}]")
        n += 1
    cur = "v0"
    first = tl[0]
    for seg in tl[1:]:
        k = seg["i"]
        if seg["overlap"] > 0:
            F.append(f"[{cur}][v{k}]xfade=transition={XFADE[seg['type']]}:duration={seg['overlap']:.3f}"
                     f":offset={seg['start']:.3f}[vx{k}]")
        else:
            F.append(f"[{cur}][v{k}]concat=n=2:v=1:a=0[vx{k}]")
        cur = f"vx{k}"

    post = []
    if first["type"] in ("fade_black", "fade_white"):
        col = "white" if first["type"] == "fade_white" else "black"
        post.append(f"fade=t=in:st=0:d={min(first['tdur'], first['length'] / 2):.3f}:c={col}")
    fo = float(edit.get("fade_out", 0))
    if fo:
        post.append(f"fade=t=out:st={max(0, total - fo):.3f}:d={fo}")
    if post:
        F.append(f"[{cur}]{','.join(post)}[vp]")
        cur = "vp"

    logo = edit.get("logo")
    if logo:
        if not os.path.exists(logo["file"]):
            raise SystemExit(f"missing logo: {logo['file']}")
        inputs += ["-i", logo["file"]]
        lw = int(W * float(logo.get("scale", 0.14)))
        m = int(logo.get("margin", 48) * (0.5 if preview else 1))
        pos = {"top_right": (f"W-w-{m}", f"{m}"), "top_left": (f"{m}", f"{m}"),
               "bottom_right": (f"W-w-{m}", f"H-h-{m}"), "bottom_left": (f"{m}", f"H-h-{m}"),
               "center": ("(W-w)/2", "(H-h)/2")}[logo.get("position", "top_right")]
        F.append(f"[{n}:v]scale={lw}:-1,format=rgba,colorchannelmixer=aa={float(logo.get('opacity', 0.9))}[lg]")
        F.append(f"[{cur}][lg]overlay={pos[0]}:{pos[1]}:format=auto:eof_action=repeat[vl]")
        cur = "vl"
        n += 1

    cap = edit.get("captions")
    if cap and cap.get("burn", True) and preview and not os.path.exists(cap["file"]):
        # the preview is what captions.py is timed from — it can't need them yet
        WARNINGS.append(f"captions {cap['file']} not built yet — preview rendered without them")
        cap = None
    if cap and cap.get("burn", True):
        if not os.path.exists(cap["file"]):
            raise SystemExit(f"missing captions: {cap['file']}")
        filt = "ass" if cap["file"].lower().endswith(".ass") else "subtitles"
        F.append(f"[{cur}]{filt}=filename='{fpath(os.path.abspath(cap['file']))}'[vc]")
        cur = "vc"
    F.append(f"[{cur}]null[vout]")

    # ---- sound: each clip's audio placed on the timeline ----------------
    alabels = []
    for seg in tl:
        if not seg["audio"]:
            continue
        k, sp = seg["i"], seg["speed"]
        src_in, src_out, place = seg["a_src_in"], seg["a_src_out"], seg["a_start"]
        fin = fout = EDGE
        if seg["a_lead"] > 0:
            fin = min(0.2, seg["a_lead"])
        if seg["cut_head"] > 0 or seg["cut_tail"] > 0:     # the other clip owns the sound here
            fin = max(fin, 0.06) if seg["cut_head"] > 0 else fin
            fout = max(fout, 0.12) if seg["cut_tail"] > 0 else fout
        if seg["a_tail"] > 0:
            fout = min(0.25, seg["a_tail"])
        # crossfade under visual transitions
        if k > 0 and seg["overlap"] > 0:
            fin = max(fin, seg["overlap"])
        if k + 1 < len(tl) and tl[k + 1]["overlap"] > 0:
            fout = max(fout, tl[k + 1]["overlap"])
        alen = (src_out - src_in) / sp
        ms = max(0, int(round(place * 1000)))
        F.append(f"[{seg['idx']}:a]atrim={src_in:.3f}:{src_out:.3f},asetpts=PTS-STARTPTS,"
                 f"{atempo_chain(sp) + ',' if abs(sp - 1) > 1e-3 else ''}"
                 f"aresample=48000,aformat=channel_layouts=stereo,volume={seg['gain']}dB,"
                 f"afade=t=in:st=0:d={fin:.3f},afade=t=out:st={max(0, alen - fout):.3f}:d={fout:.3f},"
                 f"adelay={ms}|{ms}[a{k}]")
        alabels.append(f"[a{k}]")
    if not alabels:
        F.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{total:.3f}[a_sil]")
        alabels.append("[a_sil]")
    F.append(f"{''.join(alabels)}amix=inputs={len(alabels)}:normalize=0:duration=longest[dlg]")

    vo_labels = []
    for j, vo in enumerate(edit.get("voiceover") or []):
        if not os.path.exists(vo["file"]):
            raise SystemExit(f"missing voiceover: {vo['file']}")
        inputs += ["-i", vo["file"]]
        ms = int(float(vo.get("at", 0)) * 1000)
        F.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,"
                 f"volume={float(vo.get('gain_db', 0))}dB,adelay={ms}|{ms}[vo{j}]")
        vo_labels.append(f"[vo{j}]")
        n += 1
    mix = ["[dlg]"]
    if vo_labels:
        F.append(f"{''.join(vo_labels)}amix=inputs={len(vo_labels)}:normalize=0:duration=longest[voall]"
                 if len(vo_labels) > 1 else f"{vo_labels[0]}anull[voall]")
    music = edit.get("music")
    if music:
        if not os.path.exists(music["file"]):
            raise SystemExit(f"missing music: {music['file']}")
        inputs += ["-stream_loop", "-1", "-i", music["file"]]
        mfi = float(music.get("fade_in", 0))
        F.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,"
                 f"volume={float(music.get('gain_db', -18))}dB,atrim=0:{total:.3f}"
                 + (f",afade=t=in:st=0:d={mfi}" if mfi else "") + "[mus]")
        n += 1
        if vo_labels and music.get("duck_under_voiceover", True):
            F.append("[voall]asplit=2[voA][voK]")
            F.append("[mus][voK]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[musd]")
            mix += ["[voA]", "[musd]"]
        else:
            mix += (["[voall]"] if vo_labels else []) + ["[mus]"]
    elif vo_labels:
        mix.append("[voall]")
    fade = f",afade=t=out:st={max(0, total - fo):.3f}:d={fo}" if fo else ""
    F.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=longest,"
             f"apad,atrim=0:{total:.3f},loudnorm=I={target}:TP=-1.5:LRA=11{fade}[aout]")

    out = edit["output"]
    if preview:
        root, ext = os.path.splitext(out)
        out = root + "_preview" + ext
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(F),
           "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264",
           "-preset", "veryfast" if preview else "medium", "-crf", "28" if preview else "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-t", f"{total:.3f}", out]
    return cmd, tl, total, out


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble approved clips into a finished video.")
    ap.add_argument("edit")
    ap.add_argument("--preview", action="store_true", help="half-resolution fast render for review")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with open(args.edit, encoding="utf-8") as f:
        edit = json.load(f)
    if edit.get("ratio", "16:9") not in SIZES:
        raise SystemExit(f"ratio must be one of {sorted(SIZES)}")
    cmd, tl, total, out = build(edit, args.preview)
    if args.dry_run:
        print(" ".join(cmd))
        return 0
    r = run(cmd)
    if r.returncode != 0:
        print(r.stderr[-2500:])
        return 1
    target = LUFS.get(edit.get("platform", "youtube"), -14)
    measured = integrated_lufs(out)
    if measured is not None and abs(measured - target) > 0.7:
        tmp = out + ".tmp.mp4"
        r2 = run(["ffmpeg", "-y", "-v", "error", "-i", out, "-c:v", "copy", "-af",
                  f"volume={target - measured:.2f}dB,alimiter=limit=0.84:level=false",
                  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", tmp])
        if r2.returncode == 0:
            os.replace(tmp, out)
            measured = integrated_lufs(out)
    timeline = {"output": os.path.abspath(out), "total": round(total, 3), "fps": edit.get("fps", 24),
                "ratio": edit.get("ratio", "16:9"),
                "clips": [{"shot": s["shot"], "file": s["file"], "in": s["in"], "out": s["out"],
                           "speed": s["speed"], "start": s["start"],
                           "end": round(s["start"] + s["length"], 3), "transition_in": s["type"],
                           "transition_overlap": round(s["overlap"], 3),
                           "audio": {"src_in": round(s["a_src_in"], 3), "src_out": round(s["a_src_out"], 3),
                                     "start": round(s["a_start"], 3), "end": round(s["a_end"], 3)}}
                          for s in tl],
                "voiceover": [{"file": os.path.abspath(v["file"]), "at": float(v.get("at", 0)),
                               "text": v.get("text"), "seconds": probe_duration(v["file"])}
                              for v in edit.get("voiceover") or [] if os.path.exists(v["file"])]}
    with open(out + ".timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=1)
    got = probe_duration(out)
    print(f"{out}  {got:.2f}s (timeline {total:.2f}s)  loudness {measured} LUFS (target {target})")
    print(f"timeline -> {out}.timeline.json")
    for w in WARNINGS:
        print(f"  ! {w}")
    if abs(got - total) > 0.25:
        print("  X output length differs from the timeline — check clip in/out points")
        return 1
    print("Next: qc_clip.py on the output, then watch it end to end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
