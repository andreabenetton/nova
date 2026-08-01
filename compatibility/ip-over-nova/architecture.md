<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# IP-over-Nova architecture

```text
Legacy application
   |
host TCP/UDP and IP stack
   |
Platform Attachment
   |
IP-over-Nova Compatibility Service
   |
NOVA-IF-O-A
   |
O-Stratum -> R-Stratum -> P-Stratum
```

The common service handles encapsulation, destination mapping, MTU policy, profile behavior, authorization, and errors. Platform Attachments handle operating-system virtual interfaces and route configuration.
