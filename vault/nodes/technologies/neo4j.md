---
id: neo4j
label: Neo4j
node_type: Technology
tags: [graph-db, nosql, Technology]
summary: "The world's most widely deployed native graph database. Uses the property graph model and Cypher query language. ACID-compliant, supports APOC procedures and GDS (Graph Data Science) library."
properties:
  created_by: "Neo4j Inc"
  first_release: 2007
  license: "GPL-3 (Community) / Commercial (Enterprise)"
  written_in: "Java"
  current_version: "5.x"
relationships:
  - type: IMPLEMENTS
    target: property-graph-model
  - type: USES_QUERY_LANGUAGE
    target: cypher
  - type: IMPLEMENTS
    target: transaction
  - type: RELATED_TO
    target: index
  - type: COMPETES_WITH
    target: postgres
---

Neo4j stores data as a native graph — nodes, relationships, and properties are stored directly on disk as a linked structure. Traversal follows physical pointers, so relationship traversal is O(1) per hop rather than O(log n) as with a JOIN.

## Architecture

- **Native graph storage** — not a graph layer over a relational DB
- **Bolt protocol** — binary protocol for driver connections
- **Neo4j Browser** — built-in web UI at `localhost:7474`
- **APOC library** — 450+ utility procedures (string manipulation, graph algorithms, data import)
- **GDS library** — production-grade graph algorithms (PageRank, community detection, etc.)

## When to use Neo4j vs Postgres

| Scenario | Neo4j | Postgres |
|---|---|---|
| Deep relationship traversal | ✅ O(hops) | ❌ O(n) or recursive CTE |
| Known-depth lookups | Competitive | Competitive |
| Complex ad-hoc queries | Cypher easier | SQL more mature tooling |
| Reporting / analytics | Limited | Strong |
| ACID transactions | ✅ Full | ✅ Full |

See also: [[cypher]], [[property-graph-model]], [[postgres]]
