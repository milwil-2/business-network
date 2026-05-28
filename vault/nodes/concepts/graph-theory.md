---
id: graph-theory
label: Graph Theory
node_type: Concept
tags: [math, foundations, Concept]
summary: "Mathematical study of graphs — structures made of vertices (nodes) connected by edges. Foundation for all graph databases and network algorithms."
properties:
  origin: "Leonhard Euler, 1736 (Königsberg bridges)"
  branch: "Discrete mathematics"
relationships:
  - type: ENABLES
    target: property-graph-model
  - type: ENABLES
    target: adjacency-list
  - type: ENABLES
    target: bfs
  - type: ENABLES
    target: dfs
  - type: EXTENDS
    target: dag
  - type: EXTENDS
    target: tree
---

Graph theory provides the mathematical foundation for reasoning about connected data. A **graph** G = (V, E) where V is a set of vertices and E is a set of edges.

Key concepts for interviews:
- **Directed vs undirected** — edges have or lack direction
- **Weighted graphs** — edges carry numeric weights
- **Connectivity** — whether all nodes are reachable from any node
- **Cycles** — paths that return to their starting node

## Why it matters for graph databases

Graph DBs are direct implementations of graph theory. Cypher pattern matching maps to subgraph isomorphism. `shortestPath()` maps to Dijkstra/BFS. Variable-depth traversal `[*1..n]` is just graph exploration with a depth limit.

See also: [[property-graph-model]], [[bfs]], [[dijkstra]]
