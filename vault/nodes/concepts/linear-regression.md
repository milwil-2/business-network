---
id: linear-regression
label: Linear Regression
node_type: Concept
tags: [machine-learning, statistics, Concept]
summary: "A model that predicts a continuous outcome as a linear combination of input features by minimizing squared error."
relationships:
  - type: RELATED_TO
    target: gradient-descent
  - type: RELATED_TO
    target: hypothesis-testing
---

Linear regression models a continuous target *y* as a weighted sum of input features plus an intercept: y = w·x + b. Fitting the model means choosing weights that minimize a loss, almost always the **mean squared error** between predictions and observed values.

The optimal weights can be found in closed form via the normal equations (ordinary least squares) or iteratively with [[gradient-descent]] when the dataset is large. Each coefficient estimates the marginal effect of a feature, and its statistical significance is assessed using [[hypothesis-testing]].

Linear regression is the foundational supervised-learning model: simple, interpretable, and the basis for richer variants like ridge, lasso, and logistic regression. Its assumptions — linearity, independence, and homoscedastic errors — must be checked, and adding too many features can lead to [[overfitting]].
