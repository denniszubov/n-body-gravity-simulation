import numpy as np
from nbody._nbody_core import Config, Simulator


def random_disk(
    n: int = 100,
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


def figure_eight(
    G: float = 1.0,
    eps: float = 0.0001,
) -> Simulator:
    """Three equal masses tracing a figure-8 (Chenciner-Montgomery solution)."""
    positions = np.array([
        [-0.97000436, 0.24308753],
        [0.97000436, -0.24308753],
        [0.0, 0.0],
    ], dtype=np.float64)

    velocities = np.array([
        [0.4662036850, 0.4323657300],
        [0.4662036850, 0.4323657300],
        [-0.9324073700, -0.8647314600],
    ], dtype=np.float64)

    masses = np.array([1.0, 1.0, 1.0], dtype=np.float64)

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)


def galaxy_collision(
    n: int = 80,
    G: float = 1.0,
    eps: float = 0.15,
    seed: int = 42,
) -> Simulator:
    """Two rotating disks on a slow collision course."""
    rng = np.random.default_rng(seed)

    central_mass = 200.0
    body_mass = 0.01
    disk_radius = 1.5
    half_n = n // 2

    # 2 central bodies + orbiting bodies per disk
    total = 2 + n
    positions = np.zeros((total, 2), dtype=np.float64)
    velocities = np.zeros((total, 2), dtype=np.float64)
    masses = np.full(total, body_mass, dtype=np.float64)

    # Two galaxies in a bound orbit around each other
    # Tangential velocity gives orbital motion → gradual inspiral with tidal tails
    sep = 6.0
    v_orbit = 0.55 * np.sqrt(G * central_mass / sep)
    cx = np.array([-sep / 2, sep / 2])
    cy = np.array([0.0, 0.0])
    bvx = np.array([0.0, 0.0])
    bvy = np.array([v_orbit, -v_orbit])

    offset = 0
    for d in range(2):
        # Central body
        positions[offset] = [cx[d], cy[d]]
        velocities[offset] = [bvx[d], bvy[d]]
        masses[offset] = central_mass
        offset += 1

        # Orbiting bodies — tighter disk for stronger binding
        count = half_n if d == 0 else n - half_n
        r = rng.uniform(0.3, disk_radius, size=count)
        theta = rng.uniform(0.0, 2.0 * np.pi, size=count)

        positions[offset:offset + count, 0] = cx[d] + r * np.cos(theta)
        positions[offset:offset + count, 1] = cy[d] + r * np.sin(theta)

        v_circ = np.sqrt(G * central_mass / r)
        velocities[offset:offset + count, 0] = bvx[d] - v_circ * np.sin(theta)
        velocities[offset:offset + count, 1] = bvy[d] + v_circ * np.cos(theta)
        offset += count

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)


def binary_star_planets(
    G: float = 1.0,
    eps: float = 0.005,
) -> Simulator:
    """Two stars in mutual orbit with circumbinary planets."""
    star_mass = 50.0
    separation = 1.0
    orbital_speed = np.sqrt(G * star_mass / (2.0 * separation))

    planet_dists = [3.0, 5.0, 8.0, 12.0]
    planet_masses = [0.05, 0.1, 0.3, 0.08]
    total_star_mass = 2.0 * star_mass

    n = 2 + len(planet_dists)
    positions = np.zeros((n, 2), dtype=np.float64)
    velocities = np.zeros((n, 2), dtype=np.float64)
    masses = np.zeros(n, dtype=np.float64)

    # Binary stars
    positions[0] = [-separation / 2.0, 0.0]
    positions[1] = [separation / 2.0, 0.0]
    velocities[0] = [0.0, orbital_speed]
    velocities[1] = [0.0, -orbital_speed]
    masses[0] = star_mass
    masses[1] = star_mass

    # Circumbinary planets
    for i, (dist, mass) in enumerate(zip(planet_dists, planet_masses)):
        angle = i * (2.0 * np.pi / len(planet_dists))
        positions[2 + i] = [dist * np.cos(angle), dist * np.sin(angle)]
        v_circ = np.sqrt(G * total_star_mass / dist)
        velocities[2 + i] = [-v_circ * np.sin(angle), v_circ * np.cos(angle)]
        masses[2 + i] = mass

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)


def solar_system(
    G: float = 1.0,
    eps: float = 0.001,
) -> Simulator:
    """Our solar system with real mass ratios and orbital distances (AU)."""
    sun_mass = 10000.0

    # (distance AU, mass scaled so Sun=10000 matches real Sun/planet ratios)
    # Real ratio: Sun is 332,946 Earth masses, so 1 Earth mass = 10000/332946
    earth_mass = sun_mass / 332946.0
    planet_data = [
        # (dist AU, mass, name for reference)
        (0.387, 0.0553 * earth_mass),   # Mercury
        (0.723, 0.815 * earth_mass),    # Venus
        (1.000, 1.000 * earth_mass),    # Earth
        (1.524, 0.107 * earth_mass),    # Mars
        (5.203, 317.8 * earth_mass),    # Jupiter
        (9.537, 95.16 * earth_mass),    # Saturn
        (19.19, 14.54 * earth_mass),    # Uranus
        (30.07, 17.15 * earth_mass),    # Neptune
    ]

    n = len(planet_data) + 1
    positions = np.zeros((n, 2), dtype=np.float64)
    velocities = np.zeros((n, 2), dtype=np.float64)
    masses = np.zeros(n, dtype=np.float64)

    masses[0] = sun_mass

    for i, (dist, mass) in enumerate(planet_data, start=1):
        angle = (i - 1) * (2.0 * np.pi / len(planet_data))
        positions[i] = [dist * np.cos(angle), dist * np.sin(angle)]
        v_circ = np.sqrt(G * sun_mass / dist)
        velocities[i] = [-v_circ * np.sin(angle), v_circ * np.cos(angle)]
        masses[i] = mass

    return Simulator(Config(G=G, eps=eps), positions, velocities, masses)
