# Usage report schema

One JSON object per line, appended to
`~/.cache/ai-skills/reports/<skill-name>.jsonl` by
`skills/skill-enhancer/scripts/log_report.py`. Local-only, never
committed — see that script's docstring for why.

| field | type | required | notes |
|---|---|---|---|
| `skill` | string | yes | matches a `skills/<name>` folder |
| `timestamp` | string | yes | UTC, `%Y-%m-%dT%H:%M:%SZ`, set by the script |
| `tool` | string | yes | which AI tool logged this — `claude`, `cursor`, `antigravity`, `chatgpt`, or `unknown` |
| `task_summary` | string | no | one line, what the task was — **never** include the user's actual file contents, personal data, or anything sensitive; just enough to identify the pattern, e.g. "10-slide investor deck", not the deck's real financials |
| `outcome` | string | yes | `success`, `partial`, or `failure` — see below |
| `issues` | array of strings | no | specific problems hit (repeatable `--issue`) |
| `missing_coverage` | array of strings | no | something the task needed that the skill didn't handle (repeatable `--missing`) |
| `note` | string | no | free text — effort/friction notes ("needed 3 extra clarifying questions"), a suggestion, or context |

## Choosing an outcome

- **`success`** — the skill's output was used as-is, or with only the
  normal amount of back-and-forth the skill itself expects (e.g.
  premium-presentations asking about visual style is normal, not a
  friction point).
- **`partial`** — it worked but something was rough: extra
  clarifying questions beyond what the skill's own design calls for, a
  workaround was needed, the output needed manual fixing after delivery,
  or a script failed but a fallback path still got the task done.
- **`failure`** — the skill couldn't complete the task, produced
  something unusable, or a script/tool crashed with no working fallback.

## Why this shape

- **Exact-string issue/missing_coverage text, not free-form paragraphs**
  — `analyze_reports.py` counts by exact string match on purpose, so use
  a short, consistent phrase when the same problem recurs (e.g. always
  "video embedding not covered" rather than rephrasing each time) so the
  frequency count actually means something. Slightly different wordings
  for the same underlying issue are fine — the agent doing the
  enhancement pass reads the raw list and merges near-duplicates by
  judgment; the script's count is a starting signal, not the final word.
- **No numeric performance metrics (latency, token count, etc.)** — most
  of what these skills do is agentic and judgment-heavy, not a
  deterministic benchmark; a stopwatch number for "how long the
  conversation took" wouldn't mean much without huge context. If a
  specific skill has a genuinely measurable, meaningful performance
  number (e.g. omnicinema/devuniverse's `mcp_cli.mjs` could time a
  `bootstrap.sh` run), put that in `note` as free text rather than
  extending this schema for one skill's special case.
- **Local file, not a repo commit per report** — logging must be free
  (no git operations, no credentials, no network) so it never gets
  skipped because pushing felt like too much overhead for a one-line
  note. The enhancement pass is what turns accumulated local signal into
  an actual repo change.
