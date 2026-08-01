<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Licensing architecture

Nova uses licensing boundaries that follow its technical boundaries. The policy
is designed to keep modifications to the protocol core reciprocal while making
integration surfaces usable by operating-system, hardware, network, and tooling
vendors.

This document explains the policy; `legal/license-policy.yaml` and file-level
SPDX identifiers are the enforceable repository metadata.

## Policy goals

1. Modified Nova core implementations should remain available to the community,
   including when operated as a network service.
2. Independent Adapters, Bindings, Platform Attachments, SDKs, and conformance
   tools should be reusable without importing AGPL core code.
3. The protocol specifications must be readable and implementable independently
   of the reference implementation.
4. Machine-readable contracts must be usable both as specification content and
   as inputs to code generators.
5. No patent commitment or trademark permission should be implied accidentally.
6. Historical papers containing third-party material must not be relicensed
   before a rights review.

## Core implementation: AGPL-3.0-or-later

The following implementation roles are AGPL core:

- P-Stratum common;
- P-0AP and its control implementation;
- P-LAP;
- P-RAP;
- R-Stratum;
- O-Stratum;
- the Nova node daemon; and
- the IP-over-Nova Compatibility Service.

The AGPL choice is intended to preserve source availability for modified core
implementations, including covered network-service deployments. It does not
turn the normative protocol specifications into AGPL documents.

## Permissive integration surfaces: Apache-2.0

The following are Apache-licensed:

- inter-component Interface crates and shared public types;
- P-LAP Adapter implementations;
- P-RAP Binding implementations;
- Platform Attachments;
- simulated Adapters and Bindings;
- the Virtual Fabric and conformance harnesses;
- examples, tests, fuzzing, build tooling, packaging, and CI support; and
- generated implementation SDKs.

This permits independent or proprietary providers to implement a published
versioned boundary without copying AGPL core code.

### Linking and process boundaries

An Apache-licensed provider linked into an AGPL executable does not cause the
combined executable to become Apache-licensed. The provider's source remains
available separately under Apache-2.0, but the distributor of the combination
must assess and comply with all applicable terms.

Nova therefore treats out-of-process provider protocols as the preferred
license-isolation and privilege-isolation boundary for external providers:

```text
AGPL Nova core process
        |
        | versioned local IPC contract
        |
Apache, proprietary, or separately licensed provider process
```

A process boundary is not an automatic legal safe harbour. It is nevertheless a
clearer technical separation than a private in-process API. The repository does
not currently include a custom AGPL linking exception. Adding one would require
specialist legal review and a separate accepted ADR.

The same separation supports the user-space execution policy: a minimal
platform-specific privileged shim may be Apache-licensed while all Nova protocol
semantics remain in the AGPL user-space core.

## Documentation: CC-BY-4.0

Architecture, protocol prose, ADRs, manuals, compatibility profiles, and
project-authored diagrams use CC-BY-4.0. This permits commercial reuse,
quotation, translation, and adaptation with attribution.

Creative Commons licenses are not used for software implementation files.

## Contracts and schemas: Apache-2.0 OR CC-BY-4.0

NIDL contracts, schemas, registries, simulation fixtures, and generated contract
documentation are dual-licensed:

```text
Apache-2.0 OR CC-BY-4.0
```

An implementer may consume them under Apache-2.0 as functional implementation
inputs, or reuse them under CC-BY-4.0 as specification material.

## Historical source papers

`research/original-papers/` is marked
`LicenseRef-Nova-Research-Draft-Restricted`. The restriction is temporary but
necessary because the PDFs include third-party figures and quotations whose
redistribution and adaptation rights have not been fully audited. New normative
Nova documentation must not copy such material unless its rights are recorded
in `THIRD_PARTY_NOTICES.md`.

## Patents

CC-BY-4.0 addresses copyright, not implementation-essential patents. The
project intends to apply OWFa 1.0 Patent Only separately to each stable final
specification. No `0.x` draft is currently designated a Final Specification,
and `patents/final-specifications.yaml` is initially empty.

Before a `1.0` designation, the project needs:

- confirmed authority of the applicable signatory or Bound Entity;
- a specification contribution and patent-disclosure process;
- an executed OWFa record for the exact immutable version; and
- an entry in the public Final Specification registry.

## Contributions and ownership

Contributors retain copyright unless they make a separate written assignment.
Every commit must carry a DCO sign-off. The DCO certifies the contributor's
right to submit under the file's declared license but is not a patent agreement.

The owner of pre-existing Nova material must be confirmed before public release.
The repository does not infer ownership from an author's affiliation.

## SPDX and directory notices

Commentable files carry an `SPDX-License-Identifier` where doing so does not
break a published contract, generated artifact, strict adapter file, or binary
format. Non-commentable and immutable files are covered by the nearest
`LICENSE.md` and the machine-readable path policy.

Every repository directory carries a `LICENSE.md` marker. A marker states either
one applicable license or that the directory is mixed and its child/file SPDX
metadata must be consulted.

CI runs:

```text
make licenses
```

The check validates path classification, license texts, directory markers,
SPDX headers, and Rust package license metadata.

## Legal review

This policy is an engineering recommendation and repository configuration, not
legal advice. Patent ownership, pre-existing copyright ownership, trademark
clearance, a future OWFa process, and any proprietary provider deployment
should be reviewed by qualified counsel before public or commercial release.
