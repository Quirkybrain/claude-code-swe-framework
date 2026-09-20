---
name: failure-diagnosis
description: Observe, reproduce, classify, and determine the root cause and correct repair layer for a build, test, regression, integration, or environment failure. Use before patching when the cause is unknown or crosses layers.
---

# Failure Diagnosis

## Purpose

Replace speculative patching with an evidence-backed Root Cause Analysis and repair direction.

## Trigger

Run after a meaningful failure when the responsible layer is uncertain, on regression or integration failure, or before a second broad correction attempt.

## Inputs

- Expected/observed behavior, symptom, failing revision, reproduction, environment, logs, and reports.
- Recent changes and last-known-good revision.
- Relevant Requirements, architecture, detailed design, Contracts, interfaces, data, implementation, tests, and prior attempts.

## Prerequisites

- Preserve original failure evidence before changing code/tests/environment.
- Define the failure precisely enough to distinguish success from failure.

## Procedure

1. Observe and record the exact failure, scope, timing, revision, and environment.
2. Reproduce with the least invasive reliable method; record deterministic/intermittent status.
3. Build a timeline and compare failing behavior with last known good evidence.
4. Trace affected control, data, interface, and Contract paths.
5. Form multiple plausible hypotheses and identify discriminating checks.
6. Execute bounded diagnostics; falsify alternatives rather than confirming only the first theory.
7. Classify the responsible layer: Requirement, Architecture, Detailed Design, Contract, Interface, Data, Implementation, Test, Environment, or `UNKNOWN`.
8. Identify root cause, contributing factors, affected Artifacts/Components, and invalid evidence.
9. Select the smallest correct repair layer and required revalidation scope.
10. Record confidence, untested hypotheses, repair owner capability, and escalation threshold.

## Decision Rules

- Reproduction failure lowers confidence; it does not prove the issue absent.
- Root cause must explain all material observations better than alternatives.
- Do not edit production code or weaken tests merely to prove a hypothesis.
- Repair at the responsible layer, not the nearest editable line.
- Use `UNKNOWN` when evidence is insufficient.

## Outputs

- RCA report with observation, reproduction, evidence chain, hypotheses, and classification.
- Root cause/confidence or ranked unresolved hypotheses.
- Correct repair layer/owner, affected states, and revalidation plan.

## Failure Cases

- Failure cannot be reproduced and environments cannot be compared.
- Evidence/logs are unavailable or sensitive access is unauthorized.
- Expected behavior itself is ambiguous.
- Investigation budget expires without a supported root cause.

## Escalation

Use Clarification Gate for expected behavior/authority ambiguity. Invoke Failure Escalation for repeated failure, exhausted local diagnosis, broad cross-layer impact, or required stage rollback.

## Stop Conditions

Stop when root cause and repair layer are supported, when missing evidence blocks progress, or with ranked hypotheses at the investigation budget. Do not implement the fix in this Skill.
