---
name: code-review
description: Select and perform risk-appropriate Quick, Code, Architecture, Security, Performance, or Integration Review on a concrete revision. Use after implementation or integration to assess whether the solution is reasonable, maintainable, compliant, and safe.
---

# Code Review

## Purpose

Answer whether an implementation approach is reasonable and safe, independently from whether tests happen to pass.

## Trigger

Run after code changes, before a Quality Gate, after integration, or when architecture/security/performance risk requires independent assessment.

## Inputs

- Exact base/head revisions, diff, changed paths, declared scope, and intended behavior.
- Requirements, architecture, Contracts, Project Constraints, risk/impact, and current validation evidence.
- Workflow Level, known deviations, and prior findings.

## Prerequisites

- Reviewer is independent when required and defaults to read-only.
- Build/test evidence corresponds to the reviewed revision.
- Review scope and exclusions are explicit.

## Procedure

1. Classify review depth from change risk:
   - Small isolated change: Quick Review.
   - Normal module change: Code Review plus architecture consistency.
   - Cross-boundary/high-risk change: add Architecture, Security, Performance, or Integration Review as applicable.
2. Inspect the diff first, then affected call paths, data flows, trust boundaries, errors, and surrounding tests.
3. Check correctness risks, maintainability, cohesion/coupling, code smells, and scope discipline.
4. Check Requirement, architecture, Contract, API, compatibility, and Project Constraint compliance.
5. Check validation/error/recovery behavior and resource management.
6. Assess security and performance claims proportionally to exposure.
7. Assess test quality, relevance, negative/boundary coverage, and regression protection.
8. Validate each finding with location, evidence, impact, severity, and remediation direction.
9. Issue a scoped `PASS`, `FAIL`, or `BLOCKED` verdict and residual risk.

## Decision Rules

- Testing answers “does it run correctly?”; Review answers “is it implemented reasonably?”
- Style preference is not blocking unless it violates a Project Constraint or creates material risk.
- Distinguish proven defect from investigation need.
- Reviewer does not proactively fix findings; if explicitly reassigned to fix, another reviewer must approve.
- Any fix invalidates affected review/test evidence and requires revalidation.

## Outputs

- Review type/depth and selection rationale.
- Prioritized Review Report with evidence, severity, affected paths, and required remediation.
- Scoped verdict, exclusions, residual risks, and revalidation requirements.

## Failure Cases

- Review base/revision is unknown.
- Intended behavior or accepted risk is unresolved.
- Evidence is stale or insufficient.
- Reviewer authored the change where independence is mandatory.

## Escalation

Use Clarification Gate for accepted-risk or behavior choices, Architecture Decision for structural defects, Failure Diagnosis for cross-layer inconsistencies, and specialized security/performance analysis when evidence requires it.

## Stop Conditions

Stop after an evidence-backed scoped verdict or at `BLOCKED`. Do not modify reviewed code or issue Stage/User Acceptance approval.
