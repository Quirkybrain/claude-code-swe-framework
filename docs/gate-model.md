# Gate Model

## Purpose

Gates are evidence-based decisions that control whether work may proceed, must be corrected, needs user input, or should stop. A Gate is not an Agent and is not satisfied merely because a task reports completion.

The Framework defines five Gate types:

1. Clarification Gate
2. Artifact Validation Gate
3. Component Quality Gate
4. Integration Gate
5. Stage Gate

## Common Gate Record

Every Gate evaluation should record:

```text
Gate ID and type:
Purpose and scope:
Input Artifact / Component revisions:
Workflow Level:
Checks required:
Evidence reviewed:
Verdict:
Findings and residual risks:
Next action:
Evaluator and date / repository revision:
```

Recommended verdicts:

| Verdict | Meaning |
|---|---|
| `PENDING` | Evaluation has not completed |
| `PASS` | All required checks passed for the declared scope and revisions |
| `FAIL` | Evidence shows one or more required checks failed |
| `BLOCKED` | Evaluation cannot complete because required input, tool, permission, or evidence is unavailable |
| `USER_DECISION_REQUIRED` | Progress depends on material user intent or authority |

Gate results are revision-specific. A relevant change invalidates the prior result.

## 1. Clarification Gate

### Purpose

Prevent the Framework from inventing material user intent or silently resolving conflicts that substantially affect product behavior, architecture, technology, data, security, deployment, cost, or downstream work.

### Inputs

- User request and Project Configuration
- Relevant assets and Artifacts
- Conflicting statements or alternatives
- Known assumptions, decisions, risks, and constraints
- Impact analysis for each reasonable interpretation

### Checks

- Is the ambiguity real and material to the current target?
- Can context or an established convention resolve it with low risk?
- Would a choice affect user-visible behavior, architecture, data, security, deployment, cost, or substantial code?
- Are there multiple reasonable choices with meaningfully different consequences?
- Does proceeding require authority the user has not granted?
- Has the same question already been answered and persisted?

### PASS

PASS means either:

- no material clarification is required and any important low-risk inference is recorded as an Assumption; or
- the user answered, and the answer has been persisted in the relevant Requirement, Constraint, Decision, or ADR.

### FAIL

Use `USER_DECISION_REQUIRED`, rather than ordinary `FAIL`, when a material unresolved choice remains. `BLOCKED` applies when the decision owner cannot be reached or required context is unavailable.

### Next Action

- Ask one or more concrete, structured questions with options and tradeoffs.
- Pause only the affected path.
- After the answer, update dependent Artifacts, close the clarification, run Change Impact Analysis if needed, and recompute the Minimum Necessary Path.

## 2. Artifact Validation Gate

### Purpose

Decide whether an existing or newly produced Artifact can safely support downstream work and whether to Reuse, Supplement, Revalidate, or Regenerate it.

### Inputs

- Artifact content, ID, type, and revision
- Source assets and provenance
- Upstream dependency revisions
- Target and intended downstream use
- Applicable Project Constraints and standards
- Prior validation evidence and known limitations

### Checks

- Is the Artifact type correctly identified from content?
- Is required content complete for the intended use?
- Is it internally consistent and consistent with authoritative dependencies?
- Is it correct according to available evidence?
- Is it current relative to upstream revisions and project state?
- Does it satisfy relevant standards and constraints?
- Are assumptions and decisions explicit?
- Is validation evidence sufficient for the selected Workflow Level and target risk?

### PASS

PASS requires a recorded scope, evidence, validator, dependency revisions, and disposition. A sufficient Artifact becomes `VALID` for that scope and may satisfy downstream dependencies.

### FAIL

FAIL identifies concrete gaps, contradictions, invalid claims, stale dependencies, or insufficient evidence. Set the Artifact to `PARTIAL`, `UNVERIFIED`, `STALE`, or `INVALID` as appropriate; do not collapse every failure to `INVALID`.

### Next Action

- `Reuse` when valid and sufficient.
- `Supplement` when bounded gaps can be repaired safely.
- `Revalidate` when content may remain correct but evidence or freshness is missing.
- `Regenerate` only when invalid or when repair is riskier/more expensive than replacement.
- Update the registry and downstream impact before continuing.

## 3. Component Quality Gate

### Purpose

Determine whether a Component satisfies its Definition of Done and may become `STABLE`.

### Inputs

- Component implementation revision
- Component Contract and design inputs
- Acceptance criteria and Definition of Done
- Build, static-check, test, and review evidence
- Relevant Project Constraints and risk assessment
- Known defects, assumptions, and deviations

### Checks

- Is implementation complete for the declared scope?
- Does the Component build or otherwise validate syntactically?
- Do required unit/module/contract/regression tests pass?
- Does behavior satisfy acceptance criteria and Contract?
- Has required code, architecture, security, or performance review passed?
- Are test and review results based on the current code revision?
- Are known failures and residual risks within explicitly accepted bounds?
- Does the result satisfy the effective Task Workflow Level?

### PASS

PASS requires all mandatory Definition of Done items and current evidence. The Component may transition from `UNVERIFIED` to `STABLE` for the evaluated revision.

### FAIL

FAIL sets or keeps the Component as `FAILED` or `UNVERIFIED`. The result must identify failed checks and evidence. Code completion or a partial test pass cannot override it.

### Next Action

- Perform Root Cause Analysis before repeated modification.
- Repair at the responsible layer: implementation, interface, contract, data, design, architecture, or requirement.
- Rebuild, retest, and rereview affected scope.
- Escalate or roll back after repeated local failure.
- Do not integrate the Component until a new Gate passes.

## 4. Integration Gate

### Purpose

Verify that independently stable Components remain correct when combined and that their Contracts and interaction behavior are compatible.

### Inputs

- `STABLE` Component revisions and their evidence
- Versioned consumer/provider Contracts
- Integration design and integration points
- Integrated build or workspace revision
- Contract, integration, and regression test results
- Cross-cutting security, data, and performance risks

### Checks

- Are all participating Component revisions individually `STABLE`?
- Are consumer and provider Contract versions compatible?
- Does the integrated system build and initialize correctly?
- Do Contract and integration tests pass?
- Do relevant regression tests pass?
- Are error handling, data flow, boundaries, and protocols correct?
- Are cross-Component security and performance properties acceptable?
- Is evidence based on the exact integrated revision?

### PASS

PASS creates a stable integrated unit for the evaluated revision and scope. Record its constituent Component and Contract revisions.

### FAIL

FAIL leaves the integrated unit `FAILED` or `UNVERIFIED`. Individual Components may remain `STABLE` only if evidence shows the defect is strictly in integration and their inputs did not change.

### Next Action

- Diagnose whether the cause is interface, Contract, data, integration implementation, detailed design, architecture, or Requirement.
- Mark affected Artifacts or Components `STALE`/`UNVERIFIED` when their basis changes.
- Repair and rerun Contract, integration, and relevant regression tests.
- Never infer integration PASS from individual Component PASS.

## 5. Stage Gate

### Purpose

Determine whether a lifecycle stage has produced the necessary valid outcomes, whether its Definition of Done is satisfied, and whether the configured Target Stage has been reached.

### Inputs

- Current Stage and Target Stage
- Required Stage Artifacts and their states/revisions
- Stage Definition of Done
- Relevant Gate results and evidence
- Open clarifications, assumptions, decisions, risks, and deviations
- Current Minimum Necessary Path and downstream dependency readiness

### Checks

- Are all Artifacts required for the current target present and sufficiently `VALID`?
- Have applicable Clarification, Artifact, Component, and Integration Gates passed?
- Is the Stage Definition of Done satisfied at the selected Workflow Level?
- Are unresolved risks and deviations explicitly accepted or safely bounded?
- Is traceability sufficient for the risk and mode?
- Has the Target Stage been reached?
- Would continuing enter work beyond the user's requested scope?

### PASS

PASS means the current stage is complete for the declared target and scope.

- If Current Stage equals Target Stage, write a Checkpoint, set `PAUSED_AT_STAGE`, report delivered Artifacts and residual risks, and stop.
- If the target has not been reached, update state and continue only with the next ready node on the Minimum Necessary Path.

### FAIL

FAIL identifies missing, partial, stale, invalid, or insufficiently evidenced outcomes. `BLOCKED` or `USER_DECISION_REQUIRED` applies when appropriate.

### Next Action

- Rework only affected Artifacts or validations.
- Request clarification when intent or authority is missing.
- Roll back to the responsible earlier stage when the root cause lies there.
- Recompute the Minimum Necessary Path.
- Do not continue merely because a later lifecycle stage exists.

## Adaptive Gate Depth

Gate types remain the same across Workflow Levels; required evidence scales with risk.

| Level | Typical quality evidence |
|---|---|
| `LIGHTWEIGHT` | Build or equivalent check, focused tests, relevant regression, acceptance criteria, quick review |
| `STANDARD` | Build, static checks, unit/module tests, regression, code review, acceptance criteria |
| `STRICT` | Build, static analysis, unit/contract/integration/regression tests, security/performance checks, independent review, architecture compliance, traceability, acceptance evidence |

Adaptive depth cannot remove checks demanded by the actual change. An API or Contract change may require integration evidence even inside an otherwise Lightweight project.

## Gate Integrity

- An evaluator must not claim PASS without current evidence.
- Implementation authors do not provide final independent Review PASS for their own changes.
- Any change made in response to review invalidates affected test and review evidence.
- Waiving a required check is a user/authority Decision with risk and consequences, not a fabricated PASS.
- Markdown V1 guides Gate behavior but cannot mechanically prevent bypass; deterministic enforcement belongs to future Hook or policy work.
