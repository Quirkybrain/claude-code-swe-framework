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
  "task_branch": "task/wp-42",
  "parent_branch": "feat/parser",
  "commit_paths": ["artifacts/30-architecture-contracts/contract-01.md"],
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

`finish` checks the handoff, pinned inputs, branch and policy hash, scoped Git commits, deliverables and original predecessor snapshots. A specialist with `commit_paths` must advance HEAD through linear commits containing only declared paths, with each declared path committed and clean. Reports are written and committed by their author; report-only roles never edit reviewed inputs. The actual-change inventory covers Git-visible files, ignored managed `state/` and `artifacts/` output scopes, and explicitly named ignored inputs, deliverables or snapshots. Other ignored files such as build caches are outside this inventory; name any ignored source file that matters. If a task fails or is interrupted, use `finish WP-42 --failed`, then inspect the result before creating a new handoff. Never re-pin to hide drift. The older no-policy mode retains the original HEAD-stable specialist behavior for projects that have not installed `config/git-policy.json`.

The tracked `.claude/settings.json` enables a `PreToolUse` hook for specialist `Agent` calls, including `repository-manager`; it blocks calls without an active, matching handoff. A second hook blocks `Write`/`Edit` outside the active handoff's declared outputs or worktree and blocks edits to its frozen read-only inputs. The settings file contains no credentials. If merging this template into a project with existing settings, preserve these hooks while keeping credentials in private settings. Hooks do not see arbitrary shell or external editor writes; the one-active-task-per-worktree rule and `finish` inventory catch observed changes in the task's own worktree when it returns. Direct shell writes into another worktree require process-level isolation to prevent completely; keep each task's shell commands inside its assigned worktree. Confirm installed hooks with Claude Code's `/hooks` command. For OpenCode V2, keep `AGENTS.md`, `opencode.json`, `.opencode/`, `.claude/hooks/`, and `scripts/`; its `swe-guards` plugin maps native `subagent` dispatch and file edits to these same checks. See [OpenCode V2 usage](opencode.md) for the runtime mapping and the manual closure check.

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

Use [Git collaboration](git-collaboration.md) for the full branch ladder, worktree setup, sync moments, company override and merge procedure. In branch-per-task mode (`config/git-policy.json`), each specialist handoff names `task_branch`, `parent_branch` and `commit_paths`; the specialist commits only those outputs. The guard checks the branch against the pinned parent tip at dispatch and verifies all new commit subjects, paths, ancestry and clean declared outputs at `finish`. A company policy file under `input/` must be configured with `company_policy_path`, included in `inputs` with a unique anchor or location, and declared as `commit_policy_path`; its pinned bytes replace the default subject-format check. The Orchestrator still evaluates the policy's meaning. The default subject is `<type>(<scope>): <summary>` (optional scope, type `feat|fix|refactor|test|docs|chore`, at most 72 characters, no final period).

`repository-manager` uses `repository_action: status` for delegated status evidence, `commit` plus exact `commit_paths` for its own scoped repository files, or `merge` to integrate. A merge handoff declares `source_branch`, `target_branch`, `writes` covering all changed files, a `gate_evidence_path` committed on the source branch, and a persistent evidence report in `deliverables`. Feature-to-main merges additionally require an `integration_evidence_path` committed on the source branch. Under the default patterns, only `task/...` → a typed integration branch (`feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`) → `main` is accepted. `finish` checks pinned tips, merge strategy, merged path scope and a separate report commit. Resolve conflicts and rerun affected checks before finishing. A clean committed baseline is required; do not create an empty baseline commit. Scoped recovery snapshots remain separate from normal commits.

An explicit company exception that defers an intermediate commit may use `defer_commit` and a pinned `commit_policy_path` to snapshot dirty write scopes before dispatch. In branch-per-task mode, each specialist still commits its final declared outputs before `finish`; deferred timing cannot skip final task evidence.

## 4. Disputes and context cost

- A reviewer reports a finding with a reproducible case, violated source reference, severity, and reviewed revision. The orchestrator routes product intent to the user/requirements owner, Contract content to the architect, and code defects to the implementer. Record one ruling and reopen it only for new evidence or a changed authoritative input. Reviewers keep their independent PASS/FAIL authority for the reviewed revision.
- On resume, load the current Checkpoint and active handoff first. Read only the source sections needed for the current task; fetch historical ADRs and full ledgers when a specific reference or inconsistency requires them. Do not paste complete source clauses into several downstream documents merely to restate them.
- For the next comparable runs, record API request count, input/output/cache tokens, Agent role, stage, elapsed time, correction cycles, and real defects found. Compare total cost **and** quality. The two recorded runs have an aggregate total but no stage/role breakdown, so a claimed savings percentage would be unsupported. Claude Code's optional [OpenTelemetry monitoring](https://code.claude.com/docs/en/monitoring-usage) can supply usage counters; do not enable export or collect prompt bodies without deciding where the data goes.
- The tracked `.claude/settings.json` and template `.claude/settings.example.json` use a 200,000-token auto-compaction window instead of the former 786,432-token example. This changes when Claude Code compacts context, not the model's capacity or the engineering Gates. It is a starting configuration, not a measured optimal value; compare cache-aware usage and correction rates before tuning it further. When applying this template to an existing project, merge this value with its private settings deliberately.

## 5. Code delivery includes a usable README

When the target delivers a runnable new project, the code-delivery DoD includes a project-root `README.md` that identifies the product, prerequisites, verified build/run/test commands, current delivery status, and known limits. Update an existing README rather than leaving the copied Framework introduction as the project's user guide. This minimum README is part of code delivery; the existing documentation and release stages still own the full guide, package notes, and final verification. A bounded bug fix updates documentation only where its behavior or commands changed.
