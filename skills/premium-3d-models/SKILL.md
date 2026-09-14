---
name: premium-3d-models
description: >
  Build real, parametric 3D models (.glb primarily, plus .stl/.obj on
  request) for any use case that ends up embedding, printing, or viewing
  3D geometry — a Flutter app's model_viewer_plus screen, a React/web
  page with model-viewer or react-three-fiber, a part imported into
  Blender for further work, or a file ready for a 3D printer. Use this
  whenever the user asks to "model," "3D model," "make a 3D object/part/
  asset of," or describes a mechanical part, product shape, prop, or
  sculptural object that should exist as real geometry rather than a 2D
  image. Two working styles this skill switches between: an "engineer"
  persona (exact dimensions, holes, tolerances, mechanical parts) and a
  "designer" persona (organic/sculptural silhouettes, materials, product
  form). If the use case or style is not obvious from the request, ask
  briefly (see Step 1) instead of guessing a persona or output format.
---

# Premium 3D Models

## Why this skill exists, and what it actually is

This is parametric CSG (constructive solid geometry) modeling: real
primitives (boxes, cylinders, spheres, revolves, extrusions) combined
with real boolean operations (union/difference/intersection), exported
as genuine, watertight, editable geometry. It is **not** an AI mesh/point
-cloud generator and it does not sculpt organic freeform shapes — that
honesty matters as much here as premium-presentations being upfront
about what its .pptx output can and can't animate. What this pipeline is
genuinely excellent at: mechanical parts, product forms, architectural/
prop geometry, anything built from clean geometric primitives and holes
— which is the large majority of "make me a 3D model of X" requests.

A model spec is one JSON file (same "structured source of truth" pattern
as premium-presentations' `deck_spec.json`) that `scripts/build_model.py`
turns into a `.glb` (+ optional `.stl`/`.obj`). The `.glb` is the
universal deliverable: it opens in Blender, embeds in Flutter via
`model_viewer_plus`, renders on the web via `<model-viewer>` or
react-three-fiber, and is what most AR viewers expect.

## Step 1: figure out persona, use case, and output

If the request already makes this obvious (e.g. "model a mounting
bracket with 4 screw holes, 60x30mm" is unambiguously engineer/mm/STL-
likely), skip straight to Step 2.

**If it's not obvious**, ask briefly, covering:

1. **What's it for?** Embedding in an app (Flutter/web), 3D printing,
   Blender/render work, or just "show me what it'd look like"? This
   decides the export formats (`glb` always; add `stl` only for
   printing) and whether dimensional accuracy matters.
2. **Engineer or designer persona** (see `references/personas.md`) — a
   precise mechanical part with real dimensions/tolerances, or an
   organic/sculptural object where proportion and material read matter
   more than exact numbers?
3. **Real dimensions**, if it's a part meant to fit/mate with something
   real — never guess a critical dimension the user didn't give you;
   flag it and ask, the same way premium-presentations flags a missing
   number instead of inventing one.
4. **If Blender is open on the user's device** (check this session's
   tools for something like `execute_blender_code` — see
   `references/integration_blender.md`), offer to push the model
   directly into their open Blender instead of just handing over a file.

Keep this to one focused round of questions — default sensible answers
(mm + engineer for anything with the word "bracket/mount/enclosure/part"
in it; cm + designer for "vase/sculpture/decorative/prop") for whatever
the user doesn't specify.

## Step 2: write the model spec

Read `references/model_spec_schema.md` before writing your first spec —
it documents every primitive (`box`, `sphere`, `cylinder`, `cone`,
`capsule`, `torus`, `ring`, `extrude`, `revolve`) and how booleans
(`union`/`difference`/`intersection`) chain them together.

Read `references/personas.md` too — it's short, and it's the difference
between a spec that reads as "a real engineered part" vs. "a designed
object," which is the whole point of asking about persona in Step 1.

Never invent a dimension that matters (a bolt-hole spacing, a wall
thickness meant to fit a real enclosure) — use what the user gave you,
or a stated engineering standard (e.g. "M3 clearance hole" = ~3.4mm
diameter — say that's what you used), and flag anything you had to
estimate.

## Step 3: generate

First time in an environment, check the dependencies exist before
assuming they do (`python3 -c "import trimesh, manifold3d, shapely"`) and
install from `scripts/requirements.txt` if not — none of these need a
compiler or GPU, they're all pure-Python/prebuilt wheels:

```bash
pip install --break-system-packages -r scripts/requirements.txt   # if missing
python3 scripts/build_model.py model_spec.json output_basename
# writes output_basename.glb (+ .stl/.obj per spec["export"])
```

## Step 4: validate and preview — before you hand it over

**Always run the validator — this is not optional**, same rule
premium-presentations has for `validate_deck.py`:

```bash
python3 scripts/validate_model.py output_basename.glb --platform mobile_ar
```

(`--platform` is optional — use `mobile_ar`, `web_realtime`, `game_asset`,
or `print`/`unlimited` if you want a poly-count budget check; omit it to
skip that check.) A non-manifold or inconsistently-wound mesh looks fine
in a quick glance and then fails silently in a slicer, a physics engine,
or an AR viewer — fix any reported error (almost always: operands in a
boolean don't actually overlap, or a primitive's segment count is too
low) and rebuild before delivering.

Then render an actual look at it — never ship a model you haven't looked
at:

```bash
python3 scripts/render_preview.py output_basename.glb preview.png --mode hero        # designer default
python3 scripts/render_preview.py output_basename.glb preview.png --mode multiview   # engineer default
python3 scripts/render_preview.py output_basename.glb preview.gif --mode turntable   # judge it in the round
```

Look at the image before delivering — check proportions read correctly,
holes/features are where they should be, and (for engineer parts) the
multiview sheet doesn't reveal a feature landed on the wrong face.

## Step 5: hand it over

Deliver the `.glb` (+ `.stl`/`.obj` if requested) and the preview
image/GIF. Then, based on Step 1's answer:

- **Flutter** → point at `references/integration_flutter.md` (the
  `model_viewer_plus` widget — a few lines of Dart, no manual 3D setup).
- **Web/React** → `references/integration_web.md` (`<model-viewer>` for
  the common case, react-three-fiber only if they need real scene
  control).
- **Blender** → `references/integration_blender.md`. If a live Blender
  connection is available this session, offer to import it directly into
  their open file rather than making them do it by hand.
- **3D printing** → hand over the `.stl`, note the units it's in, and
  mention wall-thickness/overhang concerns only if something in the spec
  looks genuinely printable-fragile (a wall under ~1mm, an unsupported
  overhang) — don't lecture on printing basics unprompted.

## Extending: new primitives or export formats

Primitives live in `scripts/primitives.py` (`make_primitive()` — add a
new `elif t == "..."` branch backed by a `trimesh.creation.*` call, apply
`apply_transform()` at the end like every other branch). Keep
`scripts/validate_model.py` in mind when adding a primitive with a new
failure mode (e.g. a shape that's easy to build self-intersecting) —
add a check there if a new primitive can produce a broken mesh in a way
the existing watertight/winding checks won't already catch on their own
(they usually will, since those are properties of the *result* mesh, not
the primitive type).

## What this skill won't do (be upfront about these, same as
premium-presentations is about animation limits)

- **No true parametric fillets/chamfers.** Mesh-level CSG doesn't have a
  B-rep kernel's "round this edge by 2mm" operation. State this plainly
  if asked, and point at finishing in Blender (bevel modifier) or a real
  CAD tool afterward.
- **No organic/freeform sculpting.** This is primitives + booleans, not
  a digital-sculpting tool — a stylized geometric object is well within
  reach, a realistic organic creature/character is not.
- **No AI-generated mesh from a text description of an unknown shape**
  (photogrammetry-style "generate a dragon" from words alone) — this
  pipeline builds *exactly* what the spec's geometry describes,
  parametrically. If the user wants that kind of generative 3D, say so
  plainly rather than attempting a crude primitive approximation and
  calling it what they asked for.
- **No `.usdz`** (needed for iOS Quick Look AR specifically) — see the
  note in `references/integration_flutter.md`.
