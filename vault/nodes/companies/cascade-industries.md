---
id: cascade-industries
label: Cascade Industries
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: BBB
  employee_count: 1100
  fico: 775
  founded_year: 1989
  hq_location: Oakland, CA
  status: verified
  trust_score: 85
relationships:
- target: chemicals
  type: OPERATES_IN
- target: industrial-solvent
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: atlas-industries
  type: SELLS_TO
- target: anchor-specialty-chemical
  type: SELLS_TO
- target: summit-chemical-works
  type: SUPPLIES
summary: Cascade Industries — a verified chemicals business (trust 85/100, credit
  BBB, FICO 775).
tags:
- Company
---

**Cascade Industries** is a verified business in the [[chemicals]] sector, headquartered in Oakland, CA and founded in 1989. Trust score **85/100**, credit rating **BBB**, FICO **775**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $12,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
