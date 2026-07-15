# Reconstructed exact inputs for smart-search-25

The original Step-2 ZIP was found to contain a CRC-corrupted `search25_corebreak61_seeds.jsonl` member during GitHub Actions preflight. No smoke or full search ran from that damaged archive.

`data/search25_reconstructed_inputs.zip.b64` is an ASCII-safe transport of a newly reconstructed ZIP.

Checksums:

- base64 text SHA-256: `18c0a360cad88dafa40cd5ff039fca4b3a94f293010e3f5b2d3600b985236cfd`;
- decoded ZIP SHA-256: `49210583f1bc518b31decaa23b6c07b83ae3104e36e1b048d5ffba4e475ee182`.

Decoded contents:

- `search25_plateau62_closed.jsonl`: 43 exact ordered 62/64 plateau states;
- `search25_common17_core.json`: the common 17 supporting lines;
- `search25_corebreak61_seeds.jsonl`: 641 exact 61/64 core-break states in 51 missing-triple classes.

The 641-state bank contains 289 exact rows recovered from the readable prefix of the damaged member and 352 rows regenerated deterministically by exact rich-line replacement from the 43 plateau states. Every row is rechecked semantically during preflight: 22 unique supporting lines, exact coverage and missing set, common-core overlap, plateau intersection, and valley missing-class count.
