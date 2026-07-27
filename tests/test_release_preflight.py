from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_preflight",
    REPO / "scripts" / "release_preflight.py",
)
assert SPEC and SPEC.loader
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class ReleasePreflightTests(unittest.TestCase):
    def test_release_requires_exactly_the_three_canonical_source_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = {}
            for label in PREFLIGHT.REQUIRED_SOURCE_LABELS:
                paths[label] = root / label
                paths[label].mkdir()
            with self.assertRaisesRegex(ValueError, "exactly these source labels"):
                PREFLIGHT.validate_source_args(
                    [
                        f"cursor-vault={paths['cursor-vault']}",
                        f"agents-global={paths['agents-global']}",
                    ],
                    package_root=root / "package",
                )

            sources = PREFLIGHT.validate_source_args(
                [f"{label}={path}" for label, path in paths.items()],
                package_root=root / "package",
            )

            self.assertEqual(len(sources), 3)

    def test_release_rejects_package_local_or_noncanonical_source_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "package"
            package.mkdir()
            canonical = {
                label: root / label
                for label in PREFLIGHT.REQUIRED_SOURCE_LABELS
            }
            for path in canonical.values():
                path.mkdir()

            values = [f"{label}={path}" for label, path in canonical.items()]
            self.assertEqual(
                PREFLIGHT.validate_source_args(
                    values,
                    canonical_roots={label: path.resolve() for label, path in canonical.items()},
                    package_root=package,
                ),
                values,
            )

            fake = package / "fake-source"
            fake.mkdir()
            package_local = [
                f"{label}={fake if label == 'cursor-vault' else path}"
                for label, path in canonical.items()
            ]
            with self.assertRaisesRegex(ValueError, "outside the package"):
                PREFLIGHT.validate_source_args(
                    package_local,
                    canonical_roots={label: path.resolve() for label, path in canonical.items()},
                    package_root=package,
                )

            other = root / "other"
            other.mkdir()
            mismatched = [
                f"{label}={other if label == 'cursor-vault' else path}"
                for label, path in canonical.items()
            ]
            with self.assertRaisesRegex(ValueError, "canonical ledger"):
                PREFLIGHT.validate_source_args(
                    mismatched,
                    canonical_roots={label: path.resolve() for label, path in canonical.items()},
                    package_root=package,
                )

    def test_private_source_root_ledger_requires_exact_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sources = {}
            for label in PREFLIGHT.REQUIRED_SOURCE_LABELS:
                path = root / label
                path.mkdir()
                sources[label] = str(path)
            ledger = root / "private-source-roots.json"
            ledger.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "sensitivity": "private_do_not_publish",
                        "sources": sources,
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                set(PREFLIGHT.load_private_source_roots(ledger)),
                PREFLIGHT.REQUIRED_SOURCE_LABELS,
            )

            sources.pop("codex-global")
            ledger.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "sensitivity": "private_do_not_publish",
                        "sources": sources,
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "ledger is invalid"):
                PREFLIGHT.load_private_source_roots(ledger)

    def test_alignment_failure_stops_before_package_verification(self) -> None:
        calls: list[list[str]] = []

        def runner(command: list[str]) -> int:
            calls.append(command)
            return 2

        result = PREFLIGHT.run_preflight(
            alignment_command=["python", "alignment"],
            verification_command=["python", "verify"],
            runner=runner,
        )

        self.assertEqual(result, 2)
        self.assertEqual(calls, [["python", "alignment"]])

    def test_release_requires_alignment_then_package_verification(self) -> None:
        calls: list[list[str]] = []

        def runner(command: list[str]) -> int:
            calls.append(command)
            return 0

        result = PREFLIGHT.run_preflight(
            alignment_command=["python", "alignment"],
            verification_command=["python", "verify"],
            runner=runner,
        )

        self.assertEqual(result, 0)
        self.assertEqual(
            calls,
            [["python", "alignment"], ["python", "verify"]],
        )

    def test_rule_alignment_failure_stops_before_skill_alignment(self) -> None:
        calls: list[list[str]] = []

        def runner(command: list[str]) -> int:
            calls.append(command)
            return 2 if command == ["python", "rules"] else 0

        result = PREFLIGHT.run_preflight(
            rule_alignment_command=["python", "rules"],
            alignment_command=["python", "skills"],
            verification_command=["python", "verify"],
            runner=runner,
        )

        self.assertEqual(result, 2)
        self.assertEqual(calls, [["python", "rules"]])

    def test_private_privacy_failure_stops_before_alignment(self) -> None:
        calls: list[list[str]] = []

        def runner(command: list[str]) -> int:
            calls.append(command)
            return 2

        result = PREFLIGHT.run_preflight(
            privacy_command=["python", "privacy"],
            alignment_command=["python", "alignment"],
            verification_command=["python", "verify"],
            runner=runner,
        )

        self.assertEqual(result, 2)
        self.assertEqual(calls, [["python", "privacy"]])

    def test_private_release_inputs_cannot_be_replaced_by_public_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workbench = root / ".agent-config-kit-workbench"
            workbench.mkdir()
            expected = workbench / "private-term-hashes.json"
            expected.write_text("{}\n", encoding="utf-8")
            public_forgery = root / "catalog" / "private-term-hashes.json"
            public_forgery.parent.mkdir()
            public_forgery.write_text("{}\n", encoding="utf-8")

            accepted = PREFLIGHT.validate_private_path(
                expected,
                expected=expected,
                label="privacy ledger",
                ignored_checker=lambda path: path == expected,
            )

            self.assertEqual(accepted, expected)
            with self.assertRaisesRegex(
                ValueError,
                "fixed Git-ignored maintainer workbench path",
            ):
                PREFLIGHT.validate_private_path(
                    public_forgery,
                    expected=expected,
                    label="privacy ledger",
                    ignored_checker=lambda _: True,
                )

    def test_unignored_private_release_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            expected = (
                Path(temporary)
                / ".agent-config-kit-workbench"
                / "private-skill-inventory.json"
            )
            expected.parent.mkdir()
            expected.write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not Git-ignored"):
                PREFLIGHT.validate_private_path(
                    expected,
                    expected=expected,
                    label="private inventory",
                    ignored_checker=lambda _: False,
                )


if __name__ == "__main__":
    unittest.main()
