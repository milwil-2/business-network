---
id: cqrs
label: CQRS (Command Query Responsibility Segregation)
node_type: Pattern
tags: [architecture, Pattern]
summary: "Architecture pattern that separates the write model (commands that mutate state) from the read model (queries that return data). Allows each side to be independently optimized and scaled."
relationships:
  - type: RELATED_TO
    target: event-sourcing
  - type: ENABLES
    target: kafka
---

CQRS splits your application into two models:

- **Command side** — handles writes: validates business rules, mutates state, emits events
- **Query side** — handles reads: pre-computed, denormalized, optimized for specific queries

## Why split them?

Write and read patterns often have different requirements:
- Writes need strong consistency, validation, audit trails
- Reads need speed, different shapes (denormalized), and may be eventually consistent

## Example

A banking app:
- **Command**: `TransferMoney(from: 1, to: 2, amount: 100)` → emits `MoneyTransferred` event
- **Query side A**: Postgres view `account_balance` — updated by event projector
- **Query side B**: Elasticsearch index `transaction_history` — for full-text search
- **Query side C**: Redis sorted set `top_spenders` — for real-time leaderboard

## CQRS + Event Sourcing

Often used together: events (from event sourcing) are the bridge between command and query sides. The event log is the source of truth; query sides are projections.

See also: [[event-sourcing]], [[kafka]], [[postgres]]
