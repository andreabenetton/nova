<!-- SPDX-License-Identifier: Apache-2.0 OR CC-BY-4.0 -->


# Deterministic scheduler

Events are ordered by:

1. virtual timestamp;
2. event class priority defined by the scheduler version;
3. source endpoint identifier;
4. link identifier;
5. monotonically allocated event sequence.

A scheduler implementation must publish its event class order and pseudo-random algorithm. Parallel execution may optimize a run only when it preserves the exact reference trace.
