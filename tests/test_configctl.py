from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional


REPO = Path(__file__).resolve().parents[1]
CONTROLLER = REPO / "install" / "scripts" / "configctl.py"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ConfigControllerTests(unittest.TestCase):
    def run_ctl(
        self,
        *args: str,
        controller: Path = CONTROLLER,
        expected: Optional[int] = 0,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(controller), *args],
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        if expected is not None and result.returncode != expected:
            self.fail(
                f"expected {expected}, got {result.returncode}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def test_package_validates(self) -> None:
        result = self.run_ctl("verify-package")
        self.assertIn("Package OK", result.stdout)

    def test_three_runtime_lifecycle_and_recovery(self) -> None:
        rules = {
            "codex": Path("AGENTS.md"),
            "cursor": Path(".cursor/rules/agent-config-kit.mdc"),
            "claude-code": Path("CLAUDE.md"),
        }
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for runtime, rule in rules.items():
                project = base / runtime
                project.mkdir()
                common = (
                    "install",
                    "--runtime",
                    runtime,
                    "--profile",
                    "daily-work",
                    "--target",
                    str(project),
                ) + (("--without-hooks",) if os.name == "nt" else ())
                preview = self.run_ctl(*common)
                self.assertIn("Mode: dry-run", preview.stdout)
                self.assertFalse((project / rule).exists())

                self.run_ctl(*common, "--apply")
                self.assertTrue((project / rule).is_file())
                self.assertTrue((project / "START-HERE.md").is_file())
                self.assertTrue((project / ".agent-config-kit/install-state.json").is_file())
                self.run_ctl("doctor", "--target", str(project))

                second = self.run_ctl(*common, "--apply")
                self.assertIn("Already installed", second.stdout)

                if os.name != "nt":
                    if runtime == "codex":
                        config = json.loads((project / ".codex/hooks.json").read_text())
                        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
                    elif runtime == "cursor":
                        config = json.loads((project / ".cursor/hooks.json").read_text())
                        command = config["hooks"]["sessionStart"][0]["command"]
                    else:
                        config = json.loads((project / ".claude/settings.json").read_text())
                        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
                    command = command.replace(
                        "python3", subprocess.list2cmdline([sys.executable]), 1
                    )
                    hook_result = subprocess.run(
                        command,
                        cwd=project,
                        input="{}",
                        text=True,
                        capture_output=True,
                        shell=True,
                        check=True,
                    )
                    payload = json.loads(hook_result.stdout)
                    if runtime == "cursor":
                        self.assertTrue(payload["continue"])
                        self.assertTrue(payload["additional_context"])
                    else:
                        self.assertEqual(
                            payload["hookSpecificOutput"]["hookEventName"], "SessionStart"
                        )

                preview_remove = self.run_ctl(
                    "uninstall", "--target", str(project)
                )
                self.assertIn("Mode: dry-run", preview_remove.stdout)
                self.assertTrue((project / rule).exists())

                applied_remove = self.run_ctl(
                    "uninstall",
                    "--target",
                    str(project),
                    "--apply",
                    "--confirm-uninstall",
                )
                self.assertFalse((project / rule).exists())
                state = json.loads(
                    (project / ".agent-config-kit/install-state.json").read_text()
                )
                self.assertEqual(state["status"], "uninstalled")
                recovery = project / state["recovery"]
                self.assertTrue((recovery / rule).is_file())
                self.assertIn("Recovery:", applied_remove.stdout)
                restore_preview = self.run_ctl("restore", "--target", str(project))
                self.assertIn("Mode: dry-run", restore_preview.stdout)
                self.assertFalse((project / rule).exists())
                self.run_ctl("restore", "--target", str(project), "--apply")
                self.assertTrue((project / rule).is_file())
                self.run_ctl("doctor", "--target", str(project))

    def test_three_runtime_layered_hook_and_doctor_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for runtime in ("codex", "cursor", "claude-code"):
                project = base / runtime
                project.mkdir()
                install = self.run_ctl(
                    "install",
                    "--runtime",
                    runtime,
                    "--profile",
                    "knowledge-vault",
                    "--target",
                    str(project),
                    "--apply",
                )
                if runtime == "codex":
                    config = json.loads((project / ".codex/hooks.json").read_text())
                    command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
                elif runtime == "cursor":
                    config = json.loads((project / ".cursor/hooks.json").read_text())
                    command = config["hooks"]["sessionStart"][0]["command"]
                else:
                    config = json.loads((project / ".claude/settings.json").read_text())
                    command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
                command = command.replace(
                    "python3", subprocess.list2cmdline([sys.executable]), 1
                )
                result = subprocess.run(
                    command,
                    cwd=project,
                    input="{}",
                    text=True,
                    capture_output=True,
                    shell=True,
                    check=True,
                )
                payload = json.loads(result.stdout)
                context = (
                    payload["additional_context"]
                    if runtime == "cursor"
                    else payload["hookSpecificOutput"]["additionalContext"]
                )
                self.assertIn("Knowledge Vault profile is active", context)
                doctor = self.run_ctl(
                    "doctor",
                    "--target",
                    str(project),
                    "--json",
                    expected=1 if os.name == "nt" else 0,
                )
                health = json.loads(doctor.stdout)
                expected_hook = (
                    "unsupported_native_windows" if os.name == "nt" else "ready"
                )
                self.assertEqual(
                    health["capabilities"]["hook"]["status"], expected_hook
                )
                self.assertEqual(health["live_runtime_smoke"], "not_performed")
                skill_commands = health["capabilities"]["skill_commands"]
                self.assertEqual(skill_commands[0]["command"], "python3")
                self.assertFalse(skill_commands[0]["required"])

    def test_full_profile_installs_every_admitted_skill_in_three_runtimes(self) -> None:
        manifest = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))
        expected = {
            name
            for pack in manifest["profiles"]["full"]["skill_packs"]
            for name in manifest["skill_packs"][pack]
        }
        skills_roots = {
            "codex": Path(".agents/skills"),
            "cursor": Path(".cursor/skills"),
            "claude-code": Path(".claude/skills"),
        }
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            for runtime, skills_root in skills_roots.items():
                project = base / runtime
                project.mkdir()
                install = self.run_ctl(
                    "install",
                    "--runtime",
                    runtime,
                    "--profile",
                    "full",
                    "--target",
                    str(project),
                    "--without-hooks",
                    "--apply",
                )
                self.assertIn("CC BY-NC-SA 4.0", install.stdout)
                self.assertIn("not financial or investment advice", install.stdout)
                self.assertIn("direct buy or sell instructions", install.stdout)
                self.assertIn("high-stakes claims", install.stdout)
                self.assertIn("logged-in browser sessions", install.stdout)
                self.assertIn("create commits and tags", install.stdout)
                self.assertIn("selects the exact issues", install.stdout)
                self.assertIn("installs no background automation", install.stdout)
                self.assertIn("human-review packets only", install.stdout)
                self.assertIn("Cursor Agent's agent CLI", install.stdout)
                self.assertIn("every exact deletion list", install.stdout)
                self.assertIn("hidden affiliation", install.stdout)
                self.assertIn("does not install Playwright automatically", install.stdout)
                self.assertIn("does not bypass login or access controls", install.stdout)
                self.assertIn("hidden prompts", install.stdout)
                self.assertIn("not an evidence-based prediction tool", install.stdout)
                installed = {
                    path.name
                    for path in (project / skills_root).iterdir()
                    if path.is_dir() and (path / "SKILL.md").is_file()
                }
                self.assertEqual(installed, expected)
                doctor = self.run_ctl(
                    "doctor",
                    "--target",
                    str(project),
                    "--json",
                    expected=None,
                )
                self.assertIn(doctor.returncode, (0, 1))
                health = json.loads(doctor.stdout)
                self.assertEqual(health["profile"], "full")
                self.assertEqual(health["capabilities"]["hook"]["status"], "disabled")
                python_capability = next(
                    capability
                    for capability in health["capabilities"]["skill_commands"]
                    if capability["command"] == "python3|python|py"
                )
                self.assertEqual(python_capability["status"], "available")
                self.assertIn(
                    python_capability["resolved_command"],
                    {"python3", "python", "py"},
                )
                environment_capabilities = {
                    capability["environment"]: capability
                    for capability in health["capabilities"]["skill_environment"]
                }
                self.assertEqual(
                    environment_capabilities["TWITTER_AUTH_TOKEN"]["status"],
                    "present" if "TWITTER_AUTH_TOKEN" in os.environ else "missing",
                )
                self.assertFalse(
                    environment_capabilities["TWITTER_AUTH_TOKEN"]["required"]
                )
                connection_capabilities = {
                    capability["connection"]: capability
                    for capability in health["capabilities"]["skill_connections"]
                }
                self.assertEqual(
                    connection_capabilities["github-account"]["status"],
                    "not_verified",
                )
                self.assertEqual(
                    connection_capabilities["rednote-authorized-session"]["status"],
                    "not_verified",
                )
                text_doctor = self.run_ctl(
                    "doctor",
                    "--target",
                    str(project),
                    expected=None,
                )
                self.assertIn(text_doctor.returncode, (0, 1))
                self.assertIn(
                    "Capability skill-environment: TWITTER_AUTH_TOKEN=",
                    text_doctor.stdout,
                )
                self.assertIn(
                    "Capability skill-connection: github-account=not_verified",
                    text_doctor.stdout,
                )
                self.run_ctl("update", "--target", str(project), "--apply")
                self.run_ctl(
                    "uninstall",
                    "--target",
                    str(project),
                    "--apply",
                    "--confirm-uninstall",
                )
                self.assertFalse(list((project / skills_root).rglob("SKILL.md")))
                self.run_ctl("restore", "--target", str(project), "--apply")
                restored_doctor = self.run_ctl(
                    "doctor",
                    "--target",
                    str(project),
                    expected=None,
                )
                self.assertIn(restored_doctor.returncode, (0, 1))

    def test_collision_aborts_without_partial_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            rule = project / "AGENTS.md"
            rule.write_text("user-owned\n", encoding="utf-8")
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
                expected=2,
            )
            self.assertEqual(rule.read_text(encoding="utf-8"), "user-owned\n")
            self.assertFalse((project / ".agents").exists())
            self.assertFalse((project / ".agent-config-kit").exists())

    def test_identical_preexisting_file_is_adopted_and_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            shutil.copy2(REPO / "adapters/codex/AGENTS.md", project / "AGENTS.md")
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--without-hooks",
                "--apply",
            )
            original = digest(project / "AGENTS.md")
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
            )
            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertEqual(digest(project / "AGENTS.md"), original)

    def test_drift_blocks_update_and_is_preserved_on_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
            )
            drifted = project / ".agents/skills/start-here/SKILL.md"
            drifted.write_text(
                drifted.read_text(encoding="utf-8") + "\nuser edit\n",
                encoding="utf-8",
            )
            self.run_ctl(
                "update", "--target", str(project), "--apply", expected=2
            )
            self.assertIn("user edit", drifted.read_text(encoding="utf-8"))
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
            )
            self.assertTrue(drifted.is_file())
            self.assertIn("user edit", drifted.read_text(encoding="utf-8"))

    def test_missing_file_blocks_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.run_ctl(
                "install",
                "--runtime",
                "cursor",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
            )
            missing = project / ".cursor/skills/deep-read/SKILL.md"
            missing.unlink()
            rule = project / ".cursor/rules/agent-config-kit.mdc"
            before = digest(rule)
            self.run_ctl(
                "update", "--target", str(project), "--apply", expected=2
            )
            self.assertEqual(digest(rule), before)

    @unittest.skipIf(
        os.name == "nt", "creating symlinks may require elevated Windows privileges"
    )
    def test_target_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            project = base / "project"
            outside = base / "outside"
            project.mkdir()
            outside.mkdir()
            os.symlink(outside, project / ".agents")
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
                expected=2,
            )
            self.assertEqual(list(outside.iterdir()), [])

    @unittest.skipUnless(os.name == "nt", "NTFS junction test")
    def test_target_junction_is_rejected_on_windows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            project = base / "project"
            outside = base / "outside"
            project.mkdir()
            outside.mkdir()
            junction = project / ".agents"
            result = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(junction), str(outside)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode:
                self.skipTest(f"could not create junction: {result.stderr}")
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--without-hooks",
                "--apply",
                expected=2,
            )
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((project / ".agent-config-kit").exists())

    def test_real_update_changes_only_unchanged_owned_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            package = base / "package"
            project = base / "project"
            shutil.copytree(
                REPO,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            project.mkdir()
            controller = package / "install/scripts/configctl.py"
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
                controller=controller,
            )
            adapter = package / "adapters/codex/AGENTS.md"
            adapter.write_text(
                adapter.read_text(encoding="utf-8") + "\n- Updated release rule.\n",
                encoding="utf-8",
            )
            target_rule = project / "AGENTS.md"
            before = digest(target_rule)
            preview = self.run_ctl(
                "update", "--target", str(project), controller=controller
            )
            self.assertIn("update", preview.stdout)
            self.assertEqual(digest(target_rule), before)
            self.run_ctl(
                "update",
                "--target",
                str(project),
                "--apply",
                controller=controller,
            )
            self.assertIn("Updated release rule", target_rule.read_text(encoding="utf-8"))

    def test_manifest_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            package = base / "package"
            project = base / "project"
            shutil.copytree(
                REPO,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            project.mkdir()
            manifest_path = package / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["common_files"][0]["target"] = "../escape.md"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
                controller=package / "install/scripts/configctl.py",
                expected=2,
            )
            self.assertFalse((base / "escape.md").exists())

    def test_uninstall_refuses_a_broken_package_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            package = base / "package"
            project = base / "project"
            shutil.copytree(
                REPO,
                package,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            project.mkdir()
            controller = package / "install/scripts/configctl.py"
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--apply",
                controller=controller,
            )
            (package / "manifest.json").write_text("{broken", encoding="utf-8")
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
                controller=controller,
                expected=2,
            )
            self.assertTrue((project / "AGENTS.md").is_file())

    def test_forged_state_cannot_delete_an_unplanned_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            victim = project / "victim.txt"
            victim.write_text("keep me\n", encoding="utf-8")
            state_dir = project / ".agent-config-kit"
            state_dir.mkdir()
            forged = {
                "schema_version": 1,
                "status": "installed",
                "release": "0.1.0",
                "runtime": "codex",
                "profile": "daily-work",
                "hooks_enabled": False,
                "files": [
                    {
                        "target": "victim.txt",
                        "source": "packs/core/START-HERE.md",
                        "installed_sha256": digest(victim),
                        "owned": True,
                    }
                ],
            }
            (state_dir / "install-state.json").write_text(
                json.dumps(forged), encoding="utf-8"
            )
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
                expected=2,
            )
            self.assertEqual(victim.read_text(encoding="utf-8"), "keep me\n")

    def test_restore_refuses_to_overwrite_a_new_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.run_ctl(
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--without-hooks",
                "--apply",
            )
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
            )
            (project / "AGENTS.md").write_text("new owner\n", encoding="utf-8")
            self.run_ctl(
                "restore", "--target", str(project), "--apply", expected=2
            )
            self.assertEqual(
                (project / "AGENTS.md").read_text(encoding="utf-8"), "new owner\n"
            )

    def test_reinstall_after_recoverable_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            install = (
                "install",
                "--runtime",
                "codex",
                "--profile",
                "daily-work",
                "--target",
                str(project),
                "--without-hooks",
                "--apply",
            )
            self.run_ctl(*install)
            self.run_ctl(
                "uninstall",
                "--target",
                str(project),
                "--apply",
                "--confirm-uninstall",
            )
            self.run_ctl(*install)
            self.run_ctl("doctor", "--target", str(project))


if __name__ == "__main__":
    unittest.main()
