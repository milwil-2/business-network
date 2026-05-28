---
id: tree
label: Tree
node_type: Concept
tags: [data-structures, graph-theory, Concept]
summary: "A connected, acyclic undirected graph. Hierarchical structure with a root node, parent-child relationships, and no cycles. N nodes always have N-1 edges."
relationships:
  - type: EXTENDS
    target: graph-theory
  - type: IS_VARIANT_OF
    target: dag
  - type: RELATED_TO
    target: bfs
  - type: RELATED_TO
    target: dfs
---

A tree is a special case of a graph: connected (one component), undirected, acyclic. For N nodes, exactly N-1 edges.

## Common tree types

- **Binary tree** — each node has at most 2 children
- **BST** — binary tree with ordering invariant
- **B-tree / B+ tree** — used in database indexes (Postgres, MySQL)
- **Trie** — prefix tree for string lookups
- **Heap** — tree with priority queue semantics

## Relevance to graph databases

Many graph DB use cases start with a tree (org charts, file systems, category hierarchies) and then gain cross-links that make them a general graph. Neo4j handles both naturally.

See also: [[graph-theory]], [[bfs]], [[index]]
