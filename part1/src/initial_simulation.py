
"""Run and visualize the initial Lorenz trajectory."""

from pathlib import Path

import matplotlib.pyplot as plt

from lorenz import simulate


def main():
    times, states = simulate((1.0, 1.0, 1.0), steps=2000, h=0.01)
    x, y, z = states.T

    print(f"Initial state: {states[0]}")
    print(f"Final state at t={times[-1]:.2f}: {states[-1]}")

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(x, y, z, linewidth=0.8)
    ax.scatter(x[0], y[0], z[0], color="green", s=35, label="Start")
    ax.scatter(x[-1], y[-1], z[-1], color="red", s=35, label="End")

    ax.set(
        xlabel="x",
        ylabel="y",
        zlabel="z",
        title="Lorenz Attractor (2,000 steps, h=0.01)"
    )
    ax.legend()
    fig.tight_layout()

    output_dir = Path(__file__).resolve().parent.parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "initial_trajectory.png"
    fig.savefig(output_path, dpi=160)

    print(f"Plot saved to: {output_path}")
    plt.show()


if __name__ == "__main__":
    main()
