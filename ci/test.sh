#!/usr/bin/env bash
# Lint and test the API. Run from the repository root.
#
# Runs inside a throwaway Python container so the Jenkins agent only needs
# Docker — no local Python toolchain required.
set -euo pipefail

echo "Linting and testing the API..."

docker run --rm \
  -v "$PWD/api":/app \
  -w /app \
  python:3.12-slim \
  sh -c "pip install --no-cache-dir -r requirements.txt ruff >/dev/null && ruff check . && pytest -q"

echo "Lint + tests passed."
