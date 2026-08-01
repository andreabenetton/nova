# Scaffold validation

The repository scaffold was checked with:

- `nova-contract validate .`
- `nova-contract normalize contracts --check`
- `nova-contract lint contracts`
- `nova-contract context .`
- `nova-contract boundaries canon/dependency-policy.yaml implementations/rust`
- `python3 tools/check_repository_shape.py`
- Python bytecode compilation of `nova-contract`

The construction environment did not provide a Rust toolchain, so `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` were not executed locally. GitHub Actions workflows are included to run them in an environment with Rust installed. The Rust crates are architectural stubs, not verified implementations.
