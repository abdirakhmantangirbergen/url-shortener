#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    .venv/bin/pip install --quiet -r requirements.txt
fi

export PORT="${PORT:-8080}"
export PYTHONPATH="$ROOT_DIR"

exec .venv/bin/uvicorn main:app --host 0.0.0.0 --port "$PORT"
