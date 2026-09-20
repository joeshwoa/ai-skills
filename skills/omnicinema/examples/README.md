No captured example output here yet.

`scripts/mcp_cli.mjs` (the generic MCP one-shot client) is verified
end-to-end against a real, complex MCP server — see
`skills/devuniverse/examples/get_agency_roster_output.md` — so the
call mechanism itself is proven.

omnicinema-mcp specifically doesn't build from a fresh clone right now
(see the "Known upstream issue" note in `../SKILL.md` and the diagnostic
`../scripts/bootstrap.sh` prints) — once that's fixed upstream, run:

```bash
bash ../scripts/bootstrap.sh
bash ../scripts/call.sh list_providers '{}'
```

and drop the real captured output here.
