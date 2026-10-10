# Project packages — the same edit, editable in every pro app

Code: studio-mcp `src/studio/depts/video/nle/` (`doc.py` model · `gfx.py` native graphics · `luts.py` ·
`w_premiere.py` `w_ae.py` `w_resolve.py` `w_fcpxml.py` `w_capcut.py` `w_otio.py` · `package.py` · `guide.py`)
and `pro_package.py` (open in apps on the Mac). Tests: `tests/test_video_nle.py`.

## How it works
1. The render normalises the timeline (same object every writer reads), so the geometry (fit / zoom /
   focus / Ken Burns / overlay positions), transitions, J/L cuts, speed, levels and ducking are computed
   with the SAME maths as the MP4 — then converted to each app's units (Premiere: % of native size +
   centre offset; FCPXML: % of frame height, y up; CapCut: scale vs fit, half-canvas units; AE: pixels).
2. Motion graphics: the HTML page each graphic was rendered from is opened again, seeked to the moment
   it is fully on screen, and every element is read (text, font family/weight/size, colour, letter
   spacing, alignment, RTL, boxes, gradients, radii, images). Text → live text layers; shapes → AE shape
   layers or a transparent "plate" PNG in apps without vector shapes; the entrance/exit becomes a
   fade + rise. A side-by-side check image compares it with the render (score ≤ 12 = match).
   Only `motion_title_card` and `motion_lower_third` are rebuilt natively; overlapping-state graphics
   (CTA button swaps, counters, countdowns, reveals, kinetic text) stay rendered alpha clips.
3. Grades → one 33³ .cube per graded clip, baked from the exact ffmpeg colour chain (clip + programme
   grade); vignette is spatial and listed separately.
4. Captions → native text per chunk (same chunks/size/position/outline as the burned captions) + .srt/.vtt/.ass.
5. Blur-fill clips (fit=blur) → a pre-rendered blurred backdrop clip under the picture (CapCut: its own
   canvas blur). Colour cards → PNGs. Title cards stay on the picture track with the native version on top.
6. Media is copied into the package (hard-linked on the same disk); `project_media: "reference"` keeps
   the originals' paths instead.

## Per-app notes and limits
- **Premiere Pro**: FCP7 XML is Premiere's own interchange. Premiere has no XML text → graphics come in as
  the rendered alpha clips (enabled); editable versions via After Effects (Replace With After Effects
  Composition) or MOGRTs (`mogrts: true`, needs AE on the Mac). Lumetri LUTs are applied by hand
  (table in OPEN-IN.md) — Premiere's XML cannot carry them.
- **After Effects**: the builder is ES3 ExtendScript; it imports from paths relative to itself (no relink
  needed). Needs the fonts installed (Fonts/). AE can't take a LUT file by script → each graded layer gets
  a comment naming its LUT. Run: File › Scripts › Run Script File; or `video_project_open app=aftereffects`
  (osascript DoScriptFile — needs "Allow Scripts to Write Files").
- **Resolve**: free version — import FCPXML, install the Fusion titles with the .command, LUTs by hand.
  Studio — `build_resolve.py` (Python API; Studio-only since 21.1) or its built-in MCP server.
  Fusion Title text size is calibrated as size_px/H×0.94 — confirm on first use and adjust in `w_resolve.py`.
- **Final Cut Pro**: FCPXML 1.10 validated against Apple's DTD. Titles use Basic Title (font, size,
  colour, position). Transitions become Cross Dissolve. Rendered graphics on a disabled lane.
- **CapCut**: desktop 8.x drafts are plain JSON (JianYing 6+ drafts are encrypted — not supported).
  Transitions use CapCut's online "Mix/dissolve" effect (downloads on first open). Text size unit is
  calibrated as 0.4 % of the canvas height (`SIZE_UNIT` in `w_capcut.py`) — confirm on first use.
  Close CapCut before adding a draft (it rewrites its index on quit).
- **Avid / Pro Tools**: AAF via otio-aaf-adapter (`pip install otio-aaf-adapter pyaaf2`): picture, audio,
  dissolves; no graphics text, no keyframes.
- **Kdenlive / Shotcut**: the original writer, render-checked with melt.

## Verify before handing over
1. OPEN-IN.md "Checks that ran": every app ✅ (fix or explain any ⚠).
2. LOOK at `Projects/tracks.png` (every lane and clip) and `Media/Graphics/Native/check-*.png`.
3. When the user's apps are reachable and the user agrees: `video_project_open` in the app they use and
   look at the first frame of each graphic and one transition against the MP4.

## Verified so far
- Cloud: every writer's check (XML parse, FCPXML DTD, OTIO/FCP7/FCPX adapters read-back, AAF opens,
  AE builder dry-run in a mock AE, CapCut materials/overlaps, Fusion braces), LUT vs ffmpeg grade mean
  error < 1 level, native lower third vs render score 0.76, title card 6.3.
- Not yet opened in the real apps (first real job: open in Premiere + CapCut on the Mac and calibrate
  Premiere's centre units, CapCut's text size and Resolve's Text+ size).
