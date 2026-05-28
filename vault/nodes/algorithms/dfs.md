---
id: dfs
label: DFS (Depth-First Search)
node_type: Algorithm
tags: [graph-traversal, algorithms, Algorithm]
summary: "Graph traversal that explores as far as possible along each branch before backtracking. Uses a stack (or recursion). O(V+E) time. Used for cycle detection, topological sort, connected components."
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: IS_VARIANT_OF
    target: bfs
  - type: RELATED_TO
    target: topological-sort
---

DFS uses a **stack** (or call stack via recursion). Explores fully down one path before backtracking.

## Properties

- **Does not guarantee shortest path** — goes deep, not wide
- **Cycle detection** — back edges (visiting an already-in-stack node) indicate a cycle
- **Topological sort** — DFS-based: post-order DFS on a DAG gives reverse topo order
- **Connected components** — DFS from every unvisited node, count starts = component count

## Implementation (Python, recursive)

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

## DFS vs BFS

| | DFS | BFS |
|---|---|---|
| Data structure | Stack / recursion | Queue |
| Shortest path | ❌ (unweighted) | ✅ (unweighted) |
| Memory | O(depth) | O(width) |
| Good for | Cycle detection, topo sort | Shortest path, level order |

See also: [[bfs]], [[topological-sort]], [[graph-theory]]
