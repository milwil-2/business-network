---
id: granite-logistics
label: Granite Logistics
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: BB
  employee_count: 140
  fico: 684
  founded_year: 1999
  hq_location: Atlanta, GA
  status: pending
  trust_score: 48
relationships:
- target: logistics
  type: OPERATES_IN
- target: cold-storage
  type: TRADES_PRODUCT
- target: last-mile-delivery
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: copperline-logistics
  type: SELLS_TO
- target: quartz-transport
  type: SELLS_TO
- target: northgate-distribution
  type: SELLS_TO
- target: northgate-distribution
  type: SUPPLIES
- target: redwood-freight
  type: SUPPLIES
- target: lumen-building-supply
  type: INVITED
summary: Granite Logistics — a pending logistics business (trust 48/100, credit BB,
  FICO 684).
tags:
- Company
---

**Granite Logistics** is a pending business in the [[logistics]] sector, headquartered in Atlanta, GA and founded in 1999. Trust score **48/100**, credit rating **BB**, FICO **684**.

## Trade profile
- Industry: Logistics
- Annual revenue: $35,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
