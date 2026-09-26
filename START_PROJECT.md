# Start Project (启动新项目)

按照当前仓库的 `CLAUDE.md` 和 Claude Code Framework 开始项目。

---

## 💡 用户提示（执行前请确认）

- **资料放置**：
  - 如果你已有需求文档或架构资料，请确认已放入 [`input/`](input/README.md)（不知道放哪可直接丢进 `input/` 根目录）；
  - 如果你只有一段想法或需求摘要，可以直接在下方填写，或直接在会话中发给 Claude：
    ```text
    项目目标简述：[在这里输入你的一句话想法或核心目标，若已放入 input/ 则留空]
    ```
- **配置确认**：可检查 [`config/project.md`](config/project.md) 中的技术栈与目标，未确定项保持 `auto` 即可。

---

## 框架执行指令

1. 读取 `config/project.md`、现有 State/Checkpoint，以及 `input/` 中所有与目标相关的原始资产。只有聊天需求时，委派前按 [`docs/operational-guards.md`](docs/operational-guards.md) 把用户原文一次性落盘并对照原消息核查；若资料和聊天目标都没有，在 Clarification Gate 中询问核心需求。识别 `input/` 中适用的公司 Git 提交时机及消息格式。
2. 首先执行 Project Intake、Artifact Validation 和 Gap Analysis。根据项目复杂度、风险、已有资产和 Target Stage，确定 Workflow Level 并推导最简必要路径（Minimum Necessary Path）。
3. 在 `STANDARD` 和 `STRICT` 模式下，**严禁主会话单体包办**，必须调用 `Agent(subagent_type=...)` 工具委派给专业智能体执行。
4. 需要用户确认的重大分歧进入 Clarification Gate。不生成非必要的中间产物。
5. 按依赖执行最小必要工作；改动前确认 Git 提交基线和仓库状态，委派前使用 [`docs/operational-guards.md`](docs/operational-guards.md) 的固定版本交接与门禁，修改旧工件或送审前完成可验证快照。按适用的公司 Git 规范或默认规则，由 `repository-manager` 在任务边界做定向提交并复核状态。持续记录 Artifact（必须包含合规的 `Producer` 字段）、验证证据与 State。首次交付可运行代码时提供已验证命令的项目 README。达到 Target Stage 后写入 Checkpoint，标记 `PAUSED_AT_STAGE` 并安全停止。
