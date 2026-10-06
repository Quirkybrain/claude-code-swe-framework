# Default Git Collaboration Policy

This policy applies when `config/git-policy.json` has `company_policy_path: null`.
An explicit user instruction has priority. When a company policy path is set,
read and pin that file; its applicable clauses override the corresponding
defaults here. `config/git-policy.json` provides machine-readable branch patterns
and merge strategy for the guard.

## Branch hierarchy and ownership

`main` is the protected release branch. Create an integration branch named for
the primary work type, then one `task/<task-id>` branch per small delegated task:

| Work | Integration branch | Example task branch |
|---|---|---|
| New feature | `feat/<name>` | `task/add-export-api` |
| Bug fix, including urgent fix | `fix/<name>` | `task/fix-null-crash` |
| Documentation only | `docs/<name>` | `task/update-install-guide` |
| Refactor | `refactor/<name>` | `task/extract-parser` |
| Tests only | `test/<name>` | `task/add-parser-regression` |
| Maintenance/build | `chore/<name>` | `task/upgrade-linter` |

The branch type follows the primary outcome, not the Agent role. A bug fix may
include regression tests and documentation on the same `fix/` integration
branch; a feature may include tests and docs on its `feat/` branch. If one
request contains independent outcomes, split them into bounded integration
branches and merge each after its own Gate. Do not create a separate `docs/`
branch merely because a feature needs a README update.

Each task branch belongs to one Agent and one worktree. The Agent commits only
its declared outputs. A report-only analyst or reviewer may write and commit
its own report, but may not edit the code or Artifact it reviews. The
`repository-manager` prepares branches/worktrees and performs merges; the
Orchestrator owns Gate decisions. Never have two Agents write in one worktree
or share one task branch.

## When to update branches

Before creating an integration branch, fetch the remote and fast-forward local
`main` only when it has an upstream and the working tree is clean. Without a
remote, use the inspected local `main`. Before creating a task branch, use the
latest committed integration tip. Before merging task into integration, fetch
remote updates if applicable, confirm both source and target tips, and
integrate any target changes explicitly. Before integration into `main`,
refresh `main` again. Do not run `git pull` or switch branches inside an active
handoff. A fetch does not merge; use `git pull --ff-only` only for a tracking
branch that should move by fast-forward. Never silently rebase or force-update
a branch after review.

## Task commits and review

Use a committed baseline and a clean task worktree before dispatch. A handoff
pins `task_branch`, `parent_branch`, and `commit_paths`. After local validation,
stage explicit paths, inspect `git diff --cached` and `git diff --cached --check`,
and commit before `finish` and independent review. Use a new commit for a fix
after review; do not amend a reviewed commit. A commit is evidence of a
revision, not a Quality Gate PASS.

Default subject: `<type>(<scope>): <summary>`, with optional scope, at most 72
characters and no trailing period. Types are `feat`, `fix`, `refactor`, `test`,
`docs`, `chore`. Match the commit type to the actual change; for example,
`fix(parser): handle empty input` or `docs(setup): explain installation`.

## Merge ladder

After a task passes its required Gate and commits a nonempty Gate report on its
task branch, merge its committed tip into the appropriate `feat/`, `fix/`,
`docs/`, `refactor/`, `test/`, or `chore/` integration branch with
`git merge --no-ff`. Record source/target refs, merge commit, conflicts, and
validation evidence. Resolve conflicts only against pinned Requirements and
Contracts; rerun affected checks after resolution. Repeat for small task
branches. After the complete integration branch passes its appropriate checks,
review, and Stage Gate, commit Gate and integration/regression evidence on that
branch, merge it into `main` with `--no-ff`, and verify the exact result. A
code-free docs branch uses relevant link/render checks rather than an unrelated
build. Never merge a failed or stale revision. Publishing, pushing, deleting
branches/worktrees, and deployment are separate actions.

## Company policy override

Set `company_policy_path` in `config/git-policy.json` to a real file under
`input/`, for example `input/standards/git.md`. Include that file as a pinned
handoff input with a unique section anchor or page/location. Company rules may
change naming, timing, message format, sync, or merge method. Update the
machine-readable `integration_branch_pattern`, `task_branch_pattern`, and merge
strategy in `config/git-policy.json` to match those rules. Older settings using
`feature_branch_pattern` remain supported when `integration_branch_pattern` is
absent. Unspecified clauses fall back to this default. Do not infer a company
policy merely because a sample file exists.
