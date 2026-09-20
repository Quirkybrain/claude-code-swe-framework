---
name: workflow-assessment
description: Assess project and task complexity, risk, impact, size, maintainability, coordination, existing assets, and target stage to select LIGHTWEIGHT, STANDARD, or STRICT. Use for AUTO mode, new tasks, scope changes, or risk-driven escalation and de-escalation.
---

# Workflow Assessment

## Purpose

Choose proportionate engineering rigor while distinguishing the Project Workflow Level from the current Task Workflow Level.

## Trigger

Run when Workflow Mode is `AUTO`, at initial planning, when a task is introduced, or when new evidence changes complexity, risk, impact, or scope.

## Inputs

- User target, Project Configuration, Execution Mode, and existing State.
- Complexity, technical uncertainty, risk, impact, Project Size, and Task Size.
- Maintainability horizon, Team/Agent Count, coordination boundaries, existing assets, and Target Stage.
- Security, safety, compliance, data, deployment, compatibility, and cost constraints.

## Prerequisites

- Complete enough Intake to avoid scoring an unknown project as simple.
- Identify mandatory organizational or regulatory checks that no level may waive.

## Procedure

1. Assess each factor as low, medium, or high with evidence and uncertainty.
2. Determine the **Project Workflow Level** as the long-lived baseline for overall system risk and maintenance needs.
3. Determine the **Task Workflow Level** independently from the task's affected scope and actual risk.
4. Compare the task level with the project baseline; document every escalation or de-escalation.
5. Check Process Budget: added ceremony must reduce relevant risk or support the target.
6. Define the required Artifact, review, testing, traceability, and Gate depth for the chosen task level.
7. Record reassessment triggers such as cross-module impact, security discovery, Contract change, or reduced scope.

## Decision Rules

- `LIGHTWEIGHT`: bounded low-risk change, small blast radius, established design, and short/simple coordination; still require build/equivalent check, relevant tests, verification, quick review, and Checkpoint.
- `STANDARD`: normal multi-step or multi-module work needing explicit dependencies, design, review, testing, and integration evidence.
- `STRICT`: high security/safety/compliance risk, major architecture/data impact, broad compatibility or deployment impact, large coordination surface, or long-lived/high-reliability system.
- A Task may be `LIGHTWEIGHT` inside a `STRICT` project only when isolation and low risk are evidenced.
- A Task may exceed the Project Level when its risk demands it.
- Uncertainty with high possible impact raises rigor; it does not justify optimistic classification.

## Outputs

- Project Workflow Level and rationale.
- Task Workflow Level and rationale.
- Factor assessment, uncertainty, escalation/de-escalation reason, and reassessment triggers.
- Required evidence and Gate depth for the current task.

## Failure Cases

- Risk or target is too ambiguous to classify.
- Mandatory standards conflict with the requested level.
- The task boundary is not defined.
- Available assets have unknown validity.

## Escalation

Use Clarification Gate when accepting risk, cost, scope, or reduced rigor requires user authority. Escalate immediately when discovered security, architecture, data, or cross-component impact exceeds the current level.

## Stop Conditions

Stop when both levels and required evidence are recorded, when clarification blocks classification, or when Intake/validation must precede a reliable decision. Do not generate lifecycle work merely because a higher level exists.
