"""Seal each completed 14-day Nepal issue once, preserving bilingual content."""
import json
from datetime import date, datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo


def archive(root=Path('.'), today=None):
    today = today or datetime.now(ZoneInfo('Asia/Baghdad')).date()
    report = json.loads((root / 'config/nepal-report.json').read_text())
    start, end = map(date.fromisoformat, (report['windowStart'], report['windowEnd']))
    if (end - start).days != 13:
        raise ValueError('Archive requires a 14-day issue window')
    if today <= end:
        return False
    manifest_path = root / 'config/archive-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    filename = f'nepal-{start}-{end}.html'
    if any(i['file'] == filename for i in manifest):
        return False
    out = root / 'public/archive'
    out.mkdir(parents=True, exist_ok=True)
    def e(value):
        return escape(str(value), quote=True)
    body = []
    for lang in ('zh', 'en'):
        suffix = '' if lang == 'zh' else 'En'
        body.append(f'<section lang="{lang}"><h1>{e(report["period"+suffix])}</h1>')
        for section in report['countries']['np']['sections']:
            if not section['items']:
                continue
            body.append(f'<h2>{e(section["category"+suffix])}</h2>')
            for item in section['items']:
                body.append(f'<article><h3>{e(item["title"+suffix])}</h3><p>{e(item["date"])}</p><p>{e(item["text"+suffix])}</p><p>{e(item.get("opportunity"+suffix,""))}</p>')
                for link in item['links']:
                    if link['url'].startswith('https://'):
                        body.append(f'<a href="{e(link["url"])}">{e(link["label"])}</a> ')
                body.append('</article>')
        body.append('</section>')
    html = '<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nepal ICT archive</title><style>body{font:16px/1.8 system-ui;max-width:1000px;margin:auto;padding:24px;color:#172033}article{border-bottom:1px solid #ddd;padding:16px 0}a{overflow-wrap:anywhere}</style>' + ''.join(body) + '</html>'
    # Exclusive creation prevents accidental replacement of a sealed report.
    with (out / filename).open('x') as f:
        f.write(html)
    manifest.insert(0, {'file': filename, 'week': report['issue'], 'date': report['period'],
        'dateEn': report['periodEn'], 'current': False, 'archivedAt': today.isoformat()})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return True


if __name__ == '__main__':
    print('Archived completed issue' if archive() else 'No new completed issue to archive')
