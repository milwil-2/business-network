"""Hermetic tests for api.ingest.

No real Neo4j and no real Groq. The Neo4j driver is replaced with a fake whose
``.session()`` is a context manager recording every ``.run(query, **params)``
call; ``extract`` (which would hit Groq) is never invoked.
"""

import json

from api import ingest
from api.ingest import ExtractedNode


# --- fake Neo4j driver -----------------------------------------------------
class FakeSession:
    def __init__(self, run_log, results):
        self._run_log = run_log
        self._results = results

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def run(self, query, **params):
        self._run_log.append((query, params))
        # Return the next queued result for read queries, else an empty list.
        if self._results:
            return self._results.pop(0)
        return []


class FakeDriver:
    def __init__(self, run_log, results):
        self._run_log = run_log
        self._results = results

    def session(self):
        return FakeSession(self._run_log, self._results)


def _patch_driver(monkeypatch, results=None):
    run_log: list[tuple[str, dict]] = []
    driver = FakeDriver(run_log, list(results or []))
    monkeypatch.setattr(ingest.db, "get_driver", lambda: driver)
    return run_log


# --- gating ----------------------------------------------------------------
def test_is_enabled_and_check_key(monkeypatch):
    monkeypatch.delenv("INGEST_API_KEY", raising=False)
    assert ingest.is_enabled() is False
    # Disabled => no key is ever accepted.
    assert ingest.check_key("anything") is False

    monkeypatch.setenv("INGEST_API_KEY", "s3cr3t")
    assert ingest.is_enabled() is True
    assert ingest.check_key("wrong") is False
    assert ingest.check_key(None) is False
    assert ingest.check_key("s3cr3t") is True


# --- rate limiting ---------------------------------------------------------
def test_rate_ok_window(monkeypatch):
    # Isolate the in-memory bucket for this key.
    monkeypatch.setattr(ingest, "_calls", {})
    key = "rate-key"
    for _ in range(10):
        assert ingest.rate_ok(key) is True
    # 11th call within the window is rejected.
    assert ingest.rate_ok(key) is False


# --- staging ---------------------------------------------------------------
def test_stage_skips_invalid_node_and_filters_rels(monkeypatch):
    run_log = _patch_driver(monkeypatch)
    nodes = [
        ExtractedNode(
            id="acme-foods",
            label="Acme Foods",
            node_type="Company",
            tags=["food-service"],
            summary="A food-service distributor.",
            relationships=[
                {"type": "SELLS_TO", "target": "globex-trading"},
                {"type": "NOT_A_REAL_REL", "target": "nope"},
            ],
        ),
        ExtractedNode(
            id="bogus",
            label="Bogus",
            node_type="NotAType",
            relationships=[],
        ),
    ]

    preview = ingest.stage(nodes)

    # Only the valid node is staged.
    assert len(preview) == 1
    assert preview[0]["id"] == "acme-foods"
    assert preview[0]["staged_type"] == "Company"
    assert preview[0]["n_relationships"] == 1

    # Exactly one MERGE was issued (the bogus node was skipped).
    merges = [(q, p) for q, p in run_log if "MERGE (n:Staged" in q]
    assert len(merges) == 1
    _, params = merges[0]
    assert params["id"] == "acme-foods"

    # The invalid relationship was filtered out of the stored JSON.
    stored = json.loads(params["rels_json"])
    assert stored == [{"type": "SELLS_TO", "target": "globex-trading"}]


# --- approval --------------------------------------------------------------
def test_approve_promotes_and_deletes(monkeypatch):
    staged_record = {
        "id": "acme-foods",
        "label": "Acme Foods",
        "summary": "A food-service distributor.",
        "staged_type": "Company",
        "tags": ["food-service"],
        "rels": json.dumps([{"type": "SELLS_TO", "target": "globex-trading"}]),
    }
    # First .run() in approve() is the MATCH (n:Staged) read; feed it our record.
    run_log = _patch_driver(monkeypatch, results=[[staged_record]])

    result = ingest.approve()

    assert result == {"promoted": 1}

    queries = [q for q, _ in run_log]
    # MERGE issued with the validated label interpolated in.
    assert any("MERGE (m:Company {id:$id})" in q for q in queries)
    # Relationship MERGE with the validated rel type.
    assert any("MERGE (a)-[:SELLS_TO]->(b)" in q for q in queries)
    # Quarantine node detached and deleted after promotion.
    assert any("DETACH DELETE s" in q for q in queries)
