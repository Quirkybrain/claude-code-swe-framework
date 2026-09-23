#!/usr/bin/env python3
"""
Stop Hook: check-closure.py
Ensures that before Claude Code stops a task in the SWE Framework,
a checkpoint and state record have been persisted if artifacts were created or modified.
"""

import sys
import json
from pathlib import Path

def main():
    try:
        raw_input = sys.stdin.read()
        if raw_input.strip():
            _ = json.loads(raw_input)
    except Exception:
        pass

    cwd = Path.cwd()
    artifacts_dir = cwd / "artifacts"
    state_dir = cwd / "state"

    # Only run in projects with SWE framework initialized
    if not (cwd / "CLAUDE.md").exists() or not artifacts_dir.exists():
        sys.exit(0)

    # Check if there are real managed artifacts beyond .gitkeep
    managed_artifacts = [
        f for f in artifacts_dir.glob("**/*")
        if f.is_file() and f.name != ".gitkeep" and not f.name.startswith(".")
    ]

    if not managed_artifacts:
        # No artifacts generated yet, allow clean exit
        sys.exit(0)

    # If artifacts exist, verify that a checkpoint has been recorded
    checkpoint_file = state_dir / "checkpoint.md"
    project_state_file = state_dir / "project-state.md"

    if not checkpoint_file.exists() and not project_state_file.exists():
        sys.stderr.write(
            f"\n[BLOCKED by SWE Framework Hook: Stop]\n"
            f"检测到 artifacts/ 目录下已生成 {len(managed_artifacts)} 个工程产物，但在 state/ 目录下尚未持久化 Checkpoint！\n\n"
            f"根据 SWE Framework 闭合原则，在会话停止前必须写入 Checkpoint 并标记状态：\n"
            f"  - 目标已达成：在 state/checkpoint.md 记录完成证据并标记 PAUSED_AT_STAGE\n"
            f"  - 需用户确认：记录当前阶段及待澄清问题\n\n"
            f"请在 state/checkpoint.md 中保存 Checkpoint 后再结束任务。\n"
        )
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()

