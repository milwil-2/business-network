---
id: sunrise-brewing
label: Sunrise Brewing
node_type: Company
properties:
  annual_revenue_usd: 20000000
  credit_rating: AA
  employee_count: 75
  fico: 777
  founded_year: 2004
  hq_location: Newark, NJ
  status: verified
  trust_score: 84
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: trident-wine-imports
  type: SELLS_TO
- target: ironclad-construction-supply
  type: INVITED
summary: Sunrise Brewing — a verified alcohol & beverage business (trust 84/100, credit
  AA, FICO 777).
tags:
- Company
---

**Sunrise Brewing** is a verified business in the [[alcohol-beverage]] sector, headquartered in Newark, NJ and founded in 2004. Trust score **84/100**, credit rating **AA**, FICO **777**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $20,000,000
- Employees: 75

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
