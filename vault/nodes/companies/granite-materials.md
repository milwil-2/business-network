---
id: granite-materials
label: Granite Materials
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: AAA
  employee_count: 12
  fico: 731
  founded_year: 2003
  hq_location: Portland, OR
  status: verified
  trust_score: 73
relationships:
- target: building-materials
  type: OPERATES_IN
- target: portland-cement
  type: TRADES_PRODUCT
- target: steel-rebar
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: meridian-building-supply
  type: SELLS_TO
- target: crescent-building-supply
  type: SELLS_TO
- target: brightwater-construction-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SUPPLIES
- target: meridian-building-supply
  type: SUPPLIES
summary: Granite Materials — a verified building materials business (trust 73/100,
  credit AAA, FICO 731).
tags:
- Company
---

**Granite Materials** is a verified business in the [[building-materials]] sector, headquartered in Portland, OR and founded in 2003. Trust score **73/100**, credit rating **AAA**, FICO **731**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $35,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
