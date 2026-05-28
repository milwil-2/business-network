---
id: caching
label: Caching
node_type: Pattern
tags: [performance, architecture, Pattern]
summary: "Storing copies of expensive-to-compute results closer to consumers for faster access. Trades consistency for latency and throughput. Core tradeoff: cache hit rate vs staleness."
relationships:
  - type: RELATED_TO
    target: redis
  - type: RELATED_TO
    target: index
---

Caching is the universal performance pattern: instead of recomputing or re-fetching expensive data, store a copy where it can be retrieved in O(1).

## Cache strategies

| Strategy | Description | Use when |
|---|---|---|
| **Cache-aside** | App checks cache, on miss loads from DB and populates | Read-heavy, can tolerate cold starts |
| **Write-through** | Write to cache and DB simultaneously | Consistency important |
| **Write-behind** | Write to cache immediately, async persist to DB | High write throughput, tolerate some loss |
| **Read-through** | Cache fills itself on miss transparently | Simplifies app code |

## Invalidation

"Cache invalidation is one of the two hard problems in CS." Options:
- **TTL** — expire after N seconds (simple, always stale for some window)
- **Event-driven** — invalidate on mutation events (precise, more complex)
- **Version tags** — cache key includes version; increment to invalidate

## Graph DB caching

Neo4j's query cache stores compiled Cypher plans. Application-level caching of graph traversal results in Redis is a common pattern for expensive multi-hop queries.

See also: [[redis]], [[index]]
