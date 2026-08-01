
# Fault model

Supported Path- or link-level faults may include:

- bounded delay and jitter;
- loss;
- duplication;
- reordering;
- bandwidth reduction;
- queue exhaustion and backpressure;
- one-way or two-way partition;
- endpoint pause, restart, or removal;
- characteristic update;
- malformed-unit injection by an explicitly adversarial front end.

Conforming mode translates lower faults into behavior permitted by the front end's Interface. Intentional Interface violations require adversarial provider mode.
