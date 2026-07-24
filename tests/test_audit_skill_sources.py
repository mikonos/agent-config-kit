from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
AUDITOR = REPO / "scripts" / "audit_skill_sources.py"


def write_skill(root: Path, folder: str, name: str, body: str = "") -> Path:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True)
    skill = skill_dir / "SKILL.md"
    skill.write_text(
        f"---\nname: {name}\ndescription: Test skill.\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return skill


class SkillSourceAuditTests(unittest.TestCase):
    def run_audit(
        self,
        *sources: tuple[str, Path],
        expected: int = 0,
        fail: bool = False,
        private_terms: tuple[str, ...] = (),
        entry_mode: str = "recursive",
    ) -> dict:
        with tempfile.TemporaryDirectory() as report_temp:
            output = Path(report_temp) / "audit.json"
            command = [
                sys.executable,
                str(AUDITOR),
                "--report",
                "detailed",
                "--output",
                str(output),
                "--entry-mode",
                entry_mode,
            ]
            for label, path in sources:
                command.extend(("--source", f"{label}={path}"))
            for term in private_terms:
                command.extend(("--private-term", term))
            if fail:
                command.append("--fail-on-blockers")
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(
                result.returncode,
                expected,
                msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertEqual(result.stdout, "")
            if os.name != "nt":
                self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            return json.loads(output.read_text(encoding="utf-8"))

    def test_top_level_mode_excludes_embedded_skill_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = write_skill(root, "bundle", "bundle")
            write_skill(parent.parent, "example", "example")
            report = self.run_audit(
                ("local", root),
                entry_mode="top-level",
            )
            self.assertEqual(report["entry_mode"], "top-level")
            self.assertEqual(report["summary"]["entries"], 1)
            self.assertEqual(report["entries"][0]["name"], "bundle")
            self.assertFalse(report["entries"][0]["nested"])

    def test_clean_skill_inventory_is_relative_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = write_skill(root, "hello", "hello", "Run python3 safely.")
            (skill.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            first = self.run_audit(("local", root))
            second = self.run_audit(("local", root))
            self.assertEqual(first, second)
            self.assertEqual(first["summary"]["entries"], 1)
            self.assertEqual(first["summary"]["unique_names"], 1)
            entry = first["entries"][0]
            self.assertEqual(entry["path"], "hello/SKILL.md")
            self.assertNotIn(str(root), json.dumps(first))
            self.assertEqual(entry["technical_status"], "review")
            self.assertEqual(entry["dependencies"]["commands"], ["python3"])
            self.assertEqual(entry["license"]["files"], ["hello/LICENSE"])

    def test_prompt_arguments_placeholder_is_not_an_environment_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = write_skill(root, "prompt", "prompt", "Analyze $ARGUMENTS.")
            (skill.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = self.run_audit(("local", root))
            self.assertEqual(report["entries"][0]["dependencies"]["environment"], [])

    def test_duplicate_name_and_folder_mismatch_block_release(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            one = base / "one"
            two = base / "two"
            write_skill(one, "first", "shared")
            write_skill(two, "shared", "shared")
            report = self.run_audit(("one", one), ("two", two), expected=2, fail=True)
            self.assertEqual(report["summary"]["duplicate_names"], 1)
            self.assertEqual(report["duplicates"][0]["name"], "shared")
            self.assertTrue(report["duplicates"][0]["identical_content"])
            self.assertEqual(
                report["duplicates"][0]["resolution"], "auto_deduplicate"
            )
            self.assertEqual(
                report["duplicates"][0]["canonical_candidate"],
                {"source": "one", "path": "first/SKILL.md"},
            )
            codes = {
                issue["code"]
                for entry in report["entries"]
                for issue in entry["blockers"]
            }
            self.assertIn("duplicate_name", codes)
            self.assertIn("folder_name_mismatch", codes)

    def test_different_duplicate_content_requires_manual_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            one = base / "one"
            two = base / "two"
            write_skill(one, "shared", "shared", "First implementation.")
            write_skill(two, "shared", "shared", "Second implementation.")
            report = self.run_audit(("one", one), ("two", two))
            duplicate = report["duplicates"][0]
            self.assertFalse(duplicate["identical_content"])
            self.assertEqual(duplicate["resolution"], "manual_compare")
            self.assertIsNone(duplicate["canonical_candidate"])
            self.assertEqual(report["summary"]["conflicting_duplicate_names"], 1)

    @unittest.skipIf(os.name == "nt", "POSIX executable bits are not portable to Windows")
    def test_mode_or_incomplete_package_prevents_auto_deduplication(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            one = base / "one"
            two = base / "two"
            first = write_skill(one, "shared", "shared")
            second = write_skill(two, "shared", "shared")
            first.chmod(0o644)
            second.chmod(0o755)
            mode_report = self.run_audit(("one", one), ("two", two))
            duplicate = mode_report["duplicates"][0]
            self.assertFalse(duplicate["identical_content"])
            self.assertEqual(duplicate["resolution"], "manual_compare")

            second.chmod(0o644)
            (two / "shared" / ".venv").mkdir()
            incomplete_report = self.run_audit(("one", one), ("two", two))
            duplicate = incomplete_report["duplicates"][0]
            self.assertTrue(duplicate["identical_content"])
            self.assertFalse(duplicate["complete_packages"])
            self.assertEqual(duplicate["resolution"], "manual_compare")
            self.assertIsNone(duplicate["canonical_candidate"])

    def test_sensitive_values_are_not_copied_into_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            token = "sk-" + "A" * 30
            skill = write_skill(
                root,
                "private",
                "private",
                f'Use {"/" + "Users" + "/"}example/private-vault and token "{token}".',
            )
            (skill.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = self.run_audit(("private", root), expected=2, fail=True)
            encoded = json.dumps(report)
            self.assertNotIn(token, encoded)
            codes = {
                issue["code"] for issue in report["entries"][0]["blockers"]
            }
            self.assertIn("macos_home_path", codes)
            self.assertIn("openai_style_secret", codes)

            named = write_skill(
                root,
                "named",
                "named",
                "This belongs to Example Private Workspace.",
            )
            (named.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = self.run_audit(
                ("private", root),
                expected=2,
                fail=True,
                private_terms=("Example Private Workspace",),
            )
            encoded = json.dumps(report)
            self.assertNotIn("Example Private Workspace", encoded)
            named_entry = next(
                entry for entry in report["entries"] if entry["name"] == "named"
            )
            self.assertIn(
                "private_term_1",
                {issue["code"] for issue in named_entry["blockers"]},
            )

    def test_word_internal_secret_shape_is_reviewed_not_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = write_skill(
                root,
                "false-positive",
                "false-positive",
                "A long Musk-" + "research-slug-" * 3,
            )
            (skill.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = self.run_audit(("local", root))
            entry = report["entries"][0]
            self.assertNotIn(
                "openai_style_secret",
                {issue["code"] for issue in entry["blockers"]},
            )
            self.assertIn(
                "openai_style_secret_candidate",
                {issue["code"] for issue in entry["reviews"]},
            )

    def test_default_summary_does_not_expose_skill_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill(root, "private-name", "private-name")
            result = subprocess.run(
                [
                    sys.executable,
                    str(AUDITOR),
                    "--source",
                    f"local={root}",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(report["sensitivity"], "public_summary")
            self.assertNotIn("private-name", result.stdout)
            self.assertNotIn("entries", report)

    def test_unowned_artifact_directory_blocks_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill(root, "clean", "clean")
            (root / ".venv").mkdir()
            report = self.run_audit(("local", root), expected=2, fail=True)
            self.assertEqual(report["summary"]["source_blockers"], 1)
            self.assertEqual(
                report["sources"][0]["blockers"][0]["code"],
                "source_excluded_artifact_directory",
            )

    def test_platform_builtin_skills_are_counted_but_out_of_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_skill(root, "public", "public")
            write_skill(root / ".system", "builtin", "builtin")
            report = self.run_audit(("local", root))
            self.assertEqual(report["summary"]["entries"], 1)
            source = report["sources"][0]
            self.assertEqual(
                source["excluded_skill_entries"],
                [{"path": ".system/builtin/SKILL.md", "reason": "platform_builtin"}],
            )
            self.assertEqual(report["summary"]["source_blockers"], 0)

    def test_binary_assets_are_reviewed_and_executables_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image_skill = write_skill(root, "image", "image")
            (image_skill.parent / "preview.png").write_bytes(b"\x89PNG\r\n\x1a\n\xff")
            binary_skill = write_skill(root, "binary", "binary")
            (binary_skill.parent / "payload.exe").write_bytes(b"MZ\xff")
            report = self.run_audit(("local", root))
            entries = {entry["name"]: entry for entry in report["entries"]}
            self.assertIn(
                "binary_asset_review",
                {issue["code"] for issue in entries["image"]["reviews"]},
            )
            self.assertNotIn(
                "binary_or_non_utf8_file",
                {issue["code"] for issue in entries["image"]["blockers"]},
            )
            self.assertIn(
                "dangerous_binary_file",
                {issue["code"] for issue in entries["binary"]["blockers"]},
            )

    def test_additional_private_key_shapes_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = write_skill(
                root,
                "keys",
                "keys",
                "ASIA" + "A" * 16 + "\nBEGIN " + "DSA PRIVATE KEY\n",
            )
            (skill.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            report = self.run_audit(("local", root), expected=2, fail=True)
            codes = {issue["code"] for issue in report["entries"][0]["blockers"]}
            self.assertIn("aws_temporary_access_key", codes)
            self.assertIn("private_key", codes)

    def test_artifacts_nested_skills_and_side_effects_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = write_skill(root, "bundle", "bundle")
            (parent.parent / "LICENSE").write_text("MIT\n", encoding="utf-8")
            child = write_skill(
                parent.parent,
                "child",
                "child",
                "Deploy and send a message after payment.",
            )
            (child.parent / ".venv").mkdir()
            (child.parent / ".system").mkdir()
            (child.parent / "notes.bak-1").write_text("old\n", encoding="utf-8")
            report = self.run_audit(("bundle", root), expected=2, fail=True)
            entries = {entry["name"]: entry for entry in report["entries"]}
            self.assertFalse(entries["bundle"]["nested"])
            self.assertTrue(entries["child"]["nested"])
            self.assertEqual(entries["child"]["license"]["files"], ["bundle/LICENSE"])
            self.assertIn(
                "nested_skill_entry",
                {issue["code"] for issue in entries["child"]["reviews"]},
            )
            self.assertEqual(
                entries["child"]["side_effects"],
                ["deployment_or_publish", "external_message", "payment"],
            )
            codes = {issue["code"] for issue in entries["child"]["blockers"]}
            self.assertIn("backup_or_recovery_artifact", codes)
            self.assertIn("excluded_artifact_directory", codes)
            self.assertEqual(
                report["sources"][0]["excluded_artifact_directories"], 2
            )

    @unittest.skipIf(
        os.name == "nt", "creating symlinks may require elevated Windows privileges"
    )
    def test_symlink_is_reported_without_following_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "root"
            outside = base / "outside"
            skill = write_skill(root, "linked", "linked")
            outside.mkdir()
            (outside / "secret.txt").write_text("outside\n", encoding="utf-8")
            os.symlink(outside, skill.parent / "external")
            report = self.run_audit(("linked", root), expected=2, fail=True)
            blockers = report["entries"][0]["blockers"]
            self.assertIn("symlink", {issue["code"] for issue in blockers})
            self.assertNotIn("outside", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
