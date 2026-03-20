#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""signac-flow project with Slurm integration.

This example demonstrates how signac-flow generates Slurm submission scripts
automatically, one per state point.
"""
from flow import FlowProject


class SimulationProject(FlowProject):
    pass


@SimulationProject.label
def simulated(job):
    """Label indicating job has completed simulation."""
    return job.isfile("results.txt")


@SimulationProject.operation
@SimulationProject.directives(
    np=1,
    walltime=0.5,
    executable="python simulate.py"
)
def run_simulation(job):
    """Run simulation with parameters from job.sp.

    This operation will be executed in the job's workspace directory.
    The simulate.py script will have access to job parameters.
    """
    pass


if __name__ == '__main__':
    import os
    import sys

    # Check if workspace exists (from example1)
    workspace_dir = os.path.join(os.getcwd(), 'workspace')
    parent_workspace = os.path.join(os.path.dirname(os.getcwd()), 'example1-parameter-space', 'workspace')

    if not os.path.exists(workspace_dir) and not os.path.exists(parent_workspace):
        print("ERROR: No workspace found!")
        print("\nTo use this example, you must first initialize jobs in example1:")
        print("  cd ../example1-parameter-space")
        print("  python init_project.py")
        print("\nThen return to example2-job-submission and run this script again.")
        sys.exit(1)

    SimulationProject().main()
