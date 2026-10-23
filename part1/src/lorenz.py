
"""Lorenz system and its numerical integration."""

import numpy as np
from scipy.integrate import solve_ivp


def lorenz(t, state, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    """Return the derivatives (dx/dt, dy/dt, dz/dt)."""
    x, y, z = state
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def simulate(initial_state, steps=2000, h=0.01):
    """Integrate for `steps` intervals of size `h` (including time zero)."""
    times = np.arange(steps + 1, dtype=float) * h

    solution = solve_ivp(
        lorenz,
        (0.0, steps * h),
        initial_state,
        t_eval=times,
        rtol=1e-9,
        atol=1e-12,
    )

    if not solution.success:
        raise RuntimeError(f"ODE integration failed: {solution.message}")

    return solution.t, solution.y.T
