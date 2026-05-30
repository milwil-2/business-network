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
            # 1-hop: Acme sells to Globex
            {
                "src_id": "acme-foods", "src_label": "Acme Foods", "src_type": "Company",
                "rel": "SELLS_TO",
                "dst_id": "globex-trading", "dst_label": "Globex Trading", "dst_type": "Company",
            },
            # 2-hop: Initech also supplies Globex — the vendor-recommendation pattern.
            {
                "src_id": "initech", "src_label": "Initech", "src_type": "Company",
                "rel": "SUPPLIES",
                "dst_id": "globex-trading", "dst_label": "Globex Trading", "dst_type": "Company",
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


def test_system_instruction_has_traversal_guardrails():
    """The prompt must keep its traversal-grounding clauses (issue #12).

    These exact phrases stop the LLM from naming topically-related companies
    as 'vendors' for questions like 'which vendors supply the buyers Cobalt
    Freight already sells to' — the LLM must walk the explicit
    `(a) -[:REL]-> (b)` chains shown in context or say no such pattern
    exists. If a future refactor drops these, the live /ask answers regress.
    """
    instr = rag.SYSTEM_INSTRUCTION

    # JSON shape contract is still required (validators depend on it).
    assert '"answer"' in instr and '"cited_node_ids"' in instr

    # Trust-signal guidance is preserved.
    for signal in ("trust_score", "credit_rating", "fico", "status"):
        assert signal in instr

    # Edge format the model should expect (matches `_retrieve_context`).
    assert "(<src_id>) -[:<REL>]-> (<dst_id>)" in instr

    # Direction-of-edge guidance distinguishes SELLS_TO vs SUPPLIES.
    assert "SELLS_TO" in instr and "SUPPLIES" in instr

    # Traversal-grounding clauses from the issue.
    assert "(a) -[:REL]-> (b)" in instr
    assert "Do not invent" in instr
    # Honest-refusal clause when the asked pattern is absent.
    assert "not present in the shown edges" in instr


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
