#!/usr/bin/env python3
"""
analyze_reports.py — summarize accumulated usage reports for one skill
(or all skills), so the agent has real patterns to work from instead of
re-reading every raw report line.

Usage:
  python3 analyze_reports.py <skill-name>          # one skill
  python3 analyze_reports.py --all                 # every skill with reports
  python3 analyze_reports.py <skill-name> --archive # summarize, then move
                                                     # the consumed log out of
                                                     # the way so it isn't
                                                     # re-analyzed next time

Prints a Markdown summary to stdout: outcome counts, the most frequent
issues and missing-coverage items (exact-string frequency — deliberately
simple/deterministic, the agent applies judgment on top of these counts,
not the other way around), and the most recent few raw notes for context.
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path


def load_reports(path: Path):
    entries = []
    if not path.exists():
        return entries
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"warning: {path}:{line_no}: skipping malformed line ({e})", file=sys.stderr)
    return entries


def summarize(skill: str, entries: list) -> str:
    if not entries:
        return (
            f"## {skill}\n\nNo usage reports yet. This isn't a failure — it means "
            f"either the skill hasn't been used since reporting was added, or "
            f"nothing was logged. Fall back to a direct read-through audit "
            f"instead of report-driven analysis (see "
            f"`skills/skill-enhancer/references/enhancement_checklist.md`).\n"
        )

    outcomes = Counter(e.get("outcome", "unknown") for e in entries)
    issues = Counter(i for e in entries for i in e.get("issues", []) if i)
    missing = Counter(m for e in entries for m in e.get("missing_coverage", []) if m)
    tools = Counter(e.get("tool", "unknown") for e in entries)

    lines = [f"## {skill}", ""]
    lines.append(f"**{len(entries)} report(s)** — " + ", ".join(f"{k}: {v}" for k, v in outcomes.most_common()))
    lines.append(f"By tool: " + ", ".join(f"{k}: {v}" for k, v in tools.most_common()))
    lines.append("")

    if issues:
        lines.append("**Recurring issues** (exact-text frequency — group similar wording yourself):")
        for text, count in issues.most_common(10):
            lines.append(f"- ({count}x) {text}")
        lines.append("")

    if missing:
        lines.append("**Recurring missing-coverage reports:**")
        for text, count in missing.most_common(10):
            lines.append(f"- ({count}x) {text}")
        lines.append("")

    failures = [e for e in entries if e.get("outcome") == "failure"]
    if failures:
        lines.append("**Most recent failures (up to 5):**")
        for e in sorted(failures, key=lambda x: x.get("timestamp", ""))[-5:]:
            note = e.get("note") or "(no note)"
            task = e.get("task_summary") or "(no task summary)"
            lines.append(f"- [{e.get('timestamp', '?')}] task=\"{task}\" note=\"{note}\"")
        lines.append("")

    notes = [e.get("note") for e in entries if e.get("note")]
    if notes:
        lines.append("**Recent notes (up to 5, most recent last):**")
        for n in notes[-5:]:
            lines.append(f"- {n}")
        lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Summarize skill usage reports.")
    p.add_argument("skill", nargs="?", help="skill name; omit with --all")
    p.add_argument("--all", action="store_true", help="summarize every skill with reports")
    p.add_argument("--archive", action="store_true", help="move consumed log(s) aside after summarizing")
    p.add_argument(
        "--reports-dir",
        default=str(Path.home() / ".cache" / "ai-skills" / "reports"),
    )
    args = p.parse_args()

    if not args.skill and not args.all:
        p.error("give a skill name, or pass --all")

    reports_dir = Path(args.reports_dir)

    if args.all:
        skill_files = sorted(reports_dir.glob("*.jsonl")) if reports_dir.is_dir() else []
        if not skill_files:
            print("No reports directory / no reports logged yet for any skill.")
            return
        skills = [f.stem for f in skill_files]
    else:
        skills = [args.skill]

    outputs = []
    for skill in skills:
        path = reports_dir / f"{skill}.jsonl"
        entries = load_reports(path)
        outputs.append(summarize(skill, entries))
        if args.archive and entries:
            stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
            archived = reports_dir / f"{skill}.{stamp}.jsonl.processed"
            path.rename(archived)
            print(f"(archived consumed log -> {archived})", file=sys.stderr)

    print("\n".join(outputs))


if __name__ == "__main__":
    main()
