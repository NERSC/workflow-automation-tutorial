#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""signac-flow project with Slurm integration.

This example demonstrates how signac-flow generates Slurm submission scripts
automatically, one per state point.
"""
from flow import FlowProject
import signac


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
    SimulationProject().main()
