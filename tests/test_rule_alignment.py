from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_rule_alignment",
    REPO / "scripts" / "check_rule_alignment.py",
)
assert SPEC and SPEC.loader
ALIGNMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ALIGNMENT)


BASE = "\n".join(ALIGNMENT.BASE_MARKERS) + "\n"
KNOWLEDGE = "\n".join(ALIGNMENT.PROFILE_MARKERS["knowledge-vault"]) + "\n"
FULL = "\n".join(
    marker
    for marker in ALIGNMENT.PROFILE_MARKERS["full"]
    if marker not in ALIGNMENT.PROFILE_MARKERS["knowledge-vault"]
) + "\n"


class RuleAlignmentTests(unittest.TestCase):
    def fixture(self, root: Path) -> tuple[Path, Path, Path]:
        package = root / "package"
        rules = package / "packs" / "core" / "rules"
        rules.mkdir(parents=True)
        (rules / "core.md").write_text(BASE, encoding="utf-8")
        (rules / "knowledge-vault.md").write_text(KNOWLEDGE, encoding="utf-8")
        (rules / "full.md").write_text(FULL, encoding="utf-8")
        source = root / "live" / "AGENTS.md"
        source.parent.mkdir()
        source.write_text("private live contract\n", encoding="utf-8")
        manifest = {
            "profiles": {
                "daily-work": {
                    "rule_sources": ["packs/core/rules/core.md"],
                },
                "knowledge-vault": {
                    "rule_sources": [
                        "packs/core/rules/core.md",
                        "packs/core/rules/knowledge-vault.md",
                    ],
                },
                "full": {
                    "rule_sources": [
                        "packs/core/rules/core.md",
                        "packs/core/rules/knowledge-vault.md",
                        "packs/core/rules/full.md",
                    ],
                },
            }
        }
        manifest_path = package / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        profiles = {}
        for name, profile in manifest["profiles"].items():
            body = ALIGNMENT.compose_rule(package, profile["rule_sources"])
            profiles[name] = {
                "rule_sources": profile["rule_sources"],
                "composed_sha256": hashlib.sha256(
                    body.encode("utf-8")
                ).hexdigest(),
            }
        review = {
            "schema_version": 1,
            "sensitivity": "private_do_not_publish",
            "source": {
                "label": "workspace-agents",
                "path": str(source),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            },
            "profiles": profiles,
            "reviewed_transformations": [
                "Removed local paths and runtime-specific commands.",
                "Preserved authority, expert routing, and verification gates.",
            ],
        }
        review_path = root / "review.json"
        review_path.write_text(json.dumps(review), encoding="utf-8")
        return package, manifest_path, review_path

    def test_reviewed_profile_rules_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package, manifest, review = self.fixture(Path(temporary))

            counts = ALIGNMENT.check_alignment(
                review,
                package_root=package,
                manifest_path=manifest,
            )

            self.assertEqual(counts, {"profiles": 3, "sources": 3})

    def test_live_source_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package, manifest, review = self.fixture(root)
            (root / "live" / "AGENTS.md").write_text(
                "changed live contract\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ALIGNMENT.RuleAlignmentError,
                "live AGENTS.md changed",
            ):
                ALIGNMENT.check_alignment(
                    review,
                    package_root=package,
                    manifest_path=manifest,
                )

    def test_portable_rule_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package, manifest, review = self.fixture(root)
            core = package / "packs" / "core" / "rules" / "core.md"
            core.write_text(core.read_text(encoding="utf-8") + "drift\n")

            with self.assertRaisesRegex(
                ALIGNMENT.RuleAlignmentError,
                "changed after review",
            ):
                ALIGNMENT.check_alignment(
                    review,
                    package_root=package,
                    manifest_path=manifest,
                )

    def test_private_or_local_marker_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package, manifest, review = self.fixture(root)
            review_value = json.loads(review.read_text(encoding="utf-8"))
            core = package / "packs" / "core" / "rules" / "core.md"
            core.write_text(
                core.read_text(encoding="utf-8") + "/Users/private\n",
                encoding="utf-8",
            )
            for name, profile in json.loads(
                manifest.read_text(encoding="utf-8")
            )["profiles"].items():
                body = ALIGNMENT.compose_rule(package, profile["rule_sources"])
                review_value["profiles"][name]["composed_sha256"] = (
                    hashlib.sha256(body.encode("utf-8")).hexdigest()
                )
            review.write_text(json.dumps(review_value), encoding="utf-8")

            with self.assertRaisesRegex(
                ALIGNMENT.RuleAlignmentError,
                "private or local marker",
            ):
                ALIGNMENT.check_alignment(
                    review,
                    package_root=package,
                    manifest_path=manifest,
                )


if __name__ == "__main__":
    unittest.main()
