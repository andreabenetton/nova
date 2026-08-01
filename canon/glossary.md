---
document_id: NOVA-CANON-GLOSSARY-INDEX
status: draft
normative: true
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Nova glossary index

Nova terminology is scoped by architectural ownership. There is no unified glossary that may redefine terms across strata.

- [Common terminology](glossary/common.md) contains only concepts independent of a particular stratum.
- [P-Stratum terminology](../protocols/p-stratum/glossary.md) is authoritative for P-Stratum documents.
- [R-Stratum terminology](../protocols/r-stratum/glossary.md) is authoritative for R-Stratum documents.
- [O-Stratum terminology](../protocols/o-stratum/glossary.md) is authoritative for O-Stratum documents.
- [P–R Interface terminology](../contracts/interfaces/p-r/glossary.md) defines only the mapping across that boundary.
- [R–O Interface terminology](../contracts/interfaces/r-o/glossary.md) defines only the mapping across that boundary.
- [O–Application Interface terminology](../contracts/interfaces/o-a/glossary.md) defines only the mapping across that boundary.

A term owned by one stratum must not be used to define another stratum. Terms from two strata may appear together only in documentation explicitly describing their versioned Interface.
