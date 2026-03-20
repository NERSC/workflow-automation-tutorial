#!/usr/bin/env python3
"""Parameterized simulation demonstrating parameter sweeps."""

import argparse
import time
import random

def run_simulation(size, output_file):
    """Run simulation for given size parameter."""
    print(f"Starting simulation with SIZE={size}")

    # Simulate computational work (sleep proportional to size)
    sleep_time = size / 10.0
    print(f"Simulating work for {sleep_time}s...")
    time.sleep(sleep_time)

    # Generate results (simulate some computation)
    random.seed(size)  # Reproducible results
    results = [random.randint(1, 100) for _ in range(size)]

    # Calculate statistics
    mean = sum(results) / len(results)
    min_val = min(results)
    max_val = max(results)

    # Write results
    with open(output_file, 'w') as f:
        f.write(f"Simulation Results for SIZE={size}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Sample count: {size}\n")
        f.write(f"Mean:         {mean:.2f}\n")
        f.write(f"Min:          {min_val}\n")
        f.write(f"Max:          {max_val}\n")
        f.write(f"First 5:      {results[:5]}\n")

    print(f"Simulation complete. Results written to {output_file}")
    return mean, min_val, max_val

def main():
    parser = argparse.ArgumentParser(description='Run parameterized simulation')
    parser.add_argument('--size', type=int, required=True, help='Simulation size parameter')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    run_simulation(args.size, args.output)

if __name__ == "__main__":
    main()
