# Engineer vs. designer persona

The spec's `"persona"` field doesn't change what `build_model.py` runs —
it changes how *you* (the model-builder) should think about the spec
before you write it, and which preview mode to reach for. Ask the user
which one fits if it's not obvious from the request (a "bracket",
"enclosure", "mounting plate", or anything with holes/tolerances screams
engineer; a "vase", "sculpture", "abstract shape", or "stylized icon"
screams designer) — same "ask before guessing" instinct
premium-presentations uses for visual themes.

## Engineer persona

The point is **correctness**: exact dimensions, holes that line up,
walls that are the thickness you said, a part that will actually
assemble with the real-world thing it's meant to mate with.

- Work in real, meaningful units (`"units": "mm"` is the sane default for
  mechanical parts) and use exact numbers the user gave you — never round
  a stated dimension "to make the math easier."
- Build holes/slots as `difference` operations, not by eyeballing a gap.
  If the user says "M3 bolt holes," that's a 3.2-3.4mm clearance hole
  (M3 nominal + typical clearance) — say which clearance you used.
  If they say "press fit" or "tap directly," ask which they mean rather
  than guessing a tolerance that could make the printed/machined part
  useless.
- Default preview mode: `multiview` (the 2x2 orthographic iso/front/top/
  right sheet) — proportions and hole placement across faces are the
  thing to check, not a pretty hero angle.
- Default export: `glb` + `stl` (STL is what a slicer wants for 3D
  printing; ask if the part is actually headed for a printer/CNC vs. just
  a visual/Blender/web use, since that changes whether STL is needed).
- Material defaults toward a neutral, informative finish (e.g. a light
  metallic gray, `metallic: 0.6-0.8, roughness: 0.3-0.4`) unless the user
  specifies a real material/finish — the model should read as "a
  technical part," not "a rendered product shot," unless asked.
- Be upfront about this pipeline's real limit: no true parametric
  fillets/chamfers (see `model_spec_schema.md`'s last section). If a
  design needs a genuine rounded edge for stress or fit reasons, say so
  and point at finishing it in Blender/FreeCAD/Fusion 360 after.

## Designer persona

The point is **how it reads**: silhouette, proportion, material feel,
whether it looks intentional from every angle a viewer will actually see
it from.

- Units matter less than proportion — pick something sane (`cm` is a
  comfortable working scale for most objects a hand would hold or a room
  would contain) and don't sweat exact millimeters unless the user cares.
- Lean on `revolve` (vases, bottles, knobs, anything with rotational
  symmetry) and `extrude` (flat emblem/icon/sign shapes) — these read as
  far more "designed" than a pile of boxes and spheres. Compose multiple
  primitives with real proportion relationships (a base, a body, a neck,
  an accent) rather than one blobby shape.
- This pipeline doesn't do organic sculpting (no soft-body push/pull,
  no subdivision-surface freeform modeling) — it's parametric primitives
  and CSG, which covers "designed object with clean geometric language"
  far better than "organic creature/character," and that's an honest
  boundary to state rather than attempt and disappoint.
- Default preview mode: `hero` (one well-lit 3/4 view), and offer a
  `turntable` GIF — designed objects are judged in the round, and seeing
  it spin catches an angle that reads badly before the user does.
- Materials are half the design: don't leave them at the neutral default.
  Pick metallic/roughness/color that matches the brief (a `roughness:
  0.05-0.15` with `metallic: 0.9+` for chrome/steel, `roughness: 0.4-0.6,
  metallic: 0` for matte plastic/ceramic, low `opacity` + low `roughness`
  for glass) and say what you chose and why, same as premium-presentations
  explains a theme choice.
- Export: `glb` only, almost always — designer pieces are for viewing
  (web/AR/Flutter/Blender render), not printing, unless the user says
  otherwise.
