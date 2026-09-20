---
name: integration-gate
description: Verify that individually STABLE Components remain correct when combined through Contract validation, integration, integration tests, and regression. Use before promoting any combined unit as stable.
---

# Integration Gate

## Purpose

Enforce that `A = STABLE` and `B = STABLE` does not imply `A+B = STABLE`.

## Trigger

Run when two or more Components are ready to combine, when Contracts change, or when an integrated unit needs fresh evidence.

## Inputs

- Exact Component revisions and their Component Quality Gate evidence.
- Versioned consumer/provider Contracts, integration design, and integration points.
- Integration workspace/base, test strategy, environment/data, risks, and rollback plan.

## Prerequisites

- Every participating Component is `STABLE` for the supplied revision.
- Contracts are sufficiently valid and compatible for attempted integration.
- Integration workspace and ownership are explicit; unverified changes are excluded.

## Procedure

1. Perform the Stable Component Check and reject stale/mismatched evidence.
2. Validate consumer/provider Contract versions, schemas, protocols, errors, and compatibility.
3. Confirm workspace base, constituent revisions, rollback point, and absence of overlapping untracked integration work.
4. Mark the combined unit `UNVERIFIED`.
5. Integrate the smallest dependency-ready set in controlled order.
6. Build/initialize the integrated unit.
7. Run Contract tests, integration tests, and relevant regression tests.
8. Validate cross-boundary data, error, security, performance, and lifecycle behavior as risk requires.
9. Diagnose failures at interface, Contract, data, integration implementation, environment, design, architecture, or Requirement level.
10. Record constituent revisions, commands, results, findings, and verdict.
11. Mark the combined unit `STABLE` only on Gate PASS.

## Decision Rules

- Never integrate `UNVERIFIED` or `FAILED` inputs into the stable baseline.
- Individual Components may remain `STABLE` after failure only when evidence isolates the defect to integration and their basis did not change.
- Do not silently modify Contracts to make Components fit.
- Regression depth follows actual combined impact.
- Worktree isolation prevents file collision but does not merge, validate, or synchronize State automatically.

## Outputs

- Integration Gate Record: `PASS`, `FAIL`, `BLOCKED`, or `USER_DECISION_REQUIRED`.
- Integrated revision and constituent/Contract revision manifest.
- Contract, integration, regression, and cross-cutting evidence.
- Integrated-unit state, failure classification, and next action.

## Failure Cases

- A Component is not truly `STABLE` or evidence is stale.
- Contracts are incompatible or missing.
- Integration environment/base is wrong or incomplete.
- Cross-Component failure cannot be isolated.

## Escalation

Use Failure Diagnosis for ambiguous failures and Failure Escalation after repeated local attempts. Use Change Impact when Contract/design changes invalidate Components. Request Clarification for product or authority choices.

## Stop Conditions

Stop at a recorded Gate verdict. Proceed to the next integration increment only after the current combined unit is `STABLE`; never proceed automatically to release.
