---
name: adaptive-testing
description: Select, implement, and execute the smallest sufficient test scope for a change based on affected layer, risk, Contracts, security, and performance. Use after code changes, for test planning, or when existing evidence must be refreshed.
---

# Adaptive Testing

## Purpose

Produce revision-specific behavioral evidence without mechanically running every test layer for every change.

## Trigger

Run for any code change, when a Gate requires test evidence, after integration, after upstream behavior changes, or when prior test evidence becomes stale.

## Inputs

- Changed paths/revision, change type, affected Components, and blast radius.
- Requirement/acceptance IDs, Contracts, risk, Workflow Level, supported environments, and DoD.
- Existing tests, test data, prior failures, and regression history.

## Prerequisites

- Expected behavior is sufficiently defined.
- Confirm the test environment and exact revision under test.
- Distinguish missing product behavior from missing test coverage.

## Procedure

1. Classify the change: Pure Function, Module, API/Contract, Data, Multiple Components, Architecture, Security-sensitive, or Performance-sensitive.
2. Map affected Requirements, Contracts, failure modes, and regression surface.
3. Reuse valid tests and identify genuine coverage gaps.
4. Select the minimum sufficient layers:
   - Pure Function: unit plus focused regression.
   - Module: unit, module, and relevant regression.
   - API: unit, consumer/provider Contract, integration, and regression.
   - Data/schema/migration: validation, migration/rollback, compatibility, integrity, and regression.
   - Multiple Components: Component evidence, Contract, integration, and regression.
   - Architecture: unit, Contract, integration, subsystem/system, and regression.
   - Security-sensitive: threat-relevant negative/abuse, authorization, data handling, and security regression.
   - Performance-sensitive: representative load/baseline, resource/latency thresholds, and performance regression.
5. Add or update tests without weakening expectations to fit the implementation.
6. Execute prerequisites and selected tests; record commands, environment, versions, results, skips, flakes, and coverage limits.
7. Trace results to Requirements, Contracts, risks, and acceptance criteria.
8. Classify failures as known product, test, environment, or unknown; preserve evidence.

## Decision Rules

- Risk and impact determine depth; project size alone does not.
- API compatibility requires both consumer and provider evidence where applicable.
- Skipped, unavailable, quarantined, or flaky tests do not count as PASS.
- Any code change invalidates affected prior evidence.
- User Acceptance cannot be inferred from automated tests.

## Outputs

- Test scope/strategy and selection rationale.
- New or updated tests and fixtures when required.
- Revision/environment-specific Test Report.
- Traceability links, uncovered scope, failures, and recommended next action.

## Failure Cases

- Expected behavior or Contract is ambiguous.
- Environment/data/dependency is unavailable.
- Results are nondeterministic or cannot be tied to the revision.
- Test cost exceeds Process Budget but risk still demands evidence.

## Escalation

Use Clarification Gate for ambiguous outcomes, Failure Diagnosis for unknown/repeated failures, and Workflow Assessment when risk requires deeper evidence. Never delete or weaken a test merely to obtain PASS.

## Stop Conditions

Stop when sufficient current evidence exists, when a failure requires repair/diagnosis, or when environment/intent blocks reliable testing. Do not issue code-quality or Stage approval.
