from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_semantic_privacy",
    REPO / "scripts" / "check_semantic_privacy.py",
)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def hashed(value: str) -> str:
    return hashlib.sha256(value.casefold().encode("utf-8")).hexdigest()


class SemanticPrivacyTests(unittest.TestCase):
    def ledger(self) -> dict:
        filler = [
            {
                "id": f"private_term_{index:03d}",
                "length": len(f"unused{index}"),
                "matcher": "ascii_token",
                "sha256": hashed(f"unused{index}"),
            }
            for index in range(3, 8)
        ]
        return {
            "schema_version": 1,
            "terms": [
                {
                    "id": "private_term_001",
                    "length": 11,
                    "matcher": "ascii_token",
                    "sha256": hashed("PrivateName"),
                },
                {
                    "id": "private_term_002",
                    "length": 4,
                    "matcher": "cjk_substring",
                    "sha256": hashed("私密项目"),
                },
                *filler,
            ],
        }

    def inventory(self) -> dict:
        return {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "portable_reference_aliases": {
                "private-suite/": "public-suite/",
                "_" + "preamble/": "vault-writing-preamble/",
            },
            "skills": {
                "demo": {
                    "portable_aliases": {
                        "PrivateName": "public-name",
                        "_" + "preamble": "vault-writing-preamble",
                    }
                }
            },
        }

    def test_finds_ascii_and_cjk_terms_without_reporting_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sample.md").write_text(
                "Use PrivateName for 私密项目。\n",
                encoding="utf-8",
            )
            problems = CHECKER.verify(root, self.ledger())
            self.assertEqual(
                problems,
                [
                    "private_term_001: sample.md:1",
                    "private_term_002: sample.md:1",
                ],
            )
            encoded = "\n".join(problems)
            self.assertNotIn("PrivateName", encoded)
            self.assertNotIn("私密项目", encoded)

    def test_scans_paths_and_ignores_private_workbench(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            public = root / "PrivateName" / "SKILL.md"
            public.parent.mkdir()
            public.write_text("safe\n", encoding="utf-8")
            ignored = root / ".agent-config-kit-workbench" / "private.md"
            ignored.parent.mkdir()
            ignored.write_text("PrivateName 私密项目\n", encoding="utf-8")
            problems = CHECKER.verify(root, self.ledger())
            self.assertEqual(len(problems), 1)
            self.assertIn("private_term_001: path_sha256=", problems[0])
            self.assertNotIn("PrivateName", problems[0])

    def test_rejects_missing_or_duplicate_terms(self) -> None:
        missing = self.ledger()
        missing["terms"].pop()
        with self.assertRaisesRegex(
            CHECKER.PrivacyError,
            "term set is incomplete or unexpected",
        ):
            CHECKER.load_terms(missing)

        ledger = self.ledger()
        ledger["terms"].append(dict(ledger["terms"][0]))
        with self.assertRaisesRegex(CHECKER.PrivacyError, "invalid semantic privacy term"):
            CHECKER.load_terms(ledger)

    def test_finds_ascii_term_inside_compound_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sample.md").write_text(
                "prefixPrivateNameSuffix\n",
                encoding="utf-8",
            )
            problems = CHECKER.verify(root, self.ledger())
            self.assertEqual(problems, ["private_term_001: sample.md:1"])

    def test_private_aliases_are_scanned_without_reporting_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sample.md").write_text(
                "See private-suite/README and _" + "preamble/SKILL.md.\n"
                "Use `" + "_" + "preamble` before writing.\n",
                encoding="utf-8",
            )
            problems = CHECKER.verify(
                root,
                self.ledger(),
                private_inventory=self.inventory(),
            )
            self.assertEqual(len(problems), 4)
            encoded = "\n".join(problems)
            self.assertIn("private_alias_", encoded)
            self.assertNotIn("private-suite", encoded)
            self.assertNotIn("_" + "preamble", encoded)

    def test_generic_preamble_helper_name_is_not_a_private_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "add_zk_preamble.py").write_text(
                "def has_preamble():\n    return True\n",
                encoding="utf-8",
            )
            problems = CHECKER.verify(
                root,
                self.ledger(),
                private_inventory=self.inventory(),
            )
            self.assertEqual(problems, [])

    def test_private_alias_inside_compound_identifier_is_rejected(self) -> None:
        inventory = self.inventory()
        inventory["portable_reference_aliases"]["secretbrand"] = "public-brand"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "sample.md").write_text(
                "prefixSecretBrandSuffix\n",
                encoding="utf-8",
            )
            problems = CHECKER.verify(
                root,
                self.ledger(),
                private_inventory=inventory,
            )
            self.assertEqual(len(problems), 1)
            self.assertIn("private_alias_", problems[0])

    def test_public_binary_catalog_cannot_replace_private_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = root / "catalog"
            catalog.mkdir()
            public = {
                "schema_version": 1,
                "assets": [
                    {
                        "description": "Public asset",
                        "path": "packs/demo.png",
                        "sha256": "a" * 64,
                    }
                ],
            }
            private = {
                "schema_version": 1,
                "sensitivity": "private_do_not_publish",
                "assets": [{"path": "packs/demo.png", "sha256": "b" * 64}],
            }
            (catalog / "binary_assets.json").write_text(
                json.dumps(public),
                encoding="utf-8",
            )
            problems = CHECKER.verify(
                root,
                self.ledger(),
                reviewed_binary_assets=private,
            )
            self.assertEqual(
                problems,
                ["binary_asset_approval: catalog differs from private review"],
            )

    def test_public_privacy_policy_contains_no_term_digest(self) -> None:
        path = REPO / "catalog" / "private_term_hashes.json"
        policy = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(policy["private_ledger_required"])
        self.assertNotIn("terms", policy)
        self.assertIsNone(re.search(r"[0-9a-f]{64}", path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
