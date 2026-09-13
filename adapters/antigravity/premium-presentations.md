# Premium Presentations (Antigravity agent rule)

Full skill: `skills/premium-presentations/SKILL.md` in this repo. Read it
before building any presentation, pitch deck, or slide deck.

- If the user hasn't specified a visual theme, ask them and show
  `skills/premium-presentations/assets/theme_gallery.html` — don't guess.
- Generate the deliverable natively with
  `skills/premium-presentations/scripts/build_deck.py` (python-pptx) so
  every text element stays editable — do not convert from HTML/images.
- Use `skills/premium-presentations/scripts/render_preview.py` for an
  animated HTML preview / PDF source.
- Fill the deck with real data; flag missing figures instead of inventing
  them.

Note: Antigravity's exact convention for loading project-level agent rules
may differ from this file's location — check Antigravity's current docs for
where it expects rule files, and move/symlink this one there if needed.
This file is intentionally plain Markdown with no tool-specific frontmatter
so it's easy to relocate.
