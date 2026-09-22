#!/usr/bin/env bash
set -euo pipefail
# Adapter installer for claude — copies universal skill to runtime path without forking methodology
SKILL_ID="${1:-pixz.core.orchestrator}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUNTIME="claude"
echo "Resolving $SKILL_ID for $RUNTIME..."
python3 "$ROOT/scripts/resolve.py" --install "$SKILL_ID" --runtime "$RUNTIME" --channel stable
echo "Install via adapter/$RUNTIME — see adapters/README.md for runtime path."
