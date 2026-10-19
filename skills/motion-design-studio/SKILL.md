---
name: motion-design-studio
description: A professional motion-graphics studio the AI runs itself on free engines (the user's studio-mcp) — After Effects / Cinema 4D-level work in Arabic and English. Full team: creative director, art director, motion designer/animator, typographer, 3D artist, illustrator, data-viz designer, sound designer and technical director, with an engine router that picks the best engine per job: GSAP compositions (40 animation presets, 12 transitions, camera moves, charts, motion blur), Lottie, three.js real-time 3D, Blender (Cycles/EEVEE), and Remotion when licensed. Kinetic typography, logo animations and stings, title sequences, lower thirds, social promos, app promos, explainer and infographic animation, animated charts, map routes, 3D titles and product turntables, transitions, CTAs and captions, with alpha output for editors. Use for any request to animate, make motion graphics, an intro/outro, a logo animation, a title, an animated post or ad, an explainer animation, 3D text, or "make it move" — even when no tool is named.
---

# Motion Design Studio

A motion-graphics studio in one skill, on the user's MCP server **studio-mcp**
(github.com/joeshwoa/studio-mcp — same server as creative-studio). Every render is frame-exact
(a virtual clock drives every animation), and every result comes with a timecoded contact sheet
and full-size key frames that the studio LOOKS at before anything is shown to the client. Every
piece also leaves an editable master: the spec JSON + standalone GSAP HTML, the `.blend`, or the
Lottie file.

Paths are relative to this skill's folder (`skills/motion-design-studio/` in the ai-skills repo).

## Setup
Shared environment with creative-studio — install once:
```bash
bash ../creative-studio/scripts/bootstrap.sh
bash scripts/selftest.sh            # router, a compose preview, a template render, a 3D still
```
Call: `bash scripts/call.sh <tool> '<json>'` or `@spec.json`; `call.sh help motion_compose`.
JS libraries (GSAP + all plugins, lottie-web, three.js, d3) download once into STUDIO_HOME and then
work offline. Blender is optional (`studio_install {"group": "apps"}` after the user agrees); without
it `motion_blender` falls back to three.js and says so. Remotion needs Node and a licence check.
References: `references/tools.md` (every argument), `references/engine-reference.md` (spec format,
presets, engines, measured speeds), `references/team.md`, `references/craft.md` (animation
principles and house rules), `references/recipes.md`.

## The team
| Role | Owns |
|---|---|
| Creative director | the idea, the feeling, one message per piece, approves style frames |
| Art director | palette (brand kit), type, layout grid, safe areas, composition |
| Technical director | engine choice (`motion_plan`), render settings, performance, deliverable formats/alpha |
| Motion designer / animator | timing, easing, staging, transitions, camera — the spec |
| Typographer (kinetic type) | type hierarchy, Arabic/Latin pairing, word-by-word rhythm, readability |
| 3D artist | three.js / Blender scenes: materials, lights, camera, depth of field |
| Illustrator / vector | SVG assets, icons (`stock_icon`), shapes, Lottie sourcing/recolouring |
| Data-viz designer | charts and counters that are true to the numbers |
| Sound designer | hits, whooshes, risers in sync with the animation (`audio_sfx`, music on the beat) |
| Render wrangler / QC | previews, key frames, timing check, alpha check, final formats |

## Choosing the engine (`motion_plan` does this — read its reasons)
| Job | Engine | Tool |
|---|---|---|
| Kinetic type, titles, lower thirds, social posts/promos, UI/app promos, infographics, charts, 2D logo animation, transitions | **GSAP composition** (default) | `motion_compose` (spec or `template=`) |
| An animation a designer made in After Effects (Bodymovin) or from LottieFiles | **Lottie** | `motion_lottie` (recolour to brand, retime, alpha) or a `lottie` layer inside compose |
| 3D text/logo, product turntable from .glb, device mockup with a screen recording, particles — fast | **three.js** | `motion_3d` (or a `3d` layer in compose) |
| Photoreal 3D: glass, metal, caustics, real depth of field & motion blur, hero logo, long render OK | **Blender** | `motion_blender` (writes the `.blend`) |
| An existing Remotion (React) project, or data-driven batch videos in React | **Remotion** | `motion_remotion` — only if the user's organisation is ≤ 3 people or has a Remotion company licence (`licence_ok=true`) |
| A quick standard overlay (title card, lower third, logo reveal, CTA, countdown, counter) | built-in templates | `motion_title_card`, `motion_lower_third`, `motion_logo_reveal`, `motion_cta`, … |
| Anything custom in raw HTML/CSS/canvas | power tool | `motion_render_html` |

Speed guide (2-CPU sandbox; the Mac is faster): compose ≈ 30 s for 7 s at 720p; three.js ≈ 0.6 s
per frame; Blender Cycles ≈ 20 s per frame draft. Iterate with `preview: true` (12 stills) and
720p, render the final at 1080p (4K only when asked).

## Workflow (gates)
1. **Brief** (creative director): message, audience, language, platform + ratio(s), length, brand
   (`brand=<slug>`), style references, deliverable (MP4 / alpha MOV for an editor / GIF / Lottie).
   Numbered options with one RECOMMENDED; short Arabic questions.
2. **Plan** (technical director): `motion_plan {"brief": "…", "size": "9:16", "duration": 12, "arabic": true}`
   → engine + reasons + spec skeleton. For multi-part jobs, plan each part.
3. **Style frames** (art director): render `preview: true` (or a template with the real copy) and
   LOOK at the stills: hierarchy, contrast, safe areas, Arabic shaping and direction, nothing
   clipped or colliding. Show 1–2 style frames to the client before full animation.
4. **Animate** (motion designer, typographer, 3D artist): write/adjust the spec — timing, easing,
   staging, transitions, camera. Use `id` + `below/above` + `gap` to stack text on measured heights
   (never guess y for wrapped/Arabic lines). Render 720p; LOOK at the contact sheet and key frames;
   fix; repeat until it's right.
5. **Sound** (sound designer): SFX on hits/transitions, music on the beat (`video_beats`), mixed in
   the video-post-studio pipeline or `audio_mix`.
6. **Final render** (render wrangler): 1080p (or 4K), `motion_blur: 6–8` for fast moves, formats per
   use: MP4 for social, ProRes 4444 `.mov` / WebM alpha (`transparent: true`) for overlays, GIF for
   chat. Check the last frame and the alpha over checkerboard.
7. **Deliver**: files + editable masters (spec JSON + `-source.html`, `.blend`, Lottie) + what's
   approximate. Hand to video-post-studio when it goes into an edit.

## House rules (from `references/craft.md`)
- One idea per scene; read time ≥ 1.5 s for 3–5 words; hold the final frame ≥ 1 s.
- Ease everything (no linear moves except constant spins); overshoot only for playful brands.
- Stagger 0.04–0.12 s per word; Arabic animates by WORD (never letters); RTL layouts mirror.
- Never invent copy: if a template needs text the client didn't give, ask or leave it out.
- Brand colours from the kit; contrast ≥ 4.5:1 for body text; safe areas per platform.
- No third-party logos/characters; Lottie and icons keep their licence (Iconify sets, LottieFiles
  licence); GSAP is free incl. commercial (not for no-code builders competing with Webflow).
- LOOK before you show: contact sheet + key frames every render. Say what you checked.

## Looks, presence and precision (read `references/looks-and-presence.md`)
- Designs must differ video to video: every `motion_*` tool takes `look=<id>|auto|none` (`motion_looks`
  lists 12 identities; `auto` rotates, never repeating the last 6). One look per video — pass the same `look`
  to all its pieces. Don't answer "another design" with the same look or layout variant.
- Graphics never hide the speaker: placed in the free region beside the face with a soft card; full-frame
  only for logo/title moments (≤ 15 % of the video, ≤ 3.5 s each). PiP/avatar crops are face-aware.
- Graphics are measured after build (edges, circles/rings, boxes, clipping, overlap). Never deliver with a
  `LAYOUT ERROR`; fix the copy/size and re-render.

## Hand-offs
Scripts/hooks → reels-studio · editing, sound, captions, delivery → video-post-studio · stock
footage/icons/music → stock-library · brand kit → creative-studio · cinematic AI shots →
flow-studio-director.
