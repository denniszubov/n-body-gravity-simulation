"""N-body gravity simulation with C++ core."""

from nbody._nbody_core import Config, Simulator
from nbody.presets import two_body_orbit, random_disk, solar_system

__all__ = [
    "Config",
    "Simulator",
    "two_body_orbit",
    "random_disk",
    "solar_system",
]
