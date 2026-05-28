---
id: topological-sort
label: Topological Sort
node_type: Algorithm
tags: [graph-algorithms, dag, Algorithm]
summary: "Produces a linear ordering of nodes in a DAG such that for every edge (u→v), u appears before v. Used for build dependency ordering, task scheduling, and compilation order."
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: RELATED_TO
    target: dag
  - type: IS_VARIANT_OF
    target: dfs
---

Topological sort only works on **DAGs** — if the graph has a cycle, no valid ordering exists (which is how you detect circular dependencies).

## Two approaches

**Kahn's algorithm (BFS-based):**
1. Compute in-degree of every node
2. Enqueue all nodes with in-degree 0
3. Dequeue a node, add to result, decrement in-degrees of neighbors
4. Enqueue any neighbor whose in-degree reaches 0
5. If result length < V, there's a cycle

**DFS-based:**
Post-order DFS, prepend each node to result when all its descendants are processed.

## Real uses

- **Build systems** (Make, Bazel): which files to compile first?
- **Package managers**: install dependencies before the package
- **Course prerequisites**: which courses to take in what order?
- **Airflow/Prefect DAGs**: which tasks run before which?

See also: [[dag]], [[dfs]], [[graph-theory]]
