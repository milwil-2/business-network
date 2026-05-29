#!/usr/bin/env python3
"""Embed every vault node locally and push the vectors to Neo4j Aura.

Local-only script: loads sentence-transformers (all-MiniLM-L6-v2, 384-dim,
cosine), embeds each ``vault/nodes/**/*.md`` note, then pushes them up to
Neo4j Aura in a single batched ``UNWIND`` write so the native vector index
(created in ``cypher/schema_constraints.cypher``) can serve queries.
``sentence-transformers`` is intentionally in the dev dependency group
(not ``requirements.txt``) so the Vercel bundle stays slim — runtime query
encoding hits the HuggingFace Inference API instead.

Run with:
    uv run --group dev vector/build_index.py
"""

import os
import sys
from pathlib import Path

import certifi
import frontmatter
import typer
from dotenv import load_dotenv
from neo4j import GraphDatabase
from rich.console import Console
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).parent.parent))

app = typer.Typer(help="Embed vault nodes locally and upsert into Neo4j Aura.")
console = Console()

VAULT = Path(__file__).parent.parent / "vault"
MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM = 384
BATCH_SIZE = 500  # future-proofing; 135 nodes fits in one batch trivially.

# Closed set of primary labels — used only to validate the frontmatter
# ``node_type``. The actual write uses ``MATCH (n {id: row.id})``, which
# doesn't interpolate a label at all, so injection isn't a concern here.
VALID_NODE_TYPES = {"Company", "Person", "Industry", "Product", "License", "CreditBureau"}


def _connect():
    """Open a driver to whatever Neo4j the .env points at (Aura or local)."""
    load_dotenv(Path(__file__).parent.parent / ".env")
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "")
    return GraphDatabase.driver(uri, auth=(user, password))


def _write_batch(tx, batch: list[dict]) -> int:
    """UNWIND a batch of {id, embedding} rows; MATCH existing nodes (the
    vault sync has already MERGEd them) and set the embedding + :Embedded
    secondary label. Returns the number of rows the write actually touched.
    """
    result = tx.run(
        """
        UNWIND $batch AS row
        MATCH (n {id: row.id})
        SET n.embedding = row.embedding, n:Embedded
        RETURN count(n) AS touched
        """,
        batch=batch,
    )
    record = result.single()
    return int(record["touched"]) if record else 0


@app.command()
def main() -> None:
    """Embed all vault nodes and upsert vectors into Neo4j."""
    files = sorted(VAULT.rglob("nodes/**/*.md"))
    if not files:
        console.print("[red]No nodes found under vault/nodes/**/*.md[/]")
        raise typer.Exit(1)

    parsed: list[tuple[str, str, str, str]] = []  # (id, primary_label, label, doc)
    for md_file in files:
        try:
            post = frontmatter.load(str(md_file))
        except Exception as e:
            console.print(f"[yellow]Skip[/] {md_file.name}: {e}")
            continue

        node_id = post.metadata.get("id")
        if not node_id:
            console.print(f"[yellow]Skip[/] {md_file.name}: missing id")
            continue

        node_type = str(post.metadata.get("node_type", ""))
        if node_type not in VALID_NODE_TYPES:
            console.print(
                f"[yellow]Skip[/] {md_file.name}: invalid node_type '{node_type}'"
            )
            continue

        label = str(post.metadata.get("label", node_id))
        summary = str(post.metadata.get("summary", ""))
        body = post.content
        doc = f"{label}. {summary}\n\n{body}"
        parsed.append((str(node_id), node_type, label, doc))

    if not parsed:
        console.print("[red]No valid nodes to embed.[/]")
        raise typer.Exit(1)

    console.print(
        f"[bold]Loading[/] sentence-transformers/{MODEL_NAME} "
        f"(first run downloads the model)..."
    )
    model = SentenceTransformer(MODEL_NAME)
    docs = [p[3] for p in parsed]
    console.print(f"[bold]Encoding[/] {len(docs)} nodes...")
    vectors = model.encode(docs, normalize_embeddings=True, show_progress_bar=False)

    # Build the UNWIND payload: one dict per node, embedding as a plain list
    # of floats (Neo4j doesn't accept numpy arrays directly).
    batch: list[dict] = [
        {"id": node_id, "embedding": [float(x) for x in vec]}
        for (node_id, _primary, _label, _doc), vec in zip(parsed, vectors)
    ]
    chunks = [batch[i : i + BATCH_SIZE] for i in range(0, len(batch), BATCH_SIZE)]

    driver = _connect()
    try:
        with driver.session() as session:
            for chunk in chunks:
                session.execute_write(_write_batch, chunk)

            # Verify: every embedded id should now carry the :Embedded label.
            verify = session.run("MATCH (n:Embedded) RETURN count(n) AS c").single()
            embedded_count = int(verify["c"]) if verify else 0
    finally:
        driver.close()

    assert embedded_count == len(parsed), (
        f"verification mismatch: expected {len(parsed)} :Embedded nodes, "
        f"found {embedded_count} (did the vault sync run first?)"
    )

    console.print(
        f"[bold green]Embedded {len(parsed)} nodes "
        f"({EMBED_DIM}-dim) via {len(chunks)} UNWIND batch -> Neo4j[/]"
    )


if __name__ == "__main__":
    app()
