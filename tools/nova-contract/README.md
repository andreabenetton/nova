<!-- SPDX-License-Identifier: Apache-2.0 -->

# nova-contract

Experimental CLI for the Nova contract system.

```sh
python3 -m pip install -e tools/nova-contract
nova-contract validate contracts
nova-contract normalize contracts
nova-contract lint contracts
nova-contract context .
nova-contract boundaries canon/dependency-policy.yaml implementations/rust
```

`lint` always checks identifier uniqueness, declared errors, type-field references, state transitions, Interface/scenario identities, implementation declarations, and conformance coverage. Contracts that set:

```yaml
compatibility:
  type_references: strict
```

also require every operation input, success result, and event payload to resolve to a declared NIDL type. Current P-R, Path Provider, and P-0AP Control development baselines enable this mode; older preserved experimental scaffolds do not acquire new obligations retroactively.

The current normalizer uses deterministic sorted JSON. Full RFC 8785 JSON Canonicalization is proposed but not yet claimed by this implementation.
