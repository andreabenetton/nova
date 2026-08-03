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

Set `scope` to one of `architecture`, `p-stratum`, `p-0ap`, `p-lap`, `p-rap`, `r-stratum`, `o-stratum`, `p-r-interface`, `r-o-interface`, `security`, `implementation`, or `repository`, and place the record in the matching directory. The `title` must equal the heading title. List repository-relative paths in `affected_contracts` and `affected_documents`. See [`README.md`](README.md) for identifier allocation and the section rules.

Delete this paragraph and every instruction below it as you write. Sections marked optional may be omitted entirely; required sections stay, and a required section with nothing to report says `none` rather than being dropped.

## Context

State the problem, the constraints, and the decisions already in force that bound this one. Describe the situation as it is, not the solution. Keep terminology inside the declared scope except where an Interface is explicitly under discussion.

## Decision drivers

Optional. List the forces that materially determine the outcome, such as interoperability, replaceability, privacy, determinism, migration cost, or operational simplicity. Omit this section when the drivers are already evident from the context.

## Decision

State the decision precisely enough for an independent implementation or specification author to apply it without reading anything else in this record. Use the requirement words defined by `canon/normative-language.md` only with their RFC 2119 meanings.

## Architectural boundaries

- Owned by:
- Consumed through:
- Must not depend on:
- Information allowed to cross the boundary:
- Information prohibited from crossing the boundary:

Name the component, stratum, protocol, or Interface that owns the decision, the versioned contract through which others consume it, and the dependencies it must never acquire. This is the section that keeps a decision from silently widening its blast radius, and it is what a context manifest and the dependency policy are checked against.

## Interface and contract impact

Identify the affected versioned Interfaces, schemas, state machines, errors, capabilities, limits, conformance requirements, and compatibility obligations. Name contract versions explicitly. Write `none` when no contract changes.

## Wire compatibility impact

Optional. Describe message, encoding, identifier, ordering, maximum-value, negotiation, or backward-compatibility effects. Omit when the decision is not wire-visible; include it and write `none` only when a reader would reasonably expect wire impact and there is none.

## Implementation impact

Optional. Describe consequences for crates, processes, APIs, persistence, concurrency, deployment, observability, and test tooling. Separate normative requirements from implementation guidance.

## Security and privacy impact

Describe confidentiality, integrity, authentication, availability, unlinkability, metadata exposure, trust, downgrade, and abuse implications. State plainly what the decision does not establish: a decision that improves structure rarely proves security. Write `none` only when the decision cannot affect any of these.

## Alternatives considered

For each serious alternative, state what it was and why it was not selected. Include the status quo where relevant. An alternative listed without a reason for rejection is not a considered alternative.

## Consequences

State what becomes true once this decision is in force, including the costs. Use `### Positive`, `### Negative`, and `### Risks` subsections when the record has enough substance to warrant them.

## Validation and conformance

Define the evidence that would show the decision is correctly applied: positive and negative vectors, deterministic tests, conformance scenarios, independent implementations, simulations, reviews, or operational measurements. Prefer evidence a check can produce over evidence a reader must judge.

## Migration and rollback

Describe adoption order, compatibility windows, data or wire migration, rollback conditions, and removal of superseded behavior. Write `none` when the decision introduces nothing to migrate from.

## Unresolved questions

Record questions deliberately left open, including anything this record asserts without evidence yet. Write `none` when the decision is complete.
