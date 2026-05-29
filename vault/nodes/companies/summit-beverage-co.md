---
id: summit-beverage-co
label: Summit Beverage Co
node_type: Company
properties:
  annual_revenue_usd: 5000000
  credit_rating: C
  employee_count: 12
  fico: 499
  founded_year: 1986
  hq_location: Spokane, WA
  status: flagged
  trust_score: 29
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: experian-business
  type: RATED_BY
- target: crescent-beverage-co
  type: SELLS_TO
- target: cardinal-wine-imports
  type: SUPPLIES
- target: atlas-chemical-works
  type: SUBSIDIARY_OF
- target: summit-chemical-works
  type: SELLS_TO
- target: revoked-hazmat-license
  type: HOLDS_LICENSE
summary: Summit Beverage Co — a flagged alcohol & beverage business (trust 29/100,
  credit C, FICO 499).
tags:
- Company
---

**Summit Beverage Co** is a flagged business in the [[alcohol-beverage]] sector, headquartered in Spokane, WA and founded in 1986. Trust score **29/100**, credit rating **C**, FICO **499**. This profile is **flagged** pending review.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $5,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
