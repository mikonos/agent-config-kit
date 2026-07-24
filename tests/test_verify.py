from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify", REPO / "scripts" / "verify.py")
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_recovery_artifact_detection_does_not_reject_skill_names(self) -> None:
        self.assertTrue(VERIFY.is_recovery_artifact("archive-20260723"))
        self.assertTrue(VERIFY.is_recovery_artifact("notes.bak-20260723"))
        self.assertFalse(VERIFY.is_recovery_artifact("openspec-archive-change"))

    def test_dependency_and_cache_directory_detection_is_exact(self) -> None:
        self.assertTrue(VERIFY.is_excluded_artifact_dir(Path("/tmp/example/.venv")))
        self.assertTrue(
            VERIFY.is_excluded_artifact_dir(Path("/tmp/example/node_modules"))
        )
        self.assertFalse(VERIFY.is_excluded_artifact_dir(Path("/tmp/example/vendor.md")))


if __name__ == "__main__":
    unittest.main()
