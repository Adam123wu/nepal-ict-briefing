"""Bounded public HTML extraction. No credentials, redirects or private hosts."""
import hashlib
import ipaddress
import socket
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.depth = 0
        self.parts = []
        self.article = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'nav', 'footer', 'header', 'noscript'}:
            self.skip += 1
        if tag in {'article', 'main'}:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'nav', 'footer', 'header', 'noscript'}:
            self.skip = max(0, self.skip - 1)
        if tag in {'article', 'main'}:
            self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        value = ' '.join(data.split())
        if value and not self.skip:
            self.parts.append(value)
            if self.depth:
                self.article.append(value)

    def text(self):
        return ' '.join(self.article or self.parts)


def public_host(host):
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    return bool(addresses) and all(ipaddress.ip_address(a[4][0]).is_global for a in addresses)


def fetch_article(url, allowed_hosts):
    parsed = urlparse(url)
    if (parsed.scheme != 'https' or parsed.hostname not in allowed_hosts
            or parsed.username or parsed.password or parsed.port not in (None, 443)
            or not public_host(parsed.hostname)):
        raise ValueError('Unapproved article host')

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    request = urllib.request.Request(url, headers={'User-Agent': 'NepalICTBriefing/1.0'})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=15) as response:
        if 'text/html' not in response.headers.get('Content-Type', ''):
            raise ValueError('Not an HTML article')
        raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError('Article exceeds size limit')
        parser = ArticleText()
        parser.feed(raw.decode(response.headers.get_content_charset() or 'utf-8', errors='replace'))
    text = parser.text()
    if len(text) < 400 or any(x in text[:1500].lower() for x in ('verify you are human', 'access denied', 'just a moment')):
        raise ValueError('Missing article text or access challenge')
    return text[:12000], hashlib.sha256(raw).hexdigest()
