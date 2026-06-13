#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
echo "Running base tests. These must pass before you modify the project."
PYTHONPATH=. python3 -m unittest discover -s tests/base -p 'test_*.py'
