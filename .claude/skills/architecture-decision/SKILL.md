---
name: architecture-decision
description: Evaluate significant technology or architecture alternatives and record an Architecture Decision Record. Use when a choice affects system structure, Contracts, data, security, deployment, compatibility, cost, or long-term evolution.
---

# Architecture Decision

## Purpose

Make consequential technical choices explicit, evidence-based, traceable, and reversible where possible through an ADR.

## Trigger

Run for major architecture/technology choices, meaningful deviations from existing architecture, or when an old decision must be superseded.

## Inputs

- Decision question, scope, owner, and urgency.
- Validated Requirements, quality attributes, Project Constraints, risks, existing architecture, and target.
- Candidate options with operational, security, data, cost, compatibility, and maintenance implications.

## Prerequisites

- Confirm the issue is architectural rather than an implementation detail.
- Identify who has authority when the decision embodies product preference, budget, organizational policy, or risk acceptance.

## Procedure

1. Define the ADR Context, forces, constraints, affected scope, and decision deadline.
2. Establish evaluation criteria tied to Requirements and quality attributes.
3. Identify viable Options, including retaining the current design when legitimate.
4. Compare options using evidence, tradeoffs, risks, reversibility, migration, and total lifecycle cost.
5. Reject options only with recorded rationale.
6. If authority belongs to the user, invoke Clarification Gate with bounded options before selecting.
7. Record the Decision and why it best satisfies the criteria.
8. Record positive/negative Consequences, constraints, follow-up work, and rollback/supersession conditions.
9. Link Affected Artifacts and invoke Change Impact for existing downstream work.
10. Validate ADR consistency with Requirements, Project Constraints, and related ADRs.

## Decision Rules

- Do not create an ADR for trivial, local, easily reversible implementation choices unless required by policy.
- Do not choose technology from familiarity alone.
- Major product behavior, cost, data ownership, security posture, deployment model, or organizational commitment requires user authority.
- A superseding ADR keeps the old decision as history and links both revisions.
- An undecided ADR is `PROPOSED`, not falsely `ACCEPTED`.

## Outputs

An ADR containing:

- Context
- Options and evaluation evidence
- Decision and status
- Consequences and risks
- Constraints and assumptions
- Affected Artifacts, dependencies, traceability, and follow-up validation

## Failure Cases

- Requirements or quality attributes are too ambiguous to compare options.
- Only one option is presented without evidence that alternatives are infeasible.
- Required cost/security/deployment information is unavailable.
- The actor lacks decision authority.

## Escalation

Use Clarification Gate for user-owned choices. Escalate missing domain/security/data evidence to the appropriate specialist. Increase Workflow Level when the decision's possible impact exceeds current rigor.

## Stop Conditions

Stop with an accepted/rejected/superseded ADR and impact plan, or at `USER_DECISION_REQUIRED`/`BLOCKED`. Do not implement the decision in this Skill.
