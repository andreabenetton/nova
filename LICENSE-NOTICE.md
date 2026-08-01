<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Nova licensing notice

Nova uses different licenses at deliberately versioned architectural boundaries.
The exact machine-readable policy is `legal/license-policy.yaml`; file-level SPDX
identifiers take precedence where present.

## Default path mapping

| Material | License |
|---|---|
| Nova core implementation: P-Stratum common, P-0AP, P-LAP, P-RAP, R-Stratum, O-Stratum, the node daemon, and IP-over-Nova service | `AGPL-3.0-or-later` |
| Interface crates and shared public types | `Apache-2.0` |
| P-LAP Adapters, P-RAP Bindings, Platform Attachments, simulated integration providers, and their reusable support libraries | `Apache-2.0` |
| Tooling, conformance harnesses, tests, examples, packaging, fuzzing, and CI configuration | `Apache-2.0` |
| Architecture, protocol prose, ADRs, manuals, compatibility specifications, and original project diagrams | `CC-BY-4.0` |
| NIDL contracts, schemas, registries, simulation fixtures, and generated contract documentation | `Apache-2.0 OR CC-BY-4.0` |
| Historical source papers under `research/original-papers/` | `LicenseRef-Nova-Research-Draft-Restricted` |

The `LICENSE.md` in each repository directory records the applicable local
policy or identifies the directory as mixed. Those files are explanatory; the
SPDX identifiers and `legal/license-policy.yaml` remain authoritative.

## AGPL core and permissive integration surfaces

The core is AGPL to require publication of modified core source when the
covered program is conveyed or offered as a network service under the license's
terms. The published Adapter, Binding, Platform Attachment, and inter-component
interfaces remain Apache-licensed so independent implementations can be built
without copying AGPL core code.

An Apache-licensed Adapter or Binding linked into the official AGPL executable
does not make the combined executable permissive. The individual integration
source remains reusable under Apache-2.0, while distribution of a combined work
must comply with all applicable terms. External differently licensed providers
should normally use the versioned out-of-process provider interfaces. This is an
architectural policy, not a guarantee about the legal classification of any
particular combination.

## Specifications and patents

Draft and final specification prose is licensed under CC-BY-4.0. Machine-readable
contracts are dual-licensed so they can be consumed as either implementation
inputs or specification content.

No OWFa patent commitment attaches merely because a draft is present in this
repository. A stable specification becomes subject to an OWFa 1.0 Patent Only
commitment only when it is explicitly listed in `patents/final-specifications.yaml`
and the applicable rights holder has executed the commitment. See `PATENTS.md`.

## Third-party and generated material

Third-party material is not relicensed unless the notice for that material says
otherwise. Generated files inherit the license declared by their generated
artifact directory and must reproduce appropriate SPDX metadata when the output
format supports comments.

## No trademark grant

None of these licenses grants rights in the Nova name, logos, or certification
marks beyond nominative use allowed by law. See `TRADEMARKS.md`.
