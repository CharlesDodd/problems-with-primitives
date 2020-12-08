# problems-with-primitives
Examples to show common mistakes with the implementation of cryptographic primitives

# collision_calculator.py

An example to show just how easy it is to construct a collision for poorly constructed hashes. This construction deviates very slightly from Davies-Meyer and XORs the header (chaining variable / key / etc) back onto the output. The example demonstrates just one round of this close cousin of Davies-Meyer, and calculates a datagram which will collide.

Maths:

Given a datagram  given by  <img src="https://render.githubusercontent.com/render/math?math=datagram_{1}=(header_{1},payload_{1})">  and a Hash construction like so:

![](bad_hash.png)

We can pick a different random header <img src="https://render.githubusercontent.com/render/math?math=header_{2}">  and calculate a payload such that the combination produces a collision. The following is a formula:


<img src="https://render.githubusercontent.com/render/math?math=payload_{2}%20=%20\text{SHACAL}^{-1}_{header_{2}}(\text{SHACAL}_{header_{1}}(payload_{1})\oplus%20header_{1}%20\oplus%20header_{2})">


