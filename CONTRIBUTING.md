# Contributing

## Change categories

- **Editorial**: no semantic behavior change.
- **Compatible contract addition**: allowed only under the declared minor-version rules.
- **Breaking contract change**: requires a new major version, migration notes, an ADR, and updated conformance suites.
- **Protocol change**: update peer protocol, wire schema, vectors, and interoperability tests.
- **Integration change**: update only the relevant Adapter, Binding, or Platform Attachment unless the public contract changes.

## Required workflow

1. Identify the authoritative document and boundary.
2. Read its `CONTEXT.yaml` and adjacent contract.
3. Add or update an ADR when the change is architectural.
4. Update NIDL and conformance scenarios first.
5. Regenerate derived artifacts.
6. Implement behind the generated interface.
7. Run structural, semantic, provider, consumer, and interoperability checks applicable to the change.

Published version directories are immutable. Corrections that alter behavior require a new version.
