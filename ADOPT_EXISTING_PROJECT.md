# Adopt Existing Project

按照当前运行时加载的框架主指令（Claude Code：`CLAUDE.md`；OpenCode V2：`AGENTS.md`）接手已有项目。现有代码位于项目根目录和/或 `input/existing/`。

先执行面向现有代码的 Project Intake 和 Reverse Engineering，再规划任何大规模修改。

识别并记录：项目结构、构建方式、技术栈、Architecture、Component/Module 边界、Contracts/API、数据模型、运行与部署约束、Project Constraints、现有测试及覆盖范围、已知失败和风险。

建立 Asset/Artifact Inventory 和初始 State。已有代码、测试和文档都只是证据，不自动等于正确需求或有效设计；从实现反推的需求必须标记 `INFERRED`，相关 Artifact 在验证前保持 `UNVERIFIED`。

对目标相关成果执行 Artifact Validation 和 Gap Analysis，评估 Workflow Level，并计算 Minimum Necessary Path。重大产品、架构、数据、安全或部署冲突进入 Clarification Gate。

在 Intake、逆向分析和必要澄清完成前，不要擅自重写现有系统。达到 Target Stage 后更新 Checkpoint，标记 `PAUSED_AT_STAGE` 并停止。

Git 分支与公司规范：先读取 [`config/git-policy.json`](config/git-policy.json)；公司规范路径为空时采用 [`config/git-policy.default.md`](config/git-policy.default.md)。每个小任务使用独立 `task/` 分支及 worktree，完成并提交后由 `repository-manager` 合入相应的 `feat/`、`fix/`、`docs/` 等汇总分支；完整变更通过相关验证、评审与门禁后再合入 `main`。详细时序见 [`docs/git-collaboration.md`](docs/git-collaboration.md)。
