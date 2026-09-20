---
name: traceability
description: Create, validate, and update bidirectional links from Requirements through design, architecture, APIs/Components, tasks, code, and tests. Use after Artifact changes, planning, implementation, testing, verification, or Change Impact.
---

# Traceability

## Purpose

Make it possible to determine what implements and tests each Requirement, why code exists, and what a change affects.

## Trigger

Run whenever traceable Artifacts are created/changed, before verification/Stage Gate, or when impact analysis lacks reliable links.

## Inputs

- Artifact Registry and current revisions.
- Requirements/use cases, design/models, architecture/ADRs, API/Contracts, Components, tasks, code, tests, findings, and release evidence.
- Workflow Level, target, and existing trace links.

## Prerequisites

- Each managed item has a stable ID or durable code/path reference.
- Distinguish current revisions from superseded history.

## Procedure

1. Define target-relevant chain: `Requirement → Design → Architecture → API/Component → Task → Code → Test`.
2. Add optional use-case/domain/model/ADR/review/release links where they reduce risk.
3. Walk each Requirement forward and record implementation and verification coverage.
4. Walk each changed code/test item backward to a Requirement, decision, defect, maintenance rationale, or explicit technical necessity.
5. Validate link revisions and semantics; a path mention alone is not proof of satisfaction.
6. Mark coverage as complete, partial, missing, stale, conflicting, or not applicable with rationale.
7. Detect Requirements without design/implementation/tests, code without rationale, orphan tests, and model/code drift.
8. Update links after Change Impact and preserve superseded history.
9. Scale detail to Workflow Level while retaining enough evidence for the current target.

## Decision Rules

- Traceability is bidirectional.
- One Requirement may map to many Components/tests; one code item may satisfy multiple justified concerns.
- Inferred Requirements retain `INFERRED` confidence in trace links.
- A passing test link does not prove Requirement completeness by itself.
- Lightweight tasks may use compact change-to-acceptance/test links; Strict work may require a formal matrix.

## Outputs

- Updated traceability matrix/links with IDs, revisions, relationship, status, and evidence.
- Forward/backward coverage summary.
- Orphan, missing, stale, conflicting, and unverified link findings.
- Inputs for Change Impact and System Verification.

## Failure Cases

- IDs/revisions are unstable or missing.
- Source code is generated or shared with ambiguous ownership.
- Requirements and observed behavior conflict.
- Link volume exceeds Process Budget without target prioritization.

## Escalation

Use Reverse Engineering to recover rationale/structure, Clarification Gate for intent, and Change Impact for stale downstream links. Escalate unjustified code rather than inventing a Requirement.

## Stop Conditions

Stop when target-relevant links are current and gaps explicit, or when authority/evidence blocks a reliable relationship. Do not claim coverage beyond evaluated scope.
