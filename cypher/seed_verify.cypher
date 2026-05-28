// Quick sanity checks after running --full sync.
// Run these in Neo4j Browser to confirm the graph loaded correctly.

// Total node count (expect ~22)
MATCH (n) RETURN count(n) AS total_nodes;

// Node count by type
MATCH (n) RETURN labels(n)[0] AS type, count(n) AS count ORDER BY type;

// Total relationship count (expect ~35-40)
MATCH ()-[r]->() RETURN count(r) AS total_relationships;

// Relationship types and counts
MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS count ORDER BY count DESC;

// Any isolated nodes (no edges — these are worth connecting)
MATCH (n) WHERE NOT (n)--() RETURN n.id, labels(n)[0] AS type;
