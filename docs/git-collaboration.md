# Git 多智能体协作

本流程适用于 Claude Code 和 OpenCode。以 `config/git-policy.json` 为可执行设置，以 `config/git-policy.default.md` 为默认规范；显式用户指令和已配置的公司规范优先。Orchestrator 决定任务、依赖和 Gate；`repository-manager` 管理分支、worktree、同步和合并；每名专业 Agent 在自己的任务分支提交其交付物。报告型 Agent 只写并提交报告，不改所分析或评审的对象。

## 分支类型和任务归属

```text
main（已通过的完整变更）
  ├── feat/export-api（新功能）
  │     ├── task/add-endpoint
  │     └── task/add-api-tests
  ├── fix/parser-crash（Bug 修复）
  │     └── task/fix-null-input
  └── docs/install-guide（独立文档工作）
        └── task/update-install-steps
```

汇总分支按**主要交付目标**命名：`feat/` 新功能、`fix/` Bug 修复（含紧急修复）、`docs/` 独立文档、`refactor/` 重构、`test/` 测试专项、`chore/` 构建或维护。无论类型，每个可独立交接的小任务使用唯一 `task/` 分支。一个 Bug 修复所需的回归测试和说明也放在同一个 `fix/` 分支；功能附带的 README 更新仍归该 `feat/` 分支。提交类型按**实际提交内容**选择，例如 `fix(parser): handle null input`、`test(parser): cover null input`、`docs(setup): explain installation`。不因使用 `technical-writer` 就自动新建 `docs/` 分支。

## 分支与交接顺序

1. **准备汇总分支**：`repository-manager` 检查状态与远端。若 `main` 有上游且工作区干净，执行 `git fetch`，在 `main` 上 `git pull --ff-only`；无远端时使用核对过的本地 `main`。从该提交创建匹配主要工作的 `feat/`、`fix/`、`docs/` 等分支。不得把未审查的本地改动混入基线。
2. **准备小任务**：每个任务从最新已提交的汇总分支 tip 创建唯一 `task/<task-id>`，放在独立 worktree。示例：`git worktree add -b task/fix-null-input ../fix-null-input fix/parser-crash`；独立文档任务则可从 `docs/install-guide` 创建 `task/update-install-steps`。一个 worktree 同时只有一个活动 handoff；一个 task branch 只有一个写入 Agent。需要新输入时先结束活动交接，再同步父分支、重新 pin。
3. **固定交接**：专业 Agent 的 handoff 指定 `task_branch`、`parent_branch`、精确 `commit_paths`、输入、输出和交付物。执行 `pin`、必要时 `snapshot`、`begin`。守卫核对当前分支、父分支 tip、策略哈希、输入哈希和快照。并行任务的读写范围不得冲突。
4. **任务内提交**：Agent 完成自己的实现、测试、文档或报告后，运行适用检查；只 `git add` handoff 声明路径，检查 `git diff --cached`、`git diff --cached --check`，提交后运行 `finish`。守卫验证提交从固定基线线性前进、每个提交路径均在 `commit_paths` 中、每个声明范围有提交且目标路径干净。审查修正使用新提交并重测。活动交接中不得切分支、pull、merge、rebase 或 push。
5. **小任务进入汇总分支**：任务 Gate 通过后，`repository-manager` 在干净的目标 worktree 上 pin `repository_action: merge`，给出 `source_branch: task/...`、`target_branch: fix/...`（或其他汇总分支）、合并可能影响的 `writes`、已提交在来源分支中的门禁报告 `gate_evidence_path` 和集成报告 `deliverables`；守卫按来源提交固定门禁报告的字节。核对 source tip、目标 tip，必要时对已有目标文件做快照。执行 `git merge --no-ff task/...`，解决冲突并重跑受影响检查，然后单独提交集成证据报告，最后 `finish`。守卫校验双亲 merge commit、来源 tip、目标路径范围和报告提交。任务失败或证据过期不得合并。
6. **完整变更进入 main**：所有小任务合并后，在汇总分支执行与变更相关的集成、回归、独立评审与 Stage Gate。通过后先更新干净的 `main`，再用相同的 merge handoff 将汇总分支合入 `main`，并指定来源分支中已提交的 `integration_evidence_path`；文档专项可提供链接/渲染检查证据，代码修复应提供相关测试结果。若 `main` 已前进，先停止并重新评估冲突和验证范围。推送、部署、删除分支或 worktree 另按用户授权执行。

示例 handoff 字段：

```json
{
  "task_branch": "task/fix-null-input",
  "parent_branch": "fix/parser-crash",
  "commit_paths": ["src/parser.py", "tests/test_parser.py", "artifacts/40-implementation/parser.md"]
}
```

合并 handoff 使用 `repository_action: "merge"`，并指定 `source_branch`、`target_branch`、`writes`、来源分支中的门禁证据和持久化集成报告。`repository_action: "status"` 保留只读状态检查；`commit` 用于仓库管理者自己的有界仓库文件变更。运行命令及完整字段见 [交接守卫](operational-guards.md)。

## 何时拉取与冲突处理

`git fetch` 只更新远端跟踪引用，不改工作分支；在创建汇总分支前、合并小任务前、以及合入 `main` 前检查一次。`git pull --ff-only` 只用于有上游、干净、确实应快进的本地跟踪分支。任务分支从汇总分支的已提交 tip 创建；若父分支变化，结束当前交接、分析影响后重新创建交接或有证据地同步，绝不在活动交接中悄悄拉取。冲突须由目标分支负责人按固定需求和契约解决，记录受影响路径，重新运行测试与 Gate；禁止用 `reset --hard`、强制推送或静默改写已评审提交掩盖冲突。

## 公司 Git 规范

默认 `config/git-policy.json` 的 `company_policy_path` 为 `null`，使用 [默认规范](../config/git-policy.default.md)，包括 `main` → 汇总分支（`feat/`、`fix/`、`docs/` 等）→ `task/`、`--no-ff` 和 `<type>(<scope>): <summary>`。公司提供规范时，将原文放在 `input/`（如 `input/standards/git.md`），把该路径填入 `company_policy_path`，并按规范调整 `main_branch`、`integration_branch_pattern`、`task_branch_pattern` 及 `merge_strategy`（`no-ff` 或 `ff-only`）。旧的 `feature_branch_pattern` 在没有 `integration_branch_pattern` 时仍可使用。每份 handoff 将原文作为带唯一锚点或位置的输入，并填 `commit_policy_path`；守卫固定原文与设置哈希。未写明的条款继续采用默认规范；公司规范的自然语言含义由 Orchestrator 核对，脚本只验证路径、固定版本、分支形状、提交范围及默认格式或公司规范存在。任务提交、层级合并和必要验证始终执行；若公司规则与用户要求冲突，向用户说明具体冲突。
