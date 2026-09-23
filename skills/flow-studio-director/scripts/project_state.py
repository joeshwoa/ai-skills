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
    state = {
        "project": plan.get("project"), "platform": plan.get("platform"),
        "plan_file": os.path.abspath(a.plan), "mode": a.mode, "budget": budget,
        "created": now(), "decisions": [], "open_questions": [],
        "shots": [{"id": s["id"], "beat": s.get("beat", ""), "model": s.get("model"),
                   "mode": s.get("mode"), "planned_credits": costs.get(s["id"]),
                   "depends_on": dependency(pshots, i),
                   "status": "planned", "takes": [], "approved_take": None}
                  for i, s in enumerate(pshots)],
    }
    save(state, a.state)
    print(f"state -> {a.state}  ({len(state['shots'])} shots, mode={a.mode}, budget={budget})")
    return 0


def decide(state: dict, sid: str, credits: float, approved_now: bool) -> tuple[int, str]:
    s = shot(state, sid)
    mode = state["mode"]
    budget = state.get("budget")
    used = spent(state)

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
    code, why = decide(state, a.shot, a.credits, a.approved_now)
    print(f"{ {GO: 'GO', ASK: 'ASK USER', STOP: 'STOP'}[code] }: {why}")
    return code


def cmd_start(a) -> int:
    state = load(a.state)
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


def cmd_show(a) -> int:
    state = load(a.state)
    b = state.get("budget")
    print(f"{state['project']}  mode={state['mode']}  spent={spent(state):g}" + (f"/{b:g}" if b else ""))
    for s in state["shots"]:
        takes = " ".join(f"t{t['n']}:{t['verdict']}" for t in s["takes"]) or "-"
        dep = f" <-{s['depends_on']}" if s.get("depends_on") else ""
        print(f"  {s['id']:5} {s['status']:10} {str(s['model']):16} plan={s.get('planned_credits')}{dep}  {takes}")
    return 0


def cmd_next(a) -> int:
    state = load(a.state)
    for s in state["shots"]:
        if s["status"] != "approved":
            print(s["id"])
            return 0
    print("ALL APPROVED — move to assembly")
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
    p.add_argument("--by", choices=["user", "agent"], default="user")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_approve)

    p = sub.add_parser("reject"); p.add_argument("shot"); p.add_argument("--take", type=int)
    p.add_argument("--reason", required=True)
    p.set_defaults(fn=cmd_reject)

    p = sub.add_parser("set-mode"); p.add_argument("mode", choices=MODES); p.set_defaults(fn=cmd_mode)
    p = sub.add_parser("set-budget"); p.add_argument("budget", type=float); p.set_defaults(fn=cmd_budget)
    p = sub.add_parser("show"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("next"); p.set_defaults(fn=cmd_next)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
