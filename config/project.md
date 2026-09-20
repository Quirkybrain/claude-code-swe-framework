# Project Configuration

填写本文件以控制 Framework 在真实项目中的目标、流程强度、自主程度和技术约束。

- 未确定的字段填写 `auto`。
- 多项内容可使用逗号分隔或 Markdown 列表。
- 用户明确填写的值优先于 Framework 推断。
- `auto` 不表示可以忽略重大决策；高影响且无法可靠推断时，Orchestrator 必须询问。
- 示例见 [project.example.md](project.example.md)。

## Project

| Field | Value |
|---|---|
| Project Name | auto |
| Project Description | auto |
| Target Stage | auto |
| Workflow Mode | AUTO |
| Execution Mode | GATED_AUTO |

`Target Stage` 常用值：`requirements`、`uml`、`architecture`、`detailed-design`、`implementation`、`review`、`testing`、`acceptance`、`documentation`、`release`、`maintenance` 或 `auto`。

`Workflow Mode`：`AUTO`、`LIGHTWEIGHT`、`STANDARD`、`STRICT`。

`Execution Mode`：`INTERACTIVE`、`GATED_AUTO`、`FULL_AUTO`。

## Technology

| Field | Value |
|---|---|
| Language | auto |
| Language Version | auto |
| Framework | auto |
| Frontend | auto |
| Backend | auto |
| Database | auto |
| UI Framework | auto |
| API Style | auto |
| Build System | auto |
| Package Manager | auto |
| Testing Framework | auto |
| Target Platform | auto |
| Deployment Target | auto |

## Constraints and Preferences

| Field | Value |
|---|---|
| Must Use Technologies | auto |
| Forbidden Technologies | auto |
| Technical Preferences | auto |
| Performance Requirements | auto |
| Security Requirements | auto |
| Compatibility Requirements | auto |
| Other Constraints | auto |

## Configuration Notes

Add project-specific explanations, known conflicts, or links to relevant files under `input/` here.

- None.
