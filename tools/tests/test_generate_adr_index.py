# SPDX-License-Identifier: Apache-2.0
"""Vectors for the ADR index generator and validator."""

from __future__ import annotations

import io
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import generate_adr_index as tool  # noqa: E402


VALID = textwrap.dedent(
    """\
    ---
    adr: ADR-P-0001
    title: Split P-Stratum into P-LAP and P-RAP
    scope: p-stratum
    status: proposed
    date: 2026-08-01
    supersedes: []
    superseded_by: []
    affected_contracts: []
    affected_documents: []
    ---

    <!-- SPDX-License-Identifier: CC-BY-4.0 -->

    # ADR-P-0001: Split P-Stratum into P-LAP and P-RAP

    ## Context

    Body.
    """
)


class AdrIndexTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "adr" / "p-stratum").mkdir(parents=True)
        (self.root / "generated" / "documentation").mkdir(parents=True)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / "adr" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_tool(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = tool.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def assert_rejected(self, fragment: str) -> None:
        code, _, err = self.run_tool()
        self.assertEqual(code, 1)
        self.assertIn(fragment, err)

    # Success.

    def test_valid_record_generates_index(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        code, out, _ = self.run_tool()
        self.assertEqual(code, 0)
        self.assertIn("1 record(s)", out)
        index = (self.root / "generated" / "documentation" / "adr-index.md").read_text(encoding="utf-8")
        self.assertIn("| ADR-P-0001 | Split P-Stratum into P-LAP and P-RAP | proposed | 2026-08-01 |", index)

    def test_empty_scope_is_reported_as_having_no_records(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.run_tool()
        index = (self.root / "generated" / "documentation" / "adr-index.md").read_text(encoding="utf-8")
        self.assertIn("## security (`ADR-SEC-`, `adr/security/`)\n\nNo records.", index)

    def test_quoted_date_is_accepted(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("date: 2026-08-01", 'date: "2026-08-01"'),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    def test_every_scope_round_trips_its_prefix_and_directory(self) -> None:
        for scope, (prefix, directory) in tool.SCOPES.items():
            with self.subTest(scope=scope):
                text = (
                    VALID.replace("adr: ADR-P-0001", f"adr: ADR-{prefix}-0001")
                    .replace("scope: p-stratum", f"scope: {scope}")
                    .replace("# ADR-P-0001:", f"# ADR-{prefix}-0001:")
                )
                path = self.write(f"{directory}/ADR-{prefix}-0001-example-record.md", text)
                errors: list[str] = []
                record = tool.load(path, self.root, errors)
                self.assertEqual(errors, [])
                self.assertIsNotNone(record)
                self.assertEqual(record.scope, scope)
                path.unlink()

    def test_supersession_pair_is_accepted(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("status: proposed", "status: superseded").replace(
                "superseded_by: []", "superseded_by: [ADR-P-0002]"
            ),
        )
        self.write(
            "p-stratum/ADR-P-0002-successor-record.md",
            VALID.replace("ADR-P-0001", "ADR-P-0002").replace("supersedes: []", "supersedes: [ADR-P-0001]"),
        )
        code, out, _ = self.run_tool()
        self.assertEqual(code, 0)
        self.assertIn("2 record(s)", out)

    # Rejection.

    def test_filename_without_scope_prefix_is_rejected(self) -> None:
        self.write("p-stratum/0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        code, out, _ = self.run_tool()
        # A legacy filename is not discovered as a record at all.
        self.assertEqual(code, 0)
        self.assertIn("0 record(s)", out)

    def test_malformed_scoped_filename_is_rejected(self) -> None:
        self.write("p-stratum/ADR-P-01-split.md", VALID)
        self.assert_rejected("filename must match")

    def test_unknown_prefix_is_rejected(self) -> None:
        self.write("p-stratum/ADR-XYZ-0001-split.md", VALID)
        self.assert_rejected("unknown identifier prefix")

    def test_missing_front_matter_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.split("---\n", 2)[2].lstrip(),
        )
        self.assert_rejected("missing YAML front matter")

    def test_missing_required_key_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_documents: []\n", ""),
        )
        self.assert_rejected("front matter missing affected_documents")

    def test_unknown_front_matter_key_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("status: proposed", "status: proposed\nowner: someone"),
        )
        self.assert_rejected("unknown front matter keys owner")

    def test_identifier_mismatch_with_filename_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("adr: ADR-P-0001", "adr: ADR-P-0009"),
        )
        self.assert_rejected("does not match the filename")

    def test_heading_identifier_mismatch_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("# ADR-P-0001:", "# ADR-P-0009:"),
        )
        self.assert_rejected("heading identifier")

    def test_heading_title_mismatch_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("# ADR-P-0001: Split", "# ADR-P-0001: Divide"),
        )
        self.assert_rejected("heading title does not match")

    def test_missing_heading_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("# ADR-P-0001: Split P-Stratum into P-LAP and P-RAP", "## Decision"),
        )
        self.assert_rejected("missing an '# ADR-<SCOPE>-NNNN: Title' heading")

    def test_scope_not_matching_prefix_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("scope: p-stratum", "scope: security"),
        )
        self.assert_rejected("does not match prefix P")

    def test_record_in_the_wrong_directory_is_rejected(self) -> None:
        self.write("architecture/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.assert_rejected("belongs in adr/p-stratum/")

    def test_unknown_status_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("status: proposed", "status: draft"),
        )
        self.assert_rejected("status 'draft' is not one of")

    def test_every_allowed_status_is_accepted(self) -> None:
        for status in tool.STATUSES:
            with self.subTest(status=status):
                path = self.write(
                    "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
                    VALID.replace("status: proposed", f"status: {status}"),
                )
                errors: list[str] = []
                self.assertIsNotNone(tool.load(path, self.root, errors))
                self.assertEqual(errors, [])

    def test_non_iso_date_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("date: 2026-08-01", 'date: "1 August 2026"'),
        )
        self.assert_rejected("date must be an ISO YYYY-MM-DD value")

    def test_timestamp_date_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("date: 2026-08-01", "date: 2026-08-01 09:30:00"),
        )
        self.assert_rejected("date must be an ISO YYYY-MM-DD value")

    def test_scalar_where_a_list_is_required_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("supersedes: []", "supersedes: ADR-P-0002"),
        )
        self.assert_rejected("supersedes must be a list of strings")

    def test_legacy_identifier_citation_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("Body.", "This refines ADR-0002."),
        )
        self.assert_rejected("cites retired global identifier ADR-0002")

    def test_scoped_identifier_in_the_body_is_not_a_legacy_citation(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("Body.", "This refines ADR-ARCH-0001."),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    def test_duplicate_identifier_across_scopes_is_rejected(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.write("p-stratum/ADR-P-0001-duplicate-allocation.md", VALID)
        self.assert_rejected("duplicate identifier ADR-P-0001")

    def test_supersedes_unknown_record_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("supersedes: []", "supersedes: [ADR-P-0099]"),
        )
        self.assert_rejected("supersedes unknown record ADR-P-0099")

    def test_asymmetric_supersession_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("supersedes: []", "supersedes: [ADR-P-0002]"),
        )
        self.write("p-stratum/ADR-P-0002-successor-record.md", VALID.replace("ADR-P-0001", "ADR-P-0002"))
        self.assert_rejected("which does not list it in superseded_by")

    def test_superseded_record_keeping_an_active_status_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("superseded_by: []", "superseded_by: [ADR-P-0002]"),
        )
        self.write(
            "p-stratum/ADR-P-0002-successor-record.md",
            VALID.replace("ADR-P-0001", "ADR-P-0002").replace("supersedes: []", "supersedes: [ADR-P-0001]"),
        )
        self.assert_rejected("has superseded_by but status is 'proposed'")

    # Staleness.

    def test_check_fails_on_a_stale_index(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.assertEqual(self.run_tool()[0], 0)
        self.write("p-stratum/ADR-P-0002-successor-record.md", VALID.replace("ADR-P-0001", "ADR-P-0002"))
        code, _, err = self.run_tool("--check")
        self.assertEqual(code, 1)
        self.assertIn("stale generated documentation", err)

    def test_check_passes_on_a_current_index(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.assertEqual(self.run_tool()[0], 0)
        self.assertEqual(self.run_tool("--check")[0], 0)

    def test_check_does_not_write_the_index(self) -> None:
        self.write("p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        self.assertEqual(self.run_tool("--check")[0], 1)
        self.assertFalse((self.root / "generated" / "documentation" / "adr-index.md").exists())


if __name__ == "__main__":
    unittest.main()
