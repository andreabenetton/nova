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

## Licensing rules

- Follow `legal/license-policy.yaml`; do not change a file's license by moving or copying it across a boundary without review.
- New files require the correct SPDX identifier where the format supports comments.
- Every new directory requires a `LICENSE.md` marker.
- Core crates are AGPL; Interface, Adapter, Binding, Platform Attachment, tooling, and conformance crates are Apache-2.0.
- Do not copy AGPL core implementation into Apache-licensed integration components.
- Run `make licenses` after adding, moving, or generating files.
