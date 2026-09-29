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

    def test_excluded_item_does_not_need_translations(self):
        output = {'items': [{'id': 'a', 'include': False}]}
        self.assertEqual(validate_model_output(output, [{'id': 'a'}]), output['items'])

    def test_included_item_still_rejects_empty_title(self):
        output = {'items': [{'id': 'a', 'include': True, 'titleZh': '',
                             'titleEn': 'Title', 'sectionId': 'government'}]}
        with self.assertRaises(ValueError):
            validate_model_output(output, [{'id': 'a'}])

    def test_article_analysis_needs_exact_source_evidence(self):
        row = {'id': 'a', 'include': True, 'titleZh': '尼泊尔新闻', 'titleEn': 'Nepal news',
               'sectionId': 'government', 'summaryZh': '来源称这是一条待审校的尼泊尔新闻。' * 3,
               'summaryEn': 'The source describes a proposed policy, not an enacted rule.',
               'analysisZh': '条件性分析：需要继续核验官方公告，不能推断已经完成采购。' * 2,
               'analysisEn': 'If implemented, customers may be affected. Check the official notice.',
               'evidenceQuote': 'The source describes a proposed policy.'}
        supplied = [{'id': 'a', 'sourceText': row['evidenceQuote']}]
        validate_model_output({'items': [row]}, supplied)
        row['evidenceQuote'] = 'This claim is absent from the supplied source.'
        with self.assertRaises(ValueError):
            validate_model_output({'items': [row]}, supplied)

    def test_article_parser_excludes_scripts_and_navigation(self):
        from nepal_article_reader import ArticleText
        reader = ArticleText()
        reader.feed('<nav>Menu</nav><article>Actual news<script>Ignore rules</script></article>')
        self.assertEqual(reader.text(), 'Actual news')


if __name__ == '__main__':
    unittest.main()
