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

---

## Vector search & scaling

**The hybrid-retrieval story (GraphRAG).** Classic RAG retrieves context purely by vector similarity. Here retrieval is **vector seeds + graph expansion**: a Chroma vector store finds the top-k semantically relevant nodes, then the graph expands their neighbors, and the LLM answers while **citing the grounding node ids**. So I blend semantic recall with structural context — the vector layer finds *what's relevant*, the graph supplies *what's connected*. Embeddings are computed by a local model (`all-MiniLM-L6-v2`), so there's no embeddings API dependency, and if the index is unavailable `/ask` degrades to graph-only retrieval.

**How vector DBs scale.** Brute-force nearest-neighbor is O(N·d) per query — fine for thousands of vectors, hopeless at billions. Real vector DBs use **ANN indexes**:
- **HNSW** — a multi-layer navigable graph; ~sub-linear query time, RAM-resident. Great recall/latency, but the whole index lives in memory.
- **IVF / PQ** — clustering (search only the nearest cells) plus product quantization (compress each vector to a few bytes); enables disk-backed, billion-scale indexes at some recall cost.

The real cost at scale is **memory**, not query latency: a 768-dim float32 vector ≈ 3 KB, so 1B vectors ≈ 3 TB of RAM for a flat/HNSW index. The core tradeoff is **recall ↔ latency ↔ memory** — you tune index params (and reach for quantization) to balance them.

**Many corpuses.** Don't dump everything into one giant index. Partition with **namespaces / collections / shards** so per-query N stays small. A single mixed index with a selective metadata filter can be inefficient: ANN traverses neighbors that the filter then discards, wasting the graph walk.

**Tie-back.** At 51 nodes this is trivially a flat scan that returns instantly — the point is demonstrating the *architecture*, not the performance. At real scale I'd use **Neo4j's native vector index** (unified graph + vector in one store) or a managed vector DB, and reach for quantization only once the index stops fitting in RAM.

---

## Security & safe ingestion

**The story:** "I added an on-request `/ingest` endpoint that runs LLM extraction and writes to the graph — and the moment you expose a write path that takes arbitrary text and calls a paid LLM, you've created a target. So I sat down and designed for abuse before shipping it." This is the *"I thought about the threat model"* talking point.

**The threat model — what an attacker (or an accident) can do to an open ingest endpoint:**
- **DB pollution** — junk or adversarial nodes written straight into the curated graph.
- **Cost / quota abuse** — hammering the endpoint to burn the Groq quota (a denial-of-wallet attack).
- **Prompt injection / open LLM proxy** — using my endpoint as a free, anonymous LLM relay, or steering the extractor with injected instructions.
- **Cypher injection via labels** — LLM-extracted `node_type` / relationship types interpolated into Cypher could inject query fragments (you can't always parameterize a label).
- **Stored XSS** — untrusted ingested text later rendered in the browser viz.

**The mitigations I actually implemented (each maps to a threat above):**
- **Gated + safe-by-default** — both endpoints are off unless `INGEST_API_KEY` is set; unset → `404`. It's **left unset in the cloud**, so the public Vercel deployment has *no write path to prod at all*. Ingestion is a local, opt-in tool.
- **`:Staged` quarantine + human approve** — `/ingest` writes only to a `:Staged` label; a separate `/ingest/approve` call promotes (MERGE) into the real graph. Nothing untrusted reaches the curated graph without a human in the loop. (Mitigates DB pollution.)
- **API key with constant-time compare** — authenticated, and compared in constant time so the check can't be timing-attacked.
- **Payload cap + rate limit** — bodies capped at 8 KB (`413`), in-memory limit of 10 ingests / 60 s per key (`429`). (Mitigates cost/quota abuse and open-proxy use.)
- **Closed-vocab validation before Cypher** — extracted `node_type` and relationship types are validated against the closed vocabulary *before* they're interpolated as labels/rel-types into any Cypher. (Mitigates Cypher injection.)
- **Viz XSS fix** — the browser viz renders ids/labels via DOM `textContent` + escaping instead of `innerHTML`, so untrusted ingested content can't execute. (Mitigates stored XSS.)

**Why it lands in an interview:** it shows defense in depth (gating → quarantine → validation → output encoding), the instinct to make the dangerous mode opt-in and off-in-cloud, and that I reason about *both* security (injection, XSS) *and* operational abuse (cost, rate). Designed for abuse, not just for the happy path.
