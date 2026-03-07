import numpy as np
import pytest

from nbody import Simulator, Config


def test_two_body_energy_conservation():
    """Energy should be approximately conserved over many steps."""
    pos = np.array([[1.0, 0.0], [-1.0, 0.0]], dtype=np.float64)
    vel = np.array([[0.0, 0.5], [0.0, -0.5]], dtype=np.float64)
    mass = np.array([1.0, 1.0], dtype=np.float64)

    sim = Simulator(Config(G=1.0, eps=0.01), pos, vel, mass)
    e0 = sim.total_energy()

    sim.step(0.001, n_steps=10000)
    e1 = sim.total_energy()

    assert abs(e1 - e0) / abs(e0) < 1e-4


def test_positions_returns_view():
    """positions() should return a NumPy view, not a copy."""
    pos = np.array([[1.0, 0.0]], dtype=np.float64)
    vel = np.array([[0.0, 0.0]], dtype=np.float64)
    mass = np.array([1.0], dtype=np.float64)

    sim = Simulator(Config(), pos, vel, mass)
    p = sim.positions()

    assert p.shape == (1, 2)
    assert p.dtype == np.float64
    assert not p.flags.owndata


def test_step_mutates_state():
    """Stepping should change positions."""
    pos = np.array([[1.0, 0.0], [-1.0, 0.0]], dtype=np.float64)
    vel = np.array([[0.0, 1.0], [0.0, -1.0]], dtype=np.float64)
    mass = np.array([1.0, 1.0], dtype=np.float64)

    sim = Simulator(Config(G=1.0, eps=0.01), pos, vel, mass)
    p_before = sim.positions().copy()

    sim.step(0.01)
    p_after = sim.positions()

    assert not np.allclose(p_before, p_after)


def test_n_property():
    """The n property should return the number of bodies."""
    pos = np.zeros((5, 2), dtype=np.float64)
    vel = np.zeros((5, 2), dtype=np.float64)
    mass = np.ones(5, dtype=np.float64)

    sim = Simulator(Config(), pos, vel, mass)
    assert sim.n == 5


def test_total_steps_tracking():
    """total_steps should accumulate across calls."""
    pos = np.array([[0.0, 0.0]], dtype=np.float64)
    vel = np.array([[0.0, 0.0]], dtype=np.float64)
    mass = np.array([1.0], dtype=np.float64)

    sim = Simulator(Config(), pos, vel, mass)
    assert sim.total_steps() == 0

    sim.step(0.01, n_steps=10)
    assert sim.total_steps() == 10

    sim.step(0.01, n_steps=5)
    assert sim.total_steps() == 15


def test_invalid_shapes_raise():
    """Mismatched array shapes should raise."""
    pos = np.zeros((3, 2), dtype=np.float64)
    vel = np.zeros((2, 2), dtype=np.float64)  # wrong N
    mass = np.ones(3, dtype=np.float64)

    with pytest.raises(Exception):
        Simulator(Config(), pos, vel, mass)
