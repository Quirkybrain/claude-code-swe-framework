---
name: minimum-path
description: Convert a validated Gap Set and Artifact dependencies into the Minimum Necessary Path to a target. Use to prune satisfied work, order required nodes, expose blockers, place Gates, and avoid running the full lifecycle automatically.
---

# Minimum Necessary Path

## Purpose

Produce the smallest dependency-correct, risk-appropriate path from current evidence to the requested target.

## Trigger

Run after Gap Analysis, after a material decision or Change Impact, when workflow rigor changes, or when failure invalidates the current path.

## Inputs

- Target Artifact/Stage and stop boundary.
- Gap Set, satisfied nodes, Artifact dependency graph, and current State.
- Project/Task Workflow Levels, risks, constraints, available Agents/Skills, and Process Budget.

## Prerequisites

- Target and Definition of Done are sufficiently clear.
- Target-relevant Artifact dispositions and gaps are current.

## Procedure

1. Walk backward from the target through only mandatory Artifact dependencies.
2. Prune nodes already satisfied by `VALID`, sufficient, compatible revisions.
3. Replace broad regeneration with `SUPPLEMENT` or `REVALIDATE` nodes when sufficient.
4. Add required clarification, decision, validation, implementation, test, review, integration, and Gate nodes.
5. Order nodes by dependency; mark ready, blocked, satisfied, failed, and pruned states.
6. Group independent ready nodes for possible parallel work only when write scopes do not overlap and Contracts are stable.
7. Place integration points, revalidation boundaries, Checkpoints, and the final Stage Gate.
8. Estimate process cost and remove optional work that does not reduce material risk or enable the target.
9. Record replan triggers and the first next action.

## Decision Rules

- Artifact dependencies, not Agent order, determine sequence.
- Never add the entire lifecycle by default.
- Do not include work beyond Target Stage.
- Existing valid evidence is reused; unknown evidence is validated before replacement.
- Parallel writes require non-overlapping scope, stable versioned Contracts, isolated workspaces, and an integration owner.
- Any node whose prerequisites are unmet remains blocked, not optimistically ready.
- The effective Task Workflow Level determines evidence depth, not the number of lifecycle stages executed.

## Outputs

- Current Minimum Necessary Path with node IDs, purpose, dependencies, state, owner capability, required Skill/Gate, output, and DoD.
- Pruned-node rationale and accepted reusable evidence.
- Parallel groups, integration points, blockers, replan triggers, and next ready action.

## Failure Cases

- Cyclic or missing dependencies prevent ordering.
- Target ambiguity changes the path materially.
- Required Contracts or ownership are unresolved.
- Process Budget conflicts with mandatory risk controls.

## Escalation

Use Clarification Gate for target or authority choices, Architecture Decision for structural dependency choices, and Workflow Assessment when risk outgrows the current level. Report cycles or model defects for correction before execution.

## Stop Conditions

Stop when a minimal executable path and next action are recorded, or when a blocker prevents safe planning. Do not start executing nodes merely because the plan exists.
