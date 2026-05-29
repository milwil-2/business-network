---
id: brightwater-distribution
label: Brightwater Distribution
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: A
  employee_count: 75
  fico: 770
  founded_year: 2014
  hq_location: Memphis, TN
  status: verified
  trust_score: 80
relationships:
- target: logistics
  type: OPERATES_IN
- target: freight-services
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: northgate-distribution
  type: SELLS_TO
- target: cardinal-transport
  type: SELLS_TO
- target: vertex-transport
  type: COMPETES_WITH
- target: vertex-polymers
  type: INVITED
summary: Brightwater Distribution — a verified logistics business (trust 80/100, credit
  A, FICO 770).
tags:
- Company
---

**Brightwater Distribution** is a verified business in the [[logistics]] sector, headquartered in Memphis, TN and founded in 2014. Trust score **80/100**, credit rating **A**, FICO **770**.

## Trade profile
- Industry: Logistics
- Annual revenue: $12,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
