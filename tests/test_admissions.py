from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "scripts" / "check_admissions.py"


class AdmissionTests(unittest.TestCase):
    def run_check(self, root: Path, expected: int = 0, require_full: bool = False) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(CHECKER), "--root", str(root)]
        if require_full:
            command.append("--require-full")
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def test_current_catalog_is_admitted(self) -> None:
        result = self.run_check(REPO)
        admissions = json.loads(
            (REPO / "catalog" / "admissions.json").read_text(encoding="utf-8")
        )
        self.assertIn(f"skills={len(admissions['skills'])}", result.stdout)

    def test_unadmitted_packaged_skill_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "catalog", root / "catalog")
            manifest = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))
            manifest["skill_packs"]["daily-work"].append("unreviewed")
            (root / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            result = self.run_check(root, expected=2)
            self.assertIn("missing admission: unreviewed", result.stderr)

    def test_release_gate_accepts_complete_full_profile(self) -> None:
        result = self.run_check(REPO, require_full=True)
        self.assertIn("full=True", result.stdout)

    def test_runtime_source_catalog_rejects_local_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "catalog", root / "catalog")
            shutil.copy2(REPO / "manifest.json", root / "manifest.json")
            catalog_path = root / "catalog" / "runtime_sources.json"
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["skills"][0]["source_url"] = "file:///private/skill"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            result = self.run_check(root, expected=2)
            self.assertIn("not a public HTTPS URL", result.stderr)

    def test_missing_portable_modifications_record_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(REPO / "catalog", root / "catalog")
            shutil.copy2(REPO / "manifest.json", root / "manifest.json")
            shutil.copy2(REPO / "THIRD_PARTY_NOTICES.md", root / "THIRD_PARTY_NOTICES.md")
            admissions_path = root / "catalog" / "admissions.json"
            admissions = json.loads(admissions_path.read_text(encoding="utf-8"))
            group = admissions["provenance_groups"]["nextlevelbuilder-ui-ux-pro-max"]
            group["modifications"] = "catalog/missing-portable-patches.json"
            admissions_path.write_text(json.dumps(admissions), encoding="utf-8")
            result = self.run_check(root, expected=2)
            self.assertIn("missing modifications file", result.stderr)


if __name__ == "__main__":
    unittest.main()
