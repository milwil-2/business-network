---
id: gradient-descent
label: Gradient Descent
node_type: Concept
tags: [optimization, machine-learning, Concept]
summary: "An iterative optimization algorithm that minimizes a function by repeatedly stepping in the direction of the negative gradient."
relationships:
  - type: RELATED_TO
    target: linear-regression
---

Gradient descent minimizes a differentiable loss function by computing its gradient — the direction of steepest increase — and taking a step in the opposite direction. The step size is controlled by the **learning rate**, which trades off speed of convergence against the risk of overshooting.

Several variants exist. *Batch* gradient descent uses the entire dataset per step; *stochastic* gradient descent (SGD) uses a single sample; and *mini-batch* descent strikes a balance and is the workhorse of modern machine learning. Momentum, RMSProp, and Adam adapt the update to accelerate convergence on ill-conditioned surfaces.

It is the engine behind training [[linear-regression]], logistic regression, and especially deep [[neural-network]] models, where backpropagation supplies the gradients. A learning rate that is too large diverges, while one too small crawls — tuning it is a central practical concern.
