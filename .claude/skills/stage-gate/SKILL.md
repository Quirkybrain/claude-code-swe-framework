---
name: stage-gate
description: Evaluate whether a major lifecycle Stage has complete valid Artifacts, passed required validation and Definition of Done, and reached the configured Target Stage. Use at each relevant Stage boundary before continuing or pausing.
---

# Stage Gate

## Purpose

Control progression by evidence and stop precisely at the user's Target Stage.

## Trigger

Run when target-relevant work for a Stage appears complete, before entering downstream work, or when reassessing a paused/failed Stage.

## Inputs

- Current Stage, Target Stage, Stage scope, Workflow Level, and Stage DoD.
- Required Artifact IDs/revisions/statuses and validation evidence.
- Applicable Clarification, Artifact, Component Quality, and Integration Gate results.
- Traceability, open questions, assumptions, decisions, risks, deviations, and Current Minimum Necessary Path.

## Prerequisites

- Normalize the stage/target and identify only Artifacts required for the declared scope.
- Gate evidence must apply to current revisions.

## Procedure

1. Check whether all target-required Stage Artifacts are complete and sufficiently `VALID`.
2. Check Artifact Validation and all applicable lower-level Gate verdicts.
3. Check every Stage DoD item at the effective Workflow Level.
4. Check traceability, accepted risks, unresolved deviations, assumptions, and Clarifications.
5. Determine whether failures require rework, clarification, or rollback to a responsible earlier layer.
6. Determine whether Current Stage equals Target Stage.
7. Record `PASS`, `FAIL`, `BLOCKED`, or `USER_DECISION_REQUIRED` with evidence and next action.
8. On PASS below target, update State and expose only the next ready Minimum Path node.
9. On PASS at target, create a Checkpoint, set project status `PAUSED_AT_STAGE`, report outputs/residual risks, and stop.

## Decision Rules

- Artifact existence is not completeness or validation.
- Missing/currently stale required evidence prevents PASS.
- Waived criteria require persisted authority and risk acceptance.
- Rework only affected scope and recompute the Minimum Necessary Path.
- Reaching Target Stage means `PAUSED_AT_STAGE`, never `PROJECT_COMPLETED`.
- Do not enter a later stage because it exists in the lifecycle.

## Outputs

- Stage Gate Record with Stage/target, revisions, DoD checks, evidence, verdict, findings, and next action.
- Updated Current Stage/project status and path state.
- Target delivery summary and Checkpoint when paused.

## Failure Cases

- Stage DoD or target is ambiguous.
- Evidence is stale, conflicting, or absent.
- Required user Acceptance has not occurred.
- State and repository revisions disagree.

## Escalation

Use Clarification Gate for intent/acceptance, Failure Diagnosis for failed evidence, Change Impact for drift, and Workflow Assessment when Gate depth is insufficient. Roll back only to the responsible layer.

## Stop Conditions

Stop after the recorded verdict. On target PASS, stop all downstream work at `PAUSED_AT_STAGE`; on failure/block, expose only bounded corrective action.
