"""Extract knowledge graph nodes from raw notes or topic names using Groq (Llama 3.3).

Usage:
    uv run sync/extract.py --topic "Cascade Beverage Co"
    uv run sync/extract.py --inbox
    uv run sync/extract.py --file vault/inbox/my-note.md
    uv run sync/extract.py --inbox --auto-sync
    uv run sync/extract.py --topic "Ironclad Building Supply" --dry-run
"""

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Literal

import frontmatter
import typer
import yaml
from dotenv import load_dotenv
from groq import APIError, Groq, RateLimitError
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

load_dotenv(Path(__file__).parent.parent / ".env")

app = typer.Typer(help="Extract knowledge graph nodes using Groq.")
console = Console()

VALID_NODE_TYPES = {"Company", "Person", "Industry", "Product", "License", "CreditBureau"}
VALID_REL_TYPES = {
    "SELLS_TO",
    "SUPPLIES",
    "OPERATES_IN",
    "TRADES_PRODUCT",
    "HOLDS_LICENSE",
    "RATED_BY",
    "PRINCIPAL_OF",
    "GAVE_REFERENCE_FOR",
    "SUBSIDIARY_OF",
    "PARTNERS_WITH",
    "COMPETES_WITH",
    "INVITED",
}

NODE_TYPE_SUBDIR = {
    "Company": "companies",
    "Person": "people",
    "Industry": "industries",
    "Product": "products",
    "License": "licenses",
    "CreditBureau": "bureaus",
}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class Relationship(BaseModel):
    type: str
    target: str


class ExtractedNode(BaseModel):
    id: str
    label: str
    node_type: Literal["Company", "Person", "Industry", "Product", "License", "CreditBureau"]
    tags: list[str]
    summary: str
    properties: dict[str, str | int | float] = {}
    relationships: list[Relationship] = []
    body: str


class ExtractionResult(BaseModel):
    nodes: list[ExtractedNode]


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def load_existing_nodes(vault_path: Path) -> list[str]:
    """Scan vault and return sorted list of existing node IDs."""
    ids: list[str] = []
    for md_file in vault_path.rglob("nodes/**/*.md"):
        try:
            post = frontmatter.load(str(md_file))
            node_id = post.metadata.get("id")
            if node_id:
                ids.append(str(node_id))
        except Exception:
            pass
    return sorted(ids)


def build_system_prompt(existing_ids: list[str]) -> str:
    """Build the system prompt for the extraction task."""
    ids_block = "\n".join(f"  - {nid}" for nid in existing_ids) if existing_ids else "  (none yet)"
    return f"""You are a B2B trade-network curator. Extract structured nodes from text and return a JSON object. The graph models a Nuvo-style network of verified businesses, who runs them, what they trade, and their creditworthiness/trust.

## Node types (use one of these exact values)
- Company — a business / trade entity (e.g. "Cascade Beverage Co", "Ironclad Building Supply")
- Person — a principal, owner, or officer of a company (e.g. "Dana Whitfield, CEO")
- Industry — a trade sector (e.g. "Alcohol & Beverage", "Building Materials", "Chemicals", "Food Service")
- Product — a traded commodity or good (e.g. "Craft Lager", "Portland Cement", "Industrial Solvent")
- License — a regulatory/business license (e.g. "Federal Liquor Permit", "Hazmat Handling License")
- CreditBureau — a credit-rating / business-verification agency (e.g. "Dun & Bradstreet", "Experian Business")

## Valid relationship types (use ONLY these exact strings)
SELLS_TO, SUPPLIES, OPERATES_IN, TRADES_PRODUCT, HOLDS_LICENSE, RATED_BY, PRINCIPAL_OF, GAVE_REFERENCE_FOR, SUBSIDIARY_OF, PARTNERS_WITH, COMPETES_WITH, INVITED

## Existing node IDs (ONLY use these as relationship targets — never invent new ones)
{ids_block}

## Rules
1. id: kebab-case slug, lowercase, hyphens only
2. summary: exactly one sentence
3. tags: must include the node_type string as one of the tags
4. properties: put trust signals on Company nodes when present — trust_score (0-100), credit_rating (AAA..D), fico (300-850), annual_revenue_usd, founded_year, hq_location, status (verified|pending|flagged)
5. body: 3–5 paragraphs of Obsidian markdown, use [[wikilinks]] for cross-references
6. Extract ALL relevant nodes mentioned — a single note may yield multiple nodes
7. relationships[].target must be an ID from the existing list above — if nothing fits, leave relationships empty

## Output format
Return ONLY a JSON object with this exact structure (no markdown fences):
{{"nodes": [{{"id": "...", "label": "...", "node_type": "Company|Person|Industry|Product|License|CreditBureau", "tags": ["..."], "summary": "...", "properties": {{}}, "relationships": [{{"type": "...", "target": "..."}}], "body": "..."}}]}}
"""


def extract_nodes(
    text: str,
    client: Groq,
    system_prompt: str,
) -> list[ExtractedNode]:
    """Call Groq (Llama 3.3) to extract nodes from text."""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
            )
            return ExtractionResult.model_validate_json(
                response.choices[0].message.content
            ).nodes
        except RateLimitError:
            if attempt < max_attempts:
                time.sleep(5 * attempt)
                continue
            console.print("[bold red]Groq rate limit hit.[/bold red]")
            console.print(
                "[dim]Free tier is ~30 requests/min. Wait a minute and retry.[/dim]"
            )
            raise typer.Exit(1)
        except APIError as e:
            console.print(f"[red]Groq error:[/red] {e}")
            raise typer.Exit(1)
    # Unreachable: loop either returns or raises.
    raise typer.Exit(1)


def write_node_file(node: ExtractedNode, vault_path: Path) -> tuple[Path, bool]:
    """Write a node to a markdown file. Returns (path, was_written)."""
    if node.node_type not in VALID_NODE_TYPES:
        console.print(
            f"[yellow]Warning:[/yellow] Skipping node '{node.id}' — invalid node_type '{node.node_type}'"
        )
        return vault_path, False

    subdir = NODE_TYPE_SUBDIR[node.node_type]
    path = vault_path / "nodes" / subdir / f"{node.id}.md"

    if path.exists():
        return path, False

    # Filter out invalid relationship types
    valid_rels = []
    for rel in node.relationships:
        if rel.type not in VALID_REL_TYPES:
            console.print(
                f"[yellow]Warning:[/yellow] Skipping relationship '{rel.type}' on node '{node.id}' — not in valid set"
            )
        else:
            valid_rels.append(rel)

    # Build frontmatter dict
    fm_data: dict[str, Any] = {
        "id": node.id,
        "label": node.label,
        "node_type": node.node_type,
        "summary": node.summary,
        "tags": node.tags,
    }
    if node.properties:
        fm_data["properties"] = dict(node.properties)
    if valid_rels:
        fm_data["relationships"] = [{"type": r.type, "target": r.target} for r in valid_rels]

    yaml_str = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True, sort_keys=True)
    content = f"---\n{yaml_str}---\n\n{node.body}\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path, True


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


def _run_extraction(
    text: str,
    client: Groq,
    vault_path: Path,
    source_label: str,
    dry_run: bool,
) -> list[tuple[Path, bool]]:
    """Run extraction on a single text blob and optionally write results."""
    existing_ids = load_existing_nodes(vault_path)
    system_prompt = build_system_prompt(existing_ids)

    console.print(f"[bold]Extracting nodes from:[/bold] {source_label}")
    nodes = extract_nodes(text, client, system_prompt)
    console.print(f"  → Found [cyan]{len(nodes)}[/cyan] node(s)")

    results: list[tuple[Path, bool]] = []
    for node in nodes:
        if dry_run:
            console.print(
                f"  [dim]DRY RUN[/dim] would write: [bold]{node.id}[/bold] "
                f"({node.node_type}) — {node.summary[:80]}"
            )
            results.append((vault_path / "nodes" / NODE_TYPE_SUBDIR.get(node.node_type, "concepts") / f"{node.id}.md", True))
        else:
            path, written = write_node_file(node, vault_path)
            results.append((path, written))
            status = "[green]✓[/green]" if written else "[dim]skipped (exists)[/dim]"
            console.print(f"  {status} {path.name}")

    return results


def _print_summary_table(all_results: list[tuple[Path, bool]]) -> None:
    """Print a rich summary table of all results."""
    table = Table(title="Extraction Summary")
    table.add_column("File", style="cyan")
    table.add_column("Status", justify="center")

    written = 0
    skipped = 0
    for path, was_written in all_results:
        if was_written:
            table.add_row(path.name, "[green]written[/green]")
            written += 1
        else:
            table.add_row(path.name, "[dim]skipped[/dim]")
            skipped += 1

    console.print(table)
    console.print(
        f"\n[bold]Total:[/bold] {written} written, {skipped} skipped / already existed"
    )


@app.command()
def main(
    topic: str = typer.Option(None, "--topic", help="Generate a node from a topic name"),
    inbox: bool = typer.Option(False, "--inbox", "-i", help="Process all files in vault/inbox/"),
    file: Path = typer.Option(None, "--file", help="Process a single file"),
    auto_sync: bool = typer.Option(
        False, "--auto-sync", help="After extraction, run obsidian_to_neo4j.py --full"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing files"),
) -> None:
    """Extract knowledge graph nodes from notes or topic names using Groq."""
    if not topic and not inbox and not file:
        console.print("[red]Error:[/red] Provide --topic, --inbox, or --file.")
        raise typer.Exit(1)

    vault_path = Path(__file__).parent.parent / "vault"
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    all_results: list[tuple[Path, bool]] = []

    # --topic
    if topic:
        text = (
            f"Generate a comprehensive knowledge graph node for: {topic}\n\n"
            "Include accurate technical details, key properties, and relationships to other "
            "software engineering concepts."
        )
        results = _run_extraction(text, client, vault_path, f"topic: {topic}", dry_run)
        all_results.extend(results)

    # --file
    if file:
        if not file.exists():
            console.print(f"[red]Error:[/red] File not found: {file}")
            raise typer.Exit(1)
        content = file.read_text(encoding="utf-8")
        text = f"Extract knowledge graph nodes from this note:\n\n{content}"
        results = _run_extraction(text, client, vault_path, str(file), dry_run)
        all_results.extend(results)

        if not dry_run:
            processed_dir = file.parent / "processed"
            processed_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), processed_dir / file.name)
            console.print(f"  [dim]Moved to processed/[/dim]")

    # --inbox
    if inbox:
        inbox_dir = vault_path / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        processed_dir = inbox_dir / "processed"

        inbox_files = [
            f
            for f in inbox_dir.glob("*.md")
            if f.is_file() and f.parent != processed_dir
        ]

        if not inbox_files:
            console.print("[dim]No .md files found in vault/inbox/[/dim]")
        else:
            console.print(f"Found [cyan]{len(inbox_files)}[/cyan] file(s) in inbox")
            for inbox_file in sorted(inbox_files):
                content = inbox_file.read_text(encoding="utf-8")
                text = f"Extract knowledge graph nodes from this note:\n\n{content}"
                results = _run_extraction(
                    text, client, vault_path, inbox_file.name, dry_run
                )
                all_results.extend(results)

                if not dry_run:
                    processed_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(inbox_file), processed_dir / inbox_file.name)
                    console.print(f"  [dim]Moved {inbox_file.name} to processed/[/dim]")

    _print_summary_table(all_results)

    # --auto-sync
    if auto_sync and not dry_run and any(written for _, written in all_results):
        console.print("\n[bold]Running obsidian_to_neo4j.py --full ...[/bold]")
        result = subprocess.run(
            ["uv", "run", "sync/obsidian_to_neo4j.py", "--full"],
            cwd=vault_path.parent,
        )
        if result.returncode != 0:
            console.print("[red]obsidian_to_neo4j.py exited with an error[/red]")
            raise typer.Exit(result.returncode)


if __name__ == "__main__":
    app()
