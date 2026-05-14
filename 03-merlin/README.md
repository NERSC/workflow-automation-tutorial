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

## Prerequisites

### If you completed earlier sections

Activate the environment and verify Merlin is available:

```bash
module load python
conda activate wf-seminar
merlin --version
```

If you see `merlin 1.13.0`, skip ahead to [Redis setup](#redis-setup).

### First time? Set up the environment

Follow the [setup instructions in the top-level README](../README.md#setup-instructions), then return here and activate:

```bash
module load python
conda activate wf-seminar
merlin --version
```

If `merlin --version` prints `merlin 1.13.0`, you're ready to continue.

### Redis setup

Merlin uses Redis as a message broker to coordinate tasks between workers. You'll start a local `redis-server` on the login node for these tutorial examples.

**Start Redis:**

```bash
redis-server --daemonize yes --loglevel warning
```

This starts Redis as a background process on port 6379. Verify it's running:

```bash
redis-cli ping
```

Expected output: `PONG`

### Merlin configuration

Merlin needs a config file (`~/.merlin/app.yaml`) that tells it where to find Redis. Generate the default config:

```bash
merlin config create
```

This creates `~/.merlin/app.yaml` with RabbitMQ defaults. Replace the file contents with this localhost Redis configuration:

```bash
cat > ~/.merlin/app.yaml << 'EOF'
broker:
    name: redis
    server: localhost
    port: 6379
    db_num: 0

results_backend:
    name: redis
    server: localhost
    port: 6379
    db_num: 0
    encryption_key: ~/.merlin/encrypt_data_key

celery:
    override: {}
EOF
```

**Verify the connection:**

```bash
merlin info
```

Look for these lines in the output:

```
broker server connection: OK
results server connection: OK
```

**Troubleshooting:** If `merlin info` shows `broker server connection: ERROR` or a `Connection refused` error, check two things:

1. **Redis not running?** Run `redis-cli ping`. If it doesn't return `PONG`, restart Redis with `redis-server --daemonize yes --loglevel warning`.
2. **Wrong config?** Verify `~/.merlin/app.yaml` matches the content above. If you skipped the `cat > ~/.merlin/app.yaml` step or still have the RabbitMQ defaults, `merlin info` will fail because it can't connect to a RabbitMQ server that doesn't exist.

### Cleanup

When you're done with the Merlin tutorial, stop the Redis server:

```bash
redis-cli shutdown
```

Login nodes are shared resources — don't leave Redis running when you're not using it.

> **Production deployments:** For persistent Redis beyond this tutorial, see the [Redis setup guide](../resources/installation-guides/merlin-redis-setup.md).

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
  bank: ntrain4

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
