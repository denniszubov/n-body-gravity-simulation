"""N-body gravity simulation with C++ core."""

from nbody._nbody_core import Config, Simulator
from nbody.presets import (
    random_disk,
    figure_eight,
    galaxy_collision,
    binary_star_planets,
    solar_system,
)

__all__ = [
    "Config",
    "Simulator",
    "random_disk",
    "figure_eight",
    "galaxy_collision",
    "binary_star_planets",
    "solar_system",
]
