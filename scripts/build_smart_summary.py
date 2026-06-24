from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

rows = []
miss = Counter()
for f in Path('collected').glob('**/*.json'):
    try:
        d = json.loads(f.read_text())
    except Exception:
        continue
    if 'covered_count' not in d:
        continue
    row = {
        'file': str(f),
        'mode': d.get('mode'),
        'covered_count': int(d.get('covered_count', 0)),
        'links': int(d.get('links', 0)),
        'missing': d.get('missing', []),
        'status': d.get('status'),
    }
    rows.append(row)
    for p in row['missing']:
        miss[tuple(p)] += 1

rows.sort(key=lambda r: (r['covered_count'], -r['links']), reverse=True)
summary = {
    'best': rows[0] if rows else None,
    'result_count': len(rows),
    'top_missing_points': [{'point': list(p), 'count': c} for p, c in miss.most_common(20)],
    'top_results': rows[:40],
}

out = Path('collected')
out.mkdir(parents=True, exist_ok=True)
(out / 'smart_run_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True))

md = ['# Smart run summary', '']
if rows:
    b = rows[0]
    md.append(f"Best: {b['covered_count']} / 64, links={b['links']}, mode={b['mode']}, status={b['status']}")
    md.append('')
    md.append('Best missing points:')
    for p in b['missing']:
        md.append(f'- {p}')
else:
    md.append('No JSON results found.')
md.append('')
md.append('Top recurring missing points:')
for x in summary['top_missing_points']:
    md.append(f"- {x['point']}: {x['count']}")
(out / 'smart_run_summary.md').write_text('\n'.join(md) + '\n')
print(json.dumps(summary, indent=2, sort_keys=True))
