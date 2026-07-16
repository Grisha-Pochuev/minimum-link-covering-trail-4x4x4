# search-25 exact inputs

The original `data/search25_local_inputs.zip` is retired because one member had a bad CRC. It must not
be used by future chats or workflows.

## Canonical committed transport

The lossless input archive is stored as eight deterministic text parts:

```text
data/search25_reconstructed_inputs.parts/part00.b64
...
data/search25_reconstructed_inputs.parts/part07.b64
```

Concatenate in lexical order without adding separators:

```bash
cat data/search25_reconstructed_inputs.parts/part*.b64 > search25_inputs.zip.b64
```

Required SHA-256 for the concatenated base64 text:

```text
18c0a360cad88dafa40cd5ff039fca4b3a94f293010e3f5b2d3600b985236cfd
```

Decode and check the archive:

```bash
base64 -d search25_inputs.zip.b64 > search25_inputs.zip
echo "49210583f1bc518b31decaa23b6c07b83ae3104e36e1b048d5ffba4e475ee182  search25_inputs.zip" | sha256sum -c -
python - <<'PY'
import zipfile
with zipfile.ZipFile('search25_inputs.zip') as archive:
    bad = archive.testzip()
    assert bad is None, bad
    print('\n'.join(archive.namelist()))
PY
```

Required decoded ZIP SHA-256:

```text
49210583f1bc518b31decaa23b6c07b83ae3104e36e1b048d5ffba4e475ee182
```

## Required contents

- `search25_plateau62_closed.jsonl` — 43 exact closed plateau states;
- `search25_common17_core.json` — the common 17 supporting lines;
- `search25_corebreak61_seeds.jsonl` — 641 exact core-break `61/64` states;
- `search25_local_experiment_manifest.json` — row counts and inner hashes.

A valid preflight must verify both outer hashes, ZIP CRC, exact member names, inner hashes, row counts,
line counts and exact coverage before compilation or search.

## Publication rule

Never replace these parts with one large base64 file or an unverified binary upload. If reconstruction
changes, create a new versioned directory and record part hashes, concatenated hash and decoded archive
hash in a `step3-release-v1` manifest before any trigger.
