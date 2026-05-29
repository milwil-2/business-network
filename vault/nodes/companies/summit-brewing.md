---
id: summit-brewing
label: Summit Brewing
node_type: Company
properties:
  annual_revenue_usd: 250000000
  credit_rating: AAA
  employee_count: 600
  fico: 819
  founded_year: 1984
  hq_location: Memphis, TN
  status: verified
  trust_score: 79
relationships:
- target: alcohol-beverage
  type: OPERATES_IN
- target: sparkling-wine
  type: TRADES_PRODUCT
- target: craft-lager
  type: TRADES_PRODUCT
- target: equifax-business
  type: RATED_BY
- target: food-handler-permit
  type: HOLDS_LICENSE
- target: contractor-license
  type: HOLDS_LICENSE
- target: crescent-beverage-co
  type: SELLS_TO
- target: summit-beverage-co
  type: SUPPLIES
- target: cardinal-cement-works
  type: GAVE_REFERENCE_FOR
- target: quartz-transport
  type: GAVE_REFERENCE_FOR
- target: quartz-transport
  type: PARTNERS_WITH
- target: falcon-wholesale-grocers
  type: PARTNERS_WITH
- target: crescent-building-supply
  type: GAVE_REFERENCE_FOR
summary: Summit Brewing — a verified alcohol & beverage business (trust 79/100, credit
  AAA, FICO 819).
tags:
- Company
---

**Summit Brewing** is a verified business in the [[alcohol-beverage]] sector, headquartered in Memphis, TN and founded in 1984. Trust score **79/100**, credit rating **AAA**, FICO **819**.

## Trade profile
- Industry: Alcohol & Beverage
- Annual revenue: $250,000,000
- Employees: 600

Trade relationships are modeled as SELLS_TO / SUPPLIES edges; creditworthiness is asserted via RATED_BY a credit bureau.
