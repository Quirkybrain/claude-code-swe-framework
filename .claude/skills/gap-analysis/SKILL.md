---
name: gap-analysis
description: Compare validated existing Artifacts with a target Artifact or Target Stage and find missing, partial, unverified, stale, invalid, or incompatible dependencies. Use after Intake/validation and before computing the Minimum Necessary Path.
---

# Gap Analysis

## Purpose

Identify exactly what prevents the current Artifact graph from satisfying the user's target.

## Trigger

Run after Project Intake, when a target changes, after Change Impact, on resume with repository drift, or when a Gate exposes missing evidence.

## Inputs

- Target Artifact or Target Stage and its Definition of Done.
- Artifact Inventory, dependency graph, validation records, and current State.
- Existing Asset evidence, Project Constraints, Workflow Level, and accepted assumptions/decisions.

## Prerequisites

- Normalize the target and stop boundary.
- Validate target-relevant existing Artifacts enough to distinguish presence from usability.

## Procedure

1. Start at the target and enumerate only dependencies required for its declared scope and risk.
2. Walk the Artifact dependency graph backward to source evidence.
3. For each required node, compare required revision/quality with current status and evidence.
4. Classify gaps as `MISSING`, `PARTIAL`, `UNVERIFIED`, `STALE`, `INVALID`, incompatible, or blocked by clarification.
5. Explain why each gap blocks or weakens the target and which downstream nodes it affects.
6. Recognize alternative evidence or reusable assets that may satisfy the dependency.
7. Separate required gaps from optional improvements and later-stage work.
8. Record ready gaps whose upstream dependencies are already satisfied.

## Decision Rules

- A `VALID` and sufficient Artifact is not a gap.
- `PARTIAL` is a gap only for uncovered content required by the target.
- `UNVERIFIED` and `STALE` normally require validation, not automatic regeneration.
- `INVALID` requires repair or regeneration only if it lies on the target dependency path.
- Do not add requirements, design, implementation, testing, or release work unrelated to the target.
- If the target itself is ambiguous, stop at Clarification Gate before expanding the graph.

## Outputs

- Gap Set with node ID, type, state, required revision/quality, evidence, and blocking reason.
- Satisfied/prunable dependency set.
- Ready, blocked, optional, and out-of-scope nodes.
- Dependency rationale suitable for Minimum Path computation.

## Failure Cases

- Dependency graph is absent or contradictory.
- Artifact statuses lack revision-specific evidence.
- Multiple target interpretations produce materially different gaps.
- A required asset is inaccessible.

## Escalation

Use Artifact Validation for uncertain reusable nodes, Clarification Gate for material target ambiguity, and Change Impact when the gap originates from an upstream change. Ask an architect only when dependency semantics cannot be established without a design decision.

## Stop Conditions

Stop when all target-required dependencies are classified with evidence, or when clarification/validation blocks reliable analysis. Do not execute the gaps in this Skill.
