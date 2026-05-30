"""Hermetic tests for the hybrid retrieval helper in api.rag.

No network, no real Groq, no real vector index. We monkeypatch
``api.rag.semantic_search`` (the local reference imported at module top)
and the ``api.rag.db`` accessors.
"""

from api import rag


def test_retrieve_context_hybrid(monkeypatch):
    """Vector seeds + neighbors produce a focused 'hybrid' context."""
    monkeypatch.setattr(
        rag,
        "semantic_search",
        lambda query, k=6: [
            {
                "id": "acme-foods",
                "label": "Acme Foods",
                "type": "Company",
                "score": 0.9,
            }
        ],
    )
    monkeypatch.setattr(
        rag.db,
        "get_node",
        lambda node_id: {
            "id": "acme-foods",
            "label": "Acme Foods",
            "type": "Company",
            "summary": "A verified food-service distributor.",
            "properties": {},
        },
    )
    monkeypatch.setattr(
        rag.db,
        "get_neighborhood",
        lambda node_id, hops=2: [
            # 1-hop: Acme sells to Globex (tier 1, incident to seed).
            {
                "src_id": "acme-foods", "src_label": "Acme Foods", "src_type": "Company",
                "rel": "SELLS_TO",
                "dst_id": "globex-trading", "dst_label": "Globex Trading", "dst_type": "Company",
                "tier": 1,
            },
            # 2-hop: Initech also supplies Globex — the vendor-recommendation pattern.
            {
                "src_id": "initech", "src_label": "Initech", "src_type": "Company",
                "rel": "SUPPLIES",
                "dst_id": "globex-trading", "dst_label": "Globex Trading", "dst_type": "Company",
                "tier": 2,
            },
        ],
    )

    context, mode = rag._retrieve_context("food distributor")

    assert mode == "hybrid"
    assert "Acme Foods" in context
    # 2-hop expansion surfaces the indirect vendor through Globex.
    assert "globex-trading" in context
    assert "initech" in context
    assert "SELLS_TO" in context and "SUPPLIES" in context


def test_retrieve_context_fallback(monkeypatch):
    """An empty/unavailable index falls back to the full graph summaries."""

    def _raise(query, k=6):
        raise RuntimeError("vector index is empty")

    monkeypatch.setattr(rag, "semantic_search", _raise)
    monkeypatch.setattr(
        rag.db,
        "all_node_summaries",
        lambda: [
            {
                "id": "globex-trading",
                "label": "Globex Trading",
                "type": "Company",
                "summary": "A wholesale trading company.",
            }
        ],
    )

    context, mode = rag._retrieve_context("which companies trade wholesale")

    assert mode == "graph-only"
    assert "Globex Trading" in context


def test_retrieve_context_forced_graph_only_skips_vector(monkeypatch):
    """mode='graph-only' must skip semantic_search entirely (no embed call)."""
    called = {"n": 0}

    def _should_not_run(*a, **kw):
        called["n"] += 1
        raise AssertionError("semantic_search must not be called in graph-only mode")

    monkeypatch.setattr(rag, "semantic_search", _should_not_run)
    monkeypatch.setattr(
        rag.db,
        "all_node_summaries",
        lambda: [
            {
                "id": "globex-trading",
                "label": "Globex Trading",
                "type": "Company",
                "summary": "A wholesale trading company.",
            }
        ],
    )

    context, mode = rag._retrieve_context("anything", mode="graph-only")

    assert mode == "graph-only"
    assert "Globex Trading" in context
    assert called["n"] == 0


def test_retrieve_context_cap_keeps_tier2_closing_chain(monkeypatch):
    """The per-seed cap iterates pre-sorted edges, so a tier-2 closing-chain
    edge that follows many tier-1 edges still lands in the prompt (issue #11).

    Mimics the live cobalt-freight shape: lots of 1-hop edges, then the
    recommendation edge as a tier-2 closing chain, then a flood of tier-3
    edges that must NOT push the tier-2 edge out.
    """
    monkeypatch.setattr(
        rag,
        "semantic_search",
        lambda query, k=6: [
            {"id": "cobalt-freight", "label": "Cobalt Freight", "type": "Company", "score": 0.9}
        ],
    )
    monkeypatch.setattr(
        rag.db,
        "get_node",
        lambda node_id: {
            "id": "cobalt-freight",
            "label": "Cobalt Freight",
            "type": "Company",
            "summary": "A freight hub.",
            "properties": {},
        },
    )

    # 29 tier-1 noise edges, the critical tier-2 trident edge, then 200
    # tier-3 edges. Caller hands them in tier-sorted order, as get_neighborhood
    # now does in production.
    tier1 = [
        {
            "src_id": "cobalt-freight", "src_label": "Cobalt Freight", "src_type": "Company",
            "rel": "SELLS_TO",
            "dst_id": f"buyer-{i}", "dst_label": f"Buyer {i}", "dst_type": "Company",
            "tier": 1,
        }
        for i in range(29)
    ]
    critical = {
        "src_id": "trident-distribution", "src_label": "Trident Distribution", "src_type": "Company",
        "rel": "SUPPLIES",
        "dst_id": "trident-logistics", "dst_label": "Trident Logistics", "dst_type": "Company",
        "tier": 2,
    }
    tier3 = [
        {
            "src_id": f"noise-{i}", "src_label": f"Noise {i}", "src_type": "Company",
            "rel": "OPERATES_IN",
            "dst_id": "logistics", "dst_label": "Logistics", "dst_type": "Industry",
            "tier": 3,
        }
        for i in range(200)
    ]
    edges = tier1 + [critical] + tier3
    monkeypatch.setattr(rag.db, "get_neighborhood", lambda node_id, hops=2: edges)

    context, mode = rag._retrieve_context("which vendors supply cobalt freight's buyers")

    assert mode == "hybrid"
    # The critical closing-chain edge survives the per-seed cap even though
    # 200 tier-3 noise edges follow it in the source list.
    assert "trident-distribution" in context
    assert "trident-logistics" in context
