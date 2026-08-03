---
adr: ADR-P-0007
title: Classify P-0AP, P-LAP, and P-RAP as Path Provider protocols
scope: p-stratum
status: proposed
date: 2026-08-01
supersedes: []
superseded_by: []
affected_contracts: []
affected_documents: []
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# ADR-P-0007: Classify P-0AP, P-LAP, and P-RAP as Path Provider protocols

## Context

Earlier repository drafts sometimes called P-0AP, P-LAP, and P-RAP “Path Providers.” That wording conflates a protocol specification with a running component. It also makes it unclear what implements `NOVA-IF-P-PATH-PROVIDER`.

The repository also lacked one normative document collecting the objectives of P-Stratum without importing terminology owned by another stratum.

## Decision

P-0AP, P-LAP, and P-RAP are **Path Provider protocols**.

A **Path Provider implementation** implements one of those protocols and the Path Provider Interface. A running realization is a **Path Provider instance**. Provider Paths are created and maintained by Path Provider instances, not by protocol specifications themselves.

P-Stratum consists of P-Stratum common plus one or more Path Provider instances. P-Stratum common is independent of the protocol and implementation behind each instance.

The normative objectives of P-Stratum are maintained in `protocols/p-stratum/objectives.md`. That document uses only the common and P-Stratum glossaries. Cross-stratum mappings remain confined to explicit Interface documentation.

## Consequences

- `NOVA-IF-P-PATH-PROVIDER` names its provider role `Path Provider instance`.
- P-0AP, P-LAP, and P-RAP documentation describes protocol behavior rather than treating protocols as runtime components.
- Implementation manifests identify software that implements a Path Provider protocol.
- P-Stratum common consumes instances only through the versioned Path Provider Interface.
- The distinction can be checked in documentation and LLM context instructions.

## Alternatives rejected

### Treat each protocol name as a component type

This is concise but conflates specification, implementation, and runtime instance.

### Call P-0AP, P-LAP, and P-RAP sub-strata

They do not form separate strata and do not expose separate upper services. They are internal protocol families of P-Stratum.
