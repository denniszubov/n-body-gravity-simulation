# N-Body Gravity Simulation – Physics and Implementation Guide

This document describes the physics, math, and coding concepts required to build an N-body gravitational simulation with a C++ compute core and Python/Streamlit visualization.

---

## 1. Physical Model

We model a system of N point masses interacting via Newtonian gravity.

Each body i has:

- mass: mi
- position: (xi, yi) or (xi, yi, zi)
- velocity: (vxi, vyi)
- acceleration: (axi, ayi)

The system evolves in discrete time steps of size dt.

---

## 2. Newton’s Law of Gravitation

For two bodies i and j:

dx = xj - xi  
dy = yj - yi  

Distance with softening:

r = sqrt(dx*dx + dy*dy + eps*eps)

Gravitational force magnitude:

F = G * mi * mj / (r*r)

Force direction (unit vector):

ux = dx / r  
uy = dy / r  

Force components on body i due to j:

Fx = F * ux  
Fy = F * uy  

---

## 3. Acceleration (Newton’s Second Law)

Acceleration of body i:

axi += Fx / mi  
ayi += Fy / mi  

Sum contributions from all other bodies:

axi = sum over j != i of (Fx_ij / mi)  
ayi = sum over j != i of (Fy_ij / mi)  

This double loop is O(N²) and dominates runtime.

---

## 4. Time Integration (Leapfrog Method)

Leapfrog is used instead of Euler to maintain numerical stability.

### Kick-Drift-Kick form

1. Half velocity update:
vx += 0.5 * ax * dt  
vy += 0.5 * ay * dt  

2. Position update:
x += vx * dt  
y += vy * dt  

3. Recompute acceleration using updated positions

4. Final half velocity update:
vx += 0.5 * ax * dt  
vy += 0.5 * ay * dt  

---

## 5. Softening Parameter

To avoid singularities when r approaches zero:

r² = dx*dx + dy*dy + eps*eps

eps is a small constant relative to system scale.

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

Naive approach: O(N²)  
Optimized approach: Barnes-Hut tree O(N log N)

---

## 9. What This Project Demonstrates

- Classical mechanics
- Numerical methods
- Performance-oriented C++
- Clean Python/C++ separation
