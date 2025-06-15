#!/bin/bash

echo "[Setup.sh] Create venv"
if [ -d "./.venv" ]; then
    echo "Virtual env exists"
    . ./.venv/bin/activate
else
    echo "Virtual env does not exist"
    python3 -m venv .venv
    . ./.venv/bin/activate
fi

echo "[Setup.sh] Install packages"
pip install -r requirements.txt

echo "[Setup.sh] Done"
echo "To use the virtual environment, run: source ./.venv/bin/activate"