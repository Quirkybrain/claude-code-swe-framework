# State Model

## Purpose

State records make work resumable across Claude Code sessions and context loss. They describe the current engineering situation, not a Runtime engine or database.

The authoritative recovery source is persisted project State plus versioned Artifacts and evidence. Chat history, auto memory, and Agent memory are supplementary and must not override them.

## Conceptual Project State

| State field | Required content |
|---|---|
| **Current Stage** | Lifecycle stage currently being evaluated or executed |
| **Target Stage** | User-defined stop boundary |
| **Project Workflow Level** | Project baseline: `LIGHTWEIGHT`, `STANDARD`, or `STRICT`; include reason if derived from `AUTO` |
| **Task Workflow Level** | Current task's effective level and any escalation/de-escalation reason |
| **Execution Mode** | `INTERACTIVE`, `GATED_AUTO`, or `FULL_AUTO` |
| **Active Task** | Task ID, objective, owner, dependencies, current status, and Definition of Done |
| **Artifact States** | Artifact IDs, revisions, canonical status, and evidence references |
| **Component States** | Component IDs, contracts, status, and latest build/test/review evidence |
| **Open Clarifications** | Questions blocking or constraining work, their impact, and owner |
| **Assumptions** | Active assumptions, rationale, risk, affected scope, and confirmation method |
| **Decisions** | Decisions and links to Requirements, Constraints, or ADRs |
| **Risks** | Risk, likelihood/impact, mitigation, trigger, and owner |
| **Current Minimum Necessary Path** | Ordered dependency nodes still required for the target, including ready and blocked nodes |
| **Checkpoint** | Timestamp/revision, completed work, evidence, unresolved items, next action, and recovery instructions |

## Project Status

Recommended project-level statuses:

| Status | Meaning |
|---|---|
| `INITIALIZING` | Configuration, Intake, and initial state are being established |
| `ACTIVE` | At least one node on the current path is ready or in progress |
| `BLOCKED_CLARIFICATION` | Material user input is required |
| `BLOCKED_GATE` | A Gate failed or lacks required evidence |
| `PAUSED_AT_STAGE` | The configured Target Stage passed and the Framework intentionally stopped |
| `COMPLETED_TARGET` | A user-defined target other than a stage boundary is fully satisfied |

`COMPLETED_TARGET` does not imply that the entire software lifecycle is complete.

## Artifact States

Artifact state uses the canonical values defined in [artifact-model.md](artifact-model.md):

```text
MISSING
PARTIAL
UNVERIFIED
VALID
STALE
INVALID
```

The State record references the Artifact revision and validation evidence. It must not collapse `STALE` or `UNVERIFIED` into a generic “present” value.

## Component States

| State | Meaning |
|---|---|
| `UNIMPLEMENTED` | Required implementation does not exist |
| `IMPLEMENTING` | Work is in progress and cannot be treated as integration-ready |
| `UNVERIFIED` | Implementation exists or changed, but current required evidence is incomplete |
| `FAILED` | Required build, test, review, contract, or acceptance check failed |
| `STABLE` | Definition of Done and applicable Component Quality Gate passed for the recorded revision |

Typical flow:

```text
UNIMPLEMENTED → IMPLEMENTING → UNVERIFIED → STABLE
                                  ↓           ↓ change
                                FAILED ← UNVERIFIED
```

Only `STABLE` Components may be candidates for higher-level integration. Combining stable Components creates an `UNVERIFIED` integrated unit until the Integration Gate passes.

Any relevant code, Contract, dependency, configuration, or test-basis change moves the affected `STABLE` Component to `UNVERIFIED`. Previous evidence remains historical but is not current.

## Task State

A task record should include:

- Task ID and objective
- Required input Artifact revisions
- Expected output Artifact or code scope
- Dependencies and blockers
- Assigned role/Agent
- Allowed write scope
- Workflow Level
- Definition of Done
- Required Gate
- Status and evidence

Suggested statuses are `PENDING`, `READY`, `IN_PROGRESS`, `BLOCKED`, `FAILED`, and `DONE`. A task is `DONE` only when its Definition of Done and required Gate are satisfied.

## Minimum Necessary Path State

The path is a dependency-aware working plan, not a permanent lifecycle sequence. Each node records:

| Field | Meaning |
|---|---|
| Node | Required Artifact, task, validation, or Gate |
| Why required | Relationship to target or risk |
| Dependencies | Nodes or Artifact revisions that must be ready first |
| State | Ready, active, blocked, satisfied, failed, or pruned |
| Evidence | Proof for satisfied nodes |
| Replan trigger | Change, failure, or decision that invalidates this node |

When new evidence changes risk or dependencies, recompute the remaining path rather than retaining obsolete steps.

## Clarifications, Assumptions, Decisions, and Risks

These are distinct:

- A **Clarification** is unresolved user intent or authority.
- An **Assumption** is a recorded inference that permits bounded progress.
- A **Decision** is a chosen option with consequences.
- A **Risk** is an uncertain event or condition that may harm objectives.

Resolving a Clarification must update the relevant Requirement, Constraint, Decision, or ADR and close the question. Disproving an Assumption or changing a Decision triggers Change Impact Analysis.

## Checkpoint

A recoverable Checkpoint records at least:

```text
Checkpoint ID:
Repository revision / working-tree state:
Current Stage:
Target Stage:
Workflow and Execution Modes:
Active Task:
Completed since previous checkpoint:
Artifact and Component changes:
Validation and Gate evidence:
Open clarifications and blockers:
Active assumptions, decisions, and risks:
Current Minimum Necessary Path:
Next ready action:
```

Create or refresh a Checkpoint:

- after a major Artifact or Gate result;
- before pausing at Target Stage;
- before asking a blocking question;
- after failure escalation or replanning;
- before session end or expected context loss;
- after integration changes the stable baseline.

## Recovery Procedure

On resume:

1. Read Project Configuration and the latest Checkpoint.
2. Verify repository/working-tree state against the Checkpoint.
3. Reconcile referenced Artifact and Component revisions.
4. Reopen unresolved Clarifications, Assumptions, Decisions, and Risks.
5. Validate that ready nodes still have satisfied dependencies.
6. Recompute the Minimum Necessary Path if anything changed.
7. Continue with the next ready action or report a blocker.

If State and repository evidence conflict, do not silently choose one. Mark affected entries `UNVERIFIED`, investigate, and update the Checkpoint.

## Change Impact State

For each upstream change, record:

- changed Artifact and old/new revisions;
- reason and effective decision;
- affected downstream Artifacts and Components;
- new `STALE` or `UNVERIFIED` states;
- required revalidation or rework;
- unaffected scope and why it remains valid;
- resulting path changes.

This prevents both unsafe reuse and unnecessary full-project regeneration.

## Consistency Limitation

Markdown updates are not atomic. During interruption, several State files may disagree. Recovery must reconcile them using repository evidence and latest verified Artifact revisions. Transactional consistency is a future Runtime capability, not a V1 claim.
