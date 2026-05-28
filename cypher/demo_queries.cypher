// ═══════════════════════════════════════════════════════════════════
// INTERVIEW DEMO QUERIES — Knowledge Graph
// Run in Neo4j Browser at localhost:7474
// For Q7: switch to "Graph" tab to see the visual graph
// ═══════════════════════════════════════════════════════════════════


// ─── Q1: Basic node lookup ───────────────────────────────────────
// "Show me everything about Neo4j."
// Talking point: nodes store properties, just like rows — but the
// relationships are first-class citizens, not foreign keys.

MATCH (t:Technology {id: 'neo4j'})
RETURN t;


// ─── Q2: One-hop traversal ───────────────────────────────────────
// "What does Neo4j directly relate to, and how?"
// Talking point: relationship traversal vs JOIN — no index lookup
// needed, the edge IS the pointer.

MATCH (t:Technology {id: 'neo4j'})-[r]->(neighbor)
RETURN t.label           AS source,
       type(r)           AS relationship,
       neighbor.label    AS target,
       labels(neighbor)  AS target_type
ORDER BY target_type;


// ─── Q3: Variable-depth traversal ────────────────────────────────
// "What is graph-theory connected to, up to 3 hops away?"
// Talking point: [*1..3] syntax — O(hops), not O(rows). Try this
// in a relational DB without a recursive CTE.

MATCH path = (c:Concept {id: 'graph-theory'})-[*1..3]->(connected)
RETURN DISTINCT connected.label    AS node,
               labels(connected)   AS type,
               length(path)        AS hops
ORDER BY hops, type;


// ─── Q4: Shortest path ───────────────────────────────────────────
// "What's the shortest connection between BFS and Neo4j?"
// Talking point: shortestPath() is a built-in graph primitive.
// SQL equivalent: recursive CTE + row-number window — multiple pages.

MATCH
  (start:Algorithm {id: 'bfs'}),
  (end:Technology  {id: 'neo4j'}),
  path = shortestPath((start)-[*..6]-(end))
RETURN [n IN nodes(path)         | n.label]  AS path_labels,
       [r IN relationships(path) | type(r)]  AS rel_types,
       length(path)                          AS hops;


// ─── Q5: Pattern matching ────────────────────────────────────────
// "Find algorithms and technologies that share a common concept."
// Talking point: declarative pattern matching — the shape of the
// query mirrors the shape of the data you're looking for.

MATCH (algo:Algorithm)-[:IMPLEMENTS]->(concept:Concept)<-[:IMPLEMENTS]-(tech:Technology)
RETURN algo.label     AS algorithm,
       concept.label  AS shared_concept,
       tech.label     AS technology
ORDER BY concept.label;


// ─── Q6: Aggregation + degree centrality ─────────────────────────
// "Which concepts are most central — implemented by the most nodes?"
// Talking point: degree centrality; leads naturally into PageRank
// as a recursive, graph-native improvement.

MATCH (n)-[:IMPLEMENTS]->(concept)
RETURN concept.label         AS concept,
       count(n)               AS degree,
       collect(n.label)       AS implemented_by
ORDER BY degree DESC
LIMIT 10;


// ─── Q7: Subgraph extraction (VISUAL DEMO) ───────────────────────
// "Show the full algorithm ecosystem."
// Talking point: subgraph queries are natural — no UNION, no temp
// tables. SWITCH TO GRAPH TAB IN NEO4J BROWSER for the visual.

MATCH (algo:Algorithm)-[r]->(related)
WHERE labels(related)[0] IN ['Concept', 'Pattern']
RETURN algo, r, related;


// ─── Q8: allShortestPaths with path predicate ────────────────────
// "All shortest paths from Dijkstra to event-sourcing, skipping
// any Technology nodes along the way."
// Talking point: NONE() path predicate — shows Cypher expressiveness
// for constrained traversal that would require multiple CTEs in SQL.

MATCH
  (start:Algorithm {id: 'dijkstra'}),
  (end:Pattern     {id: 'event-sourcing'}),
  path = shortestPath((start)-[*..8]-(end))
WHERE NONE(n IN nodes(path) WHERE n:Technology)
RETURN [n IN nodes(path) | n.label]  AS path,
       length(path)                  AS length
ORDER BY length
LIMIT 5;
