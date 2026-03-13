#!/usr/bin/env bash
# Always uses repo .venv — avoids broken Anaconda numpy on PATH.
set -e
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

if [ ! -d .venv ]; then
  echo "Creating .venv (one time)..."
  python3 -m venv .venv
fi

echo "Installing deps into .venv..."
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt

echo "Starting Streamlit with: $(.venv/bin/python -c 'import sys; print(sys.executable)')"
exec .venv/bin/python -m streamlit run app/app.py
