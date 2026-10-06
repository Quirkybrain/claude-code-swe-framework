# Default Git Collaboration Policy

This is the framework default when `config/git-policy.json` sets
`company_policy_path` to `null`. The current user instruction takes priority;
a configured company policy overrides only its applicable clauses. The JSON
settings make branch shapes, merge strategy, and hosted-main behavior
machine-checkable. Read the actual company source and pin it in each handoff.

## Branches and ownership

Keep `main` releasable. Create one short-lived integration branch for a coherent
outcome, then one `task/<task-id>` branch and separate worktree per delegated
small task. `repository-manager` creates branches and performs integrations;
each specialist commits only its declared outputs. A report-only reviewer
commits its report without changing reviewed files. The Orchestrator owns Gate
judgment. Never assign two active writers to one worktree or task branch.

| Primary outcome | Default integration branch | Also accepted |
|---|---|---|
| New capability | `feat/<name>` | `feature/<name>` |
| Defect correction | `fix/<name>` | `bugfix/<name>` |
| Urgent production correction | `hotfix/<name>` | — |
| Independent documentation | `docs/<name>` | — |
| Refactor, performance, tests, maintenance | `refactor/`, `test/`, `chore/` | — |
| Explicit release preparation | `release/<version>` | — |

Use the primary outcome to name the integration branch, regardless of Agent
role. Regression tests and a README update required by a bug fix belong on
its `fix/` branch. A `hotfix/` starts from the current production `main`; after
its approved merge, assess active integration branches and carry the fix
forward where needed. A `release/` branch is optional and only for a real
release candidate; do not create one for ordinary feature work. Company branch
names can replace this set through `integration_branch_pattern`.

## Synchronization and conflict handling

At branch creation and integration boundaries, inspect status and fetch remote
refs when a remote exists. On a clean local tracking `main`, use
`git pull --ff-only`; if it cannot fast-forward, stop and inspect the divergent
history. Create task branches from the latest committed integration tip. Do
not pull, switch, merge, or rebase inside an active handoff. A rebase may be
used deliberately on a private, unshared task branch before pinning; it
rewrites commit identities, so do not use `git pull --rebase` as a blanket
rule on reviewed or shared work. Resolve conflicts against pinned
Requirements/Contracts, record affected paths, and rerun affected checks.
Never force-push to hide conflicts.

## Atomic commits and messages

Commit one logical change at a time. Stage named paths or hunks with
`git add -p`; inspect `git diff --cached`, `git diff --cached --check`, and
status before committing. Commit validated work at a meaningful boundary and
before a review or dependent task. For a correction after review, make a new
commit and revalidate; do not amend a reviewed/shared commit. Before an
interruption, keep a recoverable snapshot and Checkpoint. An incomplete
checkpoint commit may preserve local work on a private task branch, but it
cannot satisfy the task Gate or be merged. A local commit is not a remote
backup.

Use Conventional Commits 1.0 style:

```text
<type>[(scope)][!]: <description>

[optional body explaining why and relevant verification]

[optional footer, such as Closes #123 or BREAKING CHANGE: ...]
```

`type` is required; `scope` is optional. The default guard accepts `feat`,
`fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`, and
`revert`, with a nonempty subject of at most 72 characters and no final
period. Match type to the specific commit, not merely its branch: a fix branch
may contain `fix`, `test`, and `docs` commits. For English descriptions prefer
a lowercase imperative verb (`add`, `fix`, `document`); a project with an
established Chinese history may use a concise Chinese description. Use a
blank line before a body; explain motivation and tradeoffs for nontrivial
changes. Mark a breaking API change with `!` after type/scope or a
`BREAKING CHANGE: <description>` footer, and explain migration in the body.
A footer may link an issue or task. The guard validates the default subject
shape; the Orchestrator reviews meaning, body, and company-specific rules.

Examples:

```text
fix(parser): handle empty input
test(parser): cover empty input
perf(cache): reduce allocations
feat(api)!: change response envelope

BREAKING CHANGE: clients must read the data field.
```

## Review, CI, and merge ladder

After a task passes its Gate and commits source-branch evidence, merge its tip
into the integration branch using the configured `merge_strategy` (`--no-ff`
by default). Record source and target tips, conflict resolution, changed
paths, review decision, and validation evidence. Revalidate the integrated
result; a passing task test does not prove the combined result stable.

After all small tasks pass, run relevant integration/regression checks and
independent review on the final integration branch. Refresh the main target
and rerun stale checks after a new commit or target change. For a hosted repo,
open a PR/MR from the integration branch to protected `main`; require at least
one independent review, resolved discussions, and the project's required CI
checks for the current revision. Configure these in the host's branch
protection/rulesets; a local Markdown rule or guard cannot enforce remote
permissions. `main_merge_mode: review_request_when_remote` blocks the local
main-merge handoff when any remote is configured. The hosting platform performs
the final merge after its requirements pass. For a repository without a
remote, a guarded local merge remains possible. `review_request` always blocks
local main merges; `local` explicitly allows them. The local merge guard does
not claim that a PR, CI, or hosted approval happened.

The `release/` branch, when used, follows the same review and protected-main
rules. Tagging, pushing, deployment, and branch/worktree deletion are separate
operations. Never merge a failed or stale revision.

## Company policy override

Place the exact company policy under `input/`, such as
`input/standards/git.md`, and set `company_policy_path` in
`config/git-policy.json`. Include that file as a handoff input with a unique
section anchor or location and set `commit_policy_path`. Change
`integration_branch_pattern`, `task_branch_pattern`, `merge_strategy`, and
`main_merge_mode` to match the company policy. The older
`feature_branch_pattern` remains valid if `integration_branch_pattern` is
absent. Unspecified clauses retain the defaults above. The guard pins policy
bytes but does not interpret natural-language approvals or test results.

## Source basis

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitLab branch protection](https://docs.gitlab.com/user/project/repository/branches/protected/) and [branching strategies](https://docs.gitlab.com/user/project/repository/branches/strategies/)
- [Conventional Commits 1.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Git pull](https://git-scm.com/docs/git-pull), [contributing and logical commits](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project.html)
