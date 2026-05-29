---
id: falcon-wholesale-grocers
label: Falcon Wholesale Grocers
node_type: Company
properties:
  annual_revenue_usd: 8000000
  credit_rating: AA
  employee_count: 320
  fico: 707
  founded_year: 2014
  hq_location: Newark, NJ
  status: verified
  trust_score: 98
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
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: cardinal-food-distributors
  type: SELLS_TO
- target: atlas-wholesale-grocers
  type: SUPPLIES
- target: summit-brewing
  type: GAVE_REFERENCE_FOR
- target: summit-brewing
  type: PARTNERS_WITH
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: vertex-solvents
  type: GAVE_REFERENCE_FOR
- target: cardinal-wine-imports
  type: GAVE_REFERENCE_FOR
- target: quartz-transport
  type: GAVE_REFERENCE_FOR
- target: quartz-transport
  type: PARTNERS_WITH
- target: crescent-building-supply
  type: PARTNERS_WITH
summary: Falcon Wholesale Grocers — a verified food service business (trust 98/100,
  credit AA, FICO 707).
tags:
- Company
---

**Falcon Wholesale Grocers** is a verified business in the [[food-service]] sector, headquartered in Newark, NJ and founded in 2014. Trust score **98/100**, credit rating **AA**, FICO **707**.

## Trade profile
- Industry: Food Service
- Annual revenue: $8,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
