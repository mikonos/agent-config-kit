from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLANNER_SPEC = importlib.util.spec_from_file_location(
    "plan_portable_migration",
    REPO / "scripts" / "plan_portable_migration.py",
)
assert PLANNER_SPEC and PLANNER_SPEC.loader
PLANNER = importlib.util.module_from_spec(PLANNER_SPEC)
sys.modules["plan_portable_migration"] = PLANNER
PLANNER_SPEC.loader.exec_module(PLANNER)

REFRESH_SPEC = importlib.util.spec_from_file_location(
    "refresh_portable_derivatives",
    REPO / "scripts" / "refresh_portable_derivatives.py",
)
assert REFRESH_SPEC and REFRESH_SPEC.loader
REFRESH = importlib.util.module_from_spec(REFRESH_SPEC)
REFRESH_SPEC.loader.exec_module(REFRESH)


class RefreshPortableDerivativesTests(unittest.TestCase):
    def test_refresh_rejects_unapplied_replacement(self) -> None:
        plan = {
            "operations": {
                "add": [],
                "replace": [{"packaged_path": "packs/core/skills/demo/SKILL.md"}],
                "delete": [],
                "mode": [],
                "preserve_derivative": [],
                "register_derivative": [],
            },
            "omissions": [],
        }

        with self.assertRaisesRegex(
            REFRESH.RefreshError,
            "not the deterministic migration output",
        ):
            REFRESH.refresh(
                plan=plan,
                current_catalog={"schema_version": 1, "patches": []},
            )

    def test_refresh_registers_only_proven_output_without_public_paths(self) -> None:
        operation = {
            "skill": "demo",
            "source_path": "SKILL.md",
            "packaged_path": "packs/core/skills/demo/SKILL.md",
            "source_sha256": "a" * 64,
            "packaged_sha256": "b" * 64,
            "expected_packaged_sha256": "b" * 64,
        }
        omission = {
            "description": "Exclude source-side test metadata.",
            "reason": "test_metadata",
            "skill": "demo",
            "source_path": "test-prompts.json",
            "source_sha256": "c" * 64,
            "source_type": "file",
        }
        plan = {
            "operations": {
                "add": [],
                "replace": [],
                "delete": [],
                "mode": [],
                "preserve_derivative": [],
                "register_derivative": [operation],
            },
            "omissions": [omission],
        }

        snapshot, public_catalog, private_catalog = REFRESH.refresh(
            plan=plan,
            current_catalog={"schema_version": 1, "patches": []},
        )

        self.assertNotIn("source_path", public_catalog["patches"][0])
        self.assertEqual(public_catalog["omissions"], [])
        self.assertEqual(public_catalog["omission_summary"]["total"], 1)
        self.assertEqual(private_catalog["omissions"], [omission])
        self.assertEqual(
            snapshot["imports"]["maintainer-current-portable"]["files"],
            [{"sha256": "a" * 64}],
        )

    def test_refresh_registers_private_reviewed_manual_derivative(self) -> None:
        operation = {
            "description": "Safety-reviewed clean rewrite.",
            "skill": "demo",
            "source_path": "SKILL.md",
            "packaged_path": "packs/core/skills/demo/SKILL.md",
            "source_sha256": "a" * 64,
            "packaged_sha256": "b" * 64,
            "reviewed_manual": True,
        }
        plan = {
            "operations": {
                "add": [],
                "replace": [],
                "delete": [],
                "mode": [],
                "preserve_derivative": [],
                "preserve_reviewed_derivative": [operation],
                "register_derivative": [],
                "register_generated": [],
            },
            "omissions": [],
        }

        _, public_catalog, _ = REFRESH.refresh(
            plan=plan,
            current_catalog={"schema_version": 1, "patches": []},
        )

        self.assertEqual(
            public_catalog["patches"][0]["transformation"],
            "reviewed_manual_portable_derivative",
        )


if __name__ == "__main__":
    unittest.main()
