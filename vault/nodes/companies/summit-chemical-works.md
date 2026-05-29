---
id: summit-chemical-works
label: Summit Chemical Works
node_type: Company
properties:
  annual_revenue_usd: 60000000
  credit_rating: CC
  employee_count: 140
  fico: 489
  founded_year: 2010
  hq_location: Tacoma, WA
  status: flagged
  trust_score: 11
relationships:
- target: chemicals
  type: OPERATES_IN
- target: polymer-resin
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: trident-polymers
  type: SELLS_TO
- target: atlas-chemical-works
  type: SUPPLIES
- target: trident-polymers
  type: SUPPLIES
- target: anchor-specialty-chemical
  type: COMPETES_WITH
- target: meridian-building-supply
  type: SELLS_TO
- target: revoked-hazmat-license
  type: HOLDS_LICENSE
summary: Summit Chemical Works — a flagged chemicals business (trust 11/100, credit
  CC, FICO 489).
tags:
- Company
---

**Summit Chemical Works** is a flagged business in the [[chemicals]] sector, headquartered in Tacoma, WA and founded in 2010. Trust score **11/100**, credit rating **CC**, FICO **489**. This profile is **flagged** pending review.

## Trade profile
- Industry: Chemicals
- Annual revenue: $60,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
