import unittest
from unittest.mock import patch
from collect_nepal_sources import scan
from nepal_monitoring import classify


class PublisherSections(unittest.TestCase):
    def test_mobile_market_headline_is_not_lost(self):
        result = classify('4G users in Nepal: 2.69 crores')
        self.assertIn('market', [m['focusId'] for m in result['focusMatches']])
        self.assertTrue(result['requiresEditorialReview'])

    def test_nepalitelecom_sections_deduplicate_and_report_failure(self):
        source = {'id': 'np-nepalitelecom', 'platform': 'Website',
                  'url': 'https://www.nepalitelecom.com/', 'enabled': True}
        visited = []

        def fake(page):
            visited.append(page['url'])
            if page['url'].endswith('/nta'):
                return {**page, 'scanError': 'TimeoutError'}, [], []
            return {**page, 'lastCollectedAt': '2026-09-30T00:00:00Z'}, [
                {'url': 'https://www.nepalitelecom.com/shared-story', 'priority': 'HIGH'}
            ], []

        with patch('collect_nepal_sources.scan_page', side_effect=fake):
            state, items, _ = scan(source)
        self.assertEqual(visited, [source['url']] + [source['url'] + 'category/' + p
                         for p in ['nepal-telecom', 'ncell', 'isp', 'nta']])
        self.assertEqual(len(items), 1)
        self.assertEqual(len(state['scanPages']), 5)
        self.assertFalse(state['scanPages'][-1]['success'])
        self.assertIn('Partial', state['statusEn'])
        self.assertEqual(state['url'], source['url'])

    def test_disabled_publisher_not_fetched(self):
        with patch('collect_nepal_sources.scan_page') as fetch:
            scan({'id': 'np-nepalitelecom', 'platform': 'Website', 'enabled': False})
            fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
