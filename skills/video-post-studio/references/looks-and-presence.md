# Looks, presence and layout precision (motion graphics inside edits)

Read this before any video that has motion graphics. Three problems it exists to prevent:
every video looking the same, the speaker being hidden or cropped, and graphics whose text touches edges.

## 1. Looks — a different design every video
A **look** is a whole visual identity: palette, Latin + Arabic fonts, corner/border/shadow style,
background decoration, easing personality and the layout variant each template uses.
`motion_looks` lists the 12 looks: neon_grid, editorial_ink, sunset_pop, brutal_yellow, emerald_gold,
swiss_mono, candy_glass, sport_heat, ocean_calm, retro_tape, blueprint, rose_studio.

- Every `motion_*` tool takes `look`: an id, `auto` (default) or `none`. `auto` never repeats one of the
  last 6 looks and never repeats the same layout variant twice in a row for a template. The history lives
  in `STUDIO_HOME/state/motion-looks.json`.
- ONE look per video. In `video_edit` the timeline picks it once (`"look": "<id>"` or auto) and every
  overlay/title uses it. For separate `motion_*` calls that belong to one video, pass the same `look=<id>`
  (or the same `project=`). The result's `data.look` / `data.style` and a warning tell you what was chosen.
- Choose by mood when the client gave one (see `mood` in `motion_looks`): tech → neon_grid/blueprint,
  luxury → emerald_gold/rose_studio, sport → sport_heat, kids/food → sunset_pop, news → editorial_ink…
  Otherwise leave `auto` — the point is variety. Never answer "make another one" with the same look.
- With `brand=<slug>` the brand keeps ITS colours and fonts; the look then changes layout, shapes, motion.
- Explicit `style=` (modern/glass/line/tag/stamp, bold/minimal/split/frame/poster, punch/stack/type…) wins over the look.
- `motion_compose template=…` also rotates looks; hand-written specs take `look=` only when asked.

## 2. The speaker stays on screen (`video_edit` presence guard)
- Graphics are placed in the FREE region next to the face (right/left/top/bottom/center for 16:9,
  top/middle/bottom for 9:16), never over it. `placement` per overlay: `auto | full | <region> | [x,y,w,h]`.
  Overlays placed over footage get a soft card (`scrim`, 0–0.8) in the look's background colour so text stays readable.
- Full-frame graphics only when the viewer must not see the speaker (logo reveal, title card, chapter card):
  ≤ 15 % of the video, ≤ 3.5 s each. Speaker visible ≥ 65 % of the time, no gap longer than 4 s —
  `data.presence` and the `-presence.png` strip report it after the render. A budget warning means re-plan.
- Picture-in-picture / avatar: shape defaults to a rounded card; `circle` only if the head fits (the crop is
  face-aware: head box + margin, face at ~47 % height). Width ≥ 36 % (portrait) / 26 % (landscape). If the
  source is too tight for a circle it falls back to rounded and says so — never a face cut in half.
- `video_presence`, `video_face_frame`, `video_free_regions` let you inspect before rendering.

## 3. Precise graphics (layout audit — automatic)
Every motion render is measured in the page: text vs frame edge (≥ 3.5 % of the short side), text inside its
circle/ring/pill/box (counters in rings!), clipped text, overlapping text, tiny type. Fixable errors are
auto-scaled and re-rendered; `data.layout_audit` and `warnings` list what was fixed. **Never deliver
with a `LAYOUT ERROR` left** — shorten the text, enlarge the container, or change the layout, then re-render.
For hand-built compose specs: counters in rings use width ≤ 0.66 × ring diameter; put text in containers with
`data-audit` opt-outs only for decorative layers.
