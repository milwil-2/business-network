---
id: anchor-distribution
label: Anchor Distribution
node_type: Company
properties:
  annual_revenue_usd: 60000000
  credit_rating: A
  employee_count: 75
  fico: 740
  founded_year: 1976
  hq_location: Boise, ID
  status: verified
  trust_score: 83
relationships:
- target: logistics
  type: OPERATES_IN
- target: freight-services
  type: TRADES_PRODUCT
- target: last-mile-delivery
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: cardinal-transport
  type: SELLS_TO
- target: vertex-transport
  type: SELLS_TO
- target: granite-logistics
  type: SELLS_TO
summary: Anchor Distribution — a verified logistics business (trust 83/100, credit
  A, FICO 740).
tags:
- Company
---

**Anchor Distribution** is a verified business in the [[logistics]] sector, headquartered in Boise, ID and founded in 1976. Trust score **83/100**, credit rating **A**, FICO **740**.

## Trade profile
- Industry: Logistics
- Annual revenue: $60,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
