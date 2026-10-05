# Motion craft — the studio's rules

## Timing
- Read time: ~0.3 s per word + 0.5 s; never under 1.2 s for any text on screen.
- Entrances 0.4–0.8 s; exits faster (0.25–0.45 s) than entrances.
- Hold the final frame (logo/CTA) ≥ 1 s; reels end on the CTA, not on black.
- Reels/ads: a visual change every 1.5–3 s; first meaningful frame within 0.3 s (no slow fade-ins on frame 1).
- Long-form explainers: one beat per 4–8 s; let diagrams breathe.

## Easing (GSAP names in specs)
| Feel | In | Out |
|---|---|---|
| Corporate, calm | power2.out | power2.in |
| Modern, snappy | expo.out | expo.in |
| Playful | back.out(1.6) | back.in(1.4) |
| Bouncy / kids | elastic.out(1, 0.5) / bounce.out | power2.in |
| Cinematic | power3.inOut (slow) | power3.inOut |
Never linear for moves (only for constant rotation/marquee).

## Staging & hierarchy
- One focal point per moment; everything else waits or dims.
- Order of appearance = order of reading: kicker → headline → support → CTA.
- Overlap animations (start the next at 60–80% of the previous) — sequential feels slow.
- Camera: subtle push-in (2–6%) adds life; handheld only for energetic pieces.
- Motion blur on anything moving > 1/10 of the frame per frame (`motion_blur: 6–8`).

## Typography in motion
- Max 2 families (brand head + body); weights 800–900 for kinetic headlines.
- Kinetic: split by words (Arabic always by words), stagger 0.06–0.14 s, punch/rise styles.
- Emphasis: `*word*` → accent colour/highlight; one emphasis per line.
- Arabic: RTL, right-aligned blocks, line-height ≥ 1.4, Arabic digits only if the brand uses them.
- Safe areas: keep text inside 90% title-safe; on 9:16 leave the bottom 20% and the right 15%
  free of key text (platform UI).

## Colour & light
- Brand palette tokens (primary, accent, background, text, muted); dark stage + brand accent reads
  premium on social.
- Glow/light leaks/grain at low intensity (grain 3–6, vignette 0.25–0.4).
- Contrast ≥ 4.5:1 for text; test the darkest and brightest frames.

## Transitions
- Inside a piece, keep one transition family (e.g. all whips, or all shape wipes in brand colours).
- Cut on the beat; transitions 0.4–0.8 s; shape wipes cover the frame fully at the midpoint.

## 3D
- three.js for speed and stylised looks; Blender for photoreal materials and true DOF.
- Three-point studio light + environment reflections; camera moves slow (orbit 10–30° over the shot).
- Arabic 3D text is extruded from pre-shaped outlines — check joining in the key frames.

## Data
- Charts to scale (no truncated axes without saying so); label units; source line.
- Counters end on the exact number; prefix/suffix formatting per locale.

## Licences & ethics
- No third-party logos, characters or trademarks; no real people's likeness without consent.
- Lottie from LottieFiles: check each file's licence (Lottie Simple License is commercial-OK);
  keep attribution where required. Icons: Iconify set licence travels with the file.
- GSAP: free incl. commercial use (not for no-code builders that compete with Webflow).
- Remotion: free for individuals and organisations of ≤ 3 people; otherwise a company licence.

## QC before delivery
- Contact sheet start → end: no blank frames, nothing clipped, no flash at scene boundaries.
- Key frames at full size: text crisp, Arabic shaped, no overlaps.
- Alpha deliverables: check over checkerboard; edges clean; first/last frames transparent if intended.
- Duration and fps as requested; audio (if any) in sync with hits.
