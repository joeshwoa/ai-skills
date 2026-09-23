#!/usr/bin/env python3
"""
project_state.py — the project's memory and its spending brake.

Two jobs:
1. Remember everything across sessions and tools: which shots exist, every
   take, its QC verdict, what it cost, which take is approved. A new chat
   (or a different AI tool) resumes from state.json without re-asking.
2. Enforce the autonomy mode the user chose — deterministically, not by
   the agent's good intentions. Before EVERY click on Generate, the agent
   runs `can-generate`. The exit code decides:
       0   go ahead
       10  stop and ask the user first
       11  hard stop (budget, repeated failures, price changed, generation in
           flight, dependency not approved…) — report and wait

MODES
  guided          the agent writes everything; the USER clicks Generate. Always 10.
  per_generation  every generation needs a yes: 10 unless --approved-now.
  per_shot        (default) one shot at a time; the next shot starts only after
                  the user approves the previous one. 1 automatic retake after a
                  failed take (stops at 2 failures in a row).
  autopilot       plan + budget approved up front (a budget is REQUIRED). Runs
                  unattended; stops at the budget, at 3 failures in a row on one
                  shot (2 automatic retakes), when the live price differs from
                  the plan, or when a shot it depends on is not approved.

GATES — the production order, enforced (a client project is right the first
time because nothing expensive happens before the cheap decisions are signed):
  script      the script interpretation (breakdown + answers) is signed off
  cast        EVERY character is built (sheet + Flow Character, + voice if
              they speak) and approved — before any scene or shot exists
  storyboard  keyframes/animatic approved (the user may waive it for a quick job)
  rough_cut   all shots approved and assembled; the cut is signed off
  final       final QC passed and delivered
  Only the user can approve or waive a gate. `script` and `cast` cannot be
  waived. A project with no characters passes `cast` automatically.

  gate script approve --by user --note "client: 'confirmed, go ahead' (email 12 Oct)"
  cast-set HANA --sheet chars/hana_sheet.png --expressions chars/hana_expr.png \
      --consistency chars/hana_test1.png --flow-character Hana --voice HANA_VOICE \
      [--voice-test takes/hana_voice_test.mp4]
  cast-approve HANA --by user --note "client approved look + voice"
  gate cast approve --by user --note "..." (refused until every character is approved)
  cast-remove X --by user --note "not a character (parsing error)"
  sync-plan plan.json                      (after editing the plan: adds/updates shots and
                                            characters; new characters reopen gate cast)
  --by is always required and approvals carry a --note quoting the user/client.
  Every file given to cast-set must exist. Reopening a gate reopens every later gate.
  gate storyboard approve|waive --by user
  can-build-asset character|keyframe       (images: sheets need `script`, keyframes need `cast`)

TAKE LIFECYCLE (every credit is counted, including failed generations)
  1. right after clicking Generate:  start-take S02 --credits 12
         -> take recorded as PENDING, its credits count against the budget
  2. after QC (script + looking):   log-take S02 --verdict PASS|CHECK|FAIL --file ...
         -> updates the pending take
     if the generation errored / was blocked / timed out:
                                     log-take S02 --verdict ERROR --credits <charged>
  3. approve / reject

  Verdict mapping from qc.md: ACCEPT -> PASS, FIX IN POST -> CHECK,
  REGENERATE or CHANGE ROUTE -> FAIL. The verdict logged is the COMBINED one:
  a clip that passes qc_clip.py but fails the visual checklist is FAIL.
  An x2-x4 generation is ONE take (credits = total charged); record the
  chosen output as --file and the others in --note.

USAGE
  project_state.py init plan.json --mode per_shot --budget 150 [--state state.json]
  project_state.py can-generate S02 --credits 12 [--approved-now]
  project_state.py start-take S02 --credits 12
  project_state.py log-take S02 --verdict PASS --file takes/S02_t1.mp4 [--credits N] [--note "..."]
  project_state.py approve S02 [--take 1] --by user|agent
  project_state.py reject S02 [--take 1] --reason "wardrobe drift"
  project_state.py set-mode autopilot | set-budget 200
  project_state.py show | next
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MODES = ["guided", "per_generation", "per_shot", "autopilot"]
# Automatic retakes allowed after the first failure.
AUTO_RETAKES = {"per_shot": 1, "autopilot": 2}
FAILED = ("FAIL", "ERROR", "REJECTED")
GO, ASK, STOP = 0, 10, 11
GATES = ["script", "cast", "storyboard", "rough_cut", "final"]
WAIVABLE = {"storyboard"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: str) -> dict:
    if not os.path.exists(path):
        raise SystemExit(f"no state at {path} — run `init` first")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(state: dict, path: str) -> None:
    state["updated"] = now()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def spent(state: dict) -> float:
    return sum(t.get("credits", 0) or 0 for s in state["shots"] for t in s["takes"])


def shot(state: dict, sid: str) -> dict:
    for s in state["shots"]:
        if s["id"] == sid:
            return s
    raise SystemExit(f"unknown shot {sid}")


def trailing_fails(s: dict) -> int:
    n = 0
    for t in reversed(s["takes"]):
        if t.get("verdict") in FAILED:
            n += 1
        else:
            break
    return n


def planned_costs(plan: dict) -> dict:
    """Price each shot from the platform capabilities, so a live price that
    differs from the plan can be caught."""
    try:
        import shot_plan
        caps_path = shot_plan.DEFAULT_CAPS
        caps = shot_plan.load_caps(caps_path)
        rows = shot_plan.validate(plan, caps)["rows"]
        return {r["id"]: r.get("cost") for r in rows}
    except Exception:
        return {}


CAST_FILES = ("sheet", "expressions", "consistency", "voice_test")


def new_character(name: str, speaks: bool) -> dict:
    return {"name": name, "speaks": speaks, "status": "planned", "sheet": None, "expressions": None,
            "consistency": None, "flow_character": None, "voice": None, "voice_test": None,
            "approved_by": None}


def missing_parts(c: dict) -> list[str]:
    need = ["sheet", "consistency", "flow_character"]
    if c.get("speaks"):
        need += ["expressions", "voice"]
    return [k for k in need if not c.get(k)]


def production_blockers(state: dict, sid: str) -> str | None:
    """The single check every production command runs (can-generate,
    start-take, log-take, approve). None = allowed."""
    for g in ("script", "cast", "storyboard"):
        if not gate_ok(state, g):
            what = {"script": "the script interpretation has not been signed off",
                    "cast": "the cast is not locked — build and approve every character first",
                    "storyboard": "the storyboard/animatic has not been approved (or waived by the user)"}[g]
            return f"gate '{g}' is closed: {what}. No shot may be produced yet."
    try:
        s = shot(state, sid)
    except SystemExit:
        return f"unknown shot {sid} — run sync-plan after editing plan.json"
    if s.get("status") == "removed":
        return f"{sid} was removed from the plan"
    unknown = [c for c in s.get("cast", []) if c not in state.get("cast", {})]
    if unknown:
        return f"{sid} uses characters that are not in the cast registry: {unknown} — build them first"
    unready = [c for c in s.get("cast", []) if state["cast"][c]["status"] != "approved"]
    if unready:
        return f"{sid} needs characters that are not approved yet: {unready}"
    return None


def resolve_cast(cast: dict, ref: str) -> str:
    """Accept a character id or name; return the id (or the ref if unknown)."""
    if ref in cast:
        return ref
    for cid, c in cast.items():
        if c["name"].strip().lower() == str(ref).strip().lower():
            return cid
    return ref


def gate_ok(state: dict, g: str) -> bool:
    return state.get("gates", {}).get(g, {}).get("status") in ("approved", "waived")


def dependency(plan_shots: list, i: int) -> str | None:
    s = plan_shots[i]
    if s.get("extends"):
        return s["extends"]
    if s.get("continuation") in ("keyframe_chain", "extend") and i > 0:
        return plan_shots[i - 1].get("id")
    return None


def cmd_init(a) -> int:
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    if os.path.exists(a.state) and not a.force:
        raise SystemExit(f"{a.state} exists — use --force to overwrite (this loses its history)")
    budget = a.budget if a.budget is not None else plan.get("budget_credits")
    if a.mode == "autopilot" and budget is None:
        raise SystemExit("autopilot needs a credit budget (--budget N)")
    costs = planned_costs(plan)
    pshots = plan.get("shots", [])
    cast = {}
    for c in plan.get("characters") or []:
        cast[c["id"]] = new_character(c.get("name", c["id"]), bool(c.get("speaks", True)))
    # Asset fields in plan.json are ignored on purpose: a character counts as
    # built only through cast-set, with files that exist.
    gates = {g: {"status": "pending"} for g in GATES}
    state = {
        "project": plan.get("project"), "platform": plan.get("platform"),
        "plan_file": os.path.abspath(a.plan), "mode": a.mode, "budget": budget,
        "created": now(), "decisions": [], "open_questions": [], "gates": gates, "cast": cast,
        "shots": [{"id": s["id"], "beat": s.get("beat", ""), "model": s.get("model"),
                   "mode": s.get("mode"), "planned_credits": costs.get(s["id"]),
                   "cast": [resolve_cast(cast, x) for x in (s.get("cast") or [])],
                   "depends_on": dependency(pshots, i),
                   "status": "planned", "takes": [], "approved_take": None}
                  for i, s in enumerate(pshots)],
    }
    save(state, a.state)
    print(f"state -> {a.state}  ({len(state['shots'])} shots, mode={a.mode}, budget={budget})")
    return 0


def decide(state: dict, sid: str, credits: float, approved_now: bool) -> tuple[int, str]:
    block = production_blockers(state, sid)
    if block:
        return STOP, block
    s = shot(state, sid)
    mode = state["mode"]
    budget = state.get("budget")
    used = spent(state)

    block = production_blockers(state, sid)
    if block:
        return STOP, block
    if any(t.get("verdict") == "PENDING" for t in s["takes"]):
        return STOP, (f"{sid} has a generation in flight or not yet QC'd — finish QC and "
                      f"log-take before generating again (a second click is a second charge)")
    if s["status"] == "approved":
        return STOP, f"{sid} is already approved — generating again would waste credits"
    if budget is not None and used + credits > budget:
        return STOP, (f"budget: {used:g} spent + {credits:g} > {budget:g}. "
                      f"Ask the user to raise the budget or cut scope.")
    planned = s.get("planned_credits")
    price_changed = planned is not None and abs(credits - planned) > 0.01

    if mode == "guided":
        return ASK, "guided mode: hand the prompt and settings to the user; they click Generate"
    if mode == "per_generation":
        if approved_now:
            return GO, "user approved this generation"
        extra = f" (plan said {planned:g})" if price_changed else ""
        return ASK, (f"per_generation mode: show prompt + settings + {credits:g} credits{extra} "
                     f"and wait for a yes")

    if price_changed:
        return (STOP if mode == "autopilot" else ASK), (
            f"live price {credits:g} differs from the plan ({planned:g}) — tell the user, "
            f"update the plan, and get a yes before generating")

    dep = s.get("depends_on")
    if dep:
        d = shot(state, dep)
        if d["status"] != "approved":
            return (STOP if mode == "autopilot" else ASK), (
                f"{sid} continues from {dep}, which is not approved yet")

    fails = trailing_fails(s)
    limit = AUTO_RETAKES[mode]
    if fails > limit:
        return STOP, (f"{sid} failed {fails} takes in a row — stop, report what failed and why, "
                      f"and propose a different route (model/method/split) instead of retrying")
    if s["takes"] and s["status"] == "review":
        return ASK, (f"{sid} has a take waiting for review — approve it or reject it first "
                     f"(autopilot: the agent may approve a PASS take itself)")

    if mode == "per_shot":
        idx = [x["id"] for x in state["shots"]].index(sid)
        pending = [x["id"] for x in state["shots"][:idx] if x["status"] != "approved"]
        if pending:
            return ASK, f"per_shot mode: the user has not approved {pending} yet — show the result and wait"
        if fails >= 1:
            return GO, "automatic retake allowed (use the corrected prompt)"
        return GO, "per_shot: previous shots approved"

    note = ""
    if budget and used + credits > 0.75 * budget:
        note = f" (warning: {used + credits:g}/{budget:g} credits used after this — over 75%)"
    return GO, "autopilot within budget" + note


def cmd_can(a) -> int:
    state = load(a.state)
    try:
        code, why = decide(state, a.shot, a.credits, a.approved_now)
    except SystemExit as e:
        code, why = STOP, str(e)
    print(f"{ {GO: 'GO', ASK: 'ASK USER', STOP: 'STOP'}[code] }: {why}")
    return code


def guard(state: dict, sid: str) -> None:
    block = production_blockers(state, sid)
    if block:
        print(f"STOP: {block}")
        raise SystemExit(STOP)


def cmd_start(a) -> int:
    state = load(a.state)
    guard(state, a.shot)
    s = shot(state, a.shot)
    s["takes"].append({"n": len(s["takes"]) + 1, "file": None, "credits": a.credits,
                       "verdict": "PENDING", "note": "", "at": now()})
    s["status"] = "generating"
    s["approved_take"] = None
    save(state, a.state)
    print(f"{a.shot} take {len(s['takes'])} started ({a.credits:g} cr) — spent {spent(state):g}"
          + (f"/{state['budget']:g}" if state.get("budget") else ""))
    return 0


def cmd_log(a) -> int:
    state = load(a.state)
    guard(state, a.shot)
    s = shot(state, a.shot)
    pend = [t for t in s["takes"] if t.get("verdict") == "PENDING"]
    if pend:
        t = pend[-1]
    else:
        if a.credits is None:
            raise SystemExit("no pending take — pass --credits (or use start-take right after Generate)")
        t = {"n": len(s["takes"]) + 1, "credits": a.credits, "at": now()}
        s["takes"].append(t)
    if a.credits is not None:
        t["credits"] = a.credits
    t.update({"file": a.file or t.get("file"), "verdict": a.verdict,
              "note": a.note, "qc_at": now()})
    s["status"] = "retake" if a.verdict in FAILED else "review"
    s["approved_take"] = None
    save(state, a.state)
    print(f"{a.shot} take {t['n']}: {a.verdict}  spent so far {spent(state):g}"
          + (f"/{state['budget']:g}" if state.get("budget") else ""))
    return 0


def pick_take(s: dict, n: int | None) -> tuple[int, dict]:
    if not s["takes"]:
        raise SystemExit("no takes")
    n = n or len(s["takes"])
    if not 1 <= n <= len(s["takes"]):
        raise SystemExit(f"take {n} does not exist ({len(s['takes'])} takes)")
    return n, s["takes"][n - 1]


def cmd_approve(a) -> int:
    state = load(a.state)
    guard(state, a.shot)
    s = shot(state, a.shot)
    n, t = pick_take(s, a.take)
    v = t.get("verdict")
    if v in ("PENDING",):
        raise SystemExit(f"take {n} has not been QC'd yet")
    if v in FAILED and not a.force:
        raise SystemExit(f"take {n} is {v} — approve anyway only with --force and a reason")
    if a.by == "agent":
        if state["mode"] != "autopilot":
            raise SystemExit(f"mode {state['mode']}: only the user can approve (--by user)")
        if v != "PASS":
            raise SystemExit(f"the agent may only approve a PASS take (this one is {v}); ask the user")
    s["approved_take"], s["status"] = n, "approved"
    t["approved_by"] = a.by
    t["approval_note"] = a.note
    save(state, a.state)
    print(f"{a.shot}: take {n} approved by {a.by}")
    return 0


def cmd_reject(a) -> int:
    state = load(a.state)
    s = shot(state, a.shot)
    n, t = pick_take(s, a.take)
    t["verdict"] = "REJECTED"
    t["note"] = (t.get("note") or "") + f" | rejected: {a.reason}"
    s["status"], s["approved_take"] = "retake", None
    save(state, a.state)
    print(f"{a.shot}: take {n} rejected ({a.reason})")
    return 0


def cmd_mode(a) -> int:
    state = load(a.state)
    if a.mode == "autopilot" and state.get("budget") is None:
        raise SystemExit("autopilot needs a budget first: set-budget N")
    state["decisions"].append({"at": now(), "decision": f"mode {state['mode']} -> {a.mode}"})
    state["mode"] = a.mode
    save(state, a.state)
    print(f"mode -> {a.mode}")
    return 0


def cmd_budget(a) -> int:
    state = load(a.state)
    state["decisions"].append({"at": now(), "decision": f"budget {state.get('budget')} -> {a.budget}"})
    state["budget"] = a.budget
    save(state, a.state)
    print(f"budget -> {a.budget:g} (spent {spent(state):g})")
    return 0


def cmd_cast_set(a) -> int:
    state = load(a.state)
    cast = state.setdefault("cast", {})
    cid = resolve_cast(cast, a.id)
    if cid not in cast:
        if not a.name:
            raise SystemExit(f"unknown character {a.id} — add it with --name to register a new one")
        cast[cid] = new_character(a.name, not a.silent)
        reopen_from(state, "cast", f"new character {cid}")
    c = cast[cid]
    base = os.path.dirname(os.path.abspath(a.state))
    changed = False
    for k in ("sheet", "expressions", "consistency", "flow_character", "voice", "voice_test"):
        v = getattr(a, k)
        if not v:
            continue
        if k in CAST_FILES:
            path = v if os.path.isabs(v) else os.path.join(base, v)
            if not os.path.exists(path):
                raise SystemExit(f"{k} file not found: {v} — make the image/clip first, then register it")
        c[k] = v
        changed = True
    if changed and c["status"] == "approved":
        c["status"], c["approved_by"] = "built", None   # a changed character must be re-approved
        reopen_from(state, "cast", f"{cid} changed after approval")
    missing = missing_parts(c)
    if not missing and c["status"] == "planned":
        c["status"] = "built"
    save(state, a.state)
    print(f"{cid} ({c['name']}): {c['status']}" + (f" — still missing {missing}" if missing else ""))
    return 0


def cmd_cast_remove(a) -> int:
    state = load(a.state)
    cid = resolve_cast(state.get("cast", {}), a.id)
    if cid not in state.get("cast", {}):
        raise SystemExit(f"unknown character {a.id}")
    used = [x["id"] for x in state["shots"] if cid in x.get("cast", []) and x["status"] != "removed"]
    if used:
        raise SystemExit(f"{cid} is still used by shots {used} — change the plan and sync-plan first")
    state["cast"].pop(cid)
    state["decisions"].append({"at": now(), "decision": f"removed character {cid}", "by": a.by, "note": a.note})
    save(state, a.state)
    print(f"{cid} removed")
    return 0


def cmd_sync(a) -> int:
    state = load(a.state)
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    cast = state.setdefault("cast", {})
    added_chars = []
    for c in plan.get("characters") or []:
        if c["id"] not in cast:
            cast[c["id"]] = new_character(c.get("name", c["id"]), bool(c.get("speaks", True)))
            added_chars.append(c["id"])
    if added_chars:
        reopen_from(state, "cast", f"new characters {added_chars}")
    costs = planned_costs(plan)
    pshots = plan.get("shots", [])
    by_id = {x["id"]: x for x in state["shots"]}
    new_list, added, updated = [], [], []
    for i, p in enumerate(pshots):
        fields = {"beat": p.get("beat", ""), "model": p.get("model"), "mode": p.get("mode"),
                  "planned_credits": costs.get(p["id"]),
                  "cast": [resolve_cast(cast, x) for x in (p.get("cast") or [])],
                  "depends_on": dependency(pshots, i)}
        if p["id"] in by_id:
            old = by_id.pop(p["id"])
            if any(old.get(k) != v for k, v in fields.items()):
                updated.append(p["id"])
                if old["status"] == "approved" and (old.get("model"), old.get("mode"), old.get("cast")) != \
                        (fields["model"], fields["mode"], fields["cast"]):
                    old["status"], old["approved_take"] = "retake", None   # the shot itself changed
            old.update(fields)
            new_list.append(old)
        else:
            new_list.append({"id": p["id"], **fields, "status": "planned", "takes": [], "approved_take": None})
            added.append(p["id"])
    for gone in by_id.values():     # keep history, never delete takes
        gone["status"] = "removed"
        new_list.append(gone)
    state["shots"] = new_list
    state["plan_file"] = os.path.abspath(a.plan)
    save(state, a.state)
    print(f"synced: +{len(added)} shots {added}, updated {updated}, removed {[g['id'] for g in by_id.values()]}"
          + (f", new characters {added_chars} (gate cast reopened)" if added_chars else ""))
    return 0


def reopen_from(state: dict, gate: str, why: str) -> None:
    """Reopen a gate and every gate after it."""
    gates = state.setdefault("gates", {g: {"status": "pending"} for g in GATES})
    for g in GATES[GATES.index(gate):]:
        if gates.get(g, {}).get("status") != "pending":
            gates[g] = {"status": "pending", "note": f"reopened: {why}", "at": now()}


def cmd_cast_approve(a) -> int:
    state = load(a.state)
    cid = resolve_cast(state.get("cast", {}), a.id)
    c = state.get("cast", {}).get(cid)
    if not c:
        raise SystemExit(f"unknown character {a.id}")
    if a.by != "user":
        raise SystemExit("characters are approved by the user (or client) only")
    missing = missing_parts(c)
    if missing:
        raise SystemExit(f"{cid} is not built yet — missing {missing}")
    c["status"], c["approved_by"] = "approved", a.by
    c["approval_note"] = a.note
    c["approved_at"] = now()
    save(state, a.state)
    left = [k for k, v in state["cast"].items() if v["status"] != "approved"]
    print(f"{cid} ({c['name']}) approved." + (f" Still to approve: {left}" if left else
                                              " All characters approved — you can now close gate 'cast'."))
    return 0


def cmd_gate(a) -> int:
    state = load(a.state)
    gates = state.setdefault("gates", {g: {"status": "pending"} for g in GATES})
    g = a.gate
    if a.by != "user":
        raise SystemExit("gates are approved or waived by the user only")
    order = GATES[:GATES.index(g)]
    closed = [x for x in order if not gate_ok(state, x)]
    if closed and a.action == "approve":
        raise SystemExit(f"cannot approve '{g}' before {closed}")
    if a.action == "waive":
        if g not in WAIVABLE:
            raise SystemExit(f"gate '{g}' cannot be waived")
        gates[g] = {"status": "waived", "by": a.by, "note": a.note, "at": now()}
    elif a.action == "reopen":
        reopen_from(state, g, a.note or "reopened by user")
    else:
        if g == "cast":
            left = [k for k, v in state.get("cast", {}).items() if v["status"] != "approved"]
            if left:
                raise SystemExit(f"cannot lock the cast: not approved yet {left}")
        if g in ("rough_cut", "final"):
            left = [x["id"] for x in state["shots"] if x["status"] != "approved"]
            if left:
                raise SystemExit(f"cannot approve '{g}': shots not approved {left}")
        gates[g] = {"status": "approved", "by": a.by, "note": a.note, "at": now()}
    state["decisions"].append({"at": now(), "decision": f"gate {g} -> {gates[g]['status']}"
                               + (f" ({a.note})" if a.note else "")})
    save(state, a.state)
    print(f"gate {g}: {gates[g]['status']}")
    return 0


def cmd_can_asset(a) -> int:
    state = load(a.state)
    need = "script" if a.kind == "character" else "cast"
    if not gate_ok(state, need):
        print(f"STOP: {a.kind} images need gate '{need}' first"
              + (" — lock every character before drawing any scene keyframe" if need == "cast" else ""))
        return STOP
    b = state.get("budget")
    if a.credits and b is not None and spent(state) + a.credits > b:
        print("STOP: over budget")
        return STOP
    if state["mode"] == "guided":
        print("ASK USER: guided mode — hand over the image prompt")
        return ASK
    print("GO")
    return GO


def cmd_show(a) -> int:
    state = load(a.state)
    b = state.get("budget")
    print(f"{state['project']}  mode={state['mode']}  spent={spent(state):g}" + (f"/{b:g}" if b else ""))
    gates = state.get("gates", {})
    print("  gates: " + "  ".join(f"{g}={gates.get(g, {}).get('status', '?')}" for g in GATES))
    for cid, c in state.get("cast", {}).items():
        print(f"  cast {cid:10} {c['name']:12} {c['status']:9} sheet={'✓' if c.get('sheet') else '·'} "
              f"flow={'✓' if c.get('flow_character') else '·'} voice={'✓' if c.get('voice') else ('-' if not c['speaks'] else '·')}")
    for s in state["shots"]:
        takes = " ".join(f"t{t['n']}:{t['verdict']}" for t in s["takes"]) or "-"
        dep = f" <-{s['depends_on']}" if s.get("depends_on") else ""
        print(f"  {s['id']:5} {s['status']:10} {str(s['model']):16} plan={s.get('planned_credits')}{dep}  {takes}")
    return 0


def cmd_next(a) -> int:
    state = load(a.state)
    for g in ("script", "cast", "storyboard"):
        if not gate_ok(state, g):
            left = [k for k, v in state.get("cast", {}).items() if v["status"] != "approved"]
            print(f"GATE {g}" + (f" — characters to build/approve: {left}" if g == "cast" and left else ""))
            return 0
    for s in state["shots"]:
        if s["status"] != "approved":
            print(s["id"])
            return 0
    for g in ("rough_cut", "final"):
        if not gate_ok(state, g):
            print(f"GATE {g}")
            return 0
    print("DELIVERED")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Project state + autonomy enforcement.")
    ap.add_argument("--state", default="state.json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("plan")
    p.add_argument("--mode", choices=MODES, default="per_shot")
    p.add_argument("--budget", type=float); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("can-generate"); p.add_argument("shot")
    p.add_argument("--credits", type=float, required=True)
    p.add_argument("--approved-now", action="store_true")
    p.set_defaults(fn=cmd_can)

    p = sub.add_parser("start-take"); p.add_argument("shot")
    p.add_argument("--credits", type=float, required=True)
    p.set_defaults(fn=cmd_start)

    p = sub.add_parser("log-take"); p.add_argument("shot")
    p.add_argument("--verdict", choices=["PASS", "CHECK", "FAIL", "ERROR"], required=True)
    p.add_argument("--file"); p.add_argument("--credits", type=float)
    p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("approve"); p.add_argument("shot"); p.add_argument("--take", type=int)
    p.add_argument("--by", choices=["user", "agent"], required=True)
    p.add_argument("--note", default="")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_approve)

    p = sub.add_parser("reject"); p.add_argument("shot"); p.add_argument("--take", type=int)
    p.add_argument("--reason", required=True)
    p.set_defaults(fn=cmd_reject)

    p = sub.add_parser("cast-set"); p.add_argument("id")
    p.add_argument("--name"); p.add_argument("--silent", action="store_true")
    p.add_argument("--sheet"); p.add_argument("--expressions"); p.add_argument("--consistency")
    p.add_argument("--flow-character"); p.add_argument("--voice"); p.add_argument("--voice-test")
    p.set_defaults(fn=cmd_cast_set)
    p = sub.add_parser("cast-approve"); p.add_argument("id")
    p.add_argument("--by", choices=["user", "agent"], required=True); p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_cast_approve)
    p = sub.add_parser("cast-remove"); p.add_argument("id")
    p.add_argument("--by", choices=["user"], required=True); p.add_argument("--note", required=True)
    p.set_defaults(fn=cmd_cast_remove)
    p = sub.add_parser("sync-plan"); p.add_argument("plan"); p.set_defaults(fn=cmd_sync)
    p = sub.add_parser("gate"); p.add_argument("gate", choices=GATES)
    p.add_argument("action", choices=["approve", "waive", "reopen"])
    p.add_argument("--by", choices=["user", "agent"], required=True); p.add_argument("--note", default="")
    p.set_defaults(fn=cmd_gate)
    p = sub.add_parser("can-build-asset"); p.add_argument("kind", choices=["character", "keyframe"])
    p.add_argument("--credits", type=float, default=0); p.set_defaults(fn=cmd_can_asset)

    p = sub.add_parser("set-mode"); p.add_argument("mode", choices=MODES); p.set_defaults(fn=cmd_mode)
    p = sub.add_parser("set-budget"); p.add_argument("budget", type=float); p.set_defaults(fn=cmd_budget)
    p = sub.add_parser("show"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("next"); p.set_defaults(fn=cmd_next)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
