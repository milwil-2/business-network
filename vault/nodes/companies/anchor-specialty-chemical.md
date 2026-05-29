---
id: anchor-specialty-chemical
label: Anchor Specialty Chemical
node_type: Company
properties:
  annual_revenue_usd: 8000000
  credit_rating: AAA
  employee_count: 12
  fico: 704
  founded_year: 1976
  hq_location: Reno, NV
  status: verified
  trust_score: 67
relationships:
- target: chemicals
  type: OPERATES_IN
- target: industrial-solvent
  type: TRADES_PRODUCT
- target: dun-bradstreet
  type: RATED_BY
- target: motor-carrier-authority
  type: HOLDS_LICENSE
- target: vertex-polymers
  type: SELLS_TO
- target: quartz-industries
  type: SELLS_TO
- target: cascade-industries
  type: SELLS_TO
summary: Anchor Specialty Chemical — a verified chemicals business (trust 67/100,
  credit AAA, FICO 704).
tags:
- Company
---

**Anchor Specialty Chemical** is a verified business in the [[chemicals]] sector, headquartered in Reno, NV and founded in 1976. Trust score **67/100**, credit rating **AAA**, FICO **704**.

## Trade profile
- Industry: Chemicals
- Annual revenue: $8,000,000
- Employees: 12

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
