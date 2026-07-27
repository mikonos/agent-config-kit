from __future__ import annotations

import copy
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "install" / "scripts"))
import externalctl  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "refresh_external_lock",
    REPO / "scripts" / "refresh_external_lock.py",
)
assert SPEC and SPEC.loader
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)


OLD_DATA = b"---\nname: official-demo\ndescription: Old.\n---\n"
NEW_DATA = b"---\nname: official-demo\ndescription: New.\n---\n"


def catalog() -> dict:
    return {
        "schema_version": 1,
        "packs": {
            "official": {
                "description": "Fixture.",
                "source_host": "official.example",
                "skills": [
                    {
                        "name": "official-demo",
                        "sha256": hashlib.sha256(OLD_DATA).hexdigest(),
                        "url": (
                            "https://official.example/.well-known/skills/"
                            "official-demo/SKILL.md"
                        ),
                    }
                ],
            }
        },
    }


def update(status: str = "update_available") -> externalctl.ExternalUpdate:
    return externalctl.ExternalUpdate(
        name="official-demo",
        url=(
            "https://official.example/.well-known/skills/"
            "official-demo/SKILL.md"
        ),
        approved_sha256=hashlib.sha256(OLD_DATA).hexdigest(),
        observed_sha256=hashlib.sha256(NEW_DATA).hexdigest(),
        status=status,
    )


class RefreshExternalLockTests(unittest.TestCase):
    def test_refresh_moves_current_hash_to_reviewed_history(self) -> None:
        value = catalog()

        changed = REFRESH.refresh_catalog(value, [update()])

        self.assertEqual(changed, 1)
        entry = value["packs"]["official"]["skills"][0]
        self.assertEqual(entry["sha256"], hashlib.sha256(NEW_DATA).hexdigest())
        self.assertEqual(
            entry["previous_sha256"],
            [hashlib.sha256(OLD_DATA).hexdigest()],
        )
        externalctl.validate_catalog(value)

    def test_existing_install_remains_valid_after_lock_refresh(self) -> None:
        value = catalog()
        old_hash = value["packs"]["official"]["skills"][0]["sha256"]
        state = {
            "schema_version": 1,
            "status": "installed",
            "runtime": "codex",
            "packs": ["official"],
            "files": [
                {
                    "name": "official-demo",
                    "target": ".agents/skills/official-demo/SKILL.md",
                    "url": value["packs"]["official"]["skills"][0]["url"],
                    "installed_sha256": old_hash,
                }
            ],
        }

        REFRESH.refresh_catalog(value, [update()])

        externalctl.validate_state(
            state,
            {
                "runtimes": {
                    "codex": {"skills_root": ".agents/skills"},
                }
            },
            value,
        )

    def test_refresh_rejects_rollback_and_partial_results(self) -> None:
        with self.assertRaisesRegex(REFRESH.RefreshError, "previously served"):
            REFRESH.refresh_catalog(
                catalog(),
                [update("rollback_detected")],
            )

        with self.assertRaisesRegex(REFRESH.RefreshError, "does not cover"):
            REFRESH.refresh_catalog(catalog(), [])

    def test_refresh_rejects_result_from_another_url(self) -> None:
        forged = update()
        forged = externalctl.ExternalUpdate(
            name=forged.name,
            url="https://official.example/.well-known/skills/other/SKILL.md",
            approved_sha256=forged.approved_sha256,
            observed_sha256=forged.observed_sha256,
            status=forged.status,
        )

        with self.assertRaisesRegex(REFRESH.RefreshError, "invalid update result"):
            REFRESH.refresh_catalog(catalog(), [forged])

    def test_report_contains_hashes_and_links_but_not_skill_contents(self) -> None:
        report = REFRESH.report_markdown([update()])

        self.assertIn(hashlib.sha256(OLD_DATA).hexdigest(), report)
        self.assertIn(hashlib.sha256(NEW_DATA).hexdigest(), report)
        self.assertIn("https://official.example/", report)
        self.assertNotIn("description: New", report)

    def test_refresh_is_idempotent_for_current_catalog(self) -> None:
        value = catalog()
        original = copy.deepcopy(value)
        current = update("current")
        current = externalctl.ExternalUpdate(
            name=current.name,
            url=current.url,
            approved_sha256=current.approved_sha256,
            observed_sha256=current.approved_sha256,
            status="current",
        )

        self.assertEqual(REFRESH.refresh_catalog(value, [current]), 0)
        self.assertEqual(value, original)

    def test_workflow_opens_review_pr_without_merging_or_installing(self) -> None:
        workflow = (
            REPO / ".github" / "workflows" / "refresh-external-lock.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("schedule:", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("--apply", workflow)
        self.assertIn("--report", workflow)
        self.assertIn("python scripts/verify.py", workflow)
        self.assertIn("gh pr create", workflow)
        self.assertNotIn("gh pr merge", workflow)
        self.assertNotIn("externalctl.py install", workflow)


if __name__ == "__main__":
    unittest.main()
