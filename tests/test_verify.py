from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify", REPO / "scripts" / "verify.py")
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_portable_patch_anchor_must_match_registered_provenance(self) -> None:
        admissions = {
            "schema_version": 1,
            "provenance_groups": {
                "approved": {
                    "origin": "https://github.com/example/skills",
                    "commit": "a" * 40,
                }
            },
        }
        snapshots = {
            "schema_version": 1,
            "imports": {
                "approved": {
                    "origin": "https://github.com/example/skills",
                    "files": [{"path": "SKILL.md", "sha256": "b" * 64}],
                }
            },
        }
        provenance = VERIFY.registered_source_anchors(admissions, snapshots)

        self.assertTrue(
            VERIFY.is_registered_source_anchor(
                upstream_origin="https://github.com/example/skills",
                upstream_commit="a" * 40,
                source_snapshot=None,
                source_sha256="c" * 64,
                provenance=provenance,
            )
        )
        self.assertFalse(
            VERIFY.is_registered_source_anchor(
                upstream_origin="https://github.com/example/skills",
                upstream_commit="d" * 40,
                source_snapshot=None,
                source_sha256="b" * 64,
                provenance=provenance,
            )
        )
        self.assertTrue(
            VERIFY.is_registered_source_anchor(
                upstream_origin="https://github.com/example/skills",
                upstream_commit=None,
                source_snapshot="catalog/snapshot_imports.json",
                source_sha256="b" * 64,
                provenance=provenance,
            )
        )
        self.assertFalse(
            VERIFY.is_registered_source_anchor(
                upstream_origin="https://example.invalid/test-fixture",
                upstream_commit="0" * 40,
                source_snapshot=None,
                source_sha256="b" * 64,
                provenance=provenance,
            )
        )

    def test_portable_omission_requires_safe_reason_and_snapshot_anchor(self) -> None:
        omission = {
            "description": "Exclude source-side evaluation metadata from runtime delivery.",
            "reason": "test_metadata",
            "skill": "demo",
            "source_path": "test-prompts.json",
            "source_sha256": "b" * 64,
            "source_snapshot": "catalog/maintainer_source_snapshot.json",
            "upstream_origin": "this-repository",
        }

        VERIFY.validate_portable_omission(
            omission,
            provenance={
                "origins": {"this-repository"},
                "commits": set(),
                "source_hashes": {("this-repository", "b" * 64)},
            },
        )

        invalid = dict(omission, reason="hide_private_material")
        with self.assertRaisesRegex(RuntimeError, "invalid portable omission reason"):
            VERIFY.validate_portable_omission(
                invalid,
                provenance={
                    "origins": {"this-repository"},
                    "commits": set(),
                    "source_hashes": {("this-repository", "b" * 64)},
                },
            )

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

    def test_binary_asset_allowlist_is_hash_locked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            asset = root / "assets" / "example.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            catalog = {
                "schema_version": 1,
                "assets": [
                    {
                        "description": "Test fixture.",
                        "path": "assets/example.png",
                        "sha256": "0" * 64,
                    }
                ],
            }

            with self.assertRaisesRegex(
                RuntimeError,
                "binary asset digest mismatch",
            ):
                VERIFY.approved_binary_assets(root, catalog)

    def test_verify_command_labels_package_scope(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "verify.py")],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PACKAGE VERIFY OK", result.stdout)
        self.assertIn("source alignment requires the maintainer gate", result.stdout)


if __name__ == "__main__":
    unittest.main()
