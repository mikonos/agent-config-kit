from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "live_runtime_smoke",
    REPO / "scripts" / "live_runtime_smoke.py",
)
assert SPEC and SPEC.loader
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class LiveRuntimeSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        contract = json.loads(
            (REPO / "catalog" / "live_runtime_smoke.json").read_text(
                encoding="utf-8"
            )
        )
        self.cases = SMOKE.validate_contract(REPO, contract)

    def valid_response(self) -> dict[str, object]:
        return {
            "results": [
                {
                    "id": case["id"],
                    "skill": case["expected_skill"],
                    "evidence": list(case["source_anchors"]),
                }
                for case in self.cases
            ]
        }

    def test_current_contract_matches_packaged_skill_text(self) -> None:
        self.assertEqual(len(self.cases), 4)

    def test_expected_response_passes(self) -> None:
        SMOKE.validate_response(self.cases, self.valid_response())

    def test_wrong_skill_fails(self) -> None:
        response = self.valid_response()
        response["results"][0]["skill"] = "deep-read"
        with self.assertRaisesRegex(SMOKE.SmokeError, "expected start-here"):
            SMOKE.validate_response(self.cases, response)

    def test_missing_method_evidence_fails(self) -> None:
        response = self.valid_response()
        response["results"][1]["evidence"] = ["generic summary", "generic analysis"]
        with self.assertRaisesRegex(SMOKE.SmokeError, "selected Skill body"):
            SMOKE.validate_response(self.cases, response)


if __name__ == "__main__":
    unittest.main()
