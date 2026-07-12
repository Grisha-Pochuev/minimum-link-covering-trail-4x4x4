# Retrospective: search-22 four-step cycle

Date: 2026-07-12

## What worked well

- The four-step cycle prevented a duplicate search-21 run and forced analysis of the completed evidence before choosing search-22.
- Small exact local experiments in Step 2 found a genuine `62/64` endpoint-repair seed before spending the full GitHub budget.
- Smoke ran before full, received all `20/20` shards, exercised every mode, checked candidates with two independent exact verifiers, and validated aggregation plus the three candidate-bank outputs.
- Search-22 kept exactly one visible workflow and the full run was launched automatically from the web chat.
- The active full run was recorded in project memory immediately after launch.

## Where time was lost

1. The Step-2 specification was broader than necessary. It mixed the essential endpoint hypothesis with many optional operations and an optional C++ rewrite. Step 3 then had to resolve too many choices while implementing.
2. The Step-2 handoff existed mainly in chat text. A concise persistent contract should have been committed before implementation: hypothesis, exact seed, invariants, selected modes, local test evidence, smoke gate and full profile.
3. Uploading one large source file through the connector was blocked. The working fallback split Python source into `part-*.pyfrag` files and reassembled it at runtime. This is reproducible but harder to read, review and maintain than normal modules.
4. Current state was duplicated in `START_HERE.md`, `frontier/latest.*`, the runbook and launch notes. The runbook still described search-21 after search-22 had started.
5. Each launch-trigger commit also started the legacy `check-and-short-search` workflow. Those extra jobs were unrelated to search-22 and wasted GitHub capacity.

## Rules adopted

### Step 2 to Step 3 handoff

Before Step 3, persist one launch/plan document containing:

- next unused search number and final workflow name;
- one primary hypothesis and a short list of explicitly optional modes;
- exact source seeds and their verification status;
- local test commands and observed results;
- invariants that must never be violated;
- smoke acceptance gate;
- fixed full profile and expected artifacts;
- implementation-language choice and reason.

Step 3 must implement that contract rather than redesign the search.

### Local dry-run gate

Before the first GitHub smoke commit:

- compile every source file;
- verify the known 23-link control;
- verify every new frontier seed twice;
- run every shard mode briefly in a local sequential test;
- run the summary builder on the generated miniature outputs;
- check artifact paths and bank outputs.

### Readable-source rule

Do not leave a new engine as concatenated code fragments unless there is no workable alternative. If a connector rejects a large file, split it into ordinary importable modules such as geometry, state, modes, search and output. Do not hide source in compressed or opaque payloads.

Search-22's `endpoint_repair_parts/part-*.pyfrag` layout is accepted for the already running immutable full run. After that run is recorded, refactor it into normal modules before reusing or extending the engine for search-23.

### Memory roles

- `START_HERE.md`: stable boot memory and reading order.
- `frontier/latest.md` and `.json`: best checked mathematical result.
- `frontier/active_run.json`: one machine-readable current run and do-not-duplicate state.
- `docs/web-chat-runbook-prompts.md`: process rules and reusable prompts.
- `runs/*`: durable evidence and completed-run archives.
- launch/plan documents: exact Step-2 to Step-3 handoff for one numbered search.

### Workflow-trigger rule

Generic regression workflows must use narrow `paths:` filters. Launch files, documentation, memory and unrelated numbered-search files must not start legacy short searches.

## Changes made in Step 4

- Added `frontier/active_run.json`.
- Narrowed `.github/workflows/check-and-short-search.yml` so launch and memory commits do not trigger it.
- Updated the runbook to the search-22 state and added the handoff, local dry-run and readable-source rules.
- Updated `START_HERE.md` to clarify file roles and record the deferred source-module cleanup.

## Next action

Do not alter or duplicate active full run `29181546758`. When it finishes, complete Prompt 1 first. After recording its evidence, refactor the search-22 fragment layout into normal Python modules before adapting the engine for search-23.
