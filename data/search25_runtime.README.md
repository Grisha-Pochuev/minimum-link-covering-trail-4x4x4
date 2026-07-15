# search-25 versioned runtime

`data/search25_runtime.tar.gz` is the exact implementation bundle for `smart-search-25-core-valley`.

SHA-256: `51f642824516333142732818b9eaca75932b7c1aeca4e0788cbad63e2869b493`.

This revision treats the outer ZIP hash as provenance only and validates the three immutable inner input files by their recorded SHA-256 hashes and row counts. This corrects a packaging-only mismatch without weakening the mathematical checks.

The archive contains the C++20 engine, two independent exact verifiers, input materializer, preflight, CI runner, and aggregate builder.
