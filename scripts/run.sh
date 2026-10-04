#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PORT="${PORT:-8080}"
export PYTHONPATH="$ROOT_DIR"

exec python3 src/server.py
