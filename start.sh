#!/usr/bin/env bash
# Start Digital Eye (backend + dashboard) on Linux/macOS.
set -euo pipefail
cd "$(dirname "$0")"

[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt

[ -d dashboard/frontend/node_modules ] || npm --prefix dashboard/frontend install

.venv/bin/python run.py &
BACKEND=$!
trap 'kill $BACKEND 2>/dev/null' EXIT

echo "Backend:   http://localhost:5000"
echo "Dashboard: http://localhost:5173"
npm --prefix dashboard/frontend run dev
