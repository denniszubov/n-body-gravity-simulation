import numpy as np
from nbody._nbody_core import Config, Simulator


def two_body_orbit(
    separation: float = 2.0,
    body_mass: float = 1.0,
    G: float = 1.0,
    eps: float = 0.001,
) -> Simulator:
    """Two equal-mass bodies in a circular orbit."""
    orbital_speed = np.sqrt(G * body_mass / (2.0 * separation))

    positions = np.array([
        [separation / 2.0, 0.0],
        [-separation / 2.0, 0.0],
    ], dtype=np.float64)

    velocities = np.array([
        [0.0, orbital_speed],
        [0.0, -orbital_speed],
    ], dtype=np.float64)

    masses = np.array([body_mass, body_mass], dtype=np.float64)

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)


def random_disk(
    n: int = 200,
    radius: float = 5.0,
    central_mass: float = 100.0,
    body_mass: float = 0.01,
    G: float = 1.0,
    eps: float = 0.05,
    seed: int = 42,
) -> Simulator:
    """N bodies in a disk orbiting a central mass."""
    rng = np.random.default_rng(seed)

    total = n + 1  # central body + orbiting bodies

    positions = np.zeros((total, 2), dtype=np.float64)
    velocities = np.zeros((total, 2), dtype=np.float64)
    masses = np.full(total, body_mass, dtype=np.float64)
    masses[0] = central_mass

    r = rng.uniform(0.5, radius, size=n)
    theta = rng.uniform(0.0, 2.0 * np.pi, size=n)

    positions[1:, 0] = r * np.cos(theta)
    positions[1:, 1] = r * np.sin(theta)

    v_circ = np.sqrt(G * central_mass / r)
    velocities[1:, 0] = -v_circ * np.sin(theta)
    velocities[1:, 1] = v_circ * np.cos(theta)

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)


def solar_system(
    G: float = 1.0,
    eps: float = 0.001,
) -> Simulator:
    """Simplified solar-like system: one star and several planets."""
    star_mass = 1000.0
    planet_data = [
        (1.0, 0.01),
        (2.0, 0.05),
        (3.0, 0.05),
        (5.0, 0.02),
        (8.0, 1.0),
        (12.0, 0.3),
    ]

    n = len(planet_data) + 1
    positions = np.zeros((n, 2), dtype=np.float64)
    velocities = np.zeros((n, 2), dtype=np.float64)
    masses = np.zeros(n, dtype=np.float64)

    masses[0] = star_mass

    for i, (dist, mass) in enumerate(planet_data, start=1):
        angle = (i - 1) * (2.0 * np.pi / len(planet_data))
        positions[i] = [dist * np.cos(angle), dist * np.sin(angle)]
        v_circ = np.sqrt(G * star_mass / dist)
        velocities[i] = [-v_circ * np.sin(angle), v_circ * np.cos(angle)]
        masses[i] = mass

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)
