---
adr: ADR-REPO-0006
title: Split core and integration licensing
scope: repository
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents:
  - legal/license-policy.yaml
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-REPO-0006: Split core and integration licensing

## Context

Nova requires reciprocal development of its core strata while also requiring
broad implementation of Adapters, Bindings, Platform Attachments, public
Interfaces, and conformance tooling. Applying AGPL to every artifact would make
external integration harder; applying a permissive license to the entire core
would not preserve network-deployed modifications.

Specifications, machine-readable contracts, historical papers, and trademarks
also require different treatment from executable software.

## Decision

Adopt the path-based policy in `legal/license-policy.yaml`:

- `AGPL-3.0-or-later` for the core implementation;
- `Apache-2.0` for Interfaces, shared public types, Adapters, Bindings, Platform
  Attachments, simulated providers, tooling, tests, and conformance code;
- `CC-BY-4.0` for project-authored documentation and specification prose;
- `Apache-2.0 OR CC-BY-4.0` for machine-readable contracts and schemas; and
- `LicenseRef-Nova-Research-Draft-Restricted` for historical PDFs pending a
  third-party rights review.

Do not add a custom linking exception initially. Prefer published,
language-neutral, versioned out-of-process provider contracts for external
providers that must remain independently licensed.

Stable final specifications may receive an OWFa 1.0 Patent Only commitment only
through the explicit process in `PATENTS.md`.

## Architectural boundaries

- Owned by: `legal/license-policy.yaml`, which maps repository paths to licenses.
- Consumed through: SPDX identifiers in files, `LICENSE.md` directory markers, and Rust crate license fields.
- Must not depend on: a file's license changing implicitly when it is moved or copied.
- Information allowed to cross the boundary: Apache-licensed Interfaces, shared public types, and conformance material, which external providers may implement against.
- Information prohibited from crossing the boundary: AGPL core implementation copied into an Apache-licensed integration component.

## Interface and contract impact

Machine-readable contracts and schemas are dual `Apache-2.0 OR CC-BY-4.0`, so an external implementation may consume a contract without taking on the core's reciprocal terms.

## Security and privacy impact

none directly. Licensing determines who may reuse code, not what the protocol protects.

## Alternatives considered

- Apply AGPL to every artifact. Rejected: it would make external Adapter, Binding, and Platform Attachment work substantially harder.
- Apply a permissive license to the whole repository. Rejected: it would not preserve network-deployed modifications to the core.
- Add a custom linking exception now. Rejected: it requires legal review, and published out-of-process provider contracts address the same need.

## Consequences

- The official monolithic executable is an AGPL-covered combination even though
  some linked components are separately reusable under Apache-2.0.
- External providers can implement the Apache interfaces without copying the
  core.
- CI must enforce path classification, SPDX metadata, directory notices, and
  crate license fields.
- Public release is blocked until rights ownership and third-party material are
  reviewed.
- Any future custom linking exception requires a separate ADR and legal review.

## Validation and conformance

CI enforces path classification, SPDX metadata, directory notices, and crate license fields through `tools/check_licenses.py`, run as `make licenses`.

## Migration and rollback

The policy was adopted before public release. Relicensing any path afterwards requires the consent of every contributor to it, so changes are effectively one-way.

## Unresolved questions

Public release is blocked until rights ownership and third-party material are reviewed. Any future linking exception requires a separate record and legal review.
