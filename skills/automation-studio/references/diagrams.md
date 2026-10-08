# Diagrams — show the automation before and after building

`auto.sh diagram <flow.json | plan.json> -o <dir> [--formats svg,png,pdf,html,mmd,excalidraw] [--title "…"]`

| Format | Use |
|---|---|
| `png` / `svg` / `pdf` | sign-off, proposals, handover documents (Graphviz, left→right, coloured by role) |
| `html` | interactive, self-contained page: zoom/pan, click a node → type, parameters, notes. Publish as an artifact for the client |
| `mmd` | Mermaid source for README/GitHub/Notion/Confluence; FigJam `generate_diagram` accepts Mermaid |
| `excalidraw` | editable whiteboard (excalidraw.com → Open); export to PNG/SVG for Miro/FigJam |

Colours: trigger green · action indigo · decision/loop amber · transform blue · code slate · AI magenta
(sub-nodes dashed with port labels: model / memory / tool / parser) · wait grey · output/response teal ·
error red · sub-workflow violet. IF edges labelled true/false, Switch edges with output names, loops "loop/done".

## Plan JSON (G2 — before choosing nodes or platform)
```json
{"title": "Lead intake",
 "steps": [
   {"id": "in",  "label": "New lead (website form)", "kind": "trigger", "app": "Tally"},
   {"id": "ok",  "label": "Valid email?",            "kind": "decision"},
   {"id": "crm", "label": "Create/Update contact",   "kind": "action",  "app": "HubSpot"},
   {"id": "ai",  "label": "Score lead 1–10",         "kind": "ai"},
   {"id": "hot", "label": "Score ≥ 8?",              "kind": "decision"},
   {"id": "sl",  "label": "Alert sales",             "kind": "action",  "app": "Slack"},
   {"id": "bad", "label": "Log invalid lead",        "kind": "error"}],
 "edges": [["in","ok"], ["ok","crm","yes"], ["ok","bad","no"], ["crm","ai"], ["ai","hot"], ["hot","sl","yes"]]}
```
kinds: trigger · action · decision · loop · transform · code · ai · ai_sub · wait · output · error · subflow · note.

## Whiteboards (when the connectors are available in the chat)
- **Miro**: render `svg`, then create the board content from the SVG (Miro canvas tools) or upload the PNG.
- **FigJam**: pass the Mermaid (`mmd`) to Figma's diagram generator.
- **Claude Whiteboard artifact type** (if listed): use for collaborative brainstorming of the process.
Always also give a PNG/PDF so the diagram survives outside the tool.

## Good diagram rules
One verb per box, app name small under it; ≤ 15 boxes per view (split into sub-workflow diagrams beyond);
every decision has labelled exits; show error/alert paths in red; put a legend in handover docs; keep node
names identical to the n8n node names so the client can find them.
