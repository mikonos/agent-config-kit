from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_source_alignment",
    REPO / "scripts" / "check_source_alignment.py",
)
assert SPEC and SPEC.loader
ALIGNMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ALIGNMENT)


class SourceAlignmentTests(unittest.TestCase):
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

    def check(
        self,
        patches: list[dict[str, str]] | None = None,
        omissions: list[dict[str, str]] | None = None,
        reviewed: dict | None = None,
    ):
        return ALIGNMENT.check_alignment(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={"cursor-vault": self.source_root},
            package_root=self.package_root,
            portable_patches={
                "schema_version": 1,
                "patches": patches or [],
                "omissions": omissions or [],
            },
            private_reviewed_derivatives=reviewed,
        )

    def portable_patch(self) -> dict[str, str]:
        source_file = self.source_skill / "SKILL.md"
        packaged_file = self.package_skill / "SKILL.md"
        return {
            "description": "Replace a private path with a project-relative path.",
            "packaged_path": packaged_file.relative_to(
                self.package_root
            ).as_posix(),
            "packaged_sha256": ALIGNMENT.sha256_file(packaged_file),
            "source_path": "demo/SKILL.md",
            "source_sha256": ALIGNMENT.sha256_file(source_file),
            "upstream_commit": "a" * 40,
            "upstream_origin": "https://example.invalid/test-fixture",
        }

    def test_exact_skill_tree_is_release_ready(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")

        report = self.check()

        self.assertEqual(report["counts"]["exact"], 1)
        self.assertTrue(report["release_ready"])

    def test_private_source_name_can_align_to_public_package_name(self) -> None:
        public_dir = (
            self.package_root
            / "packs"
            / "core"
            / "skills"
            / "public-demo"
        )
        self.package_skill.rmdir()
        self.package_skill = public_dir
        self.package_skill.mkdir(parents=True)
        self.inventory["skills"]["demo"]["public_name"] = "public-demo"
        self.manifest["skill_packs"]["core"] = ["public-demo"]
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")

        report = self.check()

        self.assertEqual(report["counts"]["exact"], 1)
        self.assertTrue(report["release_ready"])

    def test_private_alias_can_portabilize_support_file_path(self) -> None:
        public_dir = (
            self.package_root
            / "packs"
            / "core"
            / "skills"
            / "public-demo"
        )
        self.package_skill.rmdir()
        self.package_skill = public_dir
        self.package_skill.mkdir(parents=True)
        self.inventory["skills"]["demo"]["public_name"] = "public-demo"
        self.inventory["skills"]["demo"]["portable_aliases"] = {
            "demo": "public-demo"
        }
        self.manifest["skill_packs"]["core"] = ["public-demo"]
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(
            self.source_skill / "references" / "demo-guide.md",
            "same\n",
        )
        self.write(self.package_skill / "SKILL.md", "same\n")
        self.write(
            self.package_skill / "references" / "public-demo-guide.md",
            "same\n",
        )

        report = self.check()

        self.assertEqual(report["counts"]["portable_derivative"], 1)
        self.assertTrue(report["release_ready"])

    def test_shared_reference_alias_aligns_support_file_path(self) -> None:
        self.inventory["portable_reference_aliases"] = {
            "private-suite/": "public-suite/",
        }
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        self.write(
            self.source_skill / "references" / "private-suite" / "guide.md",
            "same\n",
        )
        self.write(
            self.package_skill / "references" / "public-suite" / "guide.md",
            "same\n",
        )

        report = self.check()

        self.assertEqual(report["counts"]["portable_derivative"], 1)
        self.assertTrue(report["release_ready"])

    def test_registered_portable_derivative_is_release_ready(self) -> None:
        self.write(self.source_skill / "SKILL.md", "private path\n")
        self.write(self.package_skill / "SKILL.md", "portable path\n")
        patch = self.portable_patch()

        report = self.check([patch])

        self.assertEqual(report["counts"]["portable_derivative"], 1)
        self.assertTrue(report["release_ready"])

    def test_manual_derivative_requires_exact_private_approval(self) -> None:
        self.write(self.source_skill / "SKILL.md", "unsafe source\n")
        self.write(self.package_skill / "SKILL.md", "safe reviewed rewrite\n")
        patch = self.portable_patch()
        patch.pop("source_path")
        patch.pop("upstream_commit")
        patch["source_snapshot"] = "catalog/maintainer_source_snapshot.json"
        patch["transformation"] = "reviewed_manual_portable_derivative"
        reviewed = {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "derivatives": [
                {
                    "description": "Safety-reviewed clean rewrite.",
                    "source_skill": "demo",
                    "source_path": "SKILL.md",
                    "packaged_path": patch["packaged_path"],
                    "source_sha256": patch["source_sha256"],
                    "packaged_sha256": patch["packaged_sha256"],
                }
            ],
        }

        approved = self.check([patch], reviewed=reviewed)
        unapproved = self.check([patch])

        self.assertTrue(approved["release_ready"])
        self.assertFalse(unapproved["release_ready"])
        self.assertTrue(
            any(
                "reviewed derivative lacks exact private approval" in problem
                for problem in unapproved["problems"]
            )
        )

    def test_same_name_upstream_version_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "maintainer version\n")
        self.write(self.package_skill / "SKILL.md", "upstream version\n")

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn("unregistered content difference", report["problems"][0])

    def test_missing_or_extra_support_file_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        self.write(self.source_skill / "references" / "source-only.md", "source\n")
        self.write(self.package_skill / "references" / "package-only.md", "package\n")

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertTrue(
            any("file set differs" in problem for problem in report["problems"])
        )

    def test_registered_source_omission_is_portable_derivative(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        omitted = self.source_skill / "test-prompts.json"
        self.write(omitted, "{}\n")
        omission = {
            "description": "Exclude source-side evaluation metadata from runtime delivery.",
            "reason": "test_metadata",
            "skill": "demo",
            "source_path": "test-prompts.json",
            "source_sha256": ALIGNMENT.sha256_file(omitted),
            "source_snapshot": "catalog/maintainer_source_snapshot.json",
            "upstream_origin": "this-repository",
        }

        report = self.check(omissions=[omission])

        self.assertEqual(report["counts"]["portable_derivative"], 1)
        self.assertTrue(report["release_ready"])

    def test_registered_directory_omission_skips_links_inside_cache(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        cache = self.source_skill / ".venv"
        self.write(cache / "data.txt", "cache\n")
        (cache / "python").symlink_to("missing-python")
        omission = {
            "description": "Exclude a source-side dependency directory.",
            "reason": "dependency_cache",
            "skill": "demo",
            "source_path": ".venv",
            "source_sha256": ALIGNMENT.sha256_tree(cache),
            "source_snapshot": "catalog/maintainer_source_snapshot.json",
            "source_type": "directory",
            "upstream_origin": "this-repository",
        }

        report = self.check(omissions=[omission])

        self.assertEqual(report["counts"]["portable_derivative"], 1)
        self.assertTrue(report["release_ready"])

    def test_stale_source_omission_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        omitted = self.source_skill / "test-prompts.json"
        self.write(omitted, "{}\n")
        omission = {
            "description": "Exclude source-side evaluation metadata from runtime delivery.",
            "reason": "test_metadata",
            "skill": "demo",
            "source_path": "test-prompts.json",
            "source_sha256": "0" * 64,
            "source_snapshot": "catalog/maintainer_source_snapshot.json",
            "upstream_origin": "this-repository",
        }

        report = self.check(omissions=[omission])

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo/test-prompts.json: portable omission digest does not match source",
            report["problems"],
        )

    def test_review_item_blocks_release(self) -> None:
        self.inventory["skills"]["demo"]["disposition"]["status"] = "review"

        report = self.check()

        self.assertEqual(report["counts"]["review"], 1)
        self.assertFalse(report["release_ready"])

    def test_catalog_only_skill_blocks_release(self) -> None:
        self.manifest["skill_packs"]["core"].append("catalog-only")

        report = self.check()

        self.assertEqual(report["counts"]["catalog_only"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "catalog-only: packaged Skill is missing from private inventory",
            report["problems"],
        )

    def test_explicit_private_kit_snapshot_is_release_ready(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        self.manifest["skill_packs"]["core"].append("kit-extra")
        extra = self.package_root / "packs" / "core" / "skills" / "kit-extra"
        self.write(extra / "SKILL.md", "---\nname: kit-extra\n---\n")
        self.inventory["catalog_only_skills"] = ["kit-extra"]

        report = self.check()

        self.assertEqual(report["counts"]["kit_snapshot"], 1)
        self.assertTrue(report["release_ready"])

    def test_blocked_skill_still_in_manifest_blocks_release(self) -> None:
        self.inventory["skills"]["demo"]["disposition"]["status"] = "blocked"

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo: blocked Skill is still present in manifest",
            report["problems"],
        )

    def test_external_skill_still_in_manifest_blocks_release(self) -> None:
        self.inventory["skills"]["demo"]["disposition"]["status"] = "fetch_from_origin"

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo: external Skill is still present in manifest",
            report["problems"],
        )

    def test_new_live_source_missing_from_inventory_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        self.write(
            self.source_root / "new-skill" / "SKILL.md",
            "---\nname: new-skill\ndescription: New live source.\n---\n",
        )

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "new-skill: live source is missing from private inventory",
            report["problems"],
        )

    def test_higher_priority_duplicate_makes_stale_inventory_fail(self) -> None:
        agents_root = self.root / "agents"
        self.write(self.source_skill / "SKILL.md", "cursor version\n")
        self.write(agents_root / "demo" / "SKILL.md", "agents version\n")
        self.write(self.package_skill / "SKILL.md", "agents version\n")
        self.inventory["skills"]["demo"]["selected_source"] = "agents-global"

        report = ALIGNMENT.check_alignment(
            private_inventory=self.inventory,
            manifest=self.manifest,
            source_roots={
                "cursor-vault": self.source_root,
                "agents-global": agents_root,
            },
            package_root=self.package_root,
            portable_patches={"schema_version": 1, "patches": []},
        )

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo: selected source is stale expected=cursor-vault actual=agents-global",
            report["problems"],
        )

    def test_duplicate_name_inside_selected_source_root_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "---\nname: demo\n---\nsame\n")
        self.write(
            self.source_root / "old-demo" / "SKILL.md",
            "---\nname: demo\n---\nold\n",
        )
        self.write(self.package_skill / "SKILL.md", "---\nname: demo\n---\nsame\n")

        report = self.check()

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo: selected source name is ambiguous within cursor-vault",
            report["problems"],
        )

    def test_portable_patch_with_wrong_source_path_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "private path\n")
        self.write(self.package_skill / "SKILL.md", "portable path\n")
        patch = self.portable_patch()
        patch["source_path"] = "another-skill/SKILL.md"

        report = self.check([patch])

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo/SKILL.md: portable patch source_path does not match selected Skill",
            report["problems"],
        )

    def test_portable_patch_without_source_anchor_blocks_release(self) -> None:
        self.write(self.source_skill / "SKILL.md", "private path\n")
        self.write(self.package_skill / "SKILL.md", "portable path\n")
        patch = self.portable_patch()
        patch.pop("upstream_commit")

        report = self.check([patch])

        self.assertEqual(report["counts"]["unexplained"], 1)
        self.assertFalse(report["release_ready"])
        self.assertIn(
            "demo/SKILL.md: portable patch needs exactly one source anchor",
            report["problems"],
        )

    def test_cli_report_never_serializes_source_root(self) -> None:
        self.write(self.source_skill / "SKILL.md", "same\n")
        self.write(self.package_skill / "SKILL.md", "same\n")
        report = self.check()

        serialized = json.dumps(report)
        self.assertNotIn(str(self.source_root), serialized)


if __name__ == "__main__":
    unittest.main()
