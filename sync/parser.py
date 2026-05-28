import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")

VALID_NODE_TYPES = {"Concept", "Technology", "Algorithm", "Pattern", "Course"}
VALID_REL_TYPES = {
    "IMPLEMENTS", "USES_QUERY_LANGUAGE", "EXTENDS", "IS_VARIANT_OF",
    "ENABLES", "OPTIMIZED_FOR", "USED_IN", "RELATED_TO", "STORES_AS",
    "COMPETES_WITH", "INSPIRED_BY", "PREREQUISITE_OF", "COVERS",
}


@dataclass
class ParsedNode:
    id: str
    label: str
    node_type: str
    tags: list[str]
    summary: str
    properties: dict
    relationships: list[dict]
    implicit_links: list[str]
    source_path: Path
    mtime: float


def slug(text: str) -> str:
    return text.strip().lower().replace(" ", "-")


def parse_node_file(path: Path) -> ParsedNode:
    post = frontmatter.load(str(path))
    fm = post.metadata

    node_type = fm.get("node_type", "Concept")
    if node_type not in VALID_NODE_TYPES:
        raise ValueError(f"Invalid node_type '{node_type}' in {path.name}")

    rels = fm.get("relationships", [])
    for r in rels:
        if r.get("type") not in VALID_REL_TYPES:
            raise ValueError(f"Unknown relationship type '{r.get('type')}' in {path.name}")

    explicit_targets = {slug(r["target"]) for r in rels}
    body_links = [slug(l) for l in WIKILINK_RE.findall(post.content)]
    implicit = [l for l in body_links if l not in explicit_targets]

    return ParsedNode(
        id=fm["id"],
        label=fm.get("label", fm["id"]),
        node_type=node_type,
        tags=fm.get("tags", []),
        summary=fm.get("summary", ""),
        properties=fm.get("properties", {}),
        relationships=rels,
        implicit_links=list(dict.fromkeys(implicit)),
        source_path=path,
        mtime=path.stat().st_mtime,
    )


def scan_vault(vault_path: Path) -> list[ParsedNode]:
    nodes = []
    errors = []
    for md_file in sorted(vault_path.rglob("nodes/**/*.md")):
        try:
            nodes.append(parse_node_file(md_file))
        except Exception as e:
            errors.append((md_file.name, str(e)))
    return nodes, errors
