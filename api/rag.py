"""GraphRAG over the Neo4j knowledge graph using Groq (Llama 3.3).

The whole graph is small (~22 nodes) so we pass every node summary into the
prompt as grounding context and ask the LLM to cite the node ids it used. We
then enrich the cited ids with their neighbors so the UI can show the
subgraph that grounded the answer.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import APIError, Groq, RateLimitError
from pydantic import BaseModel

from . import db

load_dotenv(Path(__file__).parent.parent / ".env")

SYSTEM_INSTRUCTION = (
    "You answer questions about software engineering using ONLY the provided "
    "knowledge-graph nodes. Respond with a JSON object of the form "
    '{"answer": "<your answer>", "cited_node_ids": ["<id>", ...]} — list the '
    "node ids you used in cited_node_ids. If the graph lacks the info, say so "
    "in the answer."
)


class RagAnswer(BaseModel):
    answer: str
    cited_node_ids: list[str]


def answer_question(question: str) -> dict:
    """Answer a question grounded in the graph; never raises."""
    summaries = db.all_node_summaries()
    context = "\n".join(
        f"- {n['id']} ({n['type']}): {n['label']} — {n['summary']}" for n in summaries
    )
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
    except APIError as e:
        return {
            "answer": f"LLM error: {e}",
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
    }
