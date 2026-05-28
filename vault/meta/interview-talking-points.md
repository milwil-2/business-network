# Graph DB Interview Talking Points

## The 30-second pitch

> "I built a knowledge graph of software-engineering concepts end to end. Obsidian is the human editing layer — each note is a typed node with YAML frontmatter and typed relationships. A Python sync script parses the vault and idempotently MERGEs it into Neo4j. On top of that I built a FastAPI service that exposes graph queries, an in-browser graph visualization, and a GraphRAG endpoint — you ask a question, it finds the relevant nodes, expands their neighborhood, and feeds that subgraph to an LLM for a cited answer. The interesting part is using Cypher for traversals that would be painful recursive CTEs in SQL — variable-depth hops, shortest path, subgraph extraction."

---

## The full system (architecture story)

```
Obsidian vault  →  sync/ (parse + idempotent MERGE)  →  Neo4j  →  api/ (FastAPI)  →  browser viz
                         ↑ extract.py (LLM: notes→nodes)              ↓ rag.py (GraphRAG Q&A)
```

Narrate it as five layers, each a deliberate choice:
1. **Obsidian** — human-friendly editing + a free graph view; notes are just markdown + frontmatter, so the data is portable and diff-able in git.
2. **`sync/`** — parses frontmatter into typed nodes, validates against a closed node-type and relationship-type vocabulary, and pushes to Neo4j. **Two things worth calling out:** (a) every write is an idempotent `MERGE` on `id`, so re-running never duplicates; (b) the sync is *incremental* — it tracks file mtimes in a small state file and only pushes changed notes. That's the kind of detail that signals you've actually run this in anger, not just for a demo.
3. **Neo4j** — native graph storage; traversal follows physical pointers (O(1)/hop) vs. JOINs (O(log n)).
4. **`api/` (FastAPI)** — a clean HTTP surface over Cypher: node lookup, neighbors, shortest path, search, full-graph export for the viz, and `POST /ask`.
5. **GraphRAG (`api/rag.py`)** — the current-and-impressive bit: retrieval is a *graph* operation (match nodes → 2-hop expand) rather than vector similarity, and the answer cites the node ids it used, so it's grounded and auditable.

**If asked "what was hard / what would you do next":** the LLM extraction and GraphRAG both depend on an external model API, so I made them degrade gracefully (a quota error returns a clear message, the rest of the API keeps serving). Next I'd add embeddings so retrieval can blend semantic similarity with graph structure.

---

## Core concepts to know cold

### What is a property graph?

4 components: **nodes** (entities with labels + properties), **relationships** (typed, directed, with properties), **labels** (node type tags), **properties** (key-value pairs on nodes or edges).

```
(:Algorithm {id: 'bfs', label: 'BFS'})-[:IMPLEMENTS]->(:Concept {id: 'graph-theory'})
```

### Why graph DBs instead of relational?

**The key insight:** In a relational DB, relationships are foreign keys resolved via JOINs — O(log n) per JOIN. In a graph DB, relationships are physical pointers — O(1) per hop.

For 3-hop traversal: Postgres does 3 JOINs × O(log n) each. Neo4j follows 3 pointers. At scale and depth, this is orders of magnitude faster.

**When NOT to use a graph DB:** Tabular reporting, aggregate analytics, simple CRUD with flat schemas — stick with Postgres.

### Property graph vs RDF

| | Property Graph (Neo4j) | RDF (SPARQL) |
|---|---|---|
| Model | Nodes/edges with properties | Triples (subject, predicate, object) |
| Query | Cypher / GQL | SPARQL |
| Use case | App development, operational | Semantic web, linked data |

---

## Cypher patterns to know

```cypher
-- Pattern matching: nodes and edges as ASCII art
MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a, b

-- MERGE: create if not exists, match if exists (idempotent)
MERGE (n:Person {id: $id}) SET n += $props

-- Variable-depth traversal
MATCH (a)-[:KNOWS*1..3]->(b) RETURN DISTINCT b

-- Shortest path
MATCH path = shortestPath((a)-[*]-(b)) RETURN path

-- Aggregation
MATCH (n)-[:IMPLEMENTS]->(c) RETURN c.label, count(n) ORDER BY count(n) DESC
```

---

## Graph algorithm vocabulary

| Algorithm | What it does | Graph DB relevance |
|---|---|---|
| **BFS** | Shortest path (unweighted), level-order | Cypher `[*1..n]` uses BFS; `shortestPath()` |
| **DFS** | Cycle detection, topo sort, connectivity | Used in constraint checking |
| **Dijkstra** | Shortest path (weighted) | Neo4j GDS `gds.shortestPath.dijkstra` |
| **A\*** | Heuristic shortest path | Navigation, game AI |
| **PageRank** | Node importance from link structure | Neo4j GDS, recommendation |
| **Topological sort** | DAG ordering | Dependency resolution |

---

## The demo story (what to show)

1. **Obsidian graph view** — "This is the knowledge graph I built. Each color is a node type: blue=Concept, orange=Technology, yellow=Algorithm, green=Pattern. The links are typed relationships."

2. **Show a node file** — "Each node is a markdown file with YAML frontmatter. The properties become Neo4j node properties, and the `relationships:` block becomes typed edges."

3. **Neo4j Browser — Q7 visual** — "This is the same graph in Neo4j. I query the algorithm ecosystem — run it, switch to Graph tab — you get an interactive subgraph you can explore."

4. **Q4 shortest path** — "Find the shortest path between BFS and Neo4j. One Cypher call vs a recursive CTE in SQL."

5. **Q6 centrality** — "Which concepts are most central? This is degree centrality — the manual precursor to PageRank."

6. **Talk about the sync** — "I wrote a Python script that parses the Obsidian vault, extracts frontmatter and wikilinks, and MERGEs everything into Neo4j idempotently. Incremental sync tracks mtimes so it only pushes what changed."

---

## Likely interview questions and answers

**Q: When would you choose Neo4j over Postgres?**
> When your queries traverse relationships of unknown depth, or when the relationship structure IS the query. Social graphs, knowledge graphs, dependency analysis, fraud detection rings. If you're doing 4+ hop traversals or pathfinding, Neo4j's native graph storage wins on performance. For flat CRUD or aggregate reporting, Postgres is still the right tool.

**Q: How does Neo4j store data physically?**
> Native graph storage — each node record has a direct pointer to its first relationship. Relationships form a doubly-linked list per node. Traversal follows physical pointers: O(1) per hop, regardless of total graph size. This is different from a relational DB where JOINs require index lookups proportional to table size.

**Q: What's ACID compliance like in Neo4j?**
> Fully ACID. Transactions are explicit — you can batch multiple writes and commit atomically. If anything fails mid-transaction, nothing is committed. The write-ahead log (WAL) ensures durability across restarts.

**Q: What's Cypher? How does it compare to SQL?**
> Declarative graph query language. You describe the pattern you're looking for using ASCII-art notation: `(node)-[:RELATIONSHIP]->(other)`. SQL describes table joins; Cypher describes graph patterns. MATCH is like SELECT+FROM+JOIN. openCypher is an open standard also supported by Amazon Neptune, Memgraph, and others.

**Q: What are limitations of graph databases?**
> Weaker aggregation and reporting than relational DBs. Less mature tooling ecosystem. OLAP-style queries (full scans, complex aggregations) are slower. Not ideal for tabular/flat data. No SQL-style window functions. Horizontal sharding is harder than in distributed SQL systems.
