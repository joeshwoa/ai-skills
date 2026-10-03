#!/usr/bin/env python3
"""Rank reel ideas with the team's rubric and print a Markdown board to show the user.

    python3 scripts/score_ideas.py ideas.json [--top 5] [--md out.md]

ideas.json = {"brief": "...", "ideas": [{"title": "...", "angle": "...", "hook": "...",
   "format": "talking_head", "trend": "optional, dated", "scores": {"hook": 0-5, "audience_fit": 0-5,
   "trend_timing": 0-5, "shareability": 0-5, "feasibility": 0-5, "brand_fit": 0-5, "originality": 0-5},
   "why": "one line"}]}

Scores are the team's honest judgement (references/ideation.md defines each 0–5 scale);
this script only makes the weighting consistent and flags ideas that fail a hard floor.
"""
from __future__ import annotations

import argparse
import json
import sys

WEIGHTS = {"hook": 0.25, "audience_fit": 0.20, "shareability": 0.15, "trend_timing": 0.10,
           "feasibility": 0.12, "brand_fit": 0.12, "originality": 0.06}
FLOORS = {"audience_fit": 3, "brand_fit": 2, "feasibility": 2}


def score(idea: dict) -> tuple[float, list[str]]:
    s = idea.get("scores") or {}
    missing = [k for k in WEIGHTS if k not in s]
    if missing:
        raise ValueError(f"idea '{idea.get('title')}' missing scores: {', '.join(missing)}")
    for k, v in s.items():
        if not isinstance(v, (int, float)) or not 0 <= v <= 5:
            raise ValueError(f"idea '{idea.get('title')}': score {k}={v!r} must be 0–5")
    total = sum(s[k] * w for k, w in WEIGHTS.items()) / 5 * 100
    fails = [f"{k}<{f}" for k, f in FLOORS.items() if s[k] < f]
    return round(total, 1), fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ideas")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--md")
    a = ap.parse_args(argv)
    data = json.load(open(a.ideas, encoding="utf-8"))
    rows = []
    try:
        for idea in data.get("ideas") or []:
            total, fails = score(idea)
            rows.append((total, fails, idea))
    except ValueError as e:
        print("error:", e, file=sys.stderr)
        return 2
    rows.sort(key=lambda r: (not r[1], r[0]), reverse=True)
    if a.top:
        rows = rows[: a.top]
    lines = [f"# Idea board — {data.get('brief', '')}".rstrip(" —"), "",
             "| # | Score | Idea | Hook | Format | Why | Flags |", "|---|---|---|---|---|---|---|"]
    for i, (total, fails, idea) in enumerate(rows, 1):
        cell = lambda x: str(x or "").replace("|", "/").replace("\n", " ")  # noqa: E731
        lines.append(f"| {i} | {total} | {cell(idea.get('title'))} | {cell(idea.get('hook'))} | "
                     f"{cell(idea.get('format'))} | {cell(idea.get('why'))} | {', '.join(fails) or '—'} |")
    lines += ["", "Weights: " + ", ".join(f"{k} {int(w * 100)}%" for k, w in WEIGHTS.items()),
              "Ideas under a floor (" + ", ".join(f"{k} ≥ {v}" for k, v in FLOORS.items()) + ") sink to the bottom."]
    md = "\n".join(lines) + "\n"
    if a.md:
        open(a.md, "w", encoding="utf-8").write(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
