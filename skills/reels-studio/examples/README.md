# Examples

| File | What it shows |
|---|---|
| `neoai_expensive_model_ar-EG.json` | Neo AI trend/myth-busting reel, Egyptian Arabic with English terms, Dr. Joshua, visual glitch hook, full posting pack — the house style (`brand: neoai`). |
| `neoai_diploma_ad_ar-EG.json` | **Ad**: 30 s performance master (PAS) for the Advanced AI Diploma + 15 s and 6 s bumper cutdowns, three ratios, ad copy, 3 hook variants. |
| `neoai_model_myth_youtube_ar-EG.json` | **Long-form**: ~3–4 min YouTube explainer with cold open, chapters, a demo, timecodes, title options and thumbnail concepts — the long version of the reel above. |
| `qahwa_house_latte_art_en.json` | English tutorial/listicle for a fictional café, left-to-right layout, series episode, default brand. |
| `ideas/ideas_neoai.json` | An idea board input for `scripts/score_ideas.py` (one idea deliberately fails the brand floor). |
| `rendered/` | Real output of `render_script.py` for the two specs (PDF via Chromium, DOCX via python-docx). |
| `tests/broken_spec.json` | Validator fixture — every planted fault must be reported (selftest checks the list). |
| `tests/broken_ad.json`, `tests/broken_long.json` | Ad and long-form rule fixtures (slot overrun, bumper limit, personal attribute, late hook, greeting opener, chapters, title length). |
| `tests/edge_spec.json` | Loose-but-legal shapes (meta as an object, strings where lists are expected, `arz`) that must still render. |

All example specs pass `validate_script.py --strict` (run with `--today 2026-10-03`; the trend
reference in the Neo AI example will start warning as it ages — that's the point).
