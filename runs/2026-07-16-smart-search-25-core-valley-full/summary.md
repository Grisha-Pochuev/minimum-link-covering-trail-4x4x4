# smart-search-25-core-valley — final recorded result

Run: `29457051261`  
Workflow: `smart-search-25-core-valley`  
Trigger commit: `22becb63bb5dc00fcc547e97a9366f25b35c391b`  
Profile: precheck -> strict smoke `20/20` -> full `20/20` -> strict aggregate  
Search time: `20400` seconds per substantive shard, `20` shards, `4` workers per shard  
Status: **complete and exactly verified**

## Ordered-trail result

- Best ordered trail in this run: `62/64`, 22 links.
- Run-best candidate: `mlct22-cv-40a5999c05294be6`.
- Missing points: `(0,2,1)` and `(3,3,1)`.
- Operation: `atomic_core_rich_pair`, parent `valley:132`, shard `3`.
- Common-17 overlap: `14/17`; the run therefore escaped three lines of the formerly closed common core.
- Exact ordered `63/64+`: `0`.
- Exact ordered `64/64`: `0`.

The global numeric frontier remains the search-23 candidate `mlct22-ct-c64aebf0ed34cdf4` at `62/64`, because search-25 did not improve coverage. Search-25 is nevertheless structurally important: it went beyond the closed one-line plateau and still found no `63/64` trail in the tested atomic two-line neighborhoods.

## Search scale

- Atomic paired attempts: `6,151,145,399`.
- Exact finite contact-span realizations: `78,081,729`.
- Minimum common-17 overlap reached: `14`.
- Exact verified `62/64` rows before compact durable selection: `191`.
- Durable new ordinary rows: `53`.
- Durable core-broken valley rows: `16,052` (`14,407` at `59/64`, `1,534` at `60/64`, `111` at `61/64`).

## Mode result

Every mode topped out at `62/64`. The largest work block was `core-rich-pair` with about `2.288` billion attempts and `37.84` million finite realizations. No mode produced `63/64`.

## Three banks

- Ordinary: `53` exact ordered `62/64` additions; symmetry/reversal compaction leaves `50` classes.
- Diagnostic: `16,052` exact finite `59/64`-`61/64` core-broken valley states. The full 17 MB JSONL is retained in Actions artifact `8365119990`; this archive records its digest and compact statistics.
- Originals: `20` raw shard bests; cube symmetry/reflection and path reversal leave `5` classes.

## Interpretation

The earlier exact local work proved that changing one rich line cannot escape the 43-state `62/64` plateau. Search-25 allowed two-line atomic changes, reached overlap `14/17`, and sampled more than 78 million finite realizations. It still found no `63/64` trail. Thus the simple hypothesis “break one common-core line and repair it with one second line” is strongly weakened in the explored families.

This is a bounded computational negative result, **not** a proof that no 22-link covering trail exists. A next search should not merely repeat search-25 with another seed; Step 2 should choose a genuinely broader structural mechanism.
