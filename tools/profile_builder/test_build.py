"""Unit tests for tools/profile_builder/build.py."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402


class ProfileBuilderTests(unittest.TestCase):
    def test_selftest_passes(self) -> None:
        self.assertEqual(build.run_selftest(check_links=False), 0)

    def test_all_three_lanes_present(self) -> None:
        data = build.load_data()
        lanes = {w["lane"] for w in data["works"]}
        self.assertEqual(lanes, {"shipped", "inflight", "horizon"})

    def test_private_works_have_no_repo_links(self) -> None:
        data = build.load_data()
        private_items = [w for w in data["works"] if w["status"] == "PRIVATE"]
        self.assertGreaterEqual(len(private_items), 3)
        for item in private_items:
            self.assertNotIn("Repo", item.get("links", {}))
            self.assertNotIn("GitLab", item.get("links", {}))

    def test_excluded_items_absent(self) -> None:
        raw = json.dumps(build.load_data()).lower()
        for forbidden in ("cve-2026-112554", "aria-x", "cairn", "sudus", "region-lock", "geo-unlock"):
            self.assertNotIn(forbidden, raw)

    def test_replace_block_missing_marker_raises(self) -> None:
        with self.assertRaises(ValueError):
            build.replace_block("plain text", "nonexistent", "body")


if __name__ == "__main__":
    unittest.main()
