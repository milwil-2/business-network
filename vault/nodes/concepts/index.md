---
id: index
label: Database Index
node_type: Concept
tags: [databases, performance, Concept]
summary: "A data structure that accelerates query lookups at the cost of additional storage and write overhead. B-tree indexes for range queries; hash indexes for equality; full-text for text search."
relationships:
  - type: RELATED_TO
    target: tree
  - type: RELATED_TO
    target: postgres
  - type: RELATED_TO
    target: neo4j
---

An index trades write performance and storage for faster reads. Without an index, every lookup is a full scan O(n). With a B-tree index, it becomes O(log n).

## Types

| Type | Best for | Structure |
|---|---|---|
| B-tree | Range queries, sorting | Balanced tree |
| Hash | Exact equality lookups | Hash table |
| Full-text | Text search (LIKE, contains) | Inverted index |
| Spatial | Geospatial queries | R-tree |
| Graph (Neo4j) | Node property lookups | B-tree on property |

## In graph databases

Neo4j indexes node properties (e.g. `MERGE (n:Person {id: $id})` is fast only if there's an index on `:Person(id)`). That's why `schema_constraints.cypher` creates uniqueness constraints — they imply an index.

See also: [[neo4j]], [[postgres]], [[tree]]
