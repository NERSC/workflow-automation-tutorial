# Workflow Management Seminar Implementation Plan - Phase 4

**Goal:** Introduce declarative DAG-based workflow specification showing when dependencies require workflow orchestration beyond parameter organization

**Architecture:** Three progressive examples demonstrating Maestro capabilities: simple sequential DAG → parameter sweeps with dependencies → Perlmutter-specific Slurm configuration in YAML

**Tech Stack:**
- Maestro (maestrowf) v1.1.11 (installed via requirements.txt in Phase 1)
- YAML for declarative workflow specification
- Slurm batch system integration
- Python 3.10+ for workflow execution

**Scope:** Phase 4 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phase 1-3 infrastructure will exist before this phase executes)

**Note on commit strategy:** Phase 4 uses per-task commits for more granular version control, differing from Phases 1-3's batch commits. This approach provides clearer history for the 4 separate Maestro components (README + 3 examples).

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC1: Tool selections are justified and appropriate for HPC audience
- **wf-seminar.AC1.1 Success:** Each of 5 tools (GNU Parallel, signac, Maestro, Merlin, AiiDA) has documented rationale explaining why it fits its category - Phase 4 adds Maestro rationale
- **wf-seminar.AC1.2 Success:** Tool justifications include: category fit, advantages over alternatives, unique teaching value, Perlmutter/Slurm compatibility

### wf-seminar.AC2: Seminar structure is pedagogically sound and time-appropriate
- **wf-seminar.AC2.3 Success:** Each section follows pattern: motivation → concepts → demo → hands-on → decision criteria
- **wf-seminar.AC2.4 Success:** Tools build on previous sections (signac uses Parallel concepts, Maestro adds to signac, etc.)

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 example specifications (15 total across 5 tools) - Phase 4 provides 3 Maestro examples
- **wf-seminar.AC4.3 Success:** Examples progress from simple to complex within each tool section
- **wf-seminar.AC4.4 Success:** All examples specify they must run on Perlmutter without modification
- **wf-seminar.AC4.5 Success:** Example specifications include: what to demonstrate, expected concepts learned, sample use case

### wf-seminar.AC5: NERSC/Perlmutter integration is accurate and complete
- **wf-seminar.AC5.1 Success:** Perlmutter-specific configuration documented for each tool (Slurm integration, filesystem usage, QOS options)

### wf-seminar.AC6: Repository structure supports autonomous learning
- **wf-seminar.AC6.2 Success:** Each section includes README with concepts, when to use, and links to official documentation

---

<!-- START_TASK_1 -->
### Task 1: Create 02-maestro/README.md with DAG concepts and tool rationale

**Verifies:** wf-seminar.AC1.1, wf-seminar.AC1.2, wf-seminar.AC2.3, wf-seminar.AC6.2

**Files:**
- Create: `02-maestro/README.md`

**Implementation:**

Create comprehensive README explaining Maestro's role in the tool progression and when to use it.

```markdown
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
```

**Verification:**

Run: `cat 02-maestro/README.md | head -20`
Expected: Shows section title, duration, concepts

Run: `grep -c "Why Maestro?" 02-maestro/README.md`
Expected: Returns `1` (section exists)

Run: `grep -c "$(LAUNCHER)" 02-maestro/README.md`
Expected: Returns at least `3` (token system explained with examples)

**Commit:**

```bash
git add 02-maestro/README.md
git commit -m "feat(maestro): add section README with DAG concepts and tool rationale

- Explains Maestro's role in tool progression (adds dependencies to signac)
- Documents advantages over alternatives (Parallel, signac, Snakemake, Airflow)
- Covers DAG concepts, declarative specification, YAML structure
- Includes Slurm integration patterns for Perlmutter
- Provides decision criteria for when to use vs graduate to Merlin
- Links to official documentation and tutorials"
```

<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create example1-simple-dag with 4-step sequential workflow

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `02-maestro/example1-simple-dag/workflow.yaml`
- Create: `02-maestro/example1-simple-dag/README.md`
- Create: `02-maestro/example1-simple-dag/scripts/prepare.sh`
- Create: `02-maestro/example1-simple-dag/scripts/simulate.py`
- Create: `02-maestro/example1-simple-dag/scripts/analyze.py`
- Create: `02-maestro/example1-simple-dag/scripts/visualize.py`

**Implementation:**

Create a simple 4-step workflow demonstrating DAG dependency resolution: prepare → simulate → analyze → visualize.

**File 1: `02-maestro/example1-simple-dag/README.md`**

```markdown
# Example 1: Simple Sequential DAG

**Learning Objectives:**
- Define multi-step workflows with dependencies in YAML
- Understand DAG execution order determined by `depends` keyword
- Use Maestro tokens (`$(SPECROOT)`, `$(OUTPUT_PATH)`)
- Run workflows on Perlmutter login nodes

**Concepts:** Sequential dependencies, declarative workflow specification, automatic execution ordering

## Workflow Structure

```
prepare → simulate → analyze → visualize
```

Each step depends on the previous:
- `prepare`: Generates input data
- `simulate`: Runs computation using prepared data
- `analyze`: Processes simulation output
- `visualize`: Creates plots from analyzed results

## Files

- `workflow.yaml` - Maestro workflow specification
- `scripts/prepare.sh` - Data preparation script
- `scripts/simulate.py` - Simple simulation (sleeps to simulate work)
- `scripts/analyze.py` - Result analysis
- `scripts/visualize.py` - Plotting (creates dummy plot)

## Running on Perlmutter

**On login node (quick test):**
```bash
module load python
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example1-simple-dag
maestro run workflow.yaml
```

Maestro creates a timestamped directory (e.g., `workflow_20260319-143022/`) containing:
- `prepare/` - Logs and outputs from prepare step
- `simulate/` - Logs and outputs from simulate step
- `analyze/` - Logs and outputs from analyze step
- `visualize/` - Logs and outputs from visualize step
- `meta/` - Maestro internal state files

**Check status:**
```bash
maestro status workflow_20260319-143022
```

**View results:**
```bash
# Prepared data
cat workflow_20260319-143022/prepare/input.dat

# Simulation output
cat workflow_20260319-143022/simulate/results.txt

# Analysis summary
cat workflow_20260319-143022/analyze/summary.txt

# Plot (would be PNG in real workflow)
cat workflow_20260319-143022/visualize/plot.txt
```

## Key Concepts Demonstrated

1. **Declarative dependencies:** `depends: [step-name]` ensures execution order
2. **Automatic ordering:** Maestro determines which steps can run in parallel (none here)
3. **Token usage:** `$(SPECROOT)` references workflow directory, `$(OUTPUT_PATH)` writes outputs
4. **Filesystem passing:** Each step reads from previous step's `$(OUTPUT_PATH)`

## Expected Output

```
$ maestro run workflow.yaml
[TIMESTAMP] INFO: Loading specification from workflow.yaml
[TIMESTAMP] INFO: Launching study workflow...
[TIMESTAMP] INFO: Study workflow launched successfully.

$ maestro status workflow_20260319-143022
Step Name       | State     | Run Time | Elapsed Time
----------------|-----------|----------|-------------
prepare         | FINISHED  | 1s       | 1s
simulate        | FINISHED  | 3s       | 3s
analyze         | FINISHED  | 1s       | 1s
visualize       | FINISHED  | 1s       | 1s
```

## Exercises

1. Modify `simulate.py` to sleep longer - observe increased run time
2. Add a 5th step `archive` that depends on `visualize`
3. Break the dependency (remove `depends: [analyze]` from visualize) - what happens?
4. Add a `description` field to each step explaining its purpose
```

**File 2: `02-maestro/example1-simple-dag/workflow.yaml`**

```yaml
description:
  name: simple-dag
  description: Four-step sequential workflow demonstrating DAG dependencies

env:
  variables:
    SLEEP_TIME: 3

study:
  - name: prepare
    description: Generate input data for simulation
    run:
      cmd: |
        bash $(SPECROOT)/scripts/prepare.sh $(OUTPUT_PATH)/input.dat
        echo "Prepared input data at $(OUTPUT_PATH)/input.dat"

  - name: simulate
    description: Run simulation using prepared data
    run:
      cmd: |
        python $(SPECROOT)/scripts/simulate.py \
          $(prepare.workspace)/input.dat \
          $(OUTPUT_PATH)/results.txt \
          $(SLEEP_TIME)
        echo "Simulation complete, results at $(OUTPUT_PATH)/results.txt"
      depends: [prepare]

  - name: analyze
    description: Analyze simulation results
    run:
      cmd: |
        python $(SPECROOT)/scripts/analyze.py \
          $(simulate.workspace)/results.txt \
          $(OUTPUT_PATH)/summary.txt
        echo "Analysis complete, summary at $(OUTPUT_PATH)/summary.txt"
      depends: [simulate]

  - name: visualize
    description: Create plots from analysis
    run:
      cmd: |
        python $(SPECROOT)/scripts/visualize.py \
          $(analyze.workspace)/summary.txt \
          $(OUTPUT_PATH)/plot.txt
        echo "Visualization complete, plot at $(OUTPUT_PATH)/plot.txt"
      depends: [analyze]
```

**File 3: `02-maestro/example1-simple-dag/scripts/prepare.sh`**

```bash
#!/bin/bash
# Generate sample input data

OUTPUT_FILE="$1"

echo "Generating input data..."

# Create simple input file with 10 data points
for i in {1..10}; do
  echo "$i $((i * i))" >> "$OUTPUT_FILE"
done

echo "Generated 10 data points in $OUTPUT_FILE"
```

**File 4: `02-maestro/example1-simple-dag/scripts/simulate.py`**

```python
#!/usr/bin/env python3
"""Simple simulation that processes input data."""

import sys
import time

def main():
    if len(sys.argv) != 4:
        print("Usage: simulate.py <input_file> <output_file> <sleep_time>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sleep_time = int(sys.argv[3])

    print(f"Reading input from {input_file}")

    # Read input data
    with open(input_file, 'r') as f:
        data = [line.strip().split() for line in f]

    # Simulate work
    print(f"Simulating work (sleeping {sleep_time}s)...")
    time.sleep(sleep_time)

    # Process data (simple transformation)
    results = []
    for x, y in data:
        x_val = int(x)
        y_val = int(y)
        result = y_val * 2  # Simple transformation
        results.append(f"{x_val} {y_val} {result}")

    # Write results
    with open(output_file, 'w') as f:
        f.write("# x y result\n")
        for line in results:
            f.write(line + '\n')

    print(f"Simulation complete. Results written to {output_file}")

if __name__ == "__main__":
    main()
```

**File 5: `02-maestro/example1-simple-dag/scripts/analyze.py`**

```python
#!/usr/bin/env python3
"""Analyze simulation results."""

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: analyze.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Analyzing results from {input_file}")

    # Read simulation results
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('#')]

    # Parse results
    results = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            results.append(int(parts[2]))

    # Calculate statistics
    if results:
        mean = sum(results) / len(results)
        min_val = min(results)
        max_val = max(results)

        # Write summary
        with open(output_file, 'w') as f:
            f.write(f"Analysis Summary\n")
            f.write(f"================\n")
            f.write(f"Count: {len(results)}\n")
            f.write(f"Mean:  {mean:.2f}\n")
            f.write(f"Min:   {min_val}\n")
            f.write(f"Max:   {max_val}\n")

        print(f"Analysis complete. Summary written to {output_file}")
    else:
        print("No results to analyze!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**File 6: `02-maestro/example1-simple-dag/scripts/visualize.py`**

```python
#!/usr/bin/env python3
"""Create visualization from analysis summary."""

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: visualize.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Creating visualization from {input_file}")

    # Read analysis summary
    with open(input_file, 'r') as f:
        summary = f.read()

    # Create simple text-based "plot" (in real workflow, would use matplotlib)
    with open(output_file, 'w') as f:
        f.write("Visualization Output\n")
        f.write("====================\n\n")
        f.write("Analysis Summary:\n")
        f.write(summary)
        f.write("\n")
        f.write("[In a real workflow, this would be a PNG/PDF plot]\n")

    print(f"Visualization complete. Plot written to {output_file}")

if __name__ == "__main__":
    main()
```

**Verification:**

Run: `ls -R 02-maestro/example1-simple-dag`
Expected: Shows workflow.yaml, README.md, and scripts/ directory with 4 scripts

Run: `cd 02-maestro/example1-simple-dag && maestro run workflow.yaml`
Expected: Creates timestamped directory, runs 4 steps sequentially

Run: `maestro status $(ls -t | grep workflow_ | head -1)`
Expected: Shows all 4 steps with FINISHED state

Run: `cat $(ls -td workflow_*/ | head -1)/visualize/plot.txt`
Expected: Shows visualization output with analysis summary

Run: `bash scripts/prepare.sh /tmp/test.dat && wc -l /tmp/test.dat`
Expected: Returns `10` (10 data points generated)

**Commit:**

```bash
git add 02-maestro/example1-simple-dag/
git commit -m "feat(maestro): add simple-dag example with 4-step sequential workflow

- Demonstrates DAG dependency resolution (prepare→simulate→analyze→visualize)
- Uses Maestro tokens (SPECROOT, OUTPUT_PATH, workspace references)
- Includes working Python/bash scripts for each step
- Runs on Perlmutter login nodes without Slurm submission
- README explains workflow structure and execution
- Scripts use filesystem-based data passing between steps"
```

<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create example2-param-sweeps with parameter variations and dependencies

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `02-maestro/example2-param-sweeps/workflow.yaml`
- Create: `02-maestro/example2-param-sweeps/README.md`
- Create: `02-maestro/example2-param-sweeps/scripts/run_simulation.py`
- Create: `02-maestro/example2-param-sweeps/scripts/aggregate_results.py`

**Implementation:**

Create a workflow demonstrating parameter sweeps combined with workflow dependencies, showing how Maestro expands parameter combinations while maintaining DAG structure.

**File 1: `02-maestro/example2-param-sweeps/README.md`**

```markdown
# Example 2: Parameter Sweeps with Dependencies

**Learning Objectives:**
- Define parameter sweeps using `global.parameters`
- Combine parameter variations with workflow dependencies
- Use wildcard dependencies `[step_*]` to wait for all parameter instances
- Aggregate results across parameter combinations

**Concepts:** Parameter expansion, parameterized workflows, funnel dependencies, result aggregation

## Workflow Structure

```
[run_simulation SIZE=10] ─┐
[run_simulation SIZE=20] ─┼─→ [aggregate_results]
[run_simulation SIZE=30] ─┘
```

Maestro automatically expands parameter combinations:
- 3 `run_simulation` jobs (one per SIZE value)
- 1 `aggregate_results` job (waits for all SIZE runs via wildcard)

## Parameter Sweep Mechanics

**global.parameters block:**
```yaml
global.parameters:
  SIZE:
    values: [10, 20, 30]
    label: SIZE.%%
```

**Effect:**
- Any step referencing `$(SIZE)` runs once per value
- Maestro creates SIZE-specific workspaces automatically
- Label determines directory naming (e.g., `SIZE.10`, `SIZE.20`, `SIZE.30`)

**Wildcard dependencies:**
```yaml
depends: [run_simulation_*]
```
Waits for ALL parameter instances of `run_simulation` before starting.

## Files

- `workflow.yaml` - Maestro workflow with parameter sweep
- `scripts/run_simulation.py` - Parameterized simulation
- `scripts/aggregate_results.py` - Collects results across all SIZE values

## Running on Perlmutter

```bash
module load python
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example2-param-sweeps
maestro run workflow.yaml
```

**Expected directory structure:**
```
workflow_20260319-150000/
├── run_simulation_SIZE.10/
│   └── output.txt
├── run_simulation_SIZE.20/
│   └── output.txt
├── run_simulation_SIZE.30/
│   └── output.txt
└── aggregate_results/
    └── summary.txt
```

**View aggregated results:**
```bash
cat workflow_20260319-150000/aggregate_results/summary.txt
```

## Key Concepts Demonstrated

1. **Parameter expansion:** One step definition creates multiple jobs
2. **Funnel dependency:** `depends: [step_*]` waits for all parameter instances
3. **Workspace isolation:** Each parameter combination gets separate directory
4. **Result aggregation:** Final step collects outputs from all parameter runs

## Expected Output

```
$ maestro run workflow.yaml
[TIMESTAMP] INFO: Loading specification from workflow.yaml
[TIMESTAMP] INFO: Launching study workflow...
[TIMESTAMP] INFO: Study workflow launched successfully.

$ maestro status workflow_20260319-150000
Step Name                    | State     | Run Time | Elapsed Time
-----------------------------|-----------|----------|-------------
run_simulation_SIZE.10       | FINISHED  | 1s       | 1s
run_simulation_SIZE.20       | FINISHED  | 2s       | 2s
run_simulation_SIZE.30       | FINISHED  | 3s       | 3s
aggregate_results            | FINISHED  | 1s       | 1s
```

Note: `run_simulation` jobs run in parallel (if resources available), then `aggregate_results` runs after all complete.

## Exercises

1. Add a second parameter (e.g., `TIMESTEP: [1, 5, 10]`) - how many jobs run?
2. Modify `run_simulation` to use both SIZE and TIMESTEP
3. Remove the wildcard (`depends: [run_simulation]`) - what error occurs?
4. Add a visualization step that depends on `aggregate_results`
5. Change SIZE values to `[100, 200, 300, 400, 500]` - verify scaling

## Comparison to signac

**signac approach:**
```python
# Define parameter space
project.open_job({"size": 10, "timestep": 1}).init()
project.open_job({"size": 20, "timestep": 1}).init()
# ... manual submission for each combination
```

**Maestro approach:**
```yaml
global.parameters:
  SIZE:
    values: [10, 20]
  TIMESTEP:
    values: [1, 5]
# Automatic expansion + dependency management
```

Maestro adds workflow orchestration to parameter organization.

## Known Limitations

**Workspace path construction:** The aggregate_results step uses `$(SPECROOT)/../../$(WORKSPACE)` to construct the path to parameter-specific workspaces. This relative path construction may be fragile depending on Maestro's working directory behavior. In production workflows, consider using absolute paths or environment variables for more robust path handling.
```

**File 2: `02-maestro/example2-param-sweeps/workflow.yaml`**

```yaml
description:
  name: param-sweep
  description: Parameter sweep with workflow dependencies and result aggregation

env:
  variables:
    OUTPUT_DIR: $(WORKSPACE)

global.parameters:
  SIZE:
    values: [10, 20, 30]
    label: SIZE.%%

study:
  - name: run_simulation
    description: Run simulation for each SIZE value
    run:
      cmd: |
        python $(SPECROOT)/scripts/run_simulation.py \
          --size $(SIZE) \
          --output $(OUTPUT_PATH)/output.txt
        echo "Completed simulation for SIZE=$(SIZE)"

  - name: aggregate_results
    description: Aggregate results from all SIZE values
    run:
      cmd: |
        python $(SPECROOT)/scripts/aggregate_results.py \
          --workspace $(SPECROOT)/../../$(WORKSPACE) \
          --pattern "run_simulation_SIZE.*/output.txt" \
          --output $(OUTPUT_PATH)/summary.txt
        echo "Aggregation complete, summary at $(OUTPUT_PATH)/summary.txt"
      depends: [run_simulation_*]
```

**File 3: `02-maestro/example2-param-sweeps/scripts/run_simulation.py`**

```python
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
```

**File 4: `02-maestro/example2-param-sweeps/scripts/aggregate_results.py`**

```python
#!/usr/bin/env python3
"""Aggregate results from all parameter sweep runs."""

import argparse
import glob
import os
import re

def parse_output_file(filepath):
    """Extract statistics from simulation output file."""
    data = {}
    with open(filepath, 'r') as f:
        for line in f:
            if 'SIZE=' in line:
                match = re.search(r'SIZE=(\d+)', line)
                if match:
                    data['size'] = int(match.group(1))
            elif 'Mean:' in line:
                data['mean'] = float(line.split(':')[1].strip())
            elif 'Min:' in line:
                data['min'] = int(line.split(':')[1].strip())
            elif 'Max:' in line:
                data['max'] = int(line.split(':')[1].strip())
    return data

def main():
    parser = argparse.ArgumentParser(description='Aggregate parameter sweep results')
    parser.add_argument('--workspace', required=True, help='Workspace directory containing run directories')
    parser.add_argument('--pattern', required=True, help='Glob pattern for output files')
    parser.add_argument('--output', required=True, help='Output summary file')
    args = parser.parse_args()

    print(f"Searching for results in {args.workspace}")

    # Find all output files matching pattern
    search_pattern = os.path.join(args.workspace, args.pattern)
    output_files = glob.glob(search_pattern)

    print(f"Found {len(output_files)} result files")

    if not output_files:
        print(f"ERROR: No files matching pattern {search_pattern}")
        return 1

    # Parse all results
    all_results = []
    for filepath in sorted(output_files):
        data = parse_output_file(filepath)
        if data:
            all_results.append(data)
            print(f"  Parsed: SIZE={data.get('size', '?')} Mean={data.get('mean', '?'):.2f}")

    # Write aggregated summary
    with open(args.output, 'w') as f:
        f.write("Aggregated Results Across All SIZE Values\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total parameter combinations: {len(all_results)}\n\n")
        f.write("Per-Parameter Results:\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'SIZE':<10} {'Mean':<10} {'Min':<10} {'Max':<10}\n")
        f.write("-" * 50 + "\n")

        for result in sorted(all_results, key=lambda x: x.get('size', 0)):
            f.write(f"{result['size']:<10} {result['mean']:<10.2f} {result['min']:<10} {result['max']:<10}\n")

        # Overall statistics
        if all_results:
            all_means = [r['mean'] for r in all_results]
            overall_mean = sum(all_means) / len(all_means)

            f.write("\n" + "-" * 50 + "\n")
            f.write(f"Overall mean across all SIZE values: {overall_mean:.2f}\n")

    print(f"Aggregation complete. Summary written to {args.output}")

if __name__ == "__main__":
    main()
```

**Verification:**

Run: `ls -R 02-maestro/example2-param-sweeps`
Expected: Shows workflow.yaml, README.md, and scripts/ directory with 2 scripts

Run: `cd 02-maestro/example2-param-sweeps && maestro run workflow.yaml`
Expected: Creates timestamped directory with 4 subdirectories (3 run_simulation + 1 aggregate)

Run: `maestro status $(ls -t | grep workflow_ | head -1)`
Expected: Shows 3 `run_simulation_SIZE.*` jobs + 1 `aggregate_results` job, all FINISHED

Run: `cat $(ls -td workflow_*/ | head -1)/aggregate_results/summary.txt`
Expected: Shows aggregated results table with 3 rows (SIZE=10, 20, 30)

Run: `ls $(ls -td workflow_*/ | head -1)/ | grep run_simulation | wc -l`
Expected: Returns `3` (three parameter instances)

**Commit:**

```bash
git add 02-maestro/example2-param-sweeps/
git commit -m "feat(maestro): add param-sweeps example demonstrating parameter expansion

- Shows global.parameters block with SIZE values [10, 20, 30]
- Demonstrates wildcard dependency (depends: [run_simulation_*])
- Includes aggregation step collecting results across parameter space
- Parameterized simulation with reproducible random results
- README explains funnel pattern and parameter mechanics
- Compares Maestro parameter sweeps to signac approach"
```

<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create example3-slurm-config with Perlmutter-specific batch configuration

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5, wf-seminar.AC5.1

**Files:**
- Create: `02-maestro/example3-slurm-config/workflow.yaml`
- Create: `02-maestro/example3-slurm-config/README.md`
- Create: `02-maestro/example3-slurm-config/scripts/compute.py`

**Implementation:**

Create a workflow demonstrating Perlmutter-specific Slurm configuration including partitions, accounts, QOS, and resource specifications.

**File 1: `02-maestro/example3-slurm-config/README.md`**

```markdown
# Example 3: Perlmutter-Specific Slurm Configuration

**Learning Objectives:**
- Configure Maestro `batch` block for Slurm on Perlmutter
- Specify per-step resource requirements (nodes, procs, walltime)
- Use `$(LAUNCHER)` token for scheduler abstraction
- Submit workflows to Perlmutter batch queues

**Concepts:** Slurm batch configuration, resource specification, scheduler job submission, HPC queue management

## Workflow Structure

```
setup (local) → compute (Slurm job) → postprocess (local)
```

- `setup`: Runs on login node, prepares input
- `compute`: Submits to Slurm, runs on compute nodes
- `postprocess`: Runs on login node, analyzes results

## Perlmutter Configuration

**System details for Maestro:**
- **Host:** `perlmutter`
- **Scheduler:** Slurm
- **Partitions:** `regular` (default), `debug` (fast scheduling), `shared` (fractional nodes)
- **Account:** Your NERSC repository (e.g., `m1234`)
- **QOS:** `regular` (default), `debug` (2h limit, faster queue)

**Maestro batch block:**
```yaml
batch:
  type: slurm
  host: perlmutter
  bank: m1234             # Replace with your account
  queue: regular          # or 'debug' for testing
```

## Resource Specification

**Per-step resources in `run` block:**
```yaml
run:
  cmd: $(LAUNCHER) python compute.py
  nodes: 1                # Number of nodes
  procs: 64               # Cores per node (up to 128 on CPU nodes)
  walltime: "00:10:00"    # HH:MM:SS format
```

**Maestro converts to Slurm directives:**
```bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --time=00:10:00
```

## $(LAUNCHER) Token

Maestro provides `$(LAUNCHER)` to abstract scheduler-specific launch commands:

**On Slurm:** `$(LAUNCHER)` → `srun --ntasks=$(PROCS)`
**On Flux:** `$(LAUNCHER)` → `flux run -n $(PROCS)`

**Why use $(LAUNCHER):**
- Portability across schedulers
- Correct task binding automatically
- Avoids hardcoded `srun` commands

## Files

- `workflow.yaml` - Maestro workflow with Slurm configuration
- `scripts/compute.py` - Parallel computation using MPI (simulated)

## Running on Perlmutter

**IMPORTANT:** Update `workflow.yaml` with your NERSC account before running!

```yaml
batch:
  bank: m1234  # CHANGE THIS to your account (e.g., m4408)
```

**Submit workflow:**
```bash
module load python
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example3-slurm-config
maestro run workflow.yaml
```

**Monitor job status:**
```bash
# Maestro status (shows workflow progress)
maestro status workflow_20260319-160000

# Slurm queue (shows submitted jobs)
squeue -u $USER
```

**View Slurm script generated by Maestro:**
```bash
cat workflow_20260319-160000/compute/compute.slurm.sh
```

**View job output:**
```bash
# Slurm stdout
cat workflow_20260319-160000/compute/compute.out

# Slurm stderr
cat workflow_20260319-160000/compute/compute.err

# Result file
cat workflow_20260319-160000/compute/result.txt
```

## Key Concepts Demonstrated

1. **Batch configuration:** Central `batch` block applies to all Slurm steps
2. **Per-step resources:** `nodes`, `procs`, `walltime` specified in each step's `run` block
3. **Mixed execution:** Some steps on login nodes, some on compute nodes
4. **Automatic submission:** Maestro generates and submits `.slurm.sh` scripts
5. **Scheduler abstraction:** `$(LAUNCHER)` enables portability

## Expected Output

```
$ maestro run workflow.yaml
[TIMESTAMP] INFO: Loading specification from workflow.yaml
[TIMESTAMP] INFO: Launching study workflow...
[TIMESTAMP] INFO: Submitting 'compute' to scheduler...
[TIMESTAMP] INFO: Study workflow launched successfully.

$ maestro status workflow_20260319-160000
Step Name       | State      | Run Time | Elapsed Time
----------------|------------|----------|-------------
setup           | FINISHED   | 1s       | 1s
compute         | RUNNING    | -        | 5m 30s
postprocess     | PENDING    | -        | -

[Wait for compute job to finish...]

$ maestro status workflow_20260319-160000
Step Name       | State      | Run Time | Elapsed Time
----------------|------------|----------|-------------
setup           | FINISHED   | 1s       | 1s
compute         | FINISHED   | 8m 45s   | 10m 00s
postprocess     | FINISHED   | 2s       | 2s
```

## Exercises

1. Change partition to `debug` and walltime to `00:05:00` - observe faster scheduling
2. Increase `nodes: 2` - verify Maestro generates correct SBATCH directives
3. Add `--constraint=cpu` to batch block for CPU-only nodes
4. Add a GPU step with `--gpus=1` in batch directives (requires custom SBATCH)
5. Remove `$(LAUNCHER)` and hardcode `srun` - compare generated scripts

## Perlmutter Best Practices

**✅ DO:**
- Use `regular` partition for production, `debug` for testing
- Specify walltime accurately (avoid killing long jobs or wasting allocation)
- Use `$(LAUNCHER)` instead of hardcoded `srun`
- Check account balance before submitting large sweeps

**❌ DON'T:**
- Hardcode scheduler commands (use `$(LAUNCHER)`)
- Submit to `debug` partition for long-running jobs (2h limit)
- Request more resources than needed (wastes allocation)
- Run compute workloads on login nodes (use Slurm)

## Troubleshooting

**Job stuck in PENDING:**
- Check queue: `squeue -u $USER`
- Verify account: `sacctmgr show assoc user=$USER`
- Check partition limits: `sinfo -p regular`

**Job fails immediately:**
- View error log: `cat workflow_*/compute/compute.err`
- Check Slurm script: `cat workflow_*/compute/compute.slurm.sh`
- Verify account in `batch` block matches your NERSC repository

**Can't find results:**
- Maestro creates timestamped directories: `ls -lt | grep workflow_`
- Each step has subdirectory: `ls workflow_20260319-160000/`
- Check both `.out` and `.err` files for messages
```

**File 2: `02-maestro/example3-slurm-config/workflow.yaml`**

```yaml
description:
  name: slurm-config
  description: Perlmutter-specific Slurm configuration demonstrating batch submission

env:
  variables:
    N_SAMPLES: 1000000

batch:
  type: slurm
  host: perlmutter
  bank: m4408              # CHANGE THIS to your NERSC account (e.g., m1234)
  queue: regular           # Use 'debug' for faster testing (2h limit)

study:
  - name: setup
    description: Prepare input data (runs on login node)
    run:
      cmd: |
        echo "Preparing input for computation with N_SAMPLES=$(N_SAMPLES)"
        echo "$(N_SAMPLES)" > $(OUTPUT_PATH)/input.txt
        echo "Setup complete at $(OUTPUT_PATH)/input.txt"

  - name: compute
    description: Run parallel computation (submits to Slurm)
    run:
      cmd: |
        echo "Starting computation with $(N_SAMPLES) samples"
        echo "Running on $(hostname) with $(nproc) cores"
        $(LAUNCHER) python $(SPECROOT)/scripts/compute.py \
          --input $(setup.workspace)/input.txt \
          --output $(OUTPUT_PATH)/result.txt \
          --procs $(PROCS)
        echo "Computation complete, results at $(OUTPUT_PATH)/result.txt"
      depends: [setup]
      nodes: 1
      procs: 64              # Request 64 cores (half of a Perlmutter CPU node)
      walltime: "00:10:00"   # 10 minutes (adjust based on workload)

  - name: postprocess
    description: Analyze results (runs on login node)
    run:
      cmd: |
        echo "Analyzing results from computation"
        RESULT_VALUE=$(cat $(compute.workspace)/result.txt | grep "Result:" | awk '{print $2}')
        echo "Computation result: $RESULT_VALUE"
        echo "Analysis complete" > $(OUTPUT_PATH)/summary.txt
        echo "  Input: $(N_SAMPLES) samples" >> $(OUTPUT_PATH)/summary.txt
        echo "  Result: $RESULT_VALUE" >> $(OUTPUT_PATH)/summary.txt
        echo "Summary written to $(OUTPUT_PATH)/summary.txt"
      depends: [compute]
```

**File 3: `02-maestro/example3-slurm-config/scripts/compute.py`**

```python
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
```

**Verification:**

Run: `ls -R 02-maestro/example3-slurm-config`
Expected: Shows workflow.yaml, README.md, and scripts/ directory

Run: `grep "bank:" 02-maestro/example3-slurm-config/workflow.yaml`
Expected: Shows `bank: m4408` (example account)

Run: `grep "$(LAUNCHER)" 02-maestro/example3-slurm-config/workflow.yaml`
Expected: Shows launcher token usage in compute step

Run: `cd 02-maestro/example3-slurm-config && maestro run workflow.yaml --dry`
Expected: Dry-run mode shows workflow structure without submitting (note: --dry flag may require checking Maestro docs for exact syntax)

**Note:** Full verification requires submitting to Slurm, which depends on user having valid NERSC account. Repository README should note: "Example 3 requires updating `bank` field with your NERSC account."

**Commit:**

```bash
git add 02-maestro/example3-slurm-config/
git commit -m "feat(maestro): add slurm-config example with Perlmutter batch configuration

- Demonstrates batch block with Slurm settings (type, host, bank, queue)
- Shows per-step resource specification (nodes, procs, walltime)
- Uses $(LAUNCHER) token for scheduler abstraction
- Mixed execution: login node steps + Slurm-submitted steps
- README includes Perlmutter best practices and troubleshooting
- Scripts show parallel computation pattern with srun
- Documents account/partition selection for NERSC"
```

<!-- END_TASK_4 -->
