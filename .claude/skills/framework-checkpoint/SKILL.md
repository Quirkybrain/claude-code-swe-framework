---
name: framework-checkpoint
description: Persist a recoverable snapshot of project Stage, target, workflow, Artifacts, Components, decisions, assumptions, questions, risks, current path, evidence, and next action. Use at major results, pauses, blockers, escalations, integration, or session end.
---

# Framework Checkpoint

## Purpose

Make project work resumable from versioned repository evidence rather than hidden chat or Agent memory.

## Trigger

Run after a major Artifact/Gate result, before a blocking question or Target Stage pause, after escalation/replanning/integration, and before session end or expected context loss.

## Inputs

- Current State, Artifact Registry, Component states, active task, and Gate evidence.
- Repository revision, branch/worktree identity, and working-tree status.
- Current/Target Stage, Project/Task Workflow Levels, Execution Mode, and Current Minimum Necessary Path.
- Decisions, assumptions, open questions, risks, blockers, and next ready action.

## Prerequisites

- Reconcile obvious State/repository discrepancies before declaring a clean snapshot.
- Reference persisted Artifact paths and exact revisions rather than copying chat claims.

## Procedure

1. Assign a Checkpoint ID and timestamp/repository reference.
2. Record repository revision, branch/worktree, dirty paths, and any uncommitted dependency relevant to recovery.
3. Record Current Stage, Target Stage, Project Workflow Level, Task Workflow Level, and Execution Mode.
4. Record Active Task, owner capability, status, dependencies, scope, and DoD.
5. Record Artifact IDs/revisions/states and Component IDs/contracts/states with latest evidence.
6. Record decisions, assumptions, Open Questions/Clarifications, risks, accepted deviations, and blockers.
7. Record work completed since the previous Checkpoint and current validation/Gate verdicts.
8. Record the Current Minimum Necessary Path, ready/blocked nodes, replan triggers, and next safe action.
9. Add recovery instructions and known State consistency limitations.
10. Validate that all referenced paths/revisions exist or mark them unresolved.

## Decision Rules

- Chat history and Agent memory are not authoritative recovery sources.
- Do not mark an Artifact `VALID` or Component `STABLE` without current evidence.
- Dirty working state must be explicit; do not imply it is committed.
- Open material uncertainty remains an open clarification/assumption, not a decision.
- A Checkpoint records state; it does not make multi-file updates atomic.

## Outputs

A persisted Checkpoint containing at least:

- Stage and Target
- Project/Task Workflow Levels and Execution Mode
- Artifacts and Components
- Active Task and completed work
- Decisions, Assumptions, Open Questions, Risks, and blockers
- Validation/Gate evidence
- Current Path, next action, and recovery instructions

## Failure Cases

- State files disagree or referenced revisions do not exist.
- Working-tree changes cannot be attributed safely.
- Evidence paths are missing.
- Concurrent work makes the snapshot unstable.

## Escalation

Mark conflicting entries `UNVERIFIED` and request reconciliation. Pause concurrent writers if necessary. Record Runtime-level atomicity limitations rather than claiming consistency guarantees.

## Stop Conditions

Stop when another session can identify exact state, evidence, blockers, and next safe action from persisted files, or when unresolved inconsistency is explicitly recorded.
