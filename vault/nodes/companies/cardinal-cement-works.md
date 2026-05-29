---
id: cardinal-cement-works
label: Cardinal Cement Works
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: AA
  employee_count: 600
  fico: 783
  founded_year: 1994
  hq_location: Denver, CO
  status: verified
  trust_score: 86
relationships:
- target: building-materials
  type: OPERATES_IN
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: import-export-license
  type: HOLDS_LICENSE
- target: trident-building-supply
  type: SELLS_TO
- target: atlas-construction-supply
  type: SUPPLIES
- target: granite-materials
  type: COMPETES_WITH
- target: summit-brewing
  type: PARTNERS_WITH
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: stonebridge-construction-supply
  type: PARTNERS_WITH
- target: cardinal-wine-imports
  type: PARTNERS_WITH
- target: quartz-transport
  type: GAVE_REFERENCE_FOR
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
- target: crescent-building-supply
  type: PARTNERS_WITH
- target: cardinal-food-distributors
  type: INVITED
summary: Cardinal Cement Works — a verified building materials business (trust 86/100,
  credit AA, FICO 783).
tags:
- Company
---

**Cardinal Cement Works** is a verified business in the [[building-materials]] sector, headquartered in Denver, CO and founded in 1994. Trust score **86/100**, credit rating **AA**, FICO **783**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $35,000,000
- Employees: 600

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
