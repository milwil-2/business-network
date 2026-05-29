---
id: cardinal-transport
label: Cardinal Transport
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: B
  employee_count: 140
  fico: 627
  founded_year: 1985
  hq_location: Boise, ID
  status: pending
  trust_score: 47
relationships:
- target: logistics
  type: OPERATES_IN
- target: cold-storage
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: harbor-freight
  type: SELLS_TO
- target: northgate-distribution
  type: SELLS_TO
- target: beacon-transport
  type: SELLS_TO
- target: anchor-distribution
  type: SUPPLIES
- target: quartz-transport
  type: SUPPLIES
summary: Cardinal Transport — a pending logistics business (trust 47/100, credit B,
  FICO 627).
tags:
- Company
---

**Cardinal Transport** is a pending business in the [[logistics]] sector, headquartered in Boise, ID and founded in 1985. Trust score **47/100**, credit rating **B**, FICO **627**.

## Trade profile
- Industry: Logistics
- Annual revenue: $35,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
