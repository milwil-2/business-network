---
id: cypher
label: Cypher
node_type: Concept
tags: [query-language, graph-db, Concept]
summary: "Declarative graph query language developed by Neo4j. Uses ASCII-art pattern syntax to express graph patterns. Analogous to SQL for relational databases."
properties:
  created_by: "Neo4j Inc"
  first_release: 2011
  standard: "openCypher (2015, open standard)"
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: RELATED_TO
    target: property-graph-model
---

Cypher uses an ASCII-art syntax where `()` represents nodes and `-->` or `-[:TYPE]->` represents relationships.

## Core patterns

```cypher
-- Match a node
MATCH (n:Person {name: 'Alice'}) RETURN n

-- Traverse a relationship
MATCH (a)-[:KNOWS]->(b) RETURN a.name, b.name

-- Create data
CREATE (a:Person {name: 'Bob'})-[:WORKS_AT]->(c:Company {name: 'Acme'})

-- Variable-depth traversal
MATCH (a)-[:KNOWS*1..3]->(b) RETURN DISTINCT b
```

## Key talking points

- **Declarative** — you describe the pattern, not the traversal algorithm
- **MERGE** — upsert semantics: create if not exists, match if exists
- **openCypher** — open standard, also supported by Memgraph, Amazon Neptune, Redis Graph

See also: [[neo4j]], [[graph-theory]]
