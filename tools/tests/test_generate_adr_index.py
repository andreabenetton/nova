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

    ## Decision

    Body.

    ## Architectural boundaries

    Body.

    ## Interface and contract impact

    none.

    ## Security and privacy impact

    none.

    ## Alternatives considered

    Body.

    ## Consequences

    Body.

    ## Validation and conformance

    Body.

    ## Migration and rollback

    none.

    ## Unresolved questions

    none.
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

    def test_prefix_containing_a_digit_is_parsed(self) -> None:
        self.write(
            "p-stratum/p-0ap/ADR-P0AP-0001-deterministic-virtual-fabric.md",
            VALID.replace("adr: ADR-P-0001", "adr: ADR-P0AP-0001")
            .replace("scope: p-stratum", "scope: p-0ap")
            .replace("# ADR-P-0001:", "# ADR-P0AP-0001:"),
        )
        code, out, _ = self.run_tool()
        self.assertEqual(code, 0)
        self.assertIn("1 record(s)", out)

    def test_prefix_starting_with_a_digit_is_rejected(self) -> None:
        self.write("p-stratum/ADR-0P-0001-split.md", VALID)
        self.assert_rejected("filename must match")

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

    def test_optional_sections_are_accepted_in_canonical_position(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Decision\n", "## Decision drivers\n\nBody.\n\n## Decision\n")
            .replace(
                "## Security and privacy impact\n",
                "## Wire compatibility impact\n\nnone.\n\n## Implementation impact\n\nBody.\n\n## Security and privacy impact\n",
            ),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    def test_existing_affected_paths_are_accepted(self) -> None:
        (self.root / "canon").mkdir()
        (self.root / "canon" / "versioning.md").write_text("x", encoding="utf-8")
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_documents: []", "affected_documents: [canon/versioning.md]"),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    # Rejection.

    def test_missing_required_section_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Migration and rollback\n\nnone.\n\n", ""),
        )
        self.assert_rejected("missing required section(s) Migration and rollback")

    def test_unknown_section_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n", "## Notes\n\nBody.\n\n## Consequences\n"),
        )
        self.assert_rejected("unknown section(s) Notes")

    def test_repeated_section_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n", "## Consequences\n\nBody.\n\n## Consequences\n"),
        )
        self.assert_rejected("repeated section(s) Consequences")

    def test_sections_out_of_canonical_order_are_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n\nBody.\n\n", "").replace(
                "## Alternatives considered\n", "## Consequences\n\nBody.\n\n## Alternatives considered\n"
            ),
        )
        self.assert_rejected("sections are out of canonical order")

    def test_absolute_affected_path_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_documents: []", "affected_documents: [/etc/passwd]"),
        )
        self.assert_rejected("names absolute path /etc/passwd")

    def test_traversal_affected_path_is_rejected(self) -> None:
        outside = self.root.parent / "outside-the-repository.md"
        outside.write_text("x", encoding="utf-8")
        self.addCleanup(outside.unlink)
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_documents: []", f"affected_documents: [../{outside.name}]"),
        )
        self.assert_rejected("resolves outside the repository")

    def test_empty_affected_path_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_documents: []", 'affected_documents: [""]'),
        )
        self.assert_rejected("contains an empty path")

    def test_heading_inside_a_fence_is_not_a_section(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace(
                "## Consequences\n\nBody.\n",
                "## Consequences\n\n```markdown\n## Retry policy\n```\n\nBody.\n",
            ),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    def test_tilde_fence_is_also_stripped(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace(
                "## Consequences\n\nBody.\n",
                "## Consequences\n\n~~~text\n## Retry policy\n~~~\n\nBody.\n",
            ),
        )
        code, _, _ = self.run_tool()
        self.assertEqual(code, 0)

    def test_longer_fence_survives_an_inner_shorter_fence(self) -> None:
        # A four-backtick fence exists so a three-backtick block can be shown
        # literally; the inner run must not close the outer fence.
        example = "````markdown\n```\n## Retry policy\n```\n````"
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n\nBody.\n", f"## Consequences\n\n{example}\n\nBody.\n"),
        )
        code, _, err = self.run_tool()
        self.assertEqual(code, 0, err)

    def test_closing_fence_must_be_at_least_as_long_as_the_opening(self) -> None:
        example = "````\n```\n````"
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n\nBody.\n", f"## Consequences\n\n{example}\n\nBody.\n"),
        )
        self.assertEqual(self.run_tool()[0], 0)

    def test_required_section_only_inside_a_fence_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("## Consequences\n\nBody.\n", "```markdown\n## Consequences\n```\n"),
        )
        self.assert_rejected("missing required section(s) Consequences")

    def test_affected_path_that_does_not_exist_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("affected_contracts: []", "affected_contracts: [contracts/interfaces/p-r/9.9.9]"),
        )
        self.assert_rejected("affected_contracts names contracts/interfaces/p-r/9.9.9, which does not exist")

    def test_filename_without_a_scope_prefix_is_ignored(self) -> None:
        self.write("p-stratum/0001-split-p-stratum-into-p-lap-and-p-rap.md", VALID)
        code, out, _ = self.run_tool()
        # A filename without the ADR- prefix is not discovered as a record at all.
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

    def test_citation_without_a_scope_segment_is_rejected(self) -> None:
        self.write(
            "p-stratum/ADR-P-0001-split-p-stratum-into-p-lap-and-p-rap.md",
            VALID.replace("Body.", "This refines ADR-9999."),
        )
        self.assert_rejected("cites ADR-9999 without a scope segment")

    def test_full_identifier_in_the_body_is_not_flagged(self) -> None:
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
