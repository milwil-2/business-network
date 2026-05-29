---
id: copperline-food-distributors
label: Copperline Food Distributors
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: AA
  employee_count: 75
  fico: 709
  founded_year: 1974
  hq_location: Spokane, WA
  status: verified
  trust_score: 65
relationships:
- target: food-service
  type: OPERATES_IN
- target: cooking-oil
  type: TRADES_PRODUCT
- target: frozen-produce
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: atlas-wholesale-grocers
  type: SELLS_TO
- target: highland-culinary-supply
  type: SELLS_TO
- target: cardinal-wine-imports
  type: GAVE_REFERENCE_FOR
summary: Copperline Food Distributors — a verified food service business (trust 65/100,
  credit AA, FICO 709).
tags:
- Company
---

**Copperline Food Distributors** is a verified business in the [[food-service]] sector, headquartered in Spokane, WA and founded in 1974. Trust score **65/100**, credit rating **AA**, FICO **709**.

## Trade profile
- Industry: Food Service
- Annual revenue: $250,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
