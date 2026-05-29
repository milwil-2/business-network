---
id: vertex-solvents
label: Vertex Solvents
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: AA
  employee_count: 12
  fico: 761
  founded_year: 1993
  hq_location: Tacoma, WA
  status: verified
  trust_score: 82
relationships:
- target: chemicals
  type: OPERATES_IN
- target: polymer-resin
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: import-export-license
  type: HOLDS_LICENSE
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: cascade-industries
  type: SELLS_TO
- target: trident-polymers
  type: SUPPLIES
- target: atlas-chemical-works
  type: SUPPLIES
- target: cardinal-wine-imports
  type: PARTNERS_WITH
- target: quartz-transport
  type: GAVE_REFERENCE_FOR
summary: Vertex Solvents — a verified chemicals business (trust 82/100, credit AA,
  FICO 761).
tags:
- Company
---

**Vertex Solvents** is a verified business in the [[chemicals]] sector, headquartered in Tacoma, WA and founded in 1993. Trust score **82/100**, credit rating **AA**, FICO **761**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $12,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
