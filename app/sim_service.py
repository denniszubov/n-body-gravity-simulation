from nbody import (
    Simulator,
    random_disk,
    figure_eight,
    galaxy_collision,
    binary_star_planets,
    solar_system,
)
from app.models import SimState, EnergyInfo, PresetInfo

PRESETS = {
    "galaxy_collision": PresetInfo(
        name="galaxy_collision",
        label="Galaxy Collision",
        default_n_bodies=160,
        view_range=12.0,
        has_n_bodies=True,
    ),
    "random_disk": PresetInfo(
        name="random_disk",
        label="Random Disk",
        default_n_bodies=200,
        view_range=8.0,
        has_n_bodies=True,
    ),
    "figure_eight": PresetInfo(
        name="figure_eight",
        label="Figure-8 Three-Body",
        default_n_bodies=3,
        view_range=2.0,
        has_n_bodies=False,
    ),
    "binary_star_planets": PresetInfo(
        name="binary_star_planets",
        label="Binary Star + Planets",
        default_n_bodies=6,
        view_range=16.0,
        has_n_bodies=False,
    ),
    "solar_system": PresetInfo(
        name="solar_system",
        label="Solar System",
        default_n_bodies=9,
        view_range=35.0,
        has_n_bodies=False,
    ),
}

FACTORIES = {
    "galaxy_collision": lambda n_bodies=160, seed=42, **_kw: galaxy_collision(n=n_bodies, seed=seed),
    "random_disk": lambda n_bodies=200, seed=42, **_kw: random_disk(n=n_bodies, seed=seed),
    "figure_eight": lambda **_kw: figure_eight(),
    "binary_star_planets": lambda **_kw: binary_star_planets(),
    "solar_system": lambda **_kw: solar_system(),
}


class SimService:
    def __init__(self) -> None:
        self.sim: Simulator | None = None
        self.elapsed_time: float = 0.0
        self.initial_energy: float = 0.0
        self.preset: str = ""

    def create(self, preset: str, **kwargs) -> SimState:
        factory = FACTORIES.get(preset)
        if factory is None:
            raise ValueError(f"Unknown preset: {preset}")
        self.sim = factory(**kwargs)
        self.elapsed_time = 0.0
        self.initial_energy = self.sim.total_energy()
        self.preset = preset
        return self._build_state()

    def step(self, dt: float, n_steps: int) -> SimState:
        if self.sim is None:
            raise RuntimeError("No simulation created")
        self.sim.step(dt, n_steps=n_steps)
        self.elapsed_time += dt * n_steps
        return self._build_state()

    def state(self) -> SimState:
        if self.sim is None:
            raise RuntimeError("No simulation created")
        return self._build_state()

    def _build_state(self) -> SimState:
        sim = self.sim
        pos = sim.positions()
        masses = sim.masses()
        ke = sim.kinetic_energy()
        pe = sim.potential_energy()
        total_e = sim.total_energy()
        drift = abs(total_e - self.initial_energy) / abs(self.initial_energy) if self.initial_energy != 0 else 0.0

        return SimState(
            t=self.elapsed_time,
            n=sim.n,
            positions=pos.tolist(),
            masses=masses.tolist(),
            energy=EnergyInfo(kinetic=ke, potential=pe, total=total_e),
            initial_energy=self.initial_energy,
            relative_drift=drift,
            total_steps=sim.total_steps(),
            step_time_ms=sim.last_step_time_sec() * 1000,
        )
