# Coding Rules

- Follow normalized Project Constraints and the standards supplied under `input/standards/`.
- Follow the project's established style, structure, naming, tooling, and error-handling patterns unless an approved decision changes them.
- Inspect relevant code, tests, Contracts, and surrounding behavior before editing.
- Keep changes minimal, cohesive, and within the authorized task and write scope.
- Do not perform unrelated refactoring, formatting churn, dependency upgrades, or cleanup.
- Do not change public behavior, APIs, schemas, protocols, or other Contracts without explicit authorization and Change Impact analysis.
- Preserve compatibility where required and make intentional incompatibility explicit.
- Never expose or commit secrets; inspect and reproduce sensitive data only to the minimum extent required.
- Production, deployment, destructive, or other high-impact external actions require explicit authority and the applicable Gate.
- Do not hide failures, weaken validation, or classify incomplete work as done.
- Language- and framework-specific style belongs in Project Constraints from `input/standards/`, not in this Framework Rule.
