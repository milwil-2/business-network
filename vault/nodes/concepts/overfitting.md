---
id: overfitting
label: Overfitting
node_type: Concept
tags: [machine-learning, generalization, Concept]
summary: "When a model fits the noise in its training data so closely that it generalizes poorly to unseen data."
relationships:
  - type: RELATED_TO
    target: linear-regression
  - type: RELATED_TO
    target: neural-network
---

Overfitting occurs when a model captures not just the underlying signal in its training data but also its random noise. The result is excellent training accuracy but poor performance on new data — the model fails to **generalize**. Its mirror image is *underfitting*, where the model is too simple to capture the signal.

Overfitting is a symptom of high variance and is governed by the **bias-variance tradeoff**. Detection relies on a gap between training and validation error, typically measured with held-out data and cross-validation. Overly flexible models — high-degree polynomials in [[linear-regression]] or large [[neural-network]] architectures — are the usual culprits.

Mitigations include gathering more data, reducing model complexity, regularization (L1/L2 penalties, dropout), early stopping, and data augmentation. The goal is always a model complex enough to fit the signal but constrained enough to ignore the noise.
