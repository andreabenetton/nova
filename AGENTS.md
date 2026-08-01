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


## Tests follow implementations

Every implementation change MUST land with tests for the behavior it adds or changes. If a change has no testable surface, state that explicitly in the completion report and explain why.

Add or update tests when a change introduces:

- new behavior or a new code path;
- a new validation, rejection, or failure branch;
- a new edge case or boundary condition;
- a regression fix whose failing case can be reproduced;
- a changed public contract, Interface behavior, wire representation, state transition, or observable result.

Tests MUST pin observable behavior rather than private implementation structure. A refactor that preserves behavior SHOULD NOT require test changes merely because helpers, modules, or internal data structures were renamed or reorganized.

### Cover the behavioral matrix

A single success case is the minimum, not complete coverage. For each changed code path, cover the directly related matrix where applicable:

- successful operation;
- each distinct rejected-input shape and its exact error or status;
- all values of closed enums, registries, mappings, and capability sets;
- error and reset branches that the implementation can produce;
- minimum and maximum values;
- empty, single-element, and multi-element collections;
- absent and present optional fields;
- stale, duplicate, reordered, expired, and conflicting events or revisions;
- authorization, scope, role, and capability variants distinguished by the Interface;
- provider loss, Interface reset, queue exhaustion, backpressure, and recovery behavior.

Use table-driven or parameterized tests for closed sets rather than selecting one representative value. If a defensive branch is genuinely unreachable because a framework or validated boundary prevents it, document that fact in a code comment rather than leaving the branch unexplained.

"Only the tests directly related to the change" is a scope limiter, not permission to omit the changed behavior's rejection, edge, and boundary cases. Do not add unrelated test cleanup to the same commit.

Integration behavior requires integration tests. Tests that replace the relevant socket, process boundary, generated contract, queue, clock, persistence layer, or other integration surface with mocks do not establish that the integration works. Mocks MAY be used for narrower unit behavior, but they do not substitute for the relevant conformance or integration test.

For Nova specifically:

- externally visible Interface changes require matching provider and consumer conformance scenarios;
- Path Provider behavior changes require tests at the Path Provider Interface boundary;
- P-0AP deterministic behavior requires scenario or trace fixtures where applicable;
- parser, serializer, registry, and normalization changes require positive and negative vectors;
- generated artifacts MUST be regenerated and verified rather than asserted through hand-written copies;
- Rust public behavior requires crate tests or integration tests in addition to contract validation where executable code exists.

If the only meaningful verification requires a real operating-system, packet, driver, hardware, or multi-process surface, perform that verification when the environment supports it. If the environment does not support it, state the exact unverified surface and do not treat type-checking, compilation, or mock-only tests as proof that the feature works.

Legitimate examples of changes with no separate testable surface include documentation-only edits, instruction files, legal texts, and CI configuration whose behavior is exercised by the CI run itself. In such cases, still run the applicable repository validators.

## Multi-fix prompts

When one prompt requests multiple unrelated fixes, do not bundle them into one commit. Treat fixes as unrelated when they address different root causes, independent ADRs, separate Interface changes, or concerns that can be reviewed and reverted independently.

For each fix, in order:

1. implement only that fix;
2. add or update only its directly related tests and conformance material;
3. run the impacted tests and validators;
4. create one commit scoped to that fix;
5. fetch and push before moving to the next fix when a writable remote is available.

A multi-fix request produces one commit per independent fix. Related sub-tasks of one fix, such as implementation, tests, generated output, a docstring, and a direct documentation cross-reference, belong in the same commit.

Do not include "while here" cleanup. Record unrelated drift for later, or address it in a separate follow-up commit after the requested fix is committed.

## Multi-component prompts

When a single prompt requires changes to more than one independently versioned or independently deployable Nova component, handle each component separately. Components covered by this rule include:

- a stratum implementation;
- a Path Provider implementation;
- an Adapter;
- a Binding;
- a Platform Attachment;
- an Interface or generated Interface crate;
- an SDK;
- a daemon or executable;
- a conformance tool;
- simulation tooling.

For each independently reviewable component:

1. implement only that component's portion;
2. add or update only its directly related tests and conformance material;
3. run that component's tests and validators;
4. create one commit whose message names only that component change;
5. fetch and push before moving to the next component when possible.

Shared contract, registry, or normative documentation changes that enable multiple components belong in their own preceding commit. Order commits in the authority direction: normative contract and registry changes first, provider implementation next, then consumers and integrations.

Do not split a single atomic cross-boundary contract revision into inconsistent commits. The contract revision, its schemas, canonical generated form, compatibility declaration, and conformance scenarios form one logical unit. Implementations that consume that completed revision follow in separate component commits.

## Debugging hygiene

When investigation reveals multiple independent root causes, commit each root cause separately. Do not squash the diagnostic chain into one broad fix; preserve bisectability and the reason each change exists.

Before committing, remove temporary diagnostic material, including:

- `println!`, `dbg!`, `print`, or equivalent ad hoc output;
- payload or secret dumps;
- temporary trace fixtures and shortcuts;
- commented-out hypotheses;
- hot-path debug logging added only for investigation;
- temporary feature flags or relaxed validation.

Keep intentional production diagnostics, such as a warning on a real fallback path, structured reporting of a previously silent failure, or a bounded startup diagnostic. Such logging MUST avoid secrets, cryptographic material, private identifiers, and unbounded packet or payload contents.

Cleanup belongs in the fix commit, or in a separate follow-up commit completed before pushing. Never publish temporary diagnostic noise with a promise to remove it later.

## Licensing rules

- Follow `legal/license-policy.yaml`; do not change a file's license by moving or copying it across a boundary without review.
- New files require the correct SPDX identifier where the format supports comments.
- Every new directory requires a `LICENSE.md` marker.
- Core crates are AGPL; Interface, Adapter, Binding, Platform Attachment, tooling, and conformance crates are Apache-2.0.
- Do not copy AGPL core implementation into Apache-licensed integration components.
- Run `make licenses` after adding, moving, or generating files.
