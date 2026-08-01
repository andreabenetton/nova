# QUIC common specification stub

The proposed first profile uses:

- one QUIC connection per active Binding instance unless multiplexing rules say otherwise;
- one reliable bidirectional control stream for P-RAP control;
- QUIC DATAGRAM for message-oriented data where negotiated;
- QUIC streams for reliable data when required;
- QUIC congestion control, loss recovery, encryption, and path validation;
- Nova identity bound to the QUIC channel;
- no second independent congestion controller above QUIC.

P-RAP Association identity remains separate from the QUIC connection.
