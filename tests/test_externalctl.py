from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "install" / "scripts"))
import externalctl  # noqa: E402


SKILL_DATA = b"---\nname: official-demo\ndescription: Demo.\n---\n"


def fixture_catalog() -> dict:
    return {
        "schema_version": 1,
        "packs": {
            "official": {
                "description": "Fixture.",
                "source_host": "official.example",
                "skills": [
                    {
                        "name": "official-demo",
                        "sha256": hashlib.sha256(SKILL_DATA).hexdigest(),
                        "url": (
                            "https://official.example/.well-known/skills/"
                            "official-demo/SKILL.md"
                        ),
                    }
                ],
            }
        },
    }


def fixture_manifest() -> dict:
    return {
        "runtimes": {
            "codex": {"skills_root": ".agents/skills"},
            "cursor": {"skills_root": ".cursor/skills"},
            "claude-code": {"skills_root": ".claude/skills"},
        }
    }


class ExternalControllerTests(unittest.TestCase):
    def test_current_external_catalog_matches_unbundled_well_known_sources(self) -> None:
        catalog = json.loads(
            (REPO / "catalog" / "external_skills.json").read_text(encoding="utf-8")
        )
        sources = json.loads(
            (REPO / "catalog" / "runtime_sources.json").read_text(encoding="utf-8")
        )
        packs = externalctl.validate_catalog(catalog)
        catalog_names = {
            entry["name"]
            for pack in packs.values()
            for entry in pack["skills"]
        }
        source_names = {
            entry["name"]
            for entry in sources["skills"]
            if entry["source_type"] == "well-known"
            and entry["delivery"] == "fetch_from_origin"
        }
        self.assertEqual(catalog_names, source_names)

    def test_catalog_rejects_unapproved_host_or_path(self) -> None:
        catalog = fixture_catalog()
        externalctl.validate_catalog(catalog)
        for bad_url in (
            "http://official.example/.well-known/skills/official-demo/SKILL.md",
            "https://evil.example/.well-known/skills/official-demo/SKILL.md",
            "https://official.example/.well-known/skills/other/SKILL.md",
            "https://official.example/.well-known/skills/official-demo/SKILL.md?new=1",
        ):
            modified = copy.deepcopy(catalog)
            modified["packs"]["official"]["skills"][0]["url"] = bad_url
            with self.assertRaises(externalctl.configctl.ConfigError):
                externalctl.validate_catalog(modified)
        duplicate_case = copy.deepcopy(catalog)
        duplicate_case["packs"]["official"]["skills"].append(
            {
                "name": "Official-Demo",
                "sha256": "a" * 64,
                "url": (
                    "https://official.example/.well-known/skills/"
                    "Official-Demo/SKILL.md"
                ),
            }
        )
        with self.assertRaises(externalctl.configctl.ConfigError):
            externalctl.validate_catalog(duplicate_case)
        for bad_name in ("CON", "LPT1.txt", "demo."):
            invalid_name = fixture_catalog()
            entry = invalid_name["packs"]["official"]["skills"][0]
            entry["name"] = bad_name
            entry["url"] = (
                f"https://official.example/.well-known/skills/{bad_name}/SKILL.md"
            )
            with self.assertRaises(externalctl.configctl.ConfigError):
                externalctl.validate_catalog(invalid_name)

    def test_fetch_plan_binds_hash_name_and_runtime_target(self) -> None:
        plan = externalctl.fetch_plan(
            fixture_manifest(),
            fixture_catalog(),
            "cursor",
            ["official"],
            fetcher=lambda entry, host: SKILL_DATA,
        )
        self.assertEqual(len(plan), 1)
        self.assertEqual(
            plan[0].target_rel,
            ".cursor/skills/official-demo/SKILL.md",
        )
        self.assertEqual(plan[0].sha256, hashlib.sha256(SKILL_DATA).hexdigest())

    def test_state_accepts_only_current_or_reviewed_previous_hash(self) -> None:
        catalog = fixture_catalog()
        old_hash = "b" * 64
        catalog["packs"]["official"]["skills"][0]["previous_sha256"] = [old_hash]
        state = {
            "schema_version": 1,
            "status": "installed",
            "runtime": "codex",
            "packs": ["official"],
            "files": [
                {
                    "name": "official-demo",
                    "target": ".agents/skills/official-demo/SKILL.md",
                    "url": (
                        "https://official.example/.well-known/skills/"
                        "official-demo/SKILL.md"
                    ),
                    "installed_sha256": old_hash,
                }
            ],
        }
        externalctl.validate_state(state, fixture_manifest(), catalog)
        state["files"][0]["installed_sha256"] = "c" * 64
        with self.assertRaises(externalctl.configctl.ConfigError):
            externalctl.validate_state(state, fixture_manifest(), catalog)

    def test_install_doctor_uninstall_and_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            install_args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=False,
            )
            with mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA):
                externalctl.command_install(
                    install_args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
                skill = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
                self.assertFalse(skill.exists())
                install_args.apply = True
                externalctl.command_install(
                    install_args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual(skill.read_bytes(), SKILL_DATA)
            self.assertEqual(
                externalctl.command_doctor(
                    argparse.Namespace(target=str(target)),
                    fixture_manifest(),
                    fixture_catalog(),
                ),
                0,
            )

            uninstall_args = argparse.Namespace(
                target=str(target),
                apply=True,
                confirm_uninstall=False,
            )
            with self.assertRaises(externalctl.configctl.ConfigError):
                externalctl.command_uninstall(
                    uninstall_args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertTrue(skill.exists())
            uninstall_args.confirm_uninstall = True
            externalctl.command_uninstall(
                uninstall_args,
                fixture_manifest(),
                fixture_catalog(),
            )
            self.assertFalse(skill.exists())

            externalctl.command_restore(
                argparse.Namespace(target=str(target), apply=True),
                fixture_manifest(),
                fixture_catalog(),
            )
            self.assertEqual(skill.read_bytes(), SKILL_DATA)
            self.assertEqual(
                externalctl.command_doctor(
                    argparse.Namespace(target=str(target)),
                    fixture_manifest(),
                    fixture_catalog(),
                ),
                0,
            )

    def test_same_name_directory_with_extra_file_stops_whole_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            skill_dir = target / ".agents" / "skills" / "official-demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "user.txt").write_text("keep\n", encoding="utf-8")
            args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=True,
            )
            with (
                mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA),
                self.assertRaises(externalctl.configctl.ConfigError),
            ):
                externalctl.command_install(
                    args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual((skill_dir / "user.txt").read_text(), "keep\n")
            self.assertFalse((skill_dir / "SKILL.md").exists())

    def test_identical_preexisting_skill_is_not_adopted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            skill = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_bytes(SKILL_DATA)
            args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=True,
            )
            with (
                mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA),
                self.assertRaises(externalctl.configctl.ConfigError),
            ):
                externalctl.command_install(
                    args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual(skill.read_bytes(), SKILL_DATA)
            self.assertFalse(
                (target / ".agent-config-kit" / "external-state.json").exists()
            )

    def test_exclusive_apply_refuses_target_created_after_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            plan = externalctl.fetch_plan(
                fixture_manifest(),
                fixture_catalog(),
                "codex",
                ["official"],
                fetcher=lambda entry, host: SKILL_DATA,
            )
            actions, writes, records = externalctl.install_records(target, plan)
            self.assertEqual(actions[0][0], "create")
            destination = target / plan[0].target_rel
            destination.parent.mkdir(parents=True)
            destination.write_text("user\n", encoding="utf-8")
            with self.assertRaises(externalctl.configctl.ConfigError):
                externalctl.apply_install(
                    target,
                    writes,
                    {
                        "schema_version": 1,
                        "status": "installed",
                        "runtime": "codex",
                        "packs": ["official"],
                        "files": records,
                    },
                )
            self.assertEqual(destination.read_text(encoding="utf-8"), "user\n")
            self.assertFalse(
                (target / ".agent-config-kit" / "external-state.json").exists()
            )

    def test_redirect_handler_refuses_followup_request(self) -> None:
        handler = externalctl.RejectRedirects()
        self.assertIsNone(
            handler.redirect_request(None, None, 302, "Found", {}, "https://evil.example")
        )

    def test_uninstall_move_failure_rolls_back_prior_files(self) -> None:
        second_data = b"---\nname: official-second\ndescription: Second.\n---\n"
        catalog = fixture_catalog()
        catalog["packs"]["official"]["skills"].append(
            {
                "name": "official-second",
                "sha256": hashlib.sha256(second_data).hexdigest(),
                "url": (
                    "https://official.example/.well-known/skills/"
                    "official-second/SKILL.md"
                ),
            }
        )
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=True,
            )
            with mock.patch.object(
                externalctl,
                "fetch_entry",
                side_effect=lambda entry, host: (
                    SKILL_DATA if entry["name"] == "official-demo" else second_data
                ),
            ):
                externalctl.command_install(
                    args,
                    fixture_manifest(),
                    catalog,
                )
            first = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
            second = target / ".agents" / "skills" / "official-second" / "SKILL.md"
            real_move = externalctl.move_file
            calls = 0

            def fail_second_move(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("fixture move failure")
                real_move(source, destination)

            with (
                mock.patch.object(
                    externalctl,
                    "move_file",
                    side_effect=fail_second_move,
                ),
                self.assertRaises(OSError),
            ):
                externalctl.command_uninstall(
                    argparse.Namespace(
                        target=str(target),
                        apply=True,
                        confirm_uninstall=True,
                    ),
                    fixture_manifest(),
                    catalog,
                )
            self.assertEqual(first.read_bytes(), SKILL_DATA)
            self.assertEqual(second.read_bytes(), second_data)
            state = json.loads(
                (target / ".agent-config-kit" / "external-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["status"], "installed")

    def test_restore_refuses_target_created_after_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            install_args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=True,
            )
            with mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA):
                externalctl.command_install(
                    install_args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            externalctl.command_uninstall(
                argparse.Namespace(
                    target=str(target),
                    apply=True,
                    confirm_uninstall=True,
                ),
                fixture_manifest(),
                fixture_catalog(),
            )
            skill = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
            real_exclusive_write = externalctl.exclusive_write

            def create_user_file_before_restore(path: Path, data: bytes) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("user\n", encoding="utf-8")
                real_exclusive_write(path, data)

            with (
                mock.patch.object(
                    externalctl,
                    "exclusive_write",
                    side_effect=create_user_file_before_restore,
                ),
                self.assertRaises(externalctl.configctl.ConfigError),
            ):
                externalctl.command_restore(
                    argparse.Namespace(target=str(target), apply=True),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual(skill.read_text(encoding="utf-8"), "user\n")
            state = json.loads(
                (target / ".agent-config-kit" / "external-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["status"], "uninstalled")

    def test_restore_rechecks_recovery_bytes_after_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            with mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA):
                externalctl.command_install(
                    argparse.Namespace(
                        target=str(target),
                        runtime="codex",
                        pack=["official"],
                        apply=True,
                    ),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            externalctl.command_uninstall(
                argparse.Namespace(
                    target=str(target),
                    apply=True,
                    confirm_uninstall=True,
                ),
                fixture_manifest(),
                fixture_catalog(),
            )
            state_path = target / ".agent-config-kit" / "external-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            backup = (
                target
                / state["recovery"]
                / ".agents"
                / "skills"
                / "official-demo"
                / "SKILL.md"
            )

            def mutate_after_preview(*args, **kwargs) -> None:
                backup.write_text("changed\n", encoding="utf-8")

            with (
                mock.patch.object(
                    externalctl.configctl,
                    "print_plan",
                    side_effect=mutate_after_preview,
                ),
                self.assertRaises(externalctl.configctl.ConfigError),
            ):
                externalctl.command_restore(
                    argparse.Namespace(target=str(target), apply=True),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            skill = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
            self.assertFalse(skill.exists())
            self.assertEqual(
                json.loads(state_path.read_text(encoding="utf-8"))["status"],
                "uninstalled",
            )

    def test_uninstall_rechecks_bytes_after_move_and_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            with mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA):
                externalctl.command_install(
                    argparse.Namespace(
                        target=str(target),
                        runtime="codex",
                        pack=["official"],
                        apply=True,
                    ),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            skill = target / ".agents" / "skills" / "official-demo" / "SKILL.md"
            real_move = externalctl.move_file
            calls = 0

            def mutate_before_first_move(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 1:
                    source.write_text("changed\n", encoding="utf-8")
                real_move(source, destination)

            with (
                mock.patch.object(
                    externalctl,
                    "move_file",
                    side_effect=mutate_before_first_move,
                ),
                self.assertRaises(externalctl.configctl.ConfigError),
            ):
                externalctl.command_uninstall(
                    argparse.Namespace(
                        target=str(target),
                        apply=True,
                        confirm_uninstall=True,
                    ),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual(skill.read_text(encoding="utf-8"), "changed\n")
            state = json.loads(
                (target / ".agent-config-kit" / "external-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["status"], "installed")

    def test_forged_state_cannot_delete_an_unapproved_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            args = argparse.Namespace(
                target=str(target),
                runtime="codex",
                pack=["official"],
                apply=True,
            )
            with mock.patch.object(externalctl, "fetch_entry", return_value=SKILL_DATA):
                externalctl.command_install(
                    args,
                    fixture_manifest(),
                    fixture_catalog(),
                )
            sentinel = target / "keep.txt"
            sentinel.write_text("keep\n", encoding="utf-8")
            state_path = target / ".agent-config-kit" / "external-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["files"][0]["target"] = "keep.txt"
            state["files"][0]["installed_sha256"] = hashlib.sha256(
                sentinel.read_bytes()
            ).hexdigest()
            state_path.write_text(json.dumps(state), encoding="utf-8")
            with self.assertRaises(externalctl.configctl.ConfigError):
                externalctl.command_uninstall(
                    argparse.Namespace(
                        target=str(target),
                        apply=True,
                        confirm_uninstall=True,
                    ),
                    fixture_manifest(),
                    fixture_catalog(),
                )
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
