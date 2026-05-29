---
id: harbor-wholesale-grocers
label: Harbor Wholesale Grocers
node_type: Company
properties:
  annual_revenue_usd: 2000000
  credit_rating: A
  employee_count: 12
  fico: 738
  founded_year: 2017
  hq_location: Atlanta, GA
  status: verified
  trust_score: 90
relationships:
- target: food-service
  type: OPERATES_IN
- target: frozen-produce
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: import-export-license
  type: HOLDS_LICENSE
- target: highland-culinary-supply
  type: SELLS_TO
- target: copperline-food-distributors
  type: SELLS_TO
- target: vertex-polymers
  type: SUBSIDIARY_OF
summary: Harbor Wholesale Grocers — a verified food service business (trust 90/100,
  credit A, FICO 738).
tags:
- Company
---

**Harbor Wholesale Grocers** is a verified business in the [[food-service]] sector, headquartered in Atlanta, GA and founded in 2017. Trust score **90/100**, credit rating **A**, FICO **738**.

## Trade profile
- Industry: Food Service
- Annual revenue: $2,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
