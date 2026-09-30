# Registering studio-mcp as an MCP server

The CLI (`scripts/call.sh`) needs no registration. Register the server when you want the tools to
appear natively in a client. Run `bash scripts/bootstrap.sh` first; it prints the two paths you need.
Below, `VENV` is the environment it created (default `/Volumes/PortableSSD/creative-studio/.venv`,
see `~/.config/ai-skills/creative-studio.venv`).

## Claude Desktop — `~/Library/Application Support/Claude/claude_desktop_config.json`
```json
{"mcpServers": {"creative-studio": {
  "command": "VENV/bin/studio-mcp",
  "env": {"PLAYWRIGHT_BROWSERS_PATH": "VENV/ms-playwright"}}}}
```

## Claude Code
```bash
claude mcp add creative-studio --env PLAYWRIGHT_BROWSERS_PATH=VENV/ms-playwright -- VENV/bin/studio-mcp
```

## Cursor — `~/.cursor/mcp.json`   ·   Antigravity — its MCP settings (same shape)
```json
{"mcpServers": {"creative-studio": {
  "command": "VENV/bin/studio-mcp",
  "env": {"PLAYWRIGHT_BROWSERS_PATH": "VENV/ms-playwright"}}}}
```

Optional env: `STUDIO_HOME` (outputs/models folder, otherwise remembered in
`~/.config/ai-skills/creative-studio.root`), `COMFYUI_URL` (an existing ComfyUI server),
`HF_TOKEN` (Hugging Face free tier). Paid keys for `ai_generate_image_byok` (`FAL_KEY`,
`REPLICATE_API_TOKEN`, `OPENAI_API_KEY`) are read from the environment only — never write them
into these files if the file is shared or synced.

110 tools is a lot for some clients' tool limits. If a client caps tools, keep the CLI route for
the rest, or register a second copy with fewer departments by disabling tools in the client UI.

Check: in the client, call `studio_doctor` — it lists STUDIO_HOME and what is installed.
