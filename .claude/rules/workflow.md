# Workflow Rules

- Follow the Minimum Necessary Path to the user's target; never run the full lifecycle by default.
- Let Artifact dependencies determine readiness and order. Never use a fixed Agent chain.
- Reuse valid existing work before supplementing, revalidating, or regenerating it.
- Generate an Artifact only when it reduces relevant risk, enables the target or downstream work, improves necessary collaboration/maintenance, or is explicitly requested.
- Keep process cost proportionate to the risk it reduces. Process Budget never waives checks required by actual risk.
- Adapt the Task Workflow Level when complexity, risk, or impact changes; do not mechanically inherit the Project Workflow Level.
- Select Agents and Skills on demand by responsibility, context, permissions, and required output.
- Do not continue past the Target Stage. When its Stage Gate passes, persist a Checkpoint, set `PAUSED_AT_STAGE`, and stop.
