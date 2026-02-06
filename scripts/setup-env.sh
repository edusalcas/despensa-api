#!/bin/bash

# Prerequisites 
# sudo apt update
# sudo apt install python3.12-venv
# sudo apt install libpq-dev python3-dev build-essential

# Ensure script runs from repo root
if [[ ! -d .git ]]; then
  echo "Error: This script must be run from the root of the repository."
  exit 1
fi

echo "Creating virtual environment..."
python3.12 -m venv .venv --prompt=dev
source .venv/bin/activate

echo "Installing requirements..."
export DEVENV=1
pip install --upgrade pip
pip install uv
uv pip install -r requirements.txt

echo "Setting up git hooks..."
git config core.hooksPath .githooks
chmod +x .githooks/pre-push