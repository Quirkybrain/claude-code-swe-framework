# Adopt Existing Project

按照当前仓库的 `CLAUDE.md` 和 Claude Code Framework 接手已有项目。现有代码位于项目根目录和/或 `input/existing/`。

先执行面向现有代码的 Project Intake 和 Reverse Engineering，再规划任何大规模修改。

识别并记录：项目结构、构建方式、技术栈、Architecture、Component/Module 边界、Contracts/API、数据模型、运行与部署约束、Project Constraints、现有测试及覆盖范围、已知失败和风险。

建立 Asset/Artifact Inventory 和初始 State。已有代码、测试和文档都只是证据，不自动等于正确需求或有效设计；从实现反推的需求必须标记 `INFERRED`，相关 Artifact 在验证前保持 `UNVERIFIED`。

对目标相关成果执行 Artifact Validation 和 Gap Analysis，评估 Workflow Level，并计算 Minimum Necessary Path。重大产品、架构、数据、安全或部署冲突进入 Clarification Gate。

在 Intake、逆向分析和必要澄清完成前，不要擅自重写现有系统。达到 Target Stage 后更新 Checkpoint，标记 `PAUSED_AT_STAGE` 并停止。
