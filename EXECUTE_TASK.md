# Execute One Task

请按当前仓库的 `CLAUDE.md` 和 Claude Code Framework 执行以下单项任务。

```text
Task: [描述 Bug Fix / Feature / Refactor / Review / Testing 任务]
Desired Outcome: [期望结果]
Allowed Scope: [允许修改或检查的范围；不确定时填写 auto]
Constraints: [额外约束；没有则填写 none]
```

读取 `config/project.md`、相关 State/Checkpoint、Artifacts、Contracts、代码和测试。先确认目标、影响范围、依赖和完成条件。

独立评估本任务的 Task Workflow Level；不要因为整个项目是 `STRICT` 就自动执行完整生命周期，也不要因任务很小而跳过实际风险要求的检查。

执行 Change Impact 和必要的 Clarification，只计算此任务的 Minimum Necessary Path。按任务类型选择所需 Agent/Skill：代码修改后必须 Build、Test、Verify，并按风险完成 Review/Gate；纯 Review 或 Testing 任务保持其职责边界。

执行修改、修 Bug、新功能或重构前，先确认 Git 基线提交及计划写入范围的状态；检查 `input/` 中适用的公司 Git 提交时机和格式，缺省时使用 `repository-manager` 的默认规则。委派专业 Agent 时，按 [`docs/operational-guards.md`](docs/operational-guards.md) 创建、固定并校验短交接单；只有聊天输入时先保存用户原文，要求实际落盘的交付物，不要转抄规范正文。修改前序工件或送审代码时，先保存可验证的 Git 快照。首次交付可运行项目代码时，同步交付项目 README 并验证其中命令。

只修改授权范围，不做无关重构。记录结果、验证证据、受影响状态和下一动作；达到本任务目标后更新 Checkpoint 并停止。
