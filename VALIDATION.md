# Repository validation

The current scaffold was checked with:

- `nova-contract validate contracts` — 99 YAML documents validated;
- `nova-contract normalize contracts --check` — 99 canonical documents current;
- `nova-contract lint contracts` — 15 Interfaces, 68 conformance scenarios, and 15 implementation manifests checked;
- `nova-contract matrix contracts --check`;
- `nova-contract context .` — 46 context manifests checked;
- `nova-contract boundaries canon/dependency-policy.yaml implementations/rust` — 12 enforced crate boundaries checked;
- `python3 -m unittest discover -s tools/nova-contract/tests` — 4 tests passed;
- `python3 tools/check_agent_instructions.py`;
- `python3 tools/check_simulation_fixtures.py` — 7 deterministic scenarios, 4 profiles, and 1 trace validated;
- `python3 tools/generate_repository_docs.py --check`;
- `python3 tools/check_repository_shape.py`;
- `python3 tools/ci/check_contract_versions.py HEAD`;
- Python byte-code compilation for the repository validation tools;
- `git diff --check`.

`make check` completes every non-Rust stage above, then stops at:

```text
cargo fmt --all -- --check
make: cargo: No such file or directory
```

The construction environment provides neither `cargo`, `rustc`, nor `rustfmt`. Consequently the Rust boundary and P-0AP skeletons were not compiled, formatted, linted, or tested locally. GitHub Actions and `make check` retain `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` for an environment with Rust installed.

The Rust code remains a compilable-intent architecture skeleton rather than conformance evidence. P-R `1.0` is explicitly blocked until P-0AP, R-Stratum, and an independent P-RAP/QUIC implementation pass the relevant generated and behavioral suites.
