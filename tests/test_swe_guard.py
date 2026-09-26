"""Regression checks for handoff drift and recoverable Git snapshots."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "swe_guard.py"
HOOK = Path(__file__).resolve().parents[1] / ".claude/hooks/check-agent-handoff.py"
WRITE_HOOK = Path(__file__).resolve().parents[1] / ".claude/hooks/check-frozen-input.py"


class GuardIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.root / "CLAUDE.md").write_text("# Test project\n", encoding="utf-8")
        (self.root / ".gitignore").write_text("state/\nartifacts/\n", encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src/code.txt").write_text("contract v1\n", encoding="utf-8")
        self.git("add", "CLAUDE.md", ".gitignore", "src/code.txt")
        self.git("commit", "-qm", "baseline")
        (self.root / "state/handoffs").mkdir(parents=True)
        (self.root / "state/decision.md").write_text("# DEC-1\naccepted\n", encoding="utf-8")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], text=True, capture_output=True, check=True).stdout.strip()

    def guard(self, *args, expected=0, input_text=None, cwd=None):
        result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd or self.root,
                                input=input_text, text=True, capture_output=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def handoff(self, task_id="WP-1", *, inputs=None, writes=None, deliverables=None,
                snapshot_paths=None, role="implementation-engineer", review_targets=None, root=None):
        target_root = root or self.root
        name = f"state/handoffs/{task_id}.json"
        data = {
            "task_id": task_id,
            "role": role,
            "inputs": inputs if inputs is not None else [{"path": "state/decision.md", "anchor": "# DEC-1"}],
            "writes": writes if writes is not None else ["src"],
            "deliverables": deliverables if deliverables is not None else ["artifacts/report.md"],
            "snapshot_paths": snapshot_paths if snapshot_paths is not None else ["src", "state/decision.md"],
            "review_targets": review_targets if review_targets is not None else [],
        }
        (target_root / "state/handoffs").mkdir(parents=True, exist_ok=True)
        (target_root / name).write_text(json.dumps(data), encoding="utf-8")
        return name

    def test_drift_and_false_claims_block_dispatch(self):
        handoff = self.handoff()
        self.guard("pin", handoff)
        self.guard("check", handoff)
        (self.root / "state/decision.md").write_text("# DEC-1\nchanged\n", encoding="utf-8")
        self.assertIn("input changed", self.guard("begin", handoff, expected=2))
        self.assertIn("none", self.guard("status"))

    def test_parallel_reader_writer_conflict_and_frozen_handoff(self):
        first = self.handoff()
        self.guard("pin", first)
        self.guard("begin", first)
        self.guard("assert-active", first, "implementation-engineer")
        self.assertIn("frozen input", self.guard("assert-write", str(self.root / "state/decision.md"), expected=2))
        self.guard("assert-write", str(self.root / "src/code.txt"))
        self.assertIn("role or frozen content", self.guard("assert-active", first, "quality-reviewer", expected=2))
        second = self.handoff("WP-2", inputs=[{"path": "src/code.txt"}], writes=["tests"])
        self.guard("pin", second)
        self.assertIn("parallel dispatch conflict", self.guard("begin", second, expected=2))
        self.guard("finish", "WP-1", "--failed")
        self.guard("begin", second)
        self.assertIn("frozen input", self.guard("assert-write", str(self.root / "src/code.txt"), expected=2))
        (self.root / "src/code.txt").write_text("changed while reader active\n", encoding="utf-8")
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/report.md").write_text("report\n", encoding="utf-8")
        self.assertIn("input changed", self.guard("finish", "WP-2", expected=2))
        self.guard("finish", "WP-2", "--failed")

    def test_snapshot_recovers_ignored_and_uncommitted_files_without_touching_index(self):
        handoff = self.handoff()
        self.guard("pin", handoff)
        (self.root / "src/code.txt").write_text("uncommitted reviewed revision\n", encoding="utf-8")
        before_head = self.git("rev-parse", "HEAD")
        before_status = self.git("status", "--short")
        output = self.guard("snapshot", handoff)
        ref = next(line.split()[1] for line in output.splitlines() if line.startswith("SNAPSHOT "))
        self.assertEqual(before_head, self.git("rev-parse", "HEAD"))
        self.assertEqual(before_status, self.git("status", "--short"))
        self.assertEqual("uncommitted reviewed revision", self.git("show", f"{ref}:src/code.txt"))
        self.assertIn("accepted", self.git("show", f"{ref}:state/decision.md"))
        self.assertIn("WP-1", self.git("show", f"{ref}:{handoff}"))

    def test_agent_hook_blocks_unpinned_or_missing_handoff(self):
        (self.root / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts/swe_guard.py")
        handoff = self.handoff()
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        payload = {
            "tool_name": "Agent", "cwd": str(self.root),
            "tool_input": {"subagent_type": "implementation-engineer", "prompt": f"Do task\nHANDOFF: {handoff}\n"},
        }
        def call_hook():
            return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), cwd=self.root,
                                  text=True, capture_output=True)
        self.assertEqual(0, call_hook().returncode)
        payload["tool_input"]["prompt"] = "Do task without handoff"
        self.assertEqual(2, call_hook().returncode)
        payload["tool_input"]["prompt"] = f"HANDOFF: {handoff}\n"
        (self.root / "state/decision.md").write_text("# DEC-1\nchanged\n", encoding="utf-8")
        self.assertEqual(2, call_hook().returncode)

    def test_write_hook_blocks_frozen_input_and_active_repin(self):
        (self.root / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts/swe_guard.py")
        handoff = self.handoff()
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        self.assertIn("already active", self.guard("pin", handoff, expected=2))
        payload = {
            "tool_name": "Edit", "cwd": str(self.root),
            "tool_input": {"file_path": str(self.root / "state/decision.md")},
        }
        blocked = subprocess.run([sys.executable, str(WRITE_HOOK)], input=json.dumps(payload),
                                 cwd=self.root, text=True, capture_output=True)
        self.assertEqual(2, blocked.returncode)
        self.assertIn("frozen input", blocked.stderr)
        payload["tool_input"]["file_path"] = str(self.root / "src/code.txt")
        allowed = subprocess.run([sys.executable, str(WRITE_HOOK)], input=json.dumps(payload),
                                 cwd=self.root, text=True, capture_output=True)
        self.assertEqual(0, allowed.returncode)
        payload["cwd"] = str(self.root / "src")
        payload["tool_input"]["file_path"] = "../state/decision.md"
        relative = subprocess.run([sys.executable, str(WRITE_HOOK)], input=json.dumps(payload),
                                  cwd=self.root, text=True, capture_output=True)
        self.assertEqual(2, relative.returncode)
        self.assertIn("frozen input", relative.stderr)
        payload["tool_input"]["file_path"] = str(self.root.parent / "outside.txt")
        outside = subprocess.run([sys.executable, str(WRITE_HOOK)], input=json.dumps(payload),
                                 cwd=self.root, text=True, capture_output=True)
        self.assertEqual(2, outside.returncode)
        self.assertIn("outside its worktree", outside.stderr)

    def test_chat_request_is_captured_verbatim_and_can_be_pinned(self):
        original = "请修复解析器。\n保留 --help 的退出码 0。\n"
        output = self.guard("capture-chat", "CHAT-1", input_text=original)
        self.assertIn("CAPTURED state/handoffs/CHAT-1.request.md", output)
        self.assertEqual(original, (self.root / "state/handoffs/CHAT-1.request.md").read_text(encoding="utf-8"))
        self.assertIn("refusing to overwrite", self.guard("capture-chat", "CHAT-1", expected=2, input_text="changed"))
        handoff = self.handoff("CHAT-1", inputs=[{"path": "state/handoffs/CHAT-1.request.md"}],
                               writes=["artifacts"], deliverables=["artifacts/intake.md"])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/intake.md").write_text("# Intake\n", encoding="utf-8")
        self.guard("finish", "CHAT-1")

    def test_empty_deliverable_and_missing_predecessor_snapshot_block(self):
        empty = self.handoff("EMPTY", deliverables=[])
        self.assertIn("at least one persistent output", self.guard("pin", empty, expected=2))
        handoff = self.handoff("AMEND", inputs=[{"path": "src/code.txt"}],
                               writes=["src"], deliverables=["src/code.txt"], snapshot_paths=["src"])
        self.guard("pin", handoff)
        self.assertIn("required snapshot missing", self.guard("begin", handoff, expected=2))
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        (self.root / "src/code.txt").write_text("contract v2\n", encoding="utf-8")
        self.guard("finish", "AMEND")

    def test_review_requires_target_coverage_real_ref_and_persisted_report(self):
        handoff = self.handoff("REVIEW", role="quality-reviewer", inputs=[{"path": "src/code.txt"}],
                               writes=[], deliverables=["artifacts/review.md"],
                               snapshot_paths=["state/decision.md"], review_targets=["src/code.txt"])
        self.guard("pin", handoff)
        self.assertIn("does not cover", self.guard("begin", handoff, expected=2))
        spec = json.loads((self.root / handoff).read_text(encoding="utf-8"))
        spec["snapshot_paths"] = ["src/code.txt"]
        (self.root / handoff).write_text(json.dumps(spec), encoding="utf-8")
        self.guard("pin", handoff)
        output = self.guard("snapshot", handoff)
        ref = next(line.split()[1] for line in output.splitlines() if line.startswith("SNAPSHOT "))
        self.git("update-ref", "-d", ref)
        self.assertIn("snapshot ref changed", self.guard("begin", handoff, expected=2))
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        self.assertIn("deliverable missing or empty", self.guard("finish", "REVIEW", expected=2))
        report = "Producer: agent:quality-reviewer\n\n# Review\nPASS\n"
        self.guard("capture-return", "REVIEW", "artifacts/review.md", input_text=report)
        self.assertEqual(report, (self.root / "artifacts/review.md").read_text(encoding="utf-8"))
        self.guard("finish", "REVIEW")

    def test_review_report_can_be_created_inside_a_broad_snapshot_directory(self):
        handoff = self.handoff("REVIEW-STATE", role="quality-reviewer",
                               inputs=[{"path": "src/code.txt"}], writes=[],
                               deliverables=["state/handoffs/REVIEW-STATE.result.md"],
                               snapshot_paths=["src", "state"], review_targets=["src"])
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        self.guard("capture-return", "REVIEW-STATE", input_text="Reviewed code revision: PASS\n")
        self.guard("finish", "REVIEW-STATE")

    def test_review_report_inside_reviewed_directory_does_not_change_review_target(self):
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/contract.md").write_text("Producer: agent:solution-architect\n", encoding="utf-8")
        handoff = self.handoff("REVIEW-ART", role="quality-reviewer", writes=[],
                               inputs=[{"path": "artifacts/contract.md"}],
                               deliverables=["artifacts/review.md"],
                               snapshot_paths=["artifacts"], review_targets=["artifacts"])
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        self.guard("capture-return", "REVIEW-ART", "artifacts/review.md", input_text="PASS\n")
        self.guard("finish", "REVIEW-ART")

    def test_default_review_requires_committed_code_baseline(self):
        (self.root / "src/code.txt").write_text("uncommitted revision\n", encoding="utf-8")
        handoff = self.handoff("REVIEW-DIRTY", role="quality-reviewer",
                               inputs=[{"path": "src/code.txt"}], writes=[],
                               deliverables=["artifacts/review-dirty.md"],
                               snapshot_paths=["src"], review_targets=["src"])
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.assertIn("review target is uncommitted", self.guard("begin", handoff, expected=2))
        self.git("add", "src/code.txt")
        self.git("commit", "-qm", "validated code")
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        self.guard("finish", "REVIEW-DIRTY", "--failed")

    def test_linked_worktrees_share_active_registry_and_conflict_checks(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked))
        first = self.handoff("MAIN", writes=["src"], deliverables=["artifacts/main.md"])
        self.guard("pin", first)
        self.guard("begin", first)
        other = self.handoff("LINKED", inputs=[{"path": "src/code.txt"}], writes=["tests"],
                             deliverables=["artifacts/linked.md"], root=linked)
        self.guard("pin", other, cwd=linked)
        self.assertIn("MAIN", self.guard("status", cwd=linked))
        self.assertIn("parallel dispatch conflict", self.guard("begin", other, cwd=linked, expected=2))
        self.guard("finish", "MAIN", "--failed")
        self.guard("begin", other, cwd=linked)
        self.guard("finish", "LINKED", "--failed", cwd=linked)

    def test_own_untracked_handoff_does_not_make_tracked_state_scope_dirty(self):
        (self.root / ".gitignore").write_text("\n", encoding="utf-8")
        self.git("add", ".gitignore", "state/decision.md")
        self.git("commit", "-qm", "track state")
        handoff = self.handoff("STATE", inputs=[{"path": "state/decision.md"}],
                               writes=["state"], deliverables=["state/new.md"],
                               snapshot_paths=["state"])
        self.guard("pin", handoff)
        self.git("add", handoff)
        self.git("commit", "-qm", "track handoff")
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        (self.root / "state/new.md").write_text("new output\n", encoding="utf-8")
        self.guard("finish", "STATE")

    def test_stale_deliverable_and_dirty_write_scope_cannot_claim_success(self):
        handoff = self.handoff("STALE", inputs=[{"path": "state/decision.md"}],
                               writes=["src"], deliverables=["artifacts/report.md"])
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/report.md").write_text("old report\n", encoding="utf-8")
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        self.assertIn("unchanged from dispatch", self.guard("finish", "STALE", expected=2))
        self.guard("finish", "STALE", "--failed")
        (self.root / "src/code.txt").write_text("dirty\n", encoding="utf-8")
        fresh = self.handoff("DIRTY", deliverables=["artifacts/new.md"])
        self.guard("pin", fresh)
        self.assertIn("uncommitted changes", self.guard("begin", fresh, expected=2))

    def test_company_commit_timing_override_requires_pinned_policy_and_snapshot(self):
        policy = self.root / "input/standards/git.md"
        policy.parent.mkdir(parents=True)
        policy.write_text("# Git policy\n## Commit timing\nCommit after batch review.\n", encoding="utf-8")
        self.git("add", "input/standards/git.md")
        self.git("commit", "-qm", "add company policy")
        (self.root / "src/code.txt").write_text("uncommitted batch work\n", encoding="utf-8")
        handoff = self.handoff("POLICY", inputs=[
            {"path": "state/decision.md"},
            {"path": "input/standards/git.md", "anchor": "## Commit timing"},
        ], writes=["src"], deliverables=["src/code.txt"], snapshot_paths=["src"])
        spec = json.loads((self.root / handoff).read_text(encoding="utf-8"))
        spec["defer_commit"] = True
        spec["commit_policy_path"] = "input/standards/git.md"
        (self.root / handoff).write_text(json.dumps(spec), encoding="utf-8")
        self.guard("pin", handoff)
        self.assertIn("required snapshot missing", self.guard("begin", handoff, expected=2))
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        (self.root / "src/code.txt").write_text("next batch revision\n", encoding="utf-8")
        self.guard("finish", "POLICY")

    def test_repository_manager_is_exclusive(self):
        first = self.handoff("WORK")
        self.guard("pin", first)
        self.guard("begin", first)
        manager = self.handoff("GIT", role="repository-manager", writes=[],
                               deliverables=["state/handoffs/GIT.result.md"])
        self.guard("pin", manager)
        self.assertIn("requires exclusive dispatch", self.guard("begin", manager, expected=2))
        self.guard("finish", "WORK", "--failed")
        self.guard("begin", manager)
        self.assertIn("outside declared output", self.guard("assert-write", str(self.root / "src/code.txt"), expected=2))
        self.guard("assert-write", str(self.root / "state/handoffs/GIT.result.md"))
        self.guard("capture-return", "GIT", input_text="HEAD baseline reviewed\n")
        self.guard("finish", "GIT")

    def test_actual_predecessor_change_needs_original_snapshot_even_when_omitted(self):
        handoff = self.handoff("OMITTED", writes=["src"], deliverables=["src/new.txt"],
                               snapshot_paths=[])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "src/code.txt").write_text("unexpected amendment\n", encoding="utf-8")
        (self.root / "src/new.txt").write_text("new file\n", encoding="utf-8")
        self.assertIn("required snapshot missing for changed predecessor: src/code.txt",
                      self.guard("finish", "OMITTED", expected=2))
        self.guard("finish", "OMITTED", "--failed")
        (self.root / "src/code.txt").write_text("contract v1\n", encoding="utf-8")
        (self.root / "src/new.txt").unlink()
        handoff = self.handoff("COVERED", writes=["src"], deliverables=["src/new.txt"],
                               snapshot_paths=["src"])
        self.guard("pin", handoff)
        self.guard("snapshot", handoff)
        self.guard("begin", handoff)
        (self.root / "src/code.txt").write_text("safe amendment\n", encoding="utf-8")
        (self.root / "src/new.txt").write_text("new file\n", encoding="utf-8")
        self.assertIn("RETURNED_FOR_GATE", self.guard("finish", "COVERED"))

    def test_snapshot_taken_after_amendment_cannot_claim_original_bytes(self):
        handoff = self.handoff("LATE", writes=["src"], deliverables=["src/new.txt"],
                               snapshot_paths=["src"])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "src/code.txt").write_text("already changed\n", encoding="utf-8")
        (self.root / "src/new.txt").write_text("new output\n", encoding="utf-8")
        self.guard("snapshot", handoff)
        self.assertIn("snapshot does not cover original bytes of changed predecessor: src/code.txt",
                      self.guard("finish", "LATE", expected=2))
        self.guard("finish", "LATE", "--failed")

    def test_ignored_predecessor_inside_write_scope_needs_snapshot(self):
        (self.root / "artifacts").mkdir()
        (self.root / "artifacts/old.md").write_text("untracked predecessor\n", encoding="utf-8")
        handoff = self.handoff("IGNORED", writes=["artifacts"],
                               deliverables=["artifacts/new.md"], snapshot_paths=[])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "artifacts/old.md").write_text("changed predecessor\n", encoding="utf-8")
        (self.root / "artifacts/new.md").write_text("new output\n", encoding="utf-8")
        self.assertIn("required snapshot missing for changed predecessor: artifacts/old.md",
                      self.guard("finish", "IGNORED", expected=2))
        self.guard("finish", "IGNORED", "--failed")

    def test_ignored_build_cache_inside_source_scope_does_not_need_snapshot(self):
        (self.root / ".gitignore").write_text("state/\nartifacts/\n__pycache__/\n", encoding="utf-8")
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "ignore generated cache")
        cache = self.root / "src/__pycache__/module.pyc"
        cache.parent.mkdir()
        cache.write_bytes(b"before")
        handoff = self.handoff("CACHE", writes=["src"], deliverables=["src/new.txt"],
                               snapshot_paths=[])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        cache.write_bytes(b"after")
        (self.root / "src/new.txt").write_text("new source\n", encoding="utf-8")
        self.guard("finish", "CACHE")

    def test_parallel_writes_need_separate_worktrees_and_actual_scope_is_checked(self):
        first = self.handoff("A", writes=["src/a.txt"], deliverables=["src/a.txt"], snapshot_paths=[])
        second = self.handoff("B", writes=["src/b.txt"], deliverables=["src/b.txt"], snapshot_paths=[])
        for handoff in (first, second):
            self.guard("pin", handoff)
        self.guard("begin", first)
        self.assertIn("same worktree already has active task A", self.guard("begin", second, expected=2))
        self.assertIn("outside declared output", self.guard("assert-write", str(self.root / "src/b.txt"), expected=2))
        (self.root / "src/b.txt").write_text("shell bypass\n", encoding="utf-8")
        (self.root / "src/a.txt").write_text("expected output\n", encoding="utf-8")
        self.assertIn("actual change outside declared output: src/b.txt", self.guard("finish", "A", expected=2))
        self.guard("finish", "A", "--failed")

    def test_disjoint_worktrees_can_finish_parallel_tasks(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked))
        (linked / "state/handoffs").mkdir(parents=True)
        (linked / "state/decision.md").write_text("# DEC-1\naccepted\n", encoding="utf-8")
        first = self.handoff("MAIN-W", writes=["src/a.txt"], deliverables=["src/a.txt"], snapshot_paths=[])
        second = self.handoff("LINK-W", writes=["src/b.txt"], deliverables=["src/b.txt"],
                              snapshot_paths=[], root=linked)
        self.guard("pin", first)
        self.guard("pin", second, cwd=linked)
        self.guard("begin", first)
        self.guard("begin", second, cwd=linked)
        (self.root / "src/a.txt").write_text("main\n", encoding="utf-8")
        (linked / "src/b.txt").write_text("linked\n", encoding="utf-8")
        self.guard("finish", "MAIN-W")
        self.guard("finish", "LINK-W", cwd=linked)

    def test_head_change_during_specialist_task_blocks_success(self):
        handoff = self.handoff("HEAD", writes=["src/new.txt"], deliverables=["src/new.txt"],
                               snapshot_paths=[])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "unrelated.txt").write_text("other revision\n", encoding="utf-8")
        self.git("add", "unrelated.txt")
        self.git("commit", "-qm", "other revision")
        (self.root / "src/new.txt").write_text("output\n", encoding="utf-8")
        self.assertIn("HEAD changed during active task", self.guard("finish", "HEAD", expected=2))
        self.guard("finish", "HEAD", "--failed")

    def test_noncommit_task_cannot_silently_change_git_index(self):
        handoff = self.handoff("INDEX", writes=["src/new.txt"], deliverables=["src/new.txt"],
                               snapshot_paths=[])
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        (self.root / "src/new.txt").write_text("new source\n", encoding="utf-8")
        self.git("add", "src/new.txt")
        self.assertIn("Git index changed during non-commit task", self.guard("finish", "INDEX", expected=2))
        self.guard("finish", "INDEX", "--failed")

    def test_commit_action_requires_physical_scoped_commit_and_default_subject(self):
        (self.root / "src/code.txt").write_text("validated change\n", encoding="utf-8")
        handoff = self.handoff("COMMIT", role="repository-manager", writes=[],
                               deliverables=["state/handoffs/COMMIT.result.md"], snapshot_paths=[])
        path = self.root / handoff
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec.update({"repository_action": "commit", "commit_paths": ["src/code.txt"]})
        path.write_text(json.dumps(spec), encoding="utf-8")
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        self.guard("capture-return", "COMMIT", input_text="commit evidence\n")
        self.assertIn("produced no new commit", self.guard("finish", "COMMIT", expected=2))
        self.git("add", "src/code.txt")
        self.git("commit", "-qm", "unstructured commit")
        self.assertIn("default format", self.guard("finish", "COMMIT", expected=2))
        self.git("commit", "--amend", "-qm", "fix(core): preserve validated change")
        self.assertIn("OK commit evidence", self.guard("finish", "COMMIT"))

    def test_commit_action_rejects_unrelated_committed_path(self):
        (self.root / "src/code.txt").write_text("validated change\n", encoding="utf-8")
        handoff = self.handoff("WRONG", role="repository-manager", writes=[],
                               deliverables=["state/handoffs/WRONG.result.md"], snapshot_paths=[])
        path = self.root / handoff
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec.update({"repository_action": "commit", "commit_paths": ["src/code.txt"]})
        path.write_text(json.dumps(spec), encoding="utf-8")
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        self.guard("capture-return", "WRONG", input_text="commit evidence\n")
        (self.root / "unrelated.txt").write_text("unrelated\n", encoding="utf-8")
        self.git("add", "src/code.txt", "unrelated.txt")
        self.git("commit", "-qm", "fix(core): commit two files")
        self.assertIn("outside commit_paths: unrelated.txt", self.guard("finish", "WRONG", expected=2))
        self.guard("finish", "WRONG", "--failed")

    def test_cited_company_commit_policy_overrides_default_subject(self):
        policy = self.root / "input/standards/git.md"
        policy.parent.mkdir(parents=True)
        policy.write_text("# Git policy\n## Message\nUse TASK-123 as the subject.\n", encoding="utf-8")
        self.git("add", "input/standards/git.md")
        self.git("commit", "-qm", "add policy")
        (self.root / "src/code.txt").write_text("validated change\n", encoding="utf-8")
        handoff = self.handoff("CUSTOM", role="repository-manager", writes=[], snapshot_paths=[],
                               inputs=[{"path": "input/standards/git.md", "anchor": "## Message"}],
                               deliverables=["state/handoffs/CUSTOM.result.md"])
        path = self.root / handoff
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec.update({"repository_action": "commit", "commit_paths": ["src/code.txt"],
                     "commit_policy_path": "input/standards/git.md"})
        path.write_text(json.dumps(spec), encoding="utf-8")
        self.guard("pin", handoff)
        self.guard("begin", handoff)
        self.git("add", "src/code.txt")
        self.git("commit", "-qm", "TASK-123")
        self.guard("capture-return", "CUSTOM", input_text="commit evidence\n")
        self.guard("finish", "CUSTOM")

    def test_simultaneous_conflicting_begins_register_only_one_task(self):
        handoffs = [self.handoff(f"RACE-{number}", deliverables=[f"artifacts/{number}.md"])
                    for number in range(4)]
        for handoff in handoffs:
            self.guard("pin", handoff)
        processes = [subprocess.Popen([sys.executable, str(SCRIPT), "begin", handoff], cwd=self.root,
                                      text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                     for handoff in handoffs]
        results = [process.communicate()[0:2] + (process.returncode,) for process in processes]
        self.assertEqual(1, sum(returncode == 0 for _, _, returncode in results), results)
        self.assertEqual(3, sum("parallel dispatch conflict" in stderr for _, stderr, _ in results), results)


if __name__ == "__main__":
    unittest.main()
