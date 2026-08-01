<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# IP-over-Nova MTU and fragmentation

The common profile derives the virtual-interface MTU from the maximum O-Stratum message payload minus IP-over-Nova overhead. Platform Attachments apply the value to the host.

The first profile should avoid outer underlay fragmentation and should preserve one inner IP datagram as one IP-over-Nova message at the O-Stratum boundary.
