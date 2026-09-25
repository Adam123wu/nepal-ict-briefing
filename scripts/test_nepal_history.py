import json
from pathlib import Path
from datetime import date
import tempfile
import unittest

from preserve_nepal_history import preserve


class HistoryTest(unittest.TestCase):
    def test_due_and_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'config').mkdir()
            report = {
                'windowStart': '2026-09-05',
                'windowEnd': '2026-09-18',
                'issue': 'W37-38',
                'period': '中文',
                'periodEn': 'English',
                'countries': {'np': {'sections': []}},
            }
            (root / 'config/nepal-report.json').write_text(json.dumps(report))
            path = root / 'config/history-reports.json'
            path.write_text('[]')

            self.assertFalse(preserve(root, date(2026, 9, 18)))
            self.assertTrue(preserve(root, date(2026, 9, 19)))
            before = path.read_bytes()
            self.assertFalse(preserve(root, date(2026, 10, 3)))
            self.assertEqual(before, path.read_bytes())

            history = json.loads(path.read_text())
            self.assertEqual(history[0]['status'], '历史完整期，共 0 条核验事件。')
            self.assertEqual(history[0]['periodEn'], 'English')
            self.assertEqual(history[0]['period'], '中文')
