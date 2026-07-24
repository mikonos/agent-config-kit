from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_skill_catalog",
    REPO / "scripts" / "build_skill_catalog.py",
)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class SkillCatalogTests(unittest.TestCase):
    def test_current_catalog_matches_manifest_and_admissions(self) -> None:
        expected = BUILDER.build_catalog(REPO)
        actual = json.loads(
            (REPO / "catalog" / "skill_catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual(actual, expected)
        self.assertEqual(actual["summary"]["bundled_skills"], 288)
        self.assertGreater(
            actual["summary"]["declared_connection_requirements"],
            0,
        )
        self.assertEqual(actual["skills"]["all-skills-router"]["side_effects"], [])

    def test_every_skill_has_release_decision_metadata(self) -> None:
        catalog = BUILDER.build_catalog(REPO)
        for name, record in catalog["skills"].items():
            self.assertEqual(Path(record["packaged_path"]).name, name)
            self.assertTrue(record["source"]["origin"])
            self.assertTrue(record["source"]["attribution"])
            self.assertTrue(record["source"]["license"])
            self.assertIsInstance(record["os_requirements"], list)
            self.assertIsInstance(record["dependencies"]["commands"], list)
            self.assertIsInstance(record["dependencies"]["environment"], list)
            self.assertIsInstance(record["dependencies"]["connections"], list)
            self.assertIsInstance(record["side_effects"], list)
            self.assertIsInstance(record["default_install"], bool)


if __name__ == "__main__":
    unittest.main()
