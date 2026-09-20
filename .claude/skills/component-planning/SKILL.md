---
name: component-planning
description: Decompose a validated system design into System, Subsystem, Module, Component, and Task graphs with Contracts, dependencies, integration points, parallel work, Gates, and milestones. Use before multi-component implementation or integration planning.
---

# Component Planning

## Purpose

Produce an executable graph of cohesive Components and tasks rather than a flat T1/T2/T3 list.

## Trigger

Run when architecture or detailed design must become bounded implementation work, especially for multi-module, parallel, or integration-sensitive changes.

## Inputs

- Validated Requirements, models, architecture, ADRs, Project Constraints, and target.
- Existing code/Component inventory, Workflow Level, risks, and delivery constraints.
- Known APIs, schemas, integration points, and current Component states.

## Prerequisites

- Resolve material architecture and product choices first.
- Ensure enough design exists to define boundaries without inventing upstream intent.

## Procedure

1. Decompose `System → Subsystem → Module → Component → Task` only to the depth needed for the target.
2. Give each Component a single cohesive responsibility, clear boundary, owner capability, inputs, outputs, and DoD.
3. Apply Contract First at every cross-Component boundary: specify Input, Output, Data Structure, Behavior, Error, Boundary, Protocol, version, and compatibility expectations.
4. Build the Component Graph and Task Graph with directional dependencies.
5. Identify integration points, consumer/provider relationships, shared data, and cross-cutting risks.
6. Mark tasks `READY` only when required Artifacts and Contracts are sufficiently valid.
7. Identify parallel work only where Contracts are stable and write scopes do not overlap.
8. Assign Component Quality Gates, Integration Gates, revalidation triggers, milestones, and Checkpoints.
9. Define integration owner/workspace and the order for incremental Lego-style assembly.
10. Verify every planned node contributes to the Minimum Necessary Path.

## Decision Rules

- Prefer high cohesion, low coupling, explicit interfaces, independent testing, and replaceability.
- Frontend and backend depend on their Contract, not each other's internals.
- Separate UI, application, business, and infrastructure concerns where applicable.
- No parallel implementation across an unstable Contract.
- Shared files or data ownership must have one explicit coordination boundary.
- Do not decompose beyond the point that planning cost exceeds risk reduction.

## Outputs

- Hierarchy and Component/Task Graphs.
- Versioned Contract definitions and ownership.
- Dependencies, ready/blocked nodes, parallel groups, integration points, milestones, Gates, and Checkpoints.
- Component/task DoD, write scopes, and integration plan.

## Failure Cases

- Boundaries require an unresolved architecture decision.
- Contracts conflict with Requirements or existing behavior.
- Cyclic ownership/dependencies cannot be bounded.
- Parallel work would overlap files or mutable data without coordination.

## Escalation

Use Architecture Decision for structural choices, Clarification Gate for product/authority choices, and Workflow Assessment when coordination risk increases. Do not hide unresolved design inside tasks.

## Stop Conditions

Stop when target-relevant Components and tasks are dependency-correct and execution-ready, or when upstream decisions block planning. Do not start implementation in this Skill.
