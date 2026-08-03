---
adr: ADR-<SCOPE>-NNNN
title: Title
scope: architecture
status: proposed
date: YYYY-MM-DD
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-<SCOPE>-NNNN: Title

Set `scope` to one of `architecture`, `p-stratum`, `r-stratum`, `o-stratum`, `p-r-interface`, `r-o-interface`, `security`, `implementation`, or `repository`, and place the record in the matching directory. The `title` must equal the heading title. List repository-relative paths in `affected_contracts` and `affected_documents`. See [`README.md`](README.md).

## Context

Describe the problem, constraints, and relevant existing decisions. Keep terminology within the declared scope except where an Interface is explicitly under discussion.

## Decision drivers

List the forces that materially determine the decision, such as interoperability, replaceability, privacy, operational simplicity, or migration cost.

## Decision

State the decision precisely enough for an independent implementation or specification author to apply it.

## Architectural boundaries

- Owned by:
- Consumed through:
- Must not depend on:
- Information allowed to cross the boundary:
- Information prohibited from crossing the boundary:

Explain what this decision owns and what remains outside its scope.

## Interface and contract impact

Identify affected versioned Interfaces, schemas, state machines, errors, conformance requirements, and compatibility obligations. Write `none` when there is no impact.

## Wire compatibility impact

Describe message, encoding, identifier, ordering, maximum-value, negotiation, or backward-compatibility effects. Write `none` when the decision is not wire-visible.

## Security and privacy impact

Describe confidentiality, integrity, authentication, availability, unlinkability, metadata exposure, trust, downgrade, and abuse implications.

## Implementation impact

Describe consequences for crates, processes, APIs, persistence, concurrency, deployment, observability, and test tooling. Separate normative requirements from implementation guidance.

## Alternatives considered

For each serious alternative, explain why it was not selected. Include the status quo where relevant.

## Consequences

### Positive

### Negative

### Risks

## Validation and conformance

Define evidence required to validate the decision, including positive and negative vectors, deterministic tests, independent implementations, simulations, reviews, or operational measurements.

## Migration and rollback

Describe adoption order, compatibility windows, data or wire migration, rollback conditions, and removal of superseded behavior.

## Unresolved questions

Record questions deliberately left open. Use `none` when the decision is complete.
