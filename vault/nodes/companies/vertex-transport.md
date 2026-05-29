---
id: vertex-transport
label: Vertex Transport
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: AA
  employee_count: 30
  fico: 798
  founded_year: 2018
  hq_location: Memphis, TN
  status: verified
  trust_score: 78
relationships:
- target: logistics
  type: OPERATES_IN
- target: freight-services
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: anchor-distribution
  type: SELLS_TO
- target: redwood-freight
  type: SELLS_TO
- target: cardinal-transport
  type: SUPPLIES
- target: granite-logistics
  type: SUPPLIES
- target: copperline-food-distributors
  type: INVITED
summary: Vertex Transport — a verified logistics business (trust 78/100, credit AA,
  FICO 798).
tags:
- Company
---

**Vertex Transport** is a verified business in the [[logistics]] sector, headquartered in Memphis, TN and founded in 2018. Trust score **78/100**, credit rating **AA**, FICO **798**.

## Trade profile
- Industry: Logistics
- Annual revenue: $250,000,000
- Employees: 30

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
