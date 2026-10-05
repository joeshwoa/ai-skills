---
name: video-post-studio
description: A complete post-production house the AI runs itself on free tools (the user's studio-mcp) — editing existing footage into a finished piece AND making new videos from a brief, stock and motion graphics. Full team: post producer, editor, assistant editor, story/transcript editor, colorist, sound editor and mixer, music supervisor, graphics, captions, QC and delivery. Scene detection and take selection, Descript-style transcript editing (Arabic and English filler removal), cut-to-beat montages, J/L cuts, b-roll from own footage or free stock, colour match and grading (.cube LUTs), ducked music, captions, broadcast/social QC, platform exports, and editable masters (Kdenlive, FCPXML/OTIO/EDL for DaVinci Resolve, Premiere, Final Cut). Use for any request to edit, cut, montage, assemble, recut, colour, mix, caption, reframe, clean up or deliver a video — or to make a reel, ad, promo, YouTube video or documentary from footage, a script or a voiceover — even when no tool is named.
---

# Video Post Studio

A professional post-production house in one skill. It works on the user's own MCP server
**studio-mcp** (github.com/joeshwoa/studio-mcp), the same server as the `creative-studio`
skill. Every tool renders real files AND returns previews (contact sheets, storyboards, QC
tables) — the editor LOOKS at every preview before anything goes to the client.

Two kinds of job:
- **EDIT** — the client has footage (interviews, talking heads, events, product shoots, phone
  clips) → a finished piece.
- **MAKE** — nothing shot yet → a new video from a brief: script or voiceover, free stock
  b-roll (stock-library skill), motion graphics (motion-design-studio skill), music, captions.
  Cinematic AI footage with characters/dialogue comes from flow-studio-director; this house
  then edits, colours, mixes and delivers it.

Paths are relative to this skill's folder (`skills/video-post-studio/` in the ai-skills repo).

## Setup
The environment is shared with creative-studio — install once:
```bash
bash ../creative-studio/scripts/bootstrap.sh     # studio-mcp + Chromium into a venv on the PortableSSD
bash scripts/selftest.sh                          # proves the editing tools work here
```
Call tools with `bash scripts/call.sh <tool> '<json>'` (or `@args.json`), `call.sh help <tool>`,
or directly when the MCP server is registered (`../creative-studio/references/mcp-setup.md`).
Full tool reference: `references/tools.md`. Engine notes and limits: `references/engine-reference.md`.

## The team (`references/team.md` has each role's checklist)
| Role | Owns | Main tools |
|---|---|---|
| Post producer | brief, deliverables list, schedule, approvals, budget of time | — |
| Assistant editor (ingest/logging) | probe, sync, shot list, best takes, transcripts | `video_probe`, `video_scene_detect`, `video_select_takes`, `video_transcript` |
| Story / transcript editor | paper edit, structure, the cut by text | `video_transcript`, `video_transcript_edit` |
| Editor | assembly → rough → fine cut, pacing, J/L cuts, b-roll, transitions | `video_edit`, `video_auto_edit`, `video_cut_to_beats`, `video_broll`, `video_beats` |
| Colorist | balance, shot matching, look | `video_auto_color`, `video_color_match`, `video_grade` |
| Sound editor + mixer | dialogue clean-up, silences, SFX, ducking, loudness | `video_remove_silence`, `audio_clean`, `audio_sfx`, `video_music`, `video_loudness`, `audio_mix` |
| Music supervisor | music choice, tempo, licence | `stock_search kind=music`, `audio_music`, `video_beats` |
| Graphics (motion) | titles, lower thirds, CTAs, captions styling | motion-design-studio skill (`motion_*` tools, overlays in the timeline) |
| Captions & localisation | captions, SRT, safe zones, other languages | `video_captions`, `audio_transcribe`; translation → premium-subtitle-localization |
| Finishing / QC | technical QC before delivery | `video_qc`, `video_export` |
| Delivery & archive | platform exports, editable masters, credits | `video_export`, `video_export_interchange`, `stock_credits` |

If the AI tool can run sub-agents, run ingest/logging and stock research in parallel, and let a
separate agent do the final QC review (it didn't make the cut). Otherwise play the roles in order.

## Workflow (gates — never skip a LOOK)

**0. Brief (post producer).** Ask only what's missing, as numbered options with one
RECOMMENDED (Arabic questions short): platform(s) and ratio(s), length, goal + CTA, language/dialect
for captions and VO, tone/style (reel · ad · promo · YouTube · documentary · event recap ·
interview), brand kit (`brand=<slug>` from creative-studio), music feel, must-have shots/lines,
deadline, deliverables (MP4 per platform, SRT, editable project). Write a one-paragraph treatment
and a deliverables list; get a yes.

**1. Ingest & log (assistant editor).** `video_probe` every file (fps/rotation/codec/audio).
`video_scene_detect` on long clips, `video_select_takes` on a pile (goal: talking, broll,
stable, faces…), `video_transcript` for anything with speech. LOOK at the shot sheets. Note bad
audio, shaky shots, vertical vs horizontal.

**2. Paper edit (story editor).** For talk-driven pieces, choose the story from the indexed
transcript: the hook line, 3–5 beats, the ending/CTA. Mark removals (fillers, false starts,
repeats). Run `video_transcript_edit` (keep/reorder by text or word numbers;
`remove_fillers=true` handles English and Egyptian/MSA fillers only when they stand alone). Read
its cut list; listen-check any "audible remnant" warnings.

**3. Assembly → rough cut (editor).**
- Talk/VO pieces: the transcript edit (or the VO) is the spine; lay b-roll over it with
  `video_broll` or the timeline's overlays; L-cut the sound into the next shot where it helps.
- Montages/music videos: `video_beats` on the song, then `video_cut_to_beats` (every 1/2/4 beats,
  or a pattern like [4,2,2]) or `"cut_to_beats"` inside a `video_edit` timeline.
- MAKE jobs: `video_auto_edit` with a full brief (see `references/workflows.md` §MAKE). It plans
  shots per phrase, pulls b-roll from own footage and/or free stock in the right orientation,
  rejects stock clips that show identifiable people (model-release risk), adds music on the beat,
  captions, title, CTA, and writes `timeline.json` + EDIT-REPORT.md. Treat its output as the
  ROUGH CUT: LOOK at the storyboard, then improve the timeline by hand and re-render with `video_edit`.
- Pacing rules of thumb: reels/ads 1.4–2.8 s shots, a pattern change every 2–3 s, hook in the first
  1.5 s; YouTube 3–6 s; documentary 4–8 s. Cut on action or on the beat; never cut mid-word.

**4. Fine cut.** Tighten every cut (`video_edit` timeline: `in/out`, `j_cut`/`l_cut`,
`audio_crossfade` 10–30 ms on hard audio cuts, transitions only with a reason — a dissolve means
time passing, a whip means energy; default to cuts). Titles, lower thirds, CTAs as overlays (from
motion-design-studio). Show the client the cut sheet + a low-res render → notes → apply → **picture lock**.

**5. Colour (colorist).** Balance first (`video_auto_color`), then match every shot to the hero
shot (`video_color_match` → .cube), then one look for the whole piece (`grade` in the timeline or
`video_grade`). Skin tones natural; don't push looks on brand colours. LOOK at before/after sheets.

**6. Sound (editor + mixer).** Dialogue clean-up (`audio_clean`), remove dead air
(`video_remove_silence` for talking heads), SFX on key moments (`audio_sfx`: whoosh on
transitions, pops on text), music bed ducked under speech (`video_music` or timeline `duck`),
master to the platform target (`loudness`: social/youtube −14 LUFS, podcast −16, broadcast −23).

**7. Captions.** `video_captions` (reels/bold/karaoke/clean/boxed) or timeline `captions`. Arabic:
captions follow the spoken dialect; Arabic defaults to Tajawal (renders right in MP4 and Kdenlive).
Design stills/graphics with `leave_bottom` so captions never sit on on-screen text. Proofread the
`.srt` (Whisper on Egyptian Arabic is good, not perfect) — or pass exact words from the script.

**8. QC (finishing — independent eye).** `video_qc` with the platform: black/frozen frames,
flashes (3 Hz rule), clipping, loudness/true peak, silence gaps, A/V length, resolution/fps/codec,
letterboxing, caption safe zones, size limits. Watch the contact sheet end to end. FAIL → fix → re-QC.

**9. Deliver.** `video_export` per platform (reels/tiktok/shorts/youtube/…), `.srt`, thumbnail
(`video_thumbnail` + design), `stock_credits` → paste `credits.txt` into the description, editable
masters: `.kdenlive` (always written by `video_edit`) and `video_export_interchange`
(FCPXML/OTIO/EDL + HOW-TO-OPEN.md) when the client edits in Resolve/Premiere/FCP. Delivery note:
what's included, where, licences, what's approximate.

## Quality bar (non-negotiable)
- LOOK at every preview (shot sheets, storyboard, contact sheet, Kdenlive check, QC table) before
  showing the client; say what you checked.
- No jump in audio levels between shots; no music fighting the voice; no cut inside a word.
- Text never covers faces or on-screen text; captions inside the safe zone for the platform.
- Identifiable people in stock b-roll: rejected by default in ads/promos (no model release).
  No trademarks/logos of other brands in hero shots. Every stock item's licence is kept and credited.
- Never claim "done" while `video_qc` shows a FAIL. Say honestly what is approximate (beat
  downbeats, Whisper timings, keyless stock coverage).
- The client signs: treatment → rough cut → picture lock → final. Revisions are applied to the
  timeline JSON and re-rendered — never patched on the MP4.

## Hand-offs
- Scripts, hooks, ad cutdowns, YouTube structure → **reels-studio** first.
- Motion graphics beyond the built-in overlays → **motion-design-studio**.
- Footage/music/SFX sourcing and licences → **stock-library**.
- AI-generated cinematic shots → **flow-studio-director** (then back here for post).
- Brand kit, thumbnails, posts → **creative-studio**.
- Subtitles in other languages → **premium-subtitle-localization**.
