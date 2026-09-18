"""Attachment-derived candidate triage. This module never approves news."""
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

FOCUS = json.loads((Path(__file__).resolve().parents[1] / 'config/monitoring-focus.json').read_text())['focusAreas']
VENDORS = ['Nokia', 'ZTE', 'Ericsson', 'Cisco', 'Juniper', 'Extreme Networks', 'Eutelsat', 'OneWeb', 'नोकिया', 'जेडटीई', 'एरिक्सन', 'सिस्को', 'जुनिपर', 'युटेलस्याट', 'वनवेब']
RANK = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
VENDORS += ['中兴', '思科', 'Whale Cloud', 'WhaleCloud', 'iWhaleCloud', '浩鲸', 'AsiaInfo', '亚信', 'H3C', '新华三', 'FiberHome', '烽火']
ALIASES = {
    'huawei': ['huawei', 'ह्वावे', 'हुवावे'],
    'operators': ['ncell', 'ntc', 'nepal telecom', 'worldlink', 'vianet', 'subisu', 'classic tech', 'cgnet', 'एनसेल', 'टेलिकम'],
    'regulation': ['nta', 'spectrum', 'licensing', 'दूरसञ्चार', 'प्राधिकरण'],
    'government': ['mocit', 'digital nepal'],
    'technology': ['5g', 'iot', 'ict', 'data centre', 'data center', 'wifi', 'wi-fi'],
    'energy': ['solar', 'renewable', 'सोलार', 'नवीकरणीय'],
    'economy': ['digital economy', 'infrastructure', 'पूर्वाधार'],
    'disaster': ['flood', 'landslide', 'earthquake', 'disaster', 'बाढी', 'पहिरो', 'भूकम्प'],
}

def normalize(value):
    return unicodedata.normalize('NFKC', value).replace('\u200d', '').replace('\u200c', '').casefold()

def contains(text, keyword):
    word = normalize(keyword)
    if not word:
        return False
    if word.isascii():
        return re.search(r'(?<![a-z0-9])' + re.escape(word) + r'(?![a-z0-9])', text) is not None
    return word in text

def classify(text):
    text = normalize(text)
    matches = []
    for area in FOCUS:
        keywords = [k for k in area['keywords'] + ALIASES.get(area['id'], []) if contains(text, k)]
        if keywords:
            matches.append({'focusId': area['id'], 'keywords': list(dict.fromkeys(keywords))[:8]})
    priorities = [a['priority'] for a in FOCUS if any(m['focusId'] == a['id'] for m in matches)]
    vendors = [v for v in VENDORS if contains(text, v)]
    if vendors:
        matches.append({'focusId': 'competitors', 'keywords': vendors})
        priorities.append('HIGH')
    priority = min(priorities, key=RANK.get) if priorities else 'LOW'
    # Headlines cannot establish that a disaster actually affected an ICT asset.
    if priority == 'CRITICAL':
        priority = 'HIGH'
    return {'priority': priority, 'focusMatches': matches, 'requiresEditorialReview': True}

def canonical_url(url):
    p = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in ('fbclid', 'gclid', 'msclkid')]
    return urlunsplit((p.scheme, p.netloc, p.path, urlencode(query), ''))
