#!/usr/bin/env python
"""Generate fake results data for demonstration.

This script populates job result files so we can demonstrate aggregation
without requiring actual simulations to complete.
"""
import signac
import numpy as np

project = signac.get_project("../example1-parameter-space")

np.random.seed(42)

print(f"Generating fake results for {len(project)} jobs...")
for i, job in enumerate(project):
    # Generate a result value that depends slightly on parameters
    # to make the aggregation output meaningful
    base = job.sp.temperature / 100.0 + job.sp.pressure / 10.0
    noise = np.random.normal(0, 0.5)
    result_value = base + noise

    with open(job.fn("results.txt"), "w") as f:
        f.write(f"{result_value:.2f}")

    if (i + 1) % 3 == 0:
        print(f"  Generated {i + 1}/{len(project)} results")

print(f"Done! All {len(project)} jobs have results.txt files.")
