import unittest
from unittest.mock import patch
from collect_nepal_sources import scan, scan_page

class Response:
    def __init__(self, url, body): self.url,self.body=url,body
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def geturl(self): return self.url
    def read(self,*args): return self.body.encode()

class CollectorTests(unittest.TestCase):
    source={'id':'np-nepalkhabar','platform':'Website','url':'https://nepalkhabar.com/'}
    def test_article_without_keyword_is_retained(self):
        html='<a href="/politics/287123-2026-9-18-12-0-0">मन्त्रीको नयाँ निर्णय सार्वजनिक भयो</a>'
        with patch('collect_nepal_sources.urlopen',return_value=Response(self.source['url'],html)):
            _,items,_=scan_page(self.source)
        self.assertEqual(len(items),1)
        self.assertIsNone(items[0]['publishedAt'])
        self.assertTrue(items[0]['requiresEditorialReview'])
    def test_sections_deduplicate_and_report_partial_failure(self):
        def fetch(req,**kwargs):
            if req.full_url.endswith('/category/politics'): raise TimeoutError()
            return Response(req.full_url,'<a href="/economy/287123-2026-9-18-12-0-0">A detailed new announcement</a>')
        with patch('collect_nepal_sources.urlopen',side_effect=fetch):
            state,items,_=scan(self.source)
        self.assertEqual(len(state['scanPages']),4)
        self.assertEqual(len(items),1)
        self.assertIn('Partial',state['statusEn'])
        self.assertEqual(state['url'],self.source['url'])
    def test_social_not_claimed_as_scanned(self):
        source={**self.source,'platform':'Facebook'}
        self.assertEqual(scan(source),(source,[],[]))
    def test_newbiz_article_without_ict_is_retained(self):
        source={**self.source,'id':'np-newbusinessage','url':'https://www.newbusinessage.com/'}
        html='<a href="/news/50179/a-new-diplomatic-development/">A new diplomatic development</a>'
        with patch('collect_nepal_sources.urlopen',return_value=Response(source['url'],html)):
            _,items,_=scan_page(source)
        self.assertEqual(len(items),1)
        self.assertTrue(items[0]['requiresEditorialReview'])

if __name__=='__main__': unittest.main()
