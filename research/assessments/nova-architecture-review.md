# Nova architecture review

Status: non-normative research assessment.

## Strong ideas

- Separate Node identity from current location.
- Permit endpoint-influenced route and service selection.
- Combine privacy, routing characteristics, and economic accountability.
- Use strict strata instead of adding only another application overlay.
- Preserve the end-to-end principle while making network service characteristics explicit.

## Main architectural risk

The original design couples many independently difficult problems: global routing, private topology discovery, QoS negotiation, traffic-analysis resistance, micropayments, monetary issuance, proof of bandwidth, consensus, and incremental deployment. The first interoperable implementation must decompose these into independently testable profiles.

## Topics excluded from the first mandatory profile

- endogenous monetary policy;
- proof of bandwidth;
- validating consensus;
- mandatory constant-rate traffic and chaff;
- complete global Beacon and authority design;
- traffic-payment integration in every Gram.

These remain research tracks rather than hidden dependencies of P-Stratum or the first R-Stratum subset.

## Required quantitative work

Future specifications must bound router state, Path and Flow state, packet overhead, cryptographic operations, control traffic, chaff overhead, lookup complexity, failure recovery, and convergence.

## Privacy discipline

Claims must be scoped by attacker model. Link encryption does not establish relationship anonymity. Payment timing, rate changes, Path creation, first and last hops, and multi-link observers require separate analysis.

## Incremental deployment

Incremental deployment is represented by P-RAP Bindings over existing routed underlays. This is different from IP-over-Nova, which is a Compatibility Service carrying legacy IP as application payload.
