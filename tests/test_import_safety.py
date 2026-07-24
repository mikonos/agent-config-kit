from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SNAPSHOT = load_module(
    "import_snapshot_skills",
    REPO / "scripts" / "import_snapshot_skills.py",
)
TREE = load_module(
    "import_tree_locked_skills",
    REPO / "scripts" / "import_tree_locked_skills.py",
)


class ImportSafetyTests(unittest.TestCase):
    def git(self, repository: Path, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repository), *args],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def test_import_components_reject_path_traversal(self) -> None:
        for module in (SNAPSHOT, TREE):
            with self.assertRaises(module.ImportError if module is TREE else module.SnapshotImportError):
                module.safe_component("../../outside", "pack")

    def test_tree_skill_name_rejects_duplicate_or_quoted_yaml_names(self) -> None:
        for frontmatter in (
            b'---\nname: forged-name\nname: "demo"\n---\n',
            b"---\nname: forged-name\nname : demo\n---\n",
            b'---\nname: "demo"\n---\n',
            b'---\nname: forged-name\n"name": demo\n---\n',
            b"---\nname: forged-name\n'name': demo\n---\n",
            b'---\nname: forged-name\n"na\\x6de": demo\n---\n',
            b"---\nname: forged-name\n? name\n: demo\n---\n",
        ):
            with self.assertRaises(TREE.ImportError):
                TREE.skill_name_from_tree([("SKILL.md", frontmatter, 0o644)])

    def test_tree_skill_name_accepts_nested_json_style_metadata_keys(self) -> None:
        frontmatter = b"""---
name: demo
metadata:
  {
    "runtime":
      {
        "requires": { "bins": ["demo"] },
      },
  }
---
"""
        self.assertEqual(
            TREE.skill_name_from_tree([("SKILL.md", frontmatter, 0o644)]),
            "demo",
        )

    @unittest.skipIf(
        os.name == "nt",
        "creating symlinks may require elevated Windows privileges",
    )
    def test_snapshot_source_rejects_symlink_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "root"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "SKILL.md").write_text("outside\n", encoding="utf-8")
            (root / "linked").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(SNAPSHOT.SnapshotImportError):
                SNAPSHOT.ensure_regular_source(
                    root,
                    root / "linked" / "SKILL.md",
                    "linked skill",
                )

    def test_tree_import_rejects_dirty_checkout_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            checkout = base / "checkout"
            checkout.mkdir()
            self.git(checkout, "init")
            self.git(checkout, "config", "user.email", "test@example.com")
            self.git(checkout, "config", "user.name", "Test")
            skill = checkout / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\nname: demo\ndescription: Demo.\n---\n",
                encoding="utf-8",
            )
            license_path = checkout / "LICENSE"
            license_path.write_text("MIT\n", encoding="utf-8")
            self.git(checkout, "add", ".")
            self.git(checkout, "commit", "-m", "fixture")
            commit = self.git(checkout, "rev-parse", "HEAD")
            tree_sha = self.git(checkout, "rev-parse", "HEAD:skills/demo")
            skill.write_bytes(b"working-tree-translation\r\n")
            object_files = {
                relative: data
                for relative, data, _ in TREE.git_tree_files(
                    checkout,
                    TREE.PurePosixPath("skills/demo"),
                )
            }
            self.assertIn(b"name: demo", object_files["SKILL.md"])
            self.assertNotEqual(object_files["SKILL.md"], skill.read_bytes())
            self.git(checkout, "checkout", "--", "skills/demo/SKILL.md")
            (skill.parent / "untracked.sh").write_text("unsafe\n", encoding="utf-8")
            groups = {
                "fixture": {
                    "allow_skills": ["demo"],
                    "commit": commit,
                    "license": "MIT",
                    "license_path": "LICENSE",
                    "license_sha256": hashlib.sha256(b"MIT\n").hexdigest(),
                    "origin": "https://github.com/example/repo",
                    "pack": "fixture",
                }
            }
            sources = {
                "skills": [
                    {
                        "name": "demo",
                        "source_url": "https://github.com/example/repo",
                        "skill_path": "skills/demo/SKILL.md",
                        "tree_sha": tree_sha,
                    }
                ]
            }
            pins = {
                "skills": [
                    {
                        "name": "demo",
                        "status": "exact_current",
                        "commit": commit,
                    }
                ]
            }
            original_root = TREE.ROOT
            TREE.ROOT = base / "package"
            TREE.ROOT.mkdir()
            try:
                with self.assertRaises(TREE.ImportError):
                    TREE.plan_imports(
                        groups,
                        sources,
                        pins,
                        {"fixture": checkout},
                    )
            finally:
                TREE.ROOT = original_root

    def test_tree_import_accepts_explicit_pinned_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            checkout = base / "checkout"
            checkout.mkdir()
            self.git(checkout, "init")
            self.git(checkout, "config", "user.email", "test@example.com")
            self.git(checkout, "config", "user.name", "Test")
            skill = checkout / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\nname: demo\ndescription: Demo.\n---\n",
                encoding="utf-8",
            )
            license_path = checkout / "LICENSE"
            license_path.write_text("MIT\n", encoding="utf-8")
            self.git(checkout, "add", ".")
            self.git(checkout, "commit", "-m", "fixture")
            commit = self.git(checkout, "rev-parse", "HEAD")
            tree_sha = self.git(checkout, "rev-parse", "HEAD:skills/demo")
            groups = {
                "fixture": {
                    "commit": commit,
                    "license": "MIT",
                    "license_path": "LICENSE",
                    "license_sha256": hashlib.sha256(b"MIT\n").hexdigest(),
                    "origin": "https://github.com/example/repo",
                    "pack": "fixture",
                    "skills": {
                        "demo": {
                            "source_dir": "skills/demo",
                            "tree_sha": tree_sha,
                        }
                    },
                }
            }
            original_root = TREE.ROOT
            TREE.ROOT = base / "package"
            TREE.ROOT.mkdir()
            try:
                files, licenses, admitted = TREE.plan_imports(
                    groups,
                    {"skills": []},
                    {"skills": []},
                    {"fixture": checkout},
                )
                groups["fixture"]["skills"] = {
                    "forged-name": {
                        "source_dir": "skills/demo",
                        "tree_sha": tree_sha,
                    }
                }
                with self.assertRaises(TREE.ImportError):
                    TREE.plan_imports(
                        groups,
                        {"skills": []},
                        {"skills": []},
                        {"fixture": checkout},
                    )
            finally:
                TREE.ROOT = original_root
            self.assertEqual(len(files), 1)
            self.assertEqual(len(licenses), 1)
            self.assertEqual(set(admitted), {"demo"})
            self.assertIn(b"name: demo", files[0][0])

    def test_tree_import_allows_pinned_root_file_subset(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            checkout = base / "checkout"
            checkout.mkdir()
            self.git(checkout, "init")
            self.git(checkout, "config", "user.email", "test@example.com")
            self.git(checkout, "config", "user.name", "Test")
            (checkout / "SKILL.md").write_text(
                "---\nname: root-demo\ndescription: Demo.\n---\n",
                encoding="utf-8",
            )
            (checkout / "not-packaged.txt").write_text("private\n", encoding="utf-8")
            (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
            self.git(checkout, "add", ".")
            self.git(checkout, "commit", "-m", "fixture")
            commit = self.git(checkout, "rev-parse", "HEAD")
            root_tree = self.git(checkout, "rev-parse", "HEAD^{tree}")
            groups = {
                "fixture": {
                    "commit": commit,
                    "license": "MIT",
                    "license_path": "LICENSE",
                    "license_sha256": hashlib.sha256(b"MIT\n").hexdigest(),
                    "origin": "https://github.com/example/repo",
                    "pack": "fixture",
                    "skills": {
                        "root-demo": {
                            "source_dir": ".",
                            "tree_sha": root_tree,
                            "include_files": ["SKILL.md"],
                        }
                    },
                }
            }
            original_root = TREE.ROOT
            TREE.ROOT = base / "package"
            TREE.ROOT.mkdir()
            try:
                files, _, admitted = TREE.plan_imports(
                    groups,
                    {"skills": []},
                    {"skills": []},
                    {"fixture": checkout},
                )
                del groups["fixture"]["skills"]["root-demo"]["include_files"]
                with self.assertRaises(TREE.ImportError):
                    TREE.plan_imports(
                        groups,
                        {"skills": []},
                        {"skills": []},
                        {"fixture": checkout},
                    )
                legacy_groups = {
                    "fixture": {
                        "allow_skills": ["root-demo"],
                        "commit": commit,
                        "license": "MIT",
                        "license_path": "LICENSE",
                        "license_sha256": hashlib.sha256(b"MIT\n").hexdigest(),
                        "origin": "https://github.com/example/repo",
                        "pack": "fixture",
                    }
                }
                legacy_sources = {
                    "skills": [
                        {
                            "name": "root-demo",
                            "source_url": "https://github.com/example/repo",
                            "skill_path": "SKILL.md",
                            "tree_sha": root_tree,
                        }
                    ]
                }
                legacy_pins = {
                    "skills": [
                        {
                            "name": "root-demo",
                            "status": "exact_current",
                            "commit": commit,
                        }
                    ]
                }
                with self.assertRaises(TREE.ImportError):
                    TREE.plan_imports(
                        legacy_groups,
                        legacy_sources,
                        legacy_pins,
                        {"fixture": checkout},
                    )
            finally:
                TREE.ROOT = original_root
            self.assertEqual(set(admitted), {"root-demo"})
            self.assertEqual([path.name for _, path, _ in files], ["SKILL.md"])
            self.assertNotIn(b"private", files[0][0])
            selected = TREE.git_tree_files(
                checkout,
                TREE.PurePosixPath("."),
                {"SKILL.md"},
            )
            self.assertEqual([relative for relative, _, _ in selected], ["SKILL.md"])

    @unittest.skipIf(
        os.name == "nt",
        "creating symlinks may require elevated Windows privileges",
    )
    def test_tree_result_write_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            package = base / "package"
            catalog = package / "catalog"
            catalog.mkdir(parents=True)
            outside = base / "outside.json"
            outside.write_text("keep\n", encoding="utf-8")
            result = catalog / "tree_import_result.json"
            result.symlink_to(outside)
            original_root = TREE.ROOT
            TREE.ROOT = package
            try:
                with self.assertRaises(TREE.ImportError):
                    TREE.atomic_write(result, b'{"changed": true}\n', 0o644)
            finally:
                TREE.ROOT = original_root
            self.assertEqual(outside.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
