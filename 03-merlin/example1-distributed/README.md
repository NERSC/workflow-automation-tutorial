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

Complete the [Prerequisites section](../README.md#prerequisites) in the Merlin README before starting this example. You should have a compute node allocation via `salloc`, Redis running on that node, and `merlin info` showing both connections as `OK`.

## Running on Perlmutter

All `merlin` commands must be run from the `03-merlin/` directory so Merlin finds the repo's `app.yaml` config automatically. All commands run inside the same `salloc` allocation where Redis is already running (see [Prerequisites](#prerequisites)).

**Submit the workflow tasks to the Redis queue:**
```bash
cd 03-merlin/
merlin run example1-distributed/spec.yaml
```

**Start workers to consume tasks (blocks until all tasks complete):**
```bash
merlin run-workers example1-distributed/spec.yaml
```

**Check status after workers finish:**
```bash
merlin status example1-distributed/spec.yaml
```

**Expected output structure** (under `$PSCRATCH/wf-seminar-merlin/`):
```
example1-distributed_<timestamp>/
├── generate/
│   └── output.txt
├── process/
│   ├── PARAM.1/
│   │   └── result.txt
│   ├── PARAM.2/
│   │   └── result.txt
│   ├── PARAM.3/
│   │   └── result.txt
│   ├── PARAM.4/
│   │   └── result.txt
│   └── PARAM.5/
│       └── result.txt
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
