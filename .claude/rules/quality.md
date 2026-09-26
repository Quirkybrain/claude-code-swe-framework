# Testing and Review Rules

- Every code addition, modification, bug fix, or refactor requires Build (or equivalent), Test, and Verify on the resulting revision.
- A relevant code, Contract, dependency, configuration, or test-basis change invalidates affected prior test and Gate evidence.
- Select test depth from change type, risk, blast radius, Contract boundaries, and Workflow Level; do not run every test layer mechanically.
- Tests must cover the behavior and failure modes required by actual risk, including relevant regression.
- Skipped, unavailable, quarantined, flaky, or stale tests do not count as PASS.
- Never weaken, delete, or rewrite a valid expectation merely to make the implementation pass.
- Derive expected behavior and Golden updates from a pinned Requirement/Contract or an independently checked oracle, not from current implementation output alone. Record the source and why an old expectation changed.
- Testing and Review are independent: testing asks whether behavior works; review asks whether the implementation is reasonable, maintainable, compliant, and safe.
- Use Quick Review for small low-risk changes; add Code and architecture-consistency review for normal module work; add Architecture, Security, Performance, or Integration Review when the corresponding risk exists.
- The implementation author must not provide the final independent Review PASS for the same change.
- Review-driven edits invalidate affected test and review evidence and require proportionate revalidation.
- A PASS must cite current revision-specific evidence; test success alone does not satisfy a broader Definition of Done.
- Stage Gate evaluation must verify process compliance: all deliverables must possess valid 'Producer' metadata, reviews must be performed by independent roles ('agent:quality-reviewer'), and any main-session authored artifacts must have recorded, valid deviation rationales.
