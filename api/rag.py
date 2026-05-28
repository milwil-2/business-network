"""GraphRAG over the Neo4j knowledge graph using Google Gemini.

The whole graph is small (~22 nodes) so we pass every node summary into the
prompt as grounding context and ask Gemini to cite the node ids it used. We
then enrich the cited ids with their neighbors so the UI can show the
subgraph that grounded the answer.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from . import db

load_dotenv(Path(__file__).parent.parent / ".env")

SYSTEM_INSTRUCTION = (
    "You answer questions about software engineering using ONLY the provided "
    "knowledge-graph nodes. Cite the node ids you used in cited_node_ids. "
    "If the graph lacks the info, say so."
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
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=RagAnswer,
            ),
        )
        parsed = RagAnswer.model_validate_json(response.text)
    except errors.ClientError as e:
        is_quota = e.code == 429 or "RESOURCE_EXHAUSTED" in str(e)
        if is_quota:
            return {
                "answer": (
                    "LLM quota exhausted — set a working GEMINI_API_KEY "
                    "(create one in a NEW project at "
                    "https://aistudio.google.com/apikey)."
                ),
                "cited_node_ids": [],
                "subgraph": {},
            }
        return {
            "answer": f"LLM error: {e.message}",
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
