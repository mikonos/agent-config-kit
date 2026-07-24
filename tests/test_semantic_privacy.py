from __future__ import annotations

import hashlib
import importlib.util
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
            for index in range(3, 6)
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


if __name__ == "__main__":
    unittest.main()
