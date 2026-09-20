# Clarification Rules

- Infer only low-risk, local, reversible choices supported by sufficient context or a strong convention.
- Record every material inference used to proceed as an Assumption with its evidence, rationale, risk, affected scope, and confirmation method.
- Ask the user before choosing among reasonable alternatives that materially affect product behavior, architecture, technology stack, data model, security, deployment, cost, destructive actions, or substantial downstream work.
- `FULL_AUTO` does not authorize invented user intent or ungranted high-impact authority.
- Questions must be concrete and structured, offer a small set of meaningful options, and explain the important differences.
- Persist an answer in the appropriate Requirement, Constraint, Decision, or ADR; chat history alone is not durable authority.
- Do not ask again when a valid persisted answer already applies.
- Pause only the affected path when possible; independent work may continue if its dependencies remain valid.
