#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

# Install the package in editable mode so imports resolve
pip install -e .

# Run FastAPI gateway
exec uvicorn a2aworld.a2a_gateway.main:app --host 0.0.0.0 --port 8000
