---
id: stonebridge-spirits
label: Stonebridge Spirits
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: BBB
  employee_count: 30
  fico: 785
  founded_year: 2000
  hq_location: Tacoma, WA
  status: verified
  trust_score: 74
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: crescent-beverage-co
  type: SELLS_TO
- target: meridian-spirits
  type: SELLS_TO
- target: lumen-spirits
  type: SUPPLIES
summary: Stonebridge Spirits — a verified alcohol & beverage business (trust 74/100,
  credit BBB, FICO 785).
tags:
- Company
---

**Stonebridge Spirits** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tacoma, WA and founded in 2000. Trust score **74/100**, credit rating **BBB**, FICO **785**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $250,000,000
- Employees: 30

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
