#!/usr/bin/env bash
# nx launcher:  bash nx.sh <command> …   (see: bash nx.sh -h)
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$(command -v python3)" "$S/nxkit.py" "$@"
