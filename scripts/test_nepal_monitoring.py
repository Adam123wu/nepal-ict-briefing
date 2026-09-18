import unittest
from nepal_monitoring import canonical_url, classify

class MonitoringTests(unittest.TestCase):
    def test_keywords_do_not_verify_news(self):
        item=classify('Huawei Nepal solar project')
        self.assertEqual(item['priority'],'HIGH')
        self.assertTrue(item['requiresEditorialReview'])
        self.assertIn('energy',[m['focusId'] for m in item['focusMatches']])
    def test_disaster_requires_impact_review(self):
        self.assertEqual(classify('नेपालमा बाढी')['priority'],'HIGH')
    def test_acronym_boundary(self):
        self.assertEqual(classify('Santa celebrates')['priority'],'LOW')
    def test_nepali_joiner(self):
        self.assertIn('regulation',[m['focusId'] for m in classify('नेपाल दूरसञ्‍चार प्राधिकरण')['focusMatches']])
    def test_tracking_dedup(self):
        self.assertEqual(canonical_url('https://example.np/news?id=7&utm_source=x&fbclid=y#top'),'https://example.np/news?id=7')
    def test_competitor_match_requires_review(self):
        item=classify('Nokia and WorldLink नेपाल')
        self.assertEqual(item['priority'],'HIGH')
        self.assertIn('competitors',[m['focusId'] for m in item['focusMatches']])
        self.assertTrue(item['requiresEditorialReview'])

if __name__=='__main__': unittest.main()
