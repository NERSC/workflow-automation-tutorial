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
