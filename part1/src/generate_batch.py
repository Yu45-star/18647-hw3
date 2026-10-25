
"""Generate a batch of Lorenz trajectories."""

import argparse

from generate_trajectory import generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-id", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--output-dir", default="part1/results")
    args = parser.parse_args()

    start = args.batch_id * args.batch_size
    end = min(start + args.batch_size, 10000)

    for trajectory_id in range(start, end):
        generate(trajectory_id, args.output_dir)

    print(f"Generated trajectories {start} to {end - 1}")


if __name__ == "__main__":
    main()
