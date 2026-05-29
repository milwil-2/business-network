---
id: tideline-culinary-supply
label: Tideline Culinary Supply
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: AAA
  employee_count: 140
  fico: 693
  founded_year: 1982
  hq_location: Atlanta, GA
  status: verified
  trust_score: 88
relationships:
- target: food-service
  type: OPERATES_IN
- target: frozen-produce
  type: TRADES_PRODUCT
- target: cooking-oil
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: highland-culinary-supply
  type: SELLS_TO
- target: copperline-food-distributors
  type: SELLS_TO
- target: highland-culinary-supply
  type: SUPPLIES
summary: Tideline Culinary Supply — a verified food service business (trust 88/100,
  credit AAA, FICO 693).
tags:
- Company
---

**Tideline Culinary Supply** is a verified business in the [[food-service]] sector, headquartered in Atlanta, GA and founded in 1982. Trust score **88/100**, credit rating **AAA**, FICO **693**.

## Trade profile
- Industry: Food Service
- Annual revenue: $12,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
