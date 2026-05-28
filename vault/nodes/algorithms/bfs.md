---
id: bfs
label: BFS (Breadth-First Search)
node_type: Algorithm
tags: [graph-traversal, algorithms, Algorithm]
summary: "Graph traversal that explores all neighbors at depth d before moving to depth d+1. Finds shortest paths in unweighted graphs. O(V+E) time, O(V) space for the queue."
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: IS_VARIANT_OF
    target: dfs
  - type: USED_IN
    target: adjacency-list
---

BFS uses a **queue** (FIFO). Start at a source node, enqueue it, then repeatedly dequeue a node, visit its unvisited neighbors, and enqueue them.

## Properties

- **Shortest path in unweighted graphs** — BFS always finds the fewest-hop path first
- **Level-order traversal** — visits all nodes at distance k before distance k+1
- **O(V + E)** time complexity

## Implementation (Python)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

## In Neo4j / Cypher

Cypher's variable-depth traversal `[*1..n]` uses BFS by default:
```cypher
MATCH (a {id: 'bfs'})-[*1..3]->(b) RETURN DISTINCT b
```

`shortestPath()` also uses BFS internally for unweighted graphs.

See also: [[dfs]], [[dijkstra]], [[graph-theory]]
