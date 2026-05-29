---
id: brightwater-foods
label: Brightwater Foods
node_type: Company
properties:
  annual_revenue_usd: 2000000
  credit_rating: CC
  employee_count: 140
  fico: 485
  founded_year: 2011
  hq_location: Tacoma, WA
  status: flagged
  trust_score: 20
relationships:
- target: food-service
  type: OPERATES_IN
- target: packaged-grains
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: atlas-wholesale-grocers
  type: SELLS_TO
- target: cardinal-culinary-supply
  type: SUPPLIES
- target: atlas-wholesale-grocers
  type: SUPPLIES
- target: summit-beverage-co
  type: SELLS_TO
- target: revoked-hazmat-license
  type: HOLDS_LICENSE
summary: Brightwater Foods — a flagged food service business (trust 20/100, credit
  CC, FICO 485).
tags:
- Company
---

**Brightwater Foods** is a flagged business in the [[food-service]] sector, headquartered in Tacoma, WA and founded in 2011. Trust score **20/100**, credit rating **CC**, FICO **485**. This profile is **flagged** pending review.

## Trade profile
- Industry: Food Service
- Annual revenue: $2,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
