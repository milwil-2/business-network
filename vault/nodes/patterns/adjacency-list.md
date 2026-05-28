---
id: adjacency-list
label: Adjacency List
node_type: Pattern
tags: [graph-representation, data-structures, Pattern]
summary: "Graph storage representation where each node keeps a list of its neighbors. O(V+E) space. Used in sparse graphs. The native storage format of most graph databases including Neo4j."
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: ENABLES
    target: bfs
  - type: ENABLES
    target: dfs
  - type: RELATED_TO
    target: neo4j
---

An adjacency list stores a graph as a mapping from each node to its list of neighbors.

```python
graph = {
    'neo4j':       ['property-graph-model', 'cypher'],
    'cypher':      ['graph-theory'],
    'bfs':         ['graph-theory'],
    'dijkstra':    ['bfs'],
}
```

## vs Adjacency Matrix

| | Adjacency List | Adjacency Matrix |
|---|---|---|
| Space | O(V + E) | O(V²) |
| Check edge (u, v) | O(degree(u)) | O(1) |
| Iterate neighbors | O(degree(u)) | O(V) |
| Best for | Sparse graphs | Dense graphs |

## In Neo4j

Neo4j's native storage IS an adjacency list — each node record contains pointers to its first relationship, and relationships form a doubly-linked list. This is why traversal is O(1) per hop rather than O(log n) for a JOIN.

See also: [[graph-theory]], [[neo4j]], [[bfs]]
