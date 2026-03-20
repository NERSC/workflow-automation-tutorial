# Section 2: Maestro - Declarative DAG Workflow Orchestration

**Duration:** 30 minutes

**Concepts:** Directed Acyclic Graphs (DAGs), declarative workflow specification, dependency management, YAML-based orchestration

## Overview

Maestro introduces **dependency management** through declarative DAG (Directed Acyclic Graph) specifications written in YAML. Where signac organizes parameter spaces using the filesystem, Maestro adds the ability to define multi-step workflows where some steps must complete before others can begin.

**Key capability:** DAG-based dependency resolution with declarative YAML specifications

## Why Maestro?

Maestro was developed at Lawrence Livermore National Laboratory (LLNL) specifically for HPC workflow orchestration. It provides:

- **Declarative specification:** Define what to run and dependencies, not how to run it
- **Scheduler abstraction:** Same YAML works across Slurm, Flux, LSF via `$(LAUNCHER)` token
- **Clear documentation:** YAML format is self-documenting and version-controllable
- **Parameter integration:** Combines parameter sweeps with workflow dependencies
- **Minimal coupling:** Workflow logic separated from system-specific details

### Advantages over alternatives:
- **vs GNU Parallel:** Adds multi-step dependencies (Parallel only does independent tasks)
- **vs signac:** Adds workflow orchestration (signac only organizes parameters)
- **vs Snakemake:** HPC-native with Slurm integration built-in, simpler for batch workloads
- **vs Airflow/Luigi:** Designed for HPC batch systems, not web services

### Unique teaching value:
- Introduces DAG concepts fundamental to all workflow systems
- Demonstrates declarative vs imperative workflow definition
- Shows scheduler abstraction patterns (`$(LAUNCHER)`, `$(SPECROOT)`)
- Bridges filesystem-based (signac) and orchestrated (Merlin) paradigms

### Perlmutter/Slurm compatibility:
- Native Slurm batch adapter
- Automatic `.slurm.sh` script generation from YAML
- Supports Perlmutter-specific options (accounts, partitions, QOS)
- Can run on login nodes or submit to scheduler

## When to Use Maestro

✅ **Good for:**
- Multi-step workflows with dependencies (prep → run → analyze → visualize)
- Parameter sweeps where all runs follow same workflow structure
- Workflows needing clear documentation (YAML is readable by non-programmers)
- Projects requiring scheduler portability (Slurm → Flux → LSF)
- Moderate complexity (10-100 steps, hundreds to thousands of jobs)

❌ **Graduate to Merlin when:**
- Scale exceeds thousands of jobs across multiple allocations
- Need persistent coordination across restarts
- Require fault tolerance with automatic retries
- Want distributed worker pools for massive parameter sweeps

❌ **Graduate to AiiDA when:**
- Need comprehensive provenance tracking for publication
- Require reproducibility verification
- Want automated workflow versioning and data lineage
- Need to answer "where did this result come from?" years later

## Core Concepts

### DAG (Directed Acyclic Graph)

A workflow structure where:
- **Nodes = steps** (tasks to execute)
- **Edges = dependencies** (step B waits for step A)
- **Directed = one-way flow** (prep → run, not bidirectional)
- **Acyclic = no loops** (prevents circular dependencies)

Maestro automatically determines execution order from dependencies.

### Declarative Specification

**Imperative (bash script):**
```bash
./prepare.sh
./run.sh
./analyze.sh
```

**Declarative (Maestro YAML):**
```yaml
study:
  - name: prepare
    run:
      cmd: ./prepare.sh

  - name: run
    run:
      cmd: ./run.sh
      depends: [prepare]

  - name: analyze
    run:
      cmd: ./analyze.sh
      depends: [run]
```

Declarative style documents *what* and *why*, not *how*.

### YAML Structure

Maestro workflows have 3 required sections:

```yaml
description:
  name: Study Name
  description: What this workflow does

env:
  variables:
    FIXED_VALUE: "constant_across_runs"

study:
  - name: step-name
    description: What this step does
    run:
      cmd: |
        commands to execute
      depends: [prerequisite-steps]
```

Optional sections:
- `batch`: Slurm/Flux/LSF configuration
- `global.parameters`: Parameter sweep definitions

### Token System

Maestro provides built-in tokens for portable path references:

- `$(SPECROOT)` - Directory containing the YAML file
- `$(OUTPUT_PATH)` - Step output directory (timestamp-based)
- `$(WORKSPACE)` - Parameter-specific workspace (in sweeps)
- `$(LAUNCHER)` - Scheduler launch command (e.g., `srun` on Slurm)
- Custom tokens from `env.variables`

Example:
```yaml
cmd: |
  cd $(SPECROOT)/data
  $(LAUNCHER) python compute.py > $(OUTPUT_PATH)/results.txt
```

### Parameter Sweeps

Combine parameter variations with workflow structure:

```yaml
global.parameters:
  SIZE:
    values: [10, 20, 30]
    label: SIZE.%%

study:
  - name: run
    run:
      cmd: python simulate.py --size $(SIZE)

  - name: analyze
    run:
      cmd: python analyze.py --size $(SIZE)
      depends: [run_*]  # Wildcard waits for all SIZE values
```

This creates 6 jobs total: 3 `run` jobs (one per SIZE) + 3 `analyze` jobs (one per SIZE).

## Slurm Integration

Maestro submits jobs to Slurm via the `batch` block:

```yaml
batch:
  type: slurm
  host: perlmutter
  bank: account_name
  queue: regular

study:
  - name: compute
    run:
      cmd: $(LAUNCHER) python code.py
      nodes: 1
      procs: 64
      walltime: "00:30:00"
```

Maestro automatically:
1. Generates `.slurm.sh` script with `#SBATCH` directives
2. Submits via `sbatch`
3. Monitors job status
4. Writes timestamped logs

## Progression from signac

**signac provided:** Parameter space organization via filesystem

**Maestro adds:**
- Multi-step dependencies
- Declarative workflow logic
- Automatic Slurm script generation
- Workflow-wide configuration

**Combined power:**
Use signac for parameter organization, Maestro for workflow orchestration when your parameter sweep needs multi-step dependencies.

## Examples in This Section

1. **example1-simple-dag** - 4-step sequential workflow (prepare → simulate → analyze → visualize)
2. **example2-param-sweeps** - Parameter sweep with workflow dependencies
3. **example3-slurm-config** - Perlmutter-specific batch configuration

## When to Graduate to Next Tool

**Stay with Maestro if:**
- Single allocation handles all work
- Workflow coordinator can run continuously during execution
- Moderate scale (hundreds to low thousands of jobs)

**Move to Merlin (Section 3) if:**
- Need distributed coordination across multiple allocations
- Want persistent queuing that survives restarts
- Require fault tolerance with retries
- Scale exceeds thousands of jobs

## Official Documentation

- [Maestro Workflow Conductor ReadTheDocs](https://maestrowf.readthedocs.io/)
- [GitHub - LLNL/maestrowf](https://github.com/LLNL/maestrowf)
- [Maestro Tutorials](https://maestrowf.readthedocs.io/en/latest/Maestro/tutorials.html)
- [HPC Workflow Management with Maestro (Carpentries)](https://carpentries-incubator.github.io/HPC-workflow-lesson-maestro/)
- [Workflows Community Initiative - Maestro](https://workflows.community/systems/maestrowf/)

## Quick Start

```bash
# Install (already in requirements.txt)
pip install maestrowf==1.1.11

# Run a workflow
maestro run workflow.yaml

# Check status
maestro status workflow_<timestamp>

# Cancel running study
maestro cancel workflow_<timestamp>
```

---

**Next:** See examples for hands-on experience with DAG workflows on Perlmutter.
