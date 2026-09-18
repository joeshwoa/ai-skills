# Premium Subtitle Localization (Antigravity agent rule)

Full skill: `skills/premium-subtitle-localization/SKILL.md` in this repo.
Read it before subtitling/translating any video.

- Step 0: confirm video path, source/target language(s), genre/tone, and
  soft-sub vs. hardsub preference before starting.
- Look for existing subtitles first
  (`skills/premium-subtitle-localization/scripts/find_subtitles.py`)
  before transcribing from audio
  (`skills/premium-subtitle-localization/scripts/transcribe.py`).
- Translate yourself, in the four passes documented in
  `skills/premium-subtitle-localization/references/translation_workflow.md`
  — never hand this off to a mechanical translation API, that produces
  flat literal output with dead jokes and broken idioms.
- Run both QA layers before merging: the automated
  `scripts/validate_srt.py` (formatting/timing) and the judgment-based
  `references/qa_review_checklist.md` (meaning/quality) — they catch
  different classes of problem.
- Merge with `scripts/merge_subtitles.py` (soft-sub default, no
  re-encode) and confirm with `scripts/verify_output.py` before telling
  the user the video is ready.

Note: Antigravity's exact convention for loading project-level agent rules
may differ from this file's location — check Antigravity's current docs for
where it expects rule files, and move/symlink this one there if needed.
