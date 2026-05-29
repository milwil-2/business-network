---
id: atlas-wholesale-grocers
label: Atlas Wholesale Grocers
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: BBB
  employee_count: 140
  fico: 723
  founded_year: 2002
  hq_location: Fresno, CA
  status: verified
  trust_score: 68
relationships:
- target: food-service
  type: OPERATES_IN
- target: packaged-grains
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: contractor-license
  type: HOLDS_LICENSE
- target: harbor-wholesale-grocers
  type: SELLS_TO
- target: cardinal-food-distributors
  type: SUPPLIES
- target: tideline-culinary-supply
  type: SUPPLIES
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
- target: cardinal-transport
  type: SUBSIDIARY_OF
summary: Atlas Wholesale Grocers — a verified food service business (trust 68/100,
  credit BBB, FICO 723).
tags:
- Company
---

**Atlas Wholesale Grocers** is a verified business in the [[food-service]] sector, headquartered in Fresno, CA and founded in 2002. Trust score **68/100**, credit rating **BBB**, FICO **723**.

## Trade profile
- Industry: Food Service
- Annual revenue: $12,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
