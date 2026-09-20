Real, captured output from:

```bash
bash scripts/bootstrap.sh
bash scripts/call.sh get_agency_roster '{}'
```

(devuniverse-mcp built and ran cleanly from a fresh clone — this is the
actual `.content[0].text` from a live run, confirming the CLI-wrapper
approach works end to end against the real server, not a mock.)

```json
{
  "content": [
    {
      "type": "text",
      "text": "# The DevUniverse bench — 27 seniors\n\n| Persona | Title | Focus |\n|---|---|---|\n| **Priya Raman** | Delivery Lead & Roundtable Chair | Scope control, sequencing, and making 23 opinionated seniors converge. |\n| **Konstantin Vogel** | Principal Systems Architect | Cross-cutting structure: module boundaries, data flow, failure domains. |\n...\n\n*Honesty note: personas are deterministic expert heuristics — codified rules, preferences, and critique conditions driven by your requirement signals. Every debate is reproducible and testable; no statement is invented at random.*"
    }
  ]
}
```

Exit code: `0`.
