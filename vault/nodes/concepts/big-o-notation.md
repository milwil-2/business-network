---
id: big-o-notation
label: Big-O Notation
node_type: Concept
tags: [complexity, analysis, Concept]
summary: "A mathematical notation describing the asymptotic upper bound on an algorithm's running time or space as input size grows."
relationships:
  - type: RELATED_TO
    target: graph-theory
---

Big-O notation describes how an algorithm's resource usage scales with input size *n*, ignoring constant factors and lower-order terms. Saying an algorithm is O(n log n) means its growth is bounded above by a constant multiple of n log n for large n.

Common classes, from fastest to slowest, are O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n), O(n^2) quadratic, and O(2^n) exponential. Big-O captures **worst-case** behavior; the related Big-Theta and Big-Omega describe tight and lower bounds.

This notation is the shared language for comparing algorithms independent of hardware. It explains why a binary search beats a linear scan, why graph algorithms on a sparse [[graph-theory]] representation matter, and why some problems are considered intractable.
