import sys
from pathlib import Path
from textwrap import dedent

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "sync"))

# Frontmatter content for the temp vault nodes. Each is keyed by the file name
# (placed under a `nodes/` directory so `scan_vault`'s rglob("nodes/**/*.md")
# matches them).
VALID_NODES = {
    "test-node.md": dedent(
        """\
        ---
        id: test-node
        label: Test Node
        node_type: Concept
        tags: [test, Concept]
        summary: "A test node."
        relationships:
          - type: RELATED_TO
            target: other-node
        ---
        Body with a [[wikilink]] reference and a link to [[other-node]].
        """
    ),
    "other-node.md": dedent(
        """\
        ---
        id: other-node
        label: Other Node
        node_type: Technology
        tags: [test, Technology]
        summary: "Another test node."
        ---
        A node with no explicit relationships but a [[test-node]] mention.
        """
    ),
    "third-node.md": dedent(
        """\
        ---
        id: third-node
        label: Third Node
        node_type: Algorithm
        summary: "A third node."
        relationships:
          - type: USED_IN
            target: test-node
        ---
        Plain body, no wikilinks here.
        """
    ),
}


def _write_vault(root: Path, files: dict[str, str]) -> Path:
    """Write the given {filename: content} mapping under root/nodes/ and return root."""
    nodes_dir = root / "nodes"
    nodes_dir.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (nodes_dir / name).write_text(content)
    return root


@pytest.fixture
def temp_vault(tmp_path: Path) -> Path:
    """Create a small vault with 3 valid node files; return the vault root."""
    return _write_vault(tmp_path, VALID_NODES)


@pytest.fixture
def temp_node_file(temp_vault: Path) -> Path:
    """Path to a single valid node file inside the temp vault."""
    return temp_vault / "nodes" / "test-node.md"
