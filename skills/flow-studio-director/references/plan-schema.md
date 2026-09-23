# plan.json — field reference

Read by `scripts/shot_plan.py` (validation + pricing) and
`scripts/project_state.py` (planned credits, dependencies).

## Project level

| Field | Meaning |
|---|---|
| `project` | name |
| `platform` | `google-flow` (selects `references/platforms/<platform>/capabilities.json`) |
| `aspect_ratio` | `16:9` or `9:16` for video |
| `language` | BCP-47, e.g. `ar-EG`, `en-US` — sets the dialogue pace check |
| `budget_credits` | ceiling for the whole project (required for autopilot) |
| `audio_mode` | `native` (default: dialogue + SFX from the video model) |
| `voiceover` | `null`, or `{"provider": "gemini"|"elevenlabs"|"user", "voice": "Charon"}` |

## Characters (required whenever any shot has people or dialogue)

```json
"characters": [
  {"id": "HANA", "name": "Hana", "speaks": true, "flow_character": "Hana",
   "voice": "HANA_VOICE", "sheet": "chars/hana_sheet.png"}
]
```
| Field | Meaning |
|---|---|
| `id` | short upper-case id used in `cast` (names are accepted too) |
| `name` | as written in the script — dialogue `character` must match it |
| `speaks` | false for silent characters (no voice needed) |
| `flow_character` / `voice` / `sheet` | the built assets; `project_state.py` tracks their approval |

`voiceover_lines` (written by the breakdown) lists narration with its scene;
narration is generated off-screen (`voiceover.py`), never inside a shot.

## Per shot

| Field | Meaning | Checked by |
|---|---|---|
| `id` | unique, e.g. `S03` | duplicates are an error |
| `beat` | one line: what this shot is for | — |
| `model` | key from capabilities.json (`omni-1.1-flash`, `veo-3.1-lite`, `veo-3.1-fast`, `veo-3.1-quality`) | must exist |
| `mode` | `text`, `frames_first`, `frames_first_last`, `ingredients`, `video_edit`, `extend` | must be supported by the model |
| `duration` | seconds | must be offered by the model (and for ingredients) |
| `resolution` | `720p` / `360p` | must be offered |
| `outputs` | 1–4 (cost multiplies) | range |
| `keyframes` | `{"start": bool, "end": bool, "model": "nano-banana-2"|"nano-banana-pro"}` | frames modes require them |
| `ingredients` | names of Flow assets used (characters, voices, locations) — include the voice asset name for speaking characters (`HANA_VOICE`) | a name containing "voice" marks the shot as needing voice support |
| `dialogue` | `[{"character", "text", "start", "end", "interrupts"?}]` | pace per language, window ≥1.2 s, inside the clip, overlaps, ≤2 speakers |
| `interrupts` (on a line) | `true` if it deliberately overlaps the previous line | suppresses the overlap warning |
| `continuation` | `first_shot`, `hard_cut`, `keyframe_chain`, `ingredients`, `extend` | `keyframe_chain`/`extend` make the shot depend on the previous one being approved |
| `extends` | id of the clip an `extend` shot continues | must be an 8 s Veo 3.1 clip |
| `ends_on_stillness` | `true` if the shot ends on a hold (required before extending it) | warning if an extended clip lacks it |
| `characters_recurring` | `true` if a character who appears in other shots is in this one | warning on text-only routing (identity drift) |
| `large_move` | `true` if the subject/camera travels far between first and last frame | warning on first+last (morphing risk) |
| `draft_first` | `true` to price a 360p Omni test take before the real one | adds the draft cost |
| `cast` | character ids/names visible in this shot | must exist in `characters`; `project_state.py` blocks the shot until each is approved |
| `dialogue[].offscreen` | the speaker is heard but not seen (O.S.) | not required in `cast` |
| `transition_in` | `{"type": ..., "duration": s, "audio_offset": s}` — see `transitions.md` | type known; post transitions ≤ half the shorter clip; first shot only cut/fade; dialogue under a transition warned; match_cut needs a start keyframe; morph needs frames mode |
| `scene` | scene number from the breakdown | — |
| `routing_reviewed` | `false` on skeleton shots until the director routes them | warning while false |
