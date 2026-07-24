from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "export_runtime_lock",
    REPO / "scripts" / "export_runtime_lock.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RuntimeLockExportTests(unittest.TestCase):
    def test_export_is_path_free_and_marks_admitted_skills(self) -> None:
        lock = {
            "version": 3,
            "skills": {
                "remote": {
                    "sourceType": "git",
                    "sourceUrl": "git@github.com:owner/repo.git",
                    "skillPath": "skills/remote/SKILL.md",
                    "skillFolderHash": "a" * 40,
                    "installedAt": "private metadata",
                },
                "official": {
                    "sourceType": "well-known",
                    "sourceUrl": "https://example.com/.well-known/skills/official/SKILL.md",
                    "skillFolderHash": "",
                },
            },
        }
        result = MODULE.export_catalog(lock, {"remote"})
        encoded = MODULE.encode(result)
        self.assertNotIn("installedAt", encoded)
        self.assertNotIn("private metadata", encoded)
        by_name = {entry["name"]: entry for entry in result["skills"]}
        self.assertEqual(by_name["remote"]["source_url"], "https://github.com/owner/repo")
        self.assertEqual(by_name["remote"]["delivery"], "bundled")
        self.assertEqual(by_name["official"]["delivery"], "fetch_from_origin")
        self.assertIsNone(by_name["official"]["tree_sha"])

    def test_export_rejects_parent_traversal_and_local_sources(self) -> None:
        base = {
            "version": 3,
            "skills": {
                "unsafe": {
                    "sourceType": "github",
                    "sourceUrl": "https://github.com/owner/repo",
                    "skillPath": "../SKILL.md",
                    "skillFolderHash": "b" * 40,
                }
            },
        }
        with self.assertRaises(ValueError):
            MODULE.export_catalog(base, set())
        base["skills"]["unsafe"] = {
            "sourceType": "github",
            "sourceUrl": "https://github.com/owner/repo",
            "skillPath": "skills/unsafe/SKILL.md",
            "skillFolderHash": "c" * 40,
            "ref": "/" + "/".join(("Users", "example", "private")),
        }
        with self.assertRaises(ValueError):
            MODULE.export_catalog(base, set())
        base["skills"]["unsafe"]["skillPath"] = "SKILL.md"
        base["skills"]["unsafe"]["sourceUrl"] = "file:///private/repo"
        with self.assertRaises(ValueError):
            MODULE.export_catalog(base, set())

    def test_export_rejects_url_credentials_queries_and_unsafe_refs(self) -> None:
        base = {
            "version": 3,
            "skills": {
                "unsafe": {
                    "sourceType": "well-known",
                    "sourceUrl": "https://user:secret@example.com/SKILL.md?token=value",
                    "skillFolderHash": "",
                }
            },
        }
        with self.assertRaises(ValueError):
            MODULE.export_catalog(base, set())

    def test_export_rejects_windows_absolute_skill_path(self) -> None:
        lock = {
            "version": 3,
            "skills": {
                "unsafe": {
                    "sourceType": "github",
                    "sourceUrl": "https://github.com/owner/repo",
                    "skillPath": "C:\\private\\SKILL.md",
                    "skillFolderHash": "d" * 40,
                }
            },
        }
        with self.assertRaises(ValueError):
            MODULE.export_catalog(lock, set())


if __name__ == "__main__":
    unittest.main()
