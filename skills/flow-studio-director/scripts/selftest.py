#!/usr/bin/env python3
"""
selftest.py — prove the whole pipeline works on THIS machine, in a few minutes,
without Flow and without spending credits.

Checks the environment (python, ffmpeg features the skill relies on:
xfade, libass captions with Arabic shaping, vidstab, loudness), then runs
a miniature project end to end on synthetic media, using the bundled
Arabic sample script:

  breakdown -> plan -> gates (script, cast, storyboard) -> animatic ->
  fake takes -> clip QC -> approvals -> edit fix -> montage with
  transitions -> captions from the script -> burned final -> final QC

Run it once after installing the skill, and again after an ffmpeg update:
    python3 scripts/selftest.py            (keeps nothing)
    python3 scripts/selftest.py --keep     (prints the temp folder to inspect)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable
results = []


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def step(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    return ok


def script(name, *args, cwd=None):
    return sh([PY, os.path.join(HERE, name), *args], cwd=cwd)


PARSER_CASES = """المشهد الأول: الشارع - نهار
هند (25) ماشية بسرعة.
هند: أنا متأخرة!
هنا: استنيني!
عم حسن (60) واقف عند الكشك بيبص عليهم.

مشهد 3
خارجي. محطة. مساء
0:00-0:03: هند بتجري ناحية القطر.
NOTE TO CLIENT: we can shorten this.
الساعة 8:30 والمحطة فاضية.

سلمى
الحقي القطر!

سلمى
يلا بسرعة.

Scene Two: Rooftop
SARA (V.O.)
I never thought I'd be here.
MONTAGE
Shots of the city.
"""


def parser_regressions(tmp: str) -> None:
    f = os.path.join(tmp, "cases.txt")
    open(f, "w", encoding="utf-8").write(PARSER_CASES)
    script("script_breakdown.py", f, "--out", "cases", cwd=tmp)
    an = json.load(open(os.path.join(tmp, "cases", "breakdown.json"), encoding="utf-8"))
    names = {c["name"]: c for c in an["characters"]}
    sc = an["scenes"]
    step("parser: headings with a colon, two-line headings", len(sc) == 3 and sc[0]["location"] == "الشارع"
         and sc[1]["int_ext"] == "EXT" and sc[1]["time"] == "evening" and sc[2]["location"] == "Rooftop",
         str([(s["location"], s["time"]) for s in sc]))
    step("parser: timecodes / NOTE / clock times are not characters",
         not any(re.search(r"\d|NOTE|الساعة", n) for n in names), str(list(names)))
    step("parser: هند and هنا stay two people", "هند" in names and "هنا" in names)
    step("parser: Arabic name-on-its-own-line cues", names.get("سلمى", {}).get("lines") == 2)
    step("parser: MONTAGE is not a character; named V.O. keeps its speaker",
         "Montage" not in names and names.get("Sara", {}).get("vo_lines") == 1)
    step("parser: silent on-screen character is cast", names.get("عم حسن", {}).get("speaks") is False)


def tone_clip(path: str, d: float, bursts: list[tuple[float, float]], freq: int) -> None:
    expr = "+".join(f"between(t,{a},{b})" for a, b in bursts) or "0"
    sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=360x640:r=24:d={d}",
        "-f", "lavfi", "-i", f"sine=f={freq}:d={d}", "-af", f"volume='if({expr},1,0.0)':eval=frame",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", path])


def jl_and_caption_regressions(tmp: str) -> None:
    os.makedirs(os.path.join(tmp, "jl"), exist_ok=True)
    A, B = os.path.join(tmp, "jl", "A.mp4"), os.path.join(tmp, "jl", "B.mp4")
    tone_clip(A, 6, [(1.0, 2.5), (3.2, 4.4)], 440)
    tone_clip(B, 6, [(0.6, 2.0)], 660)
    ed = {"output": "jl/out.mp4", "ratio": "9:16", "fps": 24, "platform": "reels",
          "clips": [{"shot": "A", "file": A, "in": 0, "out": 5},
                    {"shot": "B", "file": B, "in": 0.8, "out": 5, "transition_in": {"type": "j_cut", "audio_offset": 0.5}}]}
    json.dump(ed, open(os.path.join(tmp, "jl", "edit.json"), "w"))
    r = script("assemble.py", "jl/edit.json", "--preview", cwd=tmp)
    tl = json.load(open(os.path.join(tmp, "jl", "out_preview.mp4.timeline.json")))
    a_end, b_start = tl["clips"][0]["audio"]["end"], tl["clips"][1]["audio"]["start"]
    step("J-cut: next sound leads by 0.5s and the previous sound stops there (no double audio)",
         r.returncode == 0 and abs(b_start - 4.5) < 0.02 and abs(a_end - b_start) < 0.02, f"{a_end} / {b_start}")
    ed["clips"][1]["in"] = 0.0
    json.dump(ed, open(os.path.join(tmp, "jl", "edit.json"), "w"))
    r = script("assemble.py", "jl/edit.json", "--preview", cwd=tmp)
    step("J-cut with no spare sound is reported", "NO effect" in r.stdout, r.stdout.strip()[-90:])
    # captions follow the measured speech, not the (deliberately wrong) plan
    plan = {"shots": [{"id": "A", "dialogue": [{"character": "X", "text": "السطر الأول هنا", "start": 0.2, "end": 0.9},
                                               {"character": "X", "text": "والسطر التاني", "start": 1.0, "end": 1.6}]},
                      {"id": "B", "dialogue": []}]}
    json.dump(plan, open(os.path.join(tmp, "jl", "plan.json"), "w"), ensure_ascii=False)
    script("captions.py", "--plan", "jl/plan.json", "--timeline", "jl/out_preview.mp4.timeline.json",
           "--out", "jl/cap", cwd=tmp)
    srt = open(os.path.join(tmp, "jl", "cap.srt"), encoding="utf-8").read()
    times = re.findall(r"(\d\d):(\d\d):(\d\d),(\d{3}) -->", srt)
    starts = [int(h) * 3600 + int(m) * 60 + int(s_) + int(ms) / 1000 for h, m, s_, ms in times]
    step("captions timed from the measured speech in the real clip",
         len(starts) == 2 and abs(starts[0] - 1.0) < 0.2 and abs(starts[1] - 3.2) < 0.2, str(starts))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    # ---- environment -----------------------------------------------------
    step("python >= 3.9", sys.version_info >= (3, 9), sys.version.split()[0])
    for tool in ("ffmpeg", "ffprobe"):
        if not step(f"{tool} installed", shutil.which(tool) is not None):
            print("Install ffmpeg (macOS: brew install ffmpeg) and re-run.")
            return 1
    filters = sh(["ffmpeg", "-hide_banner", "-filters"]).stdout
    need = {"xfade": "transitions", "ass": "burned captions", "subtitles": "burned captions",
            "loudnorm": "loudness", "sidechaincompress": "music ducking", "tpad": "hold frames",
            "zoompan": "animatic"}
    for f, why in need.items():
        step(f"ffmpeg filter {f}", f" {f} " in filters, why)
    step("ffmpeg vidstab (optional)", " vidstabdetect " in filters,
         "stabilize falls back to deshake if missing")
    conf = sh(["ffmpeg", "-hide_banner", "-buildconf"]).stdout
    step("libass + fribidi/harfbuzz (Arabic captions)",
         "libass" in conf and ("fribidi" in conf or "harfbuzz" in conf),
         "needed for correct Arabic shaping in burned captions")

    tmp = tempfile.mkdtemp(prefix="fsd_selftest_")
    try:
        # ---- analysis --------------------------------------------------
        parser_regressions(tmp)
        r = script("script_breakdown.py", os.path.join(ROOT, "examples", "sample_client_script_ar.txt"),
                   "--out", "bd0", "--target-seconds", "30", cwd=tmp)
        bd0 = json.load(open(os.path.join(tmp, "bd0", "breakdown.json"), encoding="utf-8"))
        step("typo'd name kept separate + asked (not merged on a guess)",
             len(bd0["characters"]) == 3 and any("كرين" in q for q in bd0["questions"]))
        r = script("script_breakdown.py", os.path.join(ROOT, "examples", "sample_client_script_ar.txt"),
                   "--out", "bd", "--target-seconds", "30", "--alias", "كرين=كريم", cwd=tmp)
        sk = os.path.join(tmp, "bd", "plan_skeleton.json")
        step("script breakdown", r.returncode in (0, 3) and os.path.exists(sk), r.stdout.splitlines()[0] if r.stdout else r.stderr[-200:])
        plan = json.load(open(sk, encoding="utf-8"))
        # asset fields written into the plan must NOT count as a built character
        for c in plan["characters"]:
            c.update({"sheet": f"chars/{c['id']}.png", "flow_character": c["name"]})
        for s in plan["shots"]:
            s["routing_reviewed"] = True
        plan["budget_credits"] = 200
        json.dump(plan, open(os.path.join(tmp, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False)
        r = script("shot_plan.py", "plan.json", cwd=tmp)
        step("shot plan validates", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-200:])

        # ---- gates -------------------------------------------------------
        st = ["--state", "state.json"]
        PS = lambda *x: script("project_state.py", *st, *x, cwd=tmp)
        U = ["--by", "user", "--note", "selftest: user said yes"]
        PS("init", "plan.json", "--mode", "per_shot")
        blocked = PS("can-generate", "S01", "--credits", "7").returncode == 11
        no_by = PS("gate", "script", "approve").returncode == 2
        take_blocked = PS("start-take", "S01", "--credits", "7").returncode == 11
        appr_blocked = PS("approve", "S01", *U).returncode == 11
        step("--by is required; take/approve refused before the gates", no_by and take_blocked and appr_blocked)
        PS("gate", "script", "approve", *U)
        kf_blocked = PS("can-build-asset", "keyframe").returncode == 11
        c0 = plan["characters"][0]["id"]
        early = PS("cast-approve", c0, *U).returncode != 0       # plan fields ignored -> not built
        ghost = PS("cast-set", c0, "--sheet", "chars/nope.png").returncode != 0
        step("gates block shots and keyframes until script+cast", blocked and kf_blocked)
        step("character can't be approved from plan fields or missing files", early and ghost)
        os.makedirs(os.path.join(tmp, "chars"))
        for c in plan["characters"]:
            files = []
            for part in ("sheet", "expressions", "consistency"):
                f = f"chars/{c['id']}_{part}.png"
                sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=256x256",
                    "-frames:v", "1", os.path.join(tmp, f)])
                files += [f"--{part}", f]
            PS("cast-set", c["id"], *files, "--flow-character", c["name"], "--voice", f"{c['id']}_VOICE")
            PS("cast-approve", c["id"], *U)
        step("cast gate locks after every character is built + approved",
             PS("gate", "cast", "approve", *U).returncode == 0)
        # reopening the script reopens everything after it
        PS("gate", "script", "reopen", *U)
        g = json.load(open(os.path.join(tmp, "state.json"), encoding="utf-8"))["gates"]
        cascade = g["cast"]["status"] == "pending" and g["storyboard"]["status"] == "pending"
        PS("gate", "script", "approve", *U)
        PS("gate", "cast", "approve", *U)
        # a new character in the plan reopens the cast gate and blocks production
        plan2 = json.loads(json.dumps(plan))
        plan2["characters"].append({"id": "BARISTA", "name": "Barista", "speaks": False})
        plan2["shots"][0]["cast"] = plan2["shots"][0].get("cast", []) + ["BARISTA"]
        json.dump(plan2, open(os.path.join(tmp, "plan2.json"), "w", encoding="utf-8"), ensure_ascii=False)
        PS("sync-plan", "plan2.json")
        g = json.load(open(os.path.join(tmp, "state.json"), encoding="utf-8"))["gates"]
        reopened = g["cast"]["status"] == "pending"
        PS("gate", "storyboard", "waive", *U)
        still = PS("can-generate", plan2["shots"][0]["id"], "--credits", "7").returncode == 11
        PS("sync-plan", "plan.json")
        PS("cast-remove", "BARISTA", "--by", "user", "--note", "selftest")
        PS("gate", "cast", "approve", *U)
        PS("gate", "storyboard", "reopen", *U)
        step("reopen cascades; sync-plan with a new character re-locks the cast", cascade and reopened and still)

        # ---- keyframes + animatic -------------------------------------------
        os.makedirs(os.path.join(tmp, "kf"))
        cols = ["0xC8783C", "0x3C78C8", "0x3CA05A", "0xE6E65A", "0x8C5AC8", "0xC85A8C"]
        for i, s in enumerate(plan["shots"][:4]):
            sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={cols[i % 6]}:s=720x1280",
                "-frames:v", "1", os.path.join(tmp, "kf", f"{s['id']}_start.png")])
        r = script("animatic.py", "--plan", "plan.json", "--keyframes", "kf", "--out", "review/animatic.mp4", cwd=tmp)
        step("animatic from keyframes", r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[0][:90])
        PS("gate", "storyboard", "approve", *U)

        # ---- fake takes -> QC -> approve -------------------------------------
        os.makedirs(os.path.join(tmp, "takes"))
        clips, ok_all = [], True
        for i, s in enumerate(plan["shots"]):
            f = os.path.join(tmp, "takes", f"{s['id']}_t1.mp4")
            d = s["duration"]
            sh(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                f"testsrc2=size=720x1280:rate=24:duration={d}", "-f", "lavfi", "-i",
                f"sine=f={300 + 60 * i}:d={d}", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", f])
            cost = sh([PY, os.path.join(HERE, "shot_plan.py"), "plan.json", "--json"], cwd=tmp)
            credits = next(x["cost"] for x in json.loads(cost.stdout)["rows"] if x["id"] == s["id"])
            gate = script("project_state.py", *st, "can-generate", s["id"], "--credits", str(credits), cwd=tmp)
            ok_all &= gate.returncode == 0
            script("project_state.py", *st, "start-take", s["id"], "--credits", str(credits), cwd=tmp)
            q = script("qc_clip.py", f, "--duration", str(d), "--ratio", "9:16", "--out", f + "_qc", cwd=tmp)
            verdict = "PASS" if q.returncode in (0, 3) else "FAIL"
            script("project_state.py", *st, "log-take", s["id"], "--verdict", verdict, "--file", f, cwd=tmp)
            PS("approve", s["id"], *U)
            tr = s.get("transition_in") or {"type": "cut"}
            clips.append({"shot": s["id"], "file": f, "in": 0.2, "out": d, "transition_in": tr})
        step("per-shot gate, take, QC, approval loop", ok_all)

        # ---- edit fix, montage, captions, final -------------------------------
        fixed = clips[0]["file"].replace(".mp4", "_fix.mp4")
        r = script("edit_clip.py", clips[0]["file"], fixed, "--cut-out", "1", "1.3", "--temperature", "5600", cwd=tmp)
        step("mechanical edit (cut-out + grade)", r.returncode == 0 and os.path.exists(fixed))
        clips[0]["file"] = fixed
        clips[0]["out"] = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                    "csv=p=0", fixed]).stdout.strip())
        clips[1]["transition_in"] = {"type": "dissolve", "duration": 0.4}
        edit = {"output": "final/test.mp4", "ratio": "9:16", "fps": 24, "platform": "reels", "clips": clips,
                "captions": {"file": "final/captions.ass", "burn": True}}      # not built yet
        json.dump(edit, open(os.path.join(tmp, "edit.json"), "w"), ensure_ascii=False)
        r = script("assemble.py", "edit.json", "--preview", cwd=tmp)
        step("preview renders before captions exist", r.returncode == 0, (r.stdout or r.stderr).strip()[-80:])
        edit.pop("captions")
        json.dump(edit, open(os.path.join(tmp, "edit.json"), "w"), ensure_ascii=False)
        r = script("assemble.py", "edit.json", cwd=tmp)
        step("montage with transitions + loudness", r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[0][-70:])
        r = script("captions.py", "--plan", "plan.json", "--timeline", "final/test.mp4.timeline.json",
                   "--out", "final/captions", cwd=tmp)
        step("captions from the script", r.returncode in (0, 3) and os.path.exists(os.path.join(tmp, "final", "captions.ass")),
             (r.stdout or r.stderr).strip().splitlines()[0][:80])
        edit["captions"] = {"file": "final/captions.ass", "burn": True}
        edit["output"] = "final/test_captioned.mp4"
        json.dump(edit, open(os.path.join(tmp, "edit.json"), "w"), ensure_ascii=False)
        r = script("assemble.py", "edit.json", cwd=tmp)
        step("burned Arabic captions", r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[0][-60:])
        q = script("qc_clip.py", "final/test_captioned.mp4", "--ratio", "9:16", "--expect-audio",
                   "--out", "final/qc", cwd=tmp)
        step("final QC runs", q.returncode in (0, 3), q.stdout.splitlines()[0] if q.stdout else "")
        jl_and_caption_regressions(tmp)
        g1 = PS("gate", "rough_cut", "approve", *U).returncode
        g2 = PS("gate", "final", "approve", *U).returncode
        nxt = script("project_state.py", *st, "next", cwd=tmp).stdout.strip()
        step("rough_cut + final gates close, project DELIVERED", g1 == 0 and g2 == 0 and nxt == "DELIVERED", nxt)
    finally:
        if a.keep:
            print(f"\nkept: {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    bad = [n for n, ok, _ in results if not ok and "optional" not in n]
    print(f"\n{len(results) - len(bad)}/{len(results)} checks passed" + (f" — FAILED: {bad}" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
