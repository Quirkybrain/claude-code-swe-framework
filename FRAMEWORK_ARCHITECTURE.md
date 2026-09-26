# Claude Code AI Software Engineering Framework

## Phase 0 — Framework Architecture Proposal

> 状态：Architecture Validation Only
>
> 日期：2026-09-20
>
> 设计依据：`design.md` 全文、任务约束、Claude Code 官方文档
>
> 本机 Claude Code：`2.1.278`

---

## 0. Phase 0 结论

本项目应实现为一套可复制到任意真实软件项目根目录的 **Claude Code 软件工程工作模板**。Claude Code 主会话是执行引擎和 Stage Orchestrator；Framework 本身不是 Runtime，不拥有常驻进程、生命周期引擎、工作流服务器或 Agent SDK 应用。

V1 的核心不是“执行一条预设 Agent Chain”，而是维护可验证的 Artifact、Artifact Dependency、状态和 Gate，由主 Claude 根据用户目标、已有资产、风险及缺口计算 **Minimum Necessary Path**，再按需选择 Agent 和 Skill。

本提案只定义未来 Framework 的结构。Phase 0 不创建下述目录或文件中的任何实体，只创建本提案文件。

### 0.1 明确不属于 V1 的内容

V1 不创建也不依赖：

- `src/`
- `package.json`
- `main.ts` / `main.py`
- workflow / artifact / state engine
- database
- CLI runtime
- server / daemon
- Node.js 或 Python Application
- Agent SDK Application

### 0.2 Source of Truth 缺口

`design.md` 已完整读取至第 2457 行。文件在 `# 68. Stage Gate` 的空代码块处结束，Stage Gate 的后续判断内容缺失。本提案只使用前文已经明确给出的 Gate、Target Stage、Artifact 和状态语义，不补写不存在的设计结论。Phase 1 前应由设计所有者补全或确认该截断内容。

---

## 1. Framework 定位

### 1.1 真正定位

Framework 是：

> 一套通过 Claude Code 原生 Markdown 配置、项目输入约定、Artifact 模板和持久化工作状态，约束 Claude Code 采用软件工程方法工作的可复制模板。

主要控制面：

- `CLAUDE.md`：主会话的常驻原则与编排协议。
- `.claude/agents/*.md`：专业任务的执行者定义。
- `.claude/skills/*/SKILL.md`：可重复调用的过程。
- `.claude/rules/*.md`：持续成立或路径相关的约束。
- Markdown Templates：Artifact、Gate、State 的统一结构。
- Project Configuration：用户控制目标、严格度、自主度与技术约束。
- `input/`：项目当前拥有的一切资产，而不只是需求。
- `artifacts/` 与 `state/`：Agent 间接口、证据和跨会话恢复依据。

### 1.2 最终使用模型

```text
Framework Template
        ↓ copy
Real Project Root
        ↓
input/ + config/project.md + input/standards/
        ↓
Start Claude Code
        ↓
Main Claude = Stage Orchestrator
        ↓
Project Intake → Artifact Inventory → Validation
        ↓
Gap Analysis → Risk / Complexity Assessment
        ↓
Adaptive Workflow → Minimum Necessary Path
        ↓
Agent / Skill Selection
        ↓
Artifact Production / Software Engineering Work
        ↓
Gate → Continue | Replan | Clarify | Pause at Target
```

### 1.3 核心不变量

1. Agent 不是流程连接点；Artifact Dependency 才是。
2. Logical Role 不等于 Agent。
3. 完整生命周期是能力上限，不是每次执行清单。
4. 复用并验证已有 Artifact，优先于重新生成。
5. 只执行到目标所必需的最小合理路径。
6. 用户指定的配置和标准优先于自动推断。
7. 重大产品、架构、数据、安全、部署和成本决策不得静默推断。
8. 所有代码变更都必须重新 Build / Test / Verify；旧验证随相关变更失效。
9. 只有 `STABLE` Component 才能参与下一层 Integration。
10. 到达 Target Stage 是 `PAUSED_AT_STAGE`，不是虚假的项目完成。

---

## 2. design.md 语义分类

| 分类 | 应进入的 Framework 层 | 主要内容 |
|---|---|---|
| A. Always-on Principles | `CLAUDE.md` + 全局 Rules | Asset/Artifact Driven、Minimum Necessary Path、Adaptive Workflow、Reuse Before Regenerate、Contract First、Process Budget、变更后验证、不得虚报完成 |
| B. Orchestrator Responsibilities | `CLAUDE.md` | 读取目标、Intake、Gap Analysis、风险评估、路径计算、Agent/Skill 路由、Gate、停止/回退/恢复 |
| C. Agent Responsibilities | `.claude/agents/*.md` | 专业分析、设计、开发、测试、Review、集成、验证、文档和发布工作 |
| D. Reusable Workflow Skills | `.claude/skills/*/SKILL.md` | Intake、Artifact Validation、Gap Analysis、Change Impact、RCA、Gate Evaluation 等重复 Procedure |
| E. Persistent Rules | `.claude/rules/*.md` | 测试义务、追踪性、Artifact 状态、写入边界、澄清条件、安全、集成条件 |
| F. Artifact Models | `templates/artifacts/` + `artifacts/` | Inventory、Requirements、Domain/UML、Architecture、ADR、Contract、Plan、Code Evidence、Test/Review/Release Report |
| G. State Models | `templates/state/` + `state/` | Project、Artifact、Component、Task、Stage、Question、Checkpoint 状态 |
| H. Gate Models | `templates/gates/` + Gate Skills + Rules | Clarification、Artifact Validation、Component Quality、Integration、Stage Gate |
| I. User Configuration | `config/project.md` | Target Stage、Workflow Mode、Execution Mode、技术栈、约束、偏好、禁止项 |
| J. Input Conventions | `input/` | 任意项目资产池、可选推荐目录、内容识别优先、Standards 约定 |
| K. Future Runtime Capabilities | 未来 `docs/future-runtime.md` | 确定性 enforcement、事务状态、自动失效、可靠并发合并、审计、外部系统和常驻调度 |

分类原则：事实与持续约束不塞进 Skill；多步 Procedure 不塞进 `CLAUDE.md`；专业责任不为每个 Logical Role 单独创建 Agent。

---

## 3. 最终目录树

以下是 Phase 1 及后续应逐步建立的目标树，不是 Phase 0 要创建的文件列表。

```text
project-root/
├── CLAUDE.md
├── README.md
├── START_PROJECT.md
├── CONTINUE_PROJECT.md
├── ADOPT_EXISTING_PROJECT.md
├── EXECUTE_TASK.md
├── config/
│   ├── project.md
│   └── project.example.md
├── .claude/
│   ├── settings.json                  # 可选；只放 Claude Code 原生设置
│   ├── agents/
│   │   ├── asset-analyst.md
│   │   ├── requirements-analyst.md
│   │   ├── system-modeler.md
│   │   ├── solution-architect.md
│   │   ├── experience-designer.md
│   │   ├── delivery-planner.md
│   │   ├── implementation-engineer.md
│   │   ├── test-engineer.md
│   │   ├── quality-reviewer.md
│   │   ├── integration-engineer.md
│   │   ├── debug-specialist.md
│   │   ├── system-verifier.md
│   │   ├── technical-writer.md
│   │   ├── release-engineer.md
│   │   └── repository-manager.md
│   ├── skills/
│   │   ├── project-intake/SKILL.md
│   │   ├── artifact-validation/SKILL.md
│   │   ├── workflow-assessment/SKILL.md
│   │   ├── gap-analysis/SKILL.md
│   │   ├── minimum-path/SKILL.md
│   │   ├── clarification-gate/SKILL.md
│   │   ├── architecture-decision/SKILL.md
│   │   ├── component-planning/SKILL.md
│   │   ├── implement-component/SKILL.md
│   │   ├── adaptive-testing/SKILL.md
│   │   ├── quality-gate/SKILL.md
│   │   ├── integration-gate/SKILL.md
│   │   ├── code-review/SKILL.md
│   │   ├── failure-diagnosis/SKILL.md
│   │   ├── failure-escalation/SKILL.md
│   │   ├── change-impact/SKILL.md
│   │   ├── reverse-engineering/SKILL.md
│   │   ├── traceability/SKILL.md
│   │   ├── stage-gate/SKILL.md
│   │   ├── framework-checkpoint/SKILL.md
│   │   └── framework-resume/SKILL.md
│   └── rules/
│       ├── workflow.md
│       ├── clarification.md
│       ├── artifacts.md
│       ├── architecture.md
│       ├── coding.md
│       ├── quality.md
│       ├── integration.md
│       └── change-management.md
├── input/
│   ├── README.md
│   ├── project/
│   ├── requirements/
│   ├── references/
│   ├── competitors/
│   ├── design/
│   ├── uml/
│   ├── architecture/
│   ├── api/
│   ├── data/
│   ├── existing/
│   ├── tests/
│   ├── standards/
│   │   └── README.md
│   └── other/
├── artifacts/
│   ├── 00-intake/
│   ├── 10-product-requirements/
│   ├── 20-models-design/
│   ├── 30-architecture-contracts/
│   ├── 40-planning/
│   ├── 50-implementation-evidence/
│   ├── 60-quality/
│   ├── 70-verification-acceptance/
│   ├── 80-documentation-release/
│   ├── decisions/
│   └── traceability/
├── state/
│   ├── project-state.md
│   ├── artifact-registry.md
│   ├── dependency-graph.md
│   ├── component-registry.md
│   ├── task-graph.md
│   ├── gate-log.md
│   ├── questions-and-decisions.md
│   ├── change-impact.md
│   └── session-handoff.md
├── templates/
│   ├── artifacts/
│   ├── gates/
│   └── state/
├── output/                            # 用户明确要求导出的最终成果；非 Agent 交换总线
└── docs/
    ├── framework-overview.md
    ├── artifact-model.md
    ├── state-model.md
    ├── gate-model.md
    ├── agent-role-map.md
    └── future-runtime.md              # 记录非 Markdown 可靠能力
```

目录约束：

- 真实项目的业务代码保留其原有布局；Framework 不要求把代码移入 `artifacts/`。
- `artifacts/` 保存工程 Artifact 和代码变更的验证证据，不复制整个业务源码。
- `state/` 是 Markdown 工作账本，不是数据库或 Runtime State Engine。
- `output/` 只保存用户要交付/导出的成果，不作为 Agent 间主要通信方式。
- `docs/future-runtime.md` 记录能力边界，不代表 Phase 1 实现了 Hook、MCP 或 Runtime。

---

## 4. Adaptive Workflow 与 Minimum Necessary Path

### 4.1 编排算法（由主 Claude 推理执行）

1. 读取 `config/project.md`、用户当前请求和已有 `state/`。
2. 执行 Project Intake；按内容而不是仅按路径/扩展名识别资产。
3. 建立或更新 Artifact Inventory，并对目标相关 Artifact 执行 Validation。
4. 规范化 Target Stage / Target Artifact；若缺失且会改变工作范围，进入 Clarification Gate。
5. 从目标沿 Artifact Dependency 反向查找必需上游。
6. 剪枝所有 `VALID` 且足以支持目标的节点；对 `PARTIAL`、`UNVERIFIED`、`STALE`、`INVALID` 分别选择 Supplement、Revalidate 或 Regenerate。
7. 按 Complexity、Risk、Impact、Project/Task Size、维护周期、已有资产和目标选择 Task Workflow Level。
8. 生成 Minimum Necessary Path，仅调度依赖已满足的节点；独立节点才可并行。
9. 为每个节点选择“专业 Agent + 必要 Skill + 适用 Rules”，而不是选择固定的下一个 Agent。
10. 产出 Artifact 和证据，执行相应 Gate，并同步 Registry、Dependency、Traceability 和 Handoff。
11. Gate 失败时先做 Root Cause Analysis，在正确层级修复或回退，不进入无界本地补丁循环。
12. 达到 Target Stage 后写入 `PAUSED_AT_STAGE` 并停止；只有用户目标明确为完整交付且 Acceptance/Release 条件满足时，才可报告相应完成状态。

### 4.2 Forward / Reverse Engineering

- Forward：Requirement → Model/Design → Architecture/Contract → Component → Code → Test → Verification。
- Reverse：Existing Code/Test/Deployment Evidence → Structure → Contract → Architecture/Model → Inferred Requirement。
- 两种方向共享同一 Artifact Registry；推断得到的 Artifact 初始状态不得高于 `UNVERIFIED`，直到有证据或用户确认。

### 4.3 任意 Stage 进入

Stage 不是强制顺序游标。入口由用户已有 Artifact 和目标共同决定。例如已有 Code 可直接进入 Review、Testing、Reverse Modeling 或 Maintenance；已有 Test Report 可直接进入 Failure Diagnosis。缺失的上游只有在确实阻塞目标时才补齐。

### 4.4 Progressive Formality

| Level | 适用 | 最小质量要求 | 通常按需增加 |
|---|---|---|---|
| `LIGHTWEIGHT` | 小功能、Bug、脚本、小重构 | Understand、Implement、Build、Relevant Test、Quick Review、Checkpoint | 不默认生成完整 SRS/UML/ADR/Test Plan |
| `STANDARD` | 普通项目、多模块应用 | 必要需求与设计、Architecture/Component Plan、Implementation、Testing、Integration、Review | 关键 Contract、ADR、Traceability |
| `STRICT` | 高风险、安全敏感、大型或长期系统 | 完整证据链、多层 Review/Test、Architecture Compliance、Acceptance | SRS、完整建模、安全/性能测试、正式发布证据 |

`AUTO` 由主 Claude选择并记录理由。Project Level 是基线，Task Level 可因单项风险升级或降级；流程成本不应明显超过其降低的风险。

---

## 5. Agent Pool

主 Claude 不定义为 `.claude/agents/` 中的 Agent；它是唯一 Stage Orchestrator。当前 15 个 Agent 是能力池，不是调用链。Phase 2 增加跨层诊断的 `debug-specialist`；仓库治理增加跨阶段的 `repository-manager`，负责 Git 基线和提交状态，不增加生命周期 Stage；其余 Phase 0 分组保持不变。

| Agent | 聚合职责 | 典型输入 / 输出 | 工具与写权限意图 | 使用理由 |
|---|---|---|---|---|
| `asset-analyst` | Intake、资产内容识别、已有 Artifact/Code/Test 盘点 | `input/`、repo → Inventory、冲突、证据索引 | 只读项目；通过 Handoff 返回 Intake 结果 | 高读取量需要上下文隔离；不应修改业务代码 |
| `requirements-analyst` | 产品理解、需求获取/分析/规格、验收标准 | 产品资料 → Requirement/Constraint/Assumption | 读；只写需求 Artifact | 产品语义高度内聚，需集中持久化用户回答 |
| `system-modeler` | Domain、UML/软件建模、结构逆向 | Requirement/Code → Domain/UML/Model | 读；只写模型 Artifact | 正逆向共享建模上下文和工具需求 |
| `solution-architect` | 软件架构、详细设计、数据/API/安全设计 | Valid Requirements/Models → Architecture、Contract、ADR | 读；只写设计 Artifact | 决策彼此耦合，应统一权衡；不实现业务代码 |
| `experience-designer` | UI/UX 与用户流程 | Requirement、UI 资产 → UX Flow、UI Spec | 读；写体验 Artifact | 视觉/交互语义独立且按需出现 |
| `delivery-planner` | Project/Component Planning、Task/Component Graph | Architecture/Contract → Plan、Milestone、Integration Point | 读；写计划/状态 | 依赖、并行度和 Gate 规划高度内聚 |
| `implementation-engineer` | Component 实现、重构、Bug 修复、代码级维护 | Contract/Task → Code、Build/Test Evidence | 读写代码、执行构建测试 | 唯一通用业务代码写入角色；实现后不能自行宣布最终通过 |
| `test-engineer` | Test Design/Execution、Contract/Regression/Performance Test | Requirement/Contract/Code → Test、Report | 可写测试；执行测试 | 测试上下文和测试资产独立，避免测试沦为开发附注 |
| `quality-reviewer` | Code/Architecture/Security/Performance Review | Diff、Design、Evidence → Review Findings/Verdict | 只读代码，可运行只读检查；不修复 | 保持 Review 与作者职责分离 |
| `integration-engineer` | Contract Validation、增量集成、集成诊断 | `STABLE` Components → Integrated Unit、Integration Report | 受控代码写入和测试 | 集成修改跨 Component，需要独立全局上下文 |
| `debug-specialist` | Root Cause Analysis、Failure Classification、Repeated Failure Escalation | Failure Evidence → Root Cause、Responsible Layer、Repair Direction | 默认只读；不实施修复 | 将跨层诊断与本地修补分离，防止无限 Local Patching |
| `system-verifier` | Traceability、一致性、System Verification、Acceptance | 全链路 Artifacts → Verification/Acceptance Report | 只读产品与代码；写报告 | 工程正确性与用户价值验证需独立于实现 |
| `technical-writer` | 用户/开发/运维文档 | Valid Artifacts/Code → Documentation | 只写文档 | 文档面向读者，避免与发布权限混合 |
| `release-engineer` | Release/Deployment 计划、可发布性验证和受控执行 | Stable Build、Release Criteria → Release Evidence | 构建/部署工具；外部副作用需 Gate | 发布具有高副作用和专门权限边界 |
| `repository-manager` | Git 基线、定向提交、仓库状态与快照引用核对 | Task/Checkpoint、适用的 `input/` Git 规范 → Commit/Status Evidence | Git 操作；不修改产品语义 | 使提交与恢复证据成为可检查的跨阶段职责 |

表中的“写权限”在纯 Markdown V1 中首先是行为约束。仅靠 Agent prompt 无法强制路径级写隔离；需要确定性 enforcement 时属于 Hook/权限系统的后续能力。

### 5.1 Agent 选择规则

- 主 Claude按待产出的 Artifact 和所需权限选择 Agent。
- 一个 Agent 可以在不同 Stage 多次被调用；每次调用从明确输入 Artifact 和完成条件开始。
- Agent 不依赖上一个 Agent 的聊天历史；必须从 Artifact 路径、状态和 delegation message 获取任务上下文。
- 写业务代码的 Agent 与给出最终 Review Verdict 的 Agent 必须不同。
- 尽管本机 `2.1.278` 支持嵌套 Subagent，V1 默认仍不允许专业 Agent 再编排其他专业 Agent；这是保持主 Claude 单点编排、避免隐藏调用链的架构策略，而不是版本限制。
- 只读调查可并行；共享 working tree 的并行写默认禁止。

---

## 6. Logical Role → Agent Mapping

| design.md Logical Role | Primary Agent | Secondary / 说明 |
|---|---|---|
| Project Intake Role | `asset-analyst` | 主 Claude启动 Intake Skill 并接收 Inventory |
| Product Analyst | `requirements-analyst` | `experience-designer` 可补充用户旅程 |
| Requirement Analyst | `requirements-analyst` | — |
| Requirement Specification Role | `requirements-analyst` | `system-verifier` 后续检查可验收性 |
| Domain Analyst | `system-modeler` | `requirements-analyst` 提供业务语义 |
| UML / Modeling Role | `system-modeler` | 同时支持正向和逆向建模 |
| Software Architect | `solution-architect` | — |
| Detailed Design Role | `solution-architect` | `delivery-planner` 将其拆为 Component Graph |
| Data Architect | `solution-architect` | 数据专项通过 Skill/Rule 复用，不另建常驻 Agent |
| API / Interface Designer | `solution-architect` | Contract First Skill |
| UI / UX Designer | `experience-designer` | — |
| Security Architect | `solution-architect` | 高风险项目须由 `quality-reviewer` 独立安全 Review |
| Project Planner | `delivery-planner` | — |
| Component Planner | `delivery-planner` | — |
| Developer | `implementation-engineer` | — |
| Code Reviewer | `quality-reviewer` | 严禁同轮兼任代码修复者和最终批准者 |
| Test Designer | `test-engineer` | — |
| Test Engineer | `test-engineer` | — |
| Integration Engineer | `integration-engineer` | — |
| Performance Engineer | `test-engineer` | `quality-reviewer` 独立审查性能风险与证据 |
| Security Reviewer | `quality-reviewer` | 必要时使用安全专项 Rule/Skill |
| System Verification Role | `system-verifier` | — |
| Acceptance Role | `system-verifier` | 用户最终确认不能由 Agent 替代 |
| Documentation Role | `technical-writer` | — |
| Release / DevOps Role | `release-engineer` | 生产变更保持用户/组织权限 Gate |
| Maintenance Role | `implementation-engineer` | 主 Claude先做 Change Impact，再按问题路由相关专家 |

合并依据：

- Context Isolation：Intake、高容量探索、Review、System Verification 独立上下文。
- Responsibility Cohesion：需求语义、建模、架构决策、测试、集成分别内聚。
- Tool Requirements：只读 Review 与可写 Implementation 分离；高副作用 Release 独立。
- Write Permission：能批准的角色不直接修复其批准对象。
- Frequency：Data/API/Security Design 通过同一 Architect 与专项 Skill 组合，避免低频微型 Agent。
- Parallelization Value：只读分析和独立 Component 有价值；共享文件修改无价值且危险。
- Skill Reuse：RCA、Gap、Validation、Gate 等横跨角色的 Procedure 不固化为 Agent。

---

## 7. Skill Library

Skill 表示可重复调用的 Procedure。它可以由主 Claude或专业 Agent 使用，但不拥有长期职责，也不是流程节点。

| Skill | Procedure | 主要产物 |
|---|---|---|
| `project-intake` | 扫描资产、内容识别、分类、冲突发现、初始状态 | Asset/Artifact Inventory |
| `artifact-validation` | 检查完整性、一致性、正确性、时效性、目标适用性 | Reuse/Supplement/Revalidate/Regenerate Verdict |
| `workflow-assessment` | 评估 Complexity/Risk/Impact 等因素，分别确定 Project/Task Level | Workflow Decision |
| `gap-analysis` | 比较 Existing Artifacts 与 Target | Missing/Invalid/Stale Gap Set |
| `minimum-path` | 反向遍历依赖、剪枝有效节点、生成最小路径 | Path + Dependency Rationale |
| `clarification-gate` | 判断是否必须询问、组织选项、持久化回答 | Question/Decision/Constraint |
| `architecture-decision` | 比较重大技术方案并记录 Context、Options、Decision、Consequences | ADR |
| `component-planning` | System→Subsystem→Module→Component→Task；包含 Contract First | Component/Task Graph + Contracts |
| `implement-component` | 按 Contract 实现、Build、Test、Review、Gate | Code Change Evidence + Component State |
| `adaptive-testing` | 按变更风险选择 Unit/Contract/Integration/System 等范围 | Test Strategy/Report |
| `quality-gate` | 按 Workflow Level 检查 Component DoD 和证据 | Component Quality Verdict |
| `integration-gate` | Stable Check、Contract、Integration、Regression | Integration Verdict |
| `code-review` | 按风险选择 Quick/Code/Architecture/Security/Performance/Integration Review | Review Report |
| `failure-diagnosis` | 复现、假设、分类责任层并定位 Root Cause | RCA Report |
| `failure-escalation` | 停止重复修补、升级分析、必要时回退 Stage | Escalation/Rollback Decision |
| `change-impact` | 沿依赖寻找受影响下游并标记失效 | Impact Set + Revalidation Plan |
| `reverse-engineering` | 从 Code/Test/Runtime Evidence 推导结构与语义 | UNVERIFIED Model/Contract/Requirement |
| `traceability` | 维护 Requirement→Design→Architecture→Component→Code→Test | Traceability Matrix |
| `stage-gate` | 检查 Stage DoD、证据、Target 是否到达 | Continue/Rework/Clarify/Pause Verdict |
| `framework-checkpoint` | 持久化 Stage、Artifacts、Components、风险、当前路径和下一动作 | Recoverable Checkpoint |
| `framework-resume` | 校验 Checkpoint 与仓库漂移，重验证并重新规划 | Reconciled State + Next Action |

Phase 3 实现 21 个独立按需加载的 Skill。frontmatter 仅使用 Claude Code 官方支持的 `name` 和 `description`；触发条件写入 `description`，工程语义保留在正文中，不发明 YAML 字段。

`framework-checkpoint` 和 `framework-resume` 使用命名空间前缀，是因为 Claude Code `2.1.278` 已将 `/checkpoint` 用作 `/rewind` 的内置别名，并将 `/resume` 用作会话恢复命令。此前缀避免命令冲突，不改变 Framework Procedure 语义。项目级 `code-review` 则按官方优先级有意覆盖同名 bundled Skill。

---

## 8. Rule Set

Rule 表示持续成立的约束。无 `paths` 的 Rule 常驻；只有确实与文件范围相关时才使用官方 `paths` frontmatter。

| Rule | 约束 |
|---|---|
| `workflow.md` | Minimum Necessary Path、Process Budget、Adaptive Workflow、按需产物、无固定 Agent Chain、Target Stop |
| `clarification.md` | 自动推断边界、重大选择必须询问、Assumption/用户回答持久化、禁止重复询问 |
| `artifacts.md` | Artifact First、状态/依赖/验证/失效/Ownership/Handoff，以及双向 Traceability |
| `architecture.md` | Contract First、边界/内聚/耦合、前后端与 UI/业务分离、重大决策 ADR |
| `coding.md` | 遵守项目约束和既有风格、最小修改、Contract/安全/外部副作用边界 |
| `quality.md` | 修改后 Build/Test/Verify、Adaptive Testing、Testing 与 Review 分离、独立审查 |
| `integration.md` | 只有 `STABLE` 可集成；组合后重新执行 Contract/Integration/Regression 验证 |
| `change-management.md` | 上游变化的 Impact、下游失效、最小重验证、重新计算 Minimum Path |

Phase 4 将 Testing 与 Review 合并为一个质量主题，并将 Traceability 合并进 Artifact 主题，共 8 个常驻 Rule 文件；这样覆盖长期约束而不为目录对称制造额外上下文。

“必须发生”的机械行为不能只靠 Rule 保证。V1 Rule 是强提示约束；需要确定性阻断时应升级为 Hook/权限策略，而不是假称 Markdown 已强制执行。

---

## 9. Project Configuration

`config/project.md` 是用户控制面，`config/project.example.md` 提供填写示例；二者都不是可执行配置文件。建议模板字段：

```yaml
project:
  name: auto
  description: auto
  project_type: auto

objective:
  target_artifact: auto
  target_stage: auto
  stop_condition: target-stage

workflow:
  mode: AUTO              # AUTO | LIGHTWEIGHT | STANDARD | STRICT
  execution_mode: GATED_AUTO  # INTERACTIVE | GATED_AUTO | FULL_AUTO

technology:
  language: auto
  language_version: auto
  framework: auto
  frontend: auto
  backend: auto
  database: auto
  ui_framework: auto
  api_technology: auto
  build_tool: auto
  package_manager: auto
  test_framework: auto
  runtime_platform: auto
  deployment: auto

constraints:
  required_technologies: []
  forbidden_technologies: []
  preferences: []
  compliance: []

inputs:
  root: input/
  standards: input/standards/

outputs:
  requested: []
  format: auto
```

这是 Markdown 中的示意结构，不代表要由 YAML Runtime 解析。Phase 1 模板可采用 Markdown 表格或 YAML fenced block，但主 Claude必须按以下优先级解释：

```text
Explicit User Decision
> Project Configuration
> Validated Existing Artifact / User Standards
> Current User Request
> Architect Inference / Industry Convention
```

冲突不得静默覆盖。未指定字段为 `auto`；只有选择会显著影响产品、架构、数据、安全、部署、成本或大量后续工作时才询问。

---

## 10. Input Structure

### 10.1 语义

```text
input = 当前项目已经拥有的一切
input ≠ requirements only
```

用户可以完全不整理目录。推荐子目录只提升可读性，不能作为资产类型的唯一判断依据。

### 10.2 Intake 约定

每个发现的资产至少记录：

- Asset ID、原始路径、媒体/格式。
- 内容摘要和识别依据。
- 推断 Artifact Type 与 Lifecycle Stage。
- 完整度、可信度、冲突和敏感性。
- 可复用范围及目标相关性。
- 无法读取/解释时的限制说明。

文件名、扩展名和目录只提供初始提示；最终分类必须基于可访问的内容。二进制、专有格式或外部系统不可访问时，不得猜测内容，应记录为 `UNVERIFIED` 或进入 Clarification/Future Integration。

### 10.3 Standards

`input/standards/` 中的公司、团队、编码、测试、安全、API 和文档规范由 `solution-architect` 解释为 Project Constraints；其他 Agent 使用已解析约束，同时保留到原文件的引用。没有用户规范时，才根据语言、框架、项目类型和已有风格采用成熟惯例。

---

## 11. Artifact Structure

### 11.1 Artifact 是协作接口

Agent 的最终报告不是充分接口。可复用结论必须进入具有稳定路径和状态的 Artifact；聊天只负责委派、澄清和摘要。

每个正式 Artifact 建议包含统一 Header：

```text
Artifact ID
Artifact Type
Status
Version / Last Updated
Owner Agent
Source Assets
Upstream Dependencies
Downstream Consumers
Target Relevance
Assumptions
Validation Evidence
Open Issues
```

### 11.2 Artifact 状态

严格保留 design.md 定义：

| 状态 | 含义 | 可否直接作为下游依据 |
|---|---|---|
| `MISSING` | 不存在 | 否 |
| `PARTIAL` | 存在但不完整 | 仅在下游明确接受缺口时 |
| `UNVERIFIED` | 尚未确认可靠 | 否，先验证 |
| `VALID` | 已验证且足以支持当前目标 | 是 |
| `STALE` | 上游变化，需要重新验证 | 否 |
| `INVALID` | 已确认不可继续使用 | 否 |

`VALID` 是针对版本、依赖和目标的结论，不是永久属性。

### 11.3 Dependency 与 Traceability

`state/dependency-graph.md` 维护：

```text
Artifact
├── Requires
├── Can Reuse
├── Produces / Enables
├── Validation Rule
└── Downstream Impact
```

`artifacts/traceability/traceability-matrix.md` 维护例如：

```text
REQ-001 → USECASE-003 → DOMAIN-002 → UML-004
        → API-007 → COMPONENT-012 → TASK-031 → TEST-052
```

依赖图决定可执行顺序；Agent 名称不得出现在图中充当固定边。

### 11.4 Artifact 按需生成

仅当 Artifact 满足至少一项时生成：降低风险、帮助后续执行、支持协作/维护、满足当前目标、或用户明确要求。Lightweight 任务不因模板存在就生成完整 SRS/UML/ADR。

---

## 12. Runtime State Structure

这里的 Runtime State 指 **Claude Code 工作过程的持久化 Markdown 状态**，不是 Runtime Engine。

### 12.1 状态文件

| 文件 | 内容 |
|---|---|
| `project-state.md` | Current/Target Stage、Project/Task Workflow Level、Execution Mode、总体状态、最后 Checkpoint |
| `artifact-registry.md` | Artifact ID、路径、状态、版本、验证证据、依赖 |
| `dependency-graph.md` | Artifact 依赖和当前 ready/blocked 节点 |
| `component-registry.md` | Component 边界、Contract、状态、Build/Test/Review evidence |
| `task-graph.md` | Task 依赖、并行组、负责 Agent、DoD、Gate |
| `gate-log.md` | Gate 类型、输入版本、证据、Verdict、失败原因 |
| `questions-and-decisions.md` | 未决问题、用户回答、Assumption、对应 Requirement/ADR |
| `change-impact.md` | 上游变更、受影响下游、失效状态、重新规划 |
| `session-handoff.md` | 已完成、未完成、下一 ready 节点、阻塞、恢复路径 |

### 12.2 Project / Stage 状态

建议的工作状态：

```text
INITIALIZING
ACTIVE
BLOCKED_CLARIFICATION
BLOCKED_GATE
PAUSED_AT_STAGE
COMPLETED_TARGET
```

`COMPLETED_TARGET` 只表示用户定义目标已满足；它不等同于整个软件生命周期结束。`PAUSED_AT_STAGE` 保留 design.md 的核心语义。

### 12.3 Component 状态

严格保留：

```text
UNIMPLEMENTED → IMPLEMENTING → UNVERIFIED → STABLE
                                  ↘ FAILED
```

任何 `STABLE` Component 的代码、Contract 或相关上游发生变化后立即回到 `UNVERIFIED`；旧验证证据保留用于审计，但不得继续作为当前 PASS 证据。

### 12.4 Gate Verdict

建议统一为：

```text
PENDING | PASS | FAIL | BLOCKED | USER_DECISION_REQUIRED
```

每个 Verdict 必须绑定输入 Artifact 版本和证据路径。Markdown V1 的状态更新是约定式、非事务性的；可靠原子更新属于未来能力。

---

## 13. Gate Models

| Gate | 核心问题 | 触发点 | PASS 证据 | FAIL 后动作 |
|---|---|---|---|---|
| Clarification Gate | 是否需要用户决定？ | 重大歧义/冲突/高影响选择 | 用户回答已写入 Requirement/Constraint/ADR | 暂停相关路径，不猜测 |
| Artifact Validation Gate | Artifact 是否足够可靠且适合当前目标？ | 复用任何已有成果前 | Validation Verdict + 来源/版本 | Supplement/Revalidate/Regenerate |
| Component Quality Gate | Component 是否达到 DoD？ | 实现或修改后 | Build、Required Tests、Review、Acceptance Criteria | RCA、修复、重新验证 |
| Integration Gate | 组合后是否仍正确？ | 合并两个或更多 Stable 单元 | Contract、Integration、Regression 证据 | 诊断 Interface/Contract/Design 层级 |
| Stage Gate | 当前 Stage 是否完成且是否达到目标？ | 主要 Stage 结束 | Stage DoD + Artifact 状态 + 未决风险 | Rework/Clarify/Rollback；到目标则 Pause |

Gate 是基于证据的决策模型，不是 Agent。`stage-gate` Skill 提供评估 Procedure，Rule 规定何时必须执行，主 Claude做最终编排决定。

---

## 14. Agent / Skill / Rule 职责边界

| 类型 | 回答的问题 | 生命周期 | 是否拥有 Artifact | 示例 |
|---|---|---|---|---|
| Agent | 谁以专业角色完成任务？ | 按需实例化，独立上下文 | 负责产出，但状态归项目 | Developer、Architect、Reviewer |
| Skill | 怎样重复执行一个过程？ | 调用时加载 | 规定过程和输出格式，不长期拥有 | Gap Analysis、RCA、Stage Gate |
| Rule | 什么约束持续成立？ | 常驻或路径触发 | 约束所有相关产出 | 修改代码后必须验证 |
| Orchestrator | 当前为何做什么、调用谁、何时停止？ | 主会话全程 | 维护全局状态和路径 | Minimum Necessary Path |
| Artifact | Agent 间交换什么可验证结果？ | 跨 Agent/Session 持久存在 | 是实际协作接口 | Requirement、Contract、Test Report |

判定顺序：

1. 如果是专业责任与独立上下文，定义 Agent。
2. 如果是跨角色复用的多步方法，定义 Skill。
3. 如果无论谁执行都必须成立，定义 Rule。
4. 如果是可验证的中间/最终结果，定义 Artifact。
5. 如果是全局路径、选择与停止决策，保留在主 Orchestrator。

---

## 15. Claude Code 原生能力映射

本节以 2026-09-20 的 Anthropic 官方文档为格式依据，并以本机 `2.1.278` 作为已核验能力基线。Framework 若需要支持更早版本，应在 Phase 1 明确另设兼容范围，不能默认向下兼容。

| Framework 需要 | Claude Code 原生机制 | 方案与限制 |
|---|---|---|
| 主编排规则 | `CLAUDE.md` | 每个 session 启动加载；应保持精炼，官方建议目标少于 200 行；长 Procedure 下沉 Skill |
| 持续/路径规则 | `.claude/rules/*.md` | Markdown 递归发现；无 frontmatter 常驻；只使用官方 `paths` frontmatter 做条件加载 |
| 专业执行者 | `.claude/agents/*.md` | YAML frontmatter + Markdown system prompt；`name`、`description` 为官方必需字段 |
| Agent 工具边界 | Agent `tools` / `disallowedTools` | 使用真实工具名；省略 `tools` 会继承可用工具，不等于最小权限 |
| Agent 上下文隔离 | Subagent 独立 context window | 不继承主会话历史或已调用 Skill；委派必须给出 Artifact 路径、目标和 DoD |
| Agent 获取项目规则 | CLAUDE.md / Rules 继承 | 官方当前自定义 subagent 默认加载项目说明；仍不得依赖聊天隐式上下文 |
| Agent 过程复用 | Agent `skills` | 可预加载完整 Skill；只预加载确实必要者，避免上下文膨胀 |
| Agent 持久记忆 | Agent `memory: user|project|local` | 本机版本支持该字段，但 Agent memory 不作为权威项目状态；权威状态写入 `state/` 和 Artifact |
| Agent 文件隔离 | `isolation: worktree` | Git 项目可用；Worktree 是独立 checkout/branch，不含未提交改动，且不会自动完成业务层合并 |
| 可复用 Procedure | `.claude/skills/<name>/SKILL.md` | `description` 帮助自动选择，也可由用户 `/name` 调用；Skill body 使用时才加载 |
| 用户主动/模型主动控制 | Skill `disable-model-invocation` / `user-invocable` | 用官方字段控制调用；不创建自定义 invocation 字段 |
| 工具预批准 | Skill `allowed-tools` | 只是调用该 Skill 的临时预批准，不是长期权限或确定性安全边界 |
| 并行只读研究 | 并行 subagents | 独立任务可并行，结果返回主会话汇总 |
| 跨会话恢复 | 文件状态 + Claude session resume | Framework 以显式 Artifact/State 为准，不仅依赖会话历史或 auto memory |

### 15.1 Agent frontmatter 兼容基线

Phase 1 在本机 `2.1.278` 上优先使用已核验存在且足够表达 V1 的字段：

```yaml
name: example-agent
description: When and why the orchestrator should use this agent
tools: Read, Grep, Glob
model: inherit
permissionMode: default
skills:
  - artifact-validation
memory: project
isolation: worktree
```

不是每个 Agent 都要使用全部字段。例如 Review Agent 不需要 memory，普通串行 Agent 不需要 worktree。Phase 1 应根据最小权限逐个选择。

本机 `2.1.278` 已覆盖官方当前文档中注明截至 `2.1.271` 才可用的 Agent frontmatter 能力，包括 `maxTurns`、`mcpServers`、`hooks`、`background`、`omitClaudeMd`、`effort` 等。Phase 1 可以按实际需要使用，但仍应坚持最小配置：不因字段可用就批量加入所有 Agent，也不使用官方文档未定义的字段。任何官方文档注明需要高于 `2.1.278` 的后续能力，都必须先升级并实测。

### 15.2 Skill frontmatter 兼容基线

```yaml
name: gap-analysis
description: Compare validated existing artifacts with a target and identify only the missing dependencies.
```

Claude Code `2.1.278` 还支持官方文档列出的可选字段，但 Phase 3 不需要它们。Artifact schema、Stage、Gate 和权限语义属于 Skill body、Template 和 State。

### 15.3 Subagent 与 Worktree 行为边界

- Subagent 是同一 session 内的隔离执行上下文，结果回到主 Claude；它不是常驻服务。
- 本机 `2.1.278` 支持嵌套 Subagent；V1 仍由主 Claude 独占工作流编排权。专业 Agent 默认不获得 `Agent` 工具，除非未来有明确、可审计且不会形成隐藏 Agent Chain 的用例。
- Worktree 隔离解决文件碰撞，不解决 Contract 冲突、状态同步、自动合并或验证。
- Worktree 默认基线可能来自默认分支而非主会话未提交内容；使用前必须确认 base 与输入 Artifact 版本。
- V1 默认允许并行只读分析；并行写只有在 Component 独立、Contract 已稳定、工作区隔离且整合负责人明确时才启用。

### 15.4 官方参考

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)

---

## 16. V1 可纯 Markdown + Claude Code 原生能力实现

可以合理实现：

- Project Intake 和内容驱动的资产分类。
- Artifact Inventory、Dependency 记录和统一状态模型。
- Gap Analysis、Minimum Necessary Path 和 Adaptive Workflow 的推理式规划。
- 任意 Stage 进入、Target Stage 停止与后续恢复。
- Forward / Reverse Engineering。
- Agent Pool 的按需选择，不使用固定 Agent Chain。
- Skill 的按需 Procedure 复用。
- Rule 的常驻或路径相关约束。
- Clarification 问题、Assumption 和用户决定的文件持久化。
- Reuse Before Regenerate 和 Artifact Validation。
- Contract First、Component Graph、Task Graph 与增量集成计划。
- 代码修改后的 Build/Test/Review/Gate 工作协议。
- 基于 Markdown 的 Traceability、ADR、Gate Log、Checkpoint 和 Handoff。
- Git 项目中可选的 Claude Code 原生 Worktree 隔离。
- 基于 Artifact/State 文件的跨会话可恢复性。

“可实现”表示 Claude Code 可以按指令推理并更新文件，不表示具备事务性、确定性或不可绕过的 enforcement。

---

## 17. V1 无法可靠实现，未来需要 Hook / MCP / Runtime 的能力

下列内容由 `docs/future-runtime.md` 持续记录，但 V1 不实现：

### 17.1 Hook 适合的确定性能力

- 每次代码 Edit 后自动执行或强制要求格式化、静态检查、相关测试。
- 在缺少验证证据时阻止提交、发布或 Stage PASS。
- 检测业务代码/Contract 变化并自动将对应 Component/Artifact 标为 `UNVERIFIED`/`STALE`。
- 阻止 Agent 写入不属于其职责的路径。
- 记录不可遗漏的审计事件和 Gate 触发。
- 在生产部署、secret 文件和破坏性命令前做机械拦截。

### 17.2 MCP 适合的外部能力

- 读取 Figma、Issue Tracker、知识库、云平台、监控、测试管理系统等外部 Artifact。
- 解析 Claude Code 本身无法可靠读取的专有格式。
- 将 Requirement、Task、Test、Release 状态同步到外部系统。
- 获取需要认证和结构化查询的运行时/生产证据。

### 17.3 独立 Runtime 才适合的能力

- Artifact Dependency Graph 的事务存储、一致性约束和自动增量计算。
- 多 Agent 并发锁、租约、任务队列、可靠重试和 exactly-once 状态迁移。
- 自动合并多个 Worktree、冲突解决、集成分支管理和回滚编排。
- 长期常驻调度、daemon、事件总线、跨机器 Agent 协调。
- 强一致 Checkpoint、崩溃恢复、不可篡改审计和历史查询。
- 大规模 Traceability 图查询、影响分析和状态派生。
- 确定性 Policy Engine、权限系统和合规证明。
- 无人值守生产部署与外部副作用的可靠补偿事务。

### 17.4 V1 必须诚实暴露的限制

- Markdown Rule 是提示，不是强制策略。
- 主 Claude 的图遍历和状态更新是推理行为，不是程序化算法保证。
- 多文件状态可能在中断时暂时不一致，需在恢复时 Reconcile。
- Agent memory 和 auto memory 不是项目权威数据源。
- 原生 Worktree 只隔离文件，不自动把产出整合回主工作区。
- FULL_AUTO 仍不能替代无法可靠推断的用户产品意图和高风险授权。

---

## 18. Phase 0 Definition of Done

- [x] 完整阅读 `design.md`，并记录其 EOF 截断事实。
- [x] 确认这是 Claude Code Framework Template，不是 Runtime 软件。
- [x] Phase 0 将 26 个 Logical Roles 合并为 13 个职责集；Phase 2 为失败升级增加独立 `debug-specialist`；仓库治理增加 `repository-manager`，当前共 15 个 Agent。
- [x] 明确分离 Agent、Skill、Rule、Artifact 与 Orchestrator。
- [x] 未设计固定 Agent Chain。
- [x] Artifact Dependency 是主要流程连接机制。
- [x] 支持 Adaptive Workflow 和动态流程升降级。
- [x] 支持 Minimum Necessary Path 与 Generate on Demand。
- [x] 支持任意 Stage 进入和 Target Stage 停止。
- [x] 支持 Forward / Reverse Engineering。
- [x] 核验本机 Claude Code `2.1.278` 与官方当前格式，并区分版本边界。
- [x] 最终 Framework 文件结构使用 Claude Code 原生 `CLAUDE.md`、Agents、Skills、Rules 和可选 Settings。
- [x] 未把不能可靠由 Markdown 实现的能力伪装为 V1 已实现能力。
- [x] Phase 0 只产出本架构提案，不开始 Phase 1。

---

## 19. Phase 1 前置决策（不在本阶段执行）

1. 补全或确认 `design.md` 在 Stage Gate 处的截断内容。
2. 决定 Phase 1 是否将 Claude Code `2.1.278` 锁定为 Framework 最低版本；如需兼容更早版本，必须单独定义降级矩阵。
3. 确认 `config/project.md` 使用 Markdown 表格还是 Markdown 内嵌 YAML；两者都只作为 Claude 可读配置，不引入解析 Runtime。
4. 为核心 Agent 逐个确定最小工具集和是否允许写入；不要批量复制同一权限。
5. 决定 Worktree 策略：默认串行共享工作区，还是仅对明确独立的写任务按需启用隔离。

**STOP：本文件完成 Phase 0，不创建或实现任何 Agent、Skill、Rule、Template、Hook、MCP 或 Runtime。**
