from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(root: Path):
    rows = []
    for f in root.glob('**/*'):
        if not f.is_file():
            continue
        if f.suffix == '.json':
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            if isinstance(d, dict) and d.get('schema') == 'cover64-stitch-line-set-v1' and d.get('line_set2'):
                d['_file'] = str(f)
                rows.append(d)
        elif f.suffix == '.jsonl':
            for line in f.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if isinstance(d, dict) and d.get('schema') == 'cover64-stitch-line-set-v1' and d.get('line_set2'):
                    d['_file'] = str(f)
                    rows.append(d)
    return rows


def compact_key(row):
    if row.get('candidate_id'):
        return str(row['candidate_id'])
    return json.dumps(row.get('line_set2', []), sort_keys=True, separators=(',', ':'))


def main():
    root = Path('collected')
    root.mkdir(parents=True, exist_ok=True)
    rows = load_rows(root)
    rows.sort(
        key=lambda r: (
            int(r.get('covered_count', 0)),
            int(r.get('stitch_path_lower_bound', 0)),
            int(r.get('max_component_size', 0)),
            -int(r.get('stitch_components', 99)),
            float(r.get('score', 0)),
        ),
        reverse=True,
    )
    best = rows[0] if rows else None
    mode_stats = defaultdict(lambda: {'count': 0, 'best_covered': 0, 'best_stitch': 0, 'cover64': 0, 'compact': set()})
    stitch_counter = Counter()
    comp_counter = Counter()
    missing_counter = Counter()
    compact = set()
    cover64_rows = []
    for r in rows:
        mode = str(r.get('mode', 'unknown'))
        cc = int(r.get('covered_count', 0))
        sp = int(r.get('stitch_path_lower_bound', 0))
        comps = int(r.get('stitch_components', 0))
        ck = compact_key(r)
        compact.add(ck)
        stitch_counter[sp] += 1
        comp_counter[comps] += 1
        for p in r.get('missing', []) or []:
            missing_counter[tuple(p)] += 1
        st = mode_stats[mode]
        st['count'] += 1
        st['best_covered'] = max(st['best_covered'], cc)
        st['best_stitch'] = max(st['best_stitch'], sp)
        st['compact'].add(ck)
        if cc >= 64:
            st['cover64'] += 1
            cover64_rows.append(r)

    summary = {
        'schema': 'cover64-stitch-summary-v1',
        'result_count': len(rows),
        'best': best,
        'cover64_count': len(cover64_rows),
        'unique_compact_line_sets': len(compact),
        'best_covered_count': int(best.get('covered_count', 0)) if best else 0,
        'best_stitch_path_lower_bound': int(best.get('stitch_path_lower_bound', 0)) if best else 0,
        'best_stitch_components': int(best.get('stitch_components', 0)) if best else 0,
        'best_max_component_size': int(best.get('max_component_size', 0)) if best else 0,
        'stitch_path_histogram': [{'stitch_path': k, 'count': v} for k, v in sorted(stitch_counter.items(), reverse=True)],
        'component_histogram': [{'components': k, 'count': v} for k, v in sorted(comp_counter.items())],
        'top_missing_points': [{'point': list(p), 'count': c} for p, c in missing_counter.most_common(20)],
        'mode_breakdown': {
            mode: {
                'count': st['count'],
                'best_covered': st['best_covered'],
                'best_stitch_path_lower_bound': st['best_stitch'],
                'cover64': st['cover64'],
                'unique_compact': len(st['compact']),
            }
            for mode, st in sorted(mode_stats.items())
        },
        'interpretation': 'unordered 22-line cover/stitch scaffolds; not certified polygonal trails',
    }
    (root / 'cover64_stitch_run_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True))

    with (root / 'cover64-stitch-candidates.jsonl').open('w') as fp:
        seen = set()
        for r in rows:
            ck = compact_key(r)
            if ck in seen:
                continue
            seen.add(ck)
            if int(r.get('covered_count', 0)) >= 64 or int(r.get('stitch_path_lower_bound', 0)) >= 20:
                fp.write(json.dumps(r, sort_keys=True) + '\n')

    md = ['# Cover64 stitch graph run summary', '']
    if best:
        md += [
            f"Best covered_count: {best.get('covered_count')} / 64",
            f"Best mode: `{best.get('mode')}`",
            f"Best source shard: `{best.get('source_shard')}`",
            f"Stitch graph: components={best.get('stitch_components')}, max_component={best.get('max_component_size')}/22, path_lower_bound={best.get('stitch_path_lower_bound')}/22, edges={best.get('stitch_graph_edges')}",
            f"Candidate: `{best.get('candidate_id')}`",
            '',
        ]
    else:
        md.append('No shard result JSON files found.')
    md.append(f"Shard result count: {summary['result_count']}")
    md.append(f"Cover64 count: {summary['cover64_count']}")
    md.append(f"Unique compact line-sets: {summary['unique_compact_line_sets']}")
    md.append('')
    md.append('Mode breakdown:')
    for mode, st in summary['mode_breakdown'].items():
        md.append(f"- `{mode}`: count={st['count']}, cover64={st['cover64']}, best_covered={st['best_covered']}, best_stitch={st['best_stitch_path_lower_bound']}, compact={st['unique_compact']}")
    md.append('')
    md.append('Stitch path histogram:')
    for x in summary['stitch_path_histogram'][:20]:
        md.append(f"- {x['stitch_path']}: {x['count']}")
    md.append('')
    md.append('Top missing points if not cover64:')
    for x in summary['top_missing_points'][:20]:
        md.append(f"- {x['point']}: {x['count']}")
    (root / 'cover64_stitch_run_summary.md').write_text('\n'.join(md) + '\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
