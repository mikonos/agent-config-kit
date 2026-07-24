from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_private_inventory",
    REPO / "scripts" / "build_private_inventory.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PrivateInventoryTests(unittest.TestCase):
    def test_builds_one_record_per_unique_name_and_preserves_decisions(self) -> None:
        audit = {
            "schema_version": 1,
            "sensitivity": "private_intake",
            "entry_mode": "top-level",
            "entries": [
                {
                    "name": "demo",
                    "source": "codex-global",
                    "path": "demo/SKILL.md",
                    "content_sha256": "a" * 64,
                    "technical_status": "review",
                    "blockers": [],
                    "reviews": [{"code": "missing_license_evidence"}],
                    "dependencies": {"commands": ["git"], "environment": []},
                    "side_effects": [],
                },
                {
                    "name": "demo",
                    "source": "cursor-vault",
                    "path": "demo/SKILL.md",
                    "content_sha256": "b" * 64,
                    "technical_status": "blocked",
                    "blockers": [{"code": "macos_home_path"}],
                    "reviews": [],
                    "dependencies": {"commands": [], "environment": ["TOKEN"]},
                    "side_effects": ["external_message"],
                },
            ],
        }
        admissions = {
            "provenance_groups": {
                "fixture": {
                    "origin": "https://example.com/repo",
                    "license": "MIT",
                }
            },
            "skills": {"demo": "fixture"},
        }
        manifest = {
            "profiles": {"daily-work": {"skill_packs": ["daily"]}},
            "skill_packs": {"daily": ["demo"]},
        }
        previous = {
            "skills": {
                "demo": {
                    "decision": {
                        "os_requirements": ["macOS"],
                        "notes": "keep",
                    }
                }
            }
        }
        result = MODULE.build_ledger(audit, admissions, manifest, previous)
        record = result["skills"]["demo"]
        self.assertEqual(record["selected_source"], "cursor-vault")
        self.assertEqual(record["duplicate_candidates"], 2)
        self.assertEqual(record["disposition"]["status"], "bundled")
        self.assertEqual(record["disposition"]["license"], "MIT")
        self.assertEqual(record["disposition"]["os_requirements"], ["macOS"])
        self.assertEqual(record["disposition"]["notes"], "keep")
        self.assertEqual(result["summary"]["unique_top_level_skills"], 1)
        self.assertEqual(result["summary"]["duplicate_names"], 1)

    def test_rejects_public_or_recursive_audit(self) -> None:
        for sensitivity, entry_mode in (
            ("public_summary", "top-level"),
            ("private_intake", "recursive"),
        ):
            with self.assertRaises(MODULE.InventoryError):
                MODULE.selected_entries(
                    {
                        "schema_version": 1,
                        "sensitivity": sensitivity,
                        "entry_mode": entry_mode,
                        "entries": [],
                    }
                )

    def test_marks_approved_external_skill_as_fetch_from_origin(self) -> None:
        audit = {
            "schema_version": 1,
            "sensitivity": "private_intake",
            "entry_mode": "top-level",
            "entries": [
                {
                    "name": "official-demo",
                    "source": "agents-global",
                    "path": "official-demo/SKILL.md",
                    "content_sha256": "a" * 64,
                    "technical_status": "review",
                    "blockers": [],
                    "reviews": [],
                    "dependencies": {"commands": [], "environment": []},
                    "side_effects": [],
                }
            ],
        }
        admissions = {"provenance_groups": {}, "skills": {}}
        manifest = {
            "profiles": {"daily-work": {"skill_packs": []}},
            "skill_packs": {},
        }
        external = {
            "schema_version": 1,
            "packs": {
                "official": {
                    "skills": [
                        {
                            "name": "official-demo",
                            "url": (
                                "https://official.example/.well-known/skills/"
                                "official-demo/SKILL.md"
                            ),
                        }
                    ]
                }
            },
        }
        result = MODULE.build_ledger(
            audit,
            admissions,
            manifest,
            external=external,
        )
        disposition = result["skills"]["official-demo"]["disposition"]
        self.assertEqual(disposition["status"], "fetch_from_origin")
        self.assertEqual(disposition["delivery"], "fetch_from_origin")
        self.assertEqual(disposition["category"], "official")
        self.assertEqual(result["summary"]["fetch_from_origin"], 1)

    def test_manual_legal_block_overrides_review_status(self) -> None:
        audit = {
            "schema_version": 1,
            "sensitivity": "private_intake",
            "entry_mode": "top-level",
            "entries": [
                {
                    "name": "restricted",
                    "source": "agents-global",
                    "path": "restricted/SKILL.md",
                    "content_sha256": "a" * 64,
                    "technical_status": "review",
                    "blockers": [],
                    "reviews": [{"code": "side_effect_review"}],
                    "dependencies": {"commands": [], "environment": []},
                    "side_effects": [],
                }
            ],
        }
        previous = {
            "skills": {
                "restricted": {
                    "decision": {
                        "status": "blocked",
                        "os_requirements": [],
                        "notes": "Upstream license prohibits redistribution.",
                    }
                }
            }
        }
        result = MODULE.build_ledger(
            audit,
            {"provenance_groups": {}, "skills": {}},
            {
                "profiles": {"daily-work": {"skill_packs": []}},
                "skill_packs": {},
            },
            previous=previous,
        )
        record = result["skills"]["restricted"]
        self.assertEqual(record["decision"]["status"], "blocked")
        self.assertEqual(record["disposition"]["status"], "blocked")
        self.assertEqual(result["summary"]["blocked"], 1)


if __name__ == "__main__":
    unittest.main()
