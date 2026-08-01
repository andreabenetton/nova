# P-LAP wire-format stub

No wire format is frozen. The final format must separate pre-association framing from post-association protected framing. Stable Nova Node addresses and post-association message types should not be exposed unnecessarily in cleartext.

Required future artifacts:

- binary schema;
- integer widths and byte order;
- AEAD nonce construction;
- authenticated-data coverage;
- maximum sizes;
- positive and negative vectors;
- malformed-frame behavior.
