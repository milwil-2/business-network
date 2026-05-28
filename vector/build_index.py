#!/usr/bin/env python3
"""Build the Chroma vector index from Obsidian vault nodes.

Run with:
    uv run vector/build_index.py
    uv run vector/build_index.py --reset
"""

import sys
from pathlib import Path

import frontmatter
import typer
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent.parent))
from vector.store import COLLECTION, get_client, get_collection

app = typer.Typer(help="Build the Chroma vector index from the Obsidian vault.")
console = Console()

VAULT = Path(__file__).parent.parent / "vault"


@app.command()
def main(
    reset: bool = typer.Option(
        False, "--reset", help="Delete and recreate the collection before indexing"
    ),
) -> None:
    """Embed all vault nodes and upsert them into the Chroma collection."""
    if reset:
        try:
            get_client().delete_collection(COLLECTION)
            console.print(f"[yellow]Reset:[/] dropped collection '{COLLECTION}'")
        except Exception:
            # Collection may not exist yet — that's fine.
            pass
        # Force the store to rebuild its lazy singleton on next access.
        import vector.store as store

        store._collection = None

    col = get_collection()

    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    for md_file in VAULT.rglob("nodes/**/*.md"):
        try:
            post = frontmatter.load(str(md_file))
        except Exception as e:
            console.print(f"[yellow]Skip[/] {md_file.name}: {e}")
            continue

        node_id = post.metadata.get("id")
        if not node_id:
            console.print(f"[yellow]Skip[/] {md_file.name}: missing id")
            continue

        label = str(post.metadata.get("label", node_id))
        summary = str(post.metadata.get("summary", ""))
        node_type = str(post.metadata.get("node_type", ""))
        body = post.content

        doc = f"{label}. {summary}\n\n{body}"

        ids.append(str(node_id))
        documents.append(doc)
        metadatas.append({"label": label, "type": node_type})

    if not ids:
        console.print("[red]No nodes found under vault/nodes/**/*.md[/]")
        raise typer.Exit(1)

    console.print(f"[bold]Embedding[/] {len(ids)} nodes (downloading model on first run)...")
    col.upsert(ids=ids, documents=documents, metadatas=metadatas)

    console.print(f"[bold green]Done.[/] Embedded {len(ids)} nodes into '{COLLECTION}'.")


if __name__ == "__main__":
    app()
