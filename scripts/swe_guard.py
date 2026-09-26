#!/usr/bin/env python3
"""Small, deterministic handoff and recovery checks for the Markdown workflow.

Run from the project root. This is a guard for the existing orchestrator, not a
scheduler or a replacement for Artifact validation and Gates.
"""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4


class GuardError(Exception):
    pass


def git(root, *args, env=None, input_text=None):
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        input=input_text,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if result.returncode:
        raise GuardError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.rstrip("\n")


def git_blob(root, revision, path):
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise GuardError(f"snapshot does not contain {path}: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def common_dir(root):
    name = git(root, "rev-parse", "--git-common-dir")
    return (root / name).resolve()


def swe_dir(root):
    directory = common_dir(root) / "swe"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


@contextmanager
def dispatch_lock(root):
    """Serialize check/register/finish across all worktrees of one repository."""
    with (swe_dir(root) / "dispatch.lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            if not lock.read(1):
                lock.write(b"\0")
                lock.flush()
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def project_root():
    root = Path.cwd().resolve()
    if not (root / "CLAUDE.md").is_file():
        raise GuardError("run from a project root containing CLAUDE.md")
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise GuardError("run from the Git repository root")
    return root


def relative_path(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise GuardError(f"invalid relative path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("..", ".git") for part in path.parts) or value == ".":
        raise GuardError(f"path must stay inside the project, outside .git: {value!r}")
    resolved = (root / str(path)).resolve()
    if os.path.commonpath([str(root), str(resolved)]) != str(root):
        raise GuardError(f"path escapes the project: {value!r}")
    return path.as_posix()


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_spec(root, name):
    path = root / relative_path(root, name)
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise GuardError(f"cannot read handoff {name}: {error}") from error
    if not isinstance(spec, dict):
        raise GuardError("handoff must be a JSON object")
    task_id = spec.get("task_id")
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", task_id):
        raise GuardError("task_id must contain only letters, digits, dots, underscores or hyphens")
    if not isinstance(spec.get("role"), str) or not spec["role"]:
        raise GuardError("role must name the delegated Agent")
    for field in ("inputs", "writes", "deliverables", "snapshot_paths"):
        if not isinstance(spec.get(field), list):
            raise GuardError(f"{field} must be a list")
    if not spec["inputs"]:
        raise GuardError("inputs must name a file; capture a chat-only request first")
    if not spec["deliverables"]:
        raise GuardError("deliverables must name at least one persistent output")
    targets = spec.get("review_targets", [])
    if not isinstance(targets, list):
        raise GuardError("review_targets must be a list")
    if spec["role"] == "quality-reviewer" and not targets:
        raise GuardError("quality-reviewer must name review_targets")
    for item in spec["inputs"]:
        if not isinstance(item, dict) or "path" not in item:
            raise GuardError("each input needs a path")
        relative_path(root, item["path"])
        if "anchor" in item and (not isinstance(item["anchor"], str) or not item["anchor"]):
            raise GuardError("anchor must be a nonempty literal string")
    for field in ("writes", "deliverables", "snapshot_paths"):
        for item in spec[field]:
            relative_path(root, item)
    for item in targets:
        relative_path(root, item)
    defer_commit = spec.get("defer_commit", False)
    if not isinstance(defer_commit, bool):
        raise GuardError("defer_commit must be true or false")
    policy_path = spec.get("commit_policy_path")
    if defer_commit or policy_path is not None:
        if not isinstance(policy_path, str) or not policy_path.startswith("input/"):
            raise GuardError("commit_policy_path must name a policy under input/")
        relative_path(root, policy_path)
        matches = [item for item in spec["inputs"] if item["path"] == policy_path]
        location = spec.get("commit_policy_location")
        if not matches or not (matches[0].get("anchor") or isinstance(location, str) and location.strip()):
            raise GuardError("commit policy requires its input file and a section anchor or page/location")
    action = spec.get("repository_action", "status")
    if spec["role"] == "repository-manager":
        if action not in ("status", "commit"):
            raise GuardError("repository_action must be status or commit")
        paths = spec.get("commit_paths", [])
        if not isinstance(paths, list):
            raise GuardError("commit_paths must be a list")
        for item in paths:
            relative_path(root, item)
        if action == "commit" and not paths:
            raise GuardError("commit action requires explicit commit_paths")
        if action == "status" and paths:
            raise GuardError("status action cannot declare commit_paths")
    elif "repository_action" in spec or "commit_paths" in spec:
        raise GuardError("repository_action and commit_paths belong to repository-manager")
    return path, spec


def check_inputs(root, spec, *, exclude_writes=False):
    for item in spec["inputs"]:
        name = relative_path(root, item["path"])
        if exclude_writes and any(overlaps(name, scope) for scope in spec["writes"]):
            continue
        path = root / name
        if not path.is_file():
            raise GuardError(f"input missing: {name}")
        expected = item.get("sha256", "")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise GuardError(f"input has no valid SHA-256 pin: {name}; run pin first")
        actual = file_hash(path)
        if actual != expected:
            raise GuardError(f"input changed: {name} (expected {expected}, found {actual})")
        if "anchor" in item:
            try:
                count = path.read_text(encoding="utf-8").count(item["anchor"])
            except UnicodeError as error:
                raise GuardError(f"anchor needs UTF-8 input: {name}") from error
            if count != 1:
                raise GuardError(f"anchor must occur exactly once in {name}; found {count}")
        print(f"OK input {name} sha256={actual}")


def overlaps(left, right):
    a, b = PurePosixPath(left).parts, PurePosixPath(right).parts
    return a[: len(b)] == b or b[: len(a)] == a


def covers(scope, path):
    a, b = PurePosixPath(scope).parts, PurePosixPath(path).parts
    return b[: len(a)] == a


def protected_paths(root, spec):
    """Existing predecessors and review targets that need a verified snapshot."""
    protected = list(spec.get("review_targets", []))
    protected += [
        item["path"] for item in spec["inputs"]
        if any(overlaps(item["path"], scope) for scope in spec["writes"])
    ]
    protected += [
        path for path in spec["deliverables"]
        if (root / path).exists() and any(overlaps(path, scope) for scope in spec["writes"])
    ]
    if spec.get("defer_commit"):
        protected += [scope for scope in spec["writes"] if dirty_scope(root, spec, scope)]
    return list(dict.fromkeys(protected))


def dirty_scope(root, spec, scope):
    dirty = git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", scope)
    generated = {
        f"state/handoffs/{spec['task_id']}.json",
        f"state/handoffs/{spec['task_id']}.request.md",
    }
    return [line for line in dirty.splitlines() if line[3:] not in generated]


def selected_files(root, paths):
    result = {}
    for name in paths:
        target = root / relative_path(root, name)
        if not target.exists() and not target.is_symlink():
            raise GuardError(f"snapshot path missing: {name}")
        members = target.rglob("*") if target.is_dir() else [target]
        for member in members:
            if not member.is_file() and not member.is_symlink():
                continue
            relative = relative_path(root, member.relative_to(root).as_posix())
            if member.is_symlink():
                content = os.fsencode(os.readlink(member))
            else:
                content = member.read_bytes()
            result[relative] = digest(content)
    return result


def working_files(root, spec):
    """Hash Git-visible files and explicitly managed ignored predecessors."""
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        capture_output=True, check=False,
    )
    if listed.returncode:
        raise GuardError(listed.stderr.decode(errors="replace").strip() or "git ls-files failed")
    names = {os.fsdecode(item) for item in listed.stdout.split(b"\0") if item}
    outputs = output_scopes(spec)
    extra_scopes = set()
    for scope in outputs:
        for managed in ("state", "artifacts"):
            if overlaps(scope, managed):
                extra_scopes.add(managed if covers(scope, managed) else scope)
    extra_scopes.update(item["path"] for item in spec["inputs"]
                        if any(overlaps(item["path"], scope) for scope in outputs))
    extra_scopes.update(spec["deliverables"])
    extra_scopes.update(path for path in spec["snapshot_paths"]
                        if any(overlaps(path, scope) for scope in outputs)
                        and ((root / path).is_file() or (root / path).is_symlink()))
    for scope in extra_scopes:
        target = root / relative_path(root, scope)
        if target.is_file() or target.is_symlink():
            names.add(scope)
        elif target.is_dir():
            names.update(member.relative_to(root).as_posix() for member in target.rglob("*")
                         if member.is_file() or member.is_symlink())
    result = {}
    for name in sorted(names):
        path = root / name
        if path.is_symlink():
            result[name] = digest(os.fsencode(os.readlink(path)))
        elif path.is_file():
            result[name] = file_hash(path)
    return result


def changed_files(before, after):
    return {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}


def output_scopes(spec):
    return list(dict.fromkeys(spec["writes"] + spec["deliverables"]))


def snapshot_dir(root):
    directory = swe_dir(root) / "snapshots"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def check_snapshot(root, name, spec, *, protected_only=False):
    protected = protected_paths(root, spec)
    if not protected:
        return None
    for path in protected:
        if not any(covers(scope, path) for scope in spec["snapshot_paths"]):
            raise GuardError(f"snapshot_paths does not cover required predecessor/review target: {path}")
    spec_hash = file_hash(root / name)
    manifests = sorted(snapshot_dir(root).glob("*.json"), key=lambda path: (path.stat().st_mtime_ns, path.name), reverse=True)
    for manifest_path in manifests:
        try:
            record = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise GuardError(f"snapshot manifest unreadable: {manifest_path}: {error}") from error
        if record.get("spec_sha256") != spec_hash or record.get("workspace") != str(root):
            continue
        ref, commit = record.get("ref"), record.get("commit")
        if not isinstance(ref, str) or not isinstance(commit, str):
            raise GuardError(f"snapshot manifest incomplete: {manifest_path}")
        try:
            actual_commit = git(root, "rev-parse", "--verify", ref)
        except GuardError as error:
            raise GuardError(f"snapshot ref changed or missing: {ref}") from error
        if actual_commit != commit:
            raise GuardError(f"snapshot ref changed: {ref}")
        coverage = record.get("coverage")
        if not isinstance(coverage, dict) or not coverage:
            raise GuardError(f"snapshot coverage missing: {manifest_path}")
        selected = record.get("selected_paths")
        if not isinstance(selected, list) or any(not isinstance(path, str) for path in selected):
            raise GuardError(f"snapshot selected_paths invalid: {manifest_path}")
        checked_paths = protected if protected_only else selected
        current = selected_files(root, checked_paths)
        expected_coverage = ({path: value for path, value in coverage.items()
                              if any(covers(target, path) for target in protected)}
                             if protected_only else coverage)
        if protected_only:
            for deliverable in spec["deliverables"]:
                current.pop(deliverable, None)
                expected_coverage.pop(deliverable, None)
        if current != expected_coverage:
            raise GuardError(f"snapshot coverage changed since {ref}; take a new snapshot")
        for path, expected in expected_coverage.items():
            if digest(git_blob(root, commit, path)) != expected:
                raise GuardError(f"snapshot has no byte-identical copy of {path}")
        for path in protected:
            if not any(covers(path, item) for item in coverage):
                raise GuardError(f"snapshot contains no files under required target: {path}")
        print(f"OK snapshot {ref} covers {', '.join(protected)}")
        return record
    raise GuardError("required snapshot missing; run snapshot before amendment or review dispatch")


def check_changed_predecessors(root, record, changed):
    """A changed existing file must have its original bytes in a pinned snapshot."""
    before = record["working_before"]
    predecessors = sorted(name for name in changed if name in before)
    if not predecessors:
        return
    manifests = sorted(snapshot_dir(root).glob("*.json"), key=lambda path: (path.stat().st_mtime_ns, path.name), reverse=True)
    for manifest_path in manifests:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise GuardError(f"snapshot manifest unreadable: {manifest_path}: {error}") from error
        if not isinstance(manifest, dict):
            raise GuardError(f"snapshot manifest invalid: {manifest_path}")
        if manifest.get("spec_sha256") != record["spec_sha256"] or manifest.get("workspace") != str(root):
            continue
        ref, commit = manifest.get("ref"), manifest.get("commit")
        if not isinstance(ref, str) or not isinstance(commit, str):
            raise GuardError(f"snapshot manifest incomplete: {manifest_path}")
        try:
            actual_commit = git(root, "rev-parse", "--verify", ref)
        except GuardError as error:
            raise GuardError(f"snapshot ref changed or missing: {ref}") from error
        if actual_commit != commit:
            raise GuardError(f"snapshot ref changed or missing: {ref}")
        coverage = manifest.get("coverage", {})
        if not isinstance(coverage, dict):
            raise GuardError(f"snapshot coverage invalid: {manifest_path}")
        for name in predecessors:
            if coverage.get(name) != before[name]:
                raise GuardError(f"snapshot does not cover original bytes of changed predecessor: {name}")
            if digest(git_blob(root, commit, name)) != before[name]:
                raise GuardError(f"snapshot cannot recover changed predecessor: {name}")
        print(f"OK snapshot {ref} preserves {len(predecessors)} changed predecessor(s)")
        return
    raise GuardError(f"required snapshot missing for changed predecessor: {predecessors[0]}")


def conflict(left, right):
    if "repository-manager" in (left["role"], right["role"]):
        return "repository-manager requires exclusive dispatch"
    left_reads = [item["path"] for item in left["inputs"]]
    right_reads = [item["path"] for item in right["inputs"]]
    for written in output_scopes(left):
        for used in right_reads + output_scopes(right):
            if overlaps(written, used):
                return f"{left['task_id']} writes {written}; {right['task_id']} uses {used}"
    for written in output_scopes(right):
        for used in left_reads:
            if overlaps(written, used):
                return f"{right['task_id']} writes {written}; {left['task_id']} reads {used}"
    return None


def active_dir(root):
    directory = swe_dir(root) / "active"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def active_specs(root):
    for path in sorted(active_dir(root).glob("*.json")):
        try:
            yield path, json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise GuardError(f"active handoff is unreadable: {path}: {error}") from error


def pin(root, name):
    with dispatch_lock(root):
        path, spec = load_spec(root, name)
        if (active_dir(root) / f"{spec['task_id']}.json").exists():
            raise GuardError(f"task already active: {spec['task_id']}; finish it before re-pinning")
        for item in spec["inputs"]:
            source = root / relative_path(root, item["path"])
            if not source.is_file():
                raise GuardError(f"input missing: {item['path']}")
            if "anchor" in item and source.read_text(encoding="utf-8").count(item["anchor"]) != 1:
                raise GuardError(f"anchor must occur exactly once: {item['path']}")
            item["sha256"] = file_hash(source)
        spec["base_commit"] = git(root, "rev-parse", "HEAD")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as output:
            json.dump(spec, output, ensure_ascii=False, indent=2)
            output.write("\n")
            temp_name = output.name
        os.replace(temp_name, path)
    check_inputs(root, spec)
    print(f"PINNED {name}")


def check(root, name):
    _, spec = load_spec(root, name)
    check_inputs(root, spec)
    if spec.get("base_commit") != git(root, "rev-parse", "HEAD"):
        raise GuardError("HEAD changed since pin; inspect the new baseline and re-pin")
    for scope in spec["writes"]:
        if dirty_scope(root, spec, scope) and not spec.get("defer_commit"):
            raise GuardError(f"write scope has uncommitted changes before dispatch: {scope}; commit or isolate them")
    if spec["role"] == "quality-reviewer" and not spec.get("defer_commit"):
        for target in spec["review_targets"]:
            if dirty_scope(root, spec, target):
                raise GuardError(f"review target is uncommitted: {target}; commit the validated revision or cite a deferred company policy")
    check_snapshot(root, name, spec)
    for _, record in active_specs(root):
        other = record["spec"]
        if other["task_id"] == spec["task_id"]:
            raise GuardError(f"task already active: {spec['task_id']}")
        problem = conflict(spec, other)
        if problem:
            raise GuardError(f"parallel dispatch conflict: {problem}")
        if record.get("workspace") == str(root):
            raise GuardError(f"parallel dispatch conflict: same worktree already has active task {other['task_id']}; use a separate worktree")
    print(f"READY {spec['task_id']}")
    return spec


def begin(root, name):
    with dispatch_lock(root):
        spec = check(root, name)
        target = active_dir(root) / f"{spec['task_id']}.json"
        record = {
            "spec": spec, "spec_path": name, "spec_sha256": file_hash(root / name),
            "workspace": str(root),
            "deliverable_before": {
                path: file_hash(root / path) if (root / path).is_file() else None
                for path in spec["deliverables"]
            },
            "index_before": git(root, "diff", "--cached", "--raw", "-z"),
            "working_before": working_files(root, spec),
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, delete=False) as output:
            json.dump(record, output, ensure_ascii=False, indent=2)
            output.write("\n")
            temp_name = output.name
        os.replace(temp_name, target)
    print(f"BEGUN {spec['task_id']}; frozen inputs and scopes recorded in {target}")


def assert_active(root, name, role):
    path, spec = load_spec(root, name)
    source = active_dir(root) / f"{spec['task_id']}.json"
    if not source.is_file():
        raise GuardError(f"handoff was not begun: {spec['task_id']}")
    record = json.loads(source.read_text(encoding="utf-8"))
    if record.get("workspace") != str(root):
        raise GuardError(f"handoff belongs to another worktree: {record.get('workspace')}")
    if file_hash(path) != record["spec_sha256"]:
        raise GuardError("handoff changed after begin")
    if record["spec"] != spec or spec["role"] != role:
        raise GuardError(f"handoff role or frozen content disagrees with Agent {role}")
    if spec["role"] != "repository-manager" and git(root, "rev-parse", "HEAD") != spec["base_commit"]:
        raise GuardError("HEAD changed during active task; fail and re-dispatch from a reviewed baseline")
    check_inputs(root, spec)
    if spec["role"] == "quality-reviewer":
        check_snapshot(root, name, spec)
    print(f"ACTIVE {spec['task_id']} role={role}")


def assert_write(root, name):
    target = Path(name).resolve()
    if os.path.commonpath([str(root), str(target)]) != str(root):
        if any(record.get("workspace") == str(root) for _, record in active_specs(root)):
            raise GuardError(f"active handoff cannot Write/Edit outside its worktree: {target}")
        return
    path = target.relative_to(root).as_posix()
    for _, record in active_specs(root):
        if record.get("workspace") != str(root):
            continue
        spec = record["spec"]
        for item in spec["inputs"]:
            if overlaps(path, item["path"]) and not any(overlaps(path, scope) for scope in spec["writes"]):
                raise GuardError(f"{path} is a frozen input of {spec['task_id']}; finish or fail that task first")
        if not any(covers(scope, path) for scope in output_scopes(spec)):
            raise GuardError(f"{spec['task_id']} cannot Write/Edit outside declared output: {path}")


def check_repository_result(root, spec):
    base = spec["base_commit"]
    head = git(root, "rev-parse", "HEAD")
    action = spec.get("repository_action", "status")
    if action == "status":
        if head != base:
            raise GuardError("status-only repository task changed HEAD; declare a commit action")
        return
    if head == base:
        raise GuardError("commit action produced no new commit")
    git(root, "merge-base", "--is-ancestor", base, head)
    commits = git(root, "rev-list", "--reverse", f"{base}..{head}").splitlines()
    changed = set()
    for commit in commits:
        parents = git(root, "rev-list", "--parents", "-n", "1", commit).split()
        if len(parents) != 2:
            raise GuardError(f"commit action includes a merge or root commit: {commit}")
        paths = {name for name in git(root, "diff-tree", "--no-commit-id", "--name-only", "--no-renames", "-r", "-z", commit).split("\0") if name}
        for name in paths:
            if not any(covers(scope, name) for scope in spec["commit_paths"]):
                raise GuardError(f"commit contains path outside commit_paths: {name}")
        changed.update(paths)
        subject = git(root, "log", "-1", "--format=%s", commit)
        if not spec.get("commit_policy_path") and (
            len(subject) > 72 or not re.fullmatch(r"(?:feat|fix|refactor|test|docs|chore)(?:\([^)]+\))?: \S(?:.*\S)?", subject)
            or subject.endswith(".")
        ):
            raise GuardError(f"commit subject does not match the default format: {subject}")
    if not changed:
        raise GuardError("commit action has no changed paths")
    for scope in spec["commit_paths"]:
        if not any(covers(scope, name) for name in changed):
            raise GuardError(f"commit_paths contains no committed change: {scope}")
        if git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", scope):
            raise GuardError(f"committed path remains dirty: {scope}")
    print(f"OK commit evidence {base[:12]}..{head[:12]} paths={len(changed)} commits={len(commits)}")


def finish(root, task_id, failed=False):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", task_id):
        raise GuardError("invalid task_id")
    with dispatch_lock(root):
        source = active_dir(root) / f"{task_id}.json"
        if not source.is_file():
            raise GuardError(f"no active task: {task_id}")
        record = json.loads(source.read_text(encoding="utf-8"))
        spec = record["spec"]
        if not failed:
            if record.get("workspace") != str(root):
                raise GuardError(f"task belongs to another worktree: {record.get('workspace')}")
            spec_path = root / relative_path(root, record["spec_path"])
            if not spec_path.is_file() or file_hash(spec_path) != record["spec_sha256"]:
                raise GuardError("handoff changed during execution; finish as failed and re-dispatch")
            if spec["role"] == "repository-manager":
                check_repository_result(root, spec)
            elif git(root, "rev-parse", "HEAD") != spec["base_commit"]:
                raise GuardError("HEAD changed during active task; finish as failed and re-dispatch")
            if (spec["role"] != "repository-manager" or spec.get("repository_action", "status") == "status") and (
                git(root, "diff", "--cached", "--raw", "-z") != record["index_before"]
            ):
                raise GuardError("Git index changed during non-commit task; finish as failed or restore staged state")
            check_inputs(root, spec, exclude_writes=True)
            if spec["role"] == "quality-reviewer":
                check_snapshot(root, record["spec_path"], spec, protected_only=True)
            after = working_files(root, spec)
            changed = changed_files(record["working_before"], after)
            for name in sorted(changed):
                if not any(covers(scope, name) for scope in output_scopes(spec)):
                    raise GuardError(f"actual change outside declared output: {name}")
            check_changed_predecessors(root, record, changed)
            record["changed_paths"] = sorted(changed)
            for name in spec["deliverables"]:
                target_file = root / name
                if not target_file.is_file() or not target_file.stat().st_size:
                    raise GuardError(f"deliverable missing or empty: {name}")
                if record["deliverable_before"].get(name) == file_hash(target_file):
                    raise GuardError(f"deliverable unchanged from dispatch: {name}")
        history = source.parent.parent / "history"
        history.mkdir(exist_ok=True)
        target = history / f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{task_id}-{uuid4().hex[:8]}.json"
        record["result"] = "FAILED" if failed else "RETURNED_FOR_GATE"
        before = record.pop("working_before", {})
        record["working_before_files"] = len(before)
        record["working_before_sha256"] = digest(json.dumps(before, sort_keys=True, ensure_ascii=True).encode("utf-8"))
        record.pop("index_before", None)
        if spec["role"] == "repository-manager":
            record["result_commit"] = git(root, "rev-parse", "HEAD")
            record["repository_status"] = git(root, "status", "--short")
        target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        source.unlink()
    print(f"{record['result']} {task_id}; record: {target}")


def snapshot(root, name):
    _, spec = load_spec(root, name)
    check_inputs(root, spec)
    if spec.get("base_commit") != git(root, "rev-parse", "HEAD"):
        raise GuardError("HEAD changed since pin; inspect the new baseline and re-pin")
    if not spec["snapshot_paths"]:
        raise GuardError("snapshot_paths is empty; select code and essential State/Artifacts explicitly")
    paths = list(dict.fromkeys(spec["snapshot_paths"] + [relative_path(root, name)]))
    coverage = selected_files(root, paths)
    if not coverage:
        raise GuardError("snapshot_paths contains no recoverable files")
    head = git(root, "rev-parse", "HEAD")
    git_dir = common_dir(root)
    with tempfile.TemporaryDirectory(prefix="swe-index-", dir=git_dir) as temporary:
        environment = os.environ.copy()
        environment["GIT_INDEX_FILE"] = str(Path(temporary) / "index")
        git(root, "read-tree", "HEAD", env=environment)
        git(root, "add", "-f", "-A", "--", *paths, env=environment)
        tree = git(root, "write-tree", env=environment)
        message = f"SWE snapshot {spec['task_id']}\n\nCaptured paths: {json.dumps(paths, ensure_ascii=False)}\n"
        identity = environment.copy()
        identity.update({
            "GIT_AUTHOR_NAME": "SWE Snapshot",
            "GIT_AUTHOR_EMAIL": "swe-snapshot@local.invalid",
            "GIT_COMMITTER_NAME": "SWE Snapshot",
            "GIT_COMMITTER_EMAIL": "swe-snapshot@local.invalid",
        })
        commit = git(root, "commit-tree", tree, "-p", head, env=identity, input_text=message)
    for path, expected in coverage.items():
        if digest(git_blob(root, commit, path)) != expected:
            raise GuardError(f"snapshot cannot recover byte-identical content for {path}")
    label = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{spec['task_id']}-{uuid4().hex[:8]}"
    ref = f"refs/swe/snapshots/{label}"
    git(root, "update-ref", ref, commit, "0" * len(head))
    manifest = {
        "task_id": spec["task_id"], "workspace": str(root),
        "spec_sha256": file_hash(root / name), "ref": ref, "commit": commit,
        "selected_paths": paths, "coverage": coverage,
    }
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=snapshot_dir(root), delete=False) as output:
        json.dump(manifest, output, ensure_ascii=False, indent=2)
        output.write("\n")
        temp_name = output.name
    os.replace(temp_name, snapshot_dir(root) / f"{label}.json")
    print(f"SNAPSHOT {ref} {commit}")
    print("Local Git ref created; branch, worktree and ordinary index were not changed.")
    print("Selected working-tree paths plus the tracked HEAD baseline were captured; inspect before sharing refs.")


def status(root):
    with dispatch_lock(root):
        active = list(active_specs(root))
    print("ACTIVE TASKS:")
    for _, record in active:
        print(f"  {record['spec']['task_id']} ({record['workspace']}: {record['spec_path']})")
    if not active:
        print("  none")
    print("RECENT SNAPSHOTS:")
    refs = git(root, "for-each-ref", "--sort=-creatordate", "--format=%(refname) %(objectname)", "refs/swe/snapshots")
    print("\n".join(f"  {line}" for line in refs.splitlines()[:10]) if refs else "  none")
    print("REPOSITORY:")
    print(f"  WORKTREE {root}")
    print(f"  BRANCH {git(root, 'branch', '--show-current') or '(detached)'}")
    print(f"  HEAD {git(root, 'rev-parse', '--short', 'HEAD')}")
    dirty = git(root, "status", "--short")
    print("\n".join(f"  {line}" for line in dirty.splitlines()) if dirty else "  clean")


def capture_text(root, task_id, kind, destination=None):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", task_id):
        raise GuardError("invalid task_id")
    content = sys.stdin.buffer.read()
    if not content.strip():
        raise GuardError(f"{kind} content is empty")
    try:
        content.decode("utf-8")
    except UnicodeError as error:
        raise GuardError(f"{kind} content must be UTF-8") from error
    default = f"state/handoffs/{task_id}.{'request' if kind == 'chat' else 'result'}.md"
    name = relative_path(root, destination or default)
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if kind == "return":
        source = active_dir(root) / f"{task_id}.json"
        if not source.is_file():
            raise GuardError(f"no active task: {task_id}")
        record = json.loads(source.read_text(encoding="utf-8"))
        if name not in record["spec"]["deliverables"]:
            raise GuardError(f"return file is not a declared deliverable: {name}")
    try:
        with target.open("xb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
    except FileExistsError as error:
        raise GuardError(f"refusing to overwrite {name}; use a new task ID") from error
    print(f"CAPTURED {name} sha256={digest(content)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("pin", "check", "begin", "snapshot"):
        commands.add_parser(command).add_argument("handoff", help="project-relative JSON handoff path")
    active_parser = commands.add_parser("assert-active")
    active_parser.add_argument("handoff")
    active_parser.add_argument("role")
    commands.add_parser("assert-write").add_argument("path")
    finish_parser = commands.add_parser("finish")
    finish_parser.add_argument("task_id")
    finish_parser.add_argument("--failed", action="store_true", help="record a failed/interrupted task without claiming a deliverable")
    commands.add_parser("capture-chat").add_argument("task_id")
    return_parser = commands.add_parser("capture-return")
    return_parser.add_argument("task_id")
    return_parser.add_argument("path", nargs="?", help="declared deliverable path; defaults to state/handoffs/<task>.result.md")
    commands.add_parser("status")
    args = parser.parse_args()
    try:
        root = project_root()
        if args.command == "pin":
            pin(root, args.handoff)
        elif args.command == "check":
            check(root, args.handoff)
        elif args.command == "begin":
            begin(root, args.handoff)
        elif args.command == "finish":
            finish(root, args.task_id, args.failed)
        elif args.command == "assert-active":
            assert_active(root, args.handoff, args.role)
        elif args.command == "assert-write":
            assert_write(root, args.path)
        elif args.command == "snapshot":
            snapshot(root, args.handoff)
        elif args.command == "capture-chat":
            capture_text(root, args.task_id, "chat")
        elif args.command == "capture-return":
            capture_text(root, args.task_id, "return", args.path)
        else:
            status(root)
    except GuardError as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
