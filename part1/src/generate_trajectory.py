"""Generate one perturbed Lorenz trajectory as a four-column CSV."""

import argparse
import csv
from pathlib import Path

import numpy as np

from lorenz import simulate


def perturbed_start(endpoint, rng, max_radius=0.5):
    """Add a random direction and a radius uniformly chosen in [0, max_radius]."""
    direction = rng.normal(size=3)
    direction /= np.linalg.norm(direction)
    radius = rng.uniform(0.0, max_radius)
    return np.asarray(endpoint) + radius * direction


def generate(trajectory_id, output_dir, base_seed=42):
    # All trajectories share the same unperturbed reference endpoint.
    _, initial_states = simulate((1.0, 1.0, 1.0), steps=2000, h=0.01)
    endpoint = initial_states[-1]

    rng = np.random.default_rng(base_seed + trajectory_id)
    start = perturbed_start(endpoint, rng)
    times, states = simulate(start, steps=1000, h=0.01)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"trajectory_{trajectory_id:05d}.csv"
    with output_file.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "x", "y", "z"])
        writer.writerows(zip(times, *states.T))

    return output_file


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", type=int, required=True, help="Trajectory ID (0-9999)")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent.parent / "results")
    parser.add_argument("--base-seed", type=int, default=42)
    args = parser.parse_args()

    if not 0 <= args.id < 10000:
        parser.error("--id must be between 0 and 9999")
    print(f"Saved {generate(args.id, args.output_dir, args.base_seed)}")


if __name__ == "__main__":
    main()
