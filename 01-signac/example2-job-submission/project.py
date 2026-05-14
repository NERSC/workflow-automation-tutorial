#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""signac-flow project with Slurm integration.

This example demonstrates how signac-flow generates Slurm submission scripts
automatically, one per state point.
"""
import time

from flow import FlowProject


class SimulationProject(FlowProject):
    pass


@SimulationProject.label
def simulated(job):
    """Label indicating job has completed simulation."""
    return job.isfile("results.txt")


@SimulationProject.post(simulated)
@SimulationProject.operation(directives={"np": 1, "walltime": 0.5})
def run_simulation(job):
    """Run simulation with parameters from job.sp.

    This operation will be executed in the job's workspace directory.
    signac-flow calls this function directly for each eligible job.
    """
    temp = job.sp.temperature
    pressure = job.sp.pressure
    # Placeholder computation
    result = temp * pressure * 0.001
    time.sleep(1)  # Simulate work
    with open(job.fn("results.txt"), "w") as f:
        f.write(f"{result}\n")
    print(f"Job {job.id[:8]}: T={temp}, P={pressure} -> result={result}")


if __name__ == '__main__':
    import os
    import sys

    # Check if workspace exists (from example1)
    workspace_dir = os.path.join(os.getcwd(), 'workspace')
    parent_workspace = os.path.join(os.path.dirname(os.getcwd()), 'example1-parameter-space', 'workspace')

    if os.path.exists(parent_workspace):
        # Use example1's project directory as the signac project root
        project_path = os.path.dirname(parent_workspace)
        SimulationProject(path=project_path).main()
    elif os.path.exists(workspace_dir):
        SimulationProject().main()
    else:
        print("ERROR: No workspace found!")
        print("\nTo use this example, you must first initialize jobs in example1:")
        print("  cd ../example1-parameter-space")
        print("  python init_project.py")
        print("\nThen return to example2-job-submission and run this script again.")
        sys.exit(1)
