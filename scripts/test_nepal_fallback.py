import datetime as dt
import unittest

from fallback_nepal_deepseek import candidate_date, eligible_candidates, is_safe_https_url, validate_model_output


class FallbackTests(unittest.TestCase):
    def setUp(self):
        self.report = {'windowStart': '2026-09-19', 'windowEnd': '2026-10-02',
                       'countries': {'np': {'sections': [{'items': []}]}}}
        self.sources = [{'id': 'np-official', 'name': 'Official', 'nameEn': 'Official',
                         'tier': 'T1', 'platform': 'Website', 'scanError': None}]
        self.candidate = {'id': 'a', 'sourceId': 'np-official', 'country': '尼泊尔',
                          'url': 'https://news.example/2026/09/20/item',
                          'titleOriginal': 'नेपाल डिजिटल शासनसम्बन्धी नयाँ सूचना प्रकाशित',
                          'observedAt': '2026-09-20T23:00:00+00:00', 'publishedAt': None,
                          'priority': 'HIGH', 'focusMatches': [{'focusId': 'government'}]}

    def test_date_from_url(self):
        self.assertEqual(candidate_date(self.candidate), dt.date(2026, 9, 20))

    def test_public_url_must_be_safe_https(self):
        self.assertTrue(is_safe_https_url(self.candidate['url']))
        self.assertFalse(is_safe_https_url('http://news.example/item'))
        self.assertFalse(is_safe_https_url('https://user:secret@news.example/item'))

    def test_eligible_requires_dated_trusted_source(self):
        result = eligible_candidates({'candidates': [self.candidate]}, self.sources,
                                     self.report, set(), dt.date(2026, 9, 21))
        self.assertEqual([row['id'] for row in result], ['a'])
        self.sources[0]['scanError'] = 'HTTPError'
        self.assertEqual(eligible_candidates({'candidates': [self.candidate]}, self.sources,
                                             self.report, set(), dt.date(2026, 9, 21)), [])

    def test_existing_report_url_is_excluded(self):
        self.report['countries']['np']['sections'][0]['items'] = [
            {'links': [{'url': self.candidate['url']}]}]
        self.assertEqual(eligible_candidates({'candidates': [self.candidate]}, self.sources,
                                             self.report, set(), dt.date(2026, 9, 21)), [])

    def test_model_output_validation(self):
        supplied = [{'id': 'a'}]
        output = {'items': [{'id': 'a', 'include': True, 'titleZh': '尼泊尔数字治理新公告',
                             'titleEn': 'New Nepal digital governance notice',
                             'sectionId': 'government'}]}
        self.assertEqual(validate_model_output(output, supplied), output['items'])

    def test_model_cannot_invent_id(self):
        output = {'items': [{'id': 'invented', 'include': True, 'titleZh': '尼泊尔数字治理新公告',
                             'titleEn': 'New Nepal digital governance notice',
                             'sectionId': 'government'}]}
        with self.assertRaises(ValueError):
            validate_model_output(output, [{'id': 'a'}])


if __name__ == '__main__':
    unittest.main()
