---
id: lumen-building-supply
label: Lumen Building Supply
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: BB
  employee_count: 75
  fico: 681
  founded_year: 1974
  hq_location: Portland, OR
  status: pending
  trust_score: 47
relationships:
- target: building-materials
  type: OPERATES_IN
- target: portland-cement
  type: TRADES_PRODUCT
- target: steel-rebar
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: import-export-license
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: sterling-construction-supply
  type: SELLS_TO
- target: atlas-construction-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SELLS_TO
- target: ironclad-construction-supply
  type: SUPPLIES
- target: granite-logistics
  type: INVITED
summary: Lumen Building Supply — a pending building materials business (trust 47/100,
  credit BB, FICO 681).
tags:
- Company
---

**Lumen Building Supply** is a pending business in the [[building-materials]] sector, headquartered in Portland, OR and founded in 1974. Trust score **47/100**, credit rating **BB**, FICO **681**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $20,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
