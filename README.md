# AI Skills — Joshua

A personal library of AI-agent skills, built to work the same way whether
you're using Claude, Cursor, Antigravity, ChatGPT, or another coding/agent
tool — one shared `skills/<name>/SKILL.md` per capability, plus thin
per-tool adapters so each tool discovers it its own way.

## Layout

```
skills/<skill-name>/
  SKILL.md          # the actual instructions an agent follows
  scripts/          # deterministic code the skill runs (not re-derived each time)
  references/        # docs loaded on demand (schemas, style guides, etc.)
  assets/            # things the skill outputs directly (templates, generated galleries)
  examples/          # worked examples / test fixtures

adapters/
  cursor/            # .mdc rule files for Cursor's Project Rules
  antigravity/        # rule files for Antigravity
  generic/AGENTS.md   # the emerging cross-tool convention several agents read automatically
  chatgpt/            # text to paste into ChatGPT custom instructions (no file API exists)

tools/install.sh     # drops the adapters into this machine's tool config dirs
```

## Skills

- **[premium-presentations](skills/premium-presentations/SKILL.md)** —
  fully editable, professional/premium slide decks (native .pptx via
  python-pptx, not flattened HTML), with a design-interview step, a themed
  visual gallery, real-data-not-placeholder content, and slide transitions.
  Also documents how to extend the same approach to docs/sheets/PDFs.
- **[premium-3d-models](skills/premium-3d-models/SKILL.md)** — real,
  parametric 3D models (.glb + optional .stl/.obj) via CSG (trimesh +
  manifold3d booleans), for Flutter (model_viewer_plus), web/React
  (model-viewer / react-three-fiber), Blender import (with a live-push
  path when Blender's MCP is connected), or 3D printing. Two personas
  (engineer: exact dimensioned mechanical parts; designer: organic/
  sculptural form) and its own validator (watertight/manifold checks) and
  preview renderer (orthographic multiview sheet or hero/turntable shot).
- **[premium-subtitle-localization](skills/premium-subtitle-localization/SKILL.md)**
  — find or transcribe source-language subtitles (faster-whisper, fully
  local), translate them through a four-pass "virtual expert team"
  workflow (literal draft, meaning-preserving rewrite, cultural/comedic
  adaptation, fluency & timing polish — never a flat mechanical
  translation), validate formatting/timing with an automated checker plus
  an agentic meaning/quality review pass, then mux into the video with
  `ffmpeg` stream-copy (no re-encode unless burned-in subtitles are
  specifically needed).

More skills get added here over time, one folder per skill, following the
same layout and the same standard: ask before guessing on anything
subjective (design, scope, tone), never fabricate data, verify the output
before handing it over, and keep every tool's adapter in sync.

## Connecting a skill to your tools

```bash
bash tools/install.sh                    # installs global rules where each tool supports them
bash tools/install.sh ~/path/to/project  # + installs project-level rules and copies skills/ in
```

Run this in a real terminal on your machine — see `tools/install.sh` for
what it does and its ChatGPT/Antigravity caveats (no universal "install a
skill" API exists across tools, so this works by placing files where each
tool already knows to look).

## Adding a new skill

1. `mkdir -p skills/<name>/{scripts,references,assets,examples}`
2. Write `skills/<name>/SKILL.md` — frontmatter (`name`, `description`)
   plus the instructions. See `skills/premium-presentations/SKILL.md` for
   the level of detail to aim for.
3. Add matching entries to `adapters/generic/AGENTS.md` and, if relevant,
   a `.mdc` file under `adapters/cursor/`.
4. Commit and push — `bash tools/install.sh` picks up every skill under
   `skills/` automatically, no need to edit the install script itself.
