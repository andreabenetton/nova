<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# P-Stratum common architecture

P-Stratum common consumes Provider Paths through `NOVA-IF-P-PATH-PROVIDER 0.3.0` and does not depend on P-0AP, P-LAP, P-RAP, Adapter, Binding, locator, or Virtual Fabric implementation details.

Its P-Stratum responsibilities are:

- validate the authenticated Node identity supplied with each Provider Path;
- group usable Paths with the same Node identity into one Peer;
- construct provider-independent delivery capabilities;
- select the Provider Path or Paths used for each accepted transfer;
- reconcile expansion-cardinality contributions;
- own finite queues, backpressure, transfer lifecycle, and provider restart handling;
- implement `NOVA-IF-P-R 0.2.0` without exporting private P-Stratum mechanics.

The semantic mapping from P-Stratum concepts to R-Stratum concepts is defined only in `contracts/interfaces/p-r/`.
