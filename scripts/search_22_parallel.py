#!/usr/bin/env python3
"""Run several independent 22-link search workers inside one GitHub Actions job."""

from __future__ import annotations

import argparse
import json
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from search_22_integer_box import FULL_MASK, bitcount, build_moves, make_vertices, missing_from_mask, one_walk


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding='utf-8')


def run_worker(worker_id, params):
    links = params['links']
    seconds = params['seconds']
    shard = params['shard']
    shards = params['shards']
    workers = params['workers']
    global_parts = shards * workers
    global_shard = shard * workers + worker_id

    t0 = time.time()
    rng = random.Random(params['seed'] + 1000003 * global_shard + 9973 * worker_id)
    vertices = make_vertices(params['box_min'], params['box_max'])
    adjacency, starts_all = build_moves(vertices)
    starts = [s for i, s in enumerate(starts_all) if i % global_parts == global_shard]

    best_mask = 0
    best_path = []
    attempts = 0
    next_report = t0 + 180

    print(f'worker={worker_id} global_shard={global_shard}/{global_parts} starts={len(starts)}', flush=True)

    while starts and time.time() - t0 < seconds:
        rng.shuffle(starts)
        for start in starts:
            if time.time() - t0 >= seconds:
                break
            mask, path, _ = one_walk(rng, vertices, adjacency, start, links, params['top_k'])
            attempts += 1
            if bitcount(mask) > bitcount(best_mask) or (bitcount(mask) == bitcount(best_mask) and len(path) > len(best_path)):
                best_mask = mask
                best_path = path
                print(f'worker={worker_id} new_best={bitcount(best_mask)}/64 missing={missing_from_mask(best_mask)}', flush=True)
            if best_mask == FULL_MASK and len(best_path) <= links + 1:
                break
        if best_mask == FULL_MASK and len(best_path) <= links + 1:
            break
        if time.time() >= next_report:
            print(f'worker={worker_id} progress attempts={attempts} best={bitcount(best_mask)}/64', flush=True)
            next_report = time.time() + 180

    return {
        'schema': 'minimum-link-covering-trail-parallel-worker-v1',
        'status': 'complete_22_found' if best_mask == FULL_MASK and len(best_path) <= links + 1 else 'partial_candidate',
        'worker_id': worker_id,
        'global_shard': global_shard,
        'global_parts': global_parts,
        'links_target': links,
        'links': max(0, len(best_path) - 1),
        'covered_count': bitcount(best_mask),
        'missing': missing_from_mask(best_mask),
        'vertices': [list(vertices[i]) for i in best_path],
        'parameters': params,
        'attempts': attempts,
        'elapsed_seconds': round(time.time() - t0, 3),
    }


def key(result):
    return (int(result.get('covered_count', 0)), int(result.get('links', 0)), int(result.get('attempts', 0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--links', type=int, default=22)
    ap.add_argument('--seconds', type=int, default=600)
    ap.add_argument('--box-min', type=int, default=-3)
    ap.add_argument('--box-max', type=int, default=7)
    ap.add_argument('--top-k', type=int, default=32)
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=1)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=20260623)
    ap.add_argument('--out', type=Path, default=Path('results/parallel_best_22.json'))
    ap.add_argument('--worker-dir', type=Path, default=Path('results/parallel_workers'))
    args = ap.parse_args()

    if args.workers < 1:
        raise SystemExit('--workers must be at least 1')

    params = {
        'links': args.links,
        'seconds': args.seconds,
        'box_min': args.box_min,
        'box_max': args.box_max,
        'top_k': args.top_k,
        'shard': args.shard,
        'shards': args.shards,
        'workers': args.workers,
        'seed': args.seed,
    }
    print('parallel_search_parameters:')
    print(json.dumps(params, indent=2, sort_keys=True), flush=True)

    t0 = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_worker, worker_id, params) for worker_id in range(args.workers)]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            save_json(args.worker_dir / f'shard_{args.shard}_worker_{result.get("worker_id")}.json', result)
            print(f'worker_done id={result.get("worker_id")} covered={result.get("covered_count")}/64', flush=True)

    best = max(results, key=key) if results else {'covered_count': 0, 'links': 0, 'missing': [], 'vertices': []}
    merged = {
        'schema': 'minimum-link-covering-trail-parallel-result-v1',
        'status': 'complete_22_found' if int(best.get('covered_count', 0)) == 64 and int(best.get('links', 99)) <= args.links else 'partial_candidate',
        'links_target': args.links,
        'links': int(best.get('links', 0)),
        'covered_count': int(best.get('covered_count', 0)),
        'missing': best.get('missing', []),
        'vertices': best.get('vertices', []),
        'best_worker_id': best.get('worker_id'),
        'parameters': {**params, 'out': str(args.out), 'worker_dir': str(args.worker_dir)},
        'total_attempts': sum(int(r.get('attempts', 0)) for r in results),
        'elapsed_seconds': round(time.time() - t0, 3),
        'worker_summaries': results,
    }
    save_json(args.out, merged)
    print('final_parallel_best:')
    print(json.dumps(merged, indent=2, sort_keys=True), flush=True)
    if merged['status'] == 'complete_22_found':
        print('FOUND A COMPLETE <=22-LINK CANDIDATE')


if __name__ == '__main__':
    main()
