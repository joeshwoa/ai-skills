# Agent instructions — this repo

This repo stores reusable "skills" (agent playbooks) under `skills/<name>/`.
Any coding agent working in a project that includes this repo (or has this
file copied into it) should, before doing work that matches a skill's
purpose, read that skill's `SKILL.md` in full and follow it.

## Available skills

- **premium-presentations** (`skills/premium-presentations/SKILL.md`) —
  build fully editable, professional/premium presentations (and to the same
  bar, documents/spreadsheets/PDFs). Trigger: any request for a deck,
  slides, pitch deck, PowerPoint, or presentation.
- **premium-3d-models** (`skills/premium-3d-models/SKILL.md`) — build
  real parametric 3D models (.glb/.stl/.obj) for Flutter, web/React,
  Blender, or 3D printing. Trigger: any request to "model," "3D model,"
  or make a 3D object/part/asset/prop.

This file follows the emerging `AGENTS.md` convention several agentic tools
(Cursor, GitHub Copilot, OpenAI Codex CLI, and others) read automatically
from a repo root. Copy this file (or symlink it) into the root of any
project where you want these skills auto-discovered, and keep the
`skills/` folder alongside it — or point your tool's rule/instructions
setting directly at `skills/<name>/SKILL.md`.
