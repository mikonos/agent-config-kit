from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "install" / "scripts"))
import configctl  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "build_adapters",
    REPO / "scripts" / "build_adapters.py",
)
assert SPEC and SPEC.loader
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class RuleProfileTests(unittest.TestCase):
    def manifest(self) -> dict:
        return json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))

    def test_render_generates_three_rule_profiles_for_three_runtimes(self) -> None:
        manifest = self.manifest()
        rendered = BUILD.render()
        expected_rules = {
            REPO / rule["source"]
            for runtime in manifest["runtimes"].values()
            for rule in runtime["rules_by_profile"].values()
        }

        self.assertEqual(len(expected_rules), 9)
        self.assertTrue(expected_rules.issubset(rendered))
        self.assertEqual(len(rendered), 18)

    def test_generated_rule_profiles_preserve_expected_layers(self) -> None:
        manifest = self.manifest()
        for runtime in manifest["runtimes"].values():
            daily = (
                REPO
                / runtime["rules_by_profile"]["daily-work"]["source"]
            ).read_text(encoding="utf-8")
            knowledge = (
                REPO
                / runtime["rules_by_profile"]["knowledge-vault"]["source"]
            ).read_text(encoding="utf-8")
            full = (
                REPO
                / runtime["rules_by_profile"]["full"]["source"]
            ).read_text(encoding="utf-8")

            for text in (daily, knowledge, full):
                self.assertIn("老板", text)
                self.assertIn("最强大脑", text)
                self.assertIn("授权矩阵", text)
                self.assertNotIn("/Users/", text)
                self.assertNotIn("\u6600\u5ce4", text)
            self.assertNotIn("Knowledge Vault working contract", daily)
            self.assertIn("Knowledge Vault working contract", knowledge)
            self.assertNotIn("Unknown Management Gate", knowledge)
            self.assertIn("Unknown Management Gate", full)
            self.assertIn("Document Restraint", full)

    def test_manifest_rejects_rule_target_drift_between_profiles(self) -> None:
        manifest = self.manifest()
        manifest["runtimes"]["codex"]["rules_by_profile"]["daily-work"][
            "target"
        ] = "OTHER.md"

        with self.assertRaisesRegex(
            configctl.ConfigError,
            "targets must stay constant",
        ):
            configctl.validate_package(manifest)

    def test_manifest_rejects_duplicate_profile_adapter_source(self) -> None:
        manifest = self.manifest()
        manifest["runtimes"]["codex"]["rules_by_profile"]["daily-work"][
            "source"
        ] = manifest["runtimes"]["codex"]["rules_by_profile"]["full"]["source"]

        with self.assertRaisesRegex(
            configctl.ConfigError,
            "sources must be unique",
        ):
            configctl.validate_package(manifest)

    def test_manifest_rejects_rule_source_outside_canonical_directory(self) -> None:
        manifest = copy.deepcopy(self.manifest())
        manifest["profiles"]["daily-work"]["rule_sources"] = [
            "packs/core/START-HERE.md"
        ]

        with self.assertRaisesRegex(
            configctl.ConfigError,
            "outside the canonical directory",
        ):
            configctl.validate_package(manifest)


if __name__ == "__main__":
    unittest.main()
