---
id: trident-polymers
label: Trident Polymers
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: BBB
  employee_count: 12
  fico: 630
  founded_year: 2008
  hq_location: Tacoma, WA
  status: pending
  trust_score: 54
relationships:
- target: chemicals
  type: OPERATES_IN
- target: sodium-hydroxide
  type: TRADES_PRODUCT
- target: polymer-resin
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: tideline-chemical-works
  type: SELLS_TO
- target: summit-chemical-works
  type: SELLS_TO
- target: vertex-polymers
  type: SELLS_TO
- target: tideline-chemical-works
  type: SUPPLIES
summary: Trident Polymers — a pending chemicals business (trust 54/100, credit BBB,
  FICO 630).
tags:
- Company
---

**Trident Polymers** is a pending business in the [[chemicals]] sector, headquartered in Tacoma, WA and founded in 2008. Trust score **54/100**, credit rating **BBB**, FICO **630**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $12,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
