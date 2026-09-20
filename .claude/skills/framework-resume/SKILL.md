---
name: framework-resume
description: Safely resume framework work by reading the latest Checkpoint, validating repository and Artifact state, detecting drift, revalidating affected work, and recomputing the Minimum Necessary Path. Use after session restart, context loss, pause, or handoff.
---

# Framework Resume

## Purpose

Continue from persisted evidence without blindly trusting an old Checkpoint or hidden conversation history.

## Trigger

Run at session recovery, after `PAUSED_AT_STAGE`, after a handoff/context reset, or whenever repository activity may have occurred since the last Checkpoint.

## Inputs

- `config/project.md`, user request, latest Checkpoint, State, Artifact Registry, and dependency/traceability records.
- Current repository revision, branch/worktree, working-tree status, files, and available validation evidence.
- Open clarifications, decisions, assumptions, risks, and prior Minimum Necessary Path.

## Prerequisites

- Locate the latest relevant Checkpoint by ID/time/repository lineage, not filename guess alone.
- Do not mutate project work until reconciliation identifies a safe next action.

## Procedure

1. Read Project Configuration, latest Checkpoint, linked Artifacts, State, and target.
2. Inspect current repository revision, branch/worktree, dirty state, and relevant file changes.
3. Compare repository/Artifact/Component revisions with the Checkpoint.
4. Detect added, removed, modified, or externally changed assets since the snapshot.
5. Reopen unresolved Clarifications, assumptions, decisions, risks, failures, and blockers.
6. Run Change Impact for every material drift and mark affected Artifacts `STALE`/`UNVERIFIED` and Components `UNVERIFIED` as appropriate.
7. Revalidate affected Artifacts and current Gate evidence; preserve unaffected evidence with rationale.
8. Reassess Workflow Level if scope/risk changed.
9. Rerun Gap Analysis and recompute the Minimum Necessary Path from current evidence.
10. Select the next dependency-ready action or report the exact blocker.
11. Write a reconciled Checkpoint before continuing substantial work.

## Decision Rules

- Repository evidence and exact revisions outrank stale Checkpoint claims, but conflicts must be investigated rather than silently overwritten.
- Do not rerun completed work whose evidence remains current and sufficient.
- Do not continue a previously ready node if its dependencies changed.
- A prior PASS is invalid when its evaluated revision or basis changed.
- Reaching a previous Target Stage remains paused unless the user requests a new target.

## Outputs

- Resume/Reconciliation Report with Checkpoint and current repository comparison.
- Changed-since-checkpoint set and resulting state invalidations.
- Revalidation results, preserved evidence rationale, updated risks, and reconciled Checkpoint.
- Recomputed Minimum Necessary Path and next ready action/blocker.

## Failure Cases

- No trustworthy Checkpoint exists.
- Multiple divergent worktrees/revisions claim continuity.
- Referenced Artifacts/evidence are missing.
- Repository contains unattributed or conflicting changes.

## Escalation

Run Project Intake when no usable snapshot exists. Use Clarification Gate for ownership/intent conflicts, Failure Diagnosis for unexplained drift, and request explicit merge/rollback authority for divergent work.

## Stop Conditions

Stop when current state is reconciled and a safe next action is identified, when the target remains intentionally paused, or when conflict/access/authority blocks recovery. Never continue solely because the old Checkpoint said a node was ready.
