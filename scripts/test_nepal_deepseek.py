import unittest
from analyze_nepal_deepseek import packet, validate


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.source = {'items': [{'id': 'a', 'links': [{'url': 'https://nta.gov.np/a'}]}]}
        fields = {k: 'Evidence-specific assessment' for k in ('change', 'customerImpact', 'competition', 'nextAction', 'uncertainty')}
        self.result = {'items': [{'id': 'a', 'evidenceUrls': ['https://nta.gov.np/a'], 'zh': fields.copy(), 'en': fields.copy()}]}

    def test_valid(self):
        self.assertEqual(validate(self.result, self.source), self.result)

    def test_invented_source(self):
        self.result['items'][0]['evidenceUrls'] = ['https://example.com/fake']
        with self.assertRaises(ValueError):
            validate(self.result, self.source)

    def test_missing_translation(self):
        del self.result['items'][0]['en']['change']
        with self.assertRaises(ValueError):
            validate(self.result, self.source)

    def test_wrong_id(self):
        self.result['items'][0]['id'] = 'invented'
        with self.assertRaises(ValueError):
            validate(self.result, self.source)

    def test_input_allowlist(self):
        report = {'issue': 'test', 'countries': {'np': {'sections': [{'items': [{'id': 'a', 'secret': 'private'}]}]}}}
        self.assertNotIn('secret', packet(report)['items'][0])

    def test_real_report_has_evidence(self):
        import json
        from analyze_nepal_deepseek import ROOT
        source = packet(json.loads((ROOT / 'config/nepal-report.json').read_text()))
        for item in source['items']:
            self.assertTrue(item['links'])
            self.assertTrue(all(link['url'].startswith('https://') for link in item['links']))
