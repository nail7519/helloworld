#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────
#  setup.sh  –  Create venv, install dependencies, and run the app locally
# ──────────────────────────────────────────────────────────────────────────
set -e

VENV_DIR="venv"

echo "──────────────────────────────────────"
echo "  Pop-Quote App – local setup"
echo "──────────────────────────────────────"

# 1. Create virtual environment (if it does not exist yet)
if [ ! -d "$VENV_DIR" ]; then
  echo "► Creating virtual environment in ./$VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
else
  echo "► Virtual environment already exists – skipping creation."
fi

# 2. Activate
echo "► Activating virtual environment ..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# 3. Install / upgrade dependencies
echo "► Installing dependencies from requirements.txt ..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo "✓  Setup complete!"
echo ""
echo "To activate the venv in your current shell, run:"
echo "    source $VENV_DIR/bin/activate"
echo ""
echo "Then start the development server with:"
echo "    python app.py"
echo ""
echo "──────────────────────────────────────"
echo "  Starting development server now ..."
echo "──────────────────────────────────────"
echo ""

python app.py
