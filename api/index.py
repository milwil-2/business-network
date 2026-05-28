"""FastAPI app for the Obsidian + Neo4j knowledge-graph project.

This module is the Vercel Python entry point (`api/index.py`), so it exposes
a module-level ``app``. Routes are root-relative (no ``/api`` prefix).
"""

from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from . import db, ingest, rag

app = FastAPI(title="Knowledge Graph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_TEMPLATE = Path(__file__).parent / "templates" / "index.html"


class AskRequest(BaseModel):
    question: str


class IngestRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return db.health()


@app.get("/nodes/{node_id}")
def get_node(node_id: str):
    node = db.get_node(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="node not found")
    return node


@app.get("/nodes/{node_id}/neighbors")
def get_neighbors(node_id: str):
    return db.get_neighbors(node_id)


@app.get("/graph")
def get_graph():
    return db.get_graph()


@app.get("/path")
def shortest_path(source: str, target: str):
    return db.shortest_path(source, target)


@app.get("/search")
def search(q: str):
    return db.search_nodes(q)


@app.get("/semantic-search")
def semantic_search(q: str, k: int = 6):
    # Lazy import so the app still loads where chromadb is absent (Vercel).
    try:
        from vector.store import semantic_search as _semantic_search

        return _semantic_search(q, k=k)
    except (ImportError, RuntimeError, Exception) as e:
        return JSONResponse(status_code=503, content={"error": str(e)})


@app.post("/ask")
def ask(req: AskRequest):
    return rag.answer_question(req.question)


def _guard_ingest(x_api_key: str | None) -> None:
    """Shared gate for the ingest routes: existence, auth, and rate limiting."""
    if not ingest.is_enabled():
        # Hide the endpoint's existence entirely when disabled.
        raise HTTPException(status_code=404, detail="not found")
    if not ingest.check_key(x_api_key):
        raise HTTPException(status_code=401, detail="invalid api key")


@app.post("/ingest")
def ingest_text(
    req: IngestRequest,
    x_api_key: str | None = Header(default=None),
):
    _guard_ingest(x_api_key)
    if len(req.text.encode()) > ingest.MAX_INGEST_BYTES:
        raise HTTPException(status_code=413, detail="payload too large")
    if not ingest.rate_ok(x_api_key):
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    try:
        nodes = ingest.extract(req.text)
        preview = ingest.stage(nodes)
        return {"staged": preview}
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/ingest/approve")
def ingest_approve(x_api_key: str | None = Header(default=None)):
    _guard_ingest(x_api_key)
    if not ingest.rate_ok(x_api_key):
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    return ingest.approve()


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(_TEMPLATE.read_text(encoding="utf-8"))
