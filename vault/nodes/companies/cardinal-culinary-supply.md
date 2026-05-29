---
id: cardinal-culinary-supply
label: Cardinal Culinary Supply
node_type: Company
properties:
  annual_revenue_usd: 5000000
  credit_rating: AAA
  employee_count: 320
  fico: 754
  founded_year: 2015
  hq_location: Tulsa, OK
  status: verified
  trust_score: 76
relationships:
- target: food-service
  type: OPERATES_IN
- target: packaged-grains
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: highland-culinary-supply
  type: SELLS_TO
- target: harbor-wholesale-grocers
  type: SUPPLIES
- target: falcon-wholesale-grocers
  type: SUPPLIES
- target: falcon-wholesale-grocers
  type: GAVE_REFERENCE_FOR
summary: Cardinal Culinary Supply — a verified food service business (trust 76/100,
  credit AAA, FICO 754).
tags:
- Company
---

**Cardinal Culinary Supply** is a verified business in the [[food-service]] sector, headquartered in Tulsa, OK and founded in 2015. Trust score **76/100**, credit rating **AAA**, FICO **754**.

## Trade profile
- Industry: Food Service
- Annual revenue: $5,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
