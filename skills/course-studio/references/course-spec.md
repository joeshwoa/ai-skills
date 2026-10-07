# course_spec.json — reference

```json
{"course": {...}, "modules": [{"id": "M1", "title": "...", "summary": "...", "outcomes": ["LO1"],
                               "sessions": [ {...}, {...} ]}]}
```

## course
| Key | Meaning |
|---|---|
| `title`, `subtitle`, `code`, `description` | names and the 2–3 sentence promise of the course |
| `language` | `ar` / `en` — documents' language (Arabic → RTL everything) |
| `slides_language` | language of the slides if different (e.g. English slides, Arabic notes) |
| `theme` / `brand` / `icon_set` / `cover_image` / `cover_style` | look (default unbranded) |
| `org`, `instructor`, `date`, `start_date` (YYYY-MM-DD), `days_between_sessions` | schedule dates |
| `audience` | {context: school·university·academy·corporate·online, school, grade, age, level, size, description} |
| `duration` | {sessions, minutes, weeks} |
| `mode`, `prerequisites`, `tools`, `materials`, `policies` | lists/strings |
| `outcomes` | [{id: "LO1", text, bloom}] — 3–8, measurable |
| `assessment` | [{name, weight (0–1, sum = 1), outcomes, description, max (score in the gradebook)}] |
| `rubrics` | [{title, levels: [...], criteria: [{name, weight, descriptors: [...one per level]}]}] |
| `students` | optional names for the gradebook (else numbered rows of audience.size) |
| `pass_mark` | percent (default 50) |

## session
| Key | Meaning |
|---|---|
| `id`, `title`, `minutes`, `summary`, `image` | |
| `outcomes` | LO ids this session teaches |
| `objectives` | [{verb, text}] — measurable, 2–4 |
| `materials`, `prep` | what the instructor prepares |
| `plan` | [{minutes, phase, title, teacher, students, notes}] — must add up to `minutes` (±5) |
| `content` | premium-documents blocks: the FULL lesson (headings, paragraphs, definitions, code, steps, tables, callouts, images) |
| `slides` | premium-presentations slides (recommended; else auto-built from content/plan/activities/quiz) |
| `activities` | [{title, minutes, mode, icon, steps, deliverable, solution, lang, space_lines}] |
| `exercises` | questions for the worksheet (same format as quiz; answers go to the guide) |
| `quiz` | [{q, options, answer (index/text), kind, points, bloom, outcomes, explanation, difficulty}] — 3–5 |
| `lab` | {title, goal, lang, setup: [...], steps: [{title, text, code, check}], checkpoints: [...]} |
| `misconceptions` | [{wrong, fix}] |
| `differentiation` | {support, extend} |
| `homework`, `recap` ([{icon, label, description}]), `worksheet_instructions`, `quiz_minutes` |

Question kinds: mcq (options + answer index) · tf · short · essay · code · fill. `answer` is required
for every quiz item (the validator blocks the build otherwise).
