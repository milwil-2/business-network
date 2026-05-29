---
id: stonebridge-construction-supply
label: Stonebridge Construction Supply
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: BBB
  employee_count: 1100
  fico: 746
  founded_year: 1972
  hq_location: Fresno, CA
  status: verified
  trust_score: 85
relationships:
- target: building-materials
  type: OPERATES_IN
- target: steel-rebar
  type: TRADES_PRODUCT
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: sterling-construction-supply
  type: SELLS_TO
- target: granite-materials
  type: SELLS_TO
- target: crescent-building-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SUPPLIES
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
- target: cardinal-wine-imports
  type: GAVE_REFERENCE_FOR
- target: falcon-wholesale-grocers
  type: GAVE_REFERENCE_FOR
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
summary: Stonebridge Construction Supply — a verified building materials business
  (trust 85/100, credit BBB, FICO 746).
tags:
- Company
---

**Stonebridge Construction Supply** is a verified business in the [[building-materials]] sector, headquartered in Fresno, CA and founded in 1972. Trust score **85/100**, credit rating **BBB**, FICO **746**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $20,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
