---
id: meridian-spirits
label: Meridian Spirits
node_type: Company
properties:
  annual_revenue_usd: 120000000
  credit_rating: A
  employee_count: 1100
  fico: 723
  founded_year: 1992
  hq_location: Tulsa, OK
  status: verified
  trust_score: 74
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: bourbon-whiskey
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: contractor-license
  type: HOLDS_LICENSE
- target: keystone-spirits
  type: SELLS_TO
- target: cascade-spirits
  type: SELLS_TO
- target: cardinal-wine-imports
  type: SELLS_TO
- target: lumen-spirits
  type: SUPPLIES
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
- target: northgate-distribution
  type: SUBSIDIARY_OF
summary: Meridian Spirits — a verified alcohol & beverage business (trust 74/100,
  credit A, FICO 723).
tags:
- Company
---

**Meridian Spirits** is a verified business in the [[alcohol-beverage]] sector, headquartered in Tulsa, OK and founded in 1992. Trust score **74/100**, credit rating **A**, FICO **723**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $120,000,000
- Employees: 1100

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
