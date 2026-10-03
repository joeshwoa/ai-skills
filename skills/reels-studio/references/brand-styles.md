# Brand files & document styles

`brands/<slug>.json` is merged over `brands/default.json`, so a brand lists only what differs.

```json
{
  "name": "Client name",
  "about": "one line",
  "colors": {"text": "000000", "editor": "1D55A3", "talent": "8A1538", "mono": "1F68B0"},
  "font": {"family": "Cairo", "medium": "Cairo Medium", "files": ["Cairo-Regular.ttf", "Cairo-Medium.ttf"]},
  "page": {"size": "A4", "margin_mm": 12},
  "sizes_pt": {"title": 24, "meta": 19, "section": 20, "scene": 14, "label": 14, "body": 14, "legend": 13},
  "color_mode": "editor_talent",
  "legend": true,
  "labels": {"legend_editor": "FOR EDITOR", "legend_talent": "FOR TALENT", "end_frame": "END FRAME",
             "editor_notes": "EDITOR NOTES", "posting": "POSTING PACK", "script": "SCRIPT"},
  "end_frame_default": ["Brand"],
  "voice": {"language_default": "ar-EG", "register": "…", "tone_words": [], "never": []},
  "talents": {"Name": {"role": "…", "format": "…"}},
  "signatures": {"…": "recurring visual/audio signatures"},
  "notes": ["lessons learned from posted reels — newest first"]
}
```
- Fonts: put extra font files in `assets/fonts/` (licence file alongside) and list them in
  `font.files`; the PDF embeds them, the DOCX names them (install them for Word to show them).
  Cairo covers Arabic + Latin; the fallbacks handle other scripts.
- Labels can be localised (e.g. `"legend_editor": "للمونتير"`) if a client wants Arabic labels.

## The Neo AI house style (built in: `brands/neoai.json`)
Taken from the team's own scripts:
- **REEL — STAY UP TO DATE (Dr. Joshua)**: title + target duration; `FOR EDITOR` (blue) /
  `FOR TALENT` (dark red) legend on the left; scenes `SCENE 0N — NAME`; Visual/SFX lines blue;
  speaker label black; spoken lines dark red; `EDITOR NOTES` in blue at the end.
- **REEL 03 / REEL 04 (Saif, Ms. Sama)**: Talent / Duration / Tone (• separated) / Purpose header;
  `Visual:` and `Dialogue:` labels in black, every body line blue → use `"color_mode": "mono"` and
  `"label": "Dialogue"` on dialogue blocks; `Pause.` lines; END FRAME with event, date, FREE EVENT,
  REGISTER NOW, Neo AI.
- **HERO REEL — Mr. Wael / Sama | COO**: Campaign / Role / Duration / Language / Tone / Format
  header; a production brief before the script (الفكرة الإبداعية, VISUAL DIRECTION, CAMERA &
  MOVEMENT, PERFORMANCE & BODY LANGUAGE, WARDROBE, MUSIC & SOUND, EDITING STYLE, OVERALL FEEL) →
  the `founder_statement` template's `sections`.

## Matching a new client's own format
If the user sends a script in their own style: read it, then set colours (sample them from the PDF
if needed), labels, header fields (`meta`), section headings and scene naming in a new brand file;
render a sample and compare side by side with their document before writing the real script.
