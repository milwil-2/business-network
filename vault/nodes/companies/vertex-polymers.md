---
id: vertex-polymers
label: Vertex Polymers
node_type: Company
properties:
  annual_revenue_usd: 120000000
  credit_rating: AAA
  employee_count: 12
  fico: 753
  founded_year: 2007
  hq_location: Tacoma, WA
  status: verified
  trust_score: 76
relationships:
- target: chemicals
  type: OPERATES_IN
- target: industrial-solvent
  type: TRADES_PRODUCT
- target: sodium-hydroxide
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: anchor-specialty-chemical
  type: SELLS_TO
- target: atlas-chemical-works
  type: SELLS_TO
- target: cardinal-wine-imports
  type: GAVE_REFERENCE_FOR
summary: Vertex Polymers — a verified chemicals business (trust 76/100, credit AAA,
  FICO 753).
tags:
- Company
---

**Vertex Polymers** is a verified business in the [[chemicals]] sector, headquartered in Tacoma, WA and founded in 2007. Trust score **76/100**, credit rating **AAA**, FICO **753**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $120,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
