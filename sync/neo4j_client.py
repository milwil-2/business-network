import os

import certifi
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from parser import ParsedNode

VALID_NODE_TYPES = {"Concept", "Technology", "Algorithm", "Pattern"}
VALID_REL_TYPES = {
    "IMPLEMENTS", "USES_QUERY_LANGUAGE", "EXTENDS", "IS_VARIANT_OF",
    "ENABLES", "OPTIMIZED_FOR", "USED_IN", "RELATED_TO", "STORES_AS",
    "COMPETES_WITH", "INSPIRED_BY",
}


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def verify_connectivity(self):
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def write_node(self, node: ParsedNode):
        assert node.node_type in VALID_NODE_TYPES
        props = {
            "id": node.id,
            "label": node.label,
            "summary": node.summary,
            "tags": node.tags,
            **{k: v for k, v in node.properties.items() if isinstance(v, (str, int, float, bool, list))},
        }
        label = node.node_type
        with self._driver.session() as s:
            s.execute_write(
                lambda tx: tx.run(
                    f"MERGE (n:{label} {{id: $id}}) SET n += $props",
                    id=node.id, props=props,
                )
            )

    def write_relationship(self, source_id: str, rel_type: str, target_id: str):
        assert rel_type in VALID_REL_TYPES
        with self._driver.session() as s:
            result = s.execute_write(
                lambda tx: tx.run(
                    f"MATCH (a {{id: $src}}) MATCH (b {{id: $tgt}}) MERGE (a)-[:{rel_type}]->(b) RETURN count(*)",
                    src=source_id, tgt=target_id,
                ).single()
            )
        return result and result[0] > 0

    def node_count(self) -> int:
        with self._driver.session() as s:
            return s.run("MATCH (n) RETURN count(n) AS c").single()["c"]

    def rel_count(self) -> int:
        with self._driver.session() as s:
            return s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
