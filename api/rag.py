"""GraphRAG over the Neo4j knowledge graph using Groq (Llama 3.3).

Retrieval is hybrid: we first try semantic (vector) search to pull the most
relevant seed nodes and their neighbors as focused context. If the embedding
service (HuggingFace Inference API) is unavailable we fall back to passing
every node summary into the prompt — the graph is small (~100 nodes) so that
still fits. Either way the LLM cites the node ids it used, and we enrich
those ids with their neighbors so the UI can show the subgraph that grounded
the answer.
"""

import os
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

    lines: list[str] = []
    for seed in seeds:
        node = db.get_node(seed["id"])
        if node is None:
            continue
        lines.append(
            f"- {node['id']} ({node['type']}): "
            f"{node['label']} — {node['summary']}"
        )
        for edge in db.get_neighbors(node["id"]):
            lines.append(
                f"  -[{edge['rel']}]-> {edge['target_label']}"
            )
    return "\n".join(lines), "hybrid"


def answer_question(question: str, mode: str = "auto") -> dict:
    """Answer a question grounded in the graph; never raises."""
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
