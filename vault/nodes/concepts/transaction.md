---
id: transaction
label: Transaction (ACID)
node_type: Concept
tags: [databases, consistency, Concept]
summary: "A unit of work that is Atomic, Consistent, Isolated, and Durable. Guarantees that either all operations in a group succeed, or none take effect."
relationships:
  - type: RELATED_TO
    target: neo4j
  - type: RELATED_TO
    target: postgres
---

ACID properties:

| Property | Meaning |
|---|---|
| **Atomic** | All-or-nothing — partial writes never visible |
| **Consistent** | Constraints always satisfied before and after |
| **Isolated** | Concurrent transactions don't see each other's partial state |
| **Durable** | Committed writes survive crashes (written to disk/WAL) |

## Neo4j and transactions

Neo4j is fully ACID-compliant (unlike some NoSQL graph stores). Every Cypher write runs in a transaction. Multiple writes can be batched in an explicit transaction:

```cypher
BEGIN
CREATE (a:Person {name: 'Alice'})
CREATE (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS]->(b)
COMMIT
```

This matters for the Python sync script: if a node write fails mid-batch, no partial state is committed.

See also: [[neo4j]], [[postgres]]
