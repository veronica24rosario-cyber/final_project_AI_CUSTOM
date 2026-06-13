#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
echo "Running CAG validation tests."
echo "If these fail, the CAG integration is incomplete or does not match the expected API contract."
PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_*.py'
