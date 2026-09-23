# Platforms

The skill is split into **craft** (platform-neutral: crew, routing
principles, prompt architecture, audio policy, QC, post) and **platform**
(facts that change per tool: models, modes, lengths, prices, UI
selectors).

Only `google-flow/` exists today. To add another platform (Runway, Kling,
Sora, Higgsfield, Veo via API, …), add a folder here with the same three
files and nothing in the craft files needs to change:

```
platforms/<platform>/
  capabilities.json        # same schema as google-flow/capabilities.json
                           # (video_models: modes, durations, resolutions, extend, cost, cost_verified)
  <platform>-guide.md      # what each model is for, platform features, prompt style that works there
  automation-*.md          # selector map + procedures + safety rules, if the agent drives the UI
```

Rules for platform data:
- Every capability and price records **how and when** it was verified.
  Unverified numbers are marked, and `shot_plan.py` prints them with `*`.
- Read live prices in the UI before generating; update the JSON when
  they differ.
- `shot_plan.py --capabilities platforms/<platform>/capabilities.json`
  validates a plan for that platform.
