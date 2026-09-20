---
name: change-impact
description: Propagate an upstream Artifact, Contract, decision, assumption, dependency, or code change through downstream dependencies, mark evidence stale or unverified, and define revalidation. Use whenever a validated basis changes.
---

# Change Impact

## Purpose

Invalidate only affected downstream work, preserve unaffected valid work, and trigger a new Minimum Necessary Path.

## Trigger

Run after any relevant upstream revision, disproven assumption, changed decision, Contract/schema/API change, dependency upgrade, or code modification to a stable Component.

## Inputs

- Changed item and old/new revisions, reason, effective decision, and changed semantics.
- Artifact dependency graph, traceability links, Component Graph, Contracts, and current State.
- Existing validation/Gate evidence, target, Workflow Level, and current Minimum Necessary Path.

## Prerequisites

- Identify the exact changed revision and avoid treating formatting-only edits as semantic changes without evidence.
- Preserve prior evidence as history.

## Procedure

1. Compare old and new revisions and describe semantic, interface, behavior, data, constraint, or evidence changes.
2. Locate direct downstream consumers through dependencies, Contracts, traceability, and code/test references.
3. Traverse transitively only while the changed semantics can affect the consumer.
4. For each affected Artifact, record the reason and mark `STALE` unless evidence already proves invalidity.
5. For affected `STABLE` Components, mark `UNVERIFIED`; set `FAILED` only when current evidence demonstrates failure.
6. Invalidate revision-specific test, review, integration, and Gate evidence as needed.
7. Identify unaffected scope and record why its evidence remains valid.
8. Define supplement, revalidation, repair, regeneration, testing, review, and integration scope.
9. Update risks, assumptions, decisions, Artifact Registry, Component State, and traceability.
10. Run Gap Analysis and recompute the Minimum Necessary Path.

## Decision Rules

- Dependence alone does not prove impact; record the semantic propagation path.
- Do not invalidate the whole project when bounded consumers are identifiable.
- Do not retain `VALID` or `STABLE` when its validation basis changed materially.
- Contract compatibility evidence can bound impact but must match exact versions.
- A code edit always invalidates affected Component verification even if behavior is intended to remain unchanged.

## Outputs

- Impact Set with changed source, downstream paths, affected revisions, and rationale.
- Updated `STALE`, `UNVERIFIED`, or `FAILED` states.
- Unaffected set with preservation rationale.
- Revalidation/rework plan and Minimum Path recomputation trigger.

## Failure Cases

- Dependency or traceability links are missing.
- Old/new revisions cannot be identified.
- Change semantics are ambiguous.
- Impact crosses an undocumented shared resource or runtime boundary.

## Escalation

Use Reverse Engineering/Traceability to recover missing links, Clarification Gate for changed intent, Architecture Decision for structural consequences, and Workflow Assessment when blast radius increases.

## Stop Conditions

Stop when affected and unaffected scope, state changes, and revalidation path are explicit, or when missing evidence blocks safe bounding. Do not execute all rework in this Skill.
