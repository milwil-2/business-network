"""FastAPI app for the Obsidian + Neo4j knowledge-graph project.

This module is the Vercel Python entry point (`api/index.py`), so it exposes
a module-level ``app``. Routes are root-relative (no ``/api`` prefix).
"""

import secrets
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from vector.store import semantic_search as _semantic_search

from . import db, ingest, rag

app = FastAPI(title="B2B Trade Network API")

# Public, read-mostly API. No cookie/session auth (the ingest routes use an
# explicit X-API-Key header), so credentials are off — a wildcard origin with
# credentials enabled would be an insecure misconfiguration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Attach baseline security headers to every response. The HTML page sets
    its own (nonce-based) CSP in the index handler; everything else gets a
    locked-down default."""
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault(
        "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
    )
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'none'; frame-ancestors 'none'; base-uri 'none'",
    )
    return response


_TEMPLATE = Path(__file__).parent / "templates" / "index.html"


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    mode: Literal["auto", "hybrid", "graph-only", "cypher"] = "auto"


class IngestRequest(BaseModel):
    text: str = Field(..., min_length=1)


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
def search(q: str = Query(..., min_length=1, max_length=200)):
    return db.search_nodes(q)


@app.get("/semantic-search")
def semantic_search(
    q: str = Query(..., min_length=1, max_length=200),
    k: int = Query(6, ge=1, le=25),
):
    # The HF query encoder can fail (auth / rate limit / network); the store
    # raises a generic RuntimeError so we never leak the underlying error.
    try:
        return _semantic_search(q, k=k)
    except RuntimeError:
        return JSONResponse(
            status_code=502,
            content={"error": "semantic search is temporarily unavailable"},
        )


@app.post("/ask")
def ask(req: AskRequest):
    return rag.answer_question(req.question, mode=req.mode)


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
    nonce = secrets.token_urlsafe(16)
    html = _TEMPLATE.read_text(encoding="utf-8").replace("__CSP_NONCE__", nonce)
    csp = (
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "frame-ancestors 'none'; base-uri 'none'; object-src 'none'"
    )
    return HTMLResponse(html, headers={"Content-Security-Policy": csp})
