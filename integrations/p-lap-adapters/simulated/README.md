<!-- SPDX-License-Identifier: Apache-2.0 -->


# Simulated P-LAP Adapter

This Adapter implements `NOVA-IF-P-LAP-ADAPTER` over the Virtual Fabric. It allows the real P-LAP protocol to be tested deterministically without Ethernet hardware or privileges.

It models Adapter-level frame delivery, discovery primitives, MTU, lower-layer availability, and optional congestion indications. It does not bypass P-LAP by directly creating Paths.
