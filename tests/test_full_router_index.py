from __future__ import annotations

import importlib.util
import json
import posixpath
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_full_router_index",
    REPO / "scripts" / "build_full_router_index.py",
)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class FullRouterIndexTests(unittest.TestCase):
    def test_current_index_matches_every_non_router_full_skill(self) -> None:
        expected = BUILDER.build_index(REPO)
        actual = json.loads(BUILDER.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(actual, expected)
        self.assertEqual(actual["summary"]["indexed_skills"], 287)
        self.assertEqual(actual["summary"]["path_base"], "router_skill_dir")
        self.assertNotIn(
            BUILDER.ROUTER_NAME,
            {record["name"] for record in actual["skills"]},
        )
        for skills_root in (".agents/skills", ".cursor/skills", ".claude/skills"):
            router_dir = f"{skills_root}/{BUILDER.ROUTER_NAME}"
            for record in actual["skills"]:
                resolved = posixpath.normpath(
                    f"{router_dir}/{record['sibling_skill_path']}"
                )
                self.assertEqual(
                    resolved,
                    f"{skills_root}/{record['name']}/SKILL.md",
                )

    def test_core_rule_explicitly_routes_large_catalog(self) -> None:
        rule = (REPO / "packs" / "core" / "rules" / "core.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("all-skills-router", rule)
        self.assertIn("initial Skill list", rule)

    def test_router_forbids_loading_the_whole_index(self) -> None:
        router = (
            REPO
            / "packs"
            / "full-routing"
            / "skills"
            / BUILDER.ROUTER_NAME
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(router.split())
        self.assertIn("Do not load or print the entire index", normalized)
        self.assertIn("at most five matching records", normalized)

    def test_router_and_public_catalog_cover_the_same_work_skills(self) -> None:
        router = json.loads(BUILDER.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        catalog = json.loads(
            (REPO / "catalog" / "skill_catalog.json").read_text(encoding="utf-8")
        )
        router_names = {record["name"] for record in router["skills"]}
        self.assertEqual(
            router_names,
            set(catalog["skills"]) - {BUILDER.ROUTER_NAME},
        )
        self.assertTrue(
            all(record["description"].strip() for record in router["skills"])
        )


if __name__ == "__main__":
    unittest.main()
