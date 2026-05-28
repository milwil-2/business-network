---
id: k-means-clustering
label: K-Means Clustering
node_type: Concept
tags: [machine-learning, unsupervised, Concept]
summary: "An unsupervised algorithm that partitions data into k clusters by iteratively assigning points to the nearest centroid and recomputing centroids."
relationships:
  - type: RELATED_TO
    target: big-o-notation
---

K-means is an unsupervised clustering algorithm that partitions data into *k* groups. It begins by initializing *k* **centroids**, then alternates two steps: assign each point to its nearest centroid, and recompute each centroid as the mean of its assigned points. The loop continues until assignments stop changing.

The algorithm minimizes within-cluster variance (inertia) but only converges to a *local* optimum, so results depend on initialization — k-means++ chooses smarter starting centroids to mitigate this. Choosing *k* is itself a judgment call, often guided by the elbow method or silhouette scores.

K-means is fast and scalable, with each iteration costing roughly O(n·k·d), analyzable via [[big-o-notation]]. Its assumptions — roughly spherical, equally sized clusters using Euclidean distance — limit it; alternatives like Gaussian mixtures or DBSCAN handle other cluster shapes.
