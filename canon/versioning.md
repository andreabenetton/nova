---
document_id: NOVA-CANON-VERSIONING
status: draft
normative: true
---

# Versioning

Nova maintains independent version domains for:

- NIDL language;
- inter-stratum Interface contracts;
- Path Provider interfaces;
- Adapter interfaces;
- Binding interfaces;
- Platform Attachment interfaces;
- peer protocols;
- wire formats;
- concrete integrations;
- language-specific implementation APIs.

## Interface version

Stable interfaces use `MAJOR.MINOR.PATCH` in repository metadata.

- Major: incompatible semantic change.
- Minor: backward-compatible optional addition.
- Patch: editorial or clarifying release with no behavior change.

During `0.x`, breaking changes may occur, but every component must pin the exact version and contract fingerprint.

Capabilities are not versions. Optional behavior is negotiated or declared through capabilities within a versioned baseline.

## Peer-protocol version

Peer protocols have independent version negotiation and wire-version identifiers. Changing an Adapter or Binding implementation does not change the peer-protocol version unless peer-observable behavior changes.

## Compatibility

Within a stable major interface version, implementations select the highest mutually supported minor version. Different major versions require an explicit compatibility shim.

## Immutability

A published version directory is immutable. Any normative correction that changes implementation behavior creates a new version.
