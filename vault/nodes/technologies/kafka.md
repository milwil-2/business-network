---
id: kafka
label: Apache Kafka
node_type: Technology
tags: [streaming, messaging, Technology]
summary: "Distributed event streaming platform. Durable, ordered, replayable log of events. Used for event sourcing, stream processing, decoupled microservices, and change data capture."
properties:
  created_by: "LinkedIn (Apache Foundation)"
  first_release: 2011
  license: "Apache-2.0"
  written_in: "Scala / Java"
relationships:
  - type: ENABLES
    target: event-sourcing
  - type: RELATED_TO
    target: cqrs
---

Kafka is a distributed commit log. Producers append events to topics; consumers read from arbitrary offsets. Events are retained for a configurable duration (default 7 days), enabling replay.

## Core concepts

- **Topic** — named, ordered, durable log of events
- **Partition** — horizontal scaling unit within a topic
- **Consumer group** — multiple consumers sharing a topic, each partition consumed by one
- **Offset** — position within a partition (enables replay, exactly-once)

## Event sourcing with Kafka

Kafka is the backbone for event-sourced systems: every state change is published as an immutable event. The current state is derived by replaying from offset 0. This is the [[event-sourcing]] pattern.

## Kafka vs Redis Pub/Sub

| | Kafka | Redis Pub/Sub |
|---|---|---|
| Durability | ✅ Persisted log | ❌ Fire and forget |
| Replay | ✅ Any offset | ❌ No history |
| Ordering | ✅ Per partition | ✅ Per channel |
| Throughput | Very high | Very high |

See also: [[event-sourcing]], [[cqrs]], [[redis]]
