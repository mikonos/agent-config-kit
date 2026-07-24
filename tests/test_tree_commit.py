from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "find_tree_commit",
    REPO / "scripts" / "find_tree_commit.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TreeCommitTests(unittest.TestCase):
    def git(self, repository: Path, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repository), *args],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def test_finds_historical_commit_with_exact_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.git(repository, "init")
            self.git(repository, "config", "user.email", "test@example.com")
            self.git(repository, "config", "user.name", "Test")
            skill = repository / "skills" / "demo" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("first\n", encoding="utf-8")
            self.git(repository, "add", ".")
            self.git(repository, "commit", "-m", "first")
            first_commit = self.git(repository, "rev-parse", "HEAD")
            tree_sha = self.git(repository, "rev-parse", "HEAD:skills/demo")
            skill.write_text("second\n", encoding="utf-8")
            self.git(repository, "commit", "-am", "second")
            self.assertEqual(
                MODULE.find_commit(repository, "skills/demo/SKILL.md", tree_sha),
                first_commit,
            )

    def test_rejects_unsafe_skill_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                MODULE.find_commit(Path(temp), "../SKILL.md", "a" * 40)


if __name__ == "__main__":
    unittest.main()
