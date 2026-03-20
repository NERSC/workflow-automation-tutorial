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
- Long-term storage (8-week retention policy - files auto-deleted after 8 weeks unused)
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

### ❌ Anti-Pattern 1: Bash Loop with `srun -n1 --exclusive` (srun loop)

**Don't do this (srun loop anti-pattern):**
```bash
for i in {1..100}; do
  srun -n1 --exclusive ./task.sh $i &
done
wait
```

**Problem:** Jobs execute in batches based on available resources. CPUs sit idle while waiting for the longest job in each batch to complete. This srun loop pattern is inefficient.

**Do this instead:**
```bash
seq 1 100 | parallel -j $SLURM_CPUS_ON_NODE './task.sh {}'
```

**Why:** GNU Parallel maintains a task queue and starts new tasks immediately as resources become available. Avoid the srun loop pattern entirely.

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

## Tool-Specific Slurm Configuration

### signac-flow on Perlmutter

**Submission template** (`submit.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=signac-study
#SBATCH --account=<your_account>
#SBATCH --partition=cpu
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --time=04:00:00
#SBATCH --qos=regular
#SBATCH -o $SCRATCH/%j.log

module load python
cd $SCRATCH/signac_project

# signac-flow submits tasks to Slurm automatically
signac run
```

**Key settings:**
- **CPUs:** Use `$SLURM_CPUS_ON_NODE` or explicit core count
- **$SCRATCH:** All workflow files stored here (auto-deleted after 8 weeks)
- **Account:** Must match allocation account
- **QOS:** `regular` for production, `debug` for quick testing

**Typical workflow:**
```bash
# Initialize signac project in $SCRATCH
cd $SCRATCH
signac init YourProject
cd YourProject

# Define jobs in src/jobs.py
signac run

# Workflow persists across submissions (state stored in workspace)
```

**Filesystem pattern:**
- Input parameters: stored in `workspace/` ($SCRATCH)
- Results: stored in `workspace/*/result_file.txt` ($SCRATCH)
- Archive results: copy to CFS after completion

---

### Maestro on Perlmutter

**Batch block configuration** (`spec.yaml`):
```yaml
batch:
  type: slurm
  partition: cpu
  constraint: cpu
  account: "<your_account>"
  queue: regular
  # Alternative: queue: debug for testing (max 30 min)
  time: 240  # minutes (4 hours)
  nodes: 4

# Job-level overrides in study:
study:
  - name: task_group
    description: "Parameter sweep"
    launch:
      cmd: srun -n 1 ./task.sh {PARAM}
      nodes: 1
      procs: 1
```

**QOS selection:**
- `regular`: Standard production jobs (default)
- `debug`: Quick testing (max 30 min, max 4 nodes)
- `shared`: Multi-user node (<= 128 cores), if applicable

**$SCRATCH usage:**
```bash
# Run from SCRATCH
cd $SCRATCH
maestro run spec.yaml

# Maestro output structure:
$SCRATCH/maestro-logs/study_<timestamp>/
  ├── workflows.log
  ├── YML/
  └── <study_name>/
```

**Best practice:** Monitor with `maestro monitor <study_dir>`, copy final results to CFS

---

### Merlin on Perlmutter

**Worker deployment** (`merlin_workers.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=merlin-workers
#SBATCH --account=<your_account>
#SBATCH --partition=cpu
#SBATCH --constraint=cpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=04:00:00
#SBATCH --qos=workflow  # <-- Lightweight coordinator access needed
#SBATCH -o $SCRATCH/merlin_workers.log

module load python
cd $SCRATCH/merlin_project

# Start workers on 2 nodes (256 cores total)
merlin run-workers merlin_spec.yaml
```

**Workflow spec considerations:**
```yaml
merlin:
  resources:
    node_packing_count: 1  # 1 task per node
    # OR for GPU work:
    node_packing_count: 4  # 4 tasks per GPU node

task:
  launch:
    cmd: srun -n1 --cpus-per-task=32 python simulate.py
```

**Redis deployment** (on SPIN):
```bash
# Prerequisites: SPIN access + redis-py installed locally
# Connect Perlmutter workers to SPIN Redis:

export MERLIN_REDIS_HOST=redis-service.spin-k8s
export MERLIN_REDIS_PORT=6379

merlin run-workers merlin_spec.yaml
```

**Filesystem pattern:**
- Workflow spec: `$SCRATCH/merlin_project/merlin_spec.yaml`
- Task inputs/outputs: `$SCRATCH/studies/<study_name>/`
- Logs: `$SCRATCH/studies/<study_name>/logs/`
- Archive: Copy completed study to CFS after job completes

---

### AiiDA on Perlmutter

**Computer configuration** (after initial setup):
```bash
verdi computer configure ssh perlmutter  # or edit ~/.ssh/config
```

**Slurm template** (`aiida-default.pbs`, auto-generated):
```bash
#!/bin/bash
#SBATCH --job-name={aiida_job_name}
#SBATCH --account=<your_account>
#SBATCH --partition=cpu
#SBATCH --constraint=cpu
#SBATCH --nodes={num_cores_physical}
#SBATCH --ntasks={num_cores_physical}
#SBATCH --time={max_wallclock_seconds}
#SBATCH --qos=regular
#SBATCH -o {slurm_log_dir}/aiida-{job_id}.log

{aiida_scheduler_command}
```

**Daemon mode** (persistent workflow orchestrator with workflow QOS):
```bash
#!/bin/bash
#SBATCH --job-name=aiida-daemon
#SBATCH --account=<your_account>
#SBATCH --partition=cpu
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8GB
#SBATCH --time=24:00:00
#SBATCH --qos=workflow  # <-- Lightweight daemon
#SBATCH -o $SCRATCH/aiida_daemon.log

module load python
verdi daemon start
sleep infinity
```

**Database configuration** (PostgreSQL on SPIN):
```bash
verdi profile configure core.postgresql_dos
# When prompted:
# Host: postgres-service.spin-k8s
# Port: 5432
# Username: aiida
# Password: <from SPIN secret>
# Database: aiida_prod
```

**Filesystem pattern:**
- AiiDA repo: `~/.aiida/` (home directory, backed up)
- Calculations I/O: `/global/cfs/cdirs/yourproject/aiida_runs/` (provenance storage)
- Temporary files: `$SCRATCH/aiida_work/` (ephemeral)

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
