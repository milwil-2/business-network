---
id: ironclad-chemical-works
label: Ironclad Chemical Works
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: A
  employee_count: 320
  fico: 801
  founded_year: 1999
  hq_location: Reno, NV
  status: verified
  trust_score: 81
relationships:
- target: chemicals
  type: OPERATES_IN
- target: sodium-hydroxide
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: import-export-license
  type: HOLDS_LICENSE
- target: anchor-specialty-chemical
  type: SELLS_TO
- target: atlas-chemical-works
  type: SELLS_TO
- target: vertex-polymers
  type: SELLS_TO
- target: quartz-industries
  type: SUPPLIES
- target: anchor-specialty-chemical
  type: SUPPLIES
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
summary: Ironclad Chemical Works — a verified chemicals business (trust 81/100, credit
  A, FICO 801).
tags:
- Company
---

**Ironclad Chemical Works** is a verified business in the [[chemicals]] sector, headquartered in Reno, NV and founded in 1999. Trust score **81/100**, credit rating **A**, FICO **801**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $35,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
