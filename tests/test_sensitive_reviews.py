from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_sensitive_reviews",
    REPO / "scripts" / "check_sensitive_reviews.py",
)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class SensitiveReviewTests(unittest.TestCase):
    def test_current_public_tree_has_no_unresolved_match(self) -> None:
        result = CHECKER.verify(
            REPO,
            json.loads(
                (REPO / "catalog" / "sensitive_reviews.json").read_text(
                    encoding="utf-8"
                )
            ),
        )
        self.assertEqual(result, (0, 2))

    def test_unreviewed_candidate_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "packs" / "demo" / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "A long Musk-" + "research-slug-" * 3,
                encoding="utf-8",
            )
            with self.assertRaisesRegex(CHECKER.ReviewError, "unresolved"):
                CHECKER.verify(
                    root,
                    {
                        "schema_version": 1,
                        "reviews": [],
                    },
                )


if __name__ == "__main__":
    unittest.main()
