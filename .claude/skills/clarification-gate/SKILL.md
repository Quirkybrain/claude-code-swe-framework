---
name: clarification-gate
description: Decide whether unresolved ambiguity, conflict, intent, or authority requires a user decision and formulate bounded options with tradeoffs. Use before making material product, architecture, technology, data, security, deployment, cost, or high-impact choices.
---

# Clarification Gate

## Purpose

Prevent invented user intent while avoiding unnecessary questions for low-risk choices that evidence or strong convention resolves safely.

## Trigger

Run when multiple reasonable interpretations exist, assets conflict, a choice has material downstream impact, or the actor lacks authority to proceed.

## Inputs

- Exact ambiguity or decision, affected target, and blocked work.
- Relevant Requirements, Constraints, decisions, assumptions, assets, and prior answers.
- Reasonable options, consequences, reversibility, risk, cost, and downstream impact.
- Execution Mode and decision owner.

## Prerequisites

- Search persisted Artifacts and State to ensure the question was not already answered.
- Separate missing factual evidence from a genuine preference or authority decision.

## Procedure

1. State the unresolved issue and why it matters to the current target.
2. Test whether existing context or a strong low-risk convention resolves it reliably.
3. Evaluate impact on product behavior, architecture, technology stack, data model, security, deployment, cost, and large downstream work.
4. If material, identify two or three viable, mutually distinguishable options.
5. Explain each option's user-visible or engineering consequences concisely.
6. Recommend an option only when evidence supports a recommendation; do not disguise it as an automatic decision.
7. Ask a concrete, structured question with limited options and allow the user to provide another answer.
8. Set the affected path to `USER_DECISION_REQUIRED` while leaving independent work available.
9. After response, persist it in a Requirement, Constraint, Decision, or ADR and close the clarification.
10. Run Change Impact and recompute the Minimum Necessary Path when the answer changes prior assumptions or work.

## Decision Rules

- Must ask for material product behavior, architecture, stack, data, security, deployment, cost, destructive action, or broad downstream-impact decisions.
- May infer only low-risk, local, reversible choices supported by context or clear convention.
- Record a consequential inference as an Assumption with rationale and confirmation path.
- `FULL_AUTO` does not grant authority to invent material intent.
- Do not ask again when a valid persisted answer applies.

## Outputs

- Gate verdict: `PASS`, `USER_DECISION_REQUIRED`, or `BLOCKED`.
- Structured question, options, tradeoffs, recommendation if justified, and affected scope.
- Persisted answer/assumption and closed clarification after resolution.
- Change-impact and path-recomputation trigger when applicable.

## Failure Cases

- No legitimate decision options can be formed from available evidence.
- The decision owner is unavailable.
- Options conceal a prerequisite fact or use misleading tradeoffs.
- Conflicting persisted decisions have unclear authority.

## Escalation

Request additional analysis before questioning when options are technically undefined. Escalate authority conflicts explicitly. Never choose silently to keep the workflow moving.

## Stop Conditions

Stop when no material question exists and low-risk assumptions are recorded, or after issuing one bounded question and pausing affected work. Resume only after the answer is persisted.
