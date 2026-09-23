#!/usr/bin/env python3
"""
edit_clip.py — fix a clip mechanically, for zero credits.

Most "this take is almost right" problems are edits, not regenerations:
a glitchy half-second, a clip that starts late, the wrong framing for
9:16, a flat grade, a clip that must end on a still frame before it can be
extended. This does them in one ffmpeg pass (two for stabilisation) and
never touches the original file. Anything that changes what is IN the
picture (a face, an object, wardrobe, an action) is not an edit — that is
Omni video-to-video or a regeneration (references/editing.md).

USAGE (combine any options; they apply in the order listed below)
  python3 edit_clip.py in.mp4 out.mp4 [options]

  --trim IN OUT            keep IN..OUT seconds
  --cut-out A B            remove A..B (e.g. a glitch) and close the gap   (repeatable)
  --reverse                play backwards
  --speed X                0.25–4.0, pitch preserved
  --stabilize              two-pass vidstab (falls back to deshake)
  --reframe RATIO          crop to 9:16 / 16:9 / 1:1 / 4:5 (with --focus-x/--focus-y 0..1)
  --zoom Z                 punch-in, e.g. 1.15 (uses --focus-x/--focus-y)
  --brightness B --contrast C --saturation S --gamma G     (eq filter)
  --temperature K          colour temperature, e.g. 5200 (warmer <6500< cooler)
  --lut file.cube          apply a 3D LUT (project look)
  --denoise --sharpen
  --hold-start S --hold-end S   freeze first/last frame S seconds
                            (--hold-end makes a clip "end on stillness" before extending)
  --fade-in S --fade-out S (picture and sound)
  --mute | --replace-audio file | --volume DB | --audio-denoise
  --size WxH               output size (default: keep; reframe defaults to 1080-wide)
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

RATIOS = {"9:16": (9, 16), "16:9": (16, 9), "1:1": (1, 1), "4:5": (4, 5)}
TARGET = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: str) -> tuple[float, bool]:
    d = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout
    a = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
             "-of", "csv=p=0", path]).stdout.strip()
    return float(d.strip() or 0), bool(a)


def has_filter(name: str) -> bool:
    return f" {name} " in run(["ffmpeg", "-hide_banner", "-filters"]).stdout


def atempo(s: float) -> list[str]:
    out = []
    while s > 2.0:
        out.append("atempo=2.0"); s /= 2
    while s < 0.5:
        out.append("atempo=0.5"); s /= 0.5
    out.append(f"atempo={s:.4f}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Mechanical clip edits (no credits).")
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--trim", nargs=2, type=float, metavar=("IN", "OUT"))
    ap.add_argument("--cut-out", nargs=2, type=float, action="append", metavar=("A", "B"))
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--stabilize", action="store_true")
    ap.add_argument("--reframe", choices=sorted(RATIOS))
    ap.add_argument("--zoom", type=float)
    ap.add_argument("--focus-x", type=float, default=0.5)
    ap.add_argument("--focus-y", type=float, default=0.5)
    ap.add_argument("--brightness", type=float); ap.add_argument("--contrast", type=float)
    ap.add_argument("--saturation", type=float); ap.add_argument("--gamma", type=float)
    ap.add_argument("--temperature", type=int)
    ap.add_argument("--lut")
    ap.add_argument("--denoise", action="store_true"); ap.add_argument("--sharpen", action="store_true")
    ap.add_argument("--hold-start", type=float); ap.add_argument("--hold-end", type=float)
    ap.add_argument("--fade-in", type=float); ap.add_argument("--fade-out", type=float)
    ap.add_argument("--mute", action="store_true"); ap.add_argument("--replace-audio")
    ap.add_argument("--volume", type=float); ap.add_argument("--audio-denoise", action="store_true")
    ap.add_argument("--size")
    a = ap.parse_args()

    if os.path.abspath(a.src) == os.path.abspath(a.dst):
        raise SystemExit("write to a new file — never overwrite the original take")
    dur, has_a = probe(a.src)
    if dur <= 0:
        raise SystemExit(f"cannot read {a.src}")
    V, A = [], []
    length = dur

    if a.trim:
        i, o = a.trim
        if not 0 <= i < o <= dur + 0.05:
            raise SystemExit(f"--trim must be within 0..{dur:.2f}")
        V += [f"trim={i}:{o}", "setpts=PTS-STARTPTS"]
        A += [f"atrim={i}:{o}", "asetpts=PTS-STARTPTS"]
        length = o - i
    for ca, cb in a.cut_out or []:
        if not 0 <= ca < cb <= length + 0.05:
            raise SystemExit(f"--cut-out {ca} {cb} is outside 0..{length:.2f}")
        V += [f"select='not(between(t,{ca},{cb}))'", "setpts=N/FRAME_RATE/TB"]
        A += [f"aselect='not(between(t,{ca},{cb}))'", "asetpts=N/SR/TB"]
        length -= (cb - ca)
    if a.reverse:
        V.append("reverse"); A.append("areverse")
    if a.speed:
        if not 0.25 <= a.speed <= 4:
            raise SystemExit("--speed must be 0.25–4.0")
        V.append(f"setpts=PTS/{a.speed}"); A += atempo(a.speed)
        length /= a.speed

    trf = None
    if a.stabilize:
        if has_filter("vidstabdetect"):
            trf = tempfile.NamedTemporaryFile(suffix=".trf", delete=False).name
            pre = ",".join(V + [f"vidstabdetect=shakiness=6:accuracy=15:result={trf}"])
            r = run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-vf", pre, "-f", "null", "-"])
            if r.returncode != 0:
                raise SystemExit("stabilisation analysis failed:\n" + r.stderr[-800:])
            V += [f"vidstabtransform=input={trf}:smoothing=20:zoom=2", "unsharp=5:5:0.5"]
        else:
            V.append("deshake")

    fx, fy = min(max(a.focus_x, 0), 1), min(max(a.focus_y, 0), 1)
    if a.reframe:
        rw, rh = RATIOS[a.reframe]
        r = f"({rw}/{rh})"
        V.append(f"crop=w='if(gt(iw/ih,{r}),ih*{r},iw)':h='if(gt(iw/ih,{r}),ih,iw/{r})'"
                 f":x='(iw-ow)*{fx}':y='(ih-oh)*{fy}'")
        if not a.size:
            a.size = "x".join(map(str, TARGET[a.reframe]))
    if a.zoom:
        if not 1.0 < a.zoom <= 2.0:
            raise SystemExit("--zoom must be between 1.0 and 2.0 (beyond that the image falls apart)")
        V.append(f"crop=iw/{a.zoom}:ih/{a.zoom}:(iw-ow)*{fx}:(ih-oh)*{fy}")
        V.append(f"scale=iw*{a.zoom}:ih*{a.zoom}:flags=lanczos")
    eq = [f"{k}={v}" for k, v in (("brightness", a.brightness), ("contrast", a.contrast),
                                   ("saturation", a.saturation), ("gamma", a.gamma)) if v is not None]
    if eq:
        V.append("eq=" + ":".join(eq))
    if a.temperature:
        V.append(f"colortemperature=temperature={a.temperature}")
    if a.lut:
        if not os.path.exists(a.lut):
            raise SystemExit(f"missing LUT {a.lut}")
        V.append(f"lut3d=file='{a.lut}'")
    if a.denoise:
        V.append("hqdn3d=3:3:6:6")
    if a.sharpen:
        V.append("unsharp=5:5:0.6")
    if a.size:
        w, h = a.size.lower().split("x")
        V.append(f"scale={w}:{h}:flags=lanczos,setsar=1")
    if a.hold_start:
        V.append(f"tpad=start_mode=clone:start_duration={a.hold_start}")
        A.append(f"adelay={int(a.hold_start * 1000)}|{int(a.hold_start * 1000)}")
        length += a.hold_start
    if a.hold_end:
        V.append(f"tpad=stop_mode=clone:stop_duration={a.hold_end}")
        A.append(f"apad=pad_dur={a.hold_end}")
        length += a.hold_end
    if a.fade_in:
        V.append(f"fade=t=in:st=0:d={a.fade_in}"); A.append(f"afade=t=in:st=0:d={a.fade_in}")
    if a.fade_out:
        V.append(f"fade=t=out:st={max(0, length - a.fade_out):.3f}:d={a.fade_out}")
        A.append(f"afade=t=out:st={max(0, length - a.fade_out):.3f}:d={a.fade_out}")
    if a.volume is not None:
        A.append(f"volume={a.volume}dB")
    if a.audio_denoise:
        A.append("afftdn=nf=-25")
    V.append("format=yuv420p")

    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.src]
    if a.replace_audio:
        cmd += ["-i", a.replace_audio]
    fg = [f"[0:v]{','.join(V)}[v]"]
    maps = ["-map", "[v]"]
    if a.replace_audio:
        fg.append(f"[1:a]aresample=48000,apad,atrim=0:{length:.3f},asetpts=PTS-STARTPTS[a]")  # pad, never loop
        maps += ["-map", "[a]"]
    elif has_a and not a.mute:
        fg.append(f"[0:a]{','.join(A) if A else 'anull'}[a]")
        maps += ["-map", "[a]"]
    cmd += ["-filter_complex", ";".join(fg), *maps, "-c:v", "libx264", "-crf", "17", "-preset", "medium",
            "-pix_fmt", "yuv420p"]
    if "[a]" in " ".join(maps):
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-t", f"{length:.3f}", "-movflags", "+faststart", a.dst]
    os.makedirs(os.path.dirname(os.path.abspath(a.dst)) or ".", exist_ok=True)
    r = run(cmd)
    if trf and os.path.exists(trf):
        os.remove(trf)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    got, _ = probe(a.dst)
    print(f"{a.dst}  {got:.2f}s (from {dur:.2f}s)")
    print("Re-run qc_clip.py on the result before using it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
