# Reset ordering

A provider reset is terminal for one provider generation.

1. Stop accepting Provider Submissions.
2. Emit exactly one terminal `PROVIDER_RESET` result for every unresolved accepted Submission.
3. Emit `provider-reset` as the final event of the generation.
4. Invalidate every Path identifier, revision, Submission identifier, and event sequence in that generation.
5. Require P-Stratum common to activate a new provider generation before further use.
