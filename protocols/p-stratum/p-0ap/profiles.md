<!-- SPDX-License-Identifier: CC-BY-4.0 -->


# P-0AP profiles

## Loopback

Returns submitted SDUs to the same local P-Stratum instance. Intended for serialization, queue, and smoke tests. It does not normally expose an Edge.

## Paired node

Connects two distinct Node instances with independent state. This is the minimum useful P-0AP profile and the first R-Stratum integration target.

## Virtual fabric

Connects an arbitrary graph of Nodes and modeled Paths through the reusable Virtual Fabric. Every Path may have independent characteristics and scheduled failures.

## Replay

Replays a recorded deterministic trace of Path events, characteristic changes, virtual-time advancement, SDU delivery, and failure.

## Adversarial provider

Intentionally violates one or more Interface invariants to test defensive behavior. This profile must be explicitly selected and test output must be labeled as non-conforming provider behavior.
