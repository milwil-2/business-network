"""Hermetic tests for the hybrid retrieval helper in api.rag.

No network, no real Groq, no real vector index. We monkeypatch
``vector.store.semantic_search`` (resolved at call time inside
``_retrieve_context``) and the ``api.rag.db`` accessors.
"""

import vector.store
from api import rag


def test_retrieve_context_hybrid(monkeypatch):
    """Vector seeds + neighbors produce a focused 'hybrid' context."""
    monkeypatch.setattr(
        vector.store,
        "semantic_search",
        lambda query, k=6: [
            {
                "id": "dijkstra",
                "label": "Dijkstra's Algorithm",
                "type": "Algorithm",
                "score": 0.9,
            }
        ],
    )
    monkeypatch.setattr(
        rag.db,
        "get_node",
        lambda node_id: {
            "id": "dijkstra",
            "label": "Dijkstra's Algorithm",
            "type": "Algorithm",
            "summary": "Single-source shortest path in weighted graphs.",
            "properties": {},
        },
    )
    monkeypatch.setattr(
        rag.db,
        "get_neighbors",
        lambda node_id: [
            {
                "rel": "USES",
                "target_id": "priority-queue",
                "target_label": "Priority Queue",
                "target_type": "DataStructure",
            }
        ],
    )

    context, mode = rag._retrieve_context("shortest path")

    assert mode == "hybrid"
    assert "Dijkstra" in context
    assert "Priority Queue" in context


def test_retrieve_context_fallback(monkeypatch):
    """An empty/unavailable index falls back to the full graph summaries."""

    def _raise(query, k=6):
        raise RuntimeError("vector index is empty")

    monkeypatch.setattr(vector.store, "semantic_search", _raise)
    monkeypatch.setattr(
        rag.db,
        "all_node_summaries",
        lambda: [
            {
                "id": "redis",
                "label": "Redis Cache",
                "type": "Technology",
                "summary": "In-memory key-value store.",
            }
        ],
    )

    context, mode = rag._retrieve_context("how do caches work")

    assert mode == "graph-only"
    assert "Redis Cache" in context
