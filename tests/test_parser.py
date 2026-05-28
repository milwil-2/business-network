import sys
from pathlib import Path
from textwrap import dedent

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "sync"))
import parser  # noqa: E402


# --- slug ---------------------------------------------------------------

def test_slug_basic():
    assert parser.slug("Hello World") == "hello-world"


def test_slug_strips_and_lowercases():
    assert parser.slug(" Mixed Case ") == "mixed-case"


# --- parse_node_file: happy path ----------------------------------------

def test_parse_valid_node(temp_node_file):
    node = parser.parse_node_file(temp_node_file)
    assert isinstance(node, parser.ParsedNode)
    assert node.id == "test-node"
    assert node.label == "Test Node"
    assert node.node_type == "Concept"
    assert node.tags == ["test", "Concept"]
    assert node.summary == "A test node."
    assert node.source_path == temp_node_file
    assert isinstance(node.mtime, float)


def test_parse_relationships_are_dicts(temp_node_file):
    node = parser.parse_node_file(temp_node_file)
    assert node.relationships == [{"type": "RELATED_TO", "target": "other-node"}]
    for r in node.relationships:
        assert set(r) >= {"type", "target"}


def test_implicit_links_exclude_explicit_targets(temp_node_file):
    # Body links to [[wikilink]] and [[other-node]]; other-node is an explicit
    # relationship target, so only "wikilink" should remain implicit.
    node = parser.parse_node_file(temp_node_file)
    assert node.implicit_links == ["wikilink"]


def test_implicit_links_default_when_no_relationships(temp_vault):
    # other-node.md has no relationships and mentions [[test-node]].
    node = parser.parse_node_file(temp_vault / "nodes" / "other-node.md")
    assert node.implicit_links == ["test-node"]


def test_label_defaults_to_id(tmp_path):
    f = tmp_path / "n.md"
    f.write_text(dedent(
        """\
        ---
        id: minimal-node
        node_type: Concept
        ---
        Body.
        """
    ))
    node = parser.parse_node_file(f)
    assert node.label == "minimal-node"


# --- parse_node_file: error cases ---------------------------------------

def test_invalid_node_type_raises(tmp_path):
    f = tmp_path / "bad.md"
    f.write_text(dedent(
        """\
        ---
        id: bad-node
        node_type: Banana
        ---
        Body.
        """
    ))
    with pytest.raises(ValueError):
        parser.parse_node_file(f)


def test_unknown_relationship_type_raises(tmp_path):
    f = tmp_path / "badrel.md"
    f.write_text(dedent(
        """\
        ---
        id: badrel-node
        node_type: Concept
        relationships:
          - type: FROBNICATES
            target: somewhere
        ---
        Body.
        """
    ))
    with pytest.raises(ValueError):
        parser.parse_node_file(f)


# --- scan_vault ---------------------------------------------------------

def test_scan_vault_all_valid(temp_vault):
    nodes, errors = parser.scan_vault(temp_vault)
    assert len(nodes) == 3
    assert errors == []
    ids = {n.id for n in nodes}
    assert ids == {"test-node", "other-node", "third-node"}


def test_scan_vault_collects_errors(temp_vault):
    bad = temp_vault / "nodes" / "broken.md"
    bad.write_text(dedent(
        """\
        ---
        id: broken-node
        node_type: Banana
        ---
        Body.
        """
    ))
    nodes, errors = parser.scan_vault(temp_vault)
    assert len(nodes) == 3  # the 3 valid ones still parse
    assert len(errors) == 1
    assert errors[0][0] == "broken.md"


# --- module constants ---------------------------------------------------

def test_valid_node_types():
    assert parser.VALID_NODE_TYPES == {"Concept", "Technology", "Algorithm", "Pattern", "Course"}


def test_valid_rel_types_members():
    expected = {
        "IMPLEMENTS", "USES_QUERY_LANGUAGE", "EXTENDS", "IS_VARIANT_OF",
        "ENABLES", "OPTIMIZED_FOR", "USED_IN", "RELATED_TO", "STORES_AS",
        "COMPETES_WITH", "INSPIRED_BY", "PREREQUISITE_OF", "COVERS",
    }
    assert parser.VALID_REL_TYPES == expected
