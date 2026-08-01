<!-- SPDX-License-Identifier: Apache-2.0 -->

# Agent rules

1. Read the nearest `CONTEXT.yaml` before modifying a component.
2. Use `canon/glossary.md` as the glossary index. Read only the common glossary, the glossary owned by the component being modified, and any explicit Interface glossary. Do not mix stratum-owned terminology outside Interface documentation.
3. A higher stratum may use only the versioned interface contract of the lower stratum.
4. Do not import implementation-specific knowledge across a declared boundary.
5. Change the lowest correct layer. A QUIC framing change belongs to a QUIC Binding document, not to the P-R Interface.
6. Update contracts before code when externally visible behavior changes.
7. Never edit generated files manually.
8. New replaceable boundaries require a versioned NIDL contract, conformance scenarios, context rules, and an ADR when the architecture changes.
9. Research documents are non-normative. Do not implement directly from an original paper when a normative contract exists.
10. In normative prose, use the uppercase requirement words defined by `canon/normative-language.md` only with their RFC 2119 meanings.
11. Run `make check` before proposing completion.

## Instruction architecture

- `AGENTS.md` is the canonical, vendor-neutral source of repository instructions.
- Nested `AGENTS.md` files provide more specific instructions for their directory trees.
- Agent-specific files are adapters or extensions only and must not copy shared rules.
- Deterministic requirements belong in tooling and CI rather than prompt instructions alone.

## Git discipline

### Logical units of work

After each completed logical unit of work:

1. create a Git commit;
2. fetch before publishing or integrating;
3. push the current task branch when a writable remote is configured.

If a push cannot be completed because no remote is configured, credentials are unavailable, remote access fails, branch protection rejects the push, or the environment otherwise prevents it, say so explicitly. Never claim that a push succeeded unless Git confirmed it.

Commit messages MUST be short, specific, and limited to the actual change. Do not leave a completed logical unit uncommitted. Do not add a `Co-Authored-By` trailer. When a commit message contains shell metacharacters such as backticks, `$`, multiplication signs, or parentheses, pass the message through a quoted heredoc rather than an inline `git commit -m` argument:

```sh
git commit -F - <<'EOF'
Describe the scoped change
EOF
```

Never force-push unless the user explicitly requests it. Do not rewrite published history. Read `git log` before attributing or modifying an existing commit.

### Concurrent contributors

Multiple agents or sessions may work on this repository concurrently and may run on different hosts. The isolation model is one complete clone per session. Do not use Git worktrees for session isolation. Sessions coordinate through the configured remote.

- Assume exclusive ownership of the clone in which the task started.
- At task start, the tree MUST be clean. Unexplained pre-existing changes indicate that clones are being shared incorrectly; stop and report the problem rather than staging selectively or committing those changes.
- Subagents share the session clone. Parallel fan-out MUST remain read-only; serialize file modification, generation, build, and test operations.
- `git add -A` is acceptable because the clone is session-owned.

### Task branches

Use one short-lived branch per task, where a task is the complete multi-file logical change being delivered. When `origin/main` exists:

1. run `git fetch origin`;
2. inspect `origin/main` and its recent log for the same change already landed or in flight;
3. create the task branch from fresh `origin/main`;
4. use the branch name format `<hostname>/<clone>/<type>/<short-description>`.

Example:

```text
develop-nova/nova-claude3/spec/p-r-lifecycle
```

Use a concise type such as `feat`, `fix`, `spec`, `docs`, `test`, `tool`, or `chore`. If no remote exists, branch from the current local `main`, preserve the same naming convention, commit locally, and report that fetch, push, and pull-request integration could not be performed.

### Integration through pull requests

When the repository has a writable GitHub remote, integrate through a pull request. Treat `main` as protected: no direct pushes, merge commits only, and no squash or rebase merge.

Before opening or updating the pull request:

1. run `git fetch origin`;
2. merge current `origin/main` into the task branch with `git merge --no-ff origin/main`;
3. resolve conflicts without rewriting published history;
4. build and test the merged tree;
5. run the Nova collision and consistency checks described below;
6. push the task branch.

Then use:

```sh
gh pr create --base main --head "$BRANCH" --title "..." --body "..."
gh pr merge <number> --merge --auto --delete-branch
```

Red required checks block the merge. If `main` moves while the pull request is open, merge `origin/main` again, rerun validation, and push the updated branch. If all GitHub Actions jobs fail immediately at the same time, first report the possibility of an account-level Actions quota or service-availability problem rather than assuming that the branch is defective. A quota or platform failure still blocks integration and MUST be reported as such.

### Pre-push collision and consistency checks

A clean textual merge does not prove semantic compatibility. After merging current `origin/main`, inspect the combined tree for collisions that may occur across different files.

For every change, run the relevant existing repository checks, normally through:

```sh
make check
```

If Rust tooling is unavailable, run every non-Rust target individually and report the omitted Rust checks explicitly. Do not describe partial validation as a complete `make check` pass.

Before pushing changes that touch contracts, Interfaces, protocol behavior, generated contract material, or Rust public API surfaces, run at least:

```sh
make contracts
make normalize
make lint
make matrix
make context
make boundaries
make contract-tests
make terminology
make repository-docs
```

For files added, moved, copied, or relicensed, also run:

```sh
make licenses
```

Manually scan the merged result for semantic collisions not guaranteed to be caught by Git, including:

- duplicate ADR numbers;
- duplicate Interface identifiers or versions;
- duplicate registry identifiers or numeric assignments;
- duplicate conformance scenario identifiers;
- conflicting glossary ownership or cross-stratum terminology;
- duplicate changelog release headings;
- stale generated repository documentation;
- incompatible duplicate Rust registrations, feature names, or public type definitions.

Use the contract immutability and repository-shape checks when applicable:

```sh
python3 tools/ci/check_contract_versions.py
python3 tools/check_repository_shape.py
```

Do not push until the merged tree has been tested and these checks have either passed or their environmental limitation has been stated precisely.

## Licensing rules

- Follow `legal/license-policy.yaml`; do not change a file's license by moving or copying it across a boundary without review.
- New files require the correct SPDX identifier where the format supports comments.
- Every new directory requires a `LICENSE.md` marker.
- Core crates are AGPL; Interface, Adapter, Binding, Platform Attachment, tooling, and conformance crates are Apache-2.0.
- Do not copy AGPL core implementation into Apache-licensed integration components.
- Run `make licenses` after adding, moving, or generating files.
