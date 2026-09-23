#!/bin/bash
# Wrapper for check-artifact-producer.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/check-artifact-producer.py"

