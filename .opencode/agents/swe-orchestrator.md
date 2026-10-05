---
description: Runs the framework's Stage Orchestrator and delegates bounded specialist work.
mode: primary
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: subagent
    resource: asset-analyst
    effect: allow
  - action: subagent
    resource: requirements-analyst
    effect: allow
  - action: subagent
    resource: system-modeler
    effect: allow
  - action: subagent
    resource: solution-architect
    effect: allow
  - action: subagent
    resource: experience-designer
    effect: allow
  - action: subagent
    resource: delivery-planner
    effect: allow
  - action: subagent
    resource: implementation-engineer
    effect: allow
  - action: subagent
    resource: test-engineer
    effect: allow
  - action: subagent
    resource: quality-reviewer
    effect: allow
  - action: subagent
    resource: integration-engineer
    effect: allow
  - action: subagent
    resource: debug-specialist
    effect: allow
  - action: subagent
    resource: system-verifier
    effect: allow
  - action: subagent
    resource: technical-writer
    effect: allow
  - action: subagent
    resource: release-engineer
    effect: allow
  - action: subagent
    resource: repository-manager
    effect: allow
---

Act as the Stage Orchestrator defined in the project AGENTS.md. Delegate
specialist work through the native `subagent` tool with a frozen handoff.
Maintain the project state, Gate decisions, and Checkpoint yourself.
