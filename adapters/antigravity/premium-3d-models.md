# Premium 3D Models (Antigravity agent rule)

Full skill: `skills/premium-3d-models/SKILL.md` in this repo. Read it
before building any 3D model.

- Ask (briefly) whether this is an "engineer" (precise, dimensioned,
  mechanical) or "designer" (organic/sculptural) piece if it's not
  obvious — see `skills/premium-3d-models/references/personas.md`.
- Build via `skills/premium-3d-models/scripts/build_model.py` (trimesh +
  manifold3d CSG) — real geometry, not an AI mesh generator, and honest
  about not doing true fillets/chamfers or organic freeform sculpting.
- Always run `skills/premium-3d-models/scripts/validate_model.py`
  (watertight/manifold check) before delivering.
- Always render a preview
  (`skills/premium-3d-models/scripts/render_preview.py --mode hero` or
  `--mode multiview`) and look at it before handing the model over.

Note: Antigravity's exact convention for loading project-level agent rules
may differ from this file's location — check Antigravity's current docs for
where it expects rule files, and move/symlink this one there if needed.
