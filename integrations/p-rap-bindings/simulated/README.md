<!-- SPDX-License-Identifier: Apache-2.0 -->


# Simulated P-RAP Binding

This Binding implements `NOVA-IF-P-RAP-BINDING` over the Virtual Fabric. It allows the real P-RAP protocol to be tested deterministically before IPv4-QUIC or IPv6-QUIC is available.

The Binding declares configurable delivery, ordering, message-boundary, congestion-control, and locator-migration properties. It does not implement or redefine P-RAP Association semantics.
