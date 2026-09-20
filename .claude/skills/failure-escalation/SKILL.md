---
name: failure-escalation
description: Stop repeated local patching and move unresolved failure to root-cause review, higher-level analysis, or stage rollback. Use after repeated failed repair attempts, cross-layer evidence, exhausted diagnosis budget, or widening regressions.
---

# Failure Escalation

## Purpose

Break unproductive repair loops and return the problem to the lowest higher layer capable of correcting its cause safely.

## Trigger

Run when the same failure persists after a bounded repair cycle, patches create new failures, diagnosis remains `UNKNOWN`, or evidence points above the current implementation layer.

## Inputs

- Failure/RCA records, attempt history, diffs, test/build evidence, and current revision.
- Classified or suspected responsible layers and confidence.
- Current Stage, Minimum Necessary Path, Workflow Level, Checkpoint, and rollback points.
- Affected Artifacts, Components, Contracts, assumptions, decisions, and risks.

## Prerequisites

- Stop further local edits and preserve the failing workspace/evidence.
- Distinguish a genuinely new failure from recurrence of the same cause.

## Procedure

1. Declare `STOP_LOCAL_PATCHING` and record the escalation trigger.
2. Summarize attempted repairs, outcomes, and why another local patch is unjustified.
3. Review or refresh Root Cause Analysis across Requirement, Architecture, Detailed Design, Contract, Interface, Data, Implementation, Test, and Environment.
4. Identify the earliest responsible layer with enough evidence to act.
5. Determine whether to rework locally with a new bounded hypothesis, transfer to a specialist, or roll back Stage/Artifact decisions.
6. Select a safe rollback/checkpoint or preserve current state for comparison.
7. Mark affected Artifacts `STALE`/`UNVERIFIED` and Components `UNVERIFIED`/`FAILED`.
8. Define higher-level analysis, clarification, repair owner, revalidation, and exit criteria.
9. Reassess Workflow Level and risk.
10. Recompute the Minimum Necessary Path after the escalation decision.

## Decision Rules

- Do not repeat an attempt without new evidence or a falsifiable hypothesis.
- Roll back only far enough to reach the responsible decision layer.
- Requirement/product rollback requires user authority; architecture rollback requires an explicit decision/ADR update.
- Preserve history; do not erase failed evidence or pretend the previous Gate passed.
- A changed repair layer invalidates downstream evidence based on the old decision.

## Outputs

- Escalation Record and `STOP_LOCAL_PATCHING` status.
- Higher-level owner/layer, rollback decision/point, and rationale.
- State invalidations, risk/workflow reassessment, revalidation scope, and recomputed path trigger.

## Failure Cases

- No safe rollback point exists.
- Evidence cannot distinguish layers.
- Required decision owner is unavailable.
- Rollback/destructive action lacks authorization.

## Escalation

Use Clarification Gate for product/risk/rollback authority. Use Architecture Decision for structural rollback. Pause the affected path when evidence or authority is unavailable rather than continuing speculative edits.

## Stop Conditions

Stop when local patching is halted and a bounded higher-level action is assigned, or when the work is explicitly blocked awaiting evidence/authority. Do not perform the repair inside this Skill.
