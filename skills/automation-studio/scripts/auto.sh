#!/usr/bin/env bash
# autokit launcher:  bash auto.sh <command> …   (see: bash auto.sh -h)
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(command -v python3)"
exec "$PY" "$S/autokit.py" "$@"
