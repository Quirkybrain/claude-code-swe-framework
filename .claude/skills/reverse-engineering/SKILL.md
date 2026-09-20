---
name: reverse-engineering
description: Derive software structure, Contracts, architecture, UML/models, and cautiously inferred requirements from existing code, tests, schemas, configuration, and runtime evidence. Use when documentation is missing, stale, or must be reconciled with implementation.
---

# Reverse Engineering

## Purpose

Recover an evidence-backed engineering model from existing implementation without confusing observed behavior with confirmed user intent.

## Trigger

Run for legacy/existing projects, code-to-model requests, missing architecture/Contract documentation, maintenance intake, or design-code drift analysis.

## Inputs

- Scoped code revision, tests, schemas, configuration, build/deployment evidence, and runtime observations.
- Existing Requirements, models, architecture, documentation, decisions, and target.
- Project Constraints, known incidents, and terminology.

## Prerequisites

- Define the reverse-engineering scope and desired output depth.
- Confirm access and avoid executing unsafe/untrusted code without authorization.
- Treat existing tests and behavior as evidence, not automatic truth.

## Procedure

1. Inventory the scoped implementation, entry points, packages, build/runtime boundaries, and dependencies.
2. Trace representative control flows, data flows, persistent state, errors, trust boundaries, and external integrations.
3. Derive structure: layers, modules, Components, ownership, dependencies, and coupling.
4. Recover observable Contracts: inputs, outputs, data structures, behavior, errors, boundaries, protocols, and versions.
5. Infer architecture styles, deployment topology, quality mechanisms, and material decisions; cite code/config evidence.
6. Create target-relevant UML/domain/behavioral models with confidence and source links.
7. Compare recovered structure with existing design Artifacts and record drift/conflicts.
8. Infer candidate product Requirements only from supported behavior/evidence.
9. Label every inferred Requirement `INFERRED`, never `USER_CONFIRMED`; distinguish accidental behavior and defects.
10. Set derived Artifacts `UNVERIFIED` until independent validation or user confirmation.
11. Update traceability from each conclusion back to code/test/config evidence.

## Decision Rules

- Follow `Code → Structure → Architecture → UML/Model → Requirement Inference`; skip a layer only with explicit rationale.
- Do not infer user intent solely because code implements behavior.
- Tests reveal expected behavior claimed by their authors, not necessarily current business intent.
- Separate observed fact, reasoned inference, and assumption.
- Limit analysis to the target; do not document the entire system by default.

## Outputs

- Structure/Component and dependency view.
- Recovered Contracts and architecture/model Artifacts.
- Drift/conflict report and evidence index.
- Candidate Requirements labeled `INFERRED`, with confidence and confirmation needs.
- `UNVERIFIED` states and traceability links.

## Failure Cases

- Code does not build or important runtime paths are inaccessible.
- Generated/vendor code obscures ownership.
- Dynamic behavior cannot be established statically.
- Existing artifacts conflict with implementation without clear authority.

## Escalation

Use Clarification Gate to confirm inferred product intent, Failure Diagnosis for unexplained runtime behavior, and Architecture Decision only after recovered evidence is sufficient. Keep unknowns explicit.

## Stop Conditions

Stop when target-relevant structure and inferences are documented with evidence/confidence, or when access/ambiguity blocks further recovery. Do not rewrite implementation or promote inferred Requirements automatically.
