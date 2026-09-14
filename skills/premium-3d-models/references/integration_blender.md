# Getting a generated model into Blender

## If Blender is open with its MCP addon running (live path)

Check this session's tool list for something like
`mcp__remote-devices__Blender__execute_blender_code` (name varies by
setup). If present, you can push the model straight into the user's open
Blender in a couple seconds instead of asking them to import it by hand:

1. Make sure the `.glb` is at a path Blender (running on their machine)
   can actually read — typically the connected project folder, not the
   cloud workspace.
2. Generate the import code:
   ```bash
   python3 scripts/blender_import.py -- /absolute/path/on/their/machine/model.glb "Bracket"
   ```
   (with no live Blender connection this just prints the snippet instead
   of running it — still useful to hand the user directly.)
3. Send that code as the `code` argument to the Blender execute tool.

The snippet only **adds** a new collection and imports into it — it never
touches or deletes anything already in their scene, so it's safe to run
against a file they have open with other work in it. It also switches the
viewport to Material Preview shading, since Blender's default Solid mode
ignores PBR materials entirely and the model would otherwise show up as
flat gray regardless of the color/metallic/roughness this skill set.

Check the result with a screenshot tool (e.g.
`get_screenshot_of_window_as_image`) rather than assuming it worked —
same "verify, don't just report" instinct as everywhere else in this
skill.

## If there's no live Blender connection (the normal case)

Just tell the user, in one line: open Blender, **File > Import > glTF
2.0 (.glb/.gltf)**, pick the file. That's genuinely the whole import —
Blender's built-in glTF importer reads the mesh, hierarchy, and PBR
materials correctly with zero extra steps.

If they want it scripted (e.g. as part of a batch/pipeline), hand them
`scripts/blender_import.py` and:

```bash
blender --background --python scripts/blender_import.py -- model.glb "My model"
```

or `blender yourfile.blend --python scripts/blender_import.py -- model.glb "My model"`
to import into an existing .blend non-interactively.

## After import: what's editable vs. what isn't

The imported mesh is a normal Blender object — bevel/subsurf modifiers,
further booleans, sculpting, UV work, all just work on it like anything
else in Blender. What doesn't carry over is this pipeline's *parametric*
history (you can't go back and "change the hole radius" the way you can
by editing the JSON spec and rebuilding) — for a dimension change, it's
faster to edit `model_spec.json` and regenerate a fresh `.glb` than to
hand-edit the imported mesh, unless the user has already started
Blender-native sculpting/detailing work on top of it that shouldn't be
thrown away.
