# Framework Overview

## Purpose

The Claude Code AI Software Engineering Framework is a reusable project template. It gives Claude Code a disciplined way to understand existing project assets, choose an appropriate engineering path, produce verifiable Artifacts, and stop at the user's requested target.

Claude Code itself performs the work. The Framework does not implement a separate lifecycle engine.

## Operating Model

The main Claude Code session is the **Stage Orchestrator**. It owns global workflow decisions:

- interpret the user target and Project Configuration;
- perform or coordinate Project Intake;
- maintain the Artifact view of the project;
- validate reusable work;
- identify missing or stale dependencies;
- calibrate workflow rigor from risk and scope;
- compute the Minimum Necessary Path;
- select appropriate Agents and Skills when available;
- require evidence at Gates;
- persist checkpoints and stop at the correct boundary.

Fourteen specialist Agents are available as an on-demand pool, not a fixed chain. The Orchestrator selects only the expertise and permission boundary required by the current Artifact gap.

Twenty-one workflow Skills provide independently loadable procedures for Intake, validation, planning, implementation, quality, failure recovery, traceability, checkpointing, and resume. They are selected by need and do not define a mandatory lifecycle.

Eight concise Rule topics keep Framework-wide invariants active across sessions. They state durable constraints only; multi-step execution remains in Skills.

## Decision Flow

```text
User Request
    ↓
Project Configuration
    ↓
Existing Assets and State
    ↓
Artifact Identification and Validation
    ↓
Clarification Gate
    ↓
Gap Analysis
    ↓
Risk / Complexity / Impact
    ↓
Workflow Level
    ↓
Minimum Necessary Path
    ↓
Skill / Agent Selection
    ↓
Execution and Validation
    ↓
Applicable Gate
    ↓
State Update
    ↓
Continue / Replan / Pause / Stop
```

This flow does not require every box to produce a new document. It is a decision model used to select only necessary work.

## Inputs and Controls

### Project Configuration

`config/project.md` records the desired Target Stage, Workflow Mode, Execution Mode, technical choices, and constraints. Unknown values may be `auto`.

### Project Asset Pool

`input/` contains any existing project material. Its suggested directories improve navigation but do not define Artifact type. Classification must consider content.

### Standards

Files under `input/standards/` are normalized once into shared Project Constraints, with source references and conflict notes. Other roles consume those constraints rather than repeatedly interpreting raw standards.

## Three Control Dimensions

### Target Stage

Defines where work stops. Reaching it produces `PAUSED_AT_STAGE`, not an assertion that every later lifecycle stage is complete.

### Workflow Mode

- `AUTO`
- `LIGHTWEIGHT`
- `STANDARD`
- `STRICT`

The Project Workflow Level is the baseline. Each task receives a Task Workflow Level that may be higher or lower when its actual risk differs.

### Execution Mode

- `INTERACTIVE`: frequent user participation.
- `GATED_AUTO`: routine technical decisions are autonomous; material decisions are clarified.
- `FULL_AUTO`: maximum safe autonomy, without inventing high-impact user intent.

## Artifact-Driven Workflow

Artifacts are the durable interfaces between stages, Agents, and sessions. Their dependencies—not Agent order—determine what work is ready.

Examples include Requirements, Models, Architecture, Contracts, ADRs, Component Designs, Code, Tests, Review Reports, and Release Evidence.

Existing Artifacts are validated before reuse. The possible outcomes are:

- Reuse
- Supplement
- Revalidate
- Regenerate

See [artifact-model.md](artifact-model.md).

## Minimum Necessary Path

The Orchestrator starts from the requested target, walks required Artifact dependencies backward, and removes dependencies already satisfied by valid, sufficient Artifacts. It then executes only the remaining ready nodes.

This enables:

- starting from any lifecycle stage;
- stopping at any requested stage;
- forward engineering;
- reverse engineering from existing code and tests;
- small fixes without lifecycle ceremony;
- strict evidence for high-risk work.

## Quality and Recovery

Five Gate types control progress: Clarification, Artifact Validation, Component Quality, Integration, and Stage. See [gate-model.md](gate-model.md).

Project state is persisted conceptually through explicit State records and checkpoints, not hidden chat history. See [state-model.md](state-model.md).

After a failure, the Framework requires Root Cause Analysis and repair at the responsible layer. Repeated local patching triggers escalation or rollback to design, architecture, or requirements as appropriate.

## Claude Code Mapping

| Concern | Claude Code mechanism |
|---|---|
| Always-on orchestration | `CLAUDE.md` |
| User controls | `config/project.md` |
| Existing assets | `input/` |
| User startup and continuation | Root `*_PROJECT.md` and `EXECUTE_TASK.md` prompt templates |
| Specialist responsibility | `.claude/agents/*.md` |
| Reusable procedures | `.claude/skills/*/SKILL.md` |
| Persistent constraints | `.claude/rules/*.md` |
| Collaboration and recovery | Markdown Artifacts and State records |

The current verified local Claude Code version is `2.1.278`.

## V1 Boundary

V1 can express adaptive reasoning, Artifact handoffs, Gates, and checkpoint discipline through Claude Code instructions and Markdown. It cannot guarantee transactional updates, deterministic enforcement, automatic concurrent integration, or external-system synchronization. Those boundaries are documented in [future-runtime.md](future-runtime.md).
