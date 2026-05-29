# B2B Trade Network — Obsidian + Neo4j + FastAPI

A graph of a **B2B trade & trust network** (modeled on platforms like Nuvo): verified company profiles connected by trade relationships, with creditworthiness/trust signals, the people who run them, the products and industries they trade in, and their licenses. Obsidian for human-friendly editing and visualization; Neo4j for real graph DB queries; a FastAPI layer for HTTP queries, an in-browser graph viz, and GraphRAG question answering.

**Node types:** `Company`, `Person`, `Industry`, `Product`, `License`, `CreditBureau`.
**Relationship types:** `SELLS_TO`, `SUPPLIES`, `OPERATES_IN`, `TRADES_PRODUCT`, `HOLDS_LICENSE`, `RATED_BY`, `PRINCIPAL_OF`, `GAVE_REFERENCE_FOR`, `SUBSIDIARY_OF`, `PARTNERS_WITH`, `COMPETES_WITH`, `INVITED`.

Each `Company` also carries first-class **trade-role labels** (`Buyer`/`Seller`/`Vendor`/`Customer`) as *secondary* Neo4j labels derived from its trade edges during sync — so `MATCH (b:Buyer)` works directly while each business remains a single node (the same node just holds extra labels alongside its primary `:Company` label).

The dataset (~130 nodes) is **mock / generated** data (real company data will be added in the future), produced by a seeded script — `uv run scripts/generate_b2b_vault.py` — which writes the Obsidian vault and embeds deliberate, query-able patterns: trust clusters, a fraud ring (companies sharing principals), supply chains, and trust hubs.

## Architecture

```
Obsidian vault (markdown notes)
        ↓
sync/ (Python: parse + idempotent MERGE)
        ↓
Neo4j (graph DB)
        ↓
api/ (FastAPI: queries + GraphRAG)
        ↓
browser viz
```

Two LLM touchpoints, both via **Groq** (`groq`, Llama 3.3 70B):

- **`sync/extract.py`** — turns raw notes into typed graph nodes.
- **`api/rag.py`** — GraphRAG question answering, using Neo4j neighborhood expansion as LLM context.

## Trust score

Each `Company` carries a **calculated** `trust_score` (0–100) — a weighted composite of the company's own data points and its network signals, computed in `scripts/generate_b2b_vault.py`:

| Component | Weight | Derived from |
|---|---|---|
| Creditworthiness | 30 | FICO blended with credit-rating tier (AAA…D) |
| Trade references | 20 | count of inbound `GAVE_REFERENCE_FOR` edges |
| Verification status | 20 | verified / pending / flagged |
| License validity | 12 | active vs. lapsed / revoked licenses held |
| Longevity | 8 | years in business |
| Principal integrity | 10 | drops to 0 if an owner is also a principal of a **flagged** company (fraud signal) |

The component sub-scores are stored as node properties (`trust_credit`, `trust_references`, …), so the browser viz shows a per-company breakdown when you click a node. Flagged fraud-ring companies score very low and densely-referenced hubs score high — emergent from the data, not hand-set.

---

## Local run

The project uses [`uv`](https://docs.astral.sh/uv/).

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Then fill in the values:

- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` — your Neo4j connection.
- `GROQ_API_KEY` — get a free key at https://console.groq.com/keys (no credit card; powers `extract.py` and the GraphRAG `/ask`).

For a local Neo4j Desktop DBMS, run `cypher/schema_constraints.cypher` once in the Neo4j Browser after creating the database.

### 3. Sync the vault → Neo4j

```bash
uv run sync/obsidian_to_neo4j.py --full
```

### 4. Run the API + viz locally

```bash
uv run uvicorn api.index:app --reload --port 8000
```

Then open http://localhost:8000 for the interactive graph visualization.

API routes: `GET /` (HTML graph viz), `GET /health`, `GET /graph`, `GET /nodes/{id}`, `GET /nodes/{id}/neighbors`, `GET /path`, `GET /search`, `POST /ask` (GraphRAG).

### 5. Extract nodes from notes (optional)

```bash
uv run sync/extract.py --inbox
```

### 6. Run tests

```bash
uv run pytest
```

---

## Vector search & hybrid GraphRAG

On top of the graph, the project adds a semantic-search layer backed by a **Chroma vector store** (HNSW index, RAM-resident) built from the vault notes.

### Build the index

```bash
uv run vector/build_index.py
```

This embeds every vault note and persists the store to `vector/chroma/` (gitignored). Embeddings are produced by a **local model** — `all-MiniLM-L6-v2` via onnxruntime, bundled with `chromadb` — so there is **no embeddings API key and no external service** to configure. (This matters because the Groq API has no embeddings endpoint.)

### `GET /semantic-search?q=...&k=6`

Returns the top-k nodes by semantic similarity as `[{id, label, type, score}]`.

### Hybrid `POST /ask` (GraphRAG)

`POST /ask` is now a hybrid GraphRAG flow: vector search finds the top-k relevant seed nodes → the graph expands their neighbors → the LLM (Groq Llama 3.3) answers and cites the node ids it used. If the vector index or `chromadb` is unavailable, `/ask` **falls back to graph-only** retrieval (passing all node summaries as context), so behavior degrades gracefully.

### Local-first / deployment caveat

`chromadb` is intentionally **not** in `requirements.txt`. As a result, the **Vercel deployment uses the graph-only fallback** for `/ask`, and `/semantic-search` returns `503` there — the vector layer runs locally. A cloud-ready path (not yet built) would use a managed vector DB (Qdrant/Pinecone) or **Neo4j's native vector index** alongside a hosted embedding API.

---

## Ingesting data (gated)

Beyond the vault-driven sync, the API exposes a gated, **safe-by-default** HTTP ingestion path that runs LLM extraction and stages the result for human review before it ever touches the curated graph.

### Endpoints

- **`POST /ingest`** (header `X-API-Key`) — accepts `{ "text": "..." }`, runs Groq (Llama 3.3) extraction, and writes the resulting nodes into a quarantine **`:Staged`** label in Neo4j. It never writes directly into the curated graph.
- **`POST /ingest/approve`** (same `X-API-Key`) — promotes the `:Staged` nodes into the real graph (idempotent `MERGE`) and removes the staged copies.

So the flow is always **extract → `:Staged` quarantine → human approve → curated graph**.

### Gating / safe-by-default

Both endpoints are **disabled unless the `INGEST_API_KEY` env var is set** — when it is unset they return `404` (the routes effectively don't exist). The key is intentionally **left unset on the Vercel deployment**, so there is **no public write path to prod**. To use ingestion, set `INGEST_API_KEY` locally. Authentication compares the supplied key with a **constant-time comparison**.

### Abuse protections

- **Payload cap** — request bodies over **8 KB** are rejected with `413`.
- **Rate limit** — an in-memory limit of **10 ingests / 60 s per key** returns `429` when exceeded.
- **Closed-vocab validation** — extracted `node_type` and relationship types are validated against the closed vocabulary **before any Cypher write**, so labels and relationship types can't inject Cypher.

Related hardening shipped alongside: the browser viz now renders node ids/labels safely (DOM `textContent` + escaping instead of `innerHTML`), so untrusted ingested content can't cause stored XSS.

---

## Deploy to the cloud (Neo4j Aura + Vercel)

### 1. Neo4j Aura (free)

1. Sign up at https://neo4j.com/cloud/aura-free/ and create a free instance.
2. Save the generated password and the `neo4j+s://...` connection URI shown on creation (the password is only displayed once).
3. In the Aura console query editor, run the contents of `cypher/schema_constraints.cypher`.
4. Load the data by pointing your local `.env` at the Aura URI/credentials and running:
   ```bash
   uv run sync/obsidian_to_neo4j.py --full
   ```

### 2. Vercel

The repo includes `vercel.json` and `requirements.txt`, so Vercel's Python runtime serves the whole FastAPI app through `api/index.py`.

1. Deploy with the Vercel CLI (`vercel`) or via the Vercel git integration.
2. In the Vercel project **Settings → Environment Variables**, set:
   - `NEO4J_URI` — your Aura `neo4j+s://...` URI
   - `NEO4J_USER` — usually `neo4j`
   - `NEO4J_PASSWORD` — your Aura password
   - `GROQ_API_KEY` — your Groq key
   - `INGEST_API_KEY` (optional) — enables the gated `/ingest` endpoints; **leave unset in the cloud** so there is no public write path to prod (see "Ingesting data (gated)").

Note: the public deployment talks to Aura, not your local DB.

### Secrets

Secrets live only in `.env` (gitignored) locally, and in the Vercel and Aura dashboards in the cloud. They are never committed.

---

## Project layout

```
vault/    Obsidian notes — one .md file per graph node (companies, people, industries, products, licenses, bureaus)
sync/     Python tooling — parse vault, idempotent MERGE into Neo4j, LLM node extraction, live watcher
api/      FastAPI app — HTTP queries, browser graph viz, GraphRAG (api/index.py exposes `app`)
vector/   Chroma vector store (store.py = access + semantic_search; build_index.py = CLI to embed the vault)
cypher/   schema_constraints.cypher (run once), demo_queries.cypher, seed_verify.cypher
scripts/  generate_b2b_vault.py — seeded generator that (re)builds the vault/nodes dataset
tests/    pytest suite
```

---

## Adding / regenerating nodes

The dataset is **owned by the generator**: `uv run scripts/generate_b2b_vault.py` wipes and rebuilds `vault/nodes/` from a fixed seed. To change the network, edit the generator (company pools, patterns, counts) and re-run it.

To hand-add a one-off node instead:

1. Create a `.md` file in the appropriate `vault/nodes/` subfolder (`companies/`, `people/`, `industries/`, `products/`, `licenses/`, `bureaus/`).
2. Follow the frontmatter schema (see any existing node for reference). Required fields: `id`, `label`, `node_type`, `summary`. Companies also carry trust signals in `properties` (`trust_score`, `credit_rating`, `fico`, `status`, …).
3. Run `uv run sync/obsidian_to_neo4j.py` to push to Neo4j. (Note: a later generator re-run will overwrite hand edits.)
