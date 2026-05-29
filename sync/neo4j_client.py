import os

import certifi
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from parser import ParsedNode

VALID_NODE_TYPES = {"Company", "Person", "Industry", "Product", "License", "CreditBureau"}
VALID_REL_TYPES = {
    "SELLS_TO", "SUPPLIES", "OPERATES_IN", "TRADES_PRODUCT",
    "HOLDS_LICENSE", "RATED_BY", "PRINCIPAL_OF", "GAVE_REFERENCE_FOR",
    "SUBSIDIARY_OF", "PARTNERS_WITH", "COMPETES_WITH", "INVITED",
}

# Secondary "trade role" labels applied to Company nodes, derived from trade
# edges (a business can hold several at once). These are first-class Neo4j
# labels — `MATCH (b:Buyer)` works — layered on top of the :Company label.
VALID_ROLE_LABELS = {"Buyer", "Seller", "Vendor", "Customer"}
# (role label, derivation pattern). Patterns are static — no user input is
# interpolated — so this is injection-safe.
ROLE_RULES = (
    ("Buyer", "MATCH (c:Company)<-[:SELLS_TO]-() SET c:Buyer"),
    ("Seller", "MATCH (c:Company)-[:SELLS_TO]->() SET c:Seller"),
    ("Vendor", "MATCH (c:Company)-[:SUPPLIES]->() SET c:Vendor"),
    ("Customer", "MATCH (c:Company)<-[:SUPPLIES]-() SET c:Customer"),
)


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

    def apply_role_labels(self) -> dict:
        """Derive trade-role labels (Buyer/Seller/Vendor/Customer) on Company
        nodes from their SELLS_TO / SUPPLIES edges. Idempotent: clears the role
        labels first, then re-applies, so it's safe to run on every sync.
        """
        with self._driver.session() as s:
            s.run("MATCH (c:Company) REMOVE c:Buyer:Seller:Vendor:Customer")
            for _role, query in ROLE_RULES:
                s.run(query)
            counts = {}
            for role in ("Buyer", "Seller", "Vendor", "Customer"):
                # Safe: role comes from the closed VALID_ROLE_LABELS set.
                counts[role] = s.run(
                    f"MATCH (c:{role}) RETURN count(c) AS c"
                ).single()["c"]
        return counts

    def node_count(self) -> int:
        with self._driver.session() as s:
            return s.run("MATCH (n) RETURN count(n) AS c").single()["c"]

    def rel_count(self) -> int:
        with self._driver.session() as s:
            return s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
