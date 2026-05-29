---
id: northgate-distribution
label: Northgate Distribution
node_type: Company
properties:
  annual_revenue_usd: 2000000
  credit_rating: AA
  employee_count: 1100
  fico: 800
  founded_year: 1991
  hq_location: Columbus, OH
  status: verified
  trust_score: 66
relationships:
- target: logistics
  type: OPERATES_IN
- target: last-mile-delivery
  type: TRADES_PRODUCT
- target: cold-storage
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: beacon-transport
  type: SELLS_TO
- target: harbor-freight
  type: SELLS_TO
- target: redwood-freight
  type: SUPPLIES
summary: Northgate Distribution — a verified logistics business (trust 66/100, credit
  AA, FICO 800).
tags:
- Company
---

**Northgate Distribution** is a verified business in the [[logistics]] sector, headquartered in Columbus, OH and founded in 1991. Trust score **66/100**, credit rating **AA**, FICO **800**.

## Trade profile
- Industry: Logistics
- Annual revenue: $2,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
