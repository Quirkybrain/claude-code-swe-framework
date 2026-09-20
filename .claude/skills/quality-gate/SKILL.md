---
name: quality-gate
description: Evaluate a Component or task against its Definition of Done with checks scaled to LIGHTWEIGHT, STANDARD, or STRICT. Use after implementation and current validation evidence exist, before marking work DONE or a Component STABLE.
---

# Quality Gate

## Purpose

Issue an evidence-based Component Quality Gate verdict appropriate to the effective Task Workflow Level.

## Trigger

Run after implementation, build, testing, and required review; rerun whenever relevant code, Contract, dependencies, tests, or accepted criteria change.

## Inputs

- Component/task revision, Contract/design, Requirements, acceptance criteria, and DoD.
- Task Workflow Level and mandatory Project Constraints.
- Build, static check, test, review, traceability, security, and performance evidence.
- Known failures, risks, assumptions, waivers, and deviations.

## Prerequisites

- All evidence names the exact evaluated revision and scope.
- The implementation author cannot substitute self-assertion for required independent review.

## Procedure

1. Confirm scope, revision, DoD, Workflow Level, and mandatory checks.
2. Reject stale or mismatched evidence.
3. Apply level-specific baseline:
   - `LIGHTWEIGHT`: build/equivalent check, relevant tests, focused regression, acceptance criteria, and Quick Review.
   - `STANDARD`: build, static checks, unit/module tests, regression, Code Review, and acceptance criteria.
   - `STRICT`: build, static analysis, unit/Contract/integration/regression tests, security/performance checks as applicable, independent reviews, architecture compliance, traceability, and acceptance evidence.
4. Add checks demanded by actual impact even if the selected level baseline is lighter.
5. Verify every mandatory DoD item and accepted-risk authority.
6. Record evidence, failures, residual risks, exclusions, and verdict.
7. On PASS, mark the evaluated Component revision `STABLE`; on failure retain `UNVERIFIED` or set `FAILED`.

## Decision Rules

- Verdict is `PASS`, `FAIL`, `BLOCKED`, or `USER_DECISION_REQUIRED`.
- PASS requires current evidence for every mandatory item; partial success is not PASS.
- A waiver is a persisted risk Decision, not fabricated evidence.
- Security-sensitive or Contract/API changes may require Strict checks in an otherwise Lightweight task.
- Any post-review code change invalidates affected test and review evidence.

## Outputs

- Gate Record with scope, revisions, level, checks, evidence, verdict, findings, residual risks, and next action.
- Updated Component/task state.
- Required repair, revalidation, clarification, or integration readiness.

## Failure Cases

- Evidence references another revision or environment.
- Required checks are unavailable or inconclusive.
- DoD conflicts with Project Constraints.
- Risk acceptance lacks an authorized owner.

## Escalation

Use Failure Diagnosis before repeated correction. Use Clarification Gate for waivers/authority and Failure Escalation for repeated or cross-layer failure. Roll back to the responsible design/Requirement layer when evidence points upstream.

## Stop Conditions

Stop after a recorded verdict. Do not integrate unless the exact Component revision is `STABLE`; do not continue because implementation merely exists.
