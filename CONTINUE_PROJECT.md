# Continue Project

按照当前运行时加载的框架主指令（Claude Code：`CLAUDE.md`；OpenCode V2：`AGENTS.md`）继续项目。

读取 `config/project.md`、`state/` 中最新 State/Checkpoint、Artifact Registry、当前 Minimum Necessary Path，以及所有相关 Artifact 和验证证据。

先核对当前仓库 revision、分支/worktree 和 working tree，检测 Checkpoint 之后发生的变化。不要盲目信任旧 Checkpoint，也不要重复已经有当前有效证据的工作。

对变化执行 Change Impact Analysis，标记受影响的 Artifact/Component，重新验证必要范围，并重新计算 Minimum Necessary Path。

先运行 `python3 scripts/swe_guard.py status` 查看跨 worktree 未结束的交接、HEAD、脏路径和本地 Git 快照引用，并与磁盘文件和 Checkpoint 核对；不得把仅有哈希、没有可恢复内容的旧版本称为已备份。恢复修改前，确认已提交基线及 `input/` 中适用的公司 Git 规范；任务验证后由专业 Agent 在任务分支定向提交，再由 `repository-manager` 根据门禁结果逐级合并并复核状态。若 Target Stage 或重大决策不明确，进入 Clarification Gate。否则从下一个 dependency-ready 节点继续；到达 Target Stage 后更新 Checkpoint，标记 `PAUSED_AT_STAGE` 并停止。

Git 分支与公司规范：先读取 [`config/git-policy.json`](config/git-policy.json)；公司规范路径为空时采用 [`config/git-policy.default.md`](config/git-policy.default.md)。每个小任务使用独立 `task/` 分支及 worktree，完成并提交后由 `repository-manager` 合入相应的 `feat/`、`fix/`、`docs/` 等汇总分支；完整变更通过相关验证、评审与门禁后再合入 `main`。详细时序见 [`docs/git-collaboration.md`](docs/git-collaboration.md)。
