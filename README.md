# N-Body Gravity Simulation

A real-time gravitational N-body simulation with a C++ physics engine, Python API, and an interactive browser frontend.

![N-Body Gravity Simulation](assets/n-body-gravity-simulator.gif)

<!-- TODO: Uncomment when deployed -->
<!-- **[Live Demo](https://your-app.onrender.com)** -->

## Quickstart

```bash
git clone https://github.com/denniszubov/n-body-gravity-simulation.git
cd n-body-gravity-simulation
python -m venv .venv && source .venv/bin/activate
make build
make run
```

Open http://127.0.0.1:8000 in your browser.

## How It Works

The physics runs entirely in C++. Python handles presets and the service layer. The browser renders particles on an HTML canvas.

```mermaid
flowchart TD
    subgraph Browser
        A[HTML Canvas + JS] -->|HTTP polling| B[FastAPI]
    end
    subgraph Python
        B --> C[nbody package]
    end
    subgraph C++
        D[pybind11 bindings] --> E[Simulator]
        E --> F[Gravity Calculation]
        E --> G[Leapfrog Integrator]
    end
    C -- parameters --> D
    D -. "positions & velocities (zero-copy NumPy views)" .-> C
```

**C++ does:** gravitational force calculation, leapfrog integration, energy tracking, step timing

**Python does:** preset initialization, simulation service, JSON API

**Browser does:** canvas rendering with glow effects, controls, stats overlay

Positions and velocities are returned to Python as NumPy views pointing directly into C++ memory — no copying.

## Presets

| Preset | Description |
|--------|-------------|
| Galaxy Collision | Two rotating galaxies in a bound orbit, merging with tidal tails |
| Random Disk | N bodies orbiting a central mass |
| Figure-8 Three-Body | Three equal masses tracing a periodic figure-8 (Chenciner-Montgomery solution) |
| Binary Star + Planets | Two stars in mutual orbit with circumbinary planets |
| Solar System | The Sun and all 8 planets with real mass ratios and orbital distances |

## Project Structure

```
cpp/                  C++ physics engine
  include/nbody/      Headers
  src/                Implementations + pybind11 bindings
python/nbody/         Python package (presets, re-exports)
app/                  FastAPI web service
static/               Browser frontend (HTML canvas + JS + CSS)
tests/                pytest suite
```

## Build System

The project uses CMake + [scikit-build-core](https://github.com/scikit-build/scikit-build-core) so the C++ extension compiles automatically via `pip install`.

| Command | What it does |
|---------|-------------|
| `make build` | Compile C++ and install the package |
| `make run` | Launch the FastAPI server |
| `make test` | Run the test suite |

## Physics

- **Gravity:** Newtonian gravitational force with a softening parameter to avoid singularities
- **Integrator:** Leapfrog (kick-drift-kick) — a symplectic integrator that conserves energy over long simulations

## API

```python
from nbody import Simulator, Config, random_disk

sim = random_disk(n=500, seed=42)
sim.step(dt=0.005, n_steps=100)

pos = sim.positions()   # (N, 2) NumPy array, zero-copy view
energy = sim.total_energy()
```
