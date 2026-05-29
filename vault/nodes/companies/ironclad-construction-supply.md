---
id: ironclad-construction-supply
label: Ironclad Construction Supply
node_type: Company
properties:
  annual_revenue_usd: 2000000
  credit_rating: A
  employee_count: 140
  fico: 705
  founded_year: 1975
  hq_location: Reno, NV
  status: verified
  trust_score: 85
relationships:
- target: building-materials
  type: OPERATES_IN
- target: steel-rebar
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: trident-building-supply
  type: SELLS_TO
- target: stonebridge-construction-supply
  type: SELLS_TO
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
- target: summit-beverage-co
  type: SUBSIDIARY_OF
summary: Ironclad Construction Supply — a verified building materials business (trust
  85/100, credit A, FICO 705).
tags:
- Company
---

**Ironclad Construction Supply** is a verified business in the [[building-materials]] sector, headquartered in Reno, NV and founded in 1975. Trust score **85/100**, credit rating **A**, FICO **705**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $2,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
