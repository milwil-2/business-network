---
id: quartz-transport
label: Quartz Transport
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: AAA
  employee_count: 140
  fico: 777
  founded_year: 1999
  hq_location: Oakland, CA
  status: verified
  trust_score: 96
relationships:
- target: logistics
  type: OPERATES_IN
- target: freight-services
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: redwood-freight
  type: SELLS_TO
- target: copperline-logistics
  type: SELLS_TO
- target: vertex-transport
  type: SUPPLIES
- target: summit-brewing
  type: GAVE_REFERENCE_FOR
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: vertex-solvents
  type: GAVE_REFERENCE_FOR
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
- target: cardinal-wine-imports
  type: PARTNERS_WITH
- target: trident-building-supply
  type: INVITED
summary: Quartz Transport — a verified logistics business (trust 96/100, credit AAA,
  FICO 777).
tags:
- Company
---

**Quartz Transport** is a verified business in the [[logistics]] sector, headquartered in Oakland, CA and founded in 1999. Trust score **96/100**, credit rating **AAA**, FICO **777**.

## Trade profile
- Industry: Logistics
- Annual revenue: $20,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
