// Quick sanity checks after running --full sync.
// Run these in Neo4j Browser (or the Aura query editor) to confirm the graph loaded correctly.

// Total node count (expect ~80-120)
MATCH (n) RETURN count(n) AS total_nodes;

// Node count by type
MATCH (n) RETURN labels(n)[0] AS type, count(n) AS count ORDER BY type;

// Total relationship count
MATCH ()-[r]->() RETURN count(r) AS total_relationships;

// Relationship types and counts
MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS count ORDER BY count DESC;

// Company status breakdown (verified / pending / flagged)
MATCH (c:Company) RETURN c.status AS status, count(c) AS count ORDER BY count DESC;

// Any isolated nodes (no edges — these are worth connecting)
MATCH (n) WHERE NOT (n)--() RETURN n.id, labels(n)[0] AS type;
