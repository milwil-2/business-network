---
id: dag
label: DAG (Directed Acyclic Graph)
node_type: Concept
tags: [graph-theory, data-structures, Concept]
summary: "A directed graph with no cycles. Used to model dependency chains, build systems, task scheduling, and dataflow pipelines."
relationships:
  - type: EXTENDS
    target: graph-theory
  - type: RELATED_TO
    target: topological-sort
---

A DAG is a directed graph where following edges never leads back to a starting node. No cycles = topological ordering is always possible.

## Real-world uses

- **Build systems** — Makefile, Bazel, Buck dependency graphs
- **Git history** — commits form a DAG (merges create diamonds)
- **Task schedulers** — Airflow, Prefect DAGs
- **Neural networks** — computation graphs in PyTorch/TensorFlow
- **Package managers** — npm/pip dependency resolution

## Key property

A DAG always has at least one **topological ordering** — a linear sequence where every node appears before all nodes it points to. This is used in build systems to determine compilation order.

See also: [[topological-sort]], [[graph-theory]]
