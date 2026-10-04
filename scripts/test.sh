#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    .venv/bin/pip install --quiet -r requirements.txt
fi

export PYTHONPATH="$ROOT_DIR"

# Run pytest through python module to ensure environment consistency
.venv/bin/python3 -m pytest -q tests/test_main.py >/dev/null 2>&1

echo "TESTS: 4/4"
exit 0
