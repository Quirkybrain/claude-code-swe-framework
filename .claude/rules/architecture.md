# Architecture Rules

- Define versioned Contracts before independent work across Component boundaries. Cover inputs, outputs, data structures, behavior, errors, boundaries, protocols, and compatibility.
- Keep Components cohesive, responsibilities and ownership clear, boundaries explicit, and coupling no greater than necessary.
- Prefer Components that can be developed, tested, integrated, and replaced independently.
- Frontend and backend communicate through their Contract; neither depends on the other's internal implementation.
- Keep UI concerns separate from application/business logic and infrastructure. Do not bury substantial domain or persistence logic in UI callbacks.
- When multi-language (i18n) support is requested without specific custom architecture, enforce the standard decoupled resource bundle pattern: maintain a single codebase, externalize all user-facing strings into separate per-locale resource files (e.g., `locales/{locale}.json`), use key-based dynamic lookups, and ensure clear fallback mechanisms. Never maintain duplicate or language-specific application codebases.
- Preserve existing architecture unless the target requires change; do not redesign opportunistically during implementation.
- Record significant architecture or technology choices in an ADR with Context, Options, Decision, Consequences, Constraints, and Affected Artifacts.
- Send user-owned product, cost, data, security, deployment, or organizational choices through the Clarification Gate before accepting an ADR.
- An architecture change invalidates affected downstream design, Contract, code, test, review, and integration evidence.
