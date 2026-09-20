---
name: artifact-validation
description: Validate an existing or newly produced Artifact for completeness, consistency, correctness, freshness, dependency compatibility, and target fitness. Use before reuse, handoff, downstream consumption, or a Gate decision.
---

# Artifact Validation

## Purpose

Decide whether a specific Artifact revision can safely support the declared target and downstream use, applying Reuse Before Regenerate.

## Trigger

Run before consuming an existing Artifact, after an Artifact is created or changed, when an upstream dependency changes, or when prior evidence is stale or incomplete.

## Inputs

- Artifact ID, type, content, revision, source, owner, and intended use.
- Required upstream Artifact revisions and applicable Project Constraints.
- Target Stage/Artifact, effective Workflow Level, prior validation, and known limitations.

## Prerequisites

- Confirm the exact revision and validation scope.
- Resolve or explicitly record uncertain Artifact type and provenance.
- Identify the minimum validation depth required by target risk.

## Procedure

1. Verify content-based Artifact classification and provenance.
2. Check completeness against its intended consumer and Definition of Done.
3. Check internal consistency and consistency with authoritative Artifacts.
4. Check correctness using source evidence, executable checks, or independent review appropriate to type.
5. Check freshness against upstream revisions, repository state, and `Last Verified`.
6. Check dependency compatibility, including versioned Contracts, schemas, constraints, and assumptions.
7. Check fitness for the current target; an Artifact may be valid for one scope but insufficient for another.
8. Record evidence, validator, evaluated revisions, coverage, limitations, and resulting status.
9. Select exactly one disposition: `REUSE`, `SUPPLEMENT`, `REVALIDATE`, or `REGENERATE`.

## Decision Rules

- `REUSE`: evidence is current and the Artifact is complete, consistent, correct, compatible, and sufficient for this target.
- `SUPPLEMENT`: useful content remains and bounded gaps can be repaired without replacing valid portions.
- `REVALIDATE`: content may still be correct, but freshness or evidence is insufficient.
- `REGENERATE`: evidence proves invalidity, or repair is riskier/costlier than replacement.
- Map the result to `VALID`, `PARTIAL`, `UNVERIFIED`, `STALE`, or `INVALID`; do not turn every failed check into `INVALID`.
- Never infer `VALID` from existence, format quality, author confidence, or an old PASS.

## Outputs

- Validation Record with scope, checks, evidence, dependency revisions, result, and limitations.
- One disposition: `REUSE`, `SUPPLEMENT`, `REVALIDATE`, or `REGENERATE`.
- Updated Artifact status and `Last Verified` when justified.
- Downstream impact and required follow-up.

## Failure Cases

- Required source or dependency revision is missing.
- Correctness cannot be checked with available evidence.
- The Artifact mixes incompatible revisions or authorities.
- Validation tooling or environment is unavailable.

Return `BLOCKED` or `UNVERIFIED` with missing evidence; never fabricate PASS.

## Escalation

Use the Clarification Gate for authority or intent conflicts. Use Change Impact when the Artifact or its basis changed. Escalate specialized correctness checks to the responsible Agent while preserving this validation scope.

## Stop Conditions

Stop after recording a supported disposition and state, when evidence is insufficient and explicitly blocked, or when user authority is required. Do not regenerate as part of this Skill unless separately authorized.
