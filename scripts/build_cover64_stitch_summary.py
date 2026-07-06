from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

root = Path('collected')
root.mkdir(parents=True, exist_ok=True)

rows = []
for f in sorted(root.glob('**/cover64_stitch_best_shard_*.json')):
    try:
        d = json.loads(f.read_text())
    except Exception:
        continue
    if isinstance(d, dict) and 'covered_count' in d and 'lines2' in d:
        d['_file'] = str(f)
        rows.append(d)

def key(r):
    return (
        int(r.get('covered_count', 0)),
        int(r.get('overlap_largest_component', 0)),
        int(r.get('overlap_greedy_path', 0)),
        int(r.get('endpoint_largest_component', 0)),
        int(r.get('endpoint_greedy_path', 0)),
        int(r.get('score', 0)),
    )

rows.sort(key=key, reverse=True)
best = rows[0] if rows else None
modes = defaultdict(lambda: {'count': 0, 'cover64': 0, 'best_covered': 0, 'best_overlap_component': 0, 'best_overlap_path': 0, 'best_endpoint_component': 0, 'best_endpoint_path': 0})
cover_hist = Counter()
path_hist = Counter()
missing_counter = Counter()

for r in rows:
    mode = str(r.get('mode', 'unknown'))
    st = modes[mode]
    st['count'] += 1
    cc = int(r.get('covered_count', 0))
    cover_hist[cc] += 1
    path_hist[int(r.get('overlap_greedy_path', 0))] += 1
    st['best_covered'] = max(st['best_covered'], cc)
    if cc == 64:
        st['cover64'] += 1
    st['best_overlap_component'] = max(st['best_overlap_component'], int(r.get('overlap_largest_component', 0)))
    st['best_overlap_path'] = max(st['best_overlap_path'], int(r.get('overlap_greedy_path', 0)))
    st['best_endpoint_component'] = max(st['best_endpoint_component'], int(r.get('endpoint_largest_component', 0)))
    st['best_endpoint_path'] = max(st['best_endpoint_path'], int(r.get('endpoint_greedy_path', 0)))
    for p in r.get('missing', []) or []:
        missing_counter[tuple(p)] += 1

summary = {
    'schema': 'cover64-stitch-summary-v1',
    'result_count': len(rows),
    'cover64_count': sum(1 for r in rows if int(r.get('covered_count', 0)) == 64),
    'best': best,
    'best_covered_count': int(best.get('covered_count', 0)) if best else 0,
    'best_overlap_largest_component': int(best.get('overlap_largest_component', 0)) if best else 0,
    'best_overlap_greedy_path': int(best.get('overlap_greedy_path', 0)) if best else 0,
    'best_endpoint_largest_component': int(best.get('endpoint_largest_component', 0)) if best else 0,
    'best_endpoint_greedy_path': int(best.get('endpoint_greedy_path', 0)) if best else 0,
    'coverage_histogram': {str(k): v for k, v in sorted(cover_hist.items())},
    'overlap_path_histogram': {str(k): v for k, v in sorted(path_hist.items())},
    'top_missing_points': [{'point': list(p), 'count': c} for p, c in missing_counter.most_common(20)],
    'mode_breakdown': {m: st for m, st in sorted(modes.items())},
    'interpretation': 'unordered 22-line cover/stitch skeletons; not verified polygonal trails',
}

(root / 'cover64_stitch_run_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True))
with (root / 'cover64-stitch-candidates.jsonl').open('w') as fp:
    for r in rows:
        if int(r.get('covered_count', 0)) == 64:
            fp.write(json.dumps(r, sort_keys=True) + '\n')

md = ['# Cover64 stitch graph run summary', '']
if best:
    md += [
        f"Best covered_count: {best.get('covered_count')} / 64",
        f"Best mode: `{best.get('mode')}`",
        f"Best source shard: `{best.get('source_shard')}`",
        f"Overlap graph: component={best.get('overlap_largest_component')}/22, greedy_path={best.get('overlap_greedy_path')}/22, edges={best.get('overlap_edges')}",
        f"Endpoint graph: component={best.get('endpoint_largest_component')}/22, greedy_path={best.get('endpoint_greedy_path')}/22, edges={best.get('endpoint_edges')}",
        '',
    ]
else:
    md.append('No shard result JSON files found.')
md.append(f"Shard result count: {summary['result_count']}")
md.append(f"Cover64 count: {summary['cover64_count']}")
md.append('')
md.append('Mode breakdown:')
for mode, st in summary['mode_breakdown'].items():
    md.append(f"- `{mode}`: count={st['count']}, cover64={st['cover64']}, best_overlap_component={st['best_overlap_component']}, best_overlap_path={st['best_overlap_path']}, best_endpoint_component={st['best_endpoint_component']}, best_endpoint_path={st['best_endpoint_path']}")
md.append('')
md.append('Coverage histogram:')
for k, v in summary['coverage_histogram'].items():
    md.append(f'- {k}: {v}')
(root / 'cover64_stitch_run_summary.md').write_text('\n'.join(md) + '\n')
print(json.dumps(summary, indent=2, sort_keys=True))
