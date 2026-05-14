# Example 2: Slurm Job Submission with signac-flow

## Overview

This example demonstrates **signac-flow's Slurm integration**. signac-flow automatically generates Slurm submission scripts from your operation definitions, creating one script per state point.

## The signac-flow Approach

Traditional HPC workflow:
```bash
# Manually create scripts for each parameter
sbatch job_T300_P1.0.sh
sbatch job_T300_P10.0.sh
sbatch job_T300_P100.0.sh
# ... repeat for other temperatures
```

With signac-flow:
```bash
python project.py submit
# Flow generates and submits all scripts automatically
```

## Components

### project.py - Workflow Definition

The `FlowProject` class defines your workflow in code:

- **@SimulationProject.operation(directives={...})**: Decorates a function as an operation (work unit) with HPC resource requirements:
  - `np=1`: 1 process per job
  - `walltime=0.5`: 30 minutes (0.5 hours)
- **@SimulationProject.label**: Defines job completion criteria (marks as "simulated" when results.txt exists)

### simulate.py - Standalone Parameter Access Demo

Not called by `project.py`. Demonstrates how to access job parameters from a standalone script using `signac.get_job()`, useful for debugging or running individual jobs outside the flow framework.

## Running This Example

### Setup (requires existing job structure from example1)

First, initialize jobs:
```bash
cd ../example1-parameter-space
python init_project.py
```

### Test Job Submission

From example2-job-submission directory:
```bash
# Preview what would be submitted (without actually submitting)
python project.py submit --pretend
```

This shows:
- Slurm commands that would be executed
- Number of jobs to be submitted
- Job parameters for each submission

### Actual Submission on Perlmutter

signac-flow forwards extra flags directly to `sbatch` via `--` on the submit command:

```bash
# Submit with account and reservation (training session)
python project.py submit -- -A ntrain4 --constraint=cpu --reservation=<reservation_name>

# Submit with account only (outside training reservation)
python project.py submit -- -A <your_account> --constraint=cpu
```

Everything after `--` is appended verbatim to the generated `sbatch` command. The `--constraint=cpu`, `-A`, and optionally `--reservation` flags must all be provided via the `--` passthrough.

### The Submission Process

When you run `python project.py submit`:

1. Flow discovers all jobs in the workspace (from example1)
2. For each job not yet marked as "simulated":
   - Creates a unique Slurm submission script in the job directory
   - Passes the job context to the operation function (parameters available via `job.sp`)
3. Submits all scripts to Slurm

### Why This Matters

**No manual script creation**: Define operations once, flow handles one-per-state-point duplication automatically.

**Parameter injection**: Each job's parameters automatically become available to the simulation script (through `job.sp`).

**State tracking**: Flow maintains labels (completion status) so it only runs incomplete jobs.

## Next Steps

See **example3-aggregation** to learn how to query completed jobs and aggregate results across the parameter space.
