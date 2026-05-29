---
id: trident-wine-imports
label: Trident Wine Imports
node_type: Company
properties:
  annual_revenue_usd: 8000000
  credit_rating: BBB
  employee_count: 30
  fico: 798
  founded_year: 1984
  hq_location: Austin, TX
  status: verified
  trust_score: 71
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: import-export-license
  type: HOLDS_LICENSE
- target: summit-beverage-co
  type: SELLS_TO
- target: meridian-spirits
  type: SELLS_TO
- target: summit-brewing
  type: SUPPLIES
- target: lumen-spirits
  type: SUPPLIES
- target: summit-brewing
  type: COMPETES_WITH
summary: Trident Wine Imports — a verified alcohol & beverage business (trust 71/100,
  credit BBB, FICO 798).
tags:
- Company
---

**Trident Wine Imports** is a verified business in the [[alcohol-beverage]] sector, headquartered in Austin, TX and founded in 1984. Trust score **71/100**, credit rating **BBB**, FICO **798**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $8,000,000
- Employees: 30

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
