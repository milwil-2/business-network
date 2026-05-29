---
id: beacon-transport
label: Beacon Transport
node_type: Company
properties:
  annual_revenue_usd: 2000000
  credit_rating: AA
  employee_count: 140
  fico: 748
  founded_year: 2014
  hq_location: Denver, CO
  status: verified
  trust_score: 88
relationships:
- target: logistics
  type: OPERATES_IN
- target: cold-storage
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: import-export-license
  type: HOLDS_LICENSE
- target: state-alcohol-license
  type: HOLDS_LICENSE
- target: harbor-freight
  type: SELLS_TO
- target: stonebridge-construction-supply
  type: SUBSIDIARY_OF
summary: Beacon Transport — a verified logistics business (trust 88/100, credit AA,
  FICO 748).
tags:
- Company
---

**Beacon Transport** is a verified business in the [[logistics]] sector, headquartered in Denver, CO and founded in 2014. Trust score **88/100**, credit rating **AA**, FICO **748**.

## Trade profile
- Industry: Logistics
- Annual revenue: $2,000,000
- Employees: 140

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
