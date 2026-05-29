---
id: atlas-construction-supply
label: Atlas Construction Supply
node_type: Company
properties:
  annual_revenue_usd: 12000000
  credit_rating: A
  employee_count: 140
  fico: 792
  founded_year: 1980
  hq_location: Tampa, FL
  status: verified
  trust_score: 75
relationships:
- target: building-materials
  type: OPERATES_IN
- target: portland-cement
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: meridian-building-supply
  type: SELLS_TO
- target: crescent-building-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SELLS_TO
- target: granite-materials
  type: SUPPLIES
- target: trident-building-supply
  type: COMPETES_WITH
- target: cardinal-wine-imports
  type: GAVE_REFERENCE_FOR
- target: vertex-transport
  type: SUBSIDIARY_OF
summary: Atlas Construction Supply — a verified building materials business (trust
  75/100, credit A, FICO 792).
tags:
- Company
---

**Atlas Construction Supply** is a verified business in the [[building-materials]] sector, headquartered in Tampa, FL and founded in 1980. Trust score **75/100**, credit rating **A**, FICO **792**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $12,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
