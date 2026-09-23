#!/usr/bin/env python3
"""
shot_plan.py — validate a project's shot plan and price it, before a single
credit is spent.

Every shot in a plan is a routing decision (model, mode, duration,
resolution, outputs, keyframes, continuation). This script checks each
decision against the platform's verified capability matrix
(references/platforms/<platform>/capabilities.json), checks spoken
dialogue fits the time it has, and prints a per-shot and total credit
estimate with the cheapest sensible alternative beside each shot.

It exists because the two most expensive mistakes in AI video are
(1) routing a shot to a feature the model does not have — you find out
after paying — and (2) dialogue that does not fit the clip, which forces
a regeneration. Both are checkable on paper.

USAGE
    python3 shot_plan.py plan.json
    python3 shot_plan.py plan.json --json          # machine-readable
    python3 shot_plan.py plan.json --capabilities path/to/capabilities.json

EXIT CODES
    0  plan is valid (warnings allowed)
    1  plan has errors — fix before generating
    2  plan is valid but over budget

PLAN FORMAT  (see examples/sample_plan.json)
{
  "project": "Name", "platform": "google-flow", "aspect_ratio": "9:16",
  "language": "ar-EG", "budget_credits": 150,
  "shots": [{
     "id": "S01", "beat": "one line", "duration": 8,
     "model": "omni-1.1-flash", "mode": "ingredients",
     "resolution": "720p", "outputs": 1,
     "keyframes": {"start": true, "end": false, "model": "nano-banana-2"},
     "ingredients": ["HANA_REF", "HANA_VOICE"],
     "dialogue": [{"character": "Hana", "text": "...", "start": 1.0, "end": 4.2}],
     "continuation": "hard_cut", "draft_first": false
  }]
}
modes: text | frames_first | frames_first_last | ingredients | video_edit | extend
continuation: hard_cut | keyframe_chain | ingredients | extend | first_shot
Full field reference: references/plan-schema.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CAPS = os.path.join(HERE, "..", "references", "platforms", "google-flow", "capabilities.json")

# Comfortable spoken pace, in words per second, for subtitles-free lip-synced
# dialogue. Above MAX the model rushes, clips words, or runs past the clip.
# Arabic words carry more syllables on average (attached pronouns,
# prefixes), so its ceiling is lower than English.
PACE = {
    "ar": {"target": (2.0, 2.6), "max": 3.0},
    "en": {"target": (2.3, 3.0), "max": 3.5},
    "default": {"target": (2.0, 2.8), "max": 3.2},
}
MIN_LINE_WINDOW = 1.2          # seconds; shorter than this never sounds natural
MAX_EXTEND_CHAIN = 3           # quality drifts along an extend chain
DRAFT_RATIO_ESTIMATE = 7 / 15  # Omni 360p vs 720p at 10s — the only verified 360p point


def load_caps(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def lang_key(lang: str | None) -> str:
    if not lang:
        return "default"
    base = lang.split("-")[0].lower()
    return base if base in PACE else "default"


def count_words(text: str) -> int:
    # Strip bracketed stage directions like [whispers] — not spoken.
    text = re.sub(r"\[[^\]]*\]", " ", text)
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def shot_cost(caps: dict, model: str, res: str, dur: int, outputs: int) -> tuple[float | None, bool]:
    """Return (credits, verified). None when the combination has no data."""
    m = caps["video_models"].get(model)
    if not m:
        return None, False
    table = m.get("cost", {})
    verified = m.get("cost_verified", {})
    if res in table and str(dur) in table[res]:
        ok = dur in verified.get(res, [])
        return table[res][str(dur)] * outputs, ok
    # Estimate 360p from 720p using the one verified ratio.
    if res == "360p" and "720p" in table and str(dur) in table["720p"]:
        return round(table["720p"][str(dur)] * DRAFT_RATIO_ESTIMATE) * outputs, False
    return None, False


def needs_voice(shot: dict) -> bool:
    ings = " ".join(shot.get("ingredients") or []).lower()
    return bool(shot.get("dialogue")) or "voice" in ings


def cheapest_alternative(caps: dict, shot: dict) -> str | None:
    """Suggest the cheapest model that supports the same mode and length —
    and, for dialogue shots, only models known to take voice assets, so a
    'cheaper' suggestion never silently drops a character's voice."""
    mode = shot.get("mode")
    dur = shot.get("duration")
    cur_cost, _ = shot_cost(caps, shot["model"], shot.get("resolution", "720p"), dur, 1)
    best = None
    for name, m in caps["video_models"].items():
        if name == shot["model"] or mode not in m["modes"] or dur not in m["durations"]:
            continue
        if needs_voice(shot) and m.get("voice_assets") is False:
            continue
        c, _ = shot_cost(caps, name, "720p", dur, 1)
        if c is not None and (cur_cost is None or c < cur_cost) and (best is None or c < best[1]):
            best = (name, c)
    if best:
        return f"{best[0]} @720p = {best[1]} cr/output"
    return None


def validate(plan: dict, caps: dict) -> dict:
    errors, warnings, rows = [], [], []
    vids = caps["video_models"]
    ratio = plan.get("aspect_ratio")
    if ratio and ratio not in caps["aspect_ratios"]["video"]:
        errors.append(f"plan aspect_ratio {ratio!r} not supported for video "
                      f"(use {caps['aspect_ratios']['video']})")
    lk = lang_key(plan.get("language"))
    pace = PACE[lk]

    shots = plan.get("shots") or []
    if not shots:
        errors.append("plan has no shots")
    ids = [s.get("id") for s in shots]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"duplicate shot ids: {sorted(dupes)}")

    by_id = {s.get("id"): s for s in shots}
    total = 0.0
    any_unverified = False
    extend_chain = 0

    for idx, s in enumerate(shots):
        sid = s.get("id", f"#{idx+1}")
        E = lambda msg: errors.append(f"{sid}: {msg}")
        W = lambda msg: warnings.append(f"{sid}: {msg}")

        model, mode = s.get("model"), s.get("mode")
        dur, res = s.get("duration"), s.get("resolution", "720p")
        outs = s.get("outputs", 1)
        m = vids.get(model)

        if not m:
            E(f"unknown model {model!r}; known: {sorted(vids)}")
            rows.append({"id": sid, "model": model, "cost": None})
            continue

        # --- mode / feature support -------------------------------------
        if mode == "extend":
            if not m.get("extend"):
                E(f"{model} cannot extend. Extend runs on veo-3.1-lite from an 8s Veo clip")
            prev = by_id.get(s.get("extends"))
            if not prev:
                E("extend shot needs 'extends': <id of the clip it continues>")
            else:
                if not str(prev.get("model", "")).startswith("veo-3.1"):
                    E(f"cannot extend {prev.get('id')}: it is {prev.get('model')}; "
                      f"only Veo 3.1 clips extend (not Omni, not uploads)")
                if prev.get("duration") != 8:
                    E(f"cannot extend {prev.get('id')}: extend needs an 8s source clip")
                if not prev.get("ends_on_stillness"):
                    W(f"{prev.get('id')} is not marked ends_on_stillness — extensions "
                      f"from a clip that ends mid-motion usually show a visible seam")
            extend_chain += 1
            if extend_chain > MAX_EXTEND_CHAIN:
                W(f"extend chain is {extend_chain} long — quality drifts; rebuild from a fresh keyframe")
        else:
            extend_chain = 0
            if mode not in m["modes"]:
                E(f"{model} does not support mode {mode!r} (supports {m['modes']})")

        if mode == "ingredients" and dur not in m.get("ingredients_durations", m["durations"]):
            E(f"{model} ingredients only at {m.get('ingredients_durations', m['durations'])}s")

        # --- duration / resolution / outputs ----------------------------
        if mode != "extend" and dur not in m["durations"]:
            note = m.get("durations_note", "")
            E(f"{model} does not offer {dur}s (offers {m['durations']}). {note}".strip())
        if res not in m["resolutions"]:
            E(f"{model} does not offer {res} (offers {m['resolutions']})")
        if outs not in caps["outputs_per_generation"]:
            E(f"outputs must be one of {caps['outputs_per_generation']}")
        if mode == "video_edit" and dur and dur > m.get("edit_max_seconds", 0):
            E(f"video edits are limited to {m.get('edit_max_seconds')}s per pass")

        # --- keyframes: when an image is required, and when it is wasted --
        kf = s.get("keyframes") or {}
        if mode == "frames_first_last" and not (kf.get("start") and kf.get("end")):
            E("frames_first_last needs both a start and an end keyframe")
        if mode == "frames_first" and not kf.get("start"):
            E("frames_first needs a start keyframe")
        if mode == "text" and s.get("characters_recurring"):
            W("recurring character in a text-only shot — identity will drift; "
              "route to ingredients or lock identity in a keyframe")
        if mode == "frames_first_last" and s.get("large_move"):
            W("marked large_move with first+last frames — frames far apart force "
              "morphing; bring the end frame closer or split the shot")

        # --- dialogue fit ------------------------------------------------
        lines = s.get("dialogue") or []
        prev_end = None
        for j, ln in enumerate(sorted(lines, key=lambda l: l.get("start", 0))):
            words = count_words(ln.get("text", ""))
            st, en = ln.get("start"), ln.get("end")
            who = ln.get("character", "?")
            if st is None or en is None:
                W(f"line {j+1} ({who}) has no start/end — cannot check fit")
                continue
            win = en - st
            if dur and en > dur + 0.01:
                E(f"line {j+1} ({who}) ends at {en}s, past the {dur}s clip")
            if win < MIN_LINE_WINDOW:
                W(f"line {j+1} ({who}) window {win:.1f}s < {MIN_LINE_WINDOW}s — "
                  f"merge with a neighbour or widen it")
            if win > 0:
                wps = words / win
                lo, hi = pace["target"]
                if wps > pace["max"]:
                    E(f"line {j+1} ({who}) is {words} words in {win:.1f}s = {wps:.1f} w/s "
                      f"(max {pace['max']} for {lk}) — shorten or split across shots")
                elif wps > hi:
                    W(f"line {j+1} ({who}) {wps:.1f} w/s is brisk (comfortable {lo}-{hi})")
            if prev_end is not None and st < prev_end - 0.05 and not ln.get("interrupts"):
                W(f"line {j+1} ({who}) overlaps the previous line — mark 'interrupts': true if intended")
            prev_end = en
        speakers = {ln.get("character") for ln in lines}
        if len(speakers) > 2:
            W(f"{len(speakers)} speakers in one clip — models often swap voices; "
              f"keep to 1-2 speakers per shot")

        # --- cost --------------------------------------------------------
        cost, verified = (None, False)
        if mode == "extend":
            cost, _ = shot_cost(caps, "veo-3.1-lite", "720p", 8, outs)
            verified = bool(vids.get("veo-3.1-lite", {}).get("extend_cost_verified"))
        else:
            cost, verified = shot_cost(caps, model, res, dur, outs)
        draft = 0.0
        if s.get("draft_first") and mode != "extend":
            dc, _ = shot_cost(caps, "omni-1.1-flash", "360p", 10 if dur == 10 else dur, 1)
            if dc:
                draft = dc
                verified = verified and False
        if cost is None:
            W("no cost data for this combination — read the live cost in the UI")
        else:
            total += cost + draft
        any_unverified |= not verified
        rows.append({
            "id": sid, "beat": s.get("beat", ""), "model": model, "mode": mode,
            "duration": dur, "resolution": res, "outputs": outs,
            "cost": cost, "draft_cost": draft or None, "verified": verified,
            "keyframes": kf, "alternative": cheapest_alternative(caps, s) if mode != "extend" else None,
        })

    budget = plan.get("budget_credits")
    over = budget is not None and total > budget
    if budget is not None and not over and total > 0.75 * budget:
        warnings.append(f"plan uses {total:.0f}/{budget} credits (>75%) — no room for retakes")
    return {
        "errors": errors, "warnings": warnings, "rows": rows,
        "total_credits": round(total, 1), "budget": budget, "over_budget": over,
        "has_estimates": any_unverified,
        "retake_reserve_suggested": round(total * 0.3, 1),
    }


def print_report(plan: dict, r: dict) -> None:
    print(f"PROJECT: {plan.get('project', '?')}  platform={plan.get('platform')}  "
          f"ratio={plan.get('aspect_ratio')}  language={plan.get('language')}")
    print()
    hdr = f"{'SHOT':6} {'MODEL':16} {'MODE':18} {'DUR':>4} {'RES':5} {'xN':>3} {'CREDITS':>8}  NOTE"
    print(hdr)
    print("-" * len(hdr))
    for row in r["rows"]:
        c = row.get("cost")
        cs = "?" if c is None else (f"{c:g}" + ("" if row.get("verified") else "*"))
        if row.get("draft_cost"):
            cs += f"+{row['draft_cost']:g}d"
        note = row.get("alternative") or ""
        note = f"cheaper: {note}" if note else ""
        print(f"{row['id']:6} {str(row.get('model')):16} {str(row.get('mode')):18} "
              f"{str(row.get('duration')):>4} {str(row.get('resolution')):5} "
              f"{str(row.get('outputs')):>3} {cs:>8}  {note}")
    print("-" * len(hdr))
    b = r["budget"]
    print(f"TOTAL: {r['total_credits']:g} credits"
          + (f" / budget {b}" if b is not None else "")
          + f"   (+ keep ~{r['retake_reserve_suggested']:g} for retakes)")
    print("Keyframe images on Nano Banana cost 0 credits on the verified plan.")
    if r["has_estimates"]:
        print("* = estimate or unverified combination. Read the live cost in Flow before generating.")
    if r["warnings"]:
        print("\nWARNINGS")
        for w in r["warnings"]:
            print(f"  ! {w}")
    if r["errors"]:
        print("\nERRORS — fix before generating")
        for e in r["errors"]:
            print(f"  X {e}")
    elif r["over_budget"]:
        print("\nOVER BUDGET — drop outputs to x1, move non-hero shots to Omni/Lite, "
              "or cut shots.")
    else:
        print("\nPlan is valid.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate and price an AI video shot plan.")
    ap.add_argument("plan")
    ap.add_argument("--capabilities", default=DEFAULT_CAPS)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    caps = load_caps(args.capabilities)
    r = validate(plan, caps)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print_report(plan, r)
    if r["errors"]:
        return 1
    if r["over_budget"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
