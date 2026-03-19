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
