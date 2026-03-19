#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize signac project with 2D parameter space (temperature x pressure)."""
import signac

project = signac.init_project("signac-demo")

# Define 2D parameter space: temperature x pressure
temps = [300, 400, 500]
pressures = [1.0, 10.0, 100.0]

for temp in temps:
    for pressure in pressures:
        # signac automatically creates unique directory for each combination
        job = project.open_job({"temperature": temp, "pressure": pressure})
        job.init()

print(f"Initialized {len(project)} jobs")
print("Workspace structure created in workspace/")
