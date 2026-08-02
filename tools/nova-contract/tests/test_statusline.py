# SPDX-License-Identifier: Apache-2.0
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATUSLINE = ROOT / ".claude" / "statusline.sh"


def usage(request_id: str, fresh: int, created: int, cached: int, out: int) -> dict:
    return {
        "type": "assistant",
        "requestId": request_id,
        "message": {
            "usage": {
                "input_tokens": fresh,
                "cache_creation_input_tokens": created,
                "cache_read_input_tokens": cached,
                "output_tokens": out,
            }
        },
    }


@unittest.skipIf(shutil.which("jq") is None, "jq is not available")
class StatusLineTests(unittest.TestCase):
    def render(self, records: list[dict] | None) -> str:
        with tempfile.TemporaryDirectory() as directory:
            payload = {
                "model": {"display_name": "Test"},
                "workspace": {"current_dir": str(ROOT)},
            }
            if records is not None:
                transcript = Path(directory) / "transcript.jsonl"
                transcript.write_text(
                    "".join(json.dumps(record) + "\n" for record in records),
                    encoding="utf-8",
                )
                payload["transcript_path"] = str(transcript)
            result = subprocess.run(
                ["bash", str(STATUSLINE)],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout

    def test_latest_turn_is_the_last_record_not_the_greatest_id(self):
        """Request ids are unordered, so transcript order decides the newest turn."""
        rendered = self.render(
            [
                usage("req_zzz_first", 1, 9, 90, 100),
                usage("req_aaa_latest", 2, 18, 980, 7),
            ]
        )
        self.assertIn("1.0k/", rendered)
        self.assertIn("↑20", rendered)
        self.assertIn("↓7", rendered)

    def test_duplicate_records_are_counted_once(self):
        duplicated = self.render(
            [
                usage("req_one", 1, 9, 90, 100),
                usage("req_one", 1, 9, 90, 100),
                usage("req_two", 2, 18, 980, 7),
            ]
        )
        self.assertIn("Σ↓107", duplicated)

    def test_session_total_sums_every_distinct_request(self):
        rendered = self.render(
            [
                usage("req_one", 1, 1, 1, 40),
                usage("req_two", 1, 1, 1, 60),
                usage("req_three", 1, 1, 1, 500),
            ]
        )
        self.assertIn("Σ↓600", rendered)

    def test_identity_fields_are_always_present(self):
        self.assertIn("[Test]", self.render([usage("req_one", 1, 1, 1, 5)]))

    def test_absent_transcript_degrades_to_identity_only(self):
        rendered = self.render(None)
        self.assertIn("[Test]", rendered)
        self.assertNotIn("\U0001f9ee", rendered)

    def test_transcript_without_usage_degrades_to_identity_only(self):
        rendered = self.render([{"type": "user", "message": {"role": "user"}}])
        self.assertIn("[Test]", rendered)
        self.assertNotIn("\U0001f9ee", rendered)


if __name__ == "__main__":
    unittest.main()
