<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-0019: Scope terminology by stratum

- Status: Proposed
- Date: 2026-08-01

## Context

The original unified glossary mixed P-Stratum and R-Stratum concepts. That encouraged definitions such as a P-Stratum Path being described directly as an R-Stratum Edge outside the P–R Interface specification.

## Decision

Each stratum owns a separate glossary. The common glossary contains only stratum-independent terms. Cross-stratum semantic mappings are defined exclusively by the corresponding versioned Interface documentation.

CI checks stratum documentation for obvious use of foreign canonical terminology. Scoped agent instructions identify the permitted glossary set.

## Consequences

- Strict layering is reflected in documentation and LLM context boundaries.
- Interface documents become the only authoritative place for cross-stratum mappings.
- Some existing documents and filenames must be renamed or rewritten.
- Lexical CI checks supplement but do not replace architectural review.
