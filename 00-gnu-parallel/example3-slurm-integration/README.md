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

- `submit.sh` - Wrapper script for simplified job submission with optional reservation support
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
  --delay 0.2 \
  < task_list.txt
```

**Key features:**
- `#SBATCH` directives configure Slurm allocation
- `module load parallel` loads GNU Parallel
- `-j $SLURM_CPUS_ON_NODE` uses all allocated cores (128)
- `--joblog parallel_job.log` tracks task completion
- `--resume-failed` skips completed tasks on resubmission
- `--delay 0.2` reduces Slurm controller load (200ms between task spawns)
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
