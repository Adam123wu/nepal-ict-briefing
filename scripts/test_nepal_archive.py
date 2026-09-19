import json
from pathlib import Path
from datetime import date
import tempfile
import unittest
from archive_nepal import archive

class ArchiveTest(unittest.TestCase):
    def test_due_and_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'config').mkdir()
            report={'windowStart':'2026-09-05','windowEnd':'2026-09-18','issue':'W37-38','period':'中文','periodEn':'English','countries':{'np':{'sections':[]}}}
            (root/'config/nepal-report.json').write_text(json.dumps(report))
            (root/'config/archive-manifest.json').write_text('[]')
            self.assertFalse(archive(root,date(2026,9,18)))
            self.assertTrue(archive(root,date(2026,9,19)))
            path=next((root/'public/archive').glob('*.html'))
            before=path.read_bytes()
            self.assertFalse(archive(root,date(2026,10,3)))
            self.assertEqual(before,path.read_bytes())
            self.assertIn('English',path.read_text())
            self.assertIn('中文',path.read_text())
