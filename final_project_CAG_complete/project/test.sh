#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
./scripts/validate_student_cag.sh
