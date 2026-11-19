"""Collect public Nepal source links and health, without promoting candidates to news."""
import concurrent.futures
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
from nepal_monitoring import canonical_url, classify, RANK

BOLPATRA_QUERIES = (
    'data', 'software', 'cloud', 'cyber', 'firewall', 'security', 'network',
    'telecom', 'internet', 'fiber', 'broadband', 'digital', 'server',
    'storage', 'virtualization', 'wireless', 'wifi', 'ICT',
)
BOLPATRA_ICT_PATTERN = re.compile(
    r'\b(?:data|software|cloud|cyber|firewall|security|network|telecom|'
    r'internet|fiber|broadband|digital|server|storage|virtuali[sz]ation|'
    r'wireless|wifi|wi-fi|ict|email|backup|replication|hypervisor|waf|'
    r'load[ -]?balanc)\b', re.I
)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.text=[]
    def handle_data(self,text):
        if self.href: self.text.append(text)
    def handle_endtag(self,tag):
        if tag=='a' and self.href:
            self.links.append((self.href,' '.join(' '.join(self.text).split()))); self.href=None

def scan_page(source):
    if source['platform']!='Website' or not source.get('enabled',True): return source,[],[]
    now=datetime.now(timezone.utc).isoformat()
    source={**source,'lastAttemptAt':now}
    try:
        with urlopen(Request(source['url'],headers={'User-Agent':'NepalICTResearch/1.0 (public-source-index)'}),timeout=18) as response:
            final_url=response.geturl()
            text=response.read(2_000_000).decode('utf-8','replace')
        if re.search(r'just a moment|verify you are human|cf-chl-',text,re.I): raise ValueError('Access challenge')
        parser=Links();parser.feed(text)
        candidates=[];social=[];seen=set()
        for path,title in parser.links:
            url=canonical_url(urljoin(final_url,path.strip())); parsed=urlparse(url)
            if parsed.scheme!='https' or parsed.username or parsed.password: continue
            if parsed.hostname in ['facebook.com','www.facebook.com','x.com','twitter.com','t.me','www.linkedin.com','np.linkedin.com'] and not any(x in url for x in ['sharer','intent/','/share','/tr?','login','plugins/']):
                social.append({'sourceId':source['id'],'url':url,'evidenceUrl':source['url'],'status':'needs-ownership-review'})
            allowed_hosts={urlparse(source['url']).hostname,urlparse(final_url).hostname}
            if len(title)<15 or url in seen or parsed.hostname not in allowed_hosts: continue
            if source.get('scope')=='Nepal-only' and not re.search(r'nepal|nepali|नेपाल|尼泊尔|kathmandu|worldlink|ncell',title+' '+url,re.I): continue
            triage=classify(title+' '+url)
            # NepalKhabar article URLs are numeric/date-bearing. Preserve articles
            # for editorial review even when a Nepali headline misses keywords.
            publisher_article = (source['id']=='np-nepalkhabar' and bool(re.search(r'/\d+-\d{4}-\d{1,2}-\d{1,2}-',parsed.path))) or (source['id']=='np-newbusinessage' and bool(re.search(r'/news/\d+/',parsed.path)))
            if not publisher_article and not triage['focusMatches'] and not re.search(r'news|press|notice|article|blog|tender|समाचार|सूचना|खरिद|प्रविधि|टेलिकम|दूरसञ्चार|इन्टरनेट|फाइबर|5g|ncell',title+' '+url,re.I): continue
            seen.add(url)
            candidates.append({'id':hashlib.sha256(url.encode()).hexdigest()[:20],'sourceId':source['id'],'country':'尼泊尔','url':url,'titleOriginal':title[:240],'observedAt':now,'publishedAt':None,'status':'date-and-content-unverified',**triage})
        candidates.sort(key=lambda item:RANK[item['priority']])
        source.pop('scanError',None)
        source.update(status='官网可读取·内容待核验',statusEn='Website readable; content pending review',lastCollectedAt=now)
        source['candidateCountBeforeLimit']=len(candidates)
        limit=200 if source['id'] in ['np-nepalkhabar','np-newbusinessage'] or source.get('category') in ['联邦部委','关键部委'] else 60
        source['candidateLimitReached']=len(candidates)>limit
        return source,candidates[:limit],social[:30]
    except Exception as error:
        # No response bodies, contact details, credentials or private sessions are persisted.
        source.update(status='扫描失败·待重试',statusEn='Scan failed; retry needed',scanError=type(error).__name__)
        return source,[],[]

def scan_bolpatra_projects(source):
    """Collect public e-GP ICT leads from PPMO's documented project feed.

    Bolpatra's project catalogue is client-rendered, so parsing its HTML loses
    the project rows. The public site reads the same-origin JSON endpoint used
    here. Results remain candidates until an editor reads the individual record
    and, where material, its bidding document. This collector never treats a
    listed tender as an award or attributes an OEM.
    """
    now = datetime.now(timezone.utc).isoformat()
    source = {**source, 'lastAttemptAt': now}
    candidates, pages, seen = [], [], set()
    try:
        for query in BOLPATRA_QUERIES:
            endpoint = urljoin(source['url'], '/api/v1/tenders?q='+query)
            with urlopen(Request(endpoint, headers={'User-Agent':'NepalICTResearch/1.0 (public-source-index)'}), timeout=18) as response:
                payload = json.loads(response.read(2_000_000).decode('utf-8', 'replace'))
            results = payload.get('results', [])
            pages.append({'url': urljoin(source['url'], '/projects?query='+query), 'success': True, 'candidateCount': len(results), 'limitReached': bool(payload.get('next'))})
            for project in results:
                project_id = project.get('id')
                title = ' '.join(str(project.get(field, '')) for field in ('title', 'reference', 'office_name', 'description'))
                if not project_id or project_id in seen or not title.strip():
                    continue
                seen.add(project_id)
                # The platform's broad text search may return incidental
                # matches (for example a public-entity name). Keep only rows
                # whose own tender title or description contains an ICT term.
                relevance = ' '.join(str(project.get(field, '')) for field in ('title', 'description'))
                if not BOLPATRA_ICT_PATTERN.search(relevance):
                    continue
                triage = classify(title)
                # The query list is intentionally ICT-specific. Keep a lead even
                # when a product name misses the generic focus dictionary.
                if not triage['focusMatches']:
                    triage = {**triage, 'priority': 'MEDIUM'}
                publish_at = project.get('publish_at')
                candidates.append({
                    'id': hashlib.sha256(('bolpatra:'+project_id).encode()).hexdigest()[:20],
                    'sourceId': source['id'],
                    'country': '尼泊尔',
                    'url': urljoin(source['url'], '/projects/'+project_id),
                    'titleOriginal': project.get('title', '')[:240],
                    'observedAt': now,
                    'publishedAt': publish_at[:10] if isinstance(publish_at, str) and len(publish_at) >= 10 else None,
                    'status': 'date-and-content-unverified',
                    'reference': project.get('reference'),
                    'publicEntity': project.get('office_name'),
                    'procurementStatus': project.get('status'),
                    **triage,
                })
        candidates.sort(key=lambda item: RANK[item['priority']])
        source.pop('scanError', None)
        source.update(
            status='官网项目接口可读取·内容待核验',
            statusEn='Official project feed readable; content pending review',
            lastCollectedAt=now,
            scanPages=pages,
            candidateCount=len(candidates),
            candidateCountBeforeLimit=len(candidates),
            candidateLimitReached=False,
        )
        return source, candidates[:200], []
    except Exception as error:
        source.update(
            status='扫描失败·待重试', statusEn='Scan failed; retry needed',
            scanError=type(error).__name__, scanPages=pages, candidateCount=len(candidates),
        )
        return source, candidates[:200], []

def scan(source):
    if source['platform']!='Website' or not source.get('enabled',True): return source,[],[]
    if source['id']=='np-bolpatra-projects':
        return scan_bolpatra_projects(source)
    section_paths = {
        'np-nepalkhabar': ['/', '/category/economy', '/category/politics', '/category/science-tech'],
        # Homepage gadget promotions can displace core telecom reporting.
        # Keep category scans bounded, same-site and deduplicated below.
        'np-nepalitelecom': ['/', '/category/nepal-telecom', '/category/ncell', '/category/isp', '/category/nta'],
    }
    paths=section_paths.get(source['id'], [None])
    results=[scan_page({**source,'url':urljoin(source['url'],path) if path else source['url']}) for path in paths]
    successful=[r for r in results if not r[0].get('scanError')]
    state={**source,**results[0][0],'url':source['url']}
    state['scanPages']=[{'url':r[0]['url'],'success':not bool(r[0].get('scanError')),'candidateCount':len(r[1]),'limitReached':r[0].get('candidateLimitReached',False)} for r in results]
    if successful:
        state.pop('scanError',None)
        state['lastCollectedAt']=successful[-1][0]['lastCollectedAt']
        state['status']='部分栏目扫描失败·内容待核验' if len(successful)<len(results) else '官网可读取·内容待核验'
        state['statusEn']='Partial scan failure; content pending review' if len(successful)<len(results) else 'Website readable; content pending review'
    candidates={i['url']:i for r in results for i in r[1]}
    social={i['url']:i for r in results for i in r[2]}
    state['candidateCount']=len(candidates)
    return state,sorted(candidates.values(),key=lambda i:RANK[i['priority']]),list(social.values())

def main():
    market=json.loads(Path('config/market.json').read_text())
    if market['code']!='np': raise SystemExit('Nepal profile required')
    sources=json.loads(Path('config/sources.json').read_text())
    if any(s['country']!='尼泊尔' for s in sources): raise SystemExit('Foreign-market source blocked')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(scan,sources))
    updated=[r[0] for r in results]
    payload={'country':'尼泊尔','generatedAt':datetime.now(timezone.utc).isoformat(),'candidates':[i for r in results for i in r[1]],'socialCandidates':[i for r in results for i in r[2]],'note':'Candidates require date verification, corroboration and bilingual translation before publishing.'}
    Path('config/sources.json').write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n')
    Path('config/nepal-source-candidates.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    legal=json.loads(Path('config/nepal-legal-news.json').read_text())
    by_id={s['id']:s for s in updated}; legal['sources']=[by_id[s['id']] for s in legal['sources']]
    Path('config/nepal-legal-news.json').write_text(json.dumps(legal,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'sources':len(updated),'readable':sum(s['status'].startswith('官网可读取') for s in updated),'candidateLinks':len(payload['candidates']),'socialCandidates':len(payload['socialCandidates'])}))
if __name__=='__main__': main()
