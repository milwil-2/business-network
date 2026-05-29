"""Cloud-native semantic search backed by Neo4j's native vector index.

Two pieces:

1. ``embed_query`` — calls the HuggingFace Inference API endpoint for
   ``sentence-transformers/all-MiniLM-L6-v2`` to turn a query string into a
   384-dim cosine vector at request time. Reads ``HF_API_TOKEN`` from env.
   On any auth / rate-limit / network failure it raises a generic
   ``RuntimeError("embedding service unavailable")`` so the underlying
   error never leaks to the API response.

2. ``semantic_search`` — embeds the query, then asks Neo4j's native vector
   index (``node_embedding`` on the ``:Embedded`` secondary label) for the
   nearest k nodes. Scores come back already in [0, 1] (cosine similarity,
   higher = closer), best match first.

Node embeddings themselves are pre-computed locally and pushed to Neo4j
once via ``vector/build_index.py``; only the query embedding hits HF at
runtime.
"""

import os

import httpx

from api.db import PRIMARY_TYPES, get_driver

HF_EMBED_URL = (
    "https://api-inference.huggingface.co/pipeline/feature-extraction/"
    "sentence-transformers/all-MiniLM-L6-v2"
)
VECTOR_INDEX_NAME = "node_embedding"
_EMBED_TIMEOUT_SECONDS = 5.0


def embed_query(text: str) -> list[float]:
    """Encode ``text`` as a 384-dim cosine vector via HF Inference API.

    Raises ``RuntimeError("embedding service unavailable")`` for any auth,
    rate-limit, timeout, or network failure — callers translate that into a
    user-facing 502 / graceful degradation without leaking the underlying
    cause.
    """
    token = os.environ.get("HF_API_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.post(
            HF_EMBED_URL,
            headers=headers,
            json={"inputs": text},
            timeout=_EMBED_TIMEOUT_SECONDS,
        )
    except (httpx.TimeoutException, httpx.HTTPError):
        raise RuntimeError("embedding service unavailable")

    if response.status_code in (401, 403, 429):
        raise RuntimeError("embedding service unavailable")
    if response.status_code >= 400:
        raise RuntimeError("embedding service unavailable")

    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError("embedding service unavailable")

    # The HF feature-extraction pipeline can return either a flat list
    # ([float, ...]) or a nested list ([[float, ...]]) depending on the
    # input shape. Normalize both to a flat list of floats.
    if isinstance(payload, list) and payload and isinstance(payload[0], list):
        payload = payload[0]
    if not isinstance(payload, list) or not all(
        isinstance(x, (int, float)) for x in payload
    ):
        raise RuntimeError("embedding service unavailable")
    return [float(x) for x in payload]


def semantic_search(query: str, k: int = 6) -> list[dict]:
    """Return the k nodes most semantically similar to ``query``.

    Each result is ``{"id": str, "label": str, "type": str, "score": float}``
    with ``score`` in [0, 1] (cosine similarity from Neo4j's native vector
    index), best match first.

    Raises ``RuntimeError("embedding service unavailable")`` when the HF
    Inference API call fails, so callers can degrade gracefully.
    """
    vec = embed_query(query)
    with get_driver().session() as session:
        records = session.run(
            """
            CALL db.index.vector.queryNodes($index, $k, $vec)
            YIELD node, score
            RETURN node.id AS id,
                   node.label AS label,
                   [l IN labels(node) WHERE l IN $primary][0] AS type,
                   score
            """,
            index=VECTOR_INDEX_NAME,
            k=k,
            vec=vec,
            primary=PRIMARY_TYPES,
        )
        return [
            {
                "id": r["id"],
                "label": r["label"],
                "type": r["type"],
                "score": r["score"],
            }
            for r in records
        ]
