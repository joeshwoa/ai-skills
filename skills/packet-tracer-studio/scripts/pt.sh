#!/usr/bin/env bash
# pt.sh — call packet-tracer-mcp from any terminal or agent that has no MCP connection.
#   pt.sh status                     -> pt_status
#   pt.sh <pt_tool> '<json args>'    -> any tool, e.g. pt.sh pt_list_devices '{}'
#   pt.sh build SPEC.json            -> pt_build_topology with the spec file (check it first with ptspec.py)
# Finds node and the server in this order: $PT_NODE / $PT_MCP_DIR, the SSD copies, then node on PATH.
set -euo pipefail
MCP_DIR="${PT_MCP_DIR:-/Volumes/PortableSSD/MCP/packet-tracer-mcp}"
NODE="${PT_NODE:-}"
[ -z "$NODE" ] && [ -x /Volumes/PortableSSD/n8nFlows/engine/node/bin/node ] && NODE=/Volumes/PortableSSD/n8nFlows/engine/node/bin/node
[ -z "$NODE" ] && NODE="$(command -v node || true)"
INDEX="$MCP_DIR/dist/index.js"
[ -f "$INDEX" ] || INDEX="$HOME/.gemini/pt_mcp_cli.mjs"
if [ -z "$NODE" ] || [ ! -f "$INDEX" ]; then
  echo "packet-tracer-mcp not found (node='$NODE', server='$INDEX'). Set PT_NODE / PT_MCP_DIR, or use offline mode: ptspec.py guide SPEC.json" >&2
  exit 3
fi
cmd="${1:-}"; shift || true
case "$cmd" in
  status) exec "$NODE" "$INDEX" cli pt_status '{}' ;;
  build)  spec="${1:?usage: pt.sh build SPEC.json}"; exec "$NODE" "$INDEX" cli pt_build_topology "$(cat "$spec")" ;;
  pt_*)   exec "$NODE" "$INDEX" cli "$cmd" "${1:-{\}}" ;;
  *) sed -n '2,6p' "$0"; exit 2 ;;
esac
