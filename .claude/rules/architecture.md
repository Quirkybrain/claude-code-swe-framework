# Architecture Rules

- Define versioned Contracts before independent work across Component boundaries. Cover inputs, outputs, data structures, behavior, errors, boundaries, protocols, and compatibility.
- Keep Components cohesive, responsibilities and ownership clear, boundaries explicit, and coupling no greater than necessary.
- Prefer Components that can be developed, tested, integrated, and replaced independently.
- Frontend and backend communicate through their Contract; neither depends on the other's internal implementation.
- Keep UI concerns separate from application/business logic and infrastructure. Do not bury substantial domain or persistence logic in UI callbacks.
- Preserve existing architecture unless the target requires change; do not redesign opportunistically during implementation.
- Record significant architecture or technology choices in an ADR with Context, Options, Decision, Consequences, Constraints, and Affected Artifacts.
- Send user-owned product, cost, data, security, deployment, or organizational choices through the Clarification Gate before accepting an ADR.
- An architecture change invalidates affected downstream design, Contract, code, test, review, and integration evidence.
