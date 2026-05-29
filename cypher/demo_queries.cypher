// ═══════════════════════════════════════════════════════════════════
// INTERVIEW DEMO QUERIES — B2B Trade & Trust Network
// Run in Neo4j Browser at localhost:7474 (or the Aura query editor)
// For Q7: switch to "Graph" tab to see the visual graph
// ═══════════════════════════════════════════════════════════════════


// ─── Q1: Basic node lookup ───────────────────────────────────────
// "Show me everything about this company, including its trust signals."
// Talking point: nodes store properties (trust_score, fico, credit_rating)
// just like rows — but relationships are first-class, not foreign keys.

MATCH (c:Company)
RETURN c
ORDER BY c.trust_score DESC
LIMIT 1;


// ─── Q2: One-hop traversal ───────────────────────────────────────
// "Who does this company trade with, and how?"
// Talking point: relationship traversal vs JOIN — the edge IS the
// pointer, no index lookup needed.

MATCH (c:Company)-[r]->(neighbor)
WITH c, r, neighbor ORDER BY c.trust_score DESC LIMIT 1
RETURN c.label           AS source,
       type(r)           AS relationship,
       neighbor.label    AS target,
       labels(neighbor)  AS target_type;


// ─── Q3: Vendor recommendation (2-hop) ───────────────────────────
// "Which vendors supply the buyers that a given company already sells to?"
// Talking point: [*2] multi-hop in one declarative pattern — the core
// 'network effect' query a B2B platform like Nuvo runs constantly.

MATCH (me:Company)-[:SELLS_TO]->(buyer:Company)<-[:SUPPLIES]-(vendor:Company)
WHERE me.status = 'verified'
RETURN me.label      AS company,
       buyer.label   AS shared_buyer,
       vendor.label  AS suggested_vendor,
       vendor.trust_score AS vendor_trust
ORDER BY vendor_trust DESC
LIMIT 15;


// ─── Q4: Trust path (shortest path) ──────────────────────────────
// "How is company A connected to company B through the trade network?"
// Talking point: shortestPath() is a built-in graph primitive. SQL
// equivalent: recursive CTE + window function — multiple pages.

MATCH (a:Company), (b:Company)
WHERE a.id <> b.id
WITH a, b LIMIT 1
MATCH path = shortestPath((a)-[*..6]-(b))
RETURN [n IN nodes(path)         | n.label]  AS path_labels,
       [r IN relationships(path) | type(r)]  AS rel_types,
       length(path)                          AS hops;


// ─── Q5: FRAUD RING — shared principals across flagged companies ──
// "Find people who are principals of more than one FLAGGED company."
// Talking point: graph-native fraud detection. The shared-principal
// pattern is trivial in Cypher and painful in SQL.

MATCH (p:Person)-[:PRINCIPAL_OF]->(c:Company)
WHERE c.status = 'flagged'
WITH p, collect(c.label) AS flagged_companies, count(c) AS n
WHERE n > 1
RETURN p.label AS principal, n AS flagged_count, flagged_companies
ORDER BY n DESC;


// ─── Q6: Trust hubs (degree centrality) ──────────────────────────
// "Which companies are most-referenced — the trust hubs of the network?"
// Talking point: degree centrality on GAVE_REFERENCE_FOR; leads
// naturally into PageRank as a recursive, graph-native improvement.

MATCH (ref:Company)-[:GAVE_REFERENCE_FOR]->(c:Company)
RETURN c.label              AS company,
       c.trust_score        AS trust_score,
       count(ref)           AS references_received,
       collect(ref.label)   AS referrers
ORDER BY references_received DESC
LIMIT 10;


// ─── Q7: Industry subgraph (VISUAL DEMO) ─────────────────────────
// "Show the full trade graph for one industry."
// Talking point: subgraph queries are natural — no UNION, no temp
// tables. SWITCH TO GRAPH TAB IN NEO4J BROWSER for the visual.

MATCH (c:Company)-[:OPERATES_IN]->(i:Industry)
WITH i LIMIT 1
MATCH (c:Company)-[:OPERATES_IN]->(i)
MATCH (c)-[r]->(related)
RETURN c, r, related, i;


// ─── Q8: Credit risk in the supply chain (path predicate) ────────
// "Find supply chains where a low-credit vendor supplies a verified buyer,
//  without passing through any flagged company along the way."
// Talking point: NONE() path predicate — constrained traversal that
// would require multiple CTEs in SQL.

MATCH (vendor:Company)-[:SUPPLIES*1..3]->(buyer:Company)
WHERE vendor.fico < 600 AND buyer.status = 'verified'
WITH vendor, buyer, shortestPath((vendor)-[:SUPPLIES*1..3]->(buyer)) AS path
WHERE NONE(n IN nodes(path) WHERE n.status = 'flagged')
RETURN vendor.label AS risky_vendor,
       vendor.fico  AS vendor_fico,
       buyer.label  AS verified_buyer,
       length(path) AS hops
ORDER BY vendor_fico ASC
LIMIT 10;


// ─── Q9: Multi-label trade roles ─────────────────────────────────
// Companies that are BOTH buyer and vendor (multi-label role labels)
// Talking point: a node can carry many secondary labels at once —
// each business stays ONE node while role queries like (:Buyer:Vendor)
// match on first-class labels derived from its trade edges.

MATCH (c:Buyer:Vendor) RETURN c.label, c.trust_score ORDER BY c.trust_score DESC LIMIT 10;
