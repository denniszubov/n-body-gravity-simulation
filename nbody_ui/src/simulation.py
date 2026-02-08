from dataclasses import dataclass

import numpy as np
import nbody_core


@dataclass
class PhysicsConfig:
    dt: float
    gravitational_constant: float
    softening: float
    substeps: int


@dataclass
class SimulationState:
    position: np.ndarray
    velocity: np.ndarray
    mass: np.ndarray
    elapsed_time: float = 0.0


def create_two_body_orbit() -> tuple[SimulationState, PhysicsConfig]:
    separation = 2.0
    body_mass = 1.0

    config = PhysicsConfig(
        dt=0.005,
        gravitational_constant=1.0,
        softening=0.001,
        substeps=4,
    )

    orbital_speed = np.sqrt(
        config.gravitational_constant * body_mass / (2.0 * separation)
    )

    position = np.array([
        [separation / 2.0, 0.0],
        [-separation / 2.0, 0.0],
    ], dtype=np.float64)

    velocity = np.array([
        [0.0, orbital_speed],
        [0.0, -orbital_speed],
    ], dtype=np.float64)

    mass = np.array([body_mass, body_mass], dtype=np.float64)

    return SimulationState(position=position, velocity=velocity, mass=mass), config


def advance(state: SimulationState, config: PhysicsConfig) -> None:
    nbody_core.step(
        state.position,
        state.velocity,
        state.mass,
        config.dt,
        config.gravitational_constant,
        config.softening,
        config.substeps,
    )
    state.elapsed_time += config.dt
