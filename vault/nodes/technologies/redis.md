---
id: redis
label: Redis
node_type: Technology
tags: [cache, nosql, in-memory, Technology]
summary: "In-memory data structure store used as cache, message broker, and session store. Sub-millisecond latency. Supports strings, hashes, lists, sets, sorted sets, streams, and more."
properties:
  created_by: "Salvatore Sanfilippo"
  first_release: 2009
  license: "BSD-3 (open source) / Redis Source Available (RSAL)"
  written_in: "C"
relationships:
  - type: OPTIMIZED_FOR
    target: caching
  - type: RELATED_TO
    target: postgres
---

Redis is the go-to solution for caching, session storage, rate limiting, and pub/sub messaging. Its data structures (sorted sets, HyperLogLog, streams) enable patterns not easily expressed in other stores.

## Common use cases

- **Application cache** — cache expensive DB query results
- **Session store** — stateless auth with TTL-backed session tokens
- **Rate limiting** — atomic incr + expire for sliding window counters
- **Leaderboards** — sorted sets with O(log n) rank queries
- **Pub/Sub** — lightweight message bus (not durable like Kafka)
- **RedisSearch** — full-text search + vector similarity (used in RAG)

## Redis vs Postgres for caching

Postgres can cache via materialized views and connection pooling, but Redis's in-memory nature gives 10-100x lower latency for hot data.

See also: [[caching]], [[kafka]], [[postgres]]
