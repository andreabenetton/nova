<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Stratum-scoped terminology

Nova terminology is owned by the architectural layer in which the concept exists. A unified glossary made it too easy to describe one stratum with another stratum's private model, weakening strict separation and giving repository agents excessive context.

## Sources of truth

- `canon/glossary/common.md`: stratum-independent terms only.
- `protocols/p-stratum/glossary.md`: P-Stratum terms.
- `protocols/r-stratum/glossary.md`: R-Stratum terms.
- `protocols/o-stratum/glossary.md`: O-Stratum terms.
- `contracts/interfaces/*/glossary.md`: cross-boundary mappings.

`canon/glossary.md` is an index, not a combined glossary.

## Rule

A stratum document may use its own glossary and the common glossary. It must not use another stratum's owned vocabulary to define its behavior. A sentence containing owned terms from two strata is valid only in documentation explicitly describing their versioned Interface.

Examples:

- P-Stratum: “A Path is established with a Peer.”
- R-Stratum: “An Edge establishes a Close in the local view.”
- P–R Interface: “One or more Paths to the same Peer are represented as one Edge and one Close.”

The third sentence is prohibited in either stratum glossary and belongs only under `contracts/interfaces/p-r/`.

## Enforcement

`tools/check_terminology.py` scans normative stratum documentation for foreign owned terms. The check is intentionally conservative: it focuses on capitalized canonical terminology and allows Interface directories to combine vocabularies. Review remains necessary for semantic misuse that lexical checks cannot detect.

Every scoped agent instruction and context manifest must point to the applicable glossary rather than loading all stratum glossaries.
