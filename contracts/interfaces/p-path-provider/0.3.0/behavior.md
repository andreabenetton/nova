# Behavioral contract

The Path Provider Interface is private to P-Stratum. P-0AP, P-LAP, and P-RAP supply Provider Paths; P-Stratum common aggregates them into R-Stratum-visible Edges.

## Activation

`activate-provider` returns a provider instance, generation, atomic initial Path snapshot, and the first event sequence after that snapshot. Provider event sequence values are total and gap-detectable within the generation.

## Identity

Every announced Provider Path contains an authenticated Node identity. `AuthenticatedNodeIdentityId` is the equality key used by P-Stratum common. Address-set rotation with the same identifier updates a Path; a changed identifier may cause Edge replacement above this Interface.

## Submission

Every accepted Provider Submission has exactly one terminal result. Submission options preserve urgency, optional priority-prefix, and expiry semantics supplied by P-Stratum common. A provider may return `WOULD_BLOCK`; queues are finite and capacity recovery is observable.

## Reset and deactivation

Before `provider-reset`, unresolved accepted Provider Submissions complete with `PROVIDER_RESET`. The reset event is the final event of the generation. Orderly deactivation drains or terminally completes accepted Submissions before returning.

## Obfuscated degree

Every Provider Path snapshot includes the current remote-Peer Obfuscated degree notification. P-Stratum common reconciles values from multiple Paths to the same authenticated Peer and exposes one Edge-level hint. The value is an expansion cardinality, not a Path count.
