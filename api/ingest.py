"""Gated, staged, safe-by-default ingestion for the knowledge-graph API.

This module is intentionally self-contained (no imports from ``sync/``, which
is excluded from the Vercel bundle) and disabled-by-default: every entry point
is a no-op unless an ``INGEST_API_KEY`` env var is set. Because the public
Vercel deploy leaves that var unset, ingestion is off there; a developer sets
it locally to turn it on.

The flow is deliberately two-phase. ``extract`` turns free text into structured
nodes via Groq; ``stage`` writes them into a quarantine ``:Staged`` label
(never the curated graph); ``approve`` promotes the quarantined nodes into real,
labelled nodes and relationships. Because the node/relationship vocabulary is a
closed set we can safely interpolate the validated label/rel-type into Cypher.
"""

import hmac
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import APIError, Groq, RateLimitError
from pydantic import BaseModel, Field

from . import db

load_dotenv(Path(__file__).parent.parent / ".env")

# --- closed vocabulary -----------------------------------------------------
VALID_NODE_TYPES = {"Concept", "Technology", "Algorithm", "Pattern", "Course"}
VALID_REL_TYPES = {
    "IMPLEMENTS",
    "USES_QUERY_LANGUAGE",
    "EXTENDS",
    "IS_VARIANT_OF",
    "ENABLES",
    "OPTIMIZED_FOR",
    "USED_IN",
    "RELATED_TO",
    "STORES_AS",
    "COMPETES_WITH",
    "INSPIRED_BY",
    "PREREQUISITE_OF",
    "COVERS",
}

# --- limits & rate limiting ------------------------------------------------
MAX_INGEST_BYTES = 8192
_RATE_LIMIT = 10
_RATE_WINDOW = 60.0
# Per-key sliding window of recent call timestamps. In-memory only; on a warm
# serverless instance this throttles bursts, which is all we need here.
_calls: dict[str, list[float]] = {}


# --- gating ----------------------------------------------------------------
def is_enabled() -> bool:
    """True only when an INGEST_API_KEY is configured."""
    return bool(os.environ.get("INGEST_API_KEY"))


def check_key(provided: str | None) -> bool:
    """Constant-time compare the provided key against INGEST_API_KEY."""
    expected = os.environ.get("INGEST_API_KEY")
    if not expected or provided is None:
        return False
    return hmac.compare_digest(provided, expected)


def rate_ok(key: str) -> bool:
    """Allow up to _RATE_LIMIT calls per key within a rolling _RATE_WINDOW."""
    now = time.monotonic()
    recent = [t for t in _calls.get(key, []) if now - t < _RATE_WINDOW]
    if len(recent) >= _RATE_LIMIT:
        _calls[key] = recent
        return False
    recent.append(now)
    _calls[key] = recent
    return True


# --- extraction schema -----------------------------------------------------
class ExtractedRelationship(BaseModel):
    type: str
    target: str


class ExtractedNode(BaseModel):
    id: str
    label: str
    node_type: str
    tags: list[str] = Field(default_factory=list)
    summary: str = ""
    properties: dict = Field(default_factory=dict)
    relationships: list[ExtractedRelationship] = Field(default_factory=list)


class ExtractionResult(BaseModel):
    nodes: list[ExtractedNode] = Field(default_factory=list)


_SYSTEM_PROMPT = (
    "You extract a software-engineering knowledge graph from the provided text. "
    "Each node must use one of these node_type values: "
    + ", ".join(sorted(VALID_NODE_TYPES))
    + ". Each relationship must use one of these type values: "
    + ", ".join(sorted(VALID_REL_TYPES))
    + ". A relationship is an object {\"type\": <rel type>, \"target\": <node id>}. "
    "Give every node a short lowercase-hyphenated id, a human label, a one-line "
    "summary, and any tags. Return ONLY a JSON object of the form "
    '{"nodes": [...]} and nothing else.'
)


def extract(text: str) -> list[ExtractedNode]:
    """Run Groq over ``text`` and return structured nodes.

    Raises ``RuntimeError`` with a clean message on Groq rate-limit/API errors;
    the FastAPI handler maps that to a 429/502.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            max_tokens=2048,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
    except RateLimitError as e:
        raise RuntimeError(
            "LLM rate limit hit — wait a minute and try again."
        ) from e
    except APIError as e:
        raise RuntimeError(f"LLM error: {e}") from e
    return ExtractionResult.model_validate_json(
        resp.choices[0].message.content
    ).nodes


# --- staging (quarantine) --------------------------------------------------
def stage(nodes: list[ExtractedNode]) -> list[dict]:
    """Write nodes into the ``:Staged`` quarantine; return a preview.

    Nodes whose ``node_type`` is outside the closed vocabulary are skipped
    entirely; relationships whose ``type`` is outside the vocabulary are dropped.
    Relationships are stored as a JSON string because Neo4j cannot store a list
    of maps as a property.
    """
    preview: list[dict] = []
    with db.get_driver().session() as s:
        for node in nodes:
            if node.node_type not in VALID_NODE_TYPES:
                continue
            valid_rels = [
                {"type": r.type, "target": r.target}
                for r in node.relationships
                if r.type in VALID_REL_TYPES
            ]
            rels_json = json.dumps(valid_rels)
            s.run(
                """
                MERGE (n:Staged {id:$id})
                SET n.label=$label,
                    n.summary=$summary,
                    n.staged_type=$type,
                    n.tags=$tags,
                    n.staged_relationships=$rels_json,
                    n.source='ingested',
                    n.staged_at=timestamp()
                """,
                id=node.id,
                label=node.label,
                summary=node.summary,
                type=node.node_type,
                tags=node.tags,
                rels_json=rels_json,
            )
            preview.append(
                {
                    "id": node.id,
                    "staged_type": node.node_type,
                    "label": node.label,
                    "n_relationships": len(valid_rels),
                }
            )
    return preview


def list_staged() -> list[dict]:
    """Return id/type/label for every quarantined node awaiting approval."""
    with db.get_driver().session() as s:
        records = s.run(
            "MATCH (n:Staged) RETURN n.id AS id, "
            "n.staged_type AS staged_type, n.label AS label"
        )
        return [dict(r) for r in records]


def approve() -> dict:
    """Promote every ``:Staged`` node into a real, labelled node.

    The staged_type and relationship types are interpolated into Cypher only
    AFTER asserting membership in the closed vocabulary, so there is no
    injection surface. Promotion only ever MERGEs.
    """
    promoted = 0
    with db.get_driver().session() as s:
        staged = list(
            s.run(
                "MATCH (n:Staged) RETURN n.id AS id, n.label AS label, "
                "n.summary AS summary, n.staged_type AS staged_type, "
                "n.tags AS tags, n.staged_relationships AS rels"
            )
        )
        for rec in staged:
            label = rec["staged_type"]
            if label not in VALID_NODE_TYPES:
                continue
            # Safe: label comes from the closed VALID_NODE_TYPES set.
            s.run(
                f"MERGE (m:{label} {{id:$id}}) "
                "SET m.label=$label, m.summary=$summary, m.tags=$tags",
                id=rec["id"],
                label=rec["label"],
                summary=rec["summary"],
                tags=rec["tags"],
            )
            try:
                rels = json.loads(rec["rels"] or "[]")
            except (TypeError, ValueError):
                rels = []
            for rel in rels:
                rel_type = rel.get("type")
                target = rel.get("target")
                if rel_type not in VALID_REL_TYPES or not target:
                    continue
                # Safe: rel_type comes from the closed VALID_REL_TYPES set.
                s.run(
                    f"MATCH (a {{id:$src}}) MATCH (b {{id:$tgt}}) "
                    f"MERGE (a)-[:{rel_type}]->(b)",
                    src=rec["id"],
                    tgt=target,
                )
            s.run(
                "MATCH (s:Staged {id:$id}) DETACH DELETE s",
                id=rec["id"],
            )
            promoted += 1
    return {"promoted": promoted}
