// Run this once after creating your Neo4j DB (before first sync).
// Open Neo4j Browser at localhost:7474 (or the Aura query editor) and paste this in.

CREATE CONSTRAINT company_id IF NOT EXISTS
  FOR (n:Company) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT person_id IF NOT EXISTS
  FOR (n:Person) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT industry_id IF NOT EXISTS
  FOR (n:Industry) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT product_id IF NOT EXISTS
  FOR (n:Product) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT license_id IF NOT EXISTS
  FOR (n:License) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT credit_bureau_id IF NOT EXISTS
  FOR (n:CreditBureau) REQUIRE n.id IS UNIQUE;

CREATE INDEX node_label IF NOT EXISTS
  FOR (n:Company) ON (n.label);

// Verify constraints were created:
SHOW CONSTRAINTS;
