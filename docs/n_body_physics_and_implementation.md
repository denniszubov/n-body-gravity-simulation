# N-Body Gravity Simulation – Physics and Implementation Guide

This document describes the physics, math, and coding concepts required to build an N-body gravitational simulation with a C++ compute core and Python/Streamlit visualization.

---

## 1. Physical Model

We model a system of $N$ point masses interacting via Newtonian gravity.

Each body $i$ has:

- mass: $m_i$
- position: $(x_i, y_i)$ or $(x_i, y_i, z_i)$
- velocity: $(v_{x_i}, v_{y_i})$
- acceleration: $(a_{x_i}, a_{y_i})$

The system evolves in discrete time steps of size $\Delta t$.

---

## 2. Newton's Law of Gravitation

For two bodies $i$ and $j$:

$$\Delta x = x_j - x_i$$
$$\Delta y = y_j - y_i$$

Distance with softening:

$$r = \sqrt{(\Delta x)^2 + (\Delta y)^2 + \varepsilon^2}$$

Gravitational force magnitude:

$$F = \frac{G \cdot m_i \cdot m_j}{r^2}$$

Force direction (unit vector):

$$\hat{u}_x = \frac{\Delta x}{r}, \quad \hat{u}_y = \frac{\Delta y}{r}$$

Force components on body $i$ due to $j$:

$$F_x = F \cdot \hat{u}_x, \quad F_y = F \cdot \hat{u}_y$$

---
## 3. Acceleration (Newton’s Second Law)

Acceleration of body $i$:

$$a_{x_i} \mathrel{+}= \frac{F_x}{m_i}$$
$$a_{y_i} \mathrel{+}= \frac{F_y}{m_i}$$

Sum contributions from all other bodies:

$$a_{x_i} = \sum_{j \neq i} \frac{F_{x_{ij}}}{m_i}$$
$$a_{y_i} = \sum_{j \neq i} \frac{F_{y_{ij}}}{m_i}$$

This double loop is $O(N^2)$ and dominates runtime.

---

## 4. Time Integration (Leapfrog Method)

Leapfrog is used instead of Euler to maintain numerical stability.

### Kick-Drift-Kick form

1. Half velocity update:
$$v_x \mathrel{+}= \frac{1}{2} a_x \Delta t$$
$$v_y \mathrel{+}= \frac{1}{2} a_y \Delta t$$

2. Position update:
$$x \mathrel{+}= v_x \Delta t$$
$$y \mathrel{+}= v_y \Delta t$$

3. Recompute acceleration using updated positions

4. Final half velocity update:
$$v_x \mathrel{+}= \frac{1}{2} a_x \Delta t$$
$$v_y \mathrel{+}= \frac{1}{2} a_y \Delta t$$  

---

## 5. Softening Parameter

To avoid singularities when $r$ approaches zero:

$$r^2 = (\Delta x)^2 + (\Delta y)^2 + \varepsilon^2$$

$\varepsilon$ is a small constant relative to system scale.

---

## 6. Conceptual Code Structure

Main simulation loop:

for step in timesteps:
    compute_accelerations()
    leapfrog_update()

Acceleration computation:

for i in bodies:
    ax[i] = 0
    ay[i] = 0
    for j in bodies:
        if i == j: continue
        compute dx, dy, r
        compute force
        accumulate ax[i], ay[i]

---

## 7. Python + C++ Architecture

1. Streamlit UI sets parameters
2. Python calls C++ backend
3. C++ performs physics updates
4. Positions returned to Python
5. Python renders visualization

---

## 8. Scaling and Optimization (Optional)

Naive approach: $O(N^2)$  
Optimized approach: Barnes-Hut tree $O(N \log N)$

---

## 9. What This Project Demonstrates

- Classical mechanics
- Numerical methods
- Performance-oriented C++
- Clean Python/C++ separation
