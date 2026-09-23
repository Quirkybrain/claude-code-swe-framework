# Workflow Rules

- Follow the Minimum Necessary Path to the user's target; never run the full lifecycle by default.
- Let Artifact dependencies determine readiness and order. Never use a fixed Agent chain.
- Reuse valid existing work before supplementing, revalidating, or regenerating it.
- Generate an Artifact only when it reduces relevant risk, enables the target or downstream work, improves necessary collaboration/maintenance, or is explicitly requested.
- Keep process cost proportionate to the risk it reduces. Process Budget never waives checks required by actual risk.
- Adapt the Task Workflow Level when complexity, risk, or impact changes; do not mechanically inherit the Project Workflow Level.
- In `STANDARD` and `STRICT` workflows, delegate specialist work by default using the native `Agent` tool (`Agent(subagent_type=...)`). The main session orchestrates, handles user clarification, and evaluates Gates, but does not author specialist design, models, code, or reviews directly.
- Direct authoring of specialist artifacts by the main session is a procedural deviation; it must be recorded under the artifact's `Producer` metadata with a concrete technical justification.
- Process compliance is a mandatory Stage Gate criterion: any deliverable with missing `Producer` metadata or unjustified deviation fails the Stage Gate.
- Do not continue past the Target Stage. When its Stage Gate passes, persist a Checkpoint, set `PAUSED_AT_STAGE`, and stop.
