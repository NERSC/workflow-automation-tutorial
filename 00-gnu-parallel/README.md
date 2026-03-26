# Section 0: GNU Parallel - Simple Task Parallelization

**Duration:** 30 minutes

**Concepts:** Task-level parallelism, parameter sweeps, Slurm integration, embarrassingly parallel workloads

## Overview

GNU Parallel represents the easiest entry point for workflow automation, demonstrating how to run the same command with different parameters in parallel and without dependency management. It is the first step before graduating to more powerful workflow systems.

**Key capability:** Parallelization without dependencies

## Why GNU Parallel?

GNU Parallel is superior to job arrays on HPC systems because:
- **Scheduler efficiency:** One job requesting many cores is prioritized over many jobs requesting few cores
- **Reduced queue time:** Single trip through queue instead of many trips, one for each step
- **Less scheduler load:** Fewer jobs to manage
- **Built-in recovery:** `--joblog` and `--resume-failed` enable fault tolerance

## When to Use GNU Parallel

✅ **Good for:**
- Running the same command with different parameters (parameter sweeps)
- Embarrassingly parallel workloads (no dependencies between tasks)
- Quick parallelization of shell scripts without framework overhead
- Tasks that fit on a single node (128 cores on Perlmutter CPU nodes)
- Shallow workflows where results don't feed into subsequent steps

❌ **Not suitable for:**
- Multi-step workflows with dependencies
- Tracking parameter spaces across multiple runs
- Distributed coordination across many jobs
- Provenance recording and preservation
- Tasks requiring more than single-node resources

## Core Concepts

### Parameter Substitution

`{}` is replaced with each input item:
```bash
seq 1 4 | parallel echo "Hello world {}!"
# Output: 
Hello world 1!
Hello world 2!
Hello world 3!
Hello world 4!
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

## Progression to more advanced Workflow Tools

GNU Parallel is the entry point for parallelism, but you'll outgrow it when you need:

| Capability | Tool | When to Graduate |
|------------|------|------------------|
| Parameter organization across runs | signac | Filesystem-based state tracking |
| Multi-step dependencies | Maestro | DAG workflow specification |
| Distributed coordination | Merlin | Persistent task queues |
| Provenance tracking | AiiDA | Full execution history |

**Graduation signal:** If you're writing bash scripts to track "which parameter combinations ran successfully" or with multiple gnu parallel launches that must run in sequence to produce a correct outcome, it's time to consider using a more powerful workflow tool.

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
