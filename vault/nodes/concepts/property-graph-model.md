---
id: property-graph-model
label: Property Graph Model
node_type: Concept
tags: [data-model, graph-db, Concept]
summary: "Data model where nodes and edges both carry arbitrary key-value properties and typed labels. Used by Neo4j, Amazon Neptune, and most modern graph databases."
properties:
  alternative: "RDF (Resource Description Framework) — W3C standard"
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: RELATED_TO
    target: cypher
---

The property graph model has four components:

| Component | Description | Example |
|---|---|---|
| **Nodes** | Entities with labels and properties | `(:Person {name: 'Alice', age: 30})` |
| **Relationships** | Typed, directed edges with properties | `-[:KNOWS {since: 2020}]->` |
| **Labels** | Tags on nodes for type grouping | `:Person`, `:Company` |
| **Properties** | Key-value pairs on nodes or edges | `{name: 'Alice'}` |

## vs RDF (the other graph model)

| | Property Graph | RDF |
|---|---|---|
| Data unit | Node/edge with properties | Triple (subject, predicate, object) |
| Query language | Cypher / GQL | SPARQL |
| Best for | App development, operational graphs | Semantic web, linked data |
| Example DB | Neo4j, Amazon Neptune (PG mode) | Apache Jena, Stardog |

See also: [[neo4j]], [[cypher]], [[graph-theory]]
