# NERSC/Perlmutter Best Practices for Workflow Tools

This guide documents best practices, anti-patterns, and configuration tips specific to NERSC's Perlmutter supercomputer.

## Table of Contents

1. [Perlmutter Platform Fundamentals](#1-perlmutter-platform-fundamentals)
   - [1.1 Filesystem Usage](#11-filesystem-usage)
   - [1.2 Slurm Basics](#12-slurm-basics)
   - [1.3 Workflow QOS](#13-workflow-qos)
   - [1.4 SPIN Integration](#14-spin-integration)
2. [Common Anti-Patterns and Best Practices](#2-common-anti-patterns-and-best-practices)
   - [2.1 Parallelization Anti-Patterns](#21-parallelization-anti-patterns)
3. [Tool-Specific Configuration](#3-tool-specific-configuration)
   - [3.1 signac-flow on Perlmutter](#31-signac-flow-on-perlmutter)
   - [3.2 Maestro on Perlmutter](#32-maestro-on-perlmutter)
   - [3.3 Merlin on Perlmutter](#33-merlin-on-perlmutter)
   - [3.4 AiiDA on Perlmutter](#34-aiida-on-perlmutter)
4. [Quick Reference](#4-quick-reference)
5. [Resources](#5-resources)

---

## 1. Perlmutter Platform Fundamentals

### 1.1 Filesystem Usage

#### **$SCRATCH**: Temporary Workflow Data

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

#### **CFS (Community File System)**: Long-Term Storage

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

#### **$HOME**: Code and Configuration

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

### 1.2 Slurm Basics

#### Use `$SLURM_CPUS_ON_NODE` for Automatic Scaling

```bash
# Good: Adapts to node type automatically
parallel -j $SLURM_CPUS_ON_NODE command ::: inputs

# Bad: Hardcoded (breaks if you change --constraint)
parallel -j 128 command ::: inputs
```

**Perlmutter CPU nodes:** 128 cores
**Perlmutter GPU nodes:** 64 cores

#### Specify Node Type with `--constraint`

```bash
#SBATCH --constraint=cpu   # CPU-only nodes (128 cores)
#SBATCH --constraint=gpu   # GPU nodes (64 cores + 4 A100 GPUs)
```

Omitting `--constraint` allows Slurm to choose, which may cause inconsistent performance.

#### Request Appropriate QOS

```bash
#SBATCH --qos=regular      # Standard production jobs
#SBATCH --qos=debug        # Short test jobs (max 30 min, max 4 nodes, max 5 concurrent per user)
#SBATCH --qos=shared       # Shared node access (<= 128 cores on CPU)
```

**For workflow coordinators:** Use `--qos=workflow` (see section 1.3 below)

**Note:** When submitting many jobs in a parameter sweep, use `--qos=regular` instead of debug due to the 5-job concurrency limit per user.

#### Set Reasonable Time Limits

```bash
#SBATCH --time=02:00:00    # 2 hours
```

**Why:**
- Shorter jobs schedule faster
- Prevents runaway jobs consuming allocation
- Use `--resume-failed` with GNU Parallel for workflows >24 hours (submit multiple times)

#### Understanding Job Arrays

Job arrays allow submitting many similar jobs with a single `sbatch` command:

```bash
#SBATCH --array=1-100
./task.sh $SLURM_ARRAY_TASK_ID
```

**How they work:**
- All tasks in an array share **identical resource requirements** (`--nodes`, `--time`, `--mem` apply to each task individually)
- Each task is treated as a **separate job** by the scheduler
- Tasks are indexed via `$SLURM_ARRAY_TASK_ID` environment variable
- Maximum array size: typically 1001 tasks

**When to use job arrays:**
- Independent tasks with uniform resource needs (same nodes, time, memory per task)
- Moderate scale (≤50 tasks recommended at NERSC)
- Tasks that need individual management (hold/release/cancel specific tasks)
- Simple parameter sweeps where `$SLURM_ARRAY_TASK_ID` indexing simplifies workflow

**When NOT to use job arrays (especially at NERSC):**
- **Many tasks (>50)** → severe queue delays due to NERSC's "2 jobs age" policy
  - Only 2 array tasks accumulate priority at once; others wait without aging
  - "A single job running many tasks will spend less time in queue than many jobs each running a single task" (NERSC)
- **Tasks with different resource requirements** → submit separate jobs or use workflow tools
- **Tasks with dependencies** → use workflow tools (Maestro, Merlin)
- **Avoiding scheduler load** → arrays create controller overhead; use GNU Parallel bundling instead

**NERSC-specific priority policy:**
NERSC allows only 2 jobs per user to gain priority simultaneously. Since each array task counts as a separate job, large arrays experience severe queue delays. For this reason, **NERSC explicitly recommends GNU Parallel as "a superior solution to task arrays" in many use cases.**

---

### 1.3 Workflow QOS

#### What is Workflow QOS?

Workflow QOS is a specialized queue for **lightweight coordination processes** that manage workflow orchestration on Perlmutter. It's designed exclusively for:

- Long-running listener/daemon processes that coordinate Slurm job submissions
- Workflow schedulers that monitor and manage batch queues
- Processes that interact with $SCRATCH filesystem for workflow coordination
- External data movement orchestration

**Important:** If your use case doesn't require Perlmutter integration (Slurm submission, $SCRATCH access), use **SPIN** instead.

#### Resource Limits

Workflow QOS jobs are **strictly limited** to:

| Resource | Limit |
|----------|-------|
| **Max walltime** | 90 days |
| **CPU** | ~32 cores (1/4 of login node) |
| **Memory** | ~64 GB (1/4 of login node) |
| **Partition** | Login nodes only (no compute node allocation) |
| **GPU access** | None |

#### Requesting Workflow QOS Access

1. Fill out the **[Workflow QOS Request Form](https://nersc.servicenowservices.com/sp/?id=sc_cat_item&sys_id=a82672d81b565910263aa82eac4bcb9a)**

2. Provide in your request:
   - Project name and email
   - Purpose (describe your coordination/scheduling use case)
   - Estimated CPU and memory usage
   - Process frequency and duration

3. Wait for NERSC approval before submitting workflow QOS jobs

#### Using Workflow QOS

**Example scrontab submission:**
```bash
#!/bin/bash
#SCRON -q workflow
#SCRON -A m1234
#SCRON -t 7-00:00:00
#SCRON --open-mode=append
#SCRON --dependency=singleton

# Run workflow coordinator every hour
0 * * * * /path/to/workflow_coordinator.sh
```

**Scrontab directives:**
- `-q workflow` - Submit to workflow QOS
- `-A <account>` - Your allocation account (required)
- `-t 7-00:00:00` - Walltime (up to 90 days: `90-00:00:00`)
- `--dependency=singleton` - Prevent multiple instances running simultaneously
- `--open-mode=append` - Append to log file instead of overwriting

**Note:** Workflow QOS jobs are typically submitted via `scrontab` rather than direct `sbatch`. Scrontab provides cron-like scheduling with automatic failover across login nodes. See [scrontab documentation](https://docs.nersc.gov/jobs/workflow/scrontab/) for syntax details.

**Best practices:**
- Use `--dependency=singleton` to prevent multiple instances when editing scrontab
- Unset `SLURM_MEM_PER_CPU` before submitting child batch jobs from workflow processes
- Limit aggregate Slurm queries to 1-2 per minute across all workflow jobs
- Use `scrontab` for periodic tasks (handles failover across login nodes)

**Cost:** Charged at reduced rate to encourage proper workflow management

#### Enforcement and Restrictions

**Strictly prohibited:**
- Compute-intensive workloads (use regular QOS instead)
- Memory-intensive applications exceeding 64 GB
- Long-running data processing tasks

**Enforcement mechanisms:**
- Linux cgroup limits automatically terminate processes exceeding resource limits
- NERSC monitors for policy violations
- Repeated violations → account restrictions or loss of workflow QOS access

#### Common Use Cases

**Appropriate uses:**
- Merlin worker coordinators (Celery workers managing task queues)
- AiiDA daemon processes (workflow orchestration)
- Maestro orchestration processes
- Periodic job submission via `scrontab`
- Workflow monitoring and status checking

**Inappropriate uses:**
- Running simulations or compute jobs (use regular QOS)
- Data analysis or processing (use compute nodes)
- Any CPU/memory-intensive work (violates policy)

---

### 1.4 SPIN Integration

#### What is SPIN?

SPIN is NERSC's **container-based platform** for deploying persistent network services. It provides Kubernetes orchestration for running containerized applications that support scientific workflows.

**Architecture:**
- **Kubernetes orchestration** managed through Rancher 2 web interface
- **Harbor-based container registry** (registry.nersc.gov) for Docker/Podman images
- Runs on dedicated worker nodes separate from Perlmutter compute

**Contrast with Perlmutter:**
- **SPIN**: Persistent services (databases, APIs, dashboards) running 24/7
- **Perlmutter**: Batch HPC computing with Slurm scheduler

#### Appropriate Use Cases

**Use SPIN for:**
- **Workflow infrastructure**: Redis (task queues), PostgreSQL (databases), RabbitMQ (message brokers)
- **Science gateways**: Web interfaces for data submission/retrieval
- **Persistent APIs**: Webhook endpoints for job notifications
- **Web dashboards**: Monitoring and visualization tools
- **Data repositories**: Long-running data management services

**Do NOT use SPIN for:**
- Compute-heavy simulations or data processing (use Perlmutter compute nodes)
- Traditional HPC batch jobs (use Slurm on Perlmutter)
- Short-lived tasks that don't need 24/7 availability

#### SPIN Access Requirements

**SPIN access is NOT provided by default to any NERSC users.** All users must:

1. **Complete training** (choose one):
   - **SpinUp Workshop** (recommended) - Two-part instructor-led program with hands-on exercises
   - **Self-guided training** - For users with time-sensitive needs or prior Rancher experience

2. **Request approval** from NERSC after training completion

3. **Check access status:**
   ```bash
   iris client info
   ```

**Resources:**
- **Office Hours**: Fridays 10 a.m.–12 p.m. Pacific Time
- **Help Portal**: https://help.nersc.gov/
- **Slack**: #spin channel in NERSC Users Slack

#### Database Services on SPIN

SPIN supports databases and message brokers via **load balancers**:

**Supported services:**
- PostgreSQL (port 5432)
- MySQL (port 3306)
- Redis (custom port)
- RabbitMQ (ports 5672, 15672)
- MongoDB (port 27017)

**Network restriction:** Load balancer services are **accessible only from NERSC networks** (Perlmutter compute nodes, login nodes), NOT from the public internet.

**Load balancer hostname pattern:**
```
<workload>-loadbalancer.<namespace>.<environment>.svc.spin.nersc.org
```

#### Common SPIN + Perlmutter Pattern

**Workflow infrastructure deployment:**

1. **SPIN:** Deploy persistent services (database, message queue)
   ```bash
   # Deploy Redis for Merlin task queue
   kubectl apply -f redis-deployment.yaml

   # Deploy PostgreSQL for AiiDA provenance
   kubectl apply -f postgres-deployment.yaml
   ```

2. **Perlmutter:** Submit compute workers as batch jobs
   ```bash
   # Workers connect to SPIN services and execute tasks
   sbatch merlin_workers.sh
   ```

**Integration methods:**
- **Shared storage**: Services access /global/cfs/ for dataset sharing
- **Load balancer**: Workers connect to SPIN databases via internal hostnames
- **Superfacility API**: SPIN services can submit jobs to Perlmutter programmatically

#### Best Practices

- **Use separate environments**: Development for testing, production for live services
- **Security**: Store credentials in Kubernetes Secrets (encrypted), not environment variables
- **Networking**: Configure proper ingress for web services, load balancers for databases
- **Monitoring**: Use Rancher UI to monitor container health and logs
- **Development**: Test containers locally before deploying to SPIN

---

## 2. Common Anti-Patterns and Best Practices

### 2.1 Parallelization Anti-Patterns

These anti-patterns apply when using GNU Parallel or similar parallelization tools on Perlmutter.

#### ❌ Anti-Pattern 1: Bash Loop with `srun -n1 --exclusive`

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

#### ❌ Anti-Pattern 2: Large Job Arrays (NERSC-Specific)

**Don't do this:**
```bash
#SBATCH --array=1-1000
./task.sh $SLURM_ARRAY_TASK_ID
```

**Problems (especially severe at NERSC):**
- **Queue delays**: NERSC allows only 2 jobs per user to gain priority simultaneously
  - Each array task counts as a separate job
  - Only 2 of 1000 tasks accumulate priority; others wait without aging
  - Result: Extremely long wait times for all tasks
- **Scheduler preference**: "Fewer jobs requesting many nodes" ranked higher than "many jobs requesting fewer nodes"
- **Controller load**: 1000 separate scheduler interactions vs. 1 bundled job

**Do this instead:**
```bash
#SBATCH --nodes=1
seq 1 1000 | parallel -j $SLURM_CPUS_ON_NODE './task.sh {}'
```

**Why:** "A single job running many tasks will spend less time in queue than many jobs each running a single task" (NERSC policy)

**When job arrays ARE appropriate:**
- Small-to-moderate scale (≤50 tasks at NERSC)
- Tasks need individual management (hold/release/cancel specific tasks)
- Simple parameter sweeps where `$SLURM_ARRAY_TASK_ID` indexing simplifies workflow
- All tasks have identical resource requirements (same nodes, time, memory)

#### ❌ Anti-Pattern 3: SSH-Based Distribution (`--sshlogin`)

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

#### ❌ Anti-Pattern 4: Missing `--delay` with Slurm Integration

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

## 3. Tool-Specific Configuration

### 3.1 signac-flow on Perlmutter

**Submission template** (`submit.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=signac-study
#SBATCH --account=<your_account>
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

### 3.2 Maestro on Perlmutter

**Batch block configuration** (`spec.yaml`):
```yaml
batch:
  type: slurm
  constraint: cpu
  account: "<your_account>"
  qos: regular
  # Note: Use regular QOS for parameter sweeps (avoid debug's 5-job limit)
  time: 240  # minutes (4 hours)
  nodes: 4

# Job-level overrides in study:
study:
  - name: task_group
    description: "Parameter sweep"
    run:
      cmd: srun -n 1 ./task.sh $(PARAM)
      nodes: 1
      procs: 1
```

**QOS selection:**
- `regular`: Standard production jobs (default); recommended for multi-job workflows
- `debug`: Quick testing only (max 30 min, max 4 nodes, max 5 concurrent per user)
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

### 3.3 Merlin on Perlmutter

**Worker deployment** (`merlin_workers.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=merlin-workers
#SBATCH --account=<your_account>
#SBATCH --constraint=cpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=04:00:00
#SBATCH --qos=regular  # Workers execute tasks on compute nodes
#SBATCH -o $SCRATCH/merlin_workers.log

module load python
cd $SCRATCH/merlin_project

# Start Celery workers on 2 nodes (256 cores total)
# Workers pull tasks from broker and execute computational work
merlin run-workers merlin_spec.yaml
```

**Note:** Merlin workers run computational tasks on compute nodes and should use `regular` (production) or `debug` (testing) QOS. Do NOT use workflow QOS for workers - that is only for lightweight coordinator processes.

**Workflow spec considerations:**
```yaml
merlin:
  resources:
    node_packing_count: 1  # 1 task per node
    # OR for GPU work:
    node_packing_count: 4  # 4 tasks per GPU node

study:
  - name: simulate
    run:
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

### 3.4 AiiDA on Perlmutter

**Computer configuration** (after initial setup):
```bash
verdi computer configure core.ssh perlmutter  # or edit ~/.ssh/config
```

**Slurm template** (`aiida-default.pbs`, auto-generated):
```bash
#!/bin/bash
#SBATCH --job-name={aiida_job_name}
#SBATCH --account=<your_account>
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
verdi presto --use-postgres
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

## 4. Quick Reference

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

## 5. Resources

**NERSC Documentation:**
- [Perlmutter Architecture](https://docs.nersc.gov/systems/perlmutter/architecture/)
- [File Systems](https://docs.nersc.gov/filesystems/)
- [Running Jobs](https://docs.nersc.gov/jobs/)
- [Workflow Tools at NERSC](https://docs.nersc.gov/jobs/workflow/)
- [SPIN Platform](https://docs.nersc.gov/services/spin/)

**Workflow Tools:**
- [GNU Parallel at NERSC](https://docs.nersc.gov/jobs/workflow/gnuparallel/)
