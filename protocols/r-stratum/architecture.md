# R-Stratum architecture

The first executable R-Stratum subset separates:

- Edge consumption and Close lifecycle;
- topology discovery and neighbor expansion;
- Route-label lifecycle;
- Trail identification and service-characteristic collection;
- Flow setup;
- Gram processing and forwarding;
- optional Facilities.

An Edge produces one Close. R-Stratum selects an Edge service profile for local SDU submission but never selects a Provider Path. Metrics are consumed with their units, source, freshness, and confidence.

Traffic payments, monetary issuance, proof of bandwidth, and validating consensus remain outside the mandatory first subset.
