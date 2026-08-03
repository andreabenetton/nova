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
- The deeper instruction file governs its own tree on conflict. A nested file may narrow or refine a shared rule; it MUST NOT relax a repository-wide constraint such as authority order, boundary rules, licensing, testing, or Git discipline.
- Resolve a relative path named by an instruction file against the directory containing that file unless the file states otherwise.
- At task start, name the instruction files in scope for the paths being changed.

## Source precedence

`canon/authority.md` defines the normative authority order. It governs; this section states only how to apply it while working.

- Read the authority chain top-down for the boundary being changed, and stop at the first artifact that answers the question. For an operation, event, error, limit, or lifecycle question, that is almost always the versioned contract, not prose about it.
- An accepted ADR explains rationale and intent. When it disagrees with canon or a versioned contract about current behavior, the contract or canon is authoritative and the divergence is itself a finding to report.
- Existing code is not a source of truth when it conflicts with an active contract. Do not propagate the code's assumption to keep a build green. Report the divergence, and change the lowest correct layer.
- `README.md`, `ROADMAP.md`, `STATUS.md`, `VALIDATION.md`, and `CHANGELOG.md` are human-facing narrative. Do not cite them as authority for behavior and do not use them as implementation context. Correct them when a change makes them factually wrong; otherwise leave them alone.
- `REPOSITORY-MAP.md` records the authority level of each tree. Use it to classify an unfamiliar path before deciding which rules apply to it.

## Context loading map

Load task-scoped context on demand. Do not copy it into this file.

| Work | Read |
|---|---|
| Any component | the nearest `CONTEXT.yaml` and the nearest `AGENTS.md` |
| Terminology | `canon/glossary.md` as the index, then only the common glossary, the glossary owned by the component being modified, and any explicit Interface glossary |
| Cross-cutting architecture, invariants, authority, security, versioning | the owning document under `canon/` |
| Peer behavior inside a stratum | `protocols/<stratum>/AGENTS.md` and the documents it names |
| A boundary contract | the Interface directory under `contracts/interfaces/`, its `AGENTS.md` where present, and `contracts/README.md` |
| Contract revision or version question | `canon/versioning.md` and `contracts/README.md` |
| A new Adapter, Binding, compatibility service, simulation front end, stratum, or Interface change | the matching template under `agents/task-templates/` |
| Review of an Interface, protocol, security, simulation, or LLM-scope change | the matching checklist under `agents/review-checklists/` |
| Bounded role framing for a component | the matching file under `agents/roles/` |
| Writing or placing an ADR | `adr/README.md` for scope, identifier, and status rules |

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

### Change-scoped validation

`make check` remains the completion gate, and the list above remains the floor before pushing a contract-touching change. Use this table to know which target actually covers a change, and to run the covering target early rather than discovering the failure at push time.

| Changed paths | Targets |
|---|---|
| `contracts/**` | `make contracts`, `make normalize`, `make lint`, `make matrix`, `make contract-tests`, and `python3 tools/ci/check_contract_versions.py` |
| Glossaries, `canon/` terminology, normative prose | `make terminology` |
| Any `CONTEXT.yaml`, or a new component directory | `make context` |
| `implementations/rust/**` or `canon/dependency-policy.yaml` | `make boundaries`, `make rust`, `make test` |
| Simulation scenarios, profiles, or traces | `make simulation-fixtures` |
| `adr/**` | `make adr-index` |
| `tools/**` | `make tool-tests`, plus the target that runs the changed tool |
| Any `AGENTS.md`, `CLAUDE.md`, or vendor instruction file | `make agent-instructions` |
| Files added, moved, copied, or relicensed, and every new directory | `make licenses` |
| Any added, removed, or renamed tracked file | `make repository-docs` |

The last row is easy to miss: `make repository-docs` regenerates `generated/repository-tree.txt` and `generated/contracts-index.md` from the tracked file list, so adding or removing any tracked file — including one unrelated to contracts — makes the generated documentation stale until the target is rerun. An untracked file that the repository intends to ignore MUST be ignored rather than committed to satisfy a check.


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

## Required documentation updates

A normative change is never the changed file alone. Propagate every dependent artifact in the same commit, or in the same commit series in the authority direction when the multi-component rule requires separate commits.

- A contract revision carries its source YAML, schemas, canonical generated form, lock entry, compatibility declaration, conformance scenarios, and the compatibility matrix.
- A registry or numeric assignment change carries the registry file under `canon/registries/` and every document that cites the assignment.
- A terminology change carries the owning glossary, and `canon/glossary.md` when ownership itself changes.
- A new or changed ADR follows `adr/README.md` for scope directory, identifier sequence, front matter, and status metadata; regenerates `generated/documentation/adr-index.md`; and updates every document that cites it. When an accepted ADR requires a normative change, update the authoritative artifact rather than relying on the ADR alone.
- A new replaceable boundary carries its versioned NIDL contract, conformance scenarios, context rules, and an ADR when the architecture changes.
- Generated material is regenerated by its tool in the same commit as the source change. Never hand-edit it and never leave it stale.
- `CHANGELOG.md` records externally visible contract and Interface changes.
- `STATUS.md`, `VALIDATION.md`, `ROADMAP.md`, and `README.md` are corrected when a change makes them factually wrong, and are otherwise left alone.

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

## Anti-patterns

Do not introduce:

- stratum-owned terminology outside the Interface documentation that owns the mapping, or a unified glossary that redefines a term across strata;
- a dependency on a lower stratum's internals, private model, or implementation behavior rather than its versioned contract;
- implementation-specific knowledge carried across a declared boundary in prose, types, tests, or fixtures;
- a change made at a higher layer because it is easier to make there, when a lower document or contract owns the behavior;
- an implementation derived directly from a research document when a normative contract covers the behavior;
- a new replaceable boundary without a versioned NIDL contract, conformance scenarios, context rules, and an ADR when the architecture changes;
- an in-place edit to a published contract version, or to preserved experimental history, in place of a new version;
- code that lands ahead of the contract when externally visible behavior changes;
- a hand edit to anything a tool generates, including generated repository documentation, canonical contract forms, and generated crates;
- a workaround in a consumer that compensates for a contract divergence instead of reporting it and fixing the owning layer;
- AGPL core implementation copied into an Apache-licensed Interface, Adapter, Binding, Platform Attachment, tooling, or conformance component;
- a new file without the correct SPDX identifier where the format supports comments, or a new directory without a `LICENSE.md` marker;
- RFC 2119 uppercase requirement words in non-normative prose, or with a meaning other than the one defined by `canon/normative-language.md`;
- a file committed only to satisfy a repository check, including build output or a lock file the repository deliberately ignores;
- mock-only tests offered as evidence that an integration, socket, process boundary, or generated contract works;
- a single happy-path test presented as coverage of a changed code path;
- "while here" cleanup folded into a fix commit;
- a completion claim that names `make check` when only part of it ran, or a push claim that Git did not confirm;
- a reference to an unrelated external project by name in repository files or commit messages.

## Completion checklist

Work through this before proposing completion. Do not reproduce it in a response unless an item is missing or needs explicit call-out.

- The change was made at the lowest correct layer, and the affected boundary consumes only versioned contracts.
- Contract, canon, or normative documentation was updated before or with the code for externally visible behavior.
- No stratum-owned terminology crossed a boundary, and the glossary index is current where ownership changed.
- Dependent documentation propagated per "Required documentation updates".
- Generated artifacts were regenerated by their tools and verified, not hand-written or asserted through copies.
- Tests cover the added or changed behavior, including its rejection, edge, and boundary cases, and externally visible Interface changes carry matching provider and consumer conformance scenarios. If the change has no testable surface, the report says so and why.
- Licensing holds: SPDX identifiers, directory markers, and crate license fields match policy.
- `make check` passed, or every executed target and every omitted target is named precisely, with the environmental reason for each omission.
- Commits are shaped per the multi-fix and multi-component rules, and carry no temporary diagnostic material.
- Commit, push, and pull-request status is reported exactly as Git and the remote confirmed it.
- Known divergences, unverified surfaces, deferred drift, and follow-up work are stated explicitly rather than left implied.
