---
id: copperline-logistics
label: Copperline Logistics
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: A
  employee_count: 600
  fico: 710
  founded_year: 2008
  hq_location: Denver, CO
  status: verified
  trust_score: 74
relationships:
- target: logistics
  type: OPERATES_IN
- target: cold-storage
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: northgate-distribution
  type: SELLS_TO
- target: brightwater-distribution
  type: SELLS_TO
- target: cardinal-transport
  type: SUPPLIES
- target: anchor-distribution
  type: COMPETES_WITH
- target: summit-brewing
  type: GAVE_REFERENCE_FOR
- target: cardinal-cement-works
  type: INVITED
summary: Copperline Logistics — a verified logistics business (trust 74/100, credit
  A, FICO 710).
tags:
- Company
---

**Copperline Logistics** is a verified business in the [[logistics]] sector, headquartered in Denver, CO and founded in 2008. Trust score **74/100**, credit rating **A**, FICO **710**.

## Trade profile
- Industry: Logistics
- Annual revenue: $35,000,000
- Employees: 600

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
