# Workflow Management Seminar Implementation Plan - Phase 5

**Goal:** Demonstrate distributed task queuing for massive scale and persistent coordination, showing when single-coordinator limits are exceeded

**Architecture:** Three progressive examples + infrastructure guide demonstrating Merlin capabilities: distributed execution with Redis → fault tolerance with retries → massive-scale hyperparameter search. Includes Redis deployment guide for SPIN.

**Tech Stack:**
- Merlin v1.13.0 (extends Maestro, installed via requirements.txt in Phase 1)
- Celery distributed task queue
- Redis message broker (deployed on SPIN or dedicated allocation)
- YAML for workflow specification (extends Maestro syntax)
- Python 3.10+ for workflow execution

**Scope:** Phase 5 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phase 1-4 infrastructure will exist before this phase executes)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC1: Tool selections are justified and appropriate for HPC audience
- **wf-seminar.AC1.1 Success:** Each of 5 tools (GNU Parallel, signac, Maestro, Merlin, AiiDA) has documented rationale explaining why it fits its category - Phase 5 adds Merlin rationale
- **wf-seminar.AC1.2 Success:** Tool justifications include: category fit, advantages over alternatives, unique teaching value, Perlmutter/Slurm compatibility
- **wf-seminar.AC1.4 Success:** Tool progression demonstrates capability building (parallelism → organization → dependencies → scale → provenance) - Merlin adds distributed scale
- **wf-seminar.AC1.5 Success:** Both paradigms represented (filesystem: signac/Maestro; database: Merlin/AiiDA) - Merlin introduces database-backed coordination

### wf-seminar.AC2: Seminar structure is pedagogically sound and time-appropriate
- **wf-seminar.AC2.3 Success:** Each section follows pattern: motivation → concepts → demo → hands-on → decision criteria
- **wf-seminar.AC2.4 Success:** Tools build on previous sections (signac uses Parallel concepts, Maestro adds to signac, etc.) - Merlin extends Maestro YAML

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 example specifications (15 total across 5 tools) - Phase 5 provides 3 Merlin examples
- **wf-seminar.AC4.3 Success:** Examples progress from simple to complex within each tool section
- **wf-seminar.AC4.4 Success:** All examples specify they must run on Perlmutter without modification
- **wf-seminar.AC4.5 Success:** Example specifications include: what to demonstrate, expected concepts learned, sample use case

### wf-seminar.AC5: NERSC/Perlmutter integration is accurate and complete
- **wf-seminar.AC5.1 Success:** Perlmutter-specific configuration documented for each tool (Slurm integration, filesystem usage, QOS options)
- **wf-seminar.AC5.3 Success:** SPIN integration documented for database-backed tools (Merlin, AiiDA) - Phase 5 covers Redis on SPIN
- **wf-seminar.AC5.5 Success:** Workflow QOS usage documented for persistent coordinator processes - Phase 5 documents worker persistence
- **wf-seminar.AC5.6 Edge:** Fallback approaches documented for attendees without SPIN access - Phase 5 provides local Redis alternative

### wf-seminar.AC6: Repository structure supports autonomous learning
- **wf-seminar.AC6.2 Success:** Each section includes README with concepts, when to use, and links to official documentation
- **wf-seminar.AC6.5 Success:** Installation guides provided for all tools with Perlmutter-specific steps - Phase 5 adds Redis setup guide

---

<!-- START_TASK_1 -->
### Task 1: Create 03-merlin/README.md with distributed coordination concepts

**Verifies:** wf-seminar.AC1.1, wf-seminar.AC1.2, wf-seminar.AC1.4, wf-seminar.AC1.5, wf-seminar.AC2.3, wf-seminar.AC6.2

**Files:**
- Create: `03-merlin/README.md`

**Implementation:**

Create comprehensive README explaining Merlin's role in tool progression and distributed coordination paradigm.

```markdown
# Section 3: Merlin - Distributed Task Queuing at Massive Scale

**Duration:** 40 minutes

**Concepts:** Distributed coordination, persistent queuing, fault tolerance, worker pools, message brokers, massive-scale ensembles

## Overview

Merlin introduces **distributed coordination** through a persistent external message broker (Redis), enabling workflows to scale beyond single-coordinator limits. Where Maestro executes workflows from one coordinator process, Merlin distributes tasks across worker pools that can span multiple allocations, survive restarts, and handle millions of tasks.

**Key capability:** Distributed persistent queuing with fault-tolerant execution at massive scale

## Why Merlin?

Merlin was developed at Lawrence Livermore National Laboratory (LLNL) specifically for massive-scale HPC ensembles. It has successfully executed **100 million simulations** on LLNL's Sierra supercomputer and processed **40 million samples** with hundreds of thousands of simulations per second.

### Advantages over Maestro:
- **Persistent coordination:** Tasks queued in Redis survive coordinator/worker failures
- **Distributed workers:** Multiple batch allocations can contribute workers to same workflow
- **Massive scale:** Proven to 100M+ tasks (vs Maestro's thousands)
- **Fault tolerance:** Automatic retries, checkpoint/restart, hard-fail cascades
- **Queue flexibility:** Dynamic task generation, worker specialization (CPU/GPU)
- **No filesystem bottleneck:** Direct broker communication (not file-based passing)

### Unique teaching value:
- Introduces persistent queue paradigm (vs ephemeral filesystem)
- Demonstrates coordinator/worker separation
- Shows infrastructure investment trade-offs (Redis deployment)
- Bridges to database-backed workflows (preparation for AiiDA)
- Teaches fault tolerance patterns essential for long-running workflows

### Perlmutter/NERSC compatibility:
- Redis deployable on SPIN (NERSC's Kubernetes platform)
- Workflow QOS available for persistent worker processes
- Multi-allocation patterns (different batches, same workflow)
- Fallback: local Redis in dedicated allocation

## When to Use Merlin

✅ **Good for:**
- Massive parameter sweeps (thousands to millions of combinations)
- Long-running workflows needing fault tolerance
- Multi-allocation workflows (span multiple batch jobs)
- ML training dataset generation from simulation ensembles
- Workflows where intermediate failures shouldn't stop progress
- Dynamic task generation (DAG expands during execution)

❌ **Stay with Maestro if:**
- Workflow fits in single allocation
- Scale is moderate (hundreds to low thousands of tasks)
- Don't need persistent coordination
- Infrastructure overhead not justified

❌ **Graduate to AiiDA when:**
- Need comprehensive provenance tracking
- Require reproducibility verification years later
- Want automated workflow versioning and data lineage
- Publication-grade documentation required

## Core Concepts

### Persistent Queue Architecture

**Maestro model (ephemeral):**
```
Coordinator → DAG → Slurm Jobs → Results (filesystem)
(If coordinator dies, workflow stops)
```

**Merlin model (persistent):**
```
Coordinator → Redis Queue ← Workers (distributed)
                ↓
           Persistent State
(Coordinator/workers can restart, workflow continues)
```

### Message Broker (Redis)

- **Role:** Central task queue and results backend
- **Deployment:** Persistent service (SPIN) or dedicated allocation
- **Communication:** Workers pull tasks directly from Redis
- **Persistence:** Tasks survive broker/worker restarts
- **Scale:** Hundreds of thousands of tasks/second throughput

### Worker Pools

**Workers consume tasks from queues:**
```bash
merlin run-workers spec.yaml --worker-name perlmutter_workers
```

**Worker characteristics:**
- Pull tasks from assigned queues
- Run independently (no inter-worker communication)
- Can be heterogeneous (CPU workers, GPU workers)
- Scalable (add/remove workers dynamically)
- Stateless (failure of one worker doesn't affect others)

### Merlin YAML Extensions

Merlin extends Maestro YAML with `merlin` block:

```yaml
description:
  name: my-workflow
  description: Distributed workflow

# Maestro sections (unchanged)
env:
  variables:
    PARAM: value

batch:
  type: slurm
  bank: m4408

study:
  - name: step1
    run:
      cmd: command here
      task_queue: simulations  # Assign to Merlin queue

# Merlin-specific additions
merlin:
  resources:
    - name: simulations
      args: --concurrency 32 --prefetch-multiplier 1 -O fair
  samples:
    generate:
      cmd: python generate_samples.py $(MERLIN_INFO)/samples.npy
    file: $(MERLIN_INFO)/samples.npy
    column_labels: [param1, param2]
```

**Key additions:**
- `task_queue`: Assign steps to specific queues
- `merlin.resources`: Configure worker concurrency per queue
- `merlin.samples`: Programmatic parameter generation
- `$(MERLIN_INFO)`: Special directory for Merlin metadata

### Fault Tolerance

**Retry mechanisms:**
```bash
# Exit with retry code
exit $(MERLIN_RETRY)  # Retry same command
exit $(MERLIN_RESTART)  # Run <step>.run.restart section
exit $(MERLIN_HARD_FAIL)  # Stop all workers on this queue
```

**Restart configuration:**
```yaml
study:
  - name: simulate
    run:
      cmd: ./run_simulation.sh
      restart: ./resume_from_checkpoint.sh
      retry_delay: 60  # Wait 60s before retry
      max_retries: 3
```

**Status persistence:**
- Completed steps marked with `MERLIN_FINISHED` files
- Remove marker to re-run step
- Queue state persists in Redis (survives restarts)

## Workflow Lifecycle

**1. Submit tasks to broker:**
```bash
merlin run spec.yaml
# Parses DAG, enqueues tasks to Redis
```

**2. Start workers (separate allocation):**
```bash
merlin run-workers spec.yaml
# Workers connect to Redis, consume tasks
```

**3. Monitor status:**
```bash
merlin status spec.yaml
merlin query-workers  # Check active workers
```

**4. Workers execute and report:**
```
Task pulled from queue → Execute → Results to Redis → Mark complete
```

## Progression from Maestro

**Maestro provided:** DAG-based workflow orchestration with Slurm integration

**Merlin adds:**
- Persistent external coordination (Redis)
- Distributed worker pools (multi-allocation)
- Fault tolerance (retries, restarts)
- Massive scale (millions of tasks)
- Queue-based task passing (not filesystem)

**Combined power:**
Use Maestro for moderate workflows in single allocations. Graduate to Merlin when scale or fault tolerance requirements exceed Maestro's capabilities.

## Infrastructure Requirements

**Redis deployment options:**

1. **SPIN (recommended for production):**
   - NERSC's Kubernetes platform
   - Persistent Redis container
   - Accessible from Perlmutter compute nodes
   - See `resources/installation-guides/merlin-redis-setup.md`

2. **Dedicated allocation (testing/small workflows):**
   - Run Redis in persistent allocation
   - Use workflow QOS (minimize hours)
   - Less robust (allocation ends = Redis stops)

**Worker deployment:**
- Submit batch jobs requesting nodes
- Run `merlin run-workers` in each allocation
- Workers connect to Redis, pull tasks
- Can span multiple allocations

## Examples in This Section

1. **example1-distributed** - Basic distributed execution with Redis queue
2. **example2-fault-tolerance** - Workflow with intentional failures showing retry mechanisms
3. **example3-massive-scale** - Hyperparameter search with 1000s of combinations

## When to Graduate to Next Tool

**Stay with Merlin if:**
- Distributed coordination meets needs
- Don't need full provenance tracking
- Results organized via filesystem conventions

**Move to AiiDA (Section 4) if:**
- Need comprehensive provenance (every calculation tracked)
- Require reproducibility verification years later
- Want automated data lineage graphs
- Publication-grade documentation required

## Official Documentation

- [Merlin Documentation](https://merlin.readthedocs.io/)
- [GitHub - LLNL/merlin](https://github.com/LLNL/merlin)
- [Configuration Guide](https://merlin.readthedocs.io/en/latest/user_guide/configuration/)
- [Celery Integration](https://merlin.readthedocs.io/en/latest/user_guide/celery/)
- [LLNL Computing Projects](https://computing.llnl.gov/projects/merlin)
- [Workflows Community Initiative](https://workflows.community/systems/merlin/)

## Quick Start

**Prerequisites:**
- Redis broker running (see installation guide)
- Merlin configured (`~/.merlin/app.yaml`)

**Basic workflow:**
```bash
# Submit workflow to queue
merlin run spec.yaml

# Start workers (in batch allocation)
merlin run-workers spec.yaml

# Check status
merlin status spec.yaml
merlin query-workers
```

---

**Next:** See examples for hands-on experience with distributed workflows on Perlmutter.
```

**Verification:**

Run: `cat 03-merlin/README.md | head -20`
Expected: Shows section title, duration, concepts

Run: `grep -c "100 million simulations" 03-merlin/README.md`
Expected: Returns `1` (scale documented)

Run: `grep -c "Redis" 03-merlin/README.md`
Expected: Returns at least `10` (persistent broker explained throughout)

Run: `grep -c "MERLIN_RETRY" 03-merlin/README.md`
Expected: Returns at least `1` (fault tolerance explained)

**Commit:**

```bash
git add 03-merlin/README.md
git commit -m "feat(merlin): add section README with distributed coordination concepts

- Explains Merlin's role in tool progression (adds distributed scale to Maestro)
- Documents 100M simulation scale proven on Sierra supercomputer
- Covers persistent queue architecture with Redis message broker
- Includes fault tolerance patterns (MERLIN_RETRY, MERLIN_RESTART, MERLIN_HARD_FAIL)
- Explains worker pool model and multi-allocation patterns
- Provides decision criteria for when to use vs graduate to AiiDA
- Documents SPIN Redis deployment and workflow QOS options
- Links to official documentation and Celery integration guides"
```

<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create resources/installation-guides/merlin-redis-setup.md

**Verifies:** wf-seminar.AC5.3, wf-seminar.AC5.5, wf-seminar.AC5.6, wf-seminar.AC6.5

**Files:**
- Create: `resources/installation-guides/merlin-redis-setup.md`

**Implementation:**

Create comprehensive Redis deployment guide covering SPIN deployment (recommended) and fallback options.

```markdown
# Merlin Redis Setup Guide for NERSC/Perlmutter

This guide covers deploying Redis as a message broker for Merlin workflows on NERSC systems.

## Overview

Merlin requires a persistent message broker (Redis or RabbitMQ) for task coordination. This guide focuses on Redis, which is simpler to deploy and sufficient for most workflows.

**Two deployment options:**
1. **SPIN (recommended):** Persistent containerized Redis on NERSC's Kubernetes platform
2. **Dedicated Allocation (fallback):** Redis in long-running batch job with workflow QOS

## Option 1: SPIN Deployment (Recommended)

SPIN is NERSC's Kubernetes-based platform for persistent services. It's ideal for Redis because:
- Runs independently of batch allocations
- Survives restarts automatically
- Accessible from Perlmutter compute nodes
- No allocation hours consumed

### Prerequisites

- SPIN account (request at https://iris.nersc.gov/spin)
- Basic familiarity with Docker/containers

### Step 1: Create Redis Container

**Create Dockerfile:**
```dockerfile
FROM redis:7.2-alpine

# Enable persistence
RUN echo "save 900 1" >> /etc/redis/redis.conf && \
    echo "save 300 10" >> /etc/redis/redis.conf && \
    echo "save 60 10000" >> /etc/redis/redis.conf

# Set password (CHANGE THIS)
RUN echo "requirepass YOUR_SECURE_PASSWORD_HERE" >> /etc/redis/redis.conf

EXPOSE 6379

CMD ["redis-server", "/etc/redis/redis.conf"]
```

**Build and push to registry:**
```bash
docker build -t registry.nersc.gov/$USER/redis-merlin:latest .
docker push registry.nersc.gov/$USER/redis-merlin:latest
```

### Step 2: Deploy to SPIN

**Create SPIN deployment:**
```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-merlin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-merlin
  template:
    metadata:
      labels:
        app: redis-merlin
    spec:
      containers:
      - name: redis
        image: registry.nersc.gov/$USER/redis-merlin:latest
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis-merlin

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

**Apply to SPIN:**
```bash
kubectl apply -f redis-deployment.yaml
```

**Get Redis hostname:**
```bash
kubectl get service redis-service
# Note the CLUSTER-IP (e.g., 10.100.x.x)
```

### Step 3: Configure Merlin

**Edit `~/.merlin/app.yaml`:**
```yaml
broker:
  name: redis
  server: 10.100.x.x  # CLUSTER-IP from above
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password  # Store password securely

results_backend:
  name: redis
  server: 10.100.x.x
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password
```

**Create password file:**
```bash
echo "YOUR_SECURE_PASSWORD_HERE" > ~/.merlin/redis_password
chmod 600 ~/.merlin/redis_password
```

### Step 4: Test Connection

**From Perlmutter login node:**
```bash
module load python
python -c "import redis; r=redis.Redis(host='10.100.x.x', port=6379, password='YOUR_PASSWORD'); r.ping()"
# Should print: True
```

**Test Merlin:**
```bash
merlin info
# Should show broker connection details
```

## Option 2: Dedicated Allocation (Fallback)

If SPIN access unavailable, run Redis in a persistent batch allocation.

### Step 1: Request Workflow QOS

Workflow QOS minimizes allocation hours for lightweight coordination processes.

**Request via NERSC ticket:**
- Subject: "Request workflow QOS access"
- Body: "I need workflow QOS for running Merlin coordinator on Perlmutter"
- Include NERSC repository (e.g., m4408)

### Step 2: Start Redis in Allocation

**Create batch script `start_redis.sh`:**
```bash
#!/bin/bash
#SBATCH --qos=workflow
#SBATCH --constraint=cpu
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --account=m4408  # Change to your account
#SBATCH --job-name=redis-coordinator

module load redis

# Start Redis with password
redis-server --requirepass YOUR_PASSWORD --save 900 1 --save 300 10 --save 60 10000 --dir $SCRATCH/redis-data

# Keep job alive
wait
```

**Submit:**
```bash
sbatch start_redis.sh
```

**Get Redis hostname:**
```bash
squeue -u $USER -o "%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"
# Note the NODELIST (e.g., nid002345)
```

### Step 3: Configure Merlin for Dedicated Redis

**Edit `~/.merlin/app.yaml`:**
```yaml
broker:
  name: redis
  server: nid002345  # Replace with actual node from squeue
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password

results_backend:
  name: redis
  server: nid002345
  port: 6379
  password: /global/homes/u/$USER/.merlin/redis_password
```

**Limitations:**
- Must update `server` if allocation ends and restarts on different node
- Redis stops when allocation time expires
- Less robust than SPIN deployment

### Step 4: Test Connection

```bash
python -c "import redis; r=redis.Redis(host='nid002345', port=6379, password='YOUR_PASSWORD'); r.ping()"
# Should print: True
```

## Security Considerations

**Password management:**
- NEVER commit passwords to git repositories
- Use `chmod 600` on password files
- Store passwords outside repository (e.g., `~/.merlin/`)

**Network access:**
- SPIN Redis accessible only from NERSC internal network
- Compute nodes can connect (Perlmutter → SPIN routable)
- External access requires VPN or SSH tunnel

## Troubleshooting

**Connection refused:**
- Check Redis is running: `kubectl get pods` (SPIN) or `squeue -u $USER` (allocation)
- Verify firewall/network rules allow port 6379
- Test with `telnet <redis-host> 6379`

**Authentication failed:**
- Verify password matches in `app.yaml` and Redis config
- Check password file permissions (`chmod 600`)
- Test password with `redis-cli`: `redis-cli -h <host> -a <password> ping`

**Workers can't connect:**
- Ensure workers running in environment with `~/.merlin/app.yaml` configured
- Check Redis hostname accessible from compute nodes
- Verify Slurm job network access (some QOS may restrict)

**Redis memory issues:**
- Monitor with `redis-cli INFO memory`
- Increase storage in SPIN PVC if needed
- Configure eviction policy for long-running workflows

## Performance Tuning

**For large workflows (>10k tasks):**
- Increase Redis maxmemory: `maxmemory 4gb`
- Enable persistence: `save 900 1` (avoids data loss on restart)
- Use multiple Redis instances (shard queues)

**For high-throughput workflows:**
- Disable persistence if transient data: `save ""`
- Increase worker concurrency: `--concurrency 64`
- Use `--prefetch-multiplier 1` for long-running HPC tasks

## Next Steps

After Redis setup:
1. Configure Merlin: `merlin config`
2. Test workflow: `merlin run spec.yaml`
3. Start workers: `merlin run-workers spec.yaml`
4. See `03-merlin/example1-distributed` for first distributed workflow
```

**Verification:**

Run: `ls resources/installation-guides/merlin-redis-setup.md`
Expected: File exists

Run: `grep -c "SPIN" resources/installation-guides/merlin-redis-setup.md`
Expected: Returns at least `10` (SPIN deployment covered extensively)

Run: `grep -c "workflow QOS" resources/installation-guides/merlin-redis-setup.md`
Expected: Returns at least `2` (fallback option documented)

Run: `grep -c "kubectl" resources/installation-guides/merlin-redis-setup.md`
Expected: Returns at least `3` (Kubernetes commands for SPIN)

**Commit:**

```bash
git add resources/installation-guides/merlin-redis-setup.md
git commit -m "feat(merlin): add Redis setup guide for SPIN and dedicated allocations

- Documents SPIN deployment (recommended) with Kubernetes manifests
- Provides dedicated allocation fallback using workflow QOS
- Includes Docker/container setup for SPIN Redis
- Covers Merlin app.yaml configuration for both options
- Security best practices for password management
- Troubleshooting section for common connection issues
- Performance tuning guidance for large/high-throughput workflows
- Network access patterns (Perlmutter → SPIN connectivity)"
```

<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create example1-distributed with basic Redis queue demonstration

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `03-merlin/example1-distributed/spec.yaml`
- Create: `03-merlin/example1-distributed/README.md`
- Create: `03-merlin/example1-distributed/scripts/process_task.py`

**Implementation:**

Create basic distributed workflow demonstrating Merlin's queue-based task distribution.

**File 1: `03-merlin/example1-distributed/README.md`**

```markdown
# Example 1: Distributed Task Execution with Redis

**Learning Objectives:**
- Configure Merlin's `merlin` block for distributed execution
- Assign steps to specific task queues
- Start workers consuming from queues
- Monitor distributed workflow with `merlin status`

**Concepts:** Task queues, worker pools, distributed coordination, Redis message broker

## Workflow Structure

```
generate → [process_PARAM.1, process_PARAM.2, ..., process_PARAM.5] → aggregate
```

- `generate`: Creates input data (runs locally)
- `process`: Distributed across 5 parameter values, each task sent to Redis queue
- `aggregate`: Collects results after all process tasks complete

## Prerequisites

- Redis broker running (see `resources/installation-guides/merlin-redis-setup.md`)
- `~/.merlin/app.yaml` configured with Redis connection

## Running on Perlmutter

**Terminal 1: Submit workflow to queue**
```bash
cd 03-merlin/example1-distributed
merlin run spec.yaml
# Workflow parsed, tasks sent to Redis queue
```

**Terminal 2: Start workers (in batch allocation)**
```bash
salloc --nodes=1 --qos=debug --time=00:30:00 --constraint=cpu --account=m4408
merlin run-workers spec.yaml
# Workers consume tasks from queue
```

**Monitor status:**
```bash
merlin status spec.yaml
```

**Expected output structure:**
```
example1_distributed_<timestamp>/
├── generate/
│   └── output.txt
├── process_PARAM.1/
│   └── result.txt
├── process_PARAM.2/
│   └── result.txt
...
└── aggregate/
    └── summary.txt
```

## Key Concepts Demonstrated

1. **Task queue assignment:** `task_queue: simulations` routes steps to specific queues
2. **Worker configuration:** `merlin.resources` defines concurrency and fairness
3. **Distributed execution:** Workers can be in different allocations/nodes
4. **Persistent coordination:** Workflow survives worker restarts (tasks remain in Redis)

## Exercises

1. Start workers in multiple allocations - observe load distribution
2. Kill workers mid-execution, restart - verify tasks resume
3. Increase PARAM values to 20 - observe scaling
4. Query Redis directly: `redis-cli -h <host> -a <password> LLEN simulations`
```

**File 2: `03-merlin/example1-distributed/spec.yaml`**

```yaml
description:
  name: example1-distributed
  description: Basic distributed workflow with Redis queues

env:
  variables:
    OUTPUT_PATH: ./output

batch:
  type: slurm
  host: perlmutter
  bank: m4408  # Change to your account
  queue: debug

global.parameters:
  PARAM:
    values: [1, 2, 3, 4, 5]
    label: PARAM.%%

merlin:
  resources:
    - name: simulations
      args: --concurrency 4 --prefetch-multiplier 1 -O fair

study:
  - name: generate
    description: Generate input data
    run:
      cmd: |
        mkdir -p $(OUTPUT_PATH)
        echo "Generated at $(date)" > $(OUTPUT_PATH)/output.txt
        for i in {1..5}; do
          echo "Input data for PARAM $i" >> $(OUTPUT_PATH)/output.txt
        done
        echo "Generation complete"

  - name: process
    description: Process each parameter value (distributed to workers)
    run:
      cmd: |
        python $(SPECROOT)/scripts/process_task.py \
          --param $(PARAM) \
          --input $(generate.workspace)/output.txt \
          --output $(OUTPUT_PATH)/result.txt
        echo "Processed PARAM=$(PARAM)"
      depends: [generate]
      task_queue: simulations

  - name: aggregate
    description: Aggregate results from all parameter values
    run:
      cmd: |
        echo "Aggregating results from all PARAM values" > $(OUTPUT_PATH)/summary.txt
        for p in 1 2 3 4 5; do
          result_file=$(find $(SPECROOT)/../example1_distributed_*/process_PARAM.$p -name result.txt 2>/dev/null | head -1)
          if [ -f "$result_file" ]; then
            cat "$result_file" >> $(OUTPUT_PATH)/summary.txt
          fi
        done
        echo "Aggregation complete"
      depends: [process_*]
```

**File 3: `03-merlin/example1-distributed/scripts/process_task.py`**

```python
#!/usr/bin/env python3
"""Process task demonstrating distributed execution."""

import argparse
import time
import socket

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', type=int, required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    hostname = socket.gethostname()
    print(f"Processing PARAM={args.param} on {hostname}")

    # Simulate work
    time.sleep(2)

    # Read input
    with open(args.input) as f:
        input_data = f.read()

    # Write result
    with open(args.output, 'w') as f:
        f.write(f"PARAM {args.param} Results\n")
        f.write(f"Processed on: {hostname}\n")
        f.write(f"Input received: {len(input_data)} bytes\n")
        f.write(f"Computation result: {args.param * 100}\n")

    print(f"PARAM={args.param} complete")

if __name__ == "__main__":
    main()
```

**Verification:**

Run: `ls 03-merlin/example1-distributed/`
Expected: Shows spec.yaml, README.md, scripts/

Run: `grep "task_queue: simulations" 03-merlin/example1-distributed/spec.yaml`
Expected: Shows task queue assignment

Run: `grep "merlin.resources" -A 3 03-merlin/example1-distributed/spec.yaml`
Expected: Shows worker configuration

**Commit:**

```bash
git add 03-merlin/example1-distributed/
git commit -m "feat(merlin): add example1-distributed demonstrating Redis queues

- Basic Merlin spec with task_queue assignments
- Worker configuration (concurrency, prefetch, fairness)
- Distributed parameter sweep (5 values)
- Shows merlin run + merlin run-workers workflow
- README explains distributed execution concepts
- Python script runs on worker nodes"
```

<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create example2-fault-tolerance with retry mechanisms

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `03-merlin/example2-fault-tolerance/spec.yaml`
- Create: `03-merlin/example2-fault-tolerance/README.md`
- Create: `03-merlin/example2-fault-tolerance/scripts/flaky_task.sh`

**Implementation:**

Create workflow demonstrating Merlin's fault tolerance with intentional failures and retries.

**File 1: `03-merlin/example2-fault-tolerance/README.md`**

```markdown
# Example 2: Fault Tolerance with Automatic Retries

**Learning Objectives:**
- Use `$(MERLIN_RETRY)` exit code for automatic retries
- Configure `retry_delay` and `max_retries`
- Use `$(MERLIN_RESTART)` for checkpoint/restart patterns
- Handle transient failures gracefully

**Concepts:** Fault tolerance, retry strategies, persistent state, task restart

## Workflow

- `flaky_task`: Fails randomly, retries up to 3 times with 5s delay
- `checkpoint_task`: Uses restart section to resume from checkpoint

## Running

```bash
merlin run spec.yaml
merlin run-workers spec.yaml
```

Tasks will fail initially, then retry until success or max_retries exceeded.
```

**File 2: `03-merlin/example2-fault-tolerance/spec.yaml`**

```yaml
description:
  name: fault-tolerance-demo
  description: Demonstrates retry and restart mechanisms

merlin:
  resources:
    - name: flaky_queue
      args: --concurrency 2 -O fair

study:
  - name: flaky_task
    description: Task that fails randomly, retries automatically
    run:
      cmd: |
        bash $(SPECROOT)/scripts/flaky_task.sh $(OUTPUT_PATH)/attempt.log
        # Script exits with $(MERLIN_RETRY) on failure
      retry_delay: 5
      max_retries: 3
      task_queue: flaky_queue

  - name: checkpoint_task
    description: Task with restart capability
    run:
      cmd: |
        if [ -f $(OUTPUT_PATH)/checkpoint.txt ]; then
          echo "Resuming from checkpoint"
          start=$(cat $(OUTPUT_PATH)/checkpoint.txt)
        else
          start=1
        fi
        for i in $(seq $start 5); do
          echo "Processing step $i"
          echo $i > $(OUTPUT_PATH)/checkpoint.txt
          sleep 1
          if [ $i -eq 3 ] && [ ! -f $(OUTPUT_PATH)/recovered ]; then
            echo "Simulated failure at step 3"
            touch $(OUTPUT_PATH)/failed_once
            exit $(MERLIN_RESTART)
          fi
        done
        echo "Completed all steps"
        touch $(OUTPUT_PATH)/recovered
      restart: |
        echo "Restarting from checkpoint..."
        # Restart section executed when MERLIN_RESTART encountered
      depends: [flaky_task]
```

**File 3: `03-merlin/example2-fault-tolerance/scripts/flaky_task.sh`**

```bash
#!/bin/bash
# Simulates flaky task that fails 50% of the time

ATTEMPT_LOG="$1"
ATTEMPT=1

if [ -f "$ATTEMPT_LOG" ]; then
  ATTEMPT=$(cat "$ATTEMPT_LOG")
  ATTEMPT=$((ATTEMPT + 1))
fi

echo $ATTEMPT > "$ATTEMPT_LOG"

echo "Attempt $ATTEMPT"

# 50% chance of failure (except on 4th attempt, always succeed)
if [ $ATTEMPT -lt 4 ]; then
  if [ $((RANDOM % 2)) -eq 0 ]; then
    echo "Task failed (transient error)"
    exit $(merlin config | grep MERLIN_RETRY | cut -d'=' -f2)
  fi
fi

echo "Task succeeded on attempt $ATTEMPT"
exit 0
```

**Verification:**

Run: `grep "retry_delay\|max_retries" 03-merlin/example2-fault-tolerance/spec.yaml`
Expected: Shows retry configuration

Run: `grep "MERLIN_RETRY\|MERLIN_RESTART" 03-merlin/example2-fault-tolerance/spec.yaml`
Expected: Shows fault tolerance exit codes

**Commit:**

```bash
git add 03-merlin/example2-fault-tolerance/
git commit -m "feat(merlin): add fault-tolerance example with retries

- Demonstrates MERLIN_RETRY for automatic retries
- Shows retry_delay and max_retries configuration
- MERLIN_RESTART for checkpoint/restart patterns
- Intentional failures with flaky_task.sh
- README explains fault tolerance concepts"
```

<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Create example3-massive-scale with large parameter sweep

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `03-merlin/example3-massive-scale/spec.yaml`
- Create: `03-merlin/example3-massive-scale/README.md`
- Create: `03-merlin/example3-massive-scale/scripts/generate_samples.py`

**Implementation:**

Create massive-scale parameter sweep demonstrating Merlin's scale capabilities.

**File 1: `03-merlin/example3-massive-scale/README.md`**

```markdown
# Example 3: Massive-Scale Parameter Sweep

**Learning Objectives:**
- Use `merlin.samples` for programmatic parameter generation
- Scale to 1000+ task combinations
- Monitor large workflows with `merlin status`
- Understand when Merlin justified over Maestro

**Concepts:** Massive scale, programmatic sampling, performance at scale

## Workflow

Hyperparameter search with 1000 combinations (10 learning_rates × 10 batch_sizes × 10 epochs).

## Running

```bash
# Generate samples
merlin run spec.yaml

# Start multiple workers for parallel execution
merlin run-workers spec.yaml --worker-name worker1 &
merlin run-workers spec.yaml --worker-name worker2 &
merlin run-workers spec.yaml --worker-name worker3 &
```

With 3 workers at concurrency 32 each, ~96 tasks execute in parallel.
```

**File 2: `03-merlin/example3-massive-scale/spec.yaml`**

```yaml
description:
  name: massive-scale
  description: 1000-task hyperparameter sweep

env:
  variables:
    N_SAMPLES: 1000

merlin:
  resources:
    - name: hparam_search
      args: --concurrency 32 -O fair
  samples:
    generate:
      cmd: python $(SPECROOT)/scripts/generate_samples.py $(MERLIN_INFO)/samples.npy $(N_SAMPLES)
    file: $(MERLIN_INFO)/samples.npy
    column_labels: [lr, batch_size, epochs]

study:
  - name: train
    description: Training task for each hyperparameter combination
    run:
      cmd: |
        echo "Training with lr=$(lr), batch_size=$(batch_size), epochs=$(epochs)"
        # Simulate training
        python -c "import time, random; time.sleep(random.uniform(0.1, 0.5)); print('Loss:', random.random())" > $(OUTPUT_PATH)/metrics.txt
      task_queue: hparam_search

  - name: aggregate
    description: Aggregate results across all combinations
    run:
      cmd: |
        echo "Processed $(N_SAMPLES) hyperparameter combinations" > $(OUTPUT_PATH)/summary.txt
        find $(WORKSPACE)/../ -name "metrics.txt" | wc -l >> $(OUTPUT_PATH)/summary.txt
      depends: [train_*]
```

**File 3: `03-merlin/example3-massive-scale/scripts/generate_samples.py`**

```python
#!/usr/bin/env python3
"""Generate hyperparameter samples for massive-scale sweep."""

import numpy as np
import sys

def main():
    output_file = sys.argv[1]
    n_samples = int(sys.argv[2])

    # Generate combinations
    lr = np.random.uniform(0.0001, 0.01, n_samples)
    batch_size = np.random.choice([16, 32, 64, 128, 256], n_samples)
    epochs = np.random.randint(10, 100, n_samples)

    # Save as structured array
    samples = np.core.records.fromarrays([lr, batch_size, epochs],
                                         names='lr,batch_size,epochs')
    np.save(output_file, samples)

    print(f"Generated {n_samples} hyperparameter combinations")

if __name__ == "__main__":
    main()
```

**Verification:**

Run: `grep "merlin.samples" -A 5 03-merlin/example3-massive-scale/spec.yaml`
Expected: Shows samples block configuration

Run: `grep "N_SAMPLES: 1000" 03-merlin/example3-massive-scale/spec.yaml`
Expected: Shows scale (1000 tasks)

**Commit:**

```bash
git add 03-merlin/example3-massive-scale/
git commit -m "feat(merlin): add massive-scale example with 1000-task sweep

- Demonstrates merlin.samples for programmatic parameter generation
- Scales to 1000 hyperparameter combinations
- Shows when Merlin justified over Maestro (massive scale)
- Multiple worker deployment for parallelism
- README explains scale characteristics"
```

<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Verify all Merlin examples execute correctly

**Verifies:** None (validation task)

**Files:**
- None (operational verification)

**Implementation:**

Verify all 3 Merlin examples run without errors.

**Verification steps:**

1. Check Redis connection:
```bash
python -c "import redis; r=redis.Redis(host='<redis-host>', port=6379, password='<password>'); print(r.ping())"
```

2. Test example1-distributed:
```bash
cd 03-merlin/example1-distributed
merlin run spec.yaml
# In separate terminal/allocation:
merlin run-workers spec.yaml
# Wait for completion, verify output directories created
```

3. Test example2-fault-tolerance:
```bash
cd 03-merlin/example2-fault-tolerance
merlin run spec.yaml && merlin run-workers spec.yaml
# Verify retry mechanisms work, check attempt logs
```

4. Test example3-massive-scale (use small N_SAMPLES for testing):
```bash
cd 03-merlin/example3-massive-scale
# Edit spec.yaml: N_SAMPLES: 50 (for quick test)
merlin run spec.yaml && merlin run-workers spec.yaml
```

**Expected results:**
- All examples create timestamped output directories
- Workers consume tasks from queues successfully
- Retry mechanisms work in example2
- No errors in Merlin logs

**Commit:** None (verification only)

<!-- END_TASK_6 -->

<!-- START_TASK_7 -->
### Task 7: Final commit for Phase 5

**Verifies:** None (housekeeping)

**Files:**
- None (commit task)

**Implementation:**

Final verification and commit summary for Phase 5.

**Final checks:**

```bash
# Verify all examples present
ls -R 03-merlin/

# Verify README complete
cat 03-merlin/README.md | grep -E "Overview|Why Merlin|When to Use|Examples"

# Verify Redis setup guide exists
ls resources/installation-guides/merlin-redis-setup.md
```

**Commit:**

```bash
git add 03-merlin/
git commit -m "feat(merlin): complete Merlin section with all examples and docs

Phase 5 complete:
- Section README with distributed coordination concepts
- Redis setup guide for SPIN deployment
- example1-distributed: Basic queue-based task distribution
- example2-fault-tolerance: Retry and restart mechanisms
- example3-massive-scale: 1000-task hyperparameter sweep
- All examples verified functional on Perlmutter
- Progression from Maestro: adds distributed persistent queuing"
```

<!-- END_TASK_7 -->
