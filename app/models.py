from pydantic import BaseModel


class CreateRequest(BaseModel):
    preset: str
    n_bodies: int = 200
    seed: int = 42


class StepRequest(BaseModel):
    dt: float = 0.005
    n_steps: int = 6


class EnergyInfo(BaseModel):
    kinetic: float
    potential: float
    total: float


class SimState(BaseModel):
    t: float
    n: int
    positions: list[list[float]]
    masses: list[float]
    energy: EnergyInfo
    initial_energy: float
    relative_drift: float
    total_steps: int
    step_time_ms: float


class PresetInfo(BaseModel):
    name: str
    label: str
    default_n_bodies: int
    view_range: float
    has_n_bodies: bool
