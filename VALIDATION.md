# Scaffold validation

The repository scaffold was checked with:

- `nova-contract validate contracts` — 42 YAML documents validated;
- `nova-contract normalize contracts --check` — 42 canonical documents current;
- `nova-contract lint contracts` — 12 Interfaces, 14 conformance scenarios, and 15 implementation manifests checked;
- `nova-contract matrix contracts --check`;
- `nova-contract context .` — 46 context manifests checked;
- `nova-contract boundaries canon/dependency-policy.yaml implementations/rust` — 12 enforced crate boundaries checked;
- `python3 -m unittest discover -s tools/nova-contract/tests`;
- `python3 tools/check_agent_instructions.py`;
- `python3 tools/check_simulation_fixtures.py` — 5 deterministic scenarios, 4 profiles, and 1 trace validated;
- `python3 tools/check_repository_shape.py`;
- `python3 -m py_compile tools/check_simulation_fixtures.py`;
- `git diff --check`.

The construction environment does not provide a Rust toolchain, so `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` could not be executed locally. GitHub Actions and `make check` retain those steps for environments with Rust installed. The Rust crates are architecture and API skeletons, not verified protocol implementations.
