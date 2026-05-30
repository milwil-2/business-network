"""Self-contained Neo4j access layer for the knowledge-graph API.

All query functions open a session, run a read query, and return plain
JSON-serializable dicts/lists so the FastAPI layer can hand them straight
to a response. The driver is a lazily-created module-level singleton so it
is reused across requests (important for serverless warm invocations).
"""

import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(Path(__file__).parent.parent / ".env")
# macOS framework Python lacks a CA bundle; point TLS at certifi so the
# neo4j+s:// connection to Aura verifies. Harmless on Linux/Vercel.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

PRIMARY_TYPES = ["Company", "Person", "Industry", "Product", "License", "CreditBureau"]

_driver = None


def get_driver():
    """Return a cached Neo4j driver, creating it on first use."""
    global _driver
    if _driver is None:
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "")
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver


def health() -> dict:
    """Return basic graph stats: status plus node and relationship counts."""
    with get_driver().session() as s:
        nodes = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        rels = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return {"status": "ok", "nodes": nodes, "relationships": rels}


def get_node(node_id: str) -> dict | None:
    """Fetch a single node by id, or None if it doesn't exist."""
    with get_driver().session() as s:
        record = s.run(
            "MATCH (n {id:$id}) RETURN n, [l IN labels(n) WHERE l IN $primary][0] AS type, "
            "[l IN labels(n) WHERE NOT l IN $primary] AS roles",
            id=node_id,
            primary=PRIMARY_TYPES,
        ).single()
    if record is None:
        return None
    node = record["n"]
    props = dict(node)
    return {
        "id": props.get("id"),
        "label": props.get("label"),
        "type": record["type"],
        "roles": record["roles"],
        "summary": props.get("summary"),
        "properties": props,
    }


def get_neighbors(node_id: str) -> list[dict]:
    """Return outgoing neighbors of a node as a list of edge/target dicts."""
    with get_driver().session() as s:
        records = s.run(
            """
            MATCH (n {id:$id})-[r]->(m)
            RETURN type(r) AS rel,
                   m.id AS target_id,
                   m.label AS target_label,
                   [l IN labels(m) WHERE l IN $primary][0] AS target_type
            """,
            id=node_id,
            primary=PRIMARY_TYPES,
        )
        return [dict(r) for r in records]


def get_neighborhood(node_id: str, hops: int = 2) -> list[dict]:
    """Return every edge within ``hops`` of ``node_id``, in either direction.

    Used by GraphRAG hybrid retrieval so the LLM can see multi-hop graph
    patterns (e.g. ``Seller -[:SELLS_TO]-> Buyer <-[:SUPPLIES]- Vendor``)
    rather than just the seed's direct neighbours. Each row is a directed
    edge ``{src_id, src_label, src_type, rel, dst_id, dst_label, dst_type,
    tier}``; the variable-length match is undirected so we don't miss inbound
    edges like the one a buyer receives from its vendors.

    Edges are returned sorted by ``tier`` so the rag layer can cap to a budget
    without losing the *critical* edges (issue #11):

    - **tier 1** — edge directly incident to the seed (1-hop).
    - **tier 2** — 2-hop edge whose *both* endpoints are 1-hop neighbours of
      the seed, i.e. an edge that closes a 2-hop chain back to the seed
      (e.g. the vendor-recommendation pattern
      ``seed -[:SELLS_TO]-> Buyer <-[:SUPPLIES]- Vendor`` becomes the tier-2
      edge ``Vendor -[:SUPPLIES]-> Buyer``). Trade relationships
      (``SELLS_TO``, ``SUPPLIES``, ``PARTNERS_WITH``, ``COMPETES_WITH``,
      ``SUBSIDIARY_OF``) within tier 2 sort before metadata/principal/
      reference rels — they're what the LLM actually needs for recommendation
      questions, and the rest are usually downstream noise.
    - **tier 3** — any other 2-hop edge (one endpoint is a 1-hop neighbour
      via a shared industry / product / license / credit bureau, the other
      isn't directly tied to the seed). High-volume; filled only after the
      first two tiers.
    """
    # ``hops`` is interpolated into Cypher (var-length patterns can't be
    # parameterised). Restrict to a tiny safe set to keep this injection-safe.
    assert hops in (1, 2, 3), f"unsupported hops: {hops}"
    # Trade rels carry the actual buyer/seller/vendor signal; everything else
    # (licenses, industries, ratings, references, principals) is metadata.
    # Sorting these first within tier 2 makes the cap survive the genuine
    # closing-chain edges before the metadata duplicates of the seed's own
    # 1-hop rels.
    trade_rels = ["SELLS_TO", "SUPPLIES", "PARTNERS_WITH", "COMPETES_WITH", "SUBSIDIARY_OF"]
    with get_driver().session() as s:
        records = s.run(
            f"""
            MATCH (seed {{id:$id}})
            OPTIONAL MATCH (seed)-[]-(hop1)
            WHERE hop1.id <> $id
            WITH seed, collect(DISTINCT hop1.id) AS hop1_ids
            MATCH path = (seed)-[*1..{hops}]-(other)
            WHERE other.id <> $id
            UNWIND relationships(path) AS r
            WITH DISTINCT r, hop1_ids, startNode(r) AS a, endNode(r) AS b
            WITH r, a, b,
                 CASE
                   WHEN a.id = $id OR b.id = $id THEN 1
                   WHEN a.id IN hop1_ids AND b.id IN hop1_ids THEN 2
                   ELSE 3
                 END AS tier
            WITH r, a, b, tier,
                 CASE WHEN tier = 2 AND type(r) IN $trade_rels THEN 0 ELSE 1 END AS trade_priority
            RETURN a.id AS src_id, a.label AS src_label,
                   [l IN labels(a) WHERE l IN $primary][0] AS src_type,
                   type(r) AS rel,
                   b.id AS dst_id, b.label AS dst_label,
                   [l IN labels(b) WHERE l IN $primary][0] AS dst_type,
                   tier
            ORDER BY tier ASC, trade_priority ASC, src_id, dst_id
            """,
            id=node_id,
            primary=PRIMARY_TYPES,
            trade_rels=trade_rels,
        )
        return [dict(r) for r in records]


def get_graph() -> dict:
    """Return the entire graph shaped for vis-network rendering."""
    with get_driver().session() as s:
        node_records = s.run(
            "MATCH (n) RETURN n.id AS id, n.label AS label, "
            "[l IN labels(n) WHERE l IN $primary][0] AS group, n.summary AS title",
            primary=PRIMARY_TYPES,
        )
        nodes = [dict(r) for r in node_records]
        edge_records = s.run(
            "MATCH (a)-[r]->(b) RETURN a.id AS from, b.id AS to, type(r) AS label"
        )
        edges = [dict(r) for r in edge_records]
    return {"nodes": nodes, "edges": edges}


def shortest_path(source: str, target: str) -> dict:
    """Return the shortest path (<= 8 hops) between two nodes by id."""
    with get_driver().session() as s:
        record = s.run(
            """
            MATCH (a {id:$source}), (b {id:$target}),
                  p = shortestPath((a)-[*..8]-(b))
            RETURN [n IN nodes(p) | n.label] AS labels,
                   [r IN relationships(p) | type(r)] AS rels,
                   length(p) AS hops
            """,
            source=source,
            target=target,
        ).single()
    if record is None:
        return {"error": "no path"}
    return {"labels": record["labels"], "rels": record["rels"], "hops": record["hops"]}


def search_nodes(query: str) -> list[dict]:
    """Case-insensitive search over node labels and summaries."""
    with get_driver().session() as s:
        records = s.run(
            """
            MATCH (n)
            WHERE toLower(n.label) CONTAINS toLower($q)
               OR toLower(n.summary) CONTAINS toLower($q)
            RETURN n.id AS id, n.label AS label,
                   [l IN labels(n) WHERE l IN $primary][0] AS type, n.summary AS summary
            LIMIT 25
            """,
            q=query,
            primary=PRIMARY_TYPES,
        )
        return [dict(r) for r in records]


def all_node_summaries() -> list[dict]:
    """Return id/label/type/summary for every node (used by GraphRAG context)."""
    with get_driver().session() as s:
        records = s.run(
            "MATCH (n) RETURN n.id AS id, n.label AS label, "
            "[l IN labels(n) WHERE l IN $primary][0] AS type, n.summary AS summary",
            primary=PRIMARY_TYPES,
        )
        return [dict(r) for r in records]
