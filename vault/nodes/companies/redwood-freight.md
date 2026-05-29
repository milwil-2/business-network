---
id: redwood-freight
label: Redwood Freight
node_type: Company
properties:
  annual_revenue_usd: 60000000
  credit_rating: BBB
  employee_count: 75
  fico: 607
  founded_year: 1972
  hq_location: Atlanta, GA
  status: pending
  trust_score: 57
relationships:
- target: logistics
  type: OPERATES_IN
- target: cold-storage
  type: TRADES_PRODUCT
- target: freight-services
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: copperline-logistics
  type: SELLS_TO
- target: northgate-distribution
  type: SELLS_TO
- target: cardinal-transport
  type: SELLS_TO
- target: granite-logistics
  type: SUPPLIES
- target: brightwater-distribution
  type: COMPETES_WITH
- target: cardinal-food-distributors
  type: INVITED
summary: Redwood Freight — a pending logistics business (trust 57/100, credit BBB,
  FICO 607).
tags:
- Company
---

**Redwood Freight** is a pending business in the [[logistics]] sector, headquartered in Atlanta, GA and founded in 1972. Trust score **57/100**, credit rating **BBB**, FICO **607**.

## Trade profile
- Industry: Logistics
- Annual revenue: $60,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
