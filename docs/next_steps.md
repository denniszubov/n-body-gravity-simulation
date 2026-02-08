# N-Body Gravity Simulation – Remaining Work

This document outlines what remains to be done to complete the project, from the C++–Python boundary to the Streamlit UI.

---

## 1. Define the Python Binding API (C++)

### Goal
Expose a **single, minimal, Python-facing function** that advances the simulation.

### Target Python API
```python
step(
    position: np.ndarray,   # shape (N, 2), float64
    velocity: np.ndarray,   # shape (N, 2), float64
    mass: np.ndarray,       # shape (N,), float64
    dt: float,
    G: float,
    eps: float,
    substeps: int = 1,
) -> None
```

### Design Principles
- Arrays are mutated in place
- Python owns memory
- C++ does only computation
- No rendering, no I/O in C++

---

## 2. Implement `step()` in `bindings.cpp`

### Tasks
- Replace the test `add()` binding
- Use `pybind11::numpy` to accept NumPy arrays
- Validate:
  - dtype is `float64`
  - shapes are correct
  - arrays are contiguous
- Convert NumPy buffers to C++ views or temporary `State`
- Call:
  1. `compute_acceleration(...)` once
  2. `leapfrog_step(...)` in a loop (`substeps` times)
- Return `None`

### Initial Approach (Recommended)
- Copy NumPy → `State`
- Run physics
- Copy back to NumPy

(Optimize later if needed.)

---

## 3. Python-Side Simulation Driver

### Tasks
- Create a small Python module (e.g. `simulation.py`)
- Responsibilities:
  - initialize position, velocity, mass arrays
  - call `nbody_core.step(...)`
  - manage simulation time
- No UI yet, just correctness testing

### Validation
- Two-body orbit remains bounded
- Energy drift is small
- Increasing `substeps` improves stability

---

## 4. Streamlit UI

### Core UI Components
- No sliders to start with, just hardcoded parameters for now
- Preset selector:
  - two-body orbit
  - disk / galaxy
  - random cluster
- Start / pause / reset controls

### Visualization
- 2D scatter plot of bodies
- Optional trails
- Frame-by-frame update driven by Python loop
- Use plotly for rendering

### Architecture
- Streamlit handles:
  - UI
  - rendering
  - user input
- C++ handles:
  - physics only

---

## Current Status Summary

### Done
- Gravity computation (C++)
- Leapfrog integrator (C++)
- Manual compilation
- pybind11 extension successfully builds and imports

### Next Immediate Task
Implement the real `step()` binding in `bindings.cpp`.
