// Run this once after creating your Neo4j DB (before first sync).
// Open Neo4j Browser at localhost:7474 and paste this in.

CREATE CONSTRAINT concept_id IF NOT EXISTS
  FOR (n:Concept) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT technology_id IF NOT EXISTS
  FOR (n:Technology) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT algorithm_id IF NOT EXISTS
  FOR (n:Algorithm) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT pattern_id IF NOT EXISTS
  FOR (n:Pattern) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT course_id IF NOT EXISTS
  FOR (n:Course) REQUIRE n.id IS UNIQUE;

CREATE INDEX node_label IF NOT EXISTS
  FOR (n:Concept) ON (n.label);

// Verify constraints were created:
SHOW CONSTRAINTS;
