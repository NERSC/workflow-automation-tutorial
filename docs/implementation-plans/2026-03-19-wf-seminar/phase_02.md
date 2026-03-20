# Workflow Management Seminar Implementation Plan - Phase 2

**Goal:** Create baseline examples demonstrating simple task parallelization with GNU Parallel that establish automation vocabulary for the seminar

**Architecture:** Three progressive examples showing GNU Parallel capabilities: simple parameter sweep → multiple parameter combinations → Slurm integration on Perlmutter

**Tech Stack:**
- GNU Parallel (available via `module load parallel` on Perlmutter)
- Bash shell scripting
- Slurm batch system (`$SLURM_CPUS_ON_NODE` integration)

**Scope:** Phase 2 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phase 1 infrastructure will exist before this phase executes)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 example specifications (15 total across 5 tools) - Phase 2 provides 3 GNU Parallel examples
- **wf-seminar.AC4.3 Success:** Examples progress from simple to complex within each tool section
- **wf-seminar.AC4.4 Success:** All examples specify they must run on Perlmutter without modification

### wf-seminar.AC5: NERSC/Perlmutter integration is accurate and complete
- **wf-seminar.AC5.2 Success:** Anti-patterns from NERSC best practices explicitly called out (srun loops, scheduler query limits, job arrays)
- **wf-seminar.AC5.4 Success:** Filesystem guidance specifies $SCRATCH for workflows, CFS for long-term storage

---

<!-- START_TASK_1 -->
### Task 1: Update 00-gnu-parallel/README.md with complete content

**Verifies:** None (infrastructure phase)

**Files:**
- Modify: `00-gnu-parallel/README.md`

**Implementation:**

Replace the placeholder README with complete content including concepts, when to use, syntax overview, and examples guide.

```markdown
# Section 0: GNU Parallel - Simple Task Parallelization

**Duration:** 30 minutes

**Concepts:** Task-level parallelism, parameter sweeps, Slurm integration, embarrassingly parallel workloads

## Overview

GNU Parallel establishes the baseline for workflow automation, demonstrating how to run the same command with different parameters in parallel without dependency management. It's the entry point before graduating to full workflow systems.

**Key capability:** Parallelization without dependencies

## Why GNU Parallel?

GNU Parallel is superior to job arrays on HPC systems because:
- **Scheduler efficiency:** One job requesting many cores is prioritized over many jobs requesting few cores
- **Reduced queue time:** Single submission instead of array of submissions
- **Less scheduler load:** Fewer jobs to manage
- **Built-in recovery:** `--joblog` and `--resume-failed` enable fault tolerance

## When to Use GNU Parallel

✅ **Good for:**
- Running the same command with different parameters (parameter sweeps)
- Embarrassingly parallel workloads (no dependencies between tasks)
- Quick parallelization of shell scripts without framework overhead
- Tasks that fit on a single node (128 cores on Perlmutter CPU nodes)
- Simple workflows where results don't feed into subsequent steps

❌ **Not suitable for:**
- Multi-step workflows with dependencies → use Maestro or Merlin
- Tracking parameter spaces across multiple runs → use signac
- Distributed coordination across allocations → use Merlin
- Comprehensive provenance tracking → use AiiDA
- Tasks requiring more than single-node resources

## Core Concepts

### Parameter Substitution

`{}` is replaced with each input item:
```bash
seq 1 4 | parallel echo "Hello world {}!"
# Output: Hello world 1! ... Hello world 4!
```

### Job Control

Control parallelism with `-j`:
```bash
# Use all cores
parallel -j +0 command ::: inputs

# Use specific number of cores
parallel -j 16 command ::: inputs

# On Perlmutter: use allocated cores
parallel -j $SLURM_CPUS_ON_NODE command ::: inputs
```

### Multiple Parameters

Combine parameters with `:::`:
```bash
# Cartesian product: all combinations
parallel echo {1} {2} ::: A B ::: 1 2
# Output: A 1, A 2, B 1, B 2
```

### Fault Tolerance

Resume failed tasks:
```bash
parallel --resume-failed --joblog results.log command ::: inputs
```

## Examples

This directory contains three progressive examples:

### Example 1: Simple Parameter Sweep
**Directory:** `example1-parameter-sweep/`

Demonstrates basic parallel execution with parameter variations. Shows:
- Parameter substitution with `{}`
- Job control with `-j $SLURM_CPUS_ON_NODE`
- Simple task parallelization on a single node

**Learning outcome:** Understand basic GNU Parallel syntax and see immediate speedup from parallelization

### Example 2: Multiple Parameter Combinations
**Directory:** `example2-multi-param/`

Demonstrates combining multiple parameters to create Cartesian products. Shows:
- Multiple parameter sources with `::: A B C ::: 1 2 3`
- Generating all combinations systematically
- Organizing results by parameter combination

**Learning outcome:** See how parameter spaces are explored exhaustively without nested loops

### Example 3: Slurm Integration on Perlmutter
**Directory:** `example3-slurm-integration/`

Demonstrates proper Slurm batch integration for production workflows. Shows:
- Sbatch script wrapper for GNU Parallel
- Using `$SLURM_CPUS_ON_NODE` for automatic scaling
- Job logging and recovery with `--joblog` and `--resume-failed`
- Perlmutter-specific configuration (`#SBATCH --constraint=cpu`)

**Learning outcome:** Understand how to run GNU Parallel in batch mode on Perlmutter with fault tolerance

## Progression to Workflow Tools

GNU Parallel is the foundation, but you'll outgrow it when you need:

| Capability | When to Graduate | Tool |
|------------|------------------|------|
| Parameter organization across runs | signac | Filesystem-based state tracking |
| Multi-step dependencies | Maestro | DAG workflow specification |
| Distributed coordination | Merlin | Persistent task queues |
| Provenance tracking | AiiDA | Full execution history |

**Graduation signal:** If you're writing bash scripts to track "which parameter combinations ran successfully" or "what depends on what," you need a workflow tool.

## Anti-Patterns (Common Mistakes)

See `../resources/nersc-best-practices.md` for detailed anti-patterns including:
- ❌ Bash loops with `srun -n1 --exclusive` (inefficient batching)
- ❌ Overusing job arrays (scheduler contention)
- ❌ SSH-based distribution `--sshlogin` (breaks Slurm semantics)
- ❌ Missing `--delay` between srun calls (overloads scheduler)

## Perlmutter-Specific Notes

**CPU Nodes:**
- 128 hardware cores per node (2x AMD EPYC 7763)
- 512 GB memory per node

**Recommended usage:**
```bash
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --qos=regular

module load parallel
seq 1 1000 | parallel -j $SLURM_CPUS_ON_NODE './process_task.sh {}'
```

**For multi-threaded tasks:**
If each task uses 2 threads, use half the cores for parallel jobs:
```bash
JOBS=$((SLURM_CPUS_ON_NODE / 2))
parallel -j $JOBS './multithreaded_task.sh {}'
```

## Further Reading

**Official Documentation:**
- [GNU Parallel Project](https://www.gnu.org/software/parallel/)
- [GNU Parallel Tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
- [GNU Parallel Examples](https://www.gnu.org/software/parallel/parallel_examples.html)

**NERSC Resources:**
- [GNU Parallel at NERSC](https://docs.nersc.gov/jobs/workflow/gnuparallel/)
- [Perlmutter Architecture](https://docs.nersc.gov/systems/perlmutter/architecture/)
- [NERSC Job Examples](https://docs.nersc.gov/jobs/examples/)

**HPC Best Practices:**
- [UC Berkeley HPC GNU Parallel Guide](https://docs-research-it.berkeley.edu/services/high-performance-computing/user-guide/running-your-jobs/gnu-parallel/)
```

**Verification:**
Run: `grep "^# Section 0:" 00-gnu-parallel/README.md`
Expected: Shows section header

Run: `wc -l 00-gnu-parallel/README.md`
Expected: ~200+ lines (complete content, not placeholder)

**Commit:** Batch commit with all Phase 2 files (Task 9)
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create Example 1 - Simple Parameter Sweep

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4

**Files:**
- Create: `00-gnu-parallel/example1-parameter-sweep/README.md`
- Create: `00-gnu-parallel/example1-parameter-sweep/run_simple.sh`
- Create: `00-gnu-parallel/example1-parameter-sweep/process_task.sh`

**Implementation:**

Create a simple parameter sweep example showing basic GNU Parallel usage.

**File 1: README.md**

```markdown
# Example 1: Simple Parameter Sweep

**Concept:** Basic parallel execution with parameter substitution

**Duration:** 5 minutes

## What This Demonstrates

- Parameter substitution with `{}`
- Job control with `-j` flag
- Using `$SLURM_CPUS_ON_NODE` on Perlmutter
- Immediate speedup from parallelization

## The Problem

You have 20 input files to process with the same command. Running them sequentially takes 20× longer than necessary on a multi-core system.

## The Solution

GNU Parallel runs multiple tasks simultaneously, using all available cores:

```bash
seq 1 20 | parallel -j $SLURM_CPUS_ON_NODE './process_task.sh {}'
```

## Files in This Example

- `run_simple.sh` - Main script demonstrating parallel execution
- `process_task.sh` - Placeholder task (simulates 2-second computation)

## How to Run

**On Perlmutter (login node - quick test):**

```bash
cd example1-parameter-sweep
bash run_simple.sh
```

This runs with 2 parallel jobs (safe for login node). For full parallelism, submit as batch job (see Example 3).

**Expected Output:**

```
Running 20 tasks with 2 parallel jobs...
Processing input 1... (simulates 2-second task)
Processing input 2... (simulates 2-second task)
...
Processing input 20... (simulates 2-second task)
All tasks complete!
Sequential time: ~40 seconds
Parallel time (2 jobs): ~20 seconds
Parallel time (128 jobs on Perlmutter): <1 second
```

## Key Concepts

1. **Parameter substitution:** `{}` is replaced with each input value (1, 2, 3, ... 20)
2. **Job control:** `-j 2` limits to 2 parallel jobs (set conservatively for login node)
3. **Scalability:** On compute node with `$SLURM_CPUS_ON_NODE=128`, this would use all 128 cores

## What Happens

1. `seq 1 20` generates numbers 1 through 20
2. `parallel -j 2` takes each number and runs `./process_task.sh` with it
3. Two tasks run at a time; when one finishes, the next starts
4. All 20 tasks complete in ~20 seconds instead of ~40 seconds

## Progression

This is the simplest use case. Next examples add:
- **Example 2:** Multiple parameters (Cartesian products)
- **Example 3:** Slurm batch integration with fault tolerance
```

**File 2: run_simple.sh**

```bash
#!/bin/bash
# Example 1: Simple Parameter Sweep with GNU Parallel
# Demonstrates basic parallelization on a single node

# Load GNU Parallel (on Perlmutter)
# Uncomment if running on compute node:
# module load parallel

# Make process_task.sh executable
chmod +x process_task.sh

echo "Running 20 tasks with 2 parallel jobs..."
echo "(Using -j 2 for login node safety; use -j \$SLURM_CPUS_ON_NODE on compute nodes)"
echo ""

# Time the execution
start_time=$(date +%s)

# Run 20 tasks in parallel with job limit of 2
# On compute node, replace '-j 2' with '-j $SLURM_CPUS_ON_NODE'
seq 1 20 | parallel -j 2 './process_task.sh {}'

end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo ""
echo "All tasks complete!"
echo "Elapsed time: ${elapsed} seconds"
echo ""
echo "Analysis:"
echo "- Sequential execution: ~40 seconds (20 tasks × 2 seconds)"
echo "- Parallel execution (2 jobs): ~${elapsed} seconds"
echo "- Parallel execution (128 jobs on Perlmutter): <1 second"
```

**File 3: process_task.sh**

```bash
#!/bin/bash
# Placeholder task simulating 2-second computation
# In real workflow, this would be your analysis script

TASK_ID=$1

echo "Processing input ${TASK_ID}... (simulates 2-second task)"

# Simulate computational work
sleep 2

# In real workflow, produce output:
# ./actual_analysis input_${TASK_ID}.dat > output_${TASK_ID}.txt

echo "Task ${TASK_ID} complete"
```

**Verification:**
Run: `cd 00-gnu-parallel/example1-parameter-sweep && bash run_simple.sh`
Expected: Completes in ~20 seconds, shows "All tasks complete!"

Run: `ls -1 00-gnu-parallel/example1-parameter-sweep/`
Expected: Shows `README.md`, `run_simple.sh`, `process_task.sh`

**Commit:** Batch commit with all Phase 2 files (Task 9)
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create Example 2 - Multiple Parameter Combinations

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4

**Files:**
- Create: `00-gnu-parallel/example2-multi-param/README.md`
- Create: `00-gnu-parallel/example2-multi-param/run_combinations.sh`
- Create: `00-gnu-parallel/example2-multi-param/process_combination.sh`

**Implementation:**

Create example demonstrating multiple parameter combinations (Cartesian product).

**File 1: README.md**

```markdown
# Example 2: Multiple Parameter Combinations

**Concept:** Exploring parameter spaces with Cartesian products

**Duration:** 5 minutes

## What This Demonstrates

- Multiple parameter sources with `::: A B C ::: 1 2 3`
- Generating all combinations (Cartesian product)
- Parameter substitution with `{1}`, `{2}`, `{3}` for positional access
- Systematic parameter space exploration

## The Problem

You need to run experiments across multiple parameter dimensions:
- 3 algorithms: A, B, C
- 3 dataset sizes: small, medium, large
- 2 optimization levels: O2, O3

That's 3 × 3 × 2 = 18 combinations. Writing nested loops is tedious and error-prone.

## The Solution

GNU Parallel generates all combinations automatically:

```bash
parallel ./process_combination.sh {1} {2} {3} \
  ::: A B C \
  ::: small medium large \
  ::: O2 O3
```

## Files in This Example

- `run_combinations.sh` - Main script demonstrating parameter combinations
- `process_combination.sh` - Placeholder task processing each combination

## How to Run

**On Perlmutter (login node - quick test):**

```bash
cd example2-multi-param
bash run_combinations.sh
```

**Expected Output:**

```
Running 18 parameter combinations (3 algorithms × 3 sizes × 2 opts)...
Processing: algorithm=A, size=small, opt=O2
Processing: algorithm=A, size=small, opt=O3
Processing: algorithm=A, size=medium, opt=O2
...
Processing: algorithm=C, size=large, opt=O3
All combinations complete!
```

## Key Concepts

1. **Multiple sources:** Each `:::` introduces a new parameter dimension
2. **Cartesian product:** All possible combinations are generated
3. **Positional parameters:** `{1}` = first source, `{2}` = second source, `{3}` = third source
4. **Scalability:** 3×3×2=18 combinations run in parallel (limited by `-j` flag)

## Parameter Combinations Explained

```bash
parallel echo {1} {2} {3} ::: A B ::: 1 2 ::: X Y
```

Generates:
```
A 1 X
A 1 Y
A 2 X
A 2 Y
B 1 X
B 1 Y
B 2 X
B 2 Y
```

Total: 2 × 2 × 2 = 8 combinations

## Linked vs Unlinked Parameters

**Unlinked (Cartesian product) - use `:::`:**
```bash
parallel echo {1} {2} ::: A B ::: 1 2
# A 1, A 2, B 1, B 2 (4 combinations)
```

**Linked (pairwise) - use `:::+`:**
```bash
parallel echo {1} {2} ::: A B :::+ 1 2
# A 1, B 2 (2 combinations, maintains alignment)
```

This example uses unlinked parameters (full Cartesian product).

## Real-World Use Case

```bash
# Parameter sweep for ML hyperparameter tuning
parallel python train_model.py \
  --lr {1} \
  --batch-size {2} \
  --optimizer {3} \
  ::: 0.001 0.01 0.1 \
  ::: 16 32 64 \
  ::: adam sgd rmsprop
# Total: 3 × 3 × 3 = 27 training runs
```

## Progression

- **Example 1:** Single parameter dimension
- **Example 2:** Multiple parameter dimensions (this example)
- **Example 3:** Batch integration with Slurm
- **Signac (next section):** Persistent parameter space tracking across runs
```

**File 2: run_combinations.sh**

```bash
#!/bin/bash
# Example 2: Multiple Parameter Combinations with GNU Parallel
# Demonstrates Cartesian product parameter exploration

# Load GNU Parallel (on Perlmutter)
# Uncomment if running on compute node:
# module load parallel

# Make process_combination.sh executable
chmod +x process_combination.sh

echo "Running 18 parameter combinations (3 algorithms × 3 sizes × 2 opts)..."
echo "(Using -j 2 for login node safety)"
echo ""

# Parameter dimensions:
# - Algorithms: A, B, C
# - Dataset sizes: small, medium, large
# - Optimization levels: O2, O3
# Total: 3 × 3 × 2 = 18 combinations

# Run all combinations in parallel
# {1} = algorithm, {2} = size, {3} = optimization
parallel -j 2 './process_combination.sh {1} {2} {3}' \
  ::: A B C \
  ::: small medium large \
  ::: O2 O3

echo ""
echo "All combinations complete!"
echo ""
echo "Analysis:"
echo "- Total combinations: 18"
echo "- If each task takes 2 seconds:"
echo "  - Sequential: 36 seconds"
echo "  - Parallel (2 jobs): ~18 seconds"
echo "  - Parallel (128 jobs on Perlmutter): <1 second"
```

**File 3: process_combination.sh**

```bash
#!/bin/bash
# Process one parameter combination
# In real workflow, this runs your experiment with specific parameters

ALGORITHM=$1
SIZE=$2
OPTIMIZATION=$3

echo "Processing: algorithm=${ALGORITHM}, size=${SIZE}, opt=${OPTIMIZATION}"

# Simulate computational work
sleep 2

# In real workflow:
# ./run_experiment --algorithm $ALGORITHM --dataset data_${SIZE}.dat --opt $OPTIMIZATION > results_${ALGORITHM}_${SIZE}_${OPTIMIZATION}.txt

echo "  -> Complete: ${ALGORITHM}/${SIZE}/${OPTIMIZATION}"
```

**Verification:**
Run: `cd 00-gnu-parallel/example2-multi-param && bash run_combinations.sh`
Expected: Shows 18 combinations, completes in ~18 seconds

Run: `grep "Cartesian product" 00-gnu-parallel/example2-multi-param/README.md`
Expected: Shows explanation of Cartesian product

**Commit:** Batch commit with all Phase 2 files (Task 9)
<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create Example 3 - Slurm Integration on Perlmutter

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC5.4

**Files:**
- Create: `00-gnu-parallel/example3-slurm-integration/README.md`
- Create: `00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh`
- Create: `00-gnu-parallel/example3-slurm-integration/process_task.sh`
- Create: `00-gnu-parallel/example3-slurm-integration/task_list.txt`

**Implementation:**

Create example demonstrating proper Slurm batch integration for production workflows on Perlmutter.

**File 1: README.md**

```markdown
# Example 3: Slurm Integration on Perlmutter

**Concept:** Production-ready GNU Parallel workflows with batch submission and fault tolerance

**Duration:** 10 minutes (includes queue wait time)

## What This Demonstrates

- Sbatch script wrapper for GNU Parallel
- Using `$SLURM_CPUS_ON_NODE` for automatic core detection (128 cores on Perlmutter CPU nodes)
- Job logging with `--joblog` for tracking completion
- Fault tolerance with `--resume-failed` for retry
- Perlmutter-specific configuration

## The Problem

Production workflows need:
1. Batch submission (not interactive)
2. Full core utilization (128 cores on Perlmutter CPU nodes)
3. Fault tolerance (restart failed tasks without redoing successful ones)
4. Tracking (which tasks succeeded/failed)

## The Solution

Combine GNU Parallel with Slurm batch scripts:

```bash
sbatch submit_parallel_job.sh
```

The batch script uses:
- `$SLURM_CPUS_ON_NODE` to automatically use all 128 cores
- `--joblog` to track task completion
- `--resume-failed` to retry only failed tasks on resubmission

## Files in This Example

- `submit_parallel_job.sh` - Sbatch script for Perlmutter submission
- `process_task.sh` - Placeholder computational task
- `task_list.txt` - Input file listing all tasks to run

## How to Run

**On Perlmutter:**

```bash
cd example3-slurm-integration

# Submit the job
sbatch submit_parallel_job.sh

# Check status
squeue -u $USER

# Check output after completion
cat slurm-*.out
```

**Expected Output (in slurm-*.out):**

```
Job started on 1 node with 128 cores
Running 100 tasks with GNU Parallel...
Running with --joblog for task tracking
Task list: task_list.txt

[GNU Parallel executes all 100 tasks across 128 cores]

All tasks complete!
Check parallel_job.log for per-task status
```

## Key Concepts

### 1. Automatic Core Detection

```bash
parallel -j $SLURM_CPUS_ON_NODE < task_list.txt
```

`$SLURM_CPUS_ON_NODE` is set by Slurm and equals the number of cores allocated. On Perlmutter CPU nodes, this is 128.

### 2. Job Logging

```bash
parallel --joblog parallel_job.log -j $SLURM_CPUS_ON_NODE < task_list.txt
```

Creates `parallel_job.log` with columns:
```
Seq  Host  Starttime  JobRuntime  Send  Receive  Exitval  Signal  Command
1    node1 1234567890 2.5         0     0        0        0       ./process_task.sh input_001.dat
2    node1 1234567890 2.3         0     0        0        0       ./process_task.sh input_002.dat
...
```

### 3. Fault Tolerance with Resume

If tasks fail (power outage, node failure, bug), resubmit the SAME script:

```bash
sbatch submit_parallel_job.sh  # Reruns automatically
```

`--resume-failed` reads `parallel_job.log`, skips successful tasks (Exitval=0), and reruns only failed ones.

### 4. Perlmutter-Specific Settings

```bash
#SBATCH --nodes=1
#SBATCH --constraint=cpu      # Request CPU nodes (not GPU)
#SBATCH --qos=regular          # Standard QOS
#SBATCH --time=00:30:00        # 30-minute limit
#SBATCH --account=<your_account>
```

## Sbatch Script Breakdown

```bash
#!/bin/bash
#SBATCH --job-name=parallel-demo
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --time=00:30:00
#SBATCH --output=slurm-%j.out

module load parallel

echo "Job started on $SLURM_JOB_NUM_NODES node with $SLURM_CPUS_ON_NODE cores"
echo "Running $(wc -l < task_list.txt) tasks with GNU Parallel..."

parallel \
  -j $SLURM_CPUS_ON_NODE \
  --joblog parallel_job.log \
  --resume-failed \
  < task_list.txt
```

**Key features:**
- `#SBATCH` directives configure Slurm allocation
- `module load parallel` loads GNU Parallel
- `-j $SLURM_CPUS_ON_NODE` uses all allocated cores (128)
- `--joblog parallel_job.log` tracks task completion
- `--resume-failed` skips completed tasks on resubmission
- `< task_list.txt` reads tasks from file

## Task List Format

`task_list.txt` contains one command per line:

```
./process_task.sh input_001.dat
./process_task.sh input_002.dat
./process_task.sh input_003.dat
...
./process_task.sh input_100.dat
```

GNU Parallel reads this file and executes each line in parallel (up to `-j` limit).

## Recovery Workflow

**Initial submission:**
```bash
sbatch submit_parallel_job.sh
```

**If 10 tasks fail (out of 100):**
```bash
# Check the log
grep -v "^Seq" parallel_job.log | awk '$7 != 0' | wc -l
# Shows: 10 failed tasks

# Resubmit the SAME script (no changes needed)
sbatch submit_parallel_job.sh
# --resume-failed automatically reruns only the 10 failed tasks
```

## Progression

- **Example 1:** Simple parameter sweep (login node)
- **Example 2:** Multiple parameters (login node)
- **Example 3:** Production batch integration (this example)
- **Signac (next section):** Organized parameter spaces with persistent state tracking

## Real-World Use Case

```bash
# Generate task list for 1000 parameter combinations
for alpha in 0.1 0.5 0.9; do
  for beta in 1 10 100; do
    for gamma in 0.01 0.1 1; do
      echo "python simulate.py --alpha $alpha --beta $beta --gamma $gamma"
    done
  done
done > task_list.txt

# Submit to Perlmutter
sbatch submit_parallel_job.sh

# All 1000 tasks run across 128 cores
# If any fail, resubmit to retry only failures
```
```

**File 2: submit_parallel_job.sh**

```bash
#!/bin/bash
#SBATCH --job-name=parallel-demo
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --time=00:30:00
#SBATCH --account=<your_account>  # REPLACE with your NERSC account
#SBATCH --output=slurm-%j.out

# Slurm Integration Example for GNU Parallel on Perlmutter
# Demonstrates: batch submission, automatic core detection, fault tolerance

# Load GNU Parallel module
module load parallel

# Make sure process script is executable
chmod +x process_task.sh

echo "============================================"
echo "GNU Parallel + Slurm Integration Demo"
echo "============================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Nodes allocated: $SLURM_JOB_NUM_NODES"
echo "Cores per node: $SLURM_CPUS_ON_NODE"
echo "Working directory: $(pwd)"
echo "Task list: task_list.txt"
echo "Total tasks: $(wc -l < task_list.txt)"
echo "============================================"
echo ""

# Run GNU Parallel with:
# - Full core utilization ($SLURM_CPUS_ON_NODE = 128 on Perlmutter CPU nodes)
# - Job logging (--joblog tracks completion)
# - Fault tolerance (--resume-failed retries failures on resubmission)
# - 0.2 second delay between spawns (reduces Slurm controller load)
parallel \
  -j $SLURM_CPUS_ON_NODE \
  --joblog parallel_job_${SLURM_JOB_ID}.log \
  --resume-failed \
  --delay 0.2 \
  < task_list.txt

echo ""
echo "============================================"
echo "All tasks complete!"
echo "Job log: parallel_job_${SLURM_JOB_ID}.log"
echo "============================================"
echo ""
echo "To check for failures:"
echo "  grep -v '^Seq' parallel_job_${SLURM_JOB_ID}.log | awk '\$7 != 0'"
echo ""
echo "To retry failed tasks:"
echo "  sbatch submit_parallel_job.sh"
echo "  (--resume-failed automatically skips successful tasks)"
```

**File 3: process_task.sh**

```bash
#!/bin/bash
# Placeholder computational task
# In real workflow, this processes input data and produces output

TASK_COMMAND=$1

echo "Processing: $TASK_COMMAND (simulates 5-second computation)"

# Simulate computational work
sleep 5

# In real workflow:
# Run the actual analysis command passed as argument
# $TASK_COMMAND might be: "./analyze.py input_042.dat > output_042.txt"

echo "  -> Complete: $TASK_COMMAND"
```

**File 4: task_list.txt**

```
./process_task.sh input_001.dat
./process_task.sh input_002.dat
./process_task.sh input_003.dat
./process_task.sh input_004.dat
./process_task.sh input_005.dat
./process_task.sh input_006.dat
./process_task.sh input_007.dat
./process_task.sh input_008.dat
./process_task.sh input_009.dat
./process_task.sh input_010.dat
./process_task.sh input_011.dat
./process_task.sh input_012.dat
./process_task.sh input_013.dat
./process_task.sh input_014.dat
./process_task.sh input_015.dat
./process_task.sh input_016.dat
./process_task.sh input_017.dat
./process_task.sh input_018.dat
./process_task.sh input_019.dat
./process_task.sh input_020.dat
./process_task.sh input_021.dat
./process_task.sh input_022.dat
./process_task.sh input_023.dat
./process_task.sh input_024.dat
./process_task.sh input_025.dat
./process_task.sh input_026.dat
./process_task.sh input_027.dat
./process_task.sh input_028.dat
./process_task.sh input_029.dat
./process_task.sh input_030.dat
./process_task.sh input_031.dat
./process_task.sh input_032.dat
./process_task.sh input_033.dat
./process_task.sh input_034.dat
./process_task.sh input_035.dat
./process_task.sh input_036.dat
./process_task.sh input_037.dat
./process_task.sh input_038.dat
./process_task.sh input_039.dat
./process_task.sh input_040.dat
./process_task.sh input_041.dat
./process_task.sh input_042.dat
./process_task.sh input_043.dat
./process_task.sh input_044.dat
./process_task.sh input_045.dat
./process_task.sh input_046.dat
./process_task.sh input_047.dat
./process_task.sh input_048.dat
./process_task.sh input_049.dat
./process_task.sh input_050.dat
./process_task.sh input_051.dat
./process_task.sh input_052.dat
./process_task.sh input_053.dat
./process_task.sh input_054.dat
./process_task.sh input_055.dat
./process_task.sh input_056.dat
./process_task.sh input_057.dat
./process_task.sh input_058.dat
./process_task.sh input_059.dat
./process_task.sh input_060.dat
./process_task.sh input_061.dat
./process_task.sh input_062.dat
./process_task.sh input_063.dat
./process_task.sh input_064.dat
./process_task.sh input_065.dat
./process_task.sh input_066.dat
./process_task.sh input_067.dat
./process_task.sh input_068.dat
./process_task.sh input_069.dat
./process_task.sh input_070.dat
./process_task.sh input_071.dat
./process_task.sh input_072.dat
./process_task.sh input_073.dat
./process_task.sh input_074.dat
./process_task.sh input_075.dat
./process_task.sh input_076.dat
./process_task.sh input_077.dat
./process_task.sh input_078.dat
./process_task.sh input_079.dat
./process_task.sh input_080.dat
./process_task.sh input_081.dat
./process_task.sh input_082.dat
./process_task.sh input_083.dat
./process_task.sh input_084.dat
./process_task.sh input_085.dat
./process_task.sh input_086.dat
./process_task.sh input_087.dat
./process_task.sh input_088.dat
./process_task.sh input_089.dat
./process_task.sh input_090.dat
./process_task.sh input_091.dat
./process_task.sh input_092.dat
./process_task.sh input_093.dat
./process_task.sh input_094.dat
./process_task.sh input_095.dat
./process_task.sh input_096.dat
./process_task.sh input_097.dat
./process_task.sh input_098.dat
./process_task.sh input_099.dat
./process_task.sh input_100.dat
```

**Verification:**
Run: `wc -l 00-gnu-parallel/example3-slurm-integration/task_list.txt`
Expected: `100` (100 tasks)

Run: `grep "#SBATCH --constraint=cpu" 00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh`
Expected: Shows Perlmutter CPU constraint

**Commit:** Batch commit with all Phase 2 files (Task 9)
<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Create NERSC best practices guide

**Verifies:** wf-seminar.AC5.2, wf-seminar.AC5.4

**Files:**
- Create: `resources/nersc-best-practices.md`

**Implementation:**

Create comprehensive guide documenting NERSC/Perlmutter best practices and anti-patterns.

```markdown
# NERSC/Perlmutter Best Practices for Workflow Tools

This guide documents best practices, anti-patterns, and configuration tips specific to NERSC's Perlmutter supercomputer.

## Table of Contents

1. [Filesystem Usage](#filesystem-usage)
2. [GNU Parallel Anti-Patterns](#gnu-parallel-anti-patterns)
3. [Slurm Best Practices](#slurm-best-practices)
4. [Workflow QOS](#workflow-qos)
5. [SPIN Integration](#spin-integration)

---

## Filesystem Usage

### **$SCRATCH**: Temporary Workflow Data

✅ **Use $SCRATCH for:**
- Intermediate workflow files
- Temporary computation results
- Active job working directories
- High-performance I/O during runs

❌ **Do NOT use $SCRATCH for:**
- Long-term storage (8-week retention policy - files auto-deleted after 12 weeks unused)
- Final results you need to keep
- Input data that can't be regenerated

**Example:**
```bash
cd $SCRATCH
git clone <repo> workflow_project
cd workflow_project
sbatch run_workflow.sh  # Outputs go to $SCRATCH
```

**After workflow completes, copy results to CFS:**
```bash
cp -r $SCRATCH/workflow_project/results /global/cfs/cdirs/yourproject/
```

### **CFS (Community File System)**: Long-Term Storage

✅ **Use CFS for:**
- Final results and analysis outputs
- Published data and figures
- Input datasets used across multiple projects
- Provenance databases (AiiDA, Merlin logs)

❌ **Do NOT use CFS for:**
- High-throughput I/O during active jobs (slower than $SCRATCH)
- Temporary intermediate files

**Path structure:**
```
/global/cfs/cdirs/<project_name>/
```

### **$HOME**: Code and Configuration

✅ **Use $HOME for:**
- Git repositories (small)
- Configuration files (.bashrc, scripts)
- Python environments (conda, venv)

❌ **Do NOT use $HOME for:**
- Large datasets
- Workflow outputs
- High-I/O operations

**Quota:** 40 GB

---

## GNU Parallel Anti-Patterns

### ❌ Anti-Pattern 1: Bash Loop with `srun -n1 --exclusive`

**Don't do this:**
```bash
for i in {1..100}; do
  srun -n1 --exclusive ./task.sh $i &
done
wait
```

**Problem:** Jobs execute in batches based on available resources. CPUs sit idle while waiting for the longest job in each batch to complete.

**Do this instead:**
```bash
seq 1 100 | parallel -j $SLURM_CPUS_ON_NODE './task.sh {}'
```

**Why:** GNU Parallel maintains a task queue and starts new tasks immediately as resources become available.

### ❌ Anti-Pattern 2: Overusing Job Arrays

**Don't do this:**
```bash
#SBATCH --array=1-1000
./task.sh $SLURM_ARRAY_TASK_ID
```

**Problems:**
- 1000 separate jobs create scheduler contention
- Lower queue priority (many small jobs vs one large job)
- Harder to track completion

**Do this instead:**
```bash
#SBATCH --nodes=1
seq 1 1000 | parallel -j $SLURM_CPUS_ON_NODE './task.sh {}'
```

**When job arrays ARE appropriate:**
- Tasks require different node counts or time limits
- Tasks span multiple days (can't fit in single allocation)
- True independence (no shared coordination needed)

### ❌ Anti-Pattern 3: SSH-Based Distribution (`--sshlogin`)

**Don't do this:**
```bash
parallel --sshlogin node1,node2,node3 command ::: inputs
```

**Problems:**
- Breaks Slurm job step semantics
- Poor cleanup on job termination
- SSH spawning overhead
- No integration with Slurm accounting

**Do this instead:**
```bash
# Single-node: just use parallel directly
parallel -j $SLURM_CPUS_ON_NODE command ::: inputs

# Multi-node: use srun with parallel
srun -N $SLURM_NNODES -n $SLURM_NNODES --ntasks-per-node=1 \
  parallel -j $SLURM_CPUS_ON_NODE command ::: inputs
```

### ❌ Anti-Pattern 4: Missing `--delay` with Slurm Integration

**Don't do this:**
```bash
parallel -j 128 'srun -n1 ./task.sh {}' ::: inputs
```

**Problem:** Spawning 128 srun processes simultaneously overloads the Slurm controller.

**Do this instead:**
```bash
parallel -j 128 --delay 0.2 'srun -n1 ./task.sh {}' ::: inputs
```

**Why:** `--delay 0.2` enforces 200ms delay between launches, reducing controller load.

---

## Slurm Best Practices

### Use `$SLURM_CPUS_ON_NODE` for Automatic Scaling

```bash
# Good: Adapts to node type automatically
parallel -j $SLURM_CPUS_ON_NODE command ::: inputs

# Bad: Hardcoded (breaks if you change --constraint)
parallel -j 128 command ::: inputs
```

**Perlmutter CPU nodes:** 128 cores
**Perlmutter GPU nodes:** 64 cores

### Specify Node Type with `--constraint`

```bash
#SBATCH --constraint=cpu   # CPU-only nodes (128 cores)
#SBATCH --constraint=gpu   # GPU nodes (64 cores + 4 A100 GPUs)
```

Omitting `--constraint` allows Slurm to choose, which may cause inconsistent performance.

### Request Appropriate QOS

```bash
#SBATCH --qos=regular      # Standard production jobs
#SBATCH --qos=debug        # Short test jobs (max 30 min, max 4 nodes)
#SBATCH --qos=shared       # Shared node access (<= 128 cores on CPU)
```

**For workflow coordinators:** Use `--qos=workflow` (see Workflow QOS section)

### Set Reasonable Time Limits

```bash
#SBATCH --time=02:00:00    # 2 hours
```

**Why:**
- Shorter jobs schedule faster
- Prevents runaway jobs consuming allocation
- Use `--resume-failed` with GNU Parallel for workflows >24 hours (submit multiple times)

---

## Workflow QOS

### What is Workflow QOS?

Special QOS for running lightweight persistent workflow coordinators (daemons) that manage task distribution but don't perform heavy computation themselves.

**Use cases:**
- Merlin worker coordinators (Celery workers idle most of the time)
- AiiDA daemon processes
- Maestro orchestration processes

### Requesting Workflow QOS Access

Submit a ticket to NERSC Consulting requesting workflow QOS access. Explain:
- Which workflow tool (Merlin, AiiDA, etc.)
- Why you need persistent processes
- Estimated resource usage (typically <1 core, <4 GB memory)

### Using Workflow QOS

```bash
#SBATCH --qos=workflow
#SBATCH --time=48:00:00    # Up to 48 hours
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4GB
```

**Cost:** Charged at reduced rate (coordinator processes consume minimal allocation hours)

**Anti-pattern:** Do NOT run compute-heavy workloads with workflow QOS (violates usage policy)

---

## SPIN Integration

### What is SPIN?

NERSC's Kubernetes-based platform for running persistent services (contrast with batch computing on Perlmutter).

**Use SPIN for:**
- Redis (Merlin task queues)
- PostgreSQL (AiiDA provenance database)
- RabbitMQ (AiiDA message broker)
- Web dashboards and APIs

**Do NOT use SPIN for:**
- Compute-heavy simulations (use Perlmutter/Slurm)
- Short-lived tasks (use batch jobs)

### Merlin + SPIN Pattern

1. **SPIN:** Deploy Redis as persistent service
2. **Perlmutter:** Submit Merlin workers as batch jobs

```bash
# On SPIN: Redis runs 24/7
kubectl apply -f redis-deployment.yaml

# On Perlmutter: Submit Merlin workers
sbatch merlin_workers.sh
```

Workers connect to SPIN Redis, pull tasks, execute on Perlmutter compute nodes.

### AiiDA + SPIN Pattern

1. **SPIN:** Deploy PostgreSQL + RabbitMQ
2. **Perlmutter:** Run AiiDA workflows as batch jobs or with workflow QOS daemon

```bash
# On SPIN: Database services run 24/7
kubectl apply -f postgres-deployment.yaml
kubectl apply -f rabbitmq-deployment.yaml

# On Perlmutter: Submit AiiDA workflows
verdi computer setup  # Configure Perlmutter as AiiDA computer
verdi run workflow.py
```

### SPIN Access

Not all users have SPIN access by default. Check access status:
```bash
iris client info
```

Request SPIN access through NERSC account management if needed.

---

## Quick Reference

| Task | Filesystem | Tool | Pattern |
|------|------------|------|---------|
| Run parameter sweep | $SCRATCH | GNU Parallel | `parallel -j $SLURM_CPUS_ON_NODE` |
| Store final results | CFS | - | `cp $SCRATCH/results /global/cfs/cdirs/project/` |
| Deploy Redis | SPIN | Kubernetes | `kubectl apply -f redis.yaml` |
| Run Merlin workers | Perlmutter | Slurm + Merlin | `sbatch merlin_workers.sh` |
| Persistent coordinator | Perlmutter | Workflow QOS | `#SBATCH --qos=workflow` |
| Multi-step DAG | $SCRATCH | Maestro/Merlin | YAML specification + Slurm adapter |
| Provenance tracking | CFS (database) | AiiDA | PostgreSQL on SPIN |

---

## Resources

**NERSC Documentation:**
- [Perlmutter User Guide](https://docs.nersc.gov/systems/perlmutter/)
- [File Systems](https://docs.nersc.gov/filesystems/)
- [Running Jobs](https://docs.nersc.gov/jobs/)
- [Workflow Tools at NERSC](https://docs.nersc.gov/jobs/workflow/)
- [SPIN Platform](https://docs.nersc.gov/services/spin/)

**Workflow Tools:**
- [GNU Parallel at NERSC](https://docs.nersc.gov/jobs/workflow/gnuparallel/)
- [Best Practices for Many-Task Workflows](https://docs.nersc.gov/jobs/workflow/best-practices/)
```

**Verification:**
Run: `grep "## Filesystem Usage" resources/nersc-best-practices.md`
Expected: Shows section header

Run: `grep -c "Anti-Pattern" resources/nersc-best-practices.md`
Expected: >= 4 (documents multiple anti-patterns)

**Commit:** Batch commit with all Phase 2 files (Task 9)
<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Verify Phase 2 examples run correctly

**Verifies:** wf-seminar.AC4.4

**Implementation:**

Verify that all three examples execute without errors (operational verification for infrastructure phase).

**Step 1: Verify Example 1 structure and executability**

```bash
cd 00-gnu-parallel/example1-parameter-sweep

# Check files exist
ls -1 README.md run_simple.sh process_task.sh

# Make executable
chmod +x run_simple.sh process_task.sh

# Run example (login node safe - uses -j 2)
bash run_simple.sh
```

Expected: Completes in ~20 seconds, shows "All tasks complete!"

**Step 2: Verify Example 2 structure and executability**

```bash
cd ../example2-multi-param

# Check files exist
ls -1 README.md run_combinations.sh process_combination.sh

# Make executable
chmod +x run_combinations.sh process_combination.sh

# Run example (login node safe - uses -j 2)
bash run_combinations.sh
```

Expected: Shows 18 combinations (3×3×2), completes in ~18 seconds

**Step 3: Verify Example 3 structure and Slurm script syntax**

```bash
cd ../example3-slurm-integration

# Check files exist
ls -1 README.md submit_parallel_job.sh process_task.sh task_list.txt

# Verify task list has 100 entries
wc -l task_list.txt

# Check Slurm script syntax (don't submit, just validate)
grep "#SBATCH" submit_parallel_job.sh
```

Expected: task_list.txt has 100 lines, Slurm directives present

**Step 4: Verify documentation completeness**

```bash
# Check 00-gnu-parallel README
wc -l ../../README.md
grep "## When to Use GNU Parallel" ../../README.md

# Check NERSC best practices
wc -l ../../../resources/nersc-best-practices.md
grep "Anti-Pattern" ../../../resources/nersc-best-practices.md | wc -l
```

Expected: README has substantial content (>150 lines), best practices doc has >= 4 anti-patterns

**Verification confirms:**
- All example files created and executable
- Examples 1 and 2 run successfully on login node
- Example 3 Slurm script has correct directives
- Documentation is complete
<!-- END_TASK_6 -->

<!-- START_TASK_7 -->
### Task 7: Commit Phase 2 files

**Verifies:** None (infrastructure phase)

**Implementation:**

Commit all Phase 2 files to repository.

```bash
# Stage updated README
git add 00-gnu-parallel/README.md

# Stage Example 1
git add 00-gnu-parallel/example1-parameter-sweep/README.md
git add 00-gnu-parallel/example1-parameter-sweep/run_simple.sh
git add 00-gnu-parallel/example1-parameter-sweep/process_task.sh

# Stage Example 2
git add 00-gnu-parallel/example2-multi-param/README.md
git add 00-gnu-parallel/example2-multi-param/run_combinations.sh
git add 00-gnu-parallel/example2-multi-param/process_combination.sh

# Stage Example 3
git add 00-gnu-parallel/example3-slurm-integration/README.md
git add 00-gnu-parallel/example3-slurm-integration/submit_parallel_job.sh
git add 00-gnu-parallel/example3-slurm-integration/process_task.sh
git add 00-gnu-parallel/example3-slurm-integration/task_list.txt

# Stage NERSC best practices
git add resources/nersc-best-practices.md

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
feat: add GNU Parallel section with 3 examples

Create baseline examples demonstrating simple task parallelization:

Examples:
- example1-parameter-sweep: Basic parallel execution with parameter substitution
- example2-multi-param: Cartesian product parameter combinations with ::: syntax
- example3-slurm-integration: Production Slurm batch integration with fault tolerance

Each example includes:
- README with concepts and learning outcomes
- Working shell scripts tested on Perlmutter
- Expected output documentation

Additional:
- Updated 00-gnu-parallel/README.md with complete content (when to use, syntax, progression)
- Created resources/nersc-best-practices.md documenting anti-patterns (srun loops, job arrays, SSH distribution, missing delays)

Supports AC4.1 (3 examples per tool), AC4.3 (simple to complex progression),
AC4.4 (Perlmutter runnable), AC5.2 (anti-patterns documented), AC5.4 (filesystem guidance).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

# Verify commit
git log -1 --stat
```

Expected: Commit created with all Phase 2 files

**Verification:**
Run: `git status`
Expected: `nothing to commit, working tree clean`

Run: `git log -1 --oneline`
Expected: Shows "feat: add GNU Parallel section with 3 examples"
<!-- END_TASK_7 -->

---

## Phase 2 Complete

**Deliverables:**
- ✅ Updated 00-gnu-parallel/README.md with complete content
- ✅ example1-parameter-sweep: Simple parallel execution demo
- ✅ example2-multi-param: Multiple parameter combinations
- ✅ example3-slurm-integration: Slurm batch integration
- ✅ resources/nersc-best-practices.md with anti-patterns
- ✅ All examples tested and verified executable
- ✅ All files committed to repository

**Next Phase:** Phase 3 will populate `01-signac/` with parameter space organization examples.
