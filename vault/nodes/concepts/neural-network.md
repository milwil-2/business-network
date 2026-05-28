---
id: neural-network
label: Neural Network
node_type: Concept
tags: [machine-learning, deep-learning, Concept]
summary: "A model composed of layers of interconnected nodes that learns nonlinear functions by adjusting connection weights."
relationships:
  - type: RELATED_TO
    target: gradient-descent
  - type: RELATED_TO
    target: overfitting
---

A neural network is composed of layers of simple units ("neurons"), each computing a weighted sum of its inputs followed by a nonlinear **activation function** such as ReLU or sigmoid. Stacking layers lets the network approximate highly nonlinear functions, a property formalized by the universal approximation theorem.

Training adjusts the connection weights to minimize a loss. The **backpropagation** algorithm computes the loss gradient with respect to every weight via the chain rule, and [[gradient-descent]] then updates the weights. Modern deep networks chain dozens to hundreds of layers and form a computation [[dag]] of operations.

Their flexibility is also a liability: large networks are prone to [[overfitting]] and require regularization, large datasets, and careful tuning. Specialized architectures — convolutional networks for images, recurrent and transformer networks for sequences — adapt the basic idea to structured data.
