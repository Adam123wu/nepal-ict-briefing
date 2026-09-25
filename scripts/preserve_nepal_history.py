"""Preserve each completed 14-day Nepal issue as structured briefing data."""
import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def preserve(root=Path('.'), today=None):
    today = today or datetime.now(ZoneInfo('Asia/Baghdad')).date()
    report = json.loads((root / 'config/nepal-report.json').read_text())
    start, end = map(date.fromisoformat, (report['windowStart'], report['windowEnd']))
    if (end - start).days != 13:
        raise ValueError('History requires a 14-day issue window')
    if today <= end:
        return False

    history_path = root / 'config/history-reports.json'
    history = json.loads(history_path.read_text())
    if any(
        item['issue'] == report['issue']
        or (item['windowStart'] == str(start) and item['windowEnd'] == str(end))
        for item in history
    ):
        return False

    completed = dict(report)
    completed['current'] = False
    sections = report['countries']['np']['sections']
    count = sum(len(section['items']) for section in sections)
    completed['status'] = f'历史完整期，共 {count} 条核验事件。'
    completed['statusEn'] = f'Completed historical issue with {count} reviewed events.'
    completed['stats'] = {
        'news': count,
        'opportunities': sum(
            bool(item.get('opportunity'))
            for section in sections
            for item in section['items']
        ),
        'telegram': 0,
        'countryCounts': {'np': count},
    }
    history.insert(0, completed)
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n')
    return True


if __name__ == '__main__':
    print('Preserved completed issue' if preserve() else 'No completed issue to preserve')
