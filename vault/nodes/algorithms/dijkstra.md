---
id: dijkstra
label: Dijkstra's Algorithm
node_type: Algorithm
tags: [shortest-path, algorithms, Algorithm]
summary: "Single-source shortest path algorithm for weighted graphs with non-negative edge weights. Uses a min-heap priority queue. O((V + E) log V) time. Used in routing, navigation, and network analysis."
properties:
  invented_by: "Edsger W. Dijkstra"
  year: 1956
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: IS_VARIANT_OF
    target: bfs
  - type: USED_IN
    target: adjacency-list
---

Dijkstra extends BFS to weighted graphs. Instead of a simple queue, it uses a **min-heap priority queue** ordered by cumulative distance from the source.

## Algorithm

1. Set distance to source = 0, all others = ∞
2. Push source into min-heap
3. Pop min-distance node, relax all outgoing edges
4. If `dist[neighbor] > dist[current] + edge_weight`, update and push to heap
5. Repeat until heap empty

## Why it fails with negative weights

If edges can be negative, a "short" path found early might not be globally shortest — a later negative edge could provide a shortcut. Use Bellman-Ford instead.

## In Neo4j GDS

```cypher
CALL gds.shortestPath.dijkstra.stream('myGraph', {
  sourceNode: id(source),
  targetNode: id(target),
  relationshipWeightProperty: 'distance'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs
```

See also: [[bfs]], [[a-star]], [[graph-theory]]
