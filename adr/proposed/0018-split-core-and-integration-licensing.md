<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-0018: Split core and integration licensing

- Status: Proposed
- Date: 2026-08-01

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
