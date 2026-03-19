# Section 0: GNU Parallel - Simple Task Parallelization

**Duration:** 30 minutes

**Concepts:** Task-level parallelism, parameter sweeps, Slurm integration

## Overview

GNU Parallel establishes the baseline for workflow automation, demonstrating simple task parallelization without dependency management.

## When to Use GNU Parallel

✅ **Good for:**
- Running the same command with different parameters (parameter sweeps)
- Embarrassingly parallel workloads (no dependencies between tasks)
- Quick parallelization of shell scripts
- Tasks that fit on a single node

❌ **Not suitable for:**
- Multi-step workflows with dependencies (use Maestro/Merlin)
- Tracking parameter spaces across runs (use signac)
- Fault tolerance and restart (use Merlin)
- Provenance tracking (use AiiDA)

## Examples

This directory will contain three examples:
1. Simple parameter sweep
2. Multiple parameter combinations
3. Slurm integration wrapper

(Examples will be added in Phase 2)

## Further Reading

- [GNU Parallel official documentation](https://www.gnu.org/software/parallel/)
- [NERSC GNU Parallel examples](https://docs.nersc.gov/)
- [Parallel command tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
