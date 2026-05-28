---
id: recursion
label: Recursion
node_type: Concept
tags: [programming, problem-solving, Concept]
summary: "A problem-solving technique where a function calls itself on smaller subproblems until reaching a base case."
relationships:
  - type: RELATED_TO
    target: tree
---

Recursion is a technique where a function solves a problem by calling itself on smaller instances of the same problem. Every recursive definition needs a **base case** that stops the recursion and a **recursive case** that reduces the problem toward that base case.

Recursion shines on naturally self-similar structures. Traversing a [[tree]] is the canonical example: to process a node, you process its children, which are themselves trees. The same idea powers divide-and-conquer algorithms like mergesort and quicksort.

Each recursive call adds a frame to the call stack, so deep recursion can overflow the stack. Many recursive algorithms can be rewritten iteratively, and **memoization** turns expensive overlapping recursive calls into an efficient bottom-up computation — the bridge to [[dynamic-programming]].
