# Current search frontier

Status: the checked ordered-trail frontier remains `62/64`. Search-25 completed strict `20/20`, escaped the formerly closed common-17 core down to overlap `14/17`, but produced no exact ordered `63/64` or `64/64` trail.

Live execution status is deliberately not stored here. Always read `frontier/active_run.json`.

## Best checked ordered trail

- candidate id: `mlct22-ct-c64aebf0ed34cdf4`
- covered count: `62 / 64`
- coverage percent: `96.875%`
- links: `22`
- vertices: `23`
- missing: `(1,0,2)`, `(3,3,1)`
- source run: `29249275103`, shard `14`, worker `1`
- frozen-core overlap: `16 / 18`
- source file: `runs/2026-07-13-smart-search-23-core-transplant-full/best_candidate.json`
- status: exactly verified partial trail from a completed run

It passed both CI exact verifiers and two additional independent exact incidence checks.

## Latest completed recorded Actions run

Run `29457051261`, workflow `smart-search-25-core-valley`:

- precheck, strict smoke and full: `20/20` success;
- best ordered finite trail: `62/64`;
- exact ordered `63/64+`: `0`;
- exact ordered `64/64`: `0`;
- atomic paired attempts: `6,151,145,399`;
- finite contact-span realizations: `78,081,729`;
- minimum common-17 overlap: `14`;
- durable ordinary bank: `53` exact `62/64` rows;
- diagnostic bank: `16,052` exact `59/64`–`61/64` valley states;
- originals: `20` raw shard bests, `5` symmetry/reversal classes;
- maximum measured process-tree RAM: `0.0154 GiB`;
- mean measured throughput: about `15,274` attempts/s/shard, including the one-second control shard.

Run-best candidate `mlct22-cv-40a5999c05294be6` covers `62/64`, misses `(0,2,1)` and `(3,3,1)`, and retains only `14/17` formerly common core lines.

Archive: `runs/2026-07-16-smart-search-25-core-valley-full/`.

## Structural interpretation

Search-25 was the correct test of the previous local diagnosis. The earlier exact experiment closed all one-rich-line moves around the 43-state `62/64` plateau. Search-25 allowed two-line changes atomically and scored finite contact spans directly.

The engine reached states changing three of the common 17 lines, so failure cannot be blamed on remaining trapped inside the one-line plateau. Yet no mode reached `63/64` after more than six billion paired mutations and 78 million finite realizations.

This is strong bounded evidence that the tested core-valley paired-repair families are saturated. It is not a proof that a 22-link covering trail is impossible. The next hypothesis should broaden the structural mechanism rather than repeat search-25 with another seed.

## Three banks

- Ordinary: `53` independently rechecked ordered `62/64` additions; `50` symmetry/reversal classes.
- Diagnostic: `16,052` exact finite valley states (`14,407` at `59/64`, `1,534` at `60/64`, `111` at `61/64`).
- Originals: `20` raw shard bests; `5` compact classes.

An unordered line cover, support graph, or diagnostic valley state is not counted as a frontier trail.
