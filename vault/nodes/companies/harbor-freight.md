---
id: harbor-freight
label: Harbor Freight
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: AAA
  employee_count: 75
  fico: 719
  founded_year: 1981
  hq_location: Austin, TX
  status: verified
  trust_score: 70
relationships:
- target: logistics
  type: OPERATES_IN
- target: last-mile-delivery
  type: TRADES_PRODUCT
- target: freight-services
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: northgate-distribution
  type: SELLS_TO
- target: vertex-transport
  type: SELLS_TO
- target: beacon-transport
  type: SUPPLIES
- target: granite-materials
  type: INVITED
summary: Harbor Freight — a verified logistics business (trust 70/100, credit AAA,
  FICO 719).
tags:
- Company
---

**Harbor Freight** is a verified business in the [[logistics]] sector, headquartered in Austin, TX and founded in 1981. Trust score **70/100**, credit rating **AAA**, FICO **719**.

## Trade profile
- Industry: Logistics
- Annual revenue: $250,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
