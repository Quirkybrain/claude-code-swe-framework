---
name: project-intake
description: Discover, inspect, classify, and inventory existing project assets and initial engineering state. Use at project startup, after major input changes, when entering an unfamiliar repository, or before planning from existing work.
---

# Project Intake

## Purpose

Establish an evidence-backed answer to “what does this project have now?” without treating filenames, directories, or existing files as proof of Artifact type or validity.

## Trigger

Run at initial startup, on an unfamiliar or resumed project with uncertain state, after substantial new `input/` material arrives, or when the current inventory no longer matches the repository.

## Inputs

- User request, `config/project.md`, `input/`, and relevant repository content.
- Existing Artifact Registry, State, and latest Checkpoint when present.
- Target Stage or target Artifact, if known.

## Prerequisites

- Confirm the project root and accessible scope.
- Do not require organized input directories; treat placement and extension as hints only.
- Do not expose secrets or inspect irrelevant sensitive content.

## Procedure

1. Read Project Configuration, current State, Checkpoint, and target.
2. Scan `input/` and target-relevant repository areas; record skipped or inaccessible scope.
3. Inspect content sufficiently to identify each asset's meaning rather than inferring from its name alone.
4. Assign an Asset ID, source path, source kind, revision/freshness signal, and confidence.
5. Classify candidate Artifact type and likely lifecycle stage from content.
6. Determine initial completeness and status: `MISSING`, `PARTIAL`, or `UNVERIFIED`; never assign `VALID` solely because a file exists.
7. Detect duplicates, contradictions, obsolete variants, unreadable assets, and authority conflicts.
8. Identify candidate upstream/downstream dependencies and reusable evidence.
9. Build or update the Asset Inventory and Artifact Inventory.
10. Establish initial Current Stage, Artifact States, known Component States, open clarifications, assumptions, risks, and target-relevant next analysis.

## Decision Rules

- Classify by content first; use directory, filename, and extension only as supporting evidence.
- Preserve original assets; do not rewrite them during Intake.
- Mark reverse-engineered meaning `UNVERIFIED` and inferred requirements `INFERRED`.
- A conflict is recorded, not silently resolved.
- Limit deep inspection to the target and material risk; Intake is not full requirements or architecture work.

## Outputs

- Asset Inventory with provenance, classification basis, confidence, and coverage.
- Artifact Inventory with IDs, types, candidate dependencies, revisions, and canonical states.
- Initial State summary and current-stage hypothesis.
- Conflict, uncertainty, standards-source, and inaccessible-content logs.
- Recommended next validation or clarification, not a fixed Agent chain.

## Failure Cases

- Content cannot be read or interpreted.
- Repository scope is too large for complete inspection.
- State, Checkpoint, and repository evidence disagree.
- Multiple sources claim authority for incompatible facts.

Record the failure, coverage impact, and affected classifications. Keep uncertain items `UNVERIFIED`.

## Escalation

Use the Clarification Gate for authority or material intent conflicts. Route raw standards for one-time normalization into Project Constraints. Request specialized analysis only for target-relevant formats or domains that cannot be interpreted reliably.

## Stop Conditions

Stop when the requested scope is inventoried with explicit evidence and uncertainty, when a blocking clarification is identified, or when access prevents reliable Intake. Do not continue automatically into the full lifecycle.
