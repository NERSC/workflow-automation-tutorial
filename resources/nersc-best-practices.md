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
