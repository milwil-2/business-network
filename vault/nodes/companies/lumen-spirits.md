---
id: lumen-spirits
label: Lumen Spirits
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: AAA
  employee_count: 1100
  fico: 753
  founded_year: 2007
  hq_location: Tulsa, OK
  status: verified
  trust_score: 68
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: craft-lager
  type: TRADES_PRODUCT
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: contractor-license
  type: HOLDS_LICENSE
- target: sunrise-brewing
  type: SELLS_TO
- target: trident-wine-imports
  type: SELLS_TO
- target: meridian-spirits
  type: SELLS_TO
- target: cascade-spirits
  type: SUPPLIES
- target: sunrise-brewing
  type: COMPETES_WITH
summary: Lumen Spirits — a verified alcohol & beverage business (trust 68/100, credit
  AAA, FICO 753).
tags:
- Company
---

**Lumen Spirits** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tulsa, OK and founded in 2007. Trust score **68/100**, credit rating **AAA**, FICO **753**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $35,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
