"""Self-contained tests for the vector store.

These build a tiny temporary Chroma collection in tmp_path so they never depend
on the production vector/chroma index. The embedding model is initialized inside
a try/except; if it can't be created (e.g. offline CI), the tests are skipped
rather than hard-failing.
"""

import chromadb
import pytest
from chromadb.utils import embedding_functions

# Try to construct the embedding function once at import time. If it fails
# (no network to download the onnx model, etc.) skip the whole module.
try:
    _EF = embedding_functions.DefaultEmbeddingFunction()
    # Force the model to actually load so we skip on download failures too.
    _EF(["warmup text"])
    _EF_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    _EF = None
    _EF_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _EF_AVAILABLE,
    reason="DefaultEmbeddingFunction unavailable (offline / model download failed)",
)

SEED = {
    "dijkstra": "Dijkstra. Single-source shortest path in weighted graphs.",
    "bfs": "Breadth-first search. Breadth-first graph traversal of unweighted graphs.",
    "redis": "Redis. In-memory cache and key-value data structure store.",
    "cqrs": "CQRS. Command query responsibility segregation architectural pattern.",
}


@pytest.fixture
def collection(tmp_path):
    client = chromadb.PersistentClient(path=str(tmp_path))
    col = client.get_or_create_collection(
        name="test_nodes",
        embedding_function=_EF,
        metadata={"hnsw:space": "cosine"},
    )
    col.upsert(
        ids=list(SEED.keys()),
        documents=list(SEED.values()),
        metadatas=[{"label": k, "type": "Test"} for k in SEED],
    )
    return col


def test_semantic_search_ranks_relevant_node_first(collection):
    res = collection.query(
        query_texts=["weighted shortest path algorithm"], n_results=2
    )
    ids = res["ids"][0]
    assert "dijkstra" in ids
    assert "redis" not in ids[:1]  # dijkstra should outrank the cache store


def test_cosine_score_in_range(collection):
    res = collection.query(query_texts=["graph traversal"], n_results=4)
    distances = res["distances"][0]
    scores = [1.0 - d for d in distances]
    assert all(-1.0001 <= s <= 1.0001 for s in scores)
    # Results come back best-first, so scores are non-increasing.
    assert scores == sorted(scores, reverse=True)
