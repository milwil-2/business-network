---
id: postgres
label: PostgreSQL
node_type: Technology
tags: [relational-db, sql, Technology]
summary: "The most advanced open-source relational database. Full ACID compliance, extensive indexing options, JSONB for semi-structured data, and strong extension ecosystem (pgvector, PostGIS, TimescaleDB)."
properties:
  created_by: "PostgreSQL Global Development Group"
  first_release: 1996
  license: "PostgreSQL License (MIT-like)"
  written_in: "C"
relationships:
  - type: IMPLEMENTS
    target: transaction
  - type: IMPLEMENTS
    target: index
  - type: RELATED_TO
    target: neo4j
---

PostgreSQL is the benchmark relational database — it's the default choice for most applications and the reference point for understanding what graph DBs do differently.

## Graph queries in Postgres

Postgres can model graphs using self-referential tables, but deep traversal is painful:

```sql
-- Find all managers up to 5 levels above employee #42
WITH RECURSIVE managers AS (
  SELECT id, manager_id, 1 AS depth
  FROM employees WHERE id = 42
  UNION ALL
  SELECT e.id, e.manager_id, m.depth + 1
  FROM employees e JOIN managers m ON e.id = m.manager_id
  WHERE m.depth < 5
)
SELECT * FROM managers;
```

Compare to Cypher: `MATCH path = (e {id: 42})-[:REPORTS_TO*1..5]->(m) RETURN m`

## When Postgres wins over Neo4j

- Complex aggregation, reporting, analytics
- Tabular data with clear schema
- Mature tooling ecosystem (ORMs, migration tools)
- Horizontal sharding with Citus

See also: [[neo4j]], [[transaction]], [[index]]
