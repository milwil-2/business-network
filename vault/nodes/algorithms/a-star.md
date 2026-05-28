---
id: a-star
label: A* Search
node_type: Algorithm
tags: [shortest-path, heuristic, algorithms, Algorithm]
summary: "Heuristic-guided shortest path algorithm. Extends Dijkstra with a heuristic function h(n) estimating cost to goal. Finds optimal path when heuristic is admissible (never overestimates). Used in game AI, navigation, and robotics."
relationships:
  - type: IMPLEMENTS
    target: graph-theory
  - type: IS_VARIANT_OF
    target: dijkstra
---

A* uses: `f(n) = g(n) + h(n)` where `g(n)` = actual cost from start, `h(n)` = heuristic estimate to goal.

## Why A* beats Dijkstra for spatial graphs

Dijkstra explores in all directions equally. A* uses a heuristic to prioritize nodes in the direction of the goal — dramatically fewer nodes explored.

## Admissibility requirement

The heuristic **must never overestimate** the true remaining cost (admissible). Common admissible heuristics:
- **Euclidean distance** for geometric graphs
- **Manhattan distance** for grid-based maps
- **0** collapses A* back to Dijkstra (admissible but useless)

## Common uses

- **Navigation / mapping** — Google Maps, game pathfinding
- **Robotics** — motion planning
- **NLP** — beam search is A* variant over sequence graphs

## Comparison

| | Dijkstra | A* |
|---|---|---|
| Heuristic | None (cost only) | Cost + heuristic estimate |
| Completeness | ✅ Always finds path | ✅ With admissible heuristic |
| Optimality | ✅ | ✅ With admissible heuristic |
| Performance | Explores more | Explores less (directed by h) |

See also: [[dijkstra]], [[bfs]], [[graph-theory]]
