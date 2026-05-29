---
id: trident-building-supply
label: Trident Building Supply
node_type: Company
properties:
  annual_revenue_usd: 5000000
  credit_rating: AAA
  employee_count: 320
  fico: 807
  founded_year: 2006
  hq_location: Denver, CO
  status: verified
  trust_score: 62
relationships:
- target: building-materials
  type: OPERATES_IN
- target: dimensional-lumber
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: sterling-construction-supply
  type: SELLS_TO
- target: cardinal-cement-works
  type: SUPPLIES
- target: stonebridge-construction-supply
  type: GAVE_REFERENCE_FOR
summary: Trident Building Supply — a verified building materials business (trust 62/100,
  credit AAA, FICO 807).
tags:
- Company
---

**Trident Building Supply** is a verified business in the [[building-materials]] sector, headquartered in Denver, CO and founded in 2006. Trust score **62/100**, credit rating **AAA**, FICO **807**.

## Trade profile
- Industry: Building Materials
- Annual revenue: $5,000,000
- Employees: 320

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
