# Minimum-Link Covering Trail for the 4×4×4 Cubic Grid

## Current research results — 16 July 2026

The results below describe the verified state of the project **as of 16 July 2026**:

- an exact covering trail with `23` links is known, so `L(4,4,4) ≤ 23`;
- the `22`-link case remains open;
- the best exactly checked ordered `22`-link trail covers `62/64` points (`96.875%`);
- its two missing points are `(1,0,2)` and `(3,3,1)`;
- no verified ordered `63/64` or `64/64` trail with `22` links has been found.

The latest completed strict search, [`smart-search-25-core-valley`](runs/2026-07-16-smart-search-25-core-valley-full/summary.md), tested atomic replacements of two supporting lines. It completed all `20/20` shards, examined `6,151,145,399` paired mutations and `78,081,729` finite contact-span realizations, changed three of the formerly common 17 core lines, but still found no `63/64` trail.

This is strong bounded evidence that the tested paired-repair family is saturated. It is not a proof that a `22`-link solution is impossible.

## Best verified 22-link trail

Candidate: [`mlct22-ct-c64aebf0ed34cdf4`](runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json)

It has `23` vertices and therefore `22` consecutive links. Vertices outside the cube and half-integer coordinates are allowed. The trail is followed in this order:

```text
P0  = ( 2.0,  3.0, 1.0)
P1  = (-1.0,  0.0, 1.0)
P2  = ( 5.5,  0.0, 1.0)
P3  = ( 3.0, -1.0, 3.0)
P4  = ( 3.0,  3.0, 3.0)
P5  = ( 0.0,  0.0, 0.0)
P6  = ( 3.0,  0.0, 0.0)
P7  = ( 0.0,  3.0, 3.0)
P8  = ( 0.0,  0.0, 3.0)
P9  = ( 3.0,  3.0, 0.0)
P10 = (-1.0,  3.0, 0.0)
P11 = ( 2.0,  0.0, 3.0)
P12 = ( 2.0,  5.0, 3.0)
P13 = (-1.0,  2.0, 0.0)
P14 = ( 4.0,  2.0, 0.0)
P15 = ( 1.0, -1.0, 3.0)
P16 = ( 1.0,  4.0, 3.0)
P17 = ( 4.0,  1.0, 0.0)
P18 = (-1.0,  1.0, 0.0)
P19 = ( 3.0,  5.0, 2.0)
P20 = ( 3.0, -1.0, 2.0)
P21 = ( 0.0,  5.0, 2.0)
P22 = ( 0.0,  0.0, 2.0)
```

This candidate passed both exact CI verifiers and two additional independent exact incidence checks. It is a verified **partial** trail, not yet a complete solution.

For the detailed and continuously updated research state, see [`START_HERE.md`](START_HERE.md) and [`frontier/latest.md`](frontier/latest.md).

## License

This project is released under the MIT License.
