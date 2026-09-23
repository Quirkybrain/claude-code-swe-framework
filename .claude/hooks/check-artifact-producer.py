#!/usr/bin/env python3
"""
PreToolUse Hook: check-artifact-producer.py
Ensures that any file written to artifacts/ contains valid 'Producer' metadata,
and that direct main-session authoring explicitly records a Deviation justification.
"""

import sys
import json
import re
from pathlib import Path

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            sys.exit(0)
        data = json.loads(raw_input)
    except Exception:
        # If payload parsing fails, do not block other tools unexpectedly
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path_str = tool_input.get("file_path") or tool_input.get("path") or ""
    if not file_path_str:
        sys.exit(0)

    file_path = Path(file_path_str)

    # Only inspect files targeted under 'artifacts/'
    is_in_artifacts = False
    for part in file_path.parts:
        if part == "artifacts":
            is_in_artifacts = True
            break

    if not is_in_artifacts or file_path.name == ".gitkeep":
        sys.exit(0)

    # Determine the content to validate
    content_to_check = ""
    if tool_name == "Write":
        content_to_check = tool_input.get("content", "")
    elif tool_name == "Edit":
        new_string = tool_input.get("new_string", "")
        existing_content = ""
        if file_path.exists():
            try:
                existing_content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
        content_to_check = existing_content + "\n" + new_string

    if not content_to_check:
        sys.exit(0)

    # Check for Producer metadata header (supports markdown list, bold, and table formats)
    producer_match = re.search(
        r'[*_]*(?:Producer|产出实体|产出者)[*_]*\s*[:：|]\s*[*_]*([^\n\r]+)',
        content_to_check,
        re.IGNORECASE
    )

    if not producer_match:
        sys.stderr.write(
            f"\n[BLOCKED by SWE Framework Hook: PreToolUse]\n"
            f"目标产物 '{file_path.name}' 位于 artifacts/ 目录下，必须声明 'Producer' (产出实体) 元数据！\n\n"
            f"规范格式示例：\n"
            f"  - **Producer**: agent:<agent-name>\n"
            f"如果由主会话直接产出（流程偏差），必须包含明确的技术理由：\n"
            f"  - **Producer**: orchestrator:main-session | Deviation: <具体技术理由>\n\n"
            f"请调用对应的 Agent 工具派发任务，或在产物头部补齐 Producer 元数据后重试。\n"
        )
        sys.exit(2)

    raw_val = producer_match.group(1).strip().rstrip('|').strip()
    producer_val = re.sub(r'^[*_]+|[*_]+$', '', raw_val).strip()

    # Check if produced by main-session / orchestrator without Deviation justification
    is_main_session = bool(re.search(r"(?:main-session|orchestrator|主会话)", producer_val, re.IGNORECASE))
    has_deviation = bool(re.search(r"(?:Deviation|偏差|理由)\s*[:：]", producer_val, re.IGNORECASE))

    if is_main_session and not has_deviation:
        sys.stderr.write(
            f"\n[BLOCKED by SWE Framework Hook: PreToolUse]\n"
            f"目标产物 '{file_path.name}' 声明由主会话直接产出，但缺少 'Deviation' 偏差说明！\n\n"
            f"在 STANDARD / STRICT 模式下，主会话直接产出核心产物属于流程异常，必须说明具体技术理由。\n"
            f"规范格式示例：\n"
            f"  - **Producer**: orchestrator:main-session | Deviation: <为什么没有委派给对应 Subagent 的具体理由>\n\n"
            f"请修正 Producer 头部或调用对应 Agent 工具。\n"
        )
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()

