# Knowledge Graph — Obsidian + Neo4j + FastAPI

A context-knowledge-graph of software engineering concepts, algorithms, technologies, and architecture patterns. Obsidian for human-friendly editing and visualization; Neo4j for real graph DB queries; a FastAPI layer for HTTP queries, an in-browser graph viz, and GraphRAG question answering.

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

Note: the public deployment talks to Aura, not your local DB.

### Secrets

Secrets live only in `.env` (gitignored) locally, and in the Vercel and Aura dashboards in the cloud. They are never committed.

---

## Project layout

```
vault/    Obsidian notes — one .md file per graph node (concepts, technologies, algorithms, patterns)
sync/     Python tooling — parse vault, idempotent MERGE into Neo4j, LLM node extraction, live watcher
api/      FastAPI app — HTTP queries, browser graph viz, GraphRAG (api/index.py exposes `app`)
vector/   Chroma vector store (store.py = access + semantic_search; build_index.py = CLI to embed the vault)
cypher/   schema_constraints.cypher (run once), demo_queries.cypher, seed_verify.cypher
tests/    pytest suite
```

---

## Adding new nodes

1. Create a `.md` file in the appropriate `vault/nodes/` subfolder.
2. Follow the frontmatter schema (see any existing node for reference). Required fields: `id`, `label`, `node_type`, `summary`.
3. Run `uv run sync/obsidian_to_neo4j.py` to push to Neo4j.
