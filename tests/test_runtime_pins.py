from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "resolve_runtime_pins",
    REPO / "scripts" / "resolve_runtime_pins.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RuntimePinTests(unittest.TestCase):
    def test_only_matching_tree_hash_receives_commit_pin(self) -> None:
        commit = "c" * 40
        catalog = {
            "skills": [
                {
                    "name": "match",
                    "source_url": "https://github.com/owner/repo",
                    "skill_path": "skills/match/SKILL.md",
                    "tree_sha": "a" * 40,
                },
                {
                    "name": "changed",
                    "source_url": "https://github.com/owner/repo",
                    "skill_path": "skills/changed/SKILL.md",
                    "tree_sha": "b" * 40,
                },
                {
                    "name": "live",
                    "source_url": "https://example.com/live/SKILL.md",
                    "skill_path": None,
                    "tree_sha": None,
                },
                {
                    "name": "root",
                    "source_url": "https://github.com/owner/repo",
                    "skill_path": "SKILL.md",
                    "tree_sha": "e" * 40,
                },
            ]
        }

        def loader(url: str) -> dict:
            if url == "https://api.github.com/repos/owner/repo":
                return {
                    "default_branch": "main",
                    "license": {"spdx_id": "MIT"},
                }
            if url.endswith("/commits/main"):
                return {"sha": commit}
            return {
                "truncated": False,
                "sha": "e" * 40,
                "tree": [
                    {"path": "skills/match", "type": "tree", "sha": "a" * 40},
                    {"path": "skills/changed", "type": "tree", "sha": "d" * 40},
                ],
            }

        result = MODULE.resolve_catalog(catalog, loader)
        by_name = {entry["name"]: entry for entry in result["skills"]}
        self.assertEqual(by_name["match"]["status"], "exact_current")
        self.assertEqual(by_name["match"]["commit"], commit)
        self.assertEqual(by_name["changed"]["status"], "current_tree_mismatch")
        self.assertIsNone(by_name["changed"]["commit"])
        self.assertEqual(by_name["live"]["status"], "live_origin_unpinned")
        self.assertEqual(by_name["root"]["status"], "exact_current")
        self.assertEqual(by_name["root"]["commit"], commit)
        self.assertEqual(
            result["repositories"]["owner/repo"]["repository_license_spdx"],
            "MIT",
        )


if __name__ == "__main__":
    unittest.main()
