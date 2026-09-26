#!/usr/bin/env python3
"""Block Write/Edit of an active Agent's read-only input."""

import json
from pathlib import Path
import subprocess
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        print("BLOCKED: cannot parse Write/Edit hook input", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("BLOCKED: Write/Edit hook input must be an object", file=sys.stderr)
        return 2
    if payload.get("tool_name") not in ("Write", "Edit"):
        return 0
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        print("BLOCKED: Write/Edit tool_input is invalid", file=sys.stderr)
        return 2
    target = tool_input.get("file_path")
    if not target:
        print("BLOCKED: Write/Edit has no file_path", file=sys.stderr)
        return 2
    cwd = Path(payload.get("cwd") or Path.cwd())
    root_result = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        text=True, capture_output=True, check=False,
    )
    if root_result.returncode:
        print("BLOCKED: cannot locate project Git root", file=sys.stderr)
        return 2
    root = Path(root_result.stdout.strip())
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = cwd / target_path
    command = [sys.executable, str(root / "scripts/swe_guard.py"), "assert-write", str(target_path.resolve())]
    checked = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if checked.returncode:
        print(checked.stderr.strip() or "BLOCKED: frozen input", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
