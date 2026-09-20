# Integration Rules

- Only exact Component revisions in `STABLE` state may enter a stable integration baseline.
- `A = STABLE` and `B = STABLE` does not imply `A+B = STABLE`.
- Every new combination starts `UNVERIFIED` and must pass compatible Contract checks, build/initialization, integration tests, and relevant regression before becoming stable.
- Record the integrated revision together with every constituent Component and Contract revision.
- Never silently change a Contract to make Components fit; route the change to its responsible design and decision boundary.
- Keep unverified or failed changes out of the stable integration baseline.
- Parallel writers require non-overlapping scope, stable Contracts, isolated workspaces, and an explicit integration owner.
- Worktree isolation prevents file collision; it does not merge changes, resolve semantic conflicts, synchronize State, or provide validation.
- Diagnose integration failure at the responsible interface, Contract, data, implementation, environment, design, architecture, or Requirement layer before repeated repair.
