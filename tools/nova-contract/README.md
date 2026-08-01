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

The current normalizer uses deterministic sorted JSON. Full RFC 8785 JSON Canonicalization is proposed but not yet claimed by this implementation.
