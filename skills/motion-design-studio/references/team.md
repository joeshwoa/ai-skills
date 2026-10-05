# Motion team — sign-off checklist per role

**Creative director** — one message per piece; the feeling in 3 words; approves style frames and
the final; kills anything that doesn't serve the message.

**Art director** — brand kit applied (`brand=<slug>`), max 2 type families, palette tokens only,
grid and safe areas (9:16: bottom 20% and right 15% free of key text), contrast ≥ 4.5:1.

**Technical director** — `motion_plan` for every new job; engine choice written in the delivery note
with the reason; resolution/fps/alpha/codec per deliverable; render time estimate before long renders
(Blender, motion blur); offline readiness (JS libs cached).

**Motion designer / animator** — timing (read time, holds), easing per brand, staging (one focal
point), overlaps, transitions from one family, camera subtle; uses `id` + `below/above` stacking.

**Typographer** — hierarchy kicker → headline → support; Arabic by words, RTL, line-height ≥ 1.4;
no orphan words on the last line of a headline; emphasis once per line.

**3D artist** — material and light that suit the brand (gold/metal premium, plastic playful, glass
tech); camera move slow; check Arabic joining on extruded text; three.js for speed, Blender for
photoreal; the `.blend` delivered when Blender was used.

**Illustrator / vector** — clean SVGs (no embedded rasters when animating draw/morph), icons from
`stock_icon` with their set licence, Lottie recoloured to the brand.

**Data-viz designer** — numbers exact, axes honest, units and source line, counters land on the
exact value.

**Sound designer** — hits on text punches, whoosh on transitions, riser into reveals, a logo
"sting" sound; mixed under VO (−18…−12 dB); music cut to the beat.

**Render wrangler / QC** — preview (12 stills) before every full render; contact sheet + key frames
LOOKED at; alpha over checkerboard; duration/fps/size as asked; files + editable masters listed with
paths.
