# OpenCode V2 使用指南

本框架现可在 Claude Code 和 OpenCode V2 中使用同一套 Artifact → Agent → Gate → Checkpoint 工作流。OpenCode 适配以本机验证过的 `v2.0.14` 为基线。

## 启动

在目标 Git 项目根目录保留 `AGENTS.md`、`opencode.json`、`.opencode/`、`.claude/`、`scripts/`、`config/` 和工作流模板。需要 Python 3、Git 和至少一个已有提交。先编辑 `config/project.md`，再启动：

```sh
opencode
```

在 OpenCode 中用 `/connect` 选择 **DeepSeek** 并输入 API key，再用 `/models` 选择可用的 DeepSeek 模型。凭据保存在 OpenCode 的用户配置中；不要把密钥写入本仓库的 `opencode.json`。Claude Code 的 `ANTHROPIC_*` 环境变量和 `.claude/settings.example.json` 不会配置 OpenCode。OpenCode 的项目配置只选择 `swe-orchestrator`，不强制覆盖用户选定的模型；所有专业 Agent 继承主会话所选模型。

然后输入任一现有模板指令，如 `读取 START_PROJECT.md 并执行。`、`读取 CONTINUE_PROJECT.md 并执行。` 或填写 `EXECUTE_TASK.md`。四个工作流入口在两种运行时共用。

## 运行时映射

| 框架能力 | Claude Code | OpenCode V2 |
|---|---|---|
| 主编排指令 | `CLAUDE.md` | 生成的 `AGENTS.md`，包含同一份主规则与运行时映射 |
| 专业 Agent | `.claude/agents/*.md` | 生成的 `.opencode/agents/*.md`，经 `subagent` 工具派发 |
| Skill | `.claude/skills/*/SKILL.md` | 原路径由 OpenCode 直接发现，按需用 `skill` 加载 |
| 持续规则 | `.claude/rules/*.md` | `AGENTS.md` 指示按任务读取相关规则 |
| 交接检查 | `.claude/settings.json` 的 `PreToolUse` | `.opencode/plugins/swe-guards.js` 的 `execute.before` |
| 结束前检查 | Claude Code `Stop` Hook | 从项目根目录运行 `python3 .claude/hooks/check-closure.py </dev/null` |

OpenCode V2 不会自动读取 `CLAUDE.md`，其 `instructions` 配置当前也不会解析文件。因此 `AGENTS.md` 是生成的完整主指令，不能仅放一个文件链接。修改 `CLAUDE.md` 或任一 `.claude/agents/*.md` 后执行：

```sh
python3 scripts/sync_opencode.py
python3 scripts/sync_opencode.py --check
```

生成文件请勿手改。`.claude/rules/` 仍是规则原文；Agent 必须在相关任务中读取。`AGENTS.md` 的运行时映射优先于其中 Claude 专属工具名称。OpenCode V2 的 Agent frontmatter 与 Claude Code 不兼容，所以同步脚本转换角色、权限和正文，而不直接复用 `.claude/agents/` 文件。

## 交接与检查

`STANDARD` 和 `STRICT` 模式继续使用 `scripts/swe_guard.py` 的 `capture-chat`、`pin`、`snapshot`、`begin`、`finish` 流程，详见 [交接与快照检查](operational-guards.md)。OpenCode 主 Agent 调用 `subagent` 时传 `agent: implementation-engineer` 等角色，并在 `prompt` 中单独放一行 `HANDOFF: state/handoffs/<task>.json`。插件将它映射到现有交接检查。`write` / `edit` 和 `apply_patch` 写入时会检查冻结输入；`write` / `edit` 还检查 Artifact 的 `Producer`。`apply_patch` 的最终 Artifact 内容在 Artifact Validation Gate 中核对。任意 shell 或外部编辑器改动仍由 `finish` 的变更清单核对。

OpenCode V2 没有 Claude Code 的 `Stop` Hook。产生了托管 Artifact 时，在结束任务前运行上面的 closure 命令，并记录 Checkpoint。这个检查依赖工作流遵循约定，不能声称 OpenCode 会自动阻止所有未写 Checkpoint 的会话结束。

## 本地验证

```sh
python3 scripts/sync_opencode.py --check
opencode reload
opencode debug agents
opencode plugin list
python3 -m unittest discover -s tests
node --test tests/test_opencode_adapter.mjs
```

`opencode debug agents` 应显示 `swe-orchestrator` 为 `primary`，15 个专业 Agent 为 `subagent`；`opencode plugin list` 应显示 `swe-guards`。这些检查不调用 DeepSeek API。实际模型连通性须在配置凭据后单独验证。
