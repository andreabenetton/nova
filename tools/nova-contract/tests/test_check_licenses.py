# SPDX-License-Identifier: Apache-2.0
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"


def load_check_licenses():
    spec = importlib.util.spec_from_file_location(
        "check_licenses", TOOLS / "check_licenses.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class RepositoryDirectoryTests(unittest.TestCase):
    """Directory markers are required only where Git tracks content.

    A directory holding nothing but ignored files exists on some clones and not
    others, so requiring a marker for it made the check clone-dependent.
    """

    def setUp(self):
        self.module = load_check_licenses()
        self._tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tempdir.name).resolve()
        self.addCleanup(self._tempdir.cleanup)

        git(self.root, "init")
        (self.root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")

        (self.root / "tracked").mkdir()
        (self.root / "tracked" / "file.md").write_text("content\n", encoding="utf-8")

        (self.root / "ignored_only").mkdir()
        (self.root / "ignored_only" / "ignored.txt").write_text("x\n", encoding="utf-8")

        self.module.ROOT = self.root

    def directories(self) -> set[str]:
        return {
            path.relative_to(self.root).as_posix()
            for path in self.module.repository_directories()
            if path != self.root
        }

    def test_directory_with_tracked_content_requires_a_marker(self):
        self.assertIn("tracked", self.directories())

    def test_directory_holding_only_ignored_files_is_excluded(self):
        self.assertNotIn("ignored_only", self.directories())

    def test_nested_directories_are_reported_for_tracked_content(self):
        nested = self.root / "outer" / "inner"
        nested.mkdir(parents=True)
        (nested / "file.md").write_text("content\n", encoding="utf-8")
        found = self.directories()
        self.assertIn("outer", found)
        self.assertIn("outer/inner", found)

    def test_internal_directories_remain_excluded(self):
        vendored = self.root / "tracked" / "__pycache__"
        vendored.mkdir()
        (vendored / "file.md").write_text("content\n", encoding="utf-8")
        self.assertNotIn("tracked/__pycache__", self.directories())

    def test_the_repository_root_is_always_reported(self):
        self.assertIn(self.root, self.module.repository_directories())


if __name__ == "__main__":
    unittest.main()
