"""Hermetic tests for vector.store (HF query encoder + Neo4j vector index).

No network, no real HF API, no real Neo4j. We monkeypatch ``httpx.post``
to fake the HF Inference API response, and patch ``api.db.get_driver`` to
return a fake driver whose session yields the records we hand it.
"""

from unittest import mock

import pytest

import vector.store as store

EMBED_DIM = 384


# --- embed_query -------------------------------------------------------

def test_embed_query_posts_to_hf_with_bearer_token(monkeypatch):
    """embed_query hits the right URL with the bearer token from env and
    returns the embedding payload as a list of floats."""
    monkeypatch.setenv("HF_API_TOKEN", "test-token-xyz")
    vec = [0.01] * EMBED_DIM

    fake_response = mock.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = vec

    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        return fake_response

    monkeypatch.setattr(store.httpx, "post", fake_post)

    result = store.embed_query("hello world")

    assert result == vec
    assert captured["url"] == store.HF_EMBED_URL
    assert captured["headers"]["Authorization"] == "Bearer test-token-xyz"
    assert captured["json"] == {"inputs": "hello world"}
    # Timeout is set; exact value is an implementation detail.
    assert captured["timeout"] is not None


def test_embed_query_accepts_nested_response(monkeypatch):
    """HF can return [[float, ...]]; embed_query normalizes it."""
    monkeypatch.setenv("HF_API_TOKEN", "tok")
    vec = [0.5] * EMBED_DIM
    fake_response = mock.Mock(status_code=200)
    fake_response.json.return_value = [vec]
    monkeypatch.setattr(
        store.httpx,
        "post",
        lambda *a, **kw: fake_response,
    )
    assert store.embed_query("q") == vec


def test_embed_query_auth_error_raises_generic_runtime_error(monkeypatch):
    """A 401 must surface as a generic 'embedding service unavailable'
    RuntimeError — the underlying status / body must not leak."""
    monkeypatch.setenv("HF_API_TOKEN", "bad")
    fake_response = mock.Mock(status_code=401)
    fake_response.json.return_value = {"error": "invalid credentials"}
    monkeypatch.setattr(
        store.httpx,
        "post",
        lambda *a, **kw: fake_response,
    )
    with pytest.raises(RuntimeError) as excinfo:
        store.embed_query("q")
    assert str(excinfo.value) == "embedding service unavailable"


def test_embed_query_rate_limit_raises_generic_runtime_error(monkeypatch):
    monkeypatch.setenv("HF_API_TOKEN", "tok")
    fake_response = mock.Mock(status_code=429)
    fake_response.json.return_value = {"error": "rate limited"}
    monkeypatch.setattr(
        store.httpx,
        "post",
        lambda *a, **kw: fake_response,
    )
    with pytest.raises(RuntimeError, match="embedding service unavailable"):
        store.embed_query("q")


def test_embed_query_timeout_raises_generic_runtime_error(monkeypatch):
    monkeypatch.setenv("HF_API_TOKEN", "tok")

    def boom(*a, **kw):
        raise store.httpx.ConnectTimeout("slow")

    monkeypatch.setattr(store.httpx, "post", boom)
    with pytest.raises(RuntimeError, match="embedding service unavailable"):
        store.embed_query("q")


# --- semantic_search ---------------------------------------------------

def _fake_record(id_, label, type_, score):
    """Minimal stand-in for a neo4j.Record: supports r[key] indexing."""
    data = {"id": id_, "label": label, "type": type_, "score": score}
    return mock.MagicMock(__getitem__=lambda self, k: data[k])


def test_semantic_search_chains_embed_and_query(monkeypatch):
    """semantic_search embeds the query, runs the parameterized vector
    query against Neo4j, and returns results best-first."""
    vec = [0.1] * EMBED_DIM
    monkeypatch.setattr(store, "embed_query", lambda text: vec)

    records = [
        _fake_record("acme", "Acme Foods", "Company", 0.92),
        _fake_record("globex", "Globex", "Company", 0.81),
        _fake_record("initech", "Initech", "Company", 0.55),
    ]
    session = mock.MagicMock()
    session.run.return_value = iter(records)

    driver = mock.MagicMock()
    driver.session.return_value.__enter__.return_value = session
    driver.session.return_value.__exit__.return_value = False

    monkeypatch.setattr(store, "get_driver", lambda: driver)

    out = store.semantic_search("food distributor", k=3)

    # Shape: list of dicts with the documented keys.
    assert out == [
        {"id": "acme", "label": "Acme Foods", "type": "Company", "score": 0.92},
        {"id": "globex", "label": "Globex", "type": "Company", "score": 0.81},
        {"id": "initech", "label": "Initech", "type": "Company", "score": 0.55},
    ]
    # Scores are returned non-increasing (Neo4j's vector index orders that way).
    scores = [r["score"] for r in out]
    assert scores == sorted(scores, reverse=True)

    # The query was parameterized — vector and k are passed as params, not
    # interpolated into the Cypher text.
    assert session.run.call_count == 1
    query_text, kwargs = session.run.call_args[0][0], session.run.call_args[1]
    assert "db.index.vector.queryNodes" in query_text
    assert "$index" in query_text and "$k" in query_text and "$vec" in query_text
    assert kwargs["k"] == 3
    assert kwargs["vec"] == vec
    assert kwargs["index"] == store.VECTOR_INDEX_NAME


def test_semantic_search_propagates_embedding_failure(monkeypatch):
    """If embed_query raises, semantic_search propagates the same
    RuntimeError so callers can degrade gracefully."""
    def boom(text):
        raise RuntimeError("embedding service unavailable")

    monkeypatch.setattr(store, "embed_query", boom)
    with pytest.raises(RuntimeError, match="embedding service unavailable"):
        store.semantic_search("q", k=3)
