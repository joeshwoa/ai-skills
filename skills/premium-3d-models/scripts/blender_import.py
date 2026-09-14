#!/usr/bin/env python3
"""
blender_import.py — generates a short bpy snippet that imports a generated
.glb into Blender, cleanly organized into its own collection.

Why generate an *import* script instead of rebuilding the geometry from
scratch with bpy.ops primitives: the .glb built by build_model.py is
already the exact, correct, validated geometry (booleans resolved,
materials assigned). Blender's own glTF importer reads PBR materials,
node names, and mesh data reliably — re-deriving equivalent bpy.ops calls
would risk subtly different geometry (different boolean engine, different
primitive parameterization) from the file everyone else is looking at.
Import, don't reconstruct.

Two ways to use this:
  1. This session has live Blender MCP tools connected (check for tools
     named like execute_blender_code) — call print_snippet() and run that
     code directly via that tool. The model appears in the user's actual
     open Blender in a couple seconds.
  2. No live Blender connection — hand the user the .glb and this
     standalone script:
         blender --background --python blender_import.py -- model.glb
     or just tell them: File > Import > glTF 2.0 (.glb/.gltf), pick the
     file. That's genuinely all it takes; this script only adds the
     "organize into a named collection + frame the view" niceties.
"""
import sys


def snippet(glb_abspath: str, collection_name: str = "Imported model") -> str:
    """Returns a bpy code string ready to paste into Blender's Python
    console, run via `blender --background --python`, or send straight to
    a live Blender MCP execute_blender_code call."""
    glb_abspath = glb_abspath.replace("\\", "\\\\").replace('"', '\\"')
    collection_name = collection_name.replace('"', "'")
    return f'''import bpy

GLB_PATH = "{glb_abspath}"
COLLECTION_NAME = "{collection_name}"

# Track what exists before import so we can move only the new objects.
before = set(bpy.data.objects.keys())

bpy.ops.import_scene.gltf(filepath=GLB_PATH)

new_objects = [obj for name, obj in bpy.data.objects.items() if name not in before]

collection = bpy.data.collections.get(COLLECTION_NAME) or bpy.data.collections.new(COLLECTION_NAME)
if collection.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(collection)

for obj in new_objects:
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection.objects.link(obj)

# Frame the new objects in the viewport, and switch to Material Preview
# shading so the PBR colors/metallic/roughness are actually visible
# (the default Solid shading mode ignores materials entirely).
for obj in new_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = new_objects[0] if new_objects else None
for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type == "VIEW_3D":
        for space in area.spaces:
            if space.type == "VIEW_3D":
                space.shading.type = "MATERIAL"
        with bpy.context.temp_override(area=area):
            bpy.ops.view3d.view_selected()

print(f"Imported {{len(new_objects)}} object(s) into collection '{{COLLECTION_NAME}}'.")
'''


def main():
    args = sys.argv[1:]
    if "--" in args:
        args = args[args.index("--") + 1:]
    if not args:
        print("Usage: blender --background --python blender_import.py -- model.glb [\"Collection Name\"]")
        sys.exit(1)
    glb_path = args[0]
    name = args[1] if len(args) > 1 else "Imported model"
    code = snippet(glb_path, name)
    try:
        import bpy  # noqa: F401 — only present when actually running inside Blender
        exec(compile(code, "<blender_import_snippet>", "exec"), {})
    except ImportError:
        # Not running inside Blender — just print the snippet so it can be
        # pasted into Blender's own Python console, or piped to a live
        # Blender MCP execute_blender_code call.
        print(code)


if __name__ == "__main__":
    main()
