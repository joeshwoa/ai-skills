# How to search for and install a skill

Used when `skills/manifest.json` has no entry matching the current task.
Go in this order — stop at the first step that resolves it.

## Step 1 — is this already covered for free?

Most AI tools (Claude sessions, Cursor, etc.) ship their own built-in
skills/plugins for common formats (Word docs, PDFs, spreadsheets, slide
decks, charts, and similar). If the current tool already has one that
covers the task, use it directly — don't build a duplicate into this
repo. Only continue past this step if the task is either not covered at
all, or needs something more specific/premium than the generic built-in
(the existing premium-presentations skill exists exactly because plain
deck generation wasn't good enough — that bar applies here too).

## Step 2 — does the user already own a source for this?

The most common case: one of Joshua's own MCP servers
(`github.com/joeshwoa/*-mcp` — check his GitHub for the current list,
it grows) does what's needed but hasn't been converted to skill form
yet. This is **pre-approved** — no need to ask before converting it.

Conversion pattern (already used for `omnicinema` and `devuniverse`,
copy that approach exactly):
1. Clone the MCP repo, read its `src/server.ts` (or equivalent) in full
   to get every tool's exact name and argument schema — never guess or
   paraphrase these, extract them verbatim.
2. Build a `scripts/mcp_cli.mjs` (copy the one from `skills/omnicinema/
   scripts/mcp_cli.mjs` — it's generic, works against any MCP stdio
   server unchanged) plus `scripts/bootstrap.sh` (clone+build into
   `~/.cache/ai-skills/<repo-name>`) and `scripts/call.sh <tool>
   '<json-args>'`.
3. Write `references/tools.md` documenting every tool (name, args,
   notes) extracted from the real source.
4. Write `SKILL.md` pointing at the workflow above.
5. **Test it end-to-end against the real server** before calling it
   done — at minimum, bootstrap it and call one safe, side-effect-free
   tool, and check the JSON result parses and isn't an error. Don't ship
   an untested wrapper.
6. If the source repo itself doesn't build cleanly from a fresh clone,
   don't patch around it by guessing at missing code — diagnose the real
   cause (check `.gitignore`, `git log --all -- <missing path>` to see
   if it was ever committed), have `bootstrap.sh` detect the failure and
   print the exact fix, and tell the user directly. (This happened with
   `omnicinema-mcp`'s `.gitignore` excluding `src/assets/` — see that
   skill's `SKILL.md` for the exact writeup style to match.)

## Step 3 — search for a pre-made skill

If nothing the user already owns covers it, search for a public skill
that does — marketplace/registry search tools if the current AI tool
has them (e.g. a skill-search or MCP-registry search tool), otherwise a
targeted search for repos structured around a `SKILL.md` file matching
the topic.

**Vet anything found before installing it** (this is the one place to
actually slow down — everywhere else in this procedure is pre-approved
because it's either the user's own code or code built here from
scratch):
- Real license, not a dead/abandoned repo with no license at all.
- Skim the scripts for anything that shells out to unexpected places,
  phones home, or asks for credentials it has no obvious reason to need.
- Prefer a skill that's mostly plain scripts/docs over one that pulls in
  a pile of new dependencies for a small task.
- If it's close but not quite right, adapt it rather than installing it
  verbatim — rewrite its `SKILL.md` to this repo's frontmatter
  convention (`name`, `description` written as a trigger, see
  `how_to_build_a_new_skill.md`), and fold its scripts/references into
  the `skills/<name>/scripts|references|examples` layout every other
  skill here uses.
- If vetting turns up something concerning (no license, suspicious
  network calls, needs a credential with no clear reason), don't install
  it — say so plainly and either look for a different source or fall
  through to Step 4.

## Step 4 — nothing suitable exists: build one

See `how_to_build_a_new_skill.md` for the full checklist. This is the
default, safest path when the task is well-scoped and reusable — it's
what built all five skills already in this repo, none of which existed
anywhere to be found beforehand.

## After any of Steps 2–4

1. `python3 skills/skill-router/scripts/build_manifest.py` (refresh the
   manifest so it's picked up immediately).
2. Validate the new/changed skill with skill-creator's packaging
   validator if available (`python3 -m scripts.package_skill
   <skill-dir> <out-dir>` from wherever that tool lives in the current
   environment) — every skill in this repo has passed this check.
3. Add/update adapters: `adapters/generic/AGENTS.md`,
   `adapters/cursor/<name>.mdc`, and a short addition to
   `adapters/chatgpt/custom_instructions.md` if the skill is something
   ChatGPT chat could meaningfully help plan even without running
   scripts itself.
4. `bash tools/install.sh` (refreshes this repo's own root-level
   `.cursor/rules/` + `AGENTS.md`, and prints the ChatGPT/global-Cursor
   reminders).
5. Commit and push to `github.com/joeshwoa/ai-skills` (transient PAT
   pattern — never persist the token, even if asked; see the project
   status doc for why).
6. Sync `~/.cursor/ai-skills` (the separate clone Cursor reads from):
   `git stash` any local WIP found there first, pull, `git stash pop` —
   never lose uncommitted work that isn't yours. Then symlink the new
   skill: `ln -s /Users/joshua/.cursor/ai-skills/skills/<name>
   ~/.cursor/skills/<name>` — the target MUST be the literal real Mac
   absolute path, not a sandbox-bridge-local path, or the symlink is
   broken when Cursor reads it natively.
7. Tell the user, briefly, what was added/changed and why — after the
   fact, not as a series of permission requests for each of the steps
   above.
