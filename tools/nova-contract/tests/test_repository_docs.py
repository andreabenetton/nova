# SPDX-License-Identifier: Apache-2.0
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "generate_repository_docs", TOOLS / "generate_repository_docs.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


class RepositoryTreeTests(unittest.TestCase):
    """The tree lists what Git knows about, not what happens to be on disk.

    Build output and agent settings exist on some clones and not others, so a
    filesystem walk produced a tree that failed --check depending on the clone.
    """

    def setUp(self):
        self.module = load_generator()
        self._tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self._tempdir.name).resolve()
        self.addCleanup(self._tempdir.cleanup)

        git(self.root, "init")
        (self.root / ".gitignore").write_text(
            "/Cargo.lock\n**/.claude/settings.local.json\n", encoding="utf-8"
        )
        (self.root / "Cargo.lock").write_text("generated\n", encoding="utf-8")

        (self.root / "src").mkdir()
        (self.root / "src" / "main.rs").write_text("fn main() {}\n", encoding="utf-8")

        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "settings.local.json").write_text("{}\n", encoding="utf-8")
        (self.root / ".claude" / "statusline.sh").write_text("echo\n", encoding="utf-8")

        self.module.ROOT = self.root

    def tree(self) -> list[str]:
        return self.module.repository_tree().splitlines()

    def test_tracked_files_and_their_directories_are_listed(self):
        listed = self.tree()
        self.assertIn("./src", listed)
        self.assertIn("./src/main.rs", listed)

    def test_ignored_build_output_is_excluded(self):
        self.assertNotIn("./Cargo.lock", self.tree())

    def test_ignored_agent_settings_are_excluded(self):
        self.assertNotIn("./.claude/settings.local.json", self.tree())

    def test_a_directory_survives_when_only_some_children_are_ignored(self):
        listed = self.tree()
        self.assertIn("./.claude", listed)
        self.assertIn("./.claude/statusline.sh", listed)

    def test_internal_directories_are_excluded(self):
        vendored = self.root / "target"
        vendored.mkdir()
        (vendored / "artifact.bin").write_text("x\n", encoding="utf-8")
        self.assertNotIn("./target", self.tree())

    def test_the_root_is_first_and_entries_are_sorted(self):
        listed = self.tree()
        self.assertEqual(listed[0], ".")
        self.assertEqual(listed[1:], sorted(listed[1:]))


if __name__ == "__main__":
    unittest.main()
