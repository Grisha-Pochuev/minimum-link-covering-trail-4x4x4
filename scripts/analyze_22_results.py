#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path


def json_files(paths):
    for p in paths:
        p = Path(p)
        if p.is_file() and p.suffix == '.json':
            yield p
        if p.is_dir():
            yield from p.rglob('*.json')


def norm_missing(value):
    if not isinstance(value, list):
        return ()
    out = []
    for item in value:
        if isinstance(item, list) and len(item) == 3:
            out.append(tuple(int(x) for x in item))
    return tuple(sorted(out))


def read_records(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'skip {path}: {exc}')
        return []
    if not isinstance(data, dict):
        return []
    records = []
    if isinstance(data.get('covered_count'), int):
        d = dict(data)
        d['_path'] = str(path)
        records.append(d)
    for item in data.get('worker_summaries', []) or []:
        if isinstance(item, dict) and isinstance(item.get('covered_count'), int):
            d = dict(item)
            d['_path'] = str(path) + '#worker'
            records.append(d)
    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', default=['results'])
    ap.add_argument('--top', type=int, default=20)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    records = []
    for p in json_files(args.paths):
        records.extend(read_records(p))

    records.sort(key=lambda r: (r.get('covered_count', 0), r.get('links', 0)), reverse=True)
    by_cov = Counter(r.get('covered_count', 0) for r in records)
    by_missing = Counter(norm_missing(r.get('missing', [])) for r in records)
    complete = [r for r in records if r.get('covered_count') == 64 and r.get('links', 99) <= 22]

    lines = []
    lines.append('# 22-link search artifact summary')
    lines.append('')
    lines.append(f'Total usable result records: {len(records)}')
    lines.append(f'Best covered_count: {records[0].get("covered_count", 0) if records else 0} / 64')
    lines.append(f'Complete <=22-link candidates: {len(complete)}')
    lines.append('')
    lines.append('## Coverage distribution')
    for k, v in sorted(by_cov.items(), reverse=True):
        lines.append(f'- {k}/64: {v}')
    lines.append('')
    lines.append('## Best individual records')
    for r in records[:args.top]:
        lines.append(f'- {r.get("covered_count")}/64, links={r.get("links")}, missing={r.get("missing")}, file={r.get("_path")}')
    lines.append('')
    lines.append('## Repeated missing-point patterns')
    for miss, count in by_missing.most_common(args.top):
        lines.append(f'- count={count}, missing={[list(p) for p in miss]}')

    text = '\n'.join(lines) + '\n'
    print(text)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()
