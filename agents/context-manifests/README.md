# Context manifests

Every component should carry a `CONTEXT.yaml` validated by the NIDL context schema. A manifest lists:

- required authoritative context;
- optional rationale or research context;
- forbidden context that would violate the knowledge boundary;
- consumed and provided Interface versions.

CI verifies that paths exist and that implementation dependencies respect the corresponding boundary policy.
