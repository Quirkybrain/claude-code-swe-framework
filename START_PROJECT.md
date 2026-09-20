# Start Project

按照当前仓库的 `CLAUDE.md` 和 Claude Code Framework 开始项目。

读取 `config/project.md`、现有 State/Checkpoint，以及 `input/` 中所有与目标相关的资产。

首先执行 Project Intake、Artifact Validation 和 Gap Analysis。根据项目复杂度、风险、影响、已有资产和 Target Stage，确定 Project/Task Workflow Level，并计算 Minimum Necessary Path。

需要用户决定的问题进入 Clarification Gate。不要假定存在的资料一定正确，不要默认执行完整软件生命周期，也不要生成当前目标不需要的 Artifact。

按依赖执行最小必要工作，持续记录 Artifact、验证证据和 State。达到 Target Stage 后写入 Checkpoint，标记 `PAUSED_AT_STAGE` 并停止。
