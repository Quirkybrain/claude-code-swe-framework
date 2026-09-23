# Artifact and Traceability Rules

- Use durable Artifacts as the primary interface between stages, Agents, and sessions; chat summaries do not replace them.
- Classify Artifact type from content. Directory, filename, and extension are hints only.
- Track each managed Artifact by stable ID, type, source, **Producer (产出实体)**, owner, revision, dependencies, status, validation evidence, assumptions, decisions, traceability, and `Last Verified`.
- Every managed Artifact MUST declare its `Producer` in its metadata header:
  - Standard delegation: `Producer: agent:<agent-name>`
  - Main-session exception: `Producer: orchestrator:main-session | Deviation: <concrete technical justification>`
- An Artifact authored directly by the main session without an explicit, valid `Deviation` rationale fails Artifact Validation Gate and cannot enter `VALID` status.
- Use only canonical statuses: `MISSING`, `PARTIAL`, `UNVERIFIED`, `VALID`, `STALE`, and `INVALID`.
- Treat `VALID` as revision-, scope-, dependency-, and target-specific, never permanent.
- Newly discovered or generated Artifacts are not `VALID` until evidence supports the declared use.
- A relevant upstream change makes affected downstream Artifacts `STALE`; do not reuse them before bounded revalidation or repair.
- Artifact ownership means responsibility for the revision, not authority to self-approve it.
- Validation must address completeness, consistency, correctness, freshness, dependency compatibility, target fitness, and producer compliance.
- Handoffs must identify Artifact paths/IDs and revisions, input dependencies, constraints, assumptions, allowed scope, DoD, Gate, and validation evidence.
- Maintain bidirectional, revision-aware traceability from Requirement through design/architecture, Contract/Component, task, code, and test at depth proportionate to risk.
- Never invent a Requirement to justify orphan code; record the missing rationale or inferred intent explicitly.
