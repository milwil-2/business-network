---
id: trident-culinary-supply
label: Trident Culinary Supply
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: AAA
  employee_count: 75
  fico: 773
  founded_year: 1974
  hq_location: Fresno, CA
  status: verified
  trust_score: 69
relationships:
- target: food-service
  type: OPERATES_IN
- target: frozen-produce
  type: TRADES_PRODUCT
- target: packaged-grains
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: cardinal-culinary-supply
  type: SELLS_TO
- target: highland-culinary-supply
  type: SUPPLIES
- target: atlas-wholesale-grocers
  type: SUPPLIES
- target: cardinal-culinary-supply
  type: SUPPLIES
- target: atlas-wholesale-grocers
  type: INVITED
summary: Trident Culinary Supply — a verified food service business (trust 69/100,
  credit AAA, FICO 773).
tags:
- Company
---

**Trident Culinary Supply** is a verified business in the [[food-service]] sector, headquartered in Fresno, CA and founded in 1974. Trust score **69/100**, credit rating **AAA**, FICO **773**.

## Trade profile
- Industry: Food Service
- Annual revenue: $12,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
