---
id: cardinal-wine-imports
label: Cardinal Wine Imports
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: AA
  employee_count: 320
  fico: 757
  founded_year: 2019
  hq_location: Tampa, FL
  status: verified
  trust_score: 76
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: craft-lager
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: crescent-beverage-co
  type: SELLS_TO
- target: summit-brewing
  type: SELLS_TO
- target: summit-beverage-co
  type: SUPPLIES
- target: stonebridge-spirits
  type: SUPPLIES
- target: cascade-spirits
  type: SUPPLIES
- target: summit-beverage-co
  type: COMPETES_WITH
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: stonebridge-construction-supply
  type: PARTNERS_WITH
- target: vertex-solvents
  type: PARTNERS_WITH
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
- target: falcon-wholesale-grocers
  type: GAVE_REFERENCE_FOR
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
summary: Cardinal Wine Imports — a verified alcohol & beverage business (trust 76/100,
  credit AA, FICO 757).
tags:
- Company
---

**Cardinal Wine Imports** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tampa, FL and founded in 2019. Trust score **76/100**, credit rating **AA**, FICO **757**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $12,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
