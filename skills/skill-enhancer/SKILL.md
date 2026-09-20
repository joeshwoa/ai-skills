---
name: skill-enhancer
description: >
  Audits and improves any skill in this repo using real usage reports
  (or a direct read-through when none exist yet) — finds recurring
  issues, missing coverage, and rough edges, fixes them, re-validates,
  and ships the update. Use when a skill produced a bad/wrong/incomplete
  result and should be fixed, when asked to "enhance"/"improve"/"audit"
  a skill, when asked to review skill quality or performance, or
  periodically to process accumulated usage reports. Also defines the
  reporting mechanism itself (skill-router logs a report after every
  skill use) that feeds this.
---

# Skill Enhancer

The other half of skill-router: skill-router gets the right skill picked
and installed; this closes the loop by finding out how each skill
actually performed and fixing what's wrong or missing.

## Part 1 — how reports get logged (already wired in)

Every skill use ends with a one-line report, logged by
`scripts/log_report.py` to `~/.cache/ai-skills/reports/<skill>.jsonl`
(local, not committed to git — see the script's docstring for why: no
git/network needed just to log, and it never bloats repo history).
`skills/skill-router/SKILL.md` is what actually instructs the agent to
do this — it's read first, always, for every task, so this is enforced
centrally rather than needing every individual skill's `SKILL.md` edited.
Nothing else to do here; this section just documents the mechanism so
it's not a mystery when you're reading accumulated reports later.

Report fields: `skill`, `timestamp`, `tool`, `task_summary` (one line,
no sensitive/personal content — just enough to identify the pattern),
`outcome` (`success`/`partial`/`failure`), `issues` (specific problems
hit), `missing_coverage` (something the task needed that the skill
didn't handle), `note` (free text). See
`references/report_schema.md` for the full spec and rationale for each
field.

## Part 2 — enhancing a skill

Full procedure: `references/enhancement_checklist.md`. Summary:

1. **Gather signal.**
   ```bash
   python3 skills/skill-enhancer/scripts/analyze_reports.py <skill-name>
   # or, across every skill with reports:
   python3 skills/skill-enhancer/scripts/analyze_reports.py --all
   ```
   This groups recurring issues/missing-coverage by exact text and
   surfaces recent failures/notes — it does the counting, you do the
   judgment (similar-but-differently-worded issues need to be merged by
   reading them, not just counted separately).
2. **No reports yet?** Not a failure — do a direct read-through audit
   instead: read the skill's `SKILL.md`, every script, and its
   `references/` in full against its own stated purpose and the general
   build standard (`skills/skill-router/references/
   how_to_build_a_new_skill.md`). Look specifically for: scripts with no
   test/validation path, vague or guessable instructions where the skill
   should instead ask or use a script, and stated capabilities with no
   corresponding example.
3. **Diagnose root cause**, not just the symptom, for each finding —
   read the actual relevant code/instructions before deciding the fix.
4. **Apply the fix** — could be a script bug fix, a new validation case,
   an expanded reference doc, a clarified `SKILL.md` instruction, a new
   example covering the gap, or an honest new line in a "limits" section
   if something genuinely can't be fixed yet.
5. **Re-verify**, same rigor as building it the first time: re-run the
   skill's own self-tests/validators, re-run skill-creator's packaging
   check, and if the fix touches a tested end-to-end path (like an MCP
   wrapper), re-run that test too. Don't ship an unverified "fix."
6. **Log the change** in that skill's own `references/changelog.md`
   (create it if this is the skill's first logged change) — one dated
   line: what changed, why, and which report(s)/finding prompted it.
7. **Ship it** — regenerate `skills/manifest.json`, commit, push, sync
   the Cursor clone + symlinks (same checklist as
   `skills/skill-router/references/how_to_build_a_new_skill.md`'s
   commit/push/sync section — don't re-derive it, follow that one).
8. **Archive the consumed reports** so the same feedback isn't
   "fixed" twice: `analyze_reports.py <skill-name> --archive`.
9. **Tell the user** what was found and fixed, in one short summary —
   and be honest about anything found but NOT fixed (needs a decision
   only they can make, or is blocked on something outside this repo,
   like the omnicinema-mcp upstream bug).

## When asked to enhance "everything"

Run `analyze_reports.py --all` first to see which skills actually have
signal. For skills with none yet, a full read-through audit of all of
them in one pass is reasonable when asked for directly, but don't invent
problems to fix — an honest "read it, nothing wrong found, here's what I
checked" is a valid outcome, not a failure to find something.
