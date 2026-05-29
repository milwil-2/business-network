---
id: cascade-spirits
label: Cascade Spirits
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: AAA
  employee_count: 320
  fico: 735
  founded_year: 2012
  hq_location: Tampa, FL
  status: verified
  trust_score: 78
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: crescent-beverage-co
  type: SELLS_TO
- target: sunrise-brewing
  type: SELLS_TO
- target: stonebridge-spirits
  type: SUPPLIES
summary: Cascade Spirits — a verified alcohol & beverage business (trust 78/100, credit
  AAA, FICO 735).
tags:
- Company
---

**Cascade Spirits** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tampa, FL and founded in 2012. Trust score **78/100**, credit rating **AAA**, FICO **735**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $20,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
