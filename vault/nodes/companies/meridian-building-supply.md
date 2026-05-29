---
id: meridian-building-supply
label: Meridian Building Supply
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: CC
  employee_count: 600
  fico: 472
  founded_year: 1972
  hq_location: Tacoma, WA
  status: flagged
  trust_score: 18
relationships:
- target: building-materials
  type: OPERATES_IN
- target: steel-rebar
  type: TRADES_PRODUCT
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: lumen-building-supply
  type: SELLS_TO
- target: brightwater-construction-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SELLS_TO
- target: stonebridge-construction-supply
  type: SUPPLIES
- target: trident-building-supply
  type: SUPPLIES
- target: brightwater-construction-supply
  type: COMPETES_WITH
- target: brightwater-foods
  type: SELLS_TO
- target: lapsed-liquor-permit
  type: HOLDS_LICENSE
summary: Meridian Building Supply — a flagged building materials business (trust 18/100,
  credit CC, FICO 472).
tags:
- Company
---

**Meridian Building Supply** is a flagged business in the [[building-materials]] sector, headquartered in Tacoma, WA and founded in 1972. Trust score **18/100**, credit rating **CC**, FICO **472**. This profile is **flagged** pending review.

## Trade profile
- Industry: Building Materials
- Annual revenue: $12,000,000
- Employees: 600

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
