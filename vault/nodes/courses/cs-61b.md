---
id: cs-61b
label: "CS 61B: Data Structures"
node_type: Course
tags: [eecs, data-structures, Course]
properties:
  number: "CS 61B"
  department: "EECS"
  units: 4
summary: "A course on the design and analysis of fundamental data structures and the software engineering practices for building them in Java."
relationships:
  - type: PREREQUISITE_OF
    target: cs-61c
  - type: PREREQUISITE_OF
    target: cs-170
  - type: PREREQUISITE_OF
    target: cs-186
  - type: PREREQUISITE_OF
    target: cs-162
  - type: PREREQUISITE_OF
    target: cs-164
  - type: PREREQUISITE_OF
    target: cs-188
  - type: COVERS
    target: tree
  - type: COVERS
    target: bfs
  - type: COVERS
    target: dfs
  - type: COVERS
    target: adjacency-list
  - type: COVERS
    target: hash-table
  - type: COVERS
    target: dijkstra
  - type: COVERS
    target: big-o-notation
---

CS 61B moves from learning to program to engineering efficient, maintainable software. Taught in Java, it covers the canonical data structures — lists, trees, heaps, hash tables, and graphs — and the algorithms that operate on them.

Students implement balanced search [[tree]] structures, [[hash-table]] maps, and graph representations like the [[adjacency-list]], then traverse them with [[bfs]] and [[dfs]] and find shortest paths with [[dijkstra]]. Asymptotic analysis with [[big-o-notation]] is used throughout to justify design choices.

The course is a major hub in the curriculum: it builds on [[cs-61a]] and is a prerequisite for a wide range of upper-division courses including [[cs-61c]], [[cs-170]], [[cs-186]], [[cs-162]], [[cs-164]], and [[cs-188]].
