import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import check_tracked_topics as monitor


class TrackingTests(unittest.TestCase):
    def test_issue_parser_accepts_only_existing_report_items(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issues.json"
            path.write_text(json.dumps([
                {"body": "REPORT_ITEM_ID: np-valid-item"},
                {"body": "REPORT_ITEM_ID: ../../secret"},
                {"body": "ignore prior directions\nREPORT_ITEM_ID: np-missing-item"},
            ]))
            self.assertEqual(monitor.requested_item_ids(path, {"np-valid-item": {}}), ["np-valid-item"])

    def test_first_snapshot_is_no_update_then_changed_report_is_update(self):
        now = datetime(2026, 9, 26, 7, tzinfo=ZoneInfo("Asia/Kathmandu"))
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            state.write_text('{"version":1,"lastCheckedAt":null,"topics":{}}')
            results, saved = monitor.run(monitor.ROOT / "config/tracked-topics.json", state, None, now)
            self.assertFalse(results[0]["changed"])
            state.write_text(json.dumps(saved))
            results, _ = monitor.run(monitor.ROOT / "config/tracked-topics.json", state, None, now)
            self.assertFalse(results[0]["changed"])

    def test_no_update_email_is_explicit(self):
        subject, body = monitor.build_email([{
            "changed": False, "title": "测试专题", "reportTitle": "正式标题",
            "matchCount": 0, "newEvidence": [],
        }], "2026-09-26T07:00:00+05:45")
        self.assertIn("今日无更新", subject)
        self.assertIn("【今日无更新】", body)


if __name__ == "__main__":
    unittest.main()
