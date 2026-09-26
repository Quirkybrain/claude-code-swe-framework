#!/usr/bin/env python3
"""PreToolUse Agent hook: require a frozen, checked specialist handoff."""

import json
from pathlib import Path
import re
import subprocess
import sys


SPECIALISTS = {
    "asset-analyst", "requirements-analyst", "system-modeler", "solution-architect",
    "experience-designer", "delivery-planner", "implementation-engineer",
    "test-engineer", "quality-reviewer", "integration-engineer", "debug-specialist",
    "system-verifier", "technical-writer", "release-engineer", "repository-manager",
}
HANDOFF = re.compile(r"(?m)^HANDOFF:\s*(state/handoffs/[A-Za-z0-9_.-]+\.json)\s*$")


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        print("BLOCKED: cannot parse Agent hook input", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("BLOCKED: Agent hook input must be an object", file=sys.stderr)
        return 2
    if payload.get("tool_name") != "Agent":
        return 0
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        print("BLOCKED: Agent tool_input is invalid", file=sys.stderr)
        return 2
    role = tool_input.get("subagent_type")
    if role not in SPECIALISTS:
        return 0
    prompt = tool_input.get("prompt") or ""
    if not isinstance(prompt, str):
        print("BLOCKED: Agent prompt is invalid", file=sys.stderr)
        return 2
    match = HANDOFF.search(prompt)
    if not match:
        print("BLOCKED: specialist Agent prompt needs one HANDOFF: state/handoffs/<task>.json line", file=sys.stderr)
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
    command = [sys.executable, str(root / "scripts/swe_guard.py"), "assert-active", match.group(1), role]
    checked = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if checked.returncode:
        print(checked.stderr.strip() or "BLOCKED: handoff validation failed", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
