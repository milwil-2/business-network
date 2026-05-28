#!/usr/bin/env python3
"""Sync Obsidian vault nodes to Neo4j. Run with: uv run sync/obsidian_to_neo4j.py"""

import os
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent))
from neo4j_client import Neo4jClient
from parser import ParsedNode, scan_vault
from state import get_changed_nodes, load_state, mark_synced, save_state

load_dotenv(Path(__file__).parent.parent / ".env")

app = typer.Typer(help="Sync Obsidian vault to Neo4j graph database.")
console = Console()

VAULT_PATH = Path(__file__).parent.parent / "vault"


@app.command()
def sync(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Parse and preview without writing to Neo4j"),
    full: bool = typer.Option(False, "--full", "-f", help="Force re-sync all nodes, ignore incremental state"),
    vault: Path = typer.Option(VAULT_PATH, "--vault", help="Path to Obsidian vault root"),
):
    nodes, errors = scan_vault(vault)

    if errors:
        console.print(f"[yellow]Warnings ({len(errors)}):[/]")
        for name, msg in errors:
            console.print(f"  [yellow]⚠[/]  {name}: {msg}")

    state = {} if full else load_state()
    changed = get_changed_nodes(nodes, state) if not full else nodes

    console.print(f"\n[bold]Vault:[/] {len(nodes)} nodes total, [bold]{len(changed)} to sync[/]\n")

    if not changed:
        console.print("[dim]Nothing changed. Use --full to force re-sync.[/]")
        return

    if dry_run:
        _print_dry_run(changed)
        return

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "")

    client = Neo4jClient(uri, user, password)
    try:
        client.verify_connectivity()
        console.print(f"[green]Connected[/] to Neo4j at {uri}\n")
    except Exception as e:
        console.print(f"[red]Cannot connect to Neo4j:[/] {e}")
        console.print("[dim]Is Neo4j Desktop running? Check .env for correct URI/credentials.[/]")
        raise typer.Exit(1)

    # Pass 1: upsert all nodes first
    console.print("[bold]Pass 1: Nodes[/]")
    for node in changed:
        client.write_node(node)
        console.print(f"  [green]MERGE[/] (:{node.node_type} {{id: '{node.id}'}})")

    # Pass 2: upsert relationships
    console.print("\n[bold]Pass 2: Relationships[/]")
    rel_count = 0
    skipped = 0
    for node in changed:
        for rel in node.relationships:
            ok = client.write_relationship(node.id, rel["type"], rel["target"])
            if ok:
                console.print(f"  [cyan]MERGE[/] ({node.id})-[:{rel['type']}]->({rel['target']})")
                rel_count += 1
            else:
                console.print(f"  [yellow]SKIP[/]  ({node.id})-[:{rel['type']}]->({rel['target']}) — target not found")
                skipped += 1

    client.close()

    new_state = mark_synced(changed, state)
    save_state(new_state)

    console.print(f"\n[bold green]Done.[/] Synced {len(changed)} nodes, {rel_count} relationships."
                  + (f" ({skipped} skipped — missing targets)" if skipped else ""))


def _print_dry_run(nodes: list[ParsedNode]):
    t = Table("id", "type", "summary", "relationships", title="Dry Run Preview", show_lines=True)
    for n in nodes:
        rels = "\n".join(f"{r['type']} → {r['target']}" for r in n.relationships) or "-"
        t.add_row(n.id, n.node_type, n.summary[:60] + ("…" if len(n.summary) > 60 else ""), rels)
    console.print(t)


if __name__ == "__main__":
    app()
