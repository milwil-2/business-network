---
id: atlas-chemical-works
label: Atlas Chemical Works
node_type: Company
properties:
  annual_revenue_usd: 8000000
  credit_rating: AA
  employee_count: 75
  fico: 733
  founded_year: 2001
  hq_location: Atlanta, GA
  status: verified
  trust_score: 81
relationships:
- target: chemicals
  type: OPERATES_IN
- target: polymer-resin
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: vertex-solvents
  type: SELLS_TO
- target: trident-polymers
  type: SELLS_TO
- target: cascade-industries
  type: SELLS_TO
- target: vertex-polymers
  type: SUPPLIES
- target: summit-chemical-works
  type: SUPPLIES
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
summary: Atlas Chemical Works — a verified chemicals business (trust 81/100, credit
  AA, FICO 733).
tags:
- Company
---

**Atlas Chemical Works** is a verified business in the [[chemicals]] sector, headquartered in Atlanta, GA and founded in 2001. Trust score **81/100**, credit rating **AA**, FICO **733**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $8,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
