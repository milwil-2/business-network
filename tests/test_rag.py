"""Hermetic tests for the hybrid retrieval helper in api.rag.

No network, no real Groq, no real vector index. We monkeypatch
``api.rag.semantic_search`` (the local reference imported at module top)
and the ``api.rag.db`` accessors.
"""

import json

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


# --- text-to-Cypher mode ---------------------------------------------------


def test_validate_cypher_accepts_safe_match():
    """A canonical read-only MATCH against the closed vocab is accepted."""
    ok, reason = rag.validate_cypher(
        "MATCH (c:Company)-[:SELLS_TO]->(b:Buyer) "
        "RETURN c.id AS id, c.label AS label LIMIT 10"
    )
    assert ok, reason
    assert reason == "ok"


def test_validate_cypher_accepts_optional_match():
    ok, _ = rag.validate_cypher(
        "OPTIONAL MATCH (c:Company) RETURN c.id AS id LIMIT 5"
    )
    assert ok


def test_validate_cypher_rejects_write_keywords():
    """Every write/admin keyword in the denylist must trigger a reject."""
    cases = [
        ("MATCH (c:Company) CREATE (m:Company {id:'x'}) RETURN c", "CREATE"),
        ("MATCH (c:Company) MERGE (m:Company {id:'x'}) RETURN c", "MERGE"),
        ("MATCH (c:Company) DELETE c RETURN c", "DELETE"),
        ("MATCH (c:Company) DETACH DELETE c", "DETACH"),
        ("MATCH (c:Company) SET c.flagged = true RETURN c", "SET"),
        ("MATCH (c:Company) REMOVE c:Vendor RETURN c", "REMOVE"),
        ("MATCH (c:Company) DROP INDEX foo RETURN c", "DROP"),
        ("MATCH (c:Company) CALL db.labels() YIELD label RETURN label", "CALL"),
        ("MATCH (c:Company) LOAD CSV FROM 'x' AS row RETURN c", "LOAD"),
    ]
    for cypher, expected_kw in cases:
        ok, reason = rag.validate_cypher(cypher)
        assert not ok, f"should have rejected {expected_kw}: {cypher!r}"
        assert expected_kw in reason


def test_validate_cypher_rejects_unknown_label():
    ok, reason = rag.validate_cypher("MATCH (c:NotARealLabel) RETURN c")
    assert not ok
    assert "NotARealLabel" in reason


def test_validate_cypher_rejects_unknown_rel_type():
    ok, reason = rag.validate_cypher(
        "MATCH (c:Company)-[:NOT_A_REL]->(b:Company) RETURN c"
    )
    assert not ok
    assert "NOT_A_REL" in reason


def test_validate_cypher_rejects_non_match_start():
    ok, reason = rag.validate_cypher("RETURN 1")
    assert not ok
    assert "MATCH" in reason


def test_validate_cypher_rejects_periodic_commit():
    ok, reason = rag.validate_cypher(
        "USING PERIODIC COMMIT 100 MATCH (c:Company) RETURN c"
    )
    assert not ok
    # Either the leading non-MATCH check or the periodic-commit check fires.
    assert ("PERIODIC COMMIT" in reason) or ("MATCH" in reason)


def test_validate_cypher_rejects_overlong_query():
    long_cypher = "MATCH (c:Company) RETURN c " + ("// pad\n" * 1000)
    # Comments are stripped before the length check, so build it differently.
    long_cypher = "MATCH (c:Company) RETURN c, " + ("c.label, " * 500) + "c.id"
    ok, reason = rag.validate_cypher(long_cypher)
    assert not ok
    assert "exceeds" in reason


def test_validate_cypher_strips_line_comments_before_check():
    """A leading ``// note`` comment is stripped, then the MATCH passes."""
    ok, _ = rag.validate_cypher(
        "// pick recent vendors\nMATCH (v:Vendor) RETURN v.id LIMIT 5"
    )
    assert ok


class _StubMessage:
    def __init__(self, content):
        self.content = content


class _StubChoice:
    def __init__(self, content):
        self.message = _StubMessage(content)


class _StubResponse:
    def __init__(self, content):
        self.choices = [_StubChoice(content)]


class _StubCompletions:
    """Two-shot stub: first call returns the Cypher plan, second the summary."""

    def __init__(self, payloads):
        self._payloads = list(payloads)
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _StubResponse(self._payloads.pop(0))


class _StubChat:
    def __init__(self, payloads):
        self.completions = _StubCompletions(payloads)


class _StubClient:
    def __init__(self, payloads):
        self.chat = _StubChat(payloads)


class _StubResult:
    def __init__(self, rows):
        self._rows = rows

    def __iter__(self):
        return iter(self._rows)


class _StubSession:
    """Mimics ``driver.session(default_access_mode="READ")``."""

    def __init__(self, rows, captured):
        self._rows = rows
        self._captured = captured

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def run(self, cypher, **params):
        self._captured["cypher"] = cypher
        self._captured["params"] = params
        return _StubResult(self._rows)


class _StubDriver:
    def __init__(self, rows, captured):
        self._rows = rows
        self._captured = captured

    def session(self, **kwargs):
        self._captured["session_kwargs"] = kwargs
        return _StubSession(self._rows, self._captured)


def test_cypher_mode_answer_end_to_end(monkeypatch):
    """End-to-end with Groq + Neo4j mocked: plan → execute → summarize."""
    cypher_query = (
        "MATCH (me:Company {id:'cobalt-freight'})-[:SELLS_TO]->(b:Company)"
        "<-[:SUPPLIES]-(v:Company) RETURN v.id AS id, v.label AS label LIMIT 5"
    )
    rows = [{"id": "trident-distribution", "label": "Trident Distribution"}]

    payloads = [
        json.dumps({"cypher": cypher_query}),
        json.dumps(
            {
                "answer": "Trident Distribution supplies the buyers Cobalt Freight sells to.",
                "cited_node_ids": ["trident-distribution"],
            }
        ),
    ]
    captured: dict = {}

    monkeypatch.setattr(rag, "Groq", lambda **_: _StubClient(payloads))
    monkeypatch.setattr(rag.db, "get_driver", lambda: _StubDriver(rows, captured))
    monkeypatch.setattr(
        rag.db,
        "get_neighbors",
        lambda node_id: [
            {
                "rel": "SUPPLIES",
                "target_id": "globex-trading",
                "target_label": "Globex Trading",
                "target_type": "Company",
            }
        ],
    )

    result = rag.answer_question(
        "Which vendors supply the buyers Cobalt Freight sells to?", mode="cypher"
    )

    assert result["mode"] == "cypher"
    assert result["cypher"] == cypher_query
    assert "trident-distribution" in result["cited_node_ids"]
    assert "Trident" in result["answer"]
    # Read-only session was requested.
    assert captured["session_kwargs"]["default_access_mode"] == "READ"
    # Subgraph for the cited id was enriched via get_neighbors.
    assert "trident-distribution" in result["subgraph"]


def test_cypher_mode_answer_rejects_unsafe_plan(monkeypatch):
    """Validator catches an LLM plan with a write keyword; we fail closed."""
    bad_plan = {
        "cypher": "MATCH (c:Company) CREATE (m:Company {id:'x'}) RETURN c"
    }
    monkeypatch.setattr(
        rag, "Groq", lambda **_: _StubClient([json.dumps(bad_plan)])
    )

    def _explode(*a, **kw):
        raise AssertionError("Neo4j must not be called when validation fails")

    monkeypatch.setattr(rag.db, "get_driver", _explode)

    result = rag.answer_question("hand me the keys", mode="cypher")
    assert result["mode"] == "cypher"
    assert result["cited_node_ids"] == []
    assert "CREATE" in result["error"]
    assert result["cypher"] == bad_plan["cypher"]
