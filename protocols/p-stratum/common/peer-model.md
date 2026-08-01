<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Peer model

A Peer is an authenticated Node reachable through one or more usable P-Stratum Paths. P-Stratum common groups Paths exclusively by the profile-qualified Node identity, never by locator, address-set equality, or provider-local identifier.

A local Peer handle remains stable for the corresponding identity during one Interface instance. Valid Node-address growth or rotation updates the same Peer. A different authenticated identity creates a different Peer and handle.

The first usable Path creates a Peer aggregate. Later Paths update that aggregate. Removing one Path does not remove the Peer while another usable Path remains. Removing the last usable Path terminates the aggregate after accepted transfers have reached terminal results.

The mapping from this private model to the upper stratum is defined only in the P–R Interface documentation.
