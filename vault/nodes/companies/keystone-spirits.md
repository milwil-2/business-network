---
id: keystone-spirits
label: Keystone Spirits
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: A
  employee_count: 140
  fico: 707
  founded_year: 2013
  hq_location: Tampa, FL
  status: verified
  trust_score: 89
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: import-export-license
  type: HOLDS_LICENSE
- target: meridian-spirits
  type: SELLS_TO
- target: summit-brewing
  type: SELLS_TO
- target: cardinal-wine-imports
  type: SELLS_TO
- target: cardinal-wine-imports
  type: SUPPLIES
summary: Keystone Spirits — a verified alcohol & beverage business (trust 89/100,
  credit A, FICO 707).
tags:
- Company
---

**Keystone Spirits** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tampa, FL and founded in 2013. Trust score **89/100**, credit rating **A**, FICO **707**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $35,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
