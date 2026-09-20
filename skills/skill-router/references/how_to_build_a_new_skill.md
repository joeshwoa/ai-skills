# How to build a new skill from scratch

The methodology every skill in this repo already follows. Use this when
`how_to_search_and_install.md` reaches Step 4 (nothing to convert, no
pre-made skill worth adopting).

## 1. Get the spec right before writing anything

- If the task involves subjective choices (visual style, tone, structure)
  and the user hasn't specified them, ask briefly — a wrong direction is
  expensive to redo, a short question is not (premium-presentations is
  the reference example for this).
- If it's a conversion of the user's own tool/prompt/workflow into a
  skill, read whatever he already has (an existing prompt, an MCP
  server, a script) in full before designing — the skill should
  faithfully capture what already works, not a guessed reinterpretation.

## 2. Scaffold

```bash
mkdir -p skills/<name>/{scripts,references,examples}
```

- `SKILL.md` — frontmatter (`name`, `description`) + the instructions.
  The `description` is a trigger, not a summary: write it the way the
  five existing skills do — mention concrete phrases a user would
  actually say, and what request types map to this skill.
- `scripts/` — deterministic code the skill runs (not re-derived by the
  agent each time it's used). Anything that can be a tested script
  should be one, rather than freeform agent reasoning repeated per run.
- `references/` — docs loaded on demand (schemas, style guides, tool
  catalogs, checklists) — keeps `SKILL.md` itself lean.
- `examples/` — worked examples / test fixtures, ideally captured from
  a real run of the skill's own scripts, not hand-written/guessed.

## 3. Build with real verification, not assumed correctness

- Every script that can be tested standalone, test it standalone first
  (e.g. `srt_utils.py`'s round-trip self-test, `mcp_cli.mjs` tested
  against both a hand-written fake server and the real target server).
- Every generator/validator pair: run the generator, then run the
  validator against real output, on both a clean case and a deliberately
  broken case, and confirm it catches the broken one.
- If a dependency fails to build in the environment being used to build
  the skill, don't fight it silently — find a dependency-free
  alternative (e.g. `srt_utils.py` was written from scratch instead of
  depending on the `srt` pip package after it failed to build) and note
  why in a comment.
- If something is discovered to be broken in a source repo the skill
  wraps (not this repo), don't patch around it by guessing replacement
  code — diagnose the real cause, have the skill's own bootstrap/setup
  step detect and clearly report it, and tell the user directly (see
  the omnicinema-mcp `.gitignore` bug for the pattern to match).

## 4. Mandatory validator + honest limits

- Every skill needs *some* automated check of its own output (a
  validator script, a packaging check, or both) — never ship a skill
  that only "looks right."
- Write down real limits in `SKILL.md` (what it can't do, what still
  needs a human) rather than implying it handles everything.

## 5. Package and validate

If skill-creator's packaging tool is available in the current
environment:
```bash
python3 -m scripts.package_skill <path/to/skills/name> <out-dir>
```
Fix anything it flags before moving on.

## 6. Wire it into the repo

- Add an entry to `adapters/generic/AGENTS.md` (one bullet: name, one-
  line summary, trigger).
- Add `adapters/cursor/<name>.mdc` (frontmatter `description` = trigger,
  body = quick-reference pointing back at the full `SKILL.md`).
- Add a short paragraph to `adapters/chatgpt/custom_instructions.md` if
  relevant — and be honest there about what ChatGPT chat literally can't
  do (e.g. run local shell scripts) rather than implying it works the
  same way as a shell-capable tool.
- Add a bullet to the repo `README.md`'s Skills list.
- Regenerate the manifest: `python3 skills/skill-router/scripts/
  build_manifest.py`.
- Re-run `bash tools/install.sh` so the repo's own root-level
  `.cursor/rules/` + `AGENTS.md` copies refresh too (these are committed
  to git, not gitignored — easy to forget this step, don't).

## 7. Commit, push, sync

- Commit with a message explaining *why*, not just *what* (see this
  repo's git log for the tone/level of detail expected).
- Push to `github.com/joeshwoa/ai-skills` — transient GitHub PAT pasted
  by the user, embedded in the remote URL, used, reset to the plain URL
  immediately after. Never persist the token to disk or any config, even
  if asked to.
- `~/.cursor/ai-skills` is a SEPARATE clone Cursor actually reads from —
  sync it too: `git stash` (there's usually real uncommitted WIP there,
  not yours to touch — never lose it), fetch+merge (or pull) with the
  same transient token, `git stash pop`.
- Symlink the new skill for Cursor: `ln -s
  /Users/joshua/.cursor/ai-skills/skills/<name>
  ~/.cursor/skills/<name>` — literal real Mac absolute path as the
  target, every time (a sandbox-bridge-local path produces a symlink
  that's broken when Cursor reads it natively on the real machine).

## 8. Tell the user

One short summary after everything above is done — what was built, what
was verified, and anything that needs his attention (a real bug found
along the way, a decision only he can make, work of his own that was
found and deliberately left untouched). Not a step-by-step narration
during the work, and not a series of permission requests for steps that
are already part of this standing procedure.
