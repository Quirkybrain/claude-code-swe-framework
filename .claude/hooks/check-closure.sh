#!/bin/bash
# Wrapper for check-closure.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/check-closure.py"

