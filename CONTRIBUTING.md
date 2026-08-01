<!-- SPDX-License-Identifier: CC-BY-4.0 -->

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

## Licensing and DCO

Nova is a multi-licensed repository. Before adding or moving a file:

1. identify its architectural role;
2. consult `legal/license-policy.yaml` and the nearest `LICENSE.md`;
3. add the applicable `SPDX-License-Identifier` where the format supports comments;
4. ensure each new directory has a `LICENSE.md`; and
5. run `make licenses`.

Do not copy AGPL core implementation into Apache-licensed Interface, Adapter,
Binding, Platform Attachment, SDK, or conformance components. Shared behavior
must cross a published versioned Interface rather than a private implementation
API.

Every contribution must certify the Developer Certificate of Origin 1.1 in the
root `DCO` file by adding a commit trailer:

```text
Signed-off-by: Full Name <email@example.com>
```

Use `git commit -s` to add the trailer. Sign-off certifies the right to submit
under the file's declared license; it does not assign copyright and does not
create the specification patent commitment described in `PATENTS.md`.
