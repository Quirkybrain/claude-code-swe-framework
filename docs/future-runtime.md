# Future Runtime Capabilities

## Purpose

This document records capabilities that the Markdown-based Claude Code Framework cannot implement reliably. It prevents V1 from disguising prompt conventions as deterministic automation.

Nothing listed here is implemented by Phase 1. Inclusion is not a commitment to build a Runtime; each capability must justify its cost and risk reduction.

## V1 Boundary

V1 can use Claude Code reasoning and Markdown files to perform Intake, Artifact validation, Gap Analysis, adaptive planning, handoffs, Gates, Change Impact Analysis, and checkpoint recovery.

V1 cannot guarantee:

- transactional or atomic State updates;
- deterministic policy enforcement;
- automatic change detection and invalidation;
- exactly-once task execution;
- reliable multi-writer concurrency or automatic merging;
- continuous background operation;
- authenticated access to every external source;
- tamper-proof audit or compliance evidence.

Agent memory, auto memory, and chat history are not substitutes for project State.

## Candidate Hook Capabilities

Hooks are appropriate when an event must trigger the same deterministic check or side effect every time.

Potential uses:

- run formatting, linting, static analysis, or focused tests after code edits;
- block completion, commit, or release when required evidence is missing;
- detect code, Contract, or configuration changes and flag affected records `UNVERIFIED` or `STALE`;
- enforce protected paths or Agent write boundaries;
- intercept destructive commands, secret-file access, and production operations;
- record mandatory audit events at tool, Agent, checkpoint, or session boundaries;
- validate Artifact metadata structure before accepting a Gate record.

Hooks must not be introduced merely to replace reasoning that belongs in a Skill. They are for deterministic triggers and enforcement.

## Candidate MCP Capabilities

MCP is appropriate for authenticated, structured access to external systems or formats Claude Code cannot reliably access directly.

Potential integrations:

- design systems and Figma assets;
- issue trackers and planning systems;
- enterprise knowledge bases and document stores;
- source hosting and pull-request evidence;
- CI/CD, test management, deployment, and observability systems;
- cloud resources and configuration inventory;
- databases and schema catalogs with safe read-only access;
- proprietary file parsers and domain-specific analysis tools.

An MCP result remains an input Artifact or evidence source and must retain provenance, freshness, and access limitations.

## Candidate Runtime Capabilities

A separate Runtime may be justified only for guarantees that prompt-driven Markdown cannot provide.

### Transactional Artifact and State Graph

- structured persistence of Artifact, Component, Task, and Gate records;
- schema validation and referential integrity;
- atomic state transitions;
- automatic incremental dependency and impact calculation;
- queryable history and revision lineage.

### Reliable Scheduling and Concurrency

- durable task queues, leases, locks, retries, and cancellation;
- exactly-once or idempotent state transitions;
- dependency-aware scheduling across machines or sessions;
- resource quotas and bounded parallelism;
- recovery after process or network failure.

### Workspace and Integration Automation

- reliable worktree creation from the correct base revision;
- ownership and locking for write scopes;
- automatic diff collection and conflict detection;
- controlled merge/integration branches;
- validation before promotion and compensating rollback.

Native Claude Code worktrees isolate files but do not by themselves solve Contract conflicts, Artifact synchronization, automatic merging, or stable integration.

### Policy, Audit, and Compliance

- deterministic authorization and least-privilege enforcement;
- signed or content-addressed Gate evidence;
- tamper-evident audit logs;
- retention policies and approval workflows;
- organization-wide compliance reporting.

### Long-Running and Event-Driven Operation

- daemon or service execution;
- external event subscriptions;
- scheduled maintenance and monitoring;
- notifications and escalation;
- cross-session or cross-machine coordination.

### External Side-Effect Transactions

- unattended production deployment;
- coordinated changes across multiple external systems;
- rollback and compensation when only part of an operation succeeds;
- robust idempotency and reconciliation.

## Decision Criteria for Adding Automation

Before introducing a Hook, MCP integration, or Runtime, document:

1. The concrete V1 failure mode or manual cost.
2. Why Claude Code instructions and Artifacts are insufficient.
3. The required reliability and security guarantee.
4. New dependencies, operational burden, and failure modes.
5. Data handling and permission implications.
6. A fallback or recovery strategy.
7. How the capability preserves Artifact-driven, adaptive workflow semantics.

Automation must not create a mandatory fixed Agent chain or force every project through a full lifecycle.

## Explicit Non-Goals Until Justified

- generic workflow server
- Node.js or Python lifecycle application
- database solely because State exists
- always-on daemon
- mandatory cloud control plane
- proprietary Agent SDK wrapper around Claude Code
- fixed stage pipeline

The Framework remains Markdown-first unless a demonstrated reliability need warrants a narrowly scoped addition.
