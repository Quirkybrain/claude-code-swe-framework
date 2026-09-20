# Claude Code AI 软件工程生命周期系统

## Final Architecture Design

---

# 1. 系统定位

本系统是一套基于 Claude Code 的：

> **AI Software Engineering Lifecycle System**

它的目标不是让 AI 简单地：

```text
读取需求
→ 写代码
→ 跑测试
```

而是让 AI 按照完整的软件工程思想，根据用户已有资产和最终目标，自主规划最合理的开发路径，并通过专业 Agent、Artifact、测试、Review 和多层 Gate 逐步完成项目。

系统必须支持：

* 从零开始开发；
* 从任意软件工程阶段开始；
* 接手已有项目；
* 已有代码逆向分析；
* 只完成某个指定阶段；
* 到达指定阶段后暂停；
* 后续继续开发；
* AI 全自动开发；
* 用户深度参与；
* 多 Agent 协作；
* 模块化并行开发；
* 中断恢复；
* 长期维护和项目演进。

---

# 2. 总体设计思想

整个系统采用：

```text
Asset Driven
+
Artifact Driven
+
Dependency Aware
+
Stage Controlled
+
Adaptive Workflow
+
User Controlled
+
Clarification Gated
+
Contract First
+
Component Based
+
Test Gated
+
Incremental Integration
+
Traceable
+
Change Aware
+
Recoverable
```

核心思想可以概括为：

> **先理解用户已经有什么，再判断还缺什么；只执行达到目标所需要的最小合理软件工程路径；设计时拆开，实现时独立，测试后稳定，稳定后组合，组合后重新测试。**

---

# 3. 系统总体结构

```text
                    USER
                      │
                      ▼
                   input/
                      │
                      ▼
               Project Intake
                      │
               Asset Discovery
                      │
                      ▼
              Artifact Inventory
                      │
                      ▼
           Artifact Dependency Graph
                      │
                      ▼
                 Gap Analysis
                      │
                      ▼
        Complexity / Risk / Impact
                      │
                      ▼
            Adaptive Workflow Engine
                      │
                      ▼
             Minimum Necessary Path
                      │
                      ▼
              Stage Orchestrator
                      │
                      ▼
                  Agent Pool
                      │
                      ▼
                  Artifacts
                      │
                      ▼
                  Gate System
                      │
             ┌────────┴────────┐
             ▼                 ▼
          CONTINUE            STOP
             │
             ▼
           output/
             │
             ▼
        Persistent State
```

---

# 4. Input：项目已有资产池

`input/` 的定位不是“需求目录”。

而是：

> **Project Asset Pool**

用户可以把任何已经拥有的项目资料放入其中。

例如：

```text
产品描述
项目想法
需求文档
竞品资料
同类产品介绍
参考系统
UI 设计图
原型图
流程图
UML
类图
时序图
架构图
数据库设计
API 文档
算法说明
函数
代码片段
已有模块
完整代码项目
测试用例
测试报告
Bug 描述
部署资料
开发规范
公司编码规范
安全规范
```

因此：

```text
input ≠ requirements
```

而应该理解为：

```text
input = 当前项目已经拥有的一切
```

---

# 5. Input 推荐结构

可以提供推荐结构：

```text
input/

├── project/
├── requirements/
├── references/
├── competitors/
├── design/
├── uml/
├── architecture/
├── api/
├── data/
├── existing/
├── tests/
├── standards/
└── other/
```

但不强制用户整理。

例如：

```text
input/
├── idea.md
├── competitor.pdf
├── login.png
├── system.puml
├── user.c
└── api.md
```

系统也必须能够正确理解。

---

# 6. 项目技术配置模板

用户应该拥有一个可选的项目配置模板。

用户可以自行指定：

```text
开发语言
语言版本
框架
前端技术
后端技术
数据库
UI 框架
API 技术
构建工具
包管理工具
测试框架
运行平台
部署方式
必须使用的技术
禁止使用的技术
技术偏好
```

每个字段可以：

```text
明确指定
```

或者：

```text
auto
```

原则：

> 用户明确指定的内容具有高优先级。

> 用户没有指定的内容，由 Architect 补全。

最终技术栈由：

```text
User Configuration
+
Requirements
+
Existing Assets
+
Architect Analysis
```

共同确定。

---

# 7. 用户编码规范

用户自己的编码和工程规范统一放入：

```text
input/standards/
```

例如：

```text
公司编码规范
团队开发规范
测试规范
安全规范
API 规范
文档规范
```

由：

```text
Architect Agent
```

统一读取和解释。

形成：

```text
Project Constraints
```

其他 Agent 使用已经解析后的 Constraints。

不要求每一个 Agent 都重新解释原始规范。

如果用户没有提供规范：

Architect 根据：

```text
语言
框架
项目类型
已有代码风格
```

采用成熟主流规范。

---

# 8. Project Intake

无论项目从哪里开始，都先经过：

> **Project Intake**

它不是需求分析。

它只负责：

```text
扫描 input
↓
识别资产
↓
分析内容
↓
识别 Artifact 类型
↓
判断所属生命周期阶段
↓
判断完整程度
↓
检测冲突
↓
建立 Artifact Inventory
↓
建立项目初始状态
```

因此无论用户只有：

```text
一句产品描述
```

还是已经拥有：

```text
完整软件项目
```

都使用相同入口。

---

# 9. Asset Recognition

系统不能仅通过：

```text
文件名
扩展名
目录
```

判断资产类型。

还必须进行：

```text
Content Analysis
```

例如：

```text
system.png
```

可能是：

```text
UI 原型
架构图
流程图
部署图
```

因此最终建立：

```text
Asset
↓
Artifact Type
```

映射。

---

# 10. Artifact Inventory

系统需要知道：

> 当前项目究竟已经有什么？

例如：

```text
Product Description      PRESENT
Requirements             PARTIAL
SRS                      MISSING
Domain Model             MISSING
UML Class Diagram        PRESENT
Architecture             MISSING
API Specification        PARTIAL
Implementation           PARTIAL
Tests                    MISSING
```

---

# 11. Artifact 状态

Artifact 可以处于：

```text
MISSING
PARTIAL
UNVERIFIED
VALID
STALE
INVALID
```

含义：

```text
MISSING
不存在

PARTIAL
存在但不完整

UNVERIFIED
存在但尚未确认可靠

VALID
经过验证，可直接使用

STALE
上游发生变化，需要重新验证

INVALID
已经确认不能继续使用
```

---

# 12. Artifact Dependency Graph

这是整个系统最重要的数据模型之一。

系统不应该规定：

```text
Requirement Agent
→ UML Agent
→ Architect Agent
```

而应该定义：

```text
某个 Artifact 需要什么输入
+
可以复用什么已有资料
+
可以产生什么输出
```

例如：

```text
UML Class Diagram

Requires:
- Requirements
- Domain Information

Can Reuse:
- Existing UML
- Existing Code
- Data Model
```

因此：

> Agent 不是流程连接点。

> Artifact Dependency 才是流程连接点。

---

# 13. Agent Pool，而不是 Agent Chain

Agent 不形成固定调用链。

错误模型：

```text
RequirementAgent
↓
ArchitectAgent
↓
DeveloperAgent
↓
TesterAgent
```

正确模型：

```text
           Artifact Graph
                 │
                 ▼
            Orchestrator
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
      Agent A  Agent B  Agent C
```

Orchestrator 根据当前：

```text
Artifact
Stage
Target
Risk
```

选择需要的 Agent。

---

# 14. Gap Analysis

系统根据：

```text
Existing Artifacts
+
Target Artifact / Target Stage
```

判断：

> 从当前状态达到目标还缺什么？

例如：

已有：

```text
Product Description
UI Design
```

目标：

```text
UML Class Diagram
```

可能得到：

```text
Missing:
Requirements
Domain Model
```

因此路径：

```text
Requirement Analysis
↓
Domain Modeling
↓
UML Class Diagram
↓
STOP
```

---

# 15. Minimum Necessary Path

系统遵循：

> **Minimum Necessary Path**

原则。

即：

> 只执行达到用户目标真正需要的软件工程步骤。

例如：

```text
已有完整 Requirements
目标 UML
```

则不执行：

```text
Implementation
Testing
Release
```

---

# 16. 任意阶段进入

系统必须允许从软件生命周期任意位置开始。

例如：

```text
只有产品描述
→ Requirement Analysis
```

```text
已有 Requirement
→ UML
```

```text
已有 UML
→ Architecture
```

```text
已有 Architecture
→ Detailed Design
```

```text
已有 Code
→ Review
```

```text
已有 Code
→ Testing
```

```text
已有 Code
→ Reverse Engineering UML
```

```text
已有 Test Report
→ Debug / Fix
```

---

# 17. Forward + Reverse Engineering

系统同时支持：

```text
Forward Engineering
```

与：

```text
Reverse Engineering
```

正向：

```text
Requirement
→ Design
→ Code
```

逆向：

```text
Code
→ Structure Understanding
→ Architecture Understanding
→ UML
→ Requirement Inference
```

因此既能开发新项目，也可以接管旧项目。

---

# 18. 用户的三个顶层控制参数

用户拥有三个独立控制维度：

```text
WHERE
做到哪里

HOW STRICT
做得多严格

HOW AUTONOMOUS
AI 多自主
```

分别对应：

```text
Target Stage

Workflow Mode

Execution Mode
```

---

# 19. Target Stage

决定：

> AI 做到哪里停止。

例如：

```text
requirements
uml
architecture
detailed-design
implementation
review
testing
release
```

达到 Target Stage 后：

```text
PAUSED_AT_STAGE
```

而不是：

```text
PROJECT_COMPLETED
```

以后用户可以继续。

---

# 20. Workflow Mode

决定：

> 软件工程流程多严格。

支持：

```text
AUTO
LIGHTWEIGHT
STANDARD
STRICT
```

推荐：

```text
AUTO
```

---

# 21. Execution Mode

决定：

> AI 有多少自主权。

可以包括：

```text
INTERACTIVE

GATED_AUTO

FULL_AUTO
```

### INTERACTIVE

用户深度参与。

较多关键节点主动询问。

### GATED_AUTO

普通技术问题 AI 自行处理。

重要产品、架构、安全问题询问用户。

推荐默认。

### FULL_AUTO

AI 尽可能自主推进。

但真正无法可靠推断的重要用户意图仍然应该停止询问。

---

# 22. Adaptive Workflow Engine

完整的软件工程生命周期代表：

> 系统拥有的最大能力。

而不是：

> 每次必须全部执行。

因此加入：

> **Adaptive Workflow Engine**

根据：

```text
Complexity
Risk
Impact
Project Size
Task Size
Long-term Maintenance
Team / Agent Count
Existing Assets
Target Stage
```

动态决定工程流程强度。

---

# 23. Progressive Formality

采用：

> Progressive Formality

原则。

```text
简单任务
→ Lightweight

普通项目
→ Standard

复杂 / 高风险项目
→ Strict
```

---

# 24. Lightweight Mode

适合：

```text
小功能
Bug Fix
脚本
独立算法
小范围重构
单模块修改
```

典型流程：

```text
Understand
↓
Clarify if Needed
↓
Implement
↓
Build
↓
Relevant Tests
↓
Quick Review
↓
Quality Gate
↓
Checkpoint
```

一般不强制生成：

```text
完整 SRS
完整 UML
完整 ADR
完整 Traceability
正式 Test Plan
```

---

# 25. Standard Mode

适合：

```text
普通软件项目
课程项目
个人长期项目
多模块应用
一般 Web / Desktop / Mobile
```

典型流程：

```text
Project Understanding
↓
Requirement Analysis
↓
Necessary Design
↓
Architecture
↓
Component Planning
↓
Implementation
↓
Testing
↓
Integration
↓
Review
↓
Verification
```

---

# 26. Strict Mode

适合：

```text
大型项目
企业项目
长期维护系统
多团队项目
高可靠系统
安全敏感系统
复杂数据系统
```

可启用：

```text
SRS
Domain Modeling
完整 UML
Architecture
ADR
Detailed Design
API Contract
Security Design
Traceability
Contract Testing
Integration Testing
Performance Testing
Security Testing
Change Impact Analysis
Acceptance
Release
```

---

# 27. Process Budget

整个系统遵循：

> **Process Budget**

原则。

软件工程流程本身的成本，不应该明显超过它所降低的风险。

例如：

```text
新增一个简单函数
```

不应该生成：

```text
SRS
UML
Architecture
ADR
正式 Test Plan
```

但仍然必须：

```text
Implement
↓
Test
↓
Verify
```

---

# 28. Generate Artifacts On Demand

Artifact 采用：

> Generate On Demand

而不是：

> 有这种文档就必须生成。

只有当 Artifact：

```text
降低风险
帮助后续 Agent
帮助协作
帮助维护
支持当前目标
或者用户明确要求
```

时才生成。

---

# 29. Dynamic Escalation / De-escalation

Workflow Level 不是永久固定。

例如：

```text
开始：
LIGHTWEIGHT
```

后来发现：

```text
影响多个模块
```

可以升级：

```text
LIGHTWEIGHT
→ STANDARD
```

发现：

```text
涉及安全模型
```

继续升级：

```text
STANDARD
→ STRICT
```

同样：

大型 Strict 项目中的：

```text
README 拼写修改
```

当前 Task 可以使用：

```text
LIGHTWEIGHT
```

因此区分：

```text
Project Workflow Level
```

和：

```text
Task Workflow Level
```

---

# 30. Clarification Gate

如果遇到：

```text
需求模糊
多种合理解释
多种重大实现方案
产品行为不明确
资产之间冲突
重要架构决策不明确
安全决策不明确
```

AI 不能擅自决定。

必须进入：

> **Clarification Gate**

并使用：

```text
Ask Me Question
```

---

# 31. 可以自动推断的情况

对于：

```text
风险低
影响小
已有上下文足够
具有明确行业惯例
```

的问题，AI 可以自行判断。

但必须将重要推断记录为：

```text
Assumption
```

---

# 32. 必须询问用户的情况

如果选择会明显影响：

```text
产品体验
用户行为
系统架构
技术栈
数据模型
安全
部署
大量后续代码
成本
```

则必须：

```text
Ask Me Question
```

---

# 33. Ask Me Question 原则

问题应：

```text
具体
结构化
提供合理选项
简要说明差异
```

例如：

```text
登录可以采用：

A. 本地账号密码
B. OAuth
C. 企业 SSO

三种方案会影响认证架构和数据模型。

请选择希望采用的方案。
```

而不是：

```text
你想怎么做？
```

---

# 34. 用户回答必须持久化

用户回答以后不能只保存在聊天记录。

应该写入适当的：

```text
Requirement
Constraint
Decision
ADR
```

以后其他 Agent 直接读取。

同一个问题不得重复询问。

---

# 35. 完整软件工程生命周期

系统能力覆盖：

```text
00 Project Intake

01 Product Understanding

02 Requirement Elicitation

03 Requirement Analysis

04 Requirement Specification

05 Domain Modeling

06 UML / Software Modeling

07 Architecture Design

08 Detailed Design

09 Data Design

10 API / Interface Design

11 UI / UX Design

12 Security Design

13 Project Planning

14 Component Planning

15 Implementation

16 Code Review

17 Test Design

18 Test Execution

19 Integration

20 System Verification

21 Acceptance

22 Documentation

23 Release / Deployment

24 Maintenance
```

但根据 Adaptive Workflow：

> 不要求每次执行全部阶段。

---

# 36. Role Pool

逻辑上拥有完整的软件工程角色：

```text
Project Intake Role

Product Analyst

Requirement Analyst

Requirement Specification Role

Domain Analyst

UML / Modeling Role

Software Architect

Detailed Design Role

Data Architect

API / Interface Designer

UI / UX Designer

Security Architect

Project Planner

Component Planner

Developer

Code Reviewer

Test Designer

Test Engineer

Integration Engineer

Performance Engineer

Security Reviewer

System Verification Role

Acceptance Role

Documentation Role

Release / DevOps Role

Maintenance Role
```

这里定义的是：

> Logical Role

并不意味着：

```text
1 Role = 1 Claude Agent
```

实际实现时可以合并职责相近角色。

---

# 37. Stage Orchestrator

Claude Code 主会话承担：

> **Stage Orchestrator**

主要职责：

```text
读取用户目标
↓
分析当前 Artifact
↓
Gap Analysis
↓
Risk / Complexity Assessment
↓
选择 Workflow Level
↓
计算 Minimum Necessary Path
↓
选择 Agent
↓
执行 Stage
↓
执行 Gate
↓
Continue / Stop / Rollback
```

---

# 38. Artifact 是 Agent 之间的接口

不同 Agent 不应该主要通过聊天上下文传递信息。

而应通过：

```text
Requirements
Domain Model
UML
Architecture
API Contract
Component Design
Code
Test Report
Review Report
```

等 Artifact 协作。

---

# 39. Artifact Validation

对于用户已有成果：

> Reuse Before Regenerate

首先执行：

```text
Validation
```

检查：

```text
完整性
一致性
正确性
是否过期
是否足以支持目标
```

然后决定：

```text
Reuse
Supplement
Revalidate
Regenerate
```

---

# 40. Traceability

整个系统维护：

> Software Engineering Traceability

例如：

```text
REQ-001
↓
USECASE-003
↓
DOMAIN-002
↓
UML-004
↓
API-007
↓
COMPONENT-012
↓
TASK-031
↓
TEST-052
```

从而可以回答：

```text
这个需求有没有实现？

在哪实现？

什么测试覆盖？

改变它会影响什么？
```

---

# 41. Change Impact Analysis

如果上游 Artifact 修改：

```text
Requirement
UML
Architecture
API
```

系统必须进行：

```text
Change Impact Analysis
```

寻找所有受影响下游成果。

例如：

```text
Requirement Changed
↓
UML            STALE
API            STALE
Code           NEEDS_REVALIDATION
Tests          NEEDS_REVALIDATION
```

然后重新规划：

```text
Minimum Necessary Path
```

而不是全部推翻。

---

# 42. ADR

重大架构和技术决策使用：

> Architecture Decision Record

记录：

```text
Context
Decision
Consequences
```

例如：

```text
为什么选择 PostgreSQL

为什么采用 REST

为什么选择 Qt

为什么使用某种架构

为什么放弃之前方案
```

---

# 43. 模块化设计原则

Architecture 和 Detailed Design 阶段将系统拆分为：

```text
System
↓
Subsystem
↓
Module
↓
Component
↓
Task
```

Component 应尽可能：

```text
职责单一
边界明确
接口明确
高内聚
低耦合
可独立开发
可独立测试
可独立替换
```

---

# 44. 前后端分离

如果存在前后端：

```text
Frontend
     ↕
API Contract
     ↕
Backend
```

Frontend 不依赖 Backend 内部实现。

Backend 不依赖 Frontend 内部实现。

---

# 45. UI 与业务逻辑分离

Web、Desktop、Mobile 都应尽可能：

```text
UI
↓
Application Layer
↓
Business Logic
↓
Infrastructure
```

避免：

```text
UI Callback
↓
直接包含大量业务逻辑和数据库操作
```

---

# 46. Contract First

不同 Component 之间首先定义：

```text
Input
Output
Data Structure
Behavior
Error
Boundary
Protocol
```

形成：

> Contract

之后各 Component 才可以独立开发。

---

# 47. Component Graph

系统设计最终应形成：

> Component Graph

描述：

```text
Component 关系
依赖
Contract
Integration Point
可以并行的部分
必须等待的部分
```

而不是简单 Task List。

---

# 48. Lego Development Model

Implementation 采用：

> Lego-style Incremental Development

例如：

```text
Component A
↓
Develop
↓
Test
↓
PASS
↓
STABLE


Component B
↓
Develop
↓
Test
↓
PASS
↓
STABLE
```

然后：

```text
A + B
↓
Integration
↓
Contract Test
↓
Integration Test
↓
PASS
↓
Stable AB
```

继续：

```text
Stable AB
+
Stable C
↓
Integration
↓
Test
↓
PASS
```

逐步组成完整系统。

---

# 49. Component 状态

Component 至少可以拥有：

```text
UNIMPLEMENTED
IMPLEMENTING
UNVERIFIED
FAILED
STABLE
```

只有：

```text
STABLE
```

Component 可以参与下一层 Integration。

---

# 50. 修改后验证失效

如果：

```text
STABLE
↓
Code Changed
```

立即：

```text
UNVERIFIED
```

旧测试结果失效。

必须重新：

```text
Build
Test
Review
Gate
```

---

# 51. 每次代码开发都必须测试

任何：

```text
新增代码
修改代码
Bug Fix
Refactor
```

完成后必须：

```text
Build
↓
Test
↓
Verify
```

Developer 不能因为：

```text
代码已经写完
```

就宣布完成。

---

# 52. 分层测试

测试与 Lego 模型对应：

```text
Component
→ Unit Test

Module
→ Module Test

Multiple Components
→ Integration Test

Subsystem
→ Subsystem Test

Whole System
→ System Test

Requirement
→ Acceptance Test
```

根据项目需要增加：

```text
Regression Test
Contract Test
Performance Test
Security Test
Compatibility Test
```

---

# 53. Adaptive Testing

测试范围也根据修改风险调整。

简单纯函数：

```text
Unit Test
+
Relevant Regression
```

模块修改：

```text
Unit Test
+
Module Test
+
Regression
```

API 修改：

```text
Unit Test
+
Contract Test
+
Integration Test
+
Regression
```

架构性修改：

```text
Unit
+
Contract
+
Integration
+
Subsystem
+
System
+
Regression
```

---

# 54. Contract Testing

即使：

```text
Frontend PASS

Backend PASS
```

也不能推出：

```text
Frontend + Backend PASS
```

所以需要：

```text
Consumer Contract Test
Provider Contract Test
Integration Test
```

保证两边真正兼容。

---

# 55. Definition of Done

Test PASS 不代表任务一定完成。

每个：

```text
Task
Component
Module
Stage
```

可以拥有自己的：

> Definition of Done

例如：

```text
Implementation Complete
Build PASS
Required Tests PASS
Contract PASS
Acceptance Criteria PASS
Required Review PASS
```

只有全部满足才能：

```text
DONE / STABLE
```

---

# 56. Adaptive Quality Gate

Quality Gate 根据 Workflow Level 调整。

### Lightweight

```text
Build
Relevant Tests
Regression
Acceptance Criteria
```

### Standard

```text
Build
Static Checks
Unit Tests
Module Tests
Regression
Code Review
Acceptance Criteria
```

### Strict

```text
Build
Static Analysis
Unit Tests
Contract Tests
Integration Tests
Regression Tests
Security Checks
Performance Checks
Code Review
Architecture Compliance
Traceability
Acceptance Criteria
```

---

# 57. Code Review

Testing 回答：

```text
功能运行是否正确？
```

Review 回答：

```text
实现方式是否合理？
```

推荐流程：

```text
Implementation
↓
Build
↓
Test
↓
Review
↓
如果发生修改
↓
Retest
↓
Quality Gate
```

---

# 58. Adaptive Review

简单修改：

```text
Quick Review
```

普通模块：

```text
Code Review
+
Architecture Consistency
```

高风险模块：

```text
Code Review
Architecture Review
Security Review
Performance Review
Integration Review
```

---

# 59. Integration Gate

即使：

```text
A = STABLE
B = STABLE
```

也不能认为：

```text
A + B = STABLE
```

必须：

```text
A + B
↓
Contract Validation
↓
Integration Test
↓
Regression
↓
PASS
```

才能成为：

```text
Stable AB
```

---

# 60. Failure Diagnosis

测试失败后：

不能直接进入：

```text
不停改代码
```

必须先：

```text
Root Cause Analysis
```

判断问题属于：

```text
Implementation
Interface
Contract
Data
Detailed Design
Architecture
Requirement
```

然后在正确层级修复。

---

# 61. Failure Escalation

禁止：

```text
FAIL
↓
乱改
↓
FAIL
↓
乱改
↓
无限循环
```

重复失败后：

```text
Repeated Failure
↓
Stop Local Patching
↓
Escalation
↓
Higher-level Analysis
```

可以交给：

```text
Debug Specialist
Detailed Designer
Architect
```

必要时：

```text
Stage Rollback
```

例如：

```text
Implementation
→ Detailed Design
```

甚至：

```text
Detailed Design
→ Architecture
```

---

# 62. Planner

Planner 不只是生成：

```text
T1
T2
T3
```

而应该维护：

```text
Task Graph
Component Graph
Dependencies
Parallel Tasks
Quality Gates
Integration Points
Milestones
```

---

# 63. 多 Agent 并行开发

独立 Component 可以并行开发。

例如：

```text
Frontend Agent
Backend Agent
Database Agent
```

但必须：

> Workspace Isolation

未来可以使用：

```text
Git Branch
Git Worktree
Independent Workspace
```

避免多个 Agent 直接修改同一个 working tree。

---

# 64. Integration Workspace

每个 Agent：

```text
独立开发
↓
独立测试
↓
STABLE
```

之后进入：

```text
Integration Workspace
```

再组合。

未验证代码不能直接进入主集成分支。

---

# 65. System Verification

项目后期需要检查：

```text
Requirement
↕
Design
↕
Architecture
↕
Implementation
↕
Tests
```

是否一致。

重点识别：

```text
Requirement 没有实现

代码没有对应 Requirement

Requirement 没有测试

设计已经和代码脱节
```

---

# 66. Acceptance

System Verification 解决：

```text
系统工程上是否正确？
```

Acceptance 解决：

```text
这是不是用户真正要的软件？
```

依据：

```text
Business Requirement
Use Case
User Scenario
Acceptance Criteria
```

判断。

---

# 67. 五类 Gate

整个系统形成五类核心 Gate。

## Clarification Gate

```text
这个问题是否需要用户决定？
```

## Artifact Validation Gate

```text
已有 Artifact 是否可使用？
```

## Component Quality Gate

```text
当前 Component 是否达到 DoD？
```

## Integration Gate

```text
组合后是否仍然正确？
```

## Stage Gate

```text
当前阶段是否完成？
是否达到 Target Stage？
```

---

# 68. Stage Gate

每一个主要生命周期阶段结束后：

```text
Stage Gate
```

判断：

```text
```

