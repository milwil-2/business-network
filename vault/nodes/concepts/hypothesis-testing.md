---
id: hypothesis-testing
label: Hypothesis Testing
node_type: Concept
tags: [statistics, inference, Concept]
summary: "A statistical procedure for deciding whether observed data provides enough evidence to reject a null hypothesis about a population."
relationships:
  - type: RELATED_TO
    target: linear-regression
---

Hypothesis testing is a framework for drawing conclusions about a population from a sample. It begins with a **null hypothesis** (a default claim of no effect) and an **alternative hypothesis**, then asks how surprising the observed data would be if the null were true.

The surprise is quantified by a **p-value**: the probability of seeing a test statistic at least as extreme as the observed one under the null. If the p-value falls below a chosen significance level (often 0.05), the null is rejected. Permutation tests and bootstrap methods let us compute these probabilities by simulation rather than relying on closed-form distributions.

Care is needed to avoid pitfalls: Type I errors (false positives), Type II errors (false negatives), and multiple-comparison inflation. Hypothesis testing underpins A/B experiments and is closely tied to confidence intervals and [[linear-regression]] coefficient significance.
