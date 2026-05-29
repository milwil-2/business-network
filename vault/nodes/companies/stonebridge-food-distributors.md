---
id: stonebridge-food-distributors
label: Stonebridge Food Distributors
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: BB
  employee_count: 140
  fico: 604
  founded_year: 1984
  hq_location: Spokane, WA
  status: pending
  trust_score: 57
relationships:
- target: food-service
  type: OPERATES_IN
- target: packaged-grains
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: cardinal-food-distributors
  type: SELLS_TO
- target: cardinal-culinary-supply
  type: SELLS_TO
- target: harbor-wholesale-grocers
  type: SUPPLIES
- target: tideline-culinary-supply
  type: SUPPLIES
summary: Stonebridge Food Distributors — a pending food service business (trust 57/100,
  credit BB, FICO 604).
tags:
- Company
---

**Stonebridge Food Distributors** is a pending business in the [[food-service]] sector, headquartered in Spokane, WA and founded in 1984. Trust score **57/100**, credit rating **BB**, FICO **604**.

## Trade profile
- Industry: Food Service
- Annual revenue: $12,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
