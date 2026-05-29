---
id: crescent-building-supply
label: Crescent Building Supply
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: AA
  employee_count: 140
  fico: 739
  founded_year: 2000
  hq_location: Oakland, CA
  status: verified
  trust_score: 79
relationships:
- target: building-materials
  type: OPERATES_IN
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: steel-rebar
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: lumen-building-supply
  type: SELLS_TO
- target: trident-building-supply
  type: SUPPLIES
- target: lumen-building-supply
  type: COMPETES_WITH
- target: summit-brewing
  type: PARTNERS_WITH
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
- target: vertex-solvents
  type: GAVE_REFERENCE_FOR
- target: vertex-solvents
  type: PARTNERS_WITH
- target: cardinal-cement-works
  type: PARTNERS_WITH
- target: cardinal-wine-imports
  type: PARTNERS_WITH
- target: quartz-transport
  type: GAVE_REFERENCE_FOR
- target: quartz-transport
  type: PARTNERS_WITH
- target: falcon-wholesale-grocers
  type: GAVE_REFERENCE_FOR
summary: Crescent Building Supply — a verified building materials business (trust
  79/100, credit AA, FICO 739).
tags:
- Company
---

**Crescent Building Supply** is a verified business in the [[building-materials]] sector, headquartered in Oakland, CA and founded in 2000. Trust score **79/100**, credit rating **AA**, FICO **739**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $250,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
