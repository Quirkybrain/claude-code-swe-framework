---
name: implement-component
description: Implement or modify one bounded Component using its validated Contract and constraints, then build, test, review as required, and pass the Component Quality Gate before STABLE. Use for feature work, bug fixes, and refactors with an explicit scope.
---

# Implement Component

## Purpose

Execute Lego-style Component development without changing upstream intent or declaring unverified code complete.

## Trigger

Run when a Component/task is ready with sufficient Requirements, design, Contract, write scope, and Definition of Done.

## Inputs

- Task/Component ID, allowed write scope, current state, target revision, and DoD.
- Validated Requirements, architecture/design, versioned Contract, Project Constraints, and acceptance criteria.
- Existing code/tests, build commands, risks, Workflow Level, and required Gate/review.

## Prerequisites

- Required dependencies are `VALID`; upstream material decisions are resolved.
- Parallel work has non-overlapping scopes, stable Contracts, correct base visibility, and an integration owner.
- Set the Component to `IMPLEMENTING`; any changed `STABLE` Component becomes `UNVERIFIED`.

## Procedure

1. Read the Contract, constraints, acceptance criteria, and existing implementation before editing.
2. Confirm task scope, base revision, workspace, dependencies, and validation commands.
3. Reproduce a bug before fixing when feasible.
4. Stop if implementation exposes a Requirement, architecture, or Contract gap.
5. Implement the smallest cohesive change within the Component boundary.
6. Add or update focused tests and traceability required by the change.
7. Build or run the project's equivalent compile/static validation.
8. Execute Adaptive Testing for the affected risk and regression scope.
9. Perform required Quick/Code/Architecture/Security/Performance/Integration Review through an independent reviewer when needed.
10. If review causes edits, rebuild and rerun affected tests/review.
11. Evaluate the Component Quality Gate against current evidence.
12. Mark `STABLE` only after Gate PASS; otherwise retain `UNVERIFIED` or set `FAILED`.

## Decision Rules

- Do not alter Requirements, architecture, acceptance criteria, or Contract behavior without an approved upstream decision.
- Every code addition, modification, bug fix, or refactor requires Build, Test, and Verify.
- Test PASS alone does not satisfy DoD.
- The implementation author does not issue the final independent review verdict.
- Never integrate a non-`STABLE` Component.

## Outputs

- Scoped code/configuration/test changes.
- Changed paths and Component/Contract revisions.
- Exact build/test/review commands and results, limitations, risks, and traceability updates.
- Component state and Gate verdict.

## Failure Cases

- Build/test/review fails, expected behavior is ambiguous, or dependency is unavailable.
- The required fix belongs to Contract, data, design, architecture, Requirement, test, or environment.
- Workspace/base differs from delegated inputs.

## Escalation

Capture evidence and use Failure Diagnosis before repeated patching. After one bounded correction cycle—or immediately for cross-layer evidence—use Failure Escalation. Route material upstream changes through Clarification/Architecture Decision and Change Impact.

## Stop Conditions

Stop at `STABLE` with current Gate evidence, at `FAILED`/`UNVERIFIED` with diagnostics, or when upstream clarification/redesign is required. Do not proceed automatically into integration.
