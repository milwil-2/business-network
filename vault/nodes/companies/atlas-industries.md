---
id: atlas-industries
label: Atlas Industries
node_type: Company
properties:
  annual_revenue_usd: 35000000
  credit_rating: AA
  employee_count: 140
  fico: 707
  founded_year: 1990
  hq_location: Oakland, CA
  status: verified
  trust_score: 73
relationships:
- target: chemicals
  type: OPERATES_IN
- target: polymer-resin
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: contractor-license
  type: HOLDS_LICENSE
- target: atlas-chemical-works
  type: SELLS_TO
- target: atlas-chemical-works
  type: SUPPLIES
- target: vertex-solvents
  type: GAVE_REFERENCE_FOR
- target: crescent-beverage-co
  type: SUBSIDIARY_OF
summary: Atlas Industries — a verified chemicals business (trust 73/100, credit AA,
  FICO 707).
tags:
- Company
---

**Atlas Industries** is a verified business in the [[chemicals]] sector, headquartered in Oakland, CA and founded in 1990. Trust score **73/100**, credit rating **AA**, FICO **707**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $35,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
