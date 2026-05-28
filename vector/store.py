"""Chroma vector store for semantic search over knowledge-graph nodes.

Lazy module-level singletons keep importing this module cheap and crash-free:
the Chroma client, embedding model, and collection are only created on first use.

Contract:
    semantic_search(query, k=6) -> list[{"id", "label", "type", "score"}]
    (score = cosine similarity, higher = closer; best match first)
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = Path(__file__).parent / "chroma"
COLLECTION = "kg_nodes"

# Lazy singletons — created on first call to the getters below.
_client = None
_collection = None
_embedding_fn = None


def get_client() -> "chromadb.api.ClientAPI":
    """Return the persistent Chroma client, creating it on first use."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


def get_embedding_fn():
    """Return the local default embedding function (all-MiniLM-L6-v2, no API key)."""
    global _embedding_fn
    if _embedding_fn is None:
        _embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    return _embedding_fn


def get_collection():
    """Return the kg_nodes collection (cosine space), creating it on first use."""
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=COLLECTION,
            embedding_function=get_embedding_fn(),
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def semantic_search(query: str, k: int = 6) -> list[dict]:
    """Return the k nodes most semantically similar to ``query``.

    Each result is ``{"id": str, "label": str, "type": str, "score": float}``
    with ``score`` a cosine similarity in [0, 1] (higher = closer), best first.

    Raises RuntimeError if the index has not been built yet so callers can
    fall back to another search strategy.
    """
    col = get_collection()
    if col.count() == 0:
        raise RuntimeError(
            "vector index is empty — run: uv run vector/build_index.py"
        )

    res = col.query(query_texts=[query], n_results=k)

    ids = res["ids"][0]
    distances = res["distances"][0]
    metadatas = res["metadatas"][0]

    results: list[dict] = []
    for node_id, distance, meta in zip(ids, distances, metadatas):
        meta = meta or {}
        results.append(
            {
                "id": node_id,
                "label": meta.get("label", node_id),
                "type": meta.get("type", ""),
                # cosine space: distance = 1 - similarity
                "score": 1.0 - distance,
            }
        )
    return results
