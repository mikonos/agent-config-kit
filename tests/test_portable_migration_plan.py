from __future__ import annotations

import importlib.util
import hashlib
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "plan_portable_migration",
    REPO / "scripts" / "plan_portable_migration.py",
)
assert SPEC and SPEC.loader
PLANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLANNER)


class PortableMigrationPlanTests(unittest.TestCase):
    def test_hash_only_sanitizer_replaces_private_tokens_without_storing_them(self) -> None:
        ledger = {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_003",
                    "length": 11,
                    "matcher": "ascii_token",
                    "sha256": hashlib.sha256(
                        "privateword".encode("utf-8")
                    ).hexdigest(),
                }
            ],
        }

        sanitized, changed = PLANNER.sanitize_text(
            "Owner: privateword",
            ledger,
            replacements={"private_term_003": "target-project"},
        )

        self.assertTrue(changed)
        self.assertEqual(sanitized, "Owner: target-project")

    def test_sanitizer_portabilizes_home_paths_and_template_markers(self) -> None:
        ledger = {"schema_version": 1, "terms": []}
        private_home = "/" + "Users" + "/local-user/project"
        unfinished = "[" + "TODO" + ": replace]"

        sanitized, changed = PLANNER.sanitize_text(
            f"root={private_home}\nlabel={unfinished}\n",
            ledger,
            replacements={},
        )

        self.assertTrue(changed)
        self.assertEqual(
            sanitized,
            "root=/path/to/project\nlabel=[TBD: replace]\n",
        )

    def test_sanitizer_applies_private_alias_map(self) -> None:
        sanitized, changed = PLANNER.sanitize_text(
            "name: PrivateCloud\nrun privatecloud now\n",
            {"schema_version": 1, "terms": []},
            replacements={},
            aliases={"privatecloud": "product-cloud-operations"},
        )

        self.assertTrue(changed)
        self.assertEqual(
            sanitized,
            "name: product-cloud-operations\n"
            "run product-cloud-operations now\n",
        )

    def test_underscore_alias_replaces_standalone_reference_only(self) -> None:
        private = "_" + "preamble"
        sanitized, changed = PLANNER.sanitize_text(
            f"Use `{private}`; keep add_zk{private}.py and has{private}.\n",
            {"schema_version": 1, "terms": []},
            replacements={},
            aliases={private: "vault-writing-preamble"},
        )

        self.assertTrue(changed)
        self.assertEqual(
            sanitized,
            "Use `vault-writing-preamble`; keep add_zk_preamble.py "
            "and has_preamble.\n",
        )

    def test_specific_alias_wins_before_generic_private_term_replacement(self) -> None:
        private_name = "private-product"
        ledger = {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_003",
                    "length": len(private_name),
                    "matcher": "ascii_token",
                    "sha256": hashlib.sha256(
                        private_name.encode("utf-8")
                    ).hexdigest(),
                }
            ],
        }

        sanitized, _ = PLANNER.sanitize_text(
            f"name: {private_name}\n",
            ledger,
            replacements={"private_term_003": "target-project"},
            aliases={private_name: "public-workflow"},
        )

        self.assertEqual(sanitized, "name: public-workflow\n")

    def test_private_ascii_term_is_replaced_inside_compound_identifier(self) -> None:
        private_name = "privateproduct"
        ledger = {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_003",
                    "length": len(private_name),
                    "matcher": "ascii_token",
                    "sha256": hashlib.sha256(
                        private_name.encode("utf-8")
                    ).hexdigest(),
                }
            ],
        }

        sanitized, _ = PLANNER.sanitize_text(
            f"example={private_name.title()}FamilyHub\n",
            ledger,
            replacements={"private_term_003": "target-project"},
        )

        self.assertEqual(sanitized, "example=target-projectFamilyHub\n")

    def test_generation_material_is_not_runtime_delivery(self) -> None:
        self.assertEqual(
            PLANNER.skill_specific_omission_reason(
                skill="huashu-nuwa",
                pack="persona-authoring",
                relative="examples/demo/SKILL.md",
                is_dir=False,
            ),
            "generation_material",
        )
        self.assertEqual(
            PLANNER.skill_specific_omission_reason(
                skill="april-dunford-perspective",
                pack="generated-domain-perspectives",
                relative="references/research/01-writings.md",
                is_dir=False,
            ),
            "generation_material",
        )
        self.assertIsNone(
            PLANNER.skill_specific_omission_reason(
                skill="demo",
                pack="core",
                relative="references/runtime.md",
                is_dir=False,
            )
        )

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source_root = self.root / "source"
        self.package_root = self.root / "package"
        self.source_skill = self.source_root / "demo"
        self.package_skill = self.package_root / "packs" / "core" / "skills" / "demo"
        self.source_skill.mkdir(parents=True)
        self.package_skill.mkdir(parents=True)
        self.inventory = {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "skills": {
                "demo": {
                    "selected_source": "cursor-vault",
                    "selected_path": "demo/SKILL.md",
                    "disposition": {"status": "bundled"},
                }
            },
        }
        self.manifest = {
            "schema_version": 1,
            "skill_packs": {"core": ["demo"]},
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_plan_separates_runtime_copy_omission_and_stale_delete(self) -> None:
        self.write(self.source_skill / "SKILL.md", "current\n")
        self.write(self.source_skill / "references" / "runtime.md", "needed\n")
        self.write(self.source_skill / "test-prompts.json", "{}\n")
        self.write(self.package_skill / "SKILL.md", "old\n")
        self.write(self.package_skill / "legacy.md", "stale\n")

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
        )

        self.assertEqual(plan["summary"]["add"], 1)
        self.assertEqual(plan["summary"]["replace"], 1)
        self.assertEqual(plan["summary"]["delete"], 1)
        self.assertEqual(plan["summary"]["omit"], 1)
        self.assertEqual(
            plan["omissions"][0]["reason"],
            "test_metadata",
        )

    def test_new_manifest_skill_can_be_added_without_existing_package_directory(self) -> None:
        self.package_skill.rmdir()
        self.write(self.source_skill / "SKILL.md", "current\n")

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
        )

        self.assertEqual(plan["summary"]["add"], 1)
        self.assertEqual(plan["summary"]["delete"], 0)

    def test_private_alias_portabilizes_support_file_path(self) -> None:
        self.package_skill.rmdir()
        self.package_skill = (
            self.package_root / "packs" / "core" / "skills" / "public-demo"
        )
        self.package_skill.mkdir(parents=True)
        self.inventory["skills"]["demo"]["public_name"] = "public-demo"
        self.inventory["skills"]["demo"]["portable_aliases"] = {
            "demo": "public-demo"
        }
        self.manifest["skill_packs"]["core"] = ["public-demo"]
        self.write(self.source_skill / "SKILL.md", "name: demo\n")
        self.write(
            self.source_skill / "references" / "demo-guide.md",
            "same\n",
        )
        self.write(self.package_skill / "SKILL.md", "name: public-demo\n")
        self.write(
            self.package_skill / "references" / "public-demo-guide.md",
            "same\n",
        )

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger={"schema_version": 1, "terms": []},
        )

        self.assertEqual(plan["summary"]["add"], 0)
        self.assertEqual(plan["summary"]["delete"], 0)
        self.assertEqual(plan["summary"]["register_derivative"], 1)

    def test_shared_reference_alias_portabilizes_runtime_reference(self) -> None:
        self.inventory["portable_reference_aliases"] = {
            "private-suite/": "public-suite/",
        }
        self.write(
            self.source_skill / "SKILL.md",
            "Read private-suite/SKILL.md\n",
        )
        self.write(
            self.package_skill / "SKILL.md",
            "Read public-suite/SKILL.md\n",
        )

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger={"schema_version": 1, "terms": []},
        )

        self.assertEqual(plan["summary"]["replace"], 0)
        self.assertEqual(plan["summary"]["register_derivative"], 1)

    def test_registered_current_replacement_is_preserved(self) -> None:
        self.write(self.source_skill / "SKILL.md", "private\n")
        self.write(self.package_skill / "SKILL.md", "portable\n")
        patch = {
            "packaged_path": "packs/core/skills/demo/SKILL.md",
            "source_sha256": PLANNER.sha256_file(self.source_skill / "SKILL.md"),
            "packaged_sha256": PLANNER.sha256_file(self.package_skill / "SKILL.md"),
        }

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": [patch]},
        )

        self.assertEqual(plan["summary"]["preserve_derivative"], 1)
        self.assertEqual(plan["summary"]["replace"], 0)

    def test_only_deterministic_sanitizer_output_can_be_registered(self) -> None:
        self.write(self.source_skill / "SKILL.md", "Owner: privateword\n")
        self.write(self.package_skill / "SKILL.md", "Owner: target-project\n")
        ledger = {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_003",
                    "length": 11,
                    "matcher": "ascii_token",
                    "sha256": hashlib.sha256(
                        "privateword".encode("utf-8")
                    ).hexdigest(),
                }
            ],
        }

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger=ledger,
        )

        self.assertEqual(plan["summary"]["register_derivative"], 1)
        self.assertEqual(plan["summary"]["replace"], 0)
        operation = plan["operations"]["register_derivative"][0]
        self.assertEqual(
            operation["expected_packaged_sha256"],
            operation["packaged_sha256"],
        )

    def test_arbitrary_existing_output_cannot_be_registered(self) -> None:
        self.write(self.source_skill / "SKILL.md", "Owner: privateword\n")
        self.write(self.package_skill / "SKILL.md", "unrelated content\n")
        ledger = {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_003",
                    "length": 11,
                    "matcher": "ascii_token",
                    "sha256": hashlib.sha256(
                        "privateword".encode("utf-8")
                    ).hexdigest(),
                }
            ],
        }

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger=ledger,
        )

        self.assertEqual(plan["summary"]["register_derivative"], 0)
        self.assertEqual(plan["summary"]["replace"], 1)

    def test_exact_private_review_preserves_manual_derivative(self) -> None:
        self.write(self.source_skill / "SKILL.md", "unsafe source\n")
        self.write(self.package_skill / "SKILL.md", "safe reviewed rewrite\n")
        packaged_path = "packs/core/skills/demo/SKILL.md"
        reviewed = {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "derivatives": [
                {
                    "description": "Safety-reviewed clean rewrite.",
                    "source_skill": "demo",
                    "source_path": "SKILL.md",
                    "packaged_path": packaged_path,
                    "source_sha256": PLANNER.sha256_file(
                        self.source_skill / "SKILL.md"
                    ),
                    "packaged_sha256": PLANNER.sha256_file(
                        self.package_skill / "SKILL.md"
                    ),
                }
            ],
        }

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger={"schema_version": 1, "terms": []},
            reviewed_derivatives=reviewed,
        )

        self.assertEqual(plan["summary"]["preserve_reviewed_derivative"], 1)
        self.assertEqual(plan["summary"]["replace"], 0)

    def test_stale_private_review_cannot_preserve_changed_package_bytes(self) -> None:
        self.write(self.source_skill / "SKILL.md", "unsafe source\n")
        self.write(self.package_skill / "SKILL.md", "unapproved rewrite\n")
        reviewed = {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "derivatives": [
                {
                    "description": "Safety-reviewed clean rewrite.",
                    "source_skill": "demo",
                    "source_path": "SKILL.md",
                    "packaged_path": "packs/core/skills/demo/SKILL.md",
                    "source_sha256": PLANNER.sha256_file(
                        self.source_skill / "SKILL.md"
                    ),
                    "packaged_sha256": "0" * 64,
                }
            ],
        }

        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
            privacy_ledger={"schema_version": 1, "terms": []},
            reviewed_derivatives=reviewed,
        )

        self.assertEqual(plan["summary"]["preserve_reviewed_derivative"], 0)
        self.assertEqual(plan["summary"]["replace"], 1)

    def test_apply_plan_checks_hashes_then_copies_and_deletes(self) -> None:
        self.write(self.source_skill / "SKILL.md", "current\n")
        self.write(self.source_skill / "references" / "runtime.md", "needed\n")
        self.write(self.package_skill / "SKILL.md", "old\n")
        self.write(self.package_skill / "legacy.md", "stale\n")
        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
        )

        PLANNER.apply_plan(
            plan=plan,
            private_inventory=self.inventory,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
        )

        self.assertEqual(
            (self.package_skill / "SKILL.md").read_text(encoding="utf-8"),
            "current\n",
        )
        self.assertTrue((self.package_skill / "references" / "runtime.md").is_file())
        self.assertFalse((self.package_skill / "legacy.md").exists())

    def test_generation_failure_happens_before_any_delete(self) -> None:
        self.write(self.source_skill / "SKILL.md", "current\n")
        self.write(self.package_skill / "SKILL.md", "old\n")
        legacy = self.package_skill / "legacy.md"
        self.write(legacy, "stale\n")
        plan = PLANNER.build_plan(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
        )

        with self.assertRaisesRegex(
            PLANNER.MigrationPlanError,
            "invalid private-term ledger",
        ):
            PLANNER.apply_plan(
                plan=plan,
                private_inventory=self.inventory,
                source_roots={"cursor-vault": self.source_root},
                package_root=self.package_root,
                privacy_ledger={"schema_version": 1},
            )

        self.assertTrue(legacy.is_file())
        self.assertEqual(
            (self.package_skill / "SKILL.md").read_text(encoding="utf-8"),
            "old\n",
        )


if __name__ == "__main__":
    unittest.main()
