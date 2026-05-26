#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query completed jobs and aggregate results across parameter space."""
import signac
import numpy as np

project = signac.get_project("../example1-parameter-space")

# Query jobs by parameter: find all jobs with temperature >= 400
high_temp_jobs = project.find_jobs({"temperature": {"$gte": 400}})

# Aggregate results
results = []
for job in high_temp_jobs:
    if job.isfile("results.txt"):
        with open(job.fn("results.txt")) as f:
            value = float(f.read())
            results.append((job.sp.temperature, job.sp.pressure, value))

# Analysis
print(f"Analyzed {len(results)} completed high-temperature jobs")
if results:
    mean_value = np.mean([r[2] for r in results])
    print(f"Mean result: {mean_value:.2f}")
    print("\nResults by job:")
    for temp, pressure, value in sorted(results):
        print(f"  T={temp}, P={pressure}: {value:.2f}")
else:
    print("No results found. Run generate_fake_data.py first.")
