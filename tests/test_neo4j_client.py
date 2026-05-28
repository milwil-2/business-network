import sys
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "sync"))
import parser  # noqa: E402


@pytest.fixture
def client():
    """A Neo4jClient with the GraphDatabase driver fully mocked (no real DB)."""
    import neo4j_client

    with mock.patch.object(neo4j_client, "GraphDatabase") as gdb:
        c = neo4j_client.Neo4jClient("bolt://localhost:7687", "neo4j", "pw")
        # Wire up a mock session usable as a context manager.
        session = mock.MagicMock()
        c._driver.session.return_value.__enter__.return_value = session
        yield c, session


def _make_node():
    return parser.ParsedNode(
        id="test-node",
        label="Test Node",
        node_type="Concept",
        tags=["test"],
        summary="A test node.",
        properties={"created": 2024, "skip_dict": {"nested": True}},
        relationships=[],
        implicit_links=[],
        source_path=Path("/tmp/test-node.md"),
        mtime=1.0,
    )


# --- constants ----------------------------------------------------------

def test_constants_match_parser():
    import neo4j_client

    assert neo4j_client.VALID_NODE_TYPES == parser.VALID_NODE_TYPES
    assert neo4j_client.VALID_REL_TYPES == parser.VALID_REL_TYPES


# --- write_node ---------------------------------------------------------

def test_write_node_invalid_type_asserts(client):
    c, _ = client
    node = _make_node()
    node.node_type = "Banana"
    with pytest.raises(AssertionError):
        c.write_node(node)


def test_write_node_builds_label_query(client):
    c, session = client
    node = _make_node()
    c.write_node(node)

    # execute_write was called once with a callable; invoke it against a fake tx
    # to capture the Cypher query and parameters that get built.
    assert session.execute_write.call_count == 1
    work = session.execute_write.call_args[0][0]
    tx = mock.MagicMock()
    work(tx)

    query = tx.run.call_args[0][0]
    kwargs = tx.run.call_args[1]
    assert "MERGE (n:Concept {id: $id})" in query
    assert kwargs["id"] == "test-node"
    # dict-valued properties are filtered out; scalars/lists kept.
    assert kwargs["props"]["created"] == 2024
    assert "skip_dict" not in kwargs["props"]
    assert kwargs["props"]["id"] == "test-node"


# --- write_relationship -------------------------------------------------

def test_write_relationship_invalid_type_asserts(client):
    c, _ = client
    with pytest.raises(AssertionError):
        c.write_relationship("a", "FROBNICATES", "b")


def test_write_relationship_builds_query(client):
    c, session = client
    # execute_write returns the result of the lambda; emulate .single() -> [1]
    session.execute_write.return_value = [1]
    out = c.write_relationship("src-id", "RELATED_TO", "tgt-id")
    assert out is True

    work = session.execute_write.call_args[0][0]
    tx = mock.MagicMock()
    tx.run.return_value.single.return_value = [1]
    work(tx)
    query = tx.run.call_args[0][0]
    kwargs = tx.run.call_args[1]
    assert ":RELATED_TO" in query
    assert kwargs["src"] == "src-id"
    assert kwargs["tgt"] == "tgt-id"
