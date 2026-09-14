# Model spec schema

A model spec is one JSON file `build_model.py`, `validate_model.py`, and
`render_preview.py` all work from — the same "one source of truth" pattern
`premium-presentations` uses for `deck_spec.json`.

```json
{
  "meta_name": "Mounting bracket",
  "persona": "engineer",
  "units": "mm",
  "export": {"glb": true, "stl": true, "obj": false},
  "parts": [ ... ],
  "output": ["bracket"]
}
```

- `persona`: `"engineer"` or `"designer"` — see `references/personas.md`. Mostly
  affects *how you write the spec* (precise dimensioned parts vs. sculpted
  organic forms) and which preview mode to default to
  (`multiview` vs. `hero`), not anything build_model.py branches on.
- `units`: `mm` | `cm` | `m` | `in`. Every number in `parts` is in this
  unit. It matters at export time: **the `.glb` is always rescaled to
  meters** (glTF's spec unit — get this wrong and the model is a speck or
  a skyscraper in web/AR/Flutter viewers), while `.stl`/`.obj` keep the
  raw numbers (those formats carry no unit metadata; slicers and Blender's
  raw import conventionally just assume "your working unit", usually mm).
- `export`: which files to write. `glb` is virtually always wanted (it's
  the one universal format for web/Flutter/Blender). Add `stl` for 3D
  printing, `obj` if a specific tool needs it.
- `output`: which part `id`s become visible geometry in the exported
  file. Anything not listed is treated as a helper (e.g. the cylinders you
  subtract to make holes) and silently excluded — it did its job as a
  boolean operand and doesn't need to exist in the final file.

## `parts`: a CSG build list

Each entry is either a **primitive** or a **boolean operation**, and later
entries can reference the `id` of any earlier entry. Order matters — this
is a dependency list, not an unordered bag.

### Primitives

Every primitive accepts optional `translate: [x,y,z]`, `rotate_deg: [x,y,z]`
(Euler, applied X then Y then Z), and `scale: [x,y,z]` (or a single number
for uniform scale) — applied in that order (scale, then rotate, then
translate) right after the shape is created.

| type | params | notes |
|---|---|---|
| `box` | `size: [x,y,z]` (or one number for a cube) | centered at origin |
| `sphere` | `radius`, `segments?` (default 32) | UV sphere |
| `cylinder` | `radius`, `height`, `sections?` (default 48) | axis = Z, centered |
| `cone` | `radius`, `height`, `sections?` | apex up on +Z |
| `capsule` | `radius`, `height` | a cylinder with hemispherical caps |
| `torus` | `major_radius`, `minor_radius`, `major_sections?`, `minor_sections?` | a ring donut |
| `ring` | `r_min`, `r_max`, `height` | a flat washer/annulus |
| `extrude` | `polygon: [[x,y],...]`, `height`, `holes?: [[[x,y],...], ...]` | a flat 2D shape pushed up into a solid — signs, logos, flat brackets, gaskets |
| `revolve` | `profile: [[x,y],...]`, `angle_deg?` (default 360), `sections?` | spins a 2D profile around the Z axis — vases, bottles, wheels, knobs |

> **`revolve` profiles**: `x` is radius (must be >= 0), `y` is height. For
> a **hollow vessel** (a real vase/bottle, not a solid blob), trace the
> full wall cross-section as one loop: up the outside, across the lip,
> back down the inside, across the base — not just the outer silhouette.
> `build_model.py` auto-closes the loop back to the first point for a
> full 360° revolve, so you don't need to repeat the first point
> yourself, but the profile still needs to actually trace a sensible
> closed wall shape (see `examples/designer_vase.json` for a full worked
> hollow-vessel profile).

```json
{"id":"base","type":"box","params":{"size":[40,20,5]}}
{"id":"hole1","type":"cylinder","params":{"radius":2.5,"height":10},"translate":[-10,-5,0]}
{"id":"knob","type":"revolve","params":{"profile":[[0,0],[8,0],[8,2],[3,4],[3,20],[0,20]]}}
```

### Booleans

```json
{"id":"bracket","type":"difference","base":"base","subtract":["hole1","hole2","hole3","hole4"],
 "material":{"color":"#C9A96A","metallic":0.6,"roughness":0.35}}
```

- `type: "union"` — `parts: [id, id, ...]` — merges shapes into one.
- `type: "difference"` — `base: id`, `subtract: [id, ...]` — cuts holes/
  pockets. This is the one you'll use constantly (every hole, slot, or
  cutout is a difference).
- `type: "intersection"` — `parts: [id, id, ...]` — keeps only the
  overlap. Good for trimming a shape to a bounding volume.

Booleans use the `manifold3d` engine — robust, no external binary, and it
produces a genuinely watertight result when the inputs are watertight and
actually overlap. **If a boolean fails or produces an empty mesh**, the
almost-always cause is the operands don't actually intersect (check
`translate` values) or a cylinder/sphere segment count is so low the
"round" shape doesn't fully punch through a flat face.

## Materials

Any primitive or boolean-result part can carry a `material` — it only
matters for parts listed in `output` (a hidden helper's material is never
seen). This maps directly to glTF's PBR material model, so it's exactly
what Blender/three.js/model-viewer/Flutter all render the same way:

```json
"material": {"color":"#C9A96A","metallic":0.6,"roughness":0.35,"opacity":1.0,"emissive":"#000000"}
```

- `color`: hex. The base color.
- `metallic`: 0 (plastic/wood/stone — dielectric) to 1 (bare metal).
- `roughness`: 0 (mirror-polished) to 1 (fully matte/chalky).
- `opacity`: 0-1, for glass/translucent parts (also set a low `roughness`
  for convincing glass).
- `emissive`: hex, for a part that should glow (an indicator light, a
  screen) — leave unset for normal parts.

No `material` at all is fine — you get a neutral default gray, useful for
a pure form/proportion check before you've decided on finish.

## A complete example — mounting bracket (engineer persona)

```json
{
  "meta_name": "4-hole mounting bracket",
  "persona": "engineer",
  "units": "mm",
  "export": {"glb": true, "stl": true},
  "parts": [
    {"id":"base","type":"box","params":{"size":[40,20,5]}},
    {"id":"hole1","type":"cylinder","params":{"radius":2.5,"height":10},"translate":[-15,-7,0]},
    {"id":"hole2","type":"cylinder","params":{"radius":2.5,"height":10},"translate":[15,-7,0]},
    {"id":"hole3","type":"cylinder","params":{"radius":2.5,"height":10},"translate":[-15,7,0]},
    {"id":"hole4","type":"cylinder","params":{"radius":2.5,"height":10},"translate":[15,7,0]},
    {"id":"bracket","type":"difference","base":"base",
     "subtract":["hole1","hole2","hole3","hole4"],
     "material":{"color":"#C9A96A","metallic":0.7,"roughness":0.3}}
  ],
  "output": ["bracket"]
}
```

See `examples/engineer_bracket.json` and `examples/designer_vase.json` for
two full worked specs (one mechanical/precise, one organic/sculptural).

## What this pipeline is *not*

Being upfront about limits, same spirit as premium-presentations' honesty
about animation limits: this is mesh-level CSG, not a full B-rep CAD
kernel. It does **not** have true parametric fillets/chamfers (a smooth
rounded edge across an arbitrary boolean seam) — if a design absolutely
needs that, build it in Blender (bevel modifier) or a real CAD tool
(Fusion 360, FreeCAD) after importing the `.glb`/`.stl` this pipeline
produces as a starting point. What this pipeline is genuinely good at:
exact parametric primitives, booleans (holes, slots, pockets), extrusions,
and revolves — which covers the large majority of "model me a part/prop/
object" requests without needing a CAD license or GPU.
