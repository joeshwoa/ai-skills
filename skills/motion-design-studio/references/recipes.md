# Recipes — tested specs (in `examples/`)

Run: `bash scripts/call.sh motion_compose @examples/<file>.json` (add `"preview": true` to iterate).

| File | What | Engine |
|---|---|---|
| `examples/kinetic_hook_ar.json` | Egyptian-Arabic kinetic hook, word punches + highlight, 9:16 | compose template kinetic_quote |
| `examples/explainer_scene.json` | 2-scene explainer: stacked kicker/headline/icon → animated bar chart with callout | compose spec (shows `id` + `below` stacking) |
| `examples/logo_sting.json` | brand logo sting: rings, bursts, draw-on, shine, tagline | compose template logo_sting_pro |
| `examples/title_3d.json` | Arabic gold 3D title with orbit camera | `motion_3d` (`call.sh motion_3d @examples/title_3d.json`) |

## Patterns
- **Reel hook (0–2 s):** kinetic_quote with 2–4 beats, `emph_style: highlight`, then cut to footage.
- **Lower thirds for an interview:** `motion_compose template=lower_third_pro` (alpha) → overlay in the
  video_edit timeline at each new speaker.
- **Product promo:** `social_promo` (headline, product image, ≤4 features, price, CTA, logo). For an
  app: `app_promo` with real screenshots.
- **Data story:** `chart_story` (data, highlight, annotation, takeaway, source) or a `chart` layer.
- **Brand opener/closer:** `logo_sting_pro` (2D) or `motion_3d preset=logo` / `motion_blender preset=logo`.
- **Transitions for an editor:** `transition_pro` (alpha MOV, cut at the midpoint) → timeline overlays.
- **Designer's Lottie:** `motion_lottie {"src": "anim.json", "recolor_mode": "brand", "brand": "<slug>", "transparent": true}`.
- **Custom anything:** write HTML/CSS/GSAP and `motion_render_html` (frame-exact, alpha).

## Spec snippets
Stack text on measured heights (never guess y for wrapped lines):
```json
{"type": "text", "id": "head", "text": "…", "y": "45%", "w": 1500},
{"type": "text", "text": "kicker", "above": "head", "gap": 30},
{"type": "text", "text": "subline", "below": "head", "gap": 40}
```
Scene transition + camera beat bumps:
```json
{"duration": 3, "transition": {"type": "whip", "duration": 0.5}, "camera": {"preset": "push-in", "amount": 0.06, "punch": [0.8, 1.6]}}
```
Motion blur on a fast scene (final render only): top-level `"motion_blur": 8`.
