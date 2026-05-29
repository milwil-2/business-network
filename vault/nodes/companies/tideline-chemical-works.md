---
id: tideline-chemical-works
label: Tideline Chemical Works
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: AAA
  employee_count: 30
  fico: 707
  founded_year: 1976
  hq_location: Tampa, FL
  status: verified
  trust_score: 69
relationships:
- target: chemicals
  type: OPERATES_IN
- target: industrial-solvent
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: anchor-specialty-chemical
  type: SELLS_TO
- target: vertex-polymers
  type: SELLS_TO
- target: vertex-solvents
  type: SELLS_TO
summary: Tideline Chemical Works — a verified chemicals business (trust 69/100, credit
  AAA, FICO 707).
tags:
- Company
---

**Tideline Chemical Works** is a verified business in the [[chemicals]] sector, headquartered in Tampa, FL and founded in 1976. Trust score **69/100**, credit rating **AAA**, FICO **707**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $35,000,000
- Employees: 30

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
