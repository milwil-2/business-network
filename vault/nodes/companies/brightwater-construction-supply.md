---
id: brightwater-construction-supply
label: Brightwater Construction Supply
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: AAA
  employee_count: 75
  fico: 697
  founded_year: 1983
  hq_location: Reno, NV
  status: verified
  trust_score: 72
relationships:
- target: building-materials
  type: OPERATES_IN
- target: steel-rebar
  type: TRADES_PRODUCT
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: trident-building-supply
  type: SELLS_TO
- target: crescent-building-supply
  type: SUPPLIES
summary: Brightwater Construction Supply — a verified building materials business
  (trust 72/100, credit AAA, FICO 697).
tags:
- Company
---

**Brightwater Construction Supply** is a verified business in the [[building-materials]] sector, headquartered in Reno, NV and founded in 1983. Trust score **72/100**, credit rating **AAA**, FICO **697**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $20,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
