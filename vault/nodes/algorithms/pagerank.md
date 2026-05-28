---
id: pagerank
label: PageRank
node_type: Algorithm
tags: [graph-algorithms, ranking, Algorithm]
summary: "Iterative algorithm that measures node importance based on the number and quality of incoming links. Originally developed by Google. Converges via power iteration. Used for web ranking, knowledge graph centrality, and recommendation."
properties:
  invented_by: "Larry Page, Sergey Brin"
  year: 1998
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: RELATED_TO
    target: neo4j
---

PageRank models a random surfer: at each step, follow a random outgoing link with probability d (damping factor, ~0.85), or jump to a random node with probability 1-d. A node's rank = probability the surfer is on it at steady state.

## Formula

`PR(u) = (1 - d) / N + d * Σ (PR(v) / OutDegree(v))` for all v pointing to u

## Key properties

- **Recursive** — a node's rank depends on the ranks of nodes linking to it
- **Converges** — power iteration until change < ε (typically ~20-50 iterations)
- **Damping factor** — models probability of random restart (avoids rank sinks)

## In Neo4j GDS

```cypher
CALL gds.pageRank.stream('myGraph', {maxIterations: 20, dampingFactor: 0.85})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).label AS name, score
ORDER BY score DESC LIMIT 10
```

## Interview talking point

PageRank is the graph-native answer to "which nodes are most important?" — analogous to degree centrality (Q6 in demo queries) but recursive and link-quality aware.

See also: [[graph-theory]], [[neo4j]]
