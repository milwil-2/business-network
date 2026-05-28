#!/usr/bin/env python3
"""Live sync: watches the vault and syncs changed nodes to Neo4j on save.

Usage: uv run sync/watcher.py
Keep running while editing in Obsidian. Every .md save triggers an incremental sync.
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

sys.path.insert(0, str(Path(__file__).parent))
from neo4j_client import Neo4jClient
from parser import parse_node_file
from state import load_state, mark_synced, save_state

load_dotenv(Path(__file__).parent.parent / ".env")

VAULT_PATH = Path(__file__).parent.parent / "vault"
console = Console()


def make_client() -> Neo4jClient:
    return Neo4jClient(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        os.environ.get("NEO4J_USER", "neo4j"),
        os.environ.get("NEO4J_PASSWORD", ""),
    )


def sync_file(path: Path, client: Neo4jClient, state: dict) -> dict:
    if "nodes/" not in str(path) or not str(path).endswith(".md"):
        return state
    try:
        node = parse_node_file(path)
        client.write_node(node)
        console.print(f"[green]MERGE[/] (:{node.node_type} {{id: '{node.id}'}})")
        for rel in node.relationships:
            ok = client.write_relationship(node.id, rel["type"], rel["target"])
            status = "[cyan]MERGE[/]" if ok else "[yellow]SKIP[/] (target not found)"
            console.print(f"  {status} ({node.id})-[:{rel['type']}]->({rel['target']})")
        return mark_synced([node], state)
    except Exception as e:
        console.print(f"[red]Error syncing {path.name}:[/] {e}")
        return state


class VaultHandler(FileSystemEventHandler):
    def __init__(self, client: Neo4jClient):
        self.client = client
        self.state = load_state()

    def on_modified(self, event):
        if event.is_directory:
            return
        self.state = sync_file(Path(event.src_path), self.client, self.state)
        save_state(self.state)

    def on_created(self, event):
        self.on_modified(event)


def main():
    client = make_client()
    try:
        client.verify_connectivity()
        console.print(f"[green]Connected[/] to Neo4j. Watching [bold]{VAULT_PATH}[/bold]...")
        console.print("[dim]Edit any node file in Obsidian — changes sync automatically. Ctrl+C to stop.[/dim]\n")
    except Exception as e:
        console.print(f"[red]Cannot connect to Neo4j:[/] {e}")
        sys.exit(1)

    handler = VaultHandler(client)
    observer = Observer()
    observer.schedule(handler, str(VAULT_PATH), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n[dim]Watcher stopped.[/dim]")
    observer.join()
    client.close()


if __name__ == "__main__":
    main()
