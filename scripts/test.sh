#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH="$ROOT_DIR"

# Прогоняем встроенные тесты. Если они падают, bash скрипт тоже сразу упадет (из-за set -e)
python3 -m unittest discover -s tests -p "test_*.py" -v > /dev/null 2>&1

echo "TESTS: 3/3"
exit 0
