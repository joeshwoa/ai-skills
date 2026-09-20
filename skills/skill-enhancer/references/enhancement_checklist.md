# Enhancement checklist (full version)

The expanded version of `SKILL.md`'s Part 2 summary — read that first for
the shape of the procedure, this is the detail for each step.

## 1. Gather signal

```bash
python3 skills/skill-enhancer/scripts/analyze_reports.py <skill-name>
python3 skills/skill-enhancer/scripts/analyze_reports.py --all
```

Read the whole summary, not just the top issue. A skill with mostly
`success` and one `partial` isn't broken — don't manufacture a rewrite
to justify the pass. A skill with several `failure`s on the same
`issues` text is the real signal to act on.

## 2. No reports yet — direct audit

Read, in full:
- The skill's `SKILL.md` — is every claimed capability actually
  something the scripts/references back up, or is part of it aspirational
  text with nothing behind it?
- Every file under `scripts/` — does it have its own test/validation
  path (a self-test, a paired validator, or was it verified end-to-end
  when built)? A script with no way to check its own output is a gap
  even with zero usage reports.
- `references/` — do they match what the scripts and SKILL.md actually
  do, or have they drifted since the skill was last touched?
- `examples/` — is there a real, captured example (ideally from an
  actual run), or is it missing/hypothetical?

Cross-check against `skills/skill-router/references/
how_to_build_a_new_skill.md`'s build standard — that's the bar every
skill in this repo is supposed to meet already; an audit is checking the
skill still meets it, not inventing a new bar.

## 3. Diagnose before fixing

For each finding, read the actual relevant script/instruction before
deciding what to change. Two issues that look similar can have different
root causes:
- "video embedding not covered" in premium-presentations could mean the
  skill's SKILL.md never mentions it (documentation gap — add guidance)
  or that `build_deck.py` has no code path for it at all (real feature
  gap — needs new generator code, test it before shipping).
- A skill "asked too many questions" could mean its design genuinely
  needs that information (not a bug — maybe the report's expectation was
  off) or that it's re-asking something already given earlier in the
  conversation (real bug in how it reads context).

Don't patch the visible symptom without knowing which of these it is —
the omnicinema-mcp `.gitignore` bug from this repo's own history is the
model here: the symptom was "build fails," the fix that actually mattered
was tracing it to the real root cause, not guessing at replacement code.

## 4. Apply the fix

Whatever form it takes, keep it consistent with how every other skill in
this repo is built (see `how_to_build_a_new_skill.md` again): scripts do
the deterministic work, `references/` hold docs loaded on demand,
`SKILL.md` stays lean, `examples/` are real captured output not
hypothetical.

If the finding is genuinely not fixable right now (an upstream bug in
someone else's repo, a decision only the user can make, a capability
that's out of scope) — say so in the changelog and to the user, don't
force a fix that doesn't actually work.

## 5. Re-verify

Match the original build's rigor:
- Any script with a self-test: re-run it.
- Any validator (e.g. `validate_srt.py`, `validate_deck.py`,
  `validate_model.py`): re-run against both a clean case and the
  specific broken case that prompted the fix, confirm the validator
  catches what it should and passes what it should.
- skill-creator packaging check on the whole skill:
  ```bash
  python3 -m scripts.package_skill <path/to/skill> <out-dir>
  ```
- For an MCP-wrapper skill (omnicinema, devuniverse): re-run
  `bootstrap.sh` and at least one `call.sh` invocation against the real
  server if the fix touched that path at all.

## 6. Log the change

`skills/<name>/references/changelog.md` — create if it's the skill's
first logged change:
```markdown
# Changelog

- YYYY-MM-DD: <what changed and why>. Prompted by: <report pattern /
  finding — be specific, e.g. "2 failure reports: video embedding not
  covered">.
```
One line per change, dated, newest at the bottom (or top — match
whatever the file already does once it exists; don't reformat past
entries).

## 7. Ship it

Same checklist as adding a new skill
(`skills/skill-router/references/how_to_build_a_new_skill.md`'s section
6-7): regenerate `skills/manifest.json` (only matters if the
`description` frontmatter changed, but cheap to always run), commit with
a message explaining what was found and fixed and why, push (transient
PAT, never persisted), sync `~/.cursor/ai-skills` (stash any real
uncommitted user WIP found there first — never touch it), symlink stays
the same if the skill already existed (only new skills need a new
symlink).

## 8. Archive consumed reports

```bash
python3 skills/skill-enhancer/scripts/analyze_reports.py <skill-name> --archive
```
So the next enhancement pass isn't re-reading and re-"fixing" the same
already-addressed reports. The archived file (`<skill>.<timestamp>.jsonl.processed`)
stays on disk as a record — don't delete it.

## 9. Tell the user

One short summary: what was found (from reports or direct audit), what
was changed and why, what was verified, and anything found but
deliberately left alone (with the reason). Don't narrate every
step — the checklist above is for you to follow, not to report back
line by line.
