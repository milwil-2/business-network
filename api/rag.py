"""GraphRAG over the Neo4j knowledge graph using Groq (Llama 3.3).

Retrieval is hybrid: we first try semantic (vector) search to pull the most
relevant seed nodes and their neighbors as focused context. If the embedding
service (HuggingFace Inference API) is unavailable we fall back to passing
every node summary into the prompt — the graph is small (~100 nodes) so that
still fits. Either way the LLM cites the node ids it used, and we enrich
those ids with their neighbors so the UI can show the subgraph that grounded
the answer.

The optional ``cypher`` mode goes a different route: it asks the LLM to emit a
read-only Cypher query against the closed-vocabulary schema, validates it
hard (write-keyword denylist, label/rel-type allowlist, length cap), executes
it in a READ session, and then summarizes the rows. This is the most accurate
path for strict graph-traversal questions ("which vendors supply the buyers a
company sells to") that hybrid retrieval can only approximate.
"""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import APIError, Groq, RateLimitError
from pydantic import BaseModel

from vector.store import semantic_search

from . import db

load_dotenv(Path(__file__).parent.parent / ".env")

SYSTEM_INSTRUCTION = (
    "You answer questions about a B2B trade & trust network (companies, their "
    "principals, trade relationships, products/industries, licenses, and "
    "creditworthiness) using ONLY the provided knowledge-graph nodes. When "
    "relevant, surface trust signals (trust_score, credit_rating, fico, status) "
    "and trade connections. Respond with a JSON object of the form "
    '{"answer": "<your answer>", "cited_node_ids": ["<id>", ...]} — list the '
    "node ids you used in cited_node_ids. If the graph lacks the info, say so "
    "in the answer."
)


class RagAnswer(BaseModel):
    answer: str
    cited_node_ids: list[str]


def _graph_only_context() -> tuple[str, str]:
    summaries = db.all_node_summaries()
    context = "\n".join(
        f"- {n['id']} ({n['type']}): {n['label']} — {n['summary']}"
        for n in summaries
    )
    return context, "graph-only"


def _retrieve_context(question: str, mode: str = "auto") -> tuple[str, str]:
    """Build grounding context for the question.

    ``mode`` controls retrieval:
      - ``"auto"`` (default): try hybrid (vector seeds + neighbors); on a
        RuntimeError from the embedding service, fall back to graph-only.
      - ``"hybrid"``: same as auto but the user explicitly asked for hybrid.
        Still falls back silently on RuntimeError; the returned mode reflects
        what was actually used.
      - ``"graph-only"``: skip vector retrieval entirely and pass every node
        summary as context.
    """
    if mode == "graph-only":
        return _graph_only_context()

    try:
        seeds = semantic_search(question, k=6)
    except RuntimeError:
        return _graph_only_context()

    # 2-hop neighbourhood per seed so the LLM can answer traversal questions
    # like "which vendors supply the buyers a company sells to" — a pattern
    # that's invisible if we only fetch the seed's direct neighbours. Highly
    # connected seeds (e.g. a freight hub) can pull 200+ edges in 2 hops, so
    # cap per-seed and overall to stay inside Groq's TPM budget.
    EDGES_PER_SEED = 30
    TOTAL_EDGES_CAP = 150
    lines: list[str] = []
    seen_seeds: set[str] = set()
    seen_edges: set[tuple] = set()
    for seed in seeds:
        if len(seen_edges) >= TOTAL_EDGES_CAP:
            break
        node = db.get_node(seed["id"])
        if node is None or node["id"] in seen_seeds:
            continue
        seen_seeds.add(node["id"])
        lines.append(
            f"- {node['id']} ({node['type']}): "
            f"{node['label']} — {node['summary']}"
        )
        seed_edges_added = 0
        for edge in db.get_neighborhood(node["id"], hops=2):
            if seed_edges_added >= EDGES_PER_SEED:
                break
            if len(seen_edges) >= TOTAL_EDGES_CAP:
                break
            key = (edge["src_id"], edge["rel"], edge["dst_id"])
            if key in seen_edges:
                continue
            seen_edges.add(key)
            seed_edges_added += 1
            lines.append(
                f"  ({edge['src_id']}) -[:{edge['rel']}]-> ({edge['dst_id']})"
            )
    return "\n".join(lines), "hybrid"


# --- text-to-Cypher mode ----------------------------------------------------
# Closed vocabularies mirrored from CLAUDE.md / sync/parser.py. The validator
# uses these as an allowlist; any label or rel-type token in the LLM's output
# that isn't here causes a hard reject (defense in depth — even though we also
# pin the session to READ and run a write-keyword denylist).
_PRIMARY_LABELS = frozenset(
    {"Company", "Person", "Industry", "Product", "License", "CreditBureau"}
)
_ROLE_LABELS = frozenset({"Buyer", "Seller", "Vendor", "Customer", "Embedded"})
_ALLOWED_LABELS = _PRIMARY_LABELS | _ROLE_LABELS
_ALLOWED_REL_TYPES = frozenset(
    {
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
)

# Word-boundary regex of write/admin keywords. CALL is rejected outright (no
# procedure access in v1); LOAD covers LOAD CSV; USING PERIODIC COMMIT is
# matched as a phrase. Case-insensitive.
_WRITE_KEYWORDS = (
    "CREATE",
    "MERGE",
    "DELETE",
    "DETACH",
    "SET",
    "REMOVE",
    "DROP",
    "CALL",
    "LOAD",
)
_WRITE_KEYWORD_RE = re.compile(
    r"\b(?:" + "|".join(_WRITE_KEYWORDS) + r")\b", re.IGNORECASE
)
_PERIODIC_COMMIT_RE = re.compile(r"\bUSING\s+PERIODIC\s+COMMIT\b", re.IGNORECASE)

# Match :Label and :REL_TYPE occurrences. Cypher identifiers are [A-Za-z_][A-Za-z0-9_]*.
# A leading ``:`` followed by an identifier covers node labels and rel types
# alike; we then look the name up in the union of allowed sets.
_LABEL_TOKEN_RE = re.compile(r":\s*([A-Za-z_][A-Za-z0-9_]*)")
_COMMENT_RE = re.compile(r"//[^\n]*")
_CYPHER_MAX_LEN = 2000


def _strip_cypher(cypher: str) -> str:
    """Strip ``//`` line comments and trim whitespace."""
    return _COMMENT_RE.sub("", cypher).strip()


def validate_cypher(cypher: str) -> tuple[bool, str]:
    """Return ``(ok, reason)`` for a candidate read-only Cypher query.

    Hard rules (any failure → reject):
      * Length cap (2000 chars after stripping comments).
      * Must start with ``MATCH`` or ``OPTIONAL MATCH`` (case-insensitive).
      * Must not contain any write/admin keyword from ``_WRITE_KEYWORDS`` or
        the ``USING PERIODIC COMMIT`` phrase.
      * Every ``:Label`` / ``:REL_TYPE`` token must be in the closed-vocab
        allowlist (primary/role labels + relationship types).
    """
    if not isinstance(cypher, str) or not cypher.strip():
        return False, "empty query"
    stripped = _strip_cypher(cypher)
    if not stripped:
        return False, "empty query"
    if len(stripped) > _CYPHER_MAX_LEN:
        return False, f"query exceeds {_CYPHER_MAX_LEN} chars"
    head = stripped.lstrip().upper()
    if not (head.startswith("MATCH") or head.startswith("OPTIONAL MATCH")):
        return False, "query must start with MATCH or OPTIONAL MATCH"
    if _PERIODIC_COMMIT_RE.search(stripped):
        return False, "write/admin keyword not allowed: USING PERIODIC COMMIT"
    write_match = _WRITE_KEYWORD_RE.search(stripped)
    if write_match:
        return False, f"write/admin keyword not allowed: {write_match.group(0).upper()}"
    for token in _LABEL_TOKEN_RE.findall(stripped):
        if token not in _ALLOWED_LABELS and token not in _ALLOWED_REL_TYPES:
            return False, f"unknown label or relationship type: {token}"
    return True, "ok"


_CYPHER_SYSTEM_PROMPT = (
    "You translate natural-language questions about a B2B trade & trust "
    "network into a single read-only Cypher query for Neo4j.\n\n"
    "Schema (closed vocabulary — do NOT invent labels or rel types):\n"
    "  Node labels (primary): "
    + ", ".join(sorted(_PRIMARY_LABELS))
    + "\n"
    "  Node labels (secondary trade roles on :Company): "
    + ", ".join(sorted(_ROLE_LABELS))
    + "\n"
    "  Relationship types: "
    + ", ".join(sorted(_ALLOWED_REL_TYPES))
    + "\n"
    "  Key Company properties: id, label, summary, trust_score, "
    "credit_rating, fico, status\n\n"
    "Rules: emit ONE query, beginning with MATCH or OPTIONAL MATCH; never use "
    "CREATE, MERGE, DELETE, DETACH, SET, REMOVE, DROP, CALL, or LOAD; always "
    "RETURN something useful (prefer id + label columns so the caller can "
    "cite nodes); add a LIMIT (<= 25) for any open-ended query. Use only the "
    "labels and rel types listed above. Respond with a JSON object of the "
    'form {"cypher": "<query>"} and nothing else.'
)


class _CypherPlan(BaseModel):
    cypher: str


class _CypherSummary(BaseModel):
    answer: str
    cited_node_ids: list[str] = []


def _serialize_rows(rows: list[dict]) -> list[dict]:
    """Convert Neo4j Record values into JSON-safe dicts.

    Node values become ``{id, label, type}``; relationship/path values fall
    back to ``str(value)``; primitives pass through.
    """
    safe: list[dict] = []
    for row in rows:
        out: dict = {}
        for key, value in row.items():
            try:
                # neo4j.graph.Node has a ``labels`` attribute and is dict-like.
                labels = getattr(value, "labels", None)
                if labels is not None and hasattr(value, "items"):
                    props = dict(value)
                    out[key] = {
                        "id": props.get("id"),
                        "label": props.get("label"),
                        "type": next(
                            (l for l in labels if l in _PRIMARY_LABELS),
                            next(iter(labels), None),
                        ),
                    }
                elif isinstance(value, (str, int, float, bool)) or value is None:
                    out[key] = value
                elif isinstance(value, (list, tuple)):
                    out[key] = [
                        v if isinstance(v, (str, int, float, bool)) or v is None else str(v)
                        for v in value
                    ]
                elif isinstance(value, dict):
                    out[key] = value
                else:
                    out[key] = str(value)
            except Exception:
                out[key] = str(value)
        safe.append(out)
    return safe


def _extract_cited_ids(rows: list[dict]) -> list[str]:
    """Pull any ``id``-shaped values out of the result rows, de-duplicated."""
    seen: list[str] = []
    seen_set: set[str] = set()
    for row in rows:
        for key, value in row.items():
            candidate = None
            if isinstance(value, dict) and isinstance(value.get("id"), str):
                candidate = value["id"]
            elif isinstance(value, str) and (
                key == "id" or key.endswith("_id") or key.endswith(".id")
            ):
                candidate = value
            if candidate and candidate not in seen_set:
                seen_set.add(candidate)
                seen.append(candidate)
    return seen


def _cypher_failure(reason: str, cypher: str) -> dict:
    """Shared failure shape for the cypher mode."""
    return {
        "answer": "Couldn't construct a safe Cypher query for that question.",
        "cited_node_ids": [],
        "subgraph": {},
        "mode": "cypher",
        "cypher": cypher,
        "error": reason,
    }


def _cypher_mode_answer(question: str) -> dict:
    """Text-to-Cypher path. Two Groq calls (plan, summarize) bracketing one
    read-only Neo4j execution. Never raises."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

    # --- 1. Plan: ask the LLM for a Cypher query --------------------------
    try:
        plan_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            max_tokens=512,
            messages=[
                {"role": "system", "content": _CYPHER_SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        plan = _CypherPlan.model_validate_json(plan_response.choices[0].message.content)
    except RateLimitError:
        return _cypher_failure("LLM rate limit hit — try again in a minute.", "")
    except APIError:
        return _cypher_failure("LLM is temporarily unavailable.", "")
    except Exception as e:
        return _cypher_failure(f"LLM returned an unparseable plan: {type(e).__name__}", "")

    cypher = plan.cypher.strip()

    # --- 2. Validate ------------------------------------------------------
    ok, reason = validate_cypher(cypher)
    if not ok:
        return _cypher_failure(reason, cypher)

    # --- 3. Execute (read-only) ------------------------------------------
    try:
        with db.get_driver().session(default_access_mode="READ") as session:
            result = session.run(cypher)
            rows = [dict(record) for record in result]
    except Exception as e:
        # Don't leak driver internals into the response.
        return _cypher_failure(
            f"Cypher execution failed: {type(e).__name__}", cypher
        )

    serialized = _serialize_rows(rows)
    cited = _extract_cited_ids(serialized)

    # --- 4. Summarize -----------------------------------------------------
    summary_system = (
        "You answer questions about a B2B trade & trust network using ONLY "
        "the rows returned by an executed Cypher query. Be concise and "
        "direct. If the rows are empty, say so. Respond with a JSON object "
        'of the form {"answer": "<your answer>", "cited_node_ids": ["<id>", ...]}.'
    )
    summary_user = (
        f"Question: {question}\n\n"
        f"Executed Cypher:\n{cypher}\n\n"
        f"Result rows (JSON):\n{json.dumps(serialized[:50], default=str)}"
    )
    try:
        summary_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            max_tokens=1024,
            messages=[
                {"role": "system", "content": summary_system},
                {"role": "user", "content": summary_user},
            ],
        )
        parsed = _CypherSummary.model_validate_json(
            summary_response.choices[0].message.content
        )
        answer = parsed.answer
        # Prefer ids the summarizer cited if any are in our extracted set;
        # otherwise fall back to what we pulled out of the rows.
        cited_final = [cid for cid in parsed.cited_node_ids if cid in set(cited)] or cited
    except RateLimitError:
        # Cypher ran; we just couldn't summarize. Hand back what we have.
        answer = "LLM rate limit hit while summarizing — see the raw rows."
        cited_final = cited
    except APIError:
        answer = "LLM is temporarily unavailable for summarizing — see the raw rows."
        cited_final = cited
    except Exception:
        answer = "Couldn't summarize the result rows."
        cited_final = cited

    # Bound the subgraph payload — only enrich up to the first 10 cited ids.
    subgraph: dict = {}
    for node_id in cited_final[:10]:
        try:
            subgraph[node_id] = db.get_neighbors(node_id)
        except Exception:
            pass

    return {
        "answer": answer,
        "cited_node_ids": cited_final,
        "subgraph": subgraph,
        "mode": "cypher",
        "cypher": cypher,
        "rows": serialized[:50],
    }


def answer_question(question: str, mode: str = "auto") -> dict:
    """Answer a question grounded in the graph; never raises."""
    if mode == "cypher":
        return _cypher_mode_answer(question)
    context, mode = _retrieve_context(question, mode=mode)
    user_content = (
        f"Question: {question}\n\n"
        f"Knowledge-graph nodes:\n{context}"
    )

    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            max_tokens=2048,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_content},
            ],
        )
        parsed = RagAnswer.model_validate_json(response.choices[0].message.content)
    except RateLimitError:
        return {
            "answer": "LLM rate limit hit — wait a minute and try again (Groq free tier is ~30 req/min).",
            "cited_node_ids": [],
            "subgraph": {},
        }
    except APIError:
        return {
            "answer": "The language model is temporarily unavailable. Please try again.",
            "cited_node_ids": [],
            "subgraph": {},
        }

    subgraph = {}
    for node_id in parsed.cited_node_ids:
        subgraph[node_id] = db.get_neighbors(node_id)

    return {
        "answer": parsed.answer,
        "cited_node_ids": parsed.cited_node_ids,
        "subgraph": subgraph,
        "mode": mode,
    }
