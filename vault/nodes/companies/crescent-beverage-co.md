---
id: crescent-beverage-co
label: Crescent Beverage Co
node_type: Company
properties:
  annual_revenue_usd: 60000000
  credit_rating: AAA
  employee_count: 1100
  fico: 715
  founded_year: 2018
  hq_location: Columbus, OH
  status: verified
  trust_score: 83
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: federal-liquor-permit
  type: HOLDS_LICENSE
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: keystone-spirits
  type: SELLS_TO
- target: sunrise-brewing
  type: SUPPLIES
- target: brightwater-distribution
  type: INVITED
summary: Crescent Beverage Co — a verified alcohol & beverage business (trust 83/100,
  credit AAA, FICO 715).
tags:
- Company
---

**Crescent Beverage Co** is a verified business in the [[alcohol-beverage]] sector, headquartered in Columbus, OH and founded in 2018. Trust score **83/100**, credit rating **AAA**, FICO **715**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $60,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
