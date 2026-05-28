---
id: event-sourcing
label: Event Sourcing
node_type: Pattern
tags: [architecture, cqrs, Pattern]
summary: "Architectural pattern where state is derived by replaying an immutable log of events rather than storing current state directly. Every change is an append-only event. State = fold(events). Used in financial systems, audit logs, and collaborative applications."
relationships:
  - type: RELATED_TO
    target: cqrs
  - type: USED_IN
    target: kafka
---

In event sourcing, you never update a record in place. Instead, you append an event:

```
AccountCreated { id: 42, owner: "Alice", balance: 0 }
MoneyDeposited { id: 42, amount: 500 }
MoneyWithdrawn  { id: 42, amount: 200 }
→ Current balance: 300
```

The current state is always derived by replaying from the beginning (or a snapshot + recent events).

## Benefits

- **Full audit log** — every state change is recorded forever
- **Time travel** — replay to any past point in time
- **Event-driven** — events are the integration contract between services
- **CQRS-friendly** — events build separate read models for different query patterns

## Downsides

- **Eventual consistency** — read models lag behind writes
- **Schema evolution** — old events must still be deserializable
- **Query complexity** — "what is the current state?" requires replay or a snapshot

## Common implementation

[[kafka]] as the event log + consumer groups that project events into read models (Postgres, Elasticsearch, Redis).

See also: [[cqrs]], [[kafka]]
