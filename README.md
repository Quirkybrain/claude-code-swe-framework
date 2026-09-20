# Claude Code AI Software Engineering Framework

一套面向真实工程场景的 **Claude Code 软件工程 (SWE) 落地框架**。通过结构化 Markdown 编排、多角色智能体协同、自适应阶段关卡与持久化状态机，帮助开发者在 Claude Code 中高效推进复杂软件研发。

Claude Code 作为底层推理与执行引擎，本框架无需部署独立的 Workflow Server、数据库或后台守护进程，零外部服务依赖，由纯工程化载体驱动。

---

## 核心特性

- **自适应工程路径 (Minimum Necessary Path)**：按需裁剪，不拘泥于固定瀑布流程。从单点 Bug 修复到高风险架构演进，依据任务复杂度自适应推导最简必要路径。
- **专业工程角色矩阵 (14 Specialist Agents)**：覆盖需求分析、系统建模、架构设计、计划排期、编码实现、测试验证、质量评审及发布等全生命周期角色。
- **双向工程支持 (Forward & Reverse Engineering)**：既支持由产品概念正向推演架构与编码，也支持对存量代码进行逆向分析、资产盘点与设计重构。
- **状态持久化与断点续传 (Checkpoint & Resume)**：工程决策、演进状态与阶段证据持久化至 Markdown，任意会话中断后均可平滑恢复上下文。
- **多级质量门禁 (Quality Gates)**：在关键交付节点设立澄清关卡、架构评审与集成验证，严控技术债务与幻觉风险。

---

## 适用场景

| 场景 | 说明 |
|---|---|
| **从零孵化新项目** | 从产品构想、需求 PRD、设计稿或接口规范出发，分阶段推进架构设计与代码落地 |
| **接管现有代码库** | 针对存量复杂项目进行逆向架构还原、测试补全、技术债务梳理及功能迭代 |
| **日常单点研发任务** | 专注于特定 Feature、Bug Fix、性能优化、代码重构或单模块 Code Review |
| **高规范度工程项目** | 需要严格变更追溯 (Traceability)、质量证据链与安全合规门禁的长期维护系统 |

---

## 目录结构

```text
.
├── CLAUDE.md                   # 框架总控编排规则与工程守则
├── .claude/
│   ├── agents/                 # 14 个专业工程角色定义
│   ├── rules/                  # 架构、代码、质量、变更等持久化工程约束
│   └── skills/                 # 需求导入、路径推导、代码评审等工程技能集
├── config/
│   ├── project.md              # 项目核心配置文件
│   └── project.example.md      # 配置参考范例
├── input/                      # 原始输入资产池（需求、旧代码、团队规范、接口定义等）
├── artifacts/                  # 阶段性持久化交付成果（PRD、ADR、设计文档、测试报告等）
├── state/                      # 状态工作账本与 Checkpoint 断点快照
├── output/                     # 最终交付导出的打包产物
├── docs/                       # 框架模型与机制说明文档
└── *.md                        # 各典型工作流入口交互模板
```

---

## 快速开始

### 1. 引入框架
将本仓库文件复制到目标项目根目录中，保留核心编排规则及角色配置。

### 2. 准备项目输入
- 将已有产品资料、需求文档、设计图或规范放入 [`input/`](input/README.md)（团队规范统一放入 [`input/standards/`](input/standards/README.md)）。
- 若项目包含存量代码，可直接保留在根目录原有位置，无需搬迁。

### 3. 配置项目基线
编辑 [`config/project.md`](config/project.md)，配置基础参数（未确定项保留 `auto`）：

```markdown
Target Stage: auto         # 目标阶段：requirements / architecture / implementation / auto 等
Workflow Mode: AUTO        # 严格度：LIGHTWEIGHT / STANDARD / STRICT / AUTO
Execution Mode: GATED_AUTO # 自治级别：INTERACTIVE / GATED_AUTO / FULL_AUTO
```

### 4. 启动与执行
在项目根目录启动 Claude Code：

```bash
claude
```

并根据当前场景输入引导指令（建议直接引用模板）：

```text
读取 START_PROJECT.md 并执行。
```

---

## 核心工作流

框架针对典型的研发场景提供了开箱即用的引导模板：

| 场景 | 对应模板 | 引导指令 | 说明 |
|---|---|---|---|
| **启动新项目** | [`START_PROJECT.md`](START_PROJECT.md) | `读取 START_PROJECT.md 并执行。` | 触发资产盘点、需求澄清并推导开发路径 |
| **恢复/继续项目** | [`CONTINUE_PROJECT.md`](CONTINUE_PROJECT.md) | `读取 CONTINUE_PROJECT.md 并执行。` | 基于 Checkpoint 检查工作树变更并断点续传 |
| **接手既有项目** | [`ADOPT_EXISTING_PROJECT.md`](ADOPT_EXISTING_PROJECT.md) | `读取 ADOPT_EXISTING_PROJECT.md 并执行。` | 对存量工程执行逆向架构分析、依赖识别与风险评估 |
| **执行独立任务** | [`EXECUTE_TASK.md`](EXECUTE_TASK.md) | 填写模板任务块后执行 | 针对独立 Bug、Feature 或重构快速评估并执行必要路径 |

---

## 核心配置机制

### 1. 目标阶段 (`Target Stage`)
用于限定当前轮次的交付边界，避免过度发散：
- `requirements`：完成可验证需求规格后暂停；
- `architecture`：完成架构方案、接口契约与关键 ADR 决策后暂停；
- `implementation`：完成业务编码及阶段验证后暂停；
- `testing` / `review` / `release`：完成指定测试覆盖、代码评审或发布准备；
- `auto`：根据任务目标自动收敛。达到边界后框架生成状态快照并安全暂停。

### 2. 工作流严格度 (`Workflow Mode`)
- `LIGHTWEIGHT`：适用于脚本开发、局部缺陷修复与小重构；保证基本验证，流程最简。
- `STANDARD`：适用于标准的多模块业务功能开发。
- `STRICT`：适用于高安全性、核心业务、复杂数据迁移或跨团队协作项目。
- `AUTO`（默认）：基于任务影响面与风险自动定级。

### 3. 资产与产物权责划分

| 目录 | 职责 | 备注 |
|---|---|---|
| [`input/`](input/README.md) | 外部原始资料池 | 存放需求、设计稿、旧资料或规范，作为只读证据来源 |
| `artifacts/` | 过程工程产出物 | 存放经过验证的规格文档、ADR、设计说明、测试报告 |
| `state/` | 状态与断点记录 | 记录阶段标记、变更影响分析及断点 Checkpoint |
| `output/` | 最终用户交付物 | 仅存放用户明确要求导出的可交付制品或打包文件 |

---

## 进阶参考与文档

- [框架总体概览 (Framework Overview)](docs/framework-overview.md)
- [产出物规范模型 (Artifact Model)](docs/artifact-model.md)
- [状态流转模型 (State Model)](docs/state-model.md)
- [阶段质量关卡 (Gate Model)](docs/gate-model.md)
- [智能体角色地图 (Agent Role Map)](docs/agent-role-map.md)
- [框架完整架构设计 (Framework Architecture)](FRAMEWORK_ARCHITECTURE.md)
- [未来运行时规划 (Future Runtime Boundary)](docs/future-runtime.md)

---

## 设计边界

当前 V1 版本依托 Claude Code 与结构化 Markdown 规范，实现了轻量化的角色协同、产物传递与质量把控。关于确定性状态事务、自动化并发合并及外部 CI/CD 插件化集成（Hook / MCP）等扩展能力的演进规划，详见 [`docs/future-runtime.md`](docs/future-runtime.md)。

---

## License

本项目采用 [MIT License](LICENSE) 授权开源。
