---
id: data-100
label: "Data 100: Principles and Techniques of Data Science"
node_type: Course
tags: [data-science, machine-learning, Course]
summary: "An intermediate data science course covering the full data lifecycle: wrangling, exploratory analysis, modeling, and inference at scale."
properties:
  number: "Data 100"
  department: "Data Science"
  units: 4
relationships:
  - type: PREREQUISITE_OF
    target: cs-189
  - type: COVERS
    target: linear-regression
  - type: COVERS
    target: gradient-descent
  - type: COVERS
    target: overfitting
---

Data 100 deepens the foundations from Data 8 into the principles and techniques of practical data science. Students work through the full lifecycle: data cleaning with pandas, SQL queries, exploratory analysis, visualization, and feature engineering.

The modeling half develops [[linear-regression]] and logistic regression with the loss-minimization view, fit using [[gradient-descent]], and introduces regularization and cross-validation to manage [[overfitting]]. Linear algebra and calculus are used to formalize the methods.

Building on both [[data-8]] and [[cs-88]], Data 100 is the prerequisite that prepares students for the rigorous treatment in [[cs-189]].
