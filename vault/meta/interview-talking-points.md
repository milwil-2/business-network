# Graph DB Interview Talking Points

## The 30-second pitch

> "I built a **B2B trade & trust network** as a graph, end to end — think of the data model behind a platform like Nuvo, where verified company profiles connect to do business. Obsidian is the human editing layer: each note is a typed node (Company, Person, Industry, Product, License, CreditBureau) with YAML frontmatter and typed trade relationships. A Python sync parses the vault and idempotently MERGEs it into Neo4j. On top I built a FastAPI service with graph queries, an in-browser visualization, and a GraphRAG endpoint — you ask a question, it finds the relevant nodes, expands their neighborhood, and feeds that subgraph to an LLM for a cited answer. The fun part is that the *interesting business questions are graph questions*: trust paths between companies, vendor recommendations via 2-hop traversal, and fraud rings via shared principals — all painful recursive CTEs in SQL, one Cypher pattern here."

---

## The full system (architecture story)

```
Obsidian vault  →  sync/ (parse + idempotent MERGE)  →  Neo4j  →  api/ (FastAPI)  →  browser viz
                         ↑ extract.py (LLM: notes→nodes)              ↓ rag.py (GraphRAG Q&A)
                                                                       ↘ vector/ (Chroma, hybrid retrieval)
```

Narrate it as five layers, each a deliberate choice:
1. **Obsidian** — human-friendly editing + a free graph view; notes are just markdown + frontmatter, so the data is portable and diff-able in git. The data is **generated** by a seeded script (`scripts/generate_b2b_vault.py`) so the whole ~130-node network is reproducible and embeds deliberate patterns (trust clusters, a fraud ring, supply chains).
2. **`sync/`** — parses frontmatter into typed nodes, validates against a closed node-type and relationship-type vocabulary, and pushes to Neo4j. **Two things worth calling out:** (a) every write is an idempotent `MERGE` on `id`, so re-running never duplicates; (b) the sync is *incremental* — it tracks file mtimes in a small state file and only pushes changed notes.
3. **Neo4j** — native graph storage; traversal follows physical pointers (O(1)/hop) vs. JOINs (O(log n)).
4. **`api/` (FastAPI)** — a clean HTTP surface over Cypher: node lookup, neighbors, shortest path, search, full-graph export for the viz, and `POST /ask`.
5. **GraphRAG (`api/rag.py`)** — retrieval is hybrid: a vector store finds semantically relevant seed companies, the graph expands their neighborhood (trade partners, principals, credit signals), and the LLM answers while **citing the node ids it used**, so it's grounded and auditable.

**If asked "what was hard / what would you do next":** the LLM extraction and GraphRAG both depend on an external model API, so I made them degrade gracefully (a quota error returns a clear message, the rest of the API keeps serving). Next I'd push the vector layer into the cloud (Neo4j's native vector index) so semantic search works on the deployed app too.

---

## The domain model

| Node type | What it is |
|---|---|
| **Company** | A verified business profile — carries `trust_score`, `credit_rating`, `fico`, revenue, `status` (verified/pending/flagged). |
| **Person** | A principal/owner/officer. **Shared principals across companies are the fraud signal.** |
| **Industry** | Trade sector (alcohol & beverage, building materials, chemicals, food service, logistics). |
| **Product** | A traded commodity. |
| **License** | A regulatory license with a `status` (active/lapsed/revoked). |
| **CreditBureau** | A rating agency that companies are `RATED_BY`. |

Relationship vocabulary: `SELLS_TO`, `SUPPLIES`, `OPERATES_IN`, `TRADES_PRODUCT`, `HOLDS_LICENSE`, `RATED_BY`, `PRINCIPAL_OF`, `GAVE_REFERENCE_FOR`, `SUBSIDIARY_OF`, `PARTNERS_WITH`, `COMPETES_WITH`, `INVITED`.

Example node + edge:
```
(:Company {id:'acme-foods', trust_score:84})-[:SELLS_TO]->(:Company {id:'globex-trading'})
(:Person {id:'dana-whitfield'})-[:PRINCIPAL_OF]->(:Company {id:'acme-foods'})
```

---

## How the trust score is computed

Each company's `trust_score` (0–100) is a **calculated weighted composite**, not a label — a good answer to "how is the score derived?":

- **Creditworthiness (30)** — FICO blended with credit-rating tier.
- **Trade references (20)** — inbound `GAVE_REFERENCE_FOR` count (network trust).
- **Verification status (20)** — verified / pending / flagged.
- **License validity (12)** — active vs. lapsed/revoked licenses held.
- **Longevity (8)** — years in business.
- **Principal integrity (10)** — drops to 0 when an owner is shared with a *flagged* company (the fraud signal).

Component sub-scores are stored as `trust_*` node properties, so the viz shows a per-company breakdown on click. The talking point: trust blends a company's **own data points** (credit, licenses, age) with **graph/network signals** (who vouches for it, who runs it) — the network signals are exactly what a graph DB makes cheap to compute.

## The demo story (what to show)

1. **Browser viz** — "This is the trade network. Each color is a node type: blue=Company, amber=Person, green=Industry, purple=Product, red=License, cyan=CreditBureau. Edges are typed trade/trust relationships."

2. **Show a node file** — "Each company is a markdown file with YAML frontmatter. Trust signals (trust_score, fico, credit_rating, status) become Neo4j properties, and the `relationships:` block becomes typed edges like SELLS_TO and RATED_BY."

3. **Vendor recommendation (Q3, 2-hop)** — "Which vendors supply the buyers a company already sells to? That's the platform's core *network-effect* query — one declarative 2-hop pattern."

4. **Trust path (Q4, shortest path)** — "How is company A connected to company B across the network? `shortestPath()` in one call vs. a recursive CTE in SQL."

5. **Fraud ring (Q5)** — the headline: "Find people who are principals of more than one *flagged* company. Shared-principal detection is trivial in Cypher and painful in SQL — this is the classic 'graph DBs are for fraud detection' example, live."

6. **Trust hubs (Q6)** — "Which companies are most-referenced — the trust hubs? Degree centrality on GAVE_REFERENCE_FOR, the manual precursor to PageRank."

7. **Talk about the sync** — "A Python script parses the vault, validates against a closed vocabulary, and MERGEs into Neo4j idempotently. Incremental sync tracks mtimes so it only pushes what changed."

---

## Core concepts to know cold

### What is a property graph?

4 components: **nodes** (entities with labels + properties), **relationships** (typed, directed, with properties), **labels** (node type tags), **properties** (key-value pairs on nodes or edges).

```
(:Company {id: 'acme-foods', trust_score: 84})-[:SUPPLIES]->(:Company {id: 'globex-trading'})
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
MATCH (a:Company)-[:SELLS_TO]->(b:Company) RETURN a, b

-- MERGE: create if not exists, match if exists (idempotent)
MERGE (n:Company {id: $id}) SET n += $props

-- Variable-depth traversal (supply chain)
MATCH (a:Company)-[:SUPPLIES*1..3]->(b:Company) RETURN DISTINCT b

-- Shortest path (trust path)
MATCH path = shortestPath((a)-[*]-(b)) RETURN path

-- Aggregation (trust hubs / degree centrality)
MATCH (ref)-[:GAVE_REFERENCE_FOR]->(c) RETURN c.label, count(ref) ORDER BY count(ref) DESC
```

---

## Graph algorithm vocabulary

| Algorithm | What it does | Graph DB relevance |
|---|---|---|
| **BFS** | Shortest path (unweighted), level-order | Cypher `[*1..n]` uses BFS; `shortestPath()` |
| **DFS** | Cycle detection, connectivity | Detecting circular ownership / circular SELLS_TO |
| **Dijkstra** | Shortest path (weighted) | Neo4j GDS `gds.shortestPath.dijkstra` |
| **PageRank** | Node importance from link structure | Trust-hub ranking, recommendation |
| **Community detection** | Cluster nodes | Finding tightly-knit trade clusters / rings |

---

## Likely interview questions and answers

**Q: When would you choose Neo4j over Postgres?**
> When your queries traverse relationships of unknown depth, or when the relationship structure IS the query. **Fraud detection rings, B2B trade networks, supply-chain traversal, recommendation.** This project is a live example: "principals shared across flagged companies" or "vendors of my buyers" are one-line Cypher patterns and multi-CTE nightmares in SQL. For flat CRUD or aggregate reporting, Postgres is still the right tool.

**Q: How does Neo4j store data physically?**
> Native graph storage — each node record has a direct pointer to its first relationship. Relationships form a doubly-linked list per node. Traversal follows physical pointers: O(1) per hop, regardless of total graph size. Different from a relational DB where JOINs require index lookups proportional to table size.

**Q: What's ACID compliance like in Neo4j?**
> Fully ACID. Transactions are explicit — batch multiple writes and commit atomically. If anything fails mid-transaction, nothing is committed. The write-ahead log (WAL) ensures durability across restarts.

**Q: What's Cypher? How does it compare to SQL?**
> Declarative graph query language. You describe the pattern using ASCII-art notation: `(node)-[:RELATIONSHIP]->(other)`. SQL describes table joins; Cypher describes graph patterns. MATCH is like SELECT+FROM+JOIN. openCypher is an open standard also supported by Amazon Neptune, Memgraph, and others.

**Q: What are limitations of graph databases?**
> Weaker aggregation and reporting than relational DBs. Less mature tooling ecosystem. OLAP-style queries (full scans, complex aggregations) are slower. Not ideal for tabular/flat data. Horizontal sharding is harder than in distributed SQL systems.

---

## Vector search & scaling

**The hybrid-retrieval story (GraphRAG).** Classic RAG retrieves context purely by vector similarity. Here retrieval is **vector seeds + graph expansion**: a Chroma vector store finds the top-k semantically relevant companies, then the graph expands their neighbors (trade partners, principals, credit signals), and the LLM answers while **citing the grounding node ids**. So I blend semantic recall with structural context — the vector layer finds *what's relevant*, the graph supplies *what's connected*. Embeddings are computed by a local model (`all-MiniLM-L6-v2`), so there's no embeddings API dependency, and if the index is unavailable `/ask` degrades to graph-only retrieval.

**How vector DBs scale.** Brute-force nearest-neighbor is O(N·d) per query — fine for thousands of vectors, hopeless at billions. Real vector DBs use **ANN indexes**:
- **HNSW** — a multi-layer navigable graph; ~sub-linear query time, RAM-resident. Great recall/latency, but the whole index lives in memory.
- **IVF / PQ** — clustering (search only the nearest cells) plus product quantization (compress each vector to a few bytes); enables disk-backed, billion-scale indexes at some recall cost.

The real cost at scale is **memory**, not query latency: a 768-dim float32 vector ≈ 3 KB, so 1B vectors ≈ 3 TB of RAM for a flat/HNSW index. The core tradeoff is **recall ↔ latency ↔ memory**.

**Tie-back.** At ~130 nodes this is trivially a flat scan that returns instantly — the point is demonstrating the *architecture*, not the performance. At real scale I'd use **Neo4j's native vector index** (unified graph + vector in one store) or a managed vector DB, and reach for quantization only once the index stops fitting in RAM.

---

## Security & safe ingestion

**The story:** "I added an on-request `/ingest` endpoint that runs LLM extraction and writes to the graph — and the moment you expose a write path that takes arbitrary text and calls a paid LLM, you've created a target. So I designed for abuse before shipping it." This is the *"I thought about the threat model"* talking point.

**The threat model — what an attacker (or an accident) can do to an open ingest endpoint:**
- **DB pollution** — junk or adversarial company/person nodes written straight into the curated graph.
- **Cost / quota abuse** — hammering the endpoint to burn the Groq quota (a denial-of-wallet attack).
- **Prompt injection / open LLM proxy** — using my endpoint as a free, anonymous LLM relay, or steering the extractor with injected instructions.
- **Cypher injection via labels** — LLM-extracted `node_type` / relationship types interpolated into Cypher could inject query fragments (you can't always parameterize a label).
- **Stored XSS** — untrusted ingested text later rendered in the browser viz.

**The mitigations I actually implemented (each maps to a threat above):**
- **Gated + safe-by-default** — both endpoints are off unless `INGEST_API_KEY` is set; unset → `404`. **Left unset in the cloud**, so the public Vercel deployment has *no write path to prod at all*. Ingestion is a local, opt-in tool.
- **`:Staged` quarantine + human approve** — `/ingest` writes only to a `:Staged` label; a separate `/ingest/approve` call promotes (MERGE) into the real graph. Nothing untrusted reaches the curated graph without a human in the loop.
- **API key with constant-time compare** — authenticated, and compared in constant time so the check can't be timing-attacked.
- **Payload cap + rate limit** — bodies capped at 8 KB (`413`), in-memory limit of 10 ingests / 60 s per key (`429`).
- **Closed-vocab validation before Cypher** — extracted `node_type` and relationship types are validated against the closed vocabulary *before* they're interpolated as labels/rel-types into any Cypher.
- **Viz XSS fix** — the browser viz renders ids/labels via DOM `textContent` + escaping instead of `innerHTML`, so untrusted ingested content can't execute.

**Why it lands in an interview:** defense in depth (gating → quarantine → validation → output encoding), the instinct to make the dangerous mode opt-in and off-in-cloud, and reasoning about *both* security (injection, XSS) *and* operational abuse (cost, rate).
