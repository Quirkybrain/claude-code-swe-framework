# Change Management Rules

- Every material upstream change triggers Change Impact analysis before downstream evidence is reused.
- Follow Artifact dependencies, Contracts, traceability, Component relationships, and shared runtime/data boundaries to find affected consumers.
- Mark affected downstream Artifacts `STALE` and affected stable Components `UNVERIFIED`; use `INVALID` or `FAILED` only when evidence proves it.
- Invalidate revision-specific test, review, integration, and Gate evidence whose basis changed.
- Preserve previous evidence as history and preserve unaffected work when its independence is supported.
- Revalidate or repair only the minimum affected scope required by risk and target.
- Recompute the remaining Minimum Necessary Path after impact, clarification, decision change, failure escalation, or rollback.
- Do not continue repeated local patching without new evidence. Escalate to the responsible Requirement, architecture, design, Contract, data, test, or environment layer when needed.
