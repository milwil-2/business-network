---
id: sterling-construction-supply
label: Sterling Construction Supply
node_type: Company
properties:
  annual_revenue_usd: 8000000
  credit_rating: AA
  employee_count: 140
  fico: 729
  founded_year: 1983
  hq_location: Tulsa, OK
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
- target: granite-materials
  type: SELLS_TO
- target: ironclad-construction-supply
  type: SELLS_TO
- target: brightwater-construction-supply
  type: SELLS_TO
- target: stonebridge-construction-supply
  type: SUPPLIES
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: stonebridge-spirits
  type: INVITED
summary: Sterling Construction Supply — a verified building materials business (trust
  85/100, credit AA, FICO 729).
tags:
- Company
---

**Sterling Construction Supply** is a verified business in the [[building-materials]] sector, headquartered in Tulsa, OK and founded in 1983. Trust score **85/100**, credit rating **AA**, FICO **729**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $8,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
