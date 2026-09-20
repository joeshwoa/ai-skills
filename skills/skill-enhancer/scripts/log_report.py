#!/usr/bin/env python3
"""
log_report.py — append one structured usage report for a skill.

Called by the agent as the LAST step after using any skill from this repo
(skill-router's SKILL.md is what actually instructs this — see there).
Deliberately dependency-free and append-only (no read-modify-write races
across multiple AI tools writing on the same machine).

Reports are NOT committed to the repo — they live in a local cache dir
(same convention as the MCP bootstrap caches: ~/.cache/ai-skills/) so
logging never needs git/network access and never bloats the repo's
history with one commit per skill use. Multiple tools (Claude, Cursor,
Antigravity, ...) on the same machine share this one location, which is
what makes cross-tool aggregation work without any sync step.

Usage:
  python3 log_report.py <skill-name> <outcome> [options]

  <outcome> is one of: success, partial, failure

Options:
  --tool NAME              which AI tool logged this (default: unknown)
  --task "one line"        one-line task summary — NO sensitive/personal
                            content, just enough to identify the pattern
  --issue "text"           a specific problem hit (repeatable)
  --missing "text"         something the task needed that the skill
                            didn't cover (repeatable)
  --note "text"            free-text suggestion or effort note
  --reports-dir PATH       override the reports directory (default:
                            ~/.cache/ai-skills/reports)

Example:
  python3 log_report.py premium-presentations success \\
    --tool claude --task "10-slide investor deck" \\
    --note "worked first try, no issues"

  python3 log_report.py omnicinema failure \\
    --tool cursor --task "generate a logo" \\
    --issue "bootstrap.sh failed: upstream build bug" \\
    --missing "no offline fallback message shown to the user before the error"
"""
import argparse
import json
import sys
import time
from pathlib import Path

VALID_OUTCOMES = ("success", "partial", "failure")


def main():
    p = argparse.ArgumentParser(description="Append a skill usage report.")
    p.add_argument("skill", help="skill name, e.g. premium-presentations")
    p.add_argument("outcome", choices=VALID_OUTCOMES)
    p.add_argument("--tool", default="unknown")
    p.add_argument("--task", default="")
    p.add_argument("--issue", action="append", default=[], dest="issues")
    p.add_argument("--missing", action="append", default=[], dest="missing_coverage")
    p.add_argument("--note", default="")
    p.add_argument(
        "--reports-dir",
        default=str(Path.home() / ".cache" / "ai-skills" / "reports"),
    )
    args = p.parse_args()

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / f"{args.skill}.jsonl"

    entry = {
        "skill": args.skill,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tool": args.tool,
        "task_summary": args.task,
        "outcome": args.outcome,
        "issues": args.issues,
        "missing_coverage": args.missing_coverage,
        "note": args.note,
    }

    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Logged {args.outcome} report for '{args.skill}' -> {out_path}")


if __name__ == "__main__":
    sys.exit(main())
