# Reel spec (JSON) — the single source of truth

Write the script as a spec, validate it, render it. Never hand-edit the PDF/DOCX; edit the spec and
re-render. Start from a template: `bash scripts/rs.sh new --list`.

```jsonc
{
  "version": 1,
  "brand": "neoai",                    // brands/<slug>.json (optional; default look otherwise)
  "language": "ar-EG",                 // drives direction (RTL/LTR), speaking rate, dialect checks
  "direction": "rtl",                  // optional override
  "color_mode": "editor_talent",       // or "mono" (all body lines one blue, like REEL 03/04)
  "legend": true,                      // FOR EDITOR / FOR TALENT (off automatically in mono)
  "title": "REEL — …",
  "meta": [["Talent", "Dr. Joshua"], ["Target Duration", "55–65 sec"], ["Tone", "A • B • C"], ["Purpose", "…"]],
  "intro_note": "السكربت مكتوب English لكن انت فري بين العربي والانجلش عادي.",   // optional

  "brief": {                           // not printed (except via production export) — the validator needs it
    "platforms": ["instagram_reels", "tiktok"],   // instagram_reels tiktok youtube_shorts facebook_reels linkedin snapchat_spotlight x threads
    "audience": "who exactly",
    "awareness_stage": "problem_aware",
    "goal": "consideration",
    "funnel_stage": "middle",
    "format": "talking_head",
    "hook_type": "news_jacking",
    "duration_sec": [55, 65],          // or a single number
    "words_per_sec": 2.1,              // optional: measured pace of this talent
    "cta": "Enroll in …",               // or "none" for a deliberate no-ask piece
    "account_type": "business",        // creator | business (audio-rights check)
    "scope": "single reel",
    "trend_refs": [{"name": "…", "kind": "audio|format|meme|news_jacking|occasion",
                    "source": "url or 'user brief'", "checked": "2026-10-03"}]
  },

  "sections": [                        // optional production brief before the script (founder style)
    {"heading": "VISUAL DIRECTION", "paragraphs": ["…"], "bullets": ["…"], "audience": "neutral|editor|talent"}
  ],
  "script_heading": "SCRIPT",          // printed only when sections exist

  "scenes": [
    {
      "title": "SCENE 01 — VISUAL HOOK",
      "duration": "1.2 sec",           // printed
      "duration_sec": 1.2,             // used for timing; otherwise estimated from words
      "blocks": [
        {"type": "visual", "lines": ["…"]},
        {"type": "sfx", "lines": ["…"]},
        {"type": "onscreen_text", "lines": ["…"]},
        {"type": "dialogue", "speaker": "Dr. Joshua", "lines": [
          "\"line one", {"pause": true}, {"direction": "Small confident smile"}, "line two.\""
        ]},
        {"type": "dialogue", "label": "Dialogue", "lines": ["…"]}     // label instead of a speaker name
      ]
    }
  ],
  "end_frame": {"lines": ["NEXT_START", "September 12, 2026", "Neo AI"], "notes": ["Minimal animation"]},
  "editor_notes": ["…"],
  "posting": {"cover_text": "…", "caption": "…", "hashtags": ["#…"], "first_comment": "…",
              "title": "YouTube Shorts title", "alt_hooks": ["…"], "best_time": "…"},
  "render_posting_pack": true          // false = keep the posting pack out of the PDF
}
```

Block types and colours:
| type | label | colour (editor_talent) |
|---|---|---|
| visual, camera, broll, sfx, music, onscreen_text, transition, note | Visual / Camera / B-Roll / SFX / Music / On-screen Text / Transition / Note | blue |
| dialogue, voiceover, direction | speaker name or label (label black) | dark red |
Override any label with `"label"`. `{"pause": true}` prints `Pause.` (or `{"pause": true, "text": "وقفة."}`).
