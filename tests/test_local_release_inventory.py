from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_module(
    "build_local_release_inventory",
    "scripts/build_local_release_inventory.py",
)
CHECKER = load_module(
    "check_local_release_inventory",
    "scripts/check_local_release_inventory.py",
)


class LocalReleaseInventoryTests(unittest.TestCase):
    def test_current_public_inventory_is_complete(self) -> None:
        summary = CHECKER.verify_inventory(
            json.loads(
                (REPO / "catalog" / "local_release_inventory.json").read_text(
                    encoding="utf-8"
                )
            ),
            json.loads((REPO / "manifest.json").read_text(encoding="utf-8")),
            json.loads(
                (REPO / "catalog" / "external_skills.json").read_text(
                    encoding="utf-8"
                )
            ),
        )
        self.assertEqual(summary["raw_source_entry_count"], 443)
        self.assertEqual(summary["raw_source_unique_count"], 398)
        self.assertEqual(summary["raw_duplicate_names"], 43)
        self.assertEqual(summary["top_level_unique_count"], 363)
        self.assertEqual(summary["nested_only_unique_count"], 30)
        self.assertEqual(summary["platform_builtin_only_unique_count"], 5)
        self.assertEqual(summary["public_bundled_total"], 288)
        self.assertEqual(summary["redacted_private_projects"], 42)

    def test_builder_resolves_bundled_external_blocked_and_manual_entries(self) -> None:
        source = {
            "schema_version": 1,
            "skills": {
                "advisory-board": {
                    "disposition": {"status": "review"},
                    "selected_path": "private/path",
                },
                "example-private": {
                    "blocker_codes": ["private_term_1"],
                    "disposition": {"status": "blocked"},
                    "selected_path": "private/path",
                },
                "local-safe": {"disposition": {"status": "review"}},
                "official-safe": {"disposition": {"status": "review"}},
            },
        }
        manifest = {
            "schema_version": 1,
            "skill_packs": {"safe": ["local-safe"]},
        }
        external = {
            "schema_version": 1,
            "packs": {
                "official": {
                    "skills": [{"name": "official-safe"}],
                }
            },
        }
        result = BUILDER.build_inventory(source, manifest, external)
        self.assertEqual(result["skills"]["local-safe"]["delivery"], "bundled")
        self.assertEqual(
            result["skills"]["official-safe"]["delivery"],
            "fetch_from_origin",
        )
        self.assertNotIn("example-private", result["skills"])
        self.assertEqual(
            result["skills"]["redacted-private-project-001"]["status"],
            "private_project",
        )
        self.assertEqual(
            result["skills"]["advisory-board"]["status"],
            "license_blocked",
        )
        serialized = json.dumps(result)
        self.assertNotIn("private/path", serialized)
        self.assertNotIn("example-private", serialized)
        CHECKER.verify_inventory(result, manifest, external)

    def test_checker_rejects_unredacted_private_project_name(self) -> None:
        inventory = {
            "schema_version": 1,
            "description": "test",
            "summary": {
                "raw_source_entry_count": 1,
                "raw_source_unique_count": 1,
                "raw_duplicate_names": 0,
                "top_level_unique_count": 1,
                "nested_only_unique_count": 0,
                "platform_builtin_only_unique_count": 0,
                "bundled_from_source_scope": 0,
                "fetch_from_origin": 0,
                "not_distributed": 1,
                "catalog_only_bundled": 0,
                "catalog_only_external": 0,
                "public_bundled_total": 0,
                "external_fetch_total": 0,
                "redacted_private_projects": 1,
            },
            "catalog_only_bundled_skills": [],
            "catalog_only_external_skills": [],
            "skills": {
                "private-name": {
                    "scope": "top_level",
                    "delivery": "not_distributed",
                    "status": "private_project",
                    "reason": "private",
                }
            },
        }
        manifest = {"schema_version": 1, "skill_packs": {}}
        external = {"schema_version": 1, "packs": {}}
        with self.assertRaisesRegex(
            CHECKER.CheckError,
            "private-project name is not redacted",
        ):
            CHECKER.verify_inventory(inventory, manifest, external)

    def test_builder_accounts_for_nested_and_platform_only_names(self) -> None:
        source = {
            "schema_version": 1,
            "skills": {
                "top": {"disposition": {"status": "review"}},
            },
        }
        manifest = {
            "schema_version": 1,
            "skill_packs": {"safe": ["top", "nested-public"]},
        }
        external = {"schema_version": 1, "packs": {}}
        scope = {
            "raw_entry_count": 4,
            "duplicate_names": 1,
            "names": {
                "top": {
                    "top_level": True,
                    "nested": False,
                    "platform_builtin": False,
                },
                "nested-public": {
                    "top_level": False,
                    "nested": True,
                    "platform_builtin": False,
                },
                "nested-private": {
                    "top_level": False,
                    "nested": True,
                    "platform_builtin": False,
                },
                "builtin": {
                    "top_level": False,
                    "nested": False,
                    "platform_builtin": True,
                },
            },
        }
        result = BUILDER.build_inventory(source, manifest, external, scope)
        self.assertEqual(result["summary"]["raw_source_unique_count"], 4)
        self.assertEqual(result["skills"]["nested-public"]["scope"], "nested_promoted")
        self.assertEqual(
            result["skills"]["nested-private"]["status"],
            "nested_component",
        )
        self.assertEqual(result["skills"]["builtin"]["status"], "platform_builtin")
        CHECKER.verify_inventory(result, manifest, external)

    def test_builder_fails_closed_on_unresolved_review(self) -> None:
        source = {
            "schema_version": 1,
            "skills": {
                "unknown-review": {
                    "disposition": {"status": "review"},
                }
            },
        }
        manifest = {"schema_version": 1, "skill_packs": {}}
        external = {"schema_version": 1, "packs": {}}
        with self.assertRaisesRegex(
            BUILDER.InventoryError,
            "needs an explicit disposition",
        ):
            BUILDER.build_inventory(source, manifest, external)


if __name__ == "__main__":
    unittest.main()
