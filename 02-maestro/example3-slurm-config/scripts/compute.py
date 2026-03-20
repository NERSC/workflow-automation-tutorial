#!/usr/bin/env python3
"""Simulated parallel computation demonstrating Slurm execution."""

import argparse
import time
import random
import os
import socket

def run_computation(n_samples, procs):
    """Simulate parallel computation work."""
    hostname = socket.gethostname()
    pid = os.getpid()

    print(f"Running on {hostname} (PID {pid}) with {procs} processes")
    print(f"Computing with {n_samples} samples...")

    # Simulate computation work (sleep time proportional to samples)
    # In real workflow, this would be MPI-parallel computation
    sleep_time = min(n_samples / 100000, 10.0)  # Cap at 10 seconds
    time.sleep(sleep_time)

    # Simulate computational result
    random.seed(n_samples)
    result = sum(random.random() for _ in range(min(n_samples, 10000)))

    print(f"Computation complete. Result: {result:.6f}")
    return result

def main():
    parser = argparse.ArgumentParser(description='Run parallel computation')
    parser.add_argument('--input', required=True, help='Input file with N_SAMPLES')
    parser.add_argument('--output', required=True, help='Output file for results')
    parser.add_argument('--procs', type=int, required=True, help='Number of processes')
    args = parser.parse_args()

    # Read input
    with open(args.input, 'r') as f:
        n_samples = int(f.read().strip())

    # Run computation
    result = run_computation(n_samples, args.procs)

    # Write output
    with open(args.output, 'w') as f:
        f.write(f"Computation Results\n")
        f.write(f"{'='*40}\n")
        f.write(f"Samples:   {n_samples}\n")
        f.write(f"Processes: {args.procs}\n")
        f.write(f"Result:    {result:.6f}\n")

    print(f"Results written to {args.output}")

if __name__ == "__main__":
    main()
