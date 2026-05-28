---
id: dynamic-programming
label: Dynamic Programming
node_type: Concept
tags: [algorithms, optimization, Concept]
summary: "An algorithmic technique that solves problems by breaking them into overlapping subproblems and caching subproblem results to avoid recomputation."
relationships:
  - type: RELATED_TO
    target: recursion
  - type: RELATED_TO
    target: big-o-notation
---

Dynamic programming (DP) solves problems that exhibit **optimal substructure** (an optimal solution is built from optimal solutions to subproblems) and **overlapping subproblems** (the same subproblems recur many times). Instead of recomputing them, DP stores each subproblem's answer in a table.

There are two styles. *Top-down* memoization starts from [[recursion]] and caches results as they are computed. *Bottom-up* tabulation fills a table in dependency order, often eliminating the call stack entirely. Both transform exponential brute-force searches into polynomial-time solutions.

Classic examples include Fibonacci, longest common subsequence, edit distance, the knapsack problem, and shortest-path algorithms like Bellman-Ford. The efficiency gains are best understood through [[big-o-notation]]: DP commonly turns O(2^n) into O(n^2) or O(n*W).
