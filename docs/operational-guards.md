# Operational Guards for the Existing Workflow

These checks support the existing Artifact → Agent → Gate → Checkpoint workflow. They do not choose stages, technical decisions, or Gate verdicts. Run them from the project root with Python 3 and Git. Keep `CLAUDE.md`, `scripts/`, `.claude/agents/`, and the relevant `.claude/hooks/` files when copying the template into a project. A baseline Git commit must exist before a modifying handoff.

## 1. A short, versioned Agent handoff

Write one JSON file under `state/handoffs/` for each delegated task. Name authoritative files and exact anchors instead of copying their normative text into a prompt. For a request given only in chat, capture its text once, check the saved bytes against the user's message, and use that file as an input:

```sh
python3 scripts/swe_guard.py capture-chat WP-42 <<'REQUEST'
The user's request, copied verbatim once.
REQUEST
```

This creates `state/handoffs/WP-42.request.md` without overwriting an earlier request. The shell command does not read the chat transcript automatically; the Orchestrator must compare the saved text with the original user message before pinning it. Existing files under `input/` can be referenced directly. Example amendment handoff:

```json
{
  "task_id": "WP-42",
  "role": "implementation-engineer",
  "inputs": [
    {"path": "artifacts/30-architecture-contracts/contract-01.md", "anchor": "## 7.1 Exit codes"},
    {"path": "state/handoffs/WP-42.request.md"}
  ],
  "writes": ["artifacts/30-architecture-contracts/contract-01.md"],
  "deliverables": ["artifacts/30-architecture-contracts/contract-01.md"],
  "snapshot_paths": ["artifacts/30-architecture-contracts/contract-01.md", "state/handoffs/WP-42.request.md"]
}
```

`inputs` are files; `anchor` is optional but, when supplied, must occur exactly once. `writes` are declared scopes; `deliverables` must contain at least one persistent, nonempty file and must be created or changed during the task. Both `writes` and `deliverables` count as output scopes for conflict and actual-change checks. For `quality-reviewer`, also set `review_targets` to the reviewed files or directories. `snapshot_paths` selects the current files to preserve. Keep passwords, API keys, local settings, and unrelated files out of this list. The guard pins the current HEAD and blocks dispatch if the planned write scope contains uncommitted changes under the default commit timing.

After checking that the source and the current user decisions are correct, generate the hashes mechanically:

```sh
python3 scripts/swe_guard.py pin state/handoffs/WP-42.json
python3 scripts/swe_guard.py snapshot state/handoffs/WP-42.json
python3 scripts/swe_guard.py begin state/handoffs/WP-42.json
```

The `snapshot` step is required when a handoff will change an existing file or the `quality-reviewer` will review named targets. Include every known predecessor in `snapshot_paths`. If a task may amend additional existing files inside a broad `writes` directory, snapshot that directory before dispatch; otherwise `finish` will block the unprotected amendment. `begin` checks the actual snapshot ref, byte coverage, input bytes, baseline HEAD, and shared cross-worktree read/write registry. Registration is serialized with a Git-common-dir file lock. One worktree may have only one active handoff at a time; use separate worktrees for genuinely independent parallel work. A normal new-file task with no predecessor/review target can omit `snapshot`. The Agent prompt carries the task goal and this exact line:

```text
HANDOFF: state/handoffs/WP-42.json
```

The Agent reads the pinned sources. It must report a semantic contradiction rather than silently re-pin or rewrite them. On return:

```sh
python3 scripts/swe_guard.py finish WP-42
```

`finish` checks that the handoff and inputs outside the Agent's own write scope stayed fixed, HEAD still matches the pinned baseline for ordinary specialist tasks, the Git index did not change during a non-commit task, every observed changed file stays inside declared output scopes, and every changed existing file has its original bytes in a matching Git snapshot. It also requires every named deliverable to be a nonempty file created or changed during the task. The actual-change inventory covers all Git-visible files, ignored files in managed `state/` and `artifacts/` output scopes, and explicitly named ignored inputs, deliverables, or file snapshots. Other Git-ignored files, such as build caches, are outside this inventory; explicitly name any ignored source file that matters to the handoff. A read-only Agent can return its complete report in its tool response; the Orchestrator persists those exact bytes to a declared deliverable with `capture-return WP-42 artifacts/60-quality/review.md` using stdin before `finish`. Do not paraphrase the report. A failure leaves the task active for investigation. If the task failed or was interrupted, record that outcome with `finish WP-42 --failed`; then revise and re-pin a new handoff before retrying. Do not use `pin` to hide an unexpected upstream change.

The tracked `.claude/settings.json` enables a `PreToolUse` hook for specialist `Agent` calls, including `repository-manager`; it blocks calls without an active, matching handoff. A second hook blocks `Write`/`Edit` outside the active handoff's declared outputs or worktree and blocks edits to its frozen read-only inputs. The settings file contains no credentials. If merging this template into a project with existing settings, preserve these hooks while keeping credentials in private settings. Hooks do not see arbitrary shell or external editor writes; the one-active-task-per-worktree rule and `finish` inventory catch observed changes in the task's own worktree when it returns. Direct shell writes into another worktree require process-level isolation to prevent completely; keep each task's shell commands inside its assigned worktree. Confirm installed hooks with Claude Code's `/hooks` command.

## 2. Recoverable local Git snapshot

Before amending a managed predecessor, use its pinned amendment handoff to snapshot the old version. Before handing code to independent Review, create a reviewer handoff with `review_targets` and snapshot the current reviewed revision. Do the same at a significant Checkpoint when uncommitted changes matter:

```sh
python3 scripts/swe_guard.py snapshot state/handoffs/WP-42.json
```

The command puts selected working-tree paths, including ignored or uncommitted files, in a local commit under `refs/swe/snapshots/`, together with the tracked HEAD baseline. It writes a manifest of selected paths and byte hashes in the shared Git common-dir. `begin` checks the ref, manifest, and byte-identical coverage; an absent or changed ref blocks dispatch. The command does not change the current branch, ordinary index, or working files. Record the ref in the existing Checkpoint or Review evidence. This is a local recovery anchor, not a release commit or remote backup. Inspect selected content before sharing Git refs.

After interruption:

```sh
python3 scripts/swe_guard.py status
git show 'refs/swe/snapshots/ID:path/to/file'
```

Compare the snapshot and current files before restoring anything. If Git is unavailable, the snapshot command fails and the task must not claim a recoverable Git anchor. A hard drive lost along with its `.git` directory still needs an external backup.

## 3. Repository management and commit policy

`repository-manager` owns scoped Git commits and repository-state evidence in STANDARD/STRICT work. Its handoff declares `"repository_action": "status"` for read-only status work, or `"repository_action": "commit"` with explicit `"commit_paths": ["src/parser.py", "tests/test_parser.py"]` for a real commit. The default action is `status` for older status-only handoffs. The commit action fails at `finish` unless HEAD advances through ordinary commits, every committed path is inside `commit_paths`, every declared commit path has a committed change, and those paths are clean afterward. Under the default policy, each new commit subject must match the documented format. A cited, pinned `commit_policy_path` under `input/` overrides the default subject check; the Agent and Orchestrator must still verify that company rule's actual meaning. The Orchestrator checks status cheaply at task start, Agent return, Gate, commit, resume, and stop; it does not launch an Agent merely to poll. Before bug fixes, features, refactors, or Artifact/documentation amendments, use a committed baseline. A clean current HEAD already qualifies; do not create an empty commit. Commit the validated task result before independent review or dependent work by default. If a company/project policy in `input/` specifies a different timing or message format, follow its applicable clause and cite it. The recovery snapshot requirement remains separate from ordinary commit timing.
Under the default policy, a `quality-reviewer` handoff also refuses uncommitted review targets. The `repository-manager` finish record in the shared Git common-dir captures the final HEAD and remaining short status after its task. A company policy that defers review commits must be cited through the handoff exception below.

If an applicable company policy deliberately defers commits while a planned write scope remains dirty, include its `input/` file in `inputs` with a unique text `anchor` when possible. Add `"defer_commit": true` and `"commit_policy_path": "input/standards/git.md"` to the handoff. For a binary policy such as PDF, add `"commit_policy_location": "page 3, Commit timing"` instead of an anchor. The guard requires a snapshot covering that entire dirty write scope before `begin`. A policy that only changes message formatting does not need this exception. The Agent/Orchestrator remains responsible for reading the actual policy; the script verifies cited file bytes and snapshot, not policy meaning.

Default commit message: `<type>(<scope>): <summary>` with optional scope, type from `feat|fix|refactor|test|docs|chore`, and a specific subject of at most 72 characters without a trailing period. Examples: `feat(cli): add JSON report output`, `fix(scanner): preserve --help exit code`. Stage explicit paths, inspect the staged diff and `git diff --cached --check`, then record commit ID and remaining dirty paths. Never include unrelated user changes or secrets to make a commit appear clean. See [repository-manager.md](../.claude/agents/repository-manager.md) and [repository.md](../.claude/rules/repository.md).

## 4. Disputes and context cost

- A reviewer reports a finding with a reproducible case, violated source reference, severity, and reviewed revision. The orchestrator routes product intent to the user/requirements owner, Contract content to the architect, and code defects to the implementer. Record one ruling and reopen it only for new evidence or a changed authoritative input. Reviewers keep their independent PASS/FAIL authority for the reviewed revision.
- On resume, load the current Checkpoint and active handoff first. Read only the source sections needed for the current task; fetch historical ADRs and full ledgers when a specific reference or inconsistency requires them. Do not paste complete source clauses into several downstream documents merely to restate them.
- For the next comparable runs, record API request count, input/output/cache tokens, Agent role, stage, elapsed time, correction cycles, and real defects found. Compare total cost **and** quality. The two recorded runs have an aggregate total but no stage/role breakdown, so a claimed savings percentage would be unsupported. Claude Code's optional [OpenTelemetry monitoring](https://code.claude.com/docs/en/monitoring-usage) can supply usage counters; do not enable export or collect prompt bodies without deciding where the data goes.
- The tracked `.claude/settings.json` and template `.claude/settings.example.json` use a 200,000-token auto-compaction window instead of the former 786,432-token example. This changes when Claude Code compacts context, not the model's capacity or the engineering Gates. It is a starting configuration, not a measured optimal value; compare cache-aware usage and correction rates before tuning it further. When applying this template to an existing project, merge this value with its private settings deliberately.

## 5. Code delivery includes a usable README

When the target delivers a runnable new project, the code-delivery DoD includes a project-root `README.md` that identifies the product, prerequisites, verified build/run/test commands, current delivery status, and known limits. Update an existing README rather than leaving the copied Framework introduction as the project's user guide. This minimum README is part of code delivery; the existing documentation and release stages still own the full guide, package notes, and final verification. A bounded bug fix updates documentation only where its behavior or commands changed.
