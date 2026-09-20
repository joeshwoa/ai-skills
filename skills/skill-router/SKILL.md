---
name: skill-router
description: >
  Read this FIRST, before any other skill, for any non-trivial request —
  it is the dispatcher for every skill in this repo. Checks
  skills/manifest.json and auto-selects a matching installed skill with no
  need to ask the user which one to use. If nothing installed matches,
  searches for or builds a new skill and installs it into this repo
  automatically (clone/build for the user's own MCP repos, or build from
  scratch via the skill-creator methodology), then tells the user what was
  added. Also covers keeping skills/manifest.json in sync as skills are
  added or changed.
---

# Skill Router

This is the meta-skill: it makes the rest of `skills/` self-selecting
(no need to be told "use the premium-presentations skill") and
self-extending (no need to hand-build every new skill from a blank
prompt — this documents the repeatable procedure).

## Part 1 — Auto-select from installed skills

1. Read `skills/manifest.json`. If it's missing or looks stale (a
   `skills/<name>/SKILL.md` exists with no matching entry, or vice
   versa), regenerate it first:
   ```bash
   python3 skills/skill-router/scripts/build_manifest.py
   ```
2. Compare the current task against each entry's `description` (these
   are the same descriptions written for exactly this purpose — every
   skill in this repo has a trigger-oriented description by convention,
   see `references/how_to_build_a_new_skill.md`).
3. On a match: read that skill's full `SKILL.md` at `<path>/SKILL.md`
   and follow it. Don't ask the user "should I use skill X for this" —
   that's what this router is for. Do briefly say which skill you're
   using if it's not obvious from context (one line, not a preamble).
4. On no match: go to Part 2.
5. Multiple skills plausibly match (e.g. a task spans video generation
   *and* subtitling): it's fine to use more than one, in whatever order
   the task naturally needs them.
6. **When the task is finished, log a usage report** (this is how
   skill-enhancer gets real signal to work from instead of guessing):
   ```bash
   python3 skills/skill-enhancer/scripts/log_report.py <skill-name> <success|partial|failure> \
     --tool <claude|cursor|antigravity|chatgpt> --task "one-line summary, no sensitive content" \
     [--issue "specific problem hit"] [--missing "something the task needed that wasn't covered"] \
     [--note "free text"]
   ```
   This is a local append, no git/network needed — do it every time, it
   costs nothing. If more than one skill was used for the task, log one
   report per skill. See `skills/skill-enhancer/references/
   report_schema.md` if the outcome/fields are unclear for a given case.

## Part 2 — No installed skill matches: search, then build

Full procedure: `references/how_to_search_and_install.md`. Summary:

1. **Check tool-native built-ins first.** If the AI tool this is running
   in already ships a built-in skill/plugin covering the task (e.g. a
   session's own `docx`/`pptx`/`pdf`/`xlsx` skills, or other bundled
   skills), just use that — don't duplicate it into this repo.
2. **Check for a matching source the user already owns** — most often
   one of his own MCP servers (github.com/joeshwoa/\*-mcp) that hasn't
   been converted yet. If the task matches one, convert it using the
   established pattern (a generic one-shot MCP stdio client — see
   `skills/omnicinema/scripts/mcp_cli.mjs` for the reference
   implementation — never reimplement the server's logic). This is
   pre-approved; don't ask before doing it.
3. **Search for a pre-made skill** matching the task (marketplace/
   registry search tools if the current AI tool has them; otherwise a
   targeted web/GitHub search for repos following the `SKILL.md`
   convention). Lightly vet anything found before installing it — see
   `references/how_to_search_and_install.md`'s vetting checklist. This
   is the one place to slow down: code from a stranger, not the user's
   own repo, gets a quick look before it's adopted and run.
4. **Nothing suitable exists anywhere: build one from scratch**, using
   the same methodology every skill in this repo already follows —
   `references/how_to_build_a_new_skill.md` is the full checklist
   (spec → generator scripts → mandatory validator → examples → SKILL.md
   → adapters → commit → push → sync to Cursor). This mirrors exactly
   how premium-presentations, premium-3d-models, and
   premium-subtitle-localization were built.
5. **After installing or building anything**: regenerate the manifest,
   run `bash tools/install.sh`, commit, push, and sync the Cursor clone
   + symlink (all covered in `references/how_to_build_a_new_skill.md`'s
   last section). Tell the user what was added and why in one short
   summary — don't ask permission at each of these steps, this whole
   sequence is the standing, already-approved procedure. The one
   exception: if installing something needs a new credential/API key
   from the user, or involves adopting a stranger's code with a real
   licensing or safety concern, say so plainly before proceeding rather
   than guessing past it.

## Keeping the manifest honest

Any time a skill is added, renamed, or its `SKILL.md` description
changes, re-run:
```bash
python3 skills/skill-router/scripts/build_manifest.py
```
`tools/install.sh` also does this automatically on every run, so a
normal install/sync already keeps it current — but re-run it by hand
right after editing a `SKILL.md` so the router has the latest version
during the same task.
