# Agent Role Map

## Purpose

`design.md` defines 26 Logical Roles. A Logical Role is a software-engineering responsibility, not a requirement to create one Claude Agent. Phase 0 grouped those roles into 13 cohesive responsibility clusters. Phase 2 added the cross-cutting `debug-specialist`; repository governance adds the cross-cutting `repository-manager`. The current 15-Agent pool remains a capability pool rather than a chain.

The implemented definitions are under `.claude/agents/`. This map explains their boundaries; it is not an invocation chain.

## Orchestrator Boundary

The main Claude session is the Stage Orchestrator. It is not a pool Agent. It owns Project Intake routing, Gap Analysis, workflow calibration, Minimum Necessary Path, delegation, Gate selection, state updates, and stop decisions.

Specialist Agents produce or validate bounded Artifacts. They do not form a fixed chain and do not recursively orchestrate by default.

## Implemented Agent Pool

| Agent | Cohesive responsibility | Write boundary |
|---|---|---|
| `asset-analyst` | Intake, asset recognition, existing Artifact/code/test inventory | Read-only; returns inventory and evidence through Handoff |
| `requirements-analyst` | Product understanding, requirements, specification, acceptance criteria | Requirement and constraint Artifacts |
| `system-modeler` | Domain and UML/software models; forward and reverse modeling | Model Artifacts |
| `solution-architect` | Architecture, detailed design, data/API/security design, ADRs | Design and contract Artifacts |
| `experience-designer` | UX flows, UI behavior, interaction specifications | Experience-design Artifacts |
| `delivery-planner` | Project, Component, Task, dependency, milestone, and Gate planning | Plan and coordination State |
| `implementation-engineer` | Component implementation, refactoring, bug fixes, code maintenance | Business code and implementation evidence |
| `test-engineer` | Test design and execution, regression, contract, performance testing | Tests and test evidence |
| `quality-reviewer` | Code, architecture, security, and performance review | Findings only; reviewed code is read-only |
| `integration-engineer` | Contract validation and incremental integration | Controlled integration changes and evidence |
| `debug-specialist` | Root Cause Analysis, failure classification, repeated-failure escalation | Read-only diagnosis and repair direction; no implementation |
| `system-verifier` | End-to-end traceability, system verification, acceptance analysis | Verification and acceptance reports |
| `technical-writer` | User, developer, operations, and maintenance documentation | Documentation only |
| `release-engineer` | Release readiness, deployment planning, controlled release evidence | Release assets; external effects remain gated |
| `repository-manager` | Git baseline, scoped commits, worktree/status and snapshot-ref evidence | Repository operations and status record; no product changes or Gate verdict |

The frontmatter tools implement coarse least privilege. More granular path boundaries remain behavioral intent; deterministic path enforcement requires permissions or Hooks and is not claimed by Markdown V1.

## Logical Role Mapping

| Logical Role | Primary Agent | Supporting responsibility |
|---|---|---|
| Project Intake Role | `asset-analyst` | Main Orchestrator initiates Intake |
| Product Analyst | `requirements-analyst` | `experience-designer` for user journeys |
| Requirement Analyst | `requirements-analyst` | — |
| Requirement Specification Role | `requirements-analyst` | `system-verifier` checks verifiability later |
| Domain Analyst | `system-modeler` | `requirements-analyst` supplies business semantics |
| UML / Modeling Role | `system-modeler` | Supports forward and reverse engineering |
| Software Architect | `solution-architect` | — |
| Detailed Design Role | `solution-architect` | `delivery-planner` converts boundaries to Component Graph |
| Data Architect | `solution-architect` | Data procedures can be reusable Skills |
| API / Interface Designer | `solution-architect` | Contract-first procedure |
| UI / UX Designer | `experience-designer` | — |
| Security Architect | `solution-architect` | Independent security review by `quality-reviewer` |
| Project Planner | `delivery-planner` | — |
| Component Planner | `delivery-planner` | — |
| Developer | `implementation-engineer` | — |
| Code Reviewer | `quality-reviewer` | Must remain independent from implementation approval |
| Test Designer | `test-engineer` | — |
| Test Engineer | `test-engineer` | — |
| Integration Engineer | `integration-engineer` | — |
| Performance Engineer | `test-engineer` | `quality-reviewer` reviews performance risk/evidence |
| Security Reviewer | `quality-reviewer` | Security-specific procedures and constraints |
| System Verification Role | `system-verifier` | — |
| Acceptance Role | `system-verifier` | Final user acceptance cannot be replaced by an Agent |
| Documentation Role | `technical-writer` | — |
| Release / DevOps Role | `release-engineer` | Production authority remains gated |
| Maintenance Role | `implementation-engineer` | Orchestrator first routes through Change Impact Analysis |

`debug-specialist` is not a one-to-one mapping of an additional lifecycle role. It is a cross-cutting diagnostic boundary used when any mapped role encounters ambiguous, repeated, or cross-layer failure.
`repository-manager` is likewise cross-cutting; it owns Git mechanics at change boundaries without adding a lifecycle Stage or replacing the Orchestrator.

## Selection Rules

Select only the Agents needed for the target under `CLAUDE.md`'s delegation rule. A small task may stay in the main session only in LIGHTWEIGHT mode or with a recorded procedural deviation. One Agent may serve several lifecycle stages, and one stage may require several Agents when Artifact dependencies permit it. `repository-manager` is used at mutation/commit boundaries, not polled continuously.

Read-only independent analysis can run in parallel. Parallel writes require non-overlapping Components, stable Contracts, isolated workspaces, and an explicit integration owner.

The implementation author cannot issue the final Review PASS for the same change. A security or architecture design decision also requires independent review when risk warrants it.
