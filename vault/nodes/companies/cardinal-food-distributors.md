---
id: cardinal-food-distributors
label: Cardinal Food Distributors
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: B
  employee_count: 140
  fico: 644
  founded_year: 1974
  hq_location: Memphis, TN
  status: pending
  trust_score: 56
relationships:
- target: food-service
  type: OPERATES_IN
- target: packaged-grains
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: copperline-food-distributors
  type: SELLS_TO
- target: cardinal-culinary-supply
  type: SELLS_TO
- target: trident-culinary-supply
  type: SELLS_TO
- target: tideline-culinary-supply
  type: SUPPLIES
- target: copperline-food-distributors
  type: SUPPLIES
- target: trident-culinary-supply
  type: SUPPLIES
- target: highland-culinary-supply
  type: COMPETES_WITH
summary: Cardinal Food Distributors — a pending food service business (trust 56/100,
  credit B, FICO 644).
tags:
- Company
---

**Cardinal Food Distributors** is a pending business in the [[food-service]] sector, headquartered in Memphis, TN and founded in 1974. Trust score **56/100**, credit rating **B**, FICO **644**.

## Trade profile
- Industry: Food Service
- Annual revenue: $20,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
