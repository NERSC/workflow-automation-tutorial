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

This automatically runs with 2 parallel jobs on login nodes (safe) or uses all available cores when run in a Slurm batch job (see Example 3).

**Expected Output:**

```
Running 20 tasks with 2 parallel jobs...
(Automatically detects Slurm allocation or defaults to 2 for login nodes)

Processing tasks in parallel (output order may vary)...
Processing input 1... (simulates 2-second task)
Task 1 complete
Processing input 2... (simulates 2-second task)
Task 2 complete
...

All tasks complete!
Elapsed time: 20 seconds

Analysis:
- Sequential execution: ~40 seconds (20 tasks × 2 seconds)
- Parallel execution (2 jobs): ~20 seconds (ceiling(20/2) batches × 2 seconds)
- Parallel execution (128 jobs on Perlmutter): ~2 seconds
  (all 20 tasks run simultaneously, limited by single-task duration)
  Note: 108 of 128 cores would sit idle - this example is too small for a full node!
```

## Key Concepts

1. **Parameter substitution:** `{}` is replaced with each input value (1, 2, 3, ... 20)
2. **Job control:** `-j $NJOBS` controls parallelism (defaults to 2 on login nodes, uses `$SLURM_CPUS_ON_NODE` in batch jobs)
3. **Scalability:** On compute node with `$SLURM_CPUS_ON_NODE=128`, this automatically uses all 128 cores

## What Happens

1. `seq 1 20` generates numbers 1 through 20
2. Script detects available cores: `${SLURM_CPUS_ON_NODE:-2}` (2 on login node, 128 on compute node)
3. `parallel -j $NJOBS` runs multiple tasks simultaneously
4. When a task finishes, the next one starts immediately
5. All 20 tasks complete in ~20 seconds (with 2 jobs) instead of ~40 seconds

## Progression

This is the simplest use case. Next examples add:
- **Example 2:** Multiple parameters (Cartesian products)
- **Example 3:** Slurm batch integration with fault tolerance
