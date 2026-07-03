from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


def load_json_rows(root: Path):
    rows = []
    for f in root.glob('**/*'):
        if not f.is_file():
            continue
        if f.suffix == '.json':
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            if isinstance(d, dict) and 'covered_count' in d:
                d['_file'] = str(f)
                rows.append(d)
        elif f.suffix == '.jsonl':
            try:
                lines = f.read_text().splitlines()
            except Exception:
                continue
            for line in lines:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if isinstance(d, dict) and 'covered_count' in d:
                    d['_file'] = str(f)
                    rows.append(d)
    return rows


def missing_key(missing):
    return tuple(tuple(p) for p in sorted(missing or []))


def compact_key(row):
    if row.get('canonical_key_sha256'):
        return str(row['canonical_key_sha256'])
    if row.get('candidate_id'):
        return str(row['candidate_id'])
    return json.dumps(row.get('vertices2', []), sort_keys=True)


root = Path('collected')
root.mkdir(parents=True, exist_ok=True)
rows = load_json_rows(root)
rows.sort(key=lambda r: (int(r.get('covered_count', 0)), -int(r.get('links', 999)), str(r.get('mode', ''))), reverse=True)

miss_counter = Counter()
miss_family_counter = Counter()
mode_stats = defaultdict(lambda: {'count': 0, 'best': 0, 'relay60_or_better': 0, 'families': set(), 'compact': set()})
compact60 = set()
relay60_rows = []
old_wall = missing_key([[0,0,1],[0,2,3],[0,3,1],[2,1,1]])
old_wall_count = 0

for r in rows:
    cc = int(r.get('covered_count', 0))
    links = int(r.get('links', 0))
    mode = str(r.get('mode', 'unknown'))
    mk = missing_key(r.get('missing', []))
    ck = compact_key(r)
    miss_family_counter[mk] += 1
    if mk == old_wall:
        old_wall_count += 1
    for p in r.get('missing', []) or []:
        miss_counter[tuple(p)] += 1
    st = mode_stats[mode]
    st['count'] += 1
    st['best'] = max(st['best'], cc)
    st['families'].add(mk)
    st['compact'].add(ck)
    if cc >= 60 and links <= 22:
        st['relay60_or_better'] += 1
        compact60.add(ck)
        relay60_rows.append(r)

best = rows[0] if rows else None
summary = {
    'schema': 'defect-relay-summary-v1',
    'best': best,
    'result_count': len(rows),
    'relay60_or_better_count': len(relay60_rows),
    'unique_compact_60_or_better': len(compact60),
    'unique_missing_families_all': len(miss_family_counter),
    'old_wall_repeat_count': old_wall_count,
    'top_missing_points': [{'point': list(p), 'count': c} for p, c in miss_counter.most_common(20)],
    'top_missing_families': [{'missing': [list(p) for p in fam], 'count': c} for fam, c in miss_family_counter.most_common(20)],
    'mode_breakdown': {
        mode: {
            'count': st['count'],
            'best': st['best'],
            'relay60_or_better': st['relay60_or_better'],
            'unique_missing_families': len(st['families']),
            'unique_compact': len(st['compact']),
        }
        for mode, st in sorted(mode_stats.items())
    },
}

(root / 'defect_relay_run_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True))

with (root / 'relay60-diversity.jsonl').open('w') as fp:
    seen = set()
    for r in relay60_rows:
        key = (compact_key(r), missing_key(r.get('missing', [])))
        if key in seen:
            continue
        seen.add(key)
        fp.write(json.dumps(r, sort_keys=True) + '\n')

md = ['# Defect relay run summary', '']
if best:
    md.append(f"Best: {best.get('covered_count')} / 64, links={best.get('links')}, mode={best.get('mode')}, status={best.get('status')}")
    md.append('')
    md.append('Best missing points:')
    for p in best.get('missing', []) or []:
        md.append(f'- {p}')
else:
    md.append('No JSON results found.')
md.append('')
md.append(f"Relay 60-or-better rows: {summary['relay60_or_better_count']}")
md.append(f"Unique compact 60-or-better: {summary['unique_compact_60_or_better']}")
md.append(f"Unique missing families: {summary['unique_missing_families_all']}")
md.append(f"Old four-hole wall repeats: {summary['old_wall_repeat_count']}")
md.append('')
md.append('Mode breakdown:')
for mode, st in summary['mode_breakdown'].items():
    md.append(f"- {mode}: best={st['best']}, count={st['count']}, relay60+={st['relay60_or_better']}, missing_families={st['unique_missing_families']}, compact={st['unique_compact']}")
md.append('')
md.append('Top missing families:')
for x in summary['top_missing_families'][:10]:
    md.append(f"- {x['missing']}: {x['count']}")
(root / 'defect_relay_run_summary.md').write_text('\n'.join(md) + '\n')

print(json.dumps(summary, indent=2, sort_keys=True))
