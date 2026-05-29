---
id: quartz-industries
label: Quartz Industries
node_type: Company
properties:
  annual_revenue_usd: 120000000
  credit_rating: AA
  employee_count: 140
  fico: 757
  founded_year: 2007
  hq_location: Memphis, TN
  status: verified
  trust_score: 82
relationships:
- target: chemicals
  type: OPERATES_IN
- target: industrial-solvent
  type: TRADES_PRODUCT
- target: polymer-resin
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: hazmat-handling-license
  type: HOLDS_LICENSE
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: cascade-industries
  type: SELLS_TO
- target: tideline-chemical-works
  type: SELLS_TO
summary: Quartz Industries — a verified chemicals business (trust 82/100, credit AA,
  FICO 757).
tags:
- Company
---

**Quartz Industries** is a verified business in the [[chemicals]] sector, headquartered in Memphis, TN and founded in 2007. Trust score **82/100**, credit rating **AA**, FICO **757**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $120,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
