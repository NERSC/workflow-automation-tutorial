# Example 3: Massive-Scale Parameter Sweep

**Learning Objectives:**
- Use `merlin.samples` for programmatic parameter generation
- Scale to 1000+ task combinations
- Monitor large workflows with `merlin status`
- Understand when Merlin justified over Maestro

**Concepts:** Massive scale, programmatic sampling, performance at scale

## Prerequisites

Complete the [Prerequisites section](../README.md#prerequisites) in the Merlin README before starting this example. You should have a compute node allocation via `salloc`, Redis running on that node, and `merlin info` showing both connections as `OK`.

## Workflow

Hyperparameter search with 1000 randomly sampled combinations (learning_rates, batch_sizes, epochs).

## Running

All `merlin` commands must be run from the `03-merlin/` directory so Merlin finds the repo's `app.yaml` config automatically. All commands run inside the same `salloc` allocation where Redis is already running (see [Prerequisites](#prerequisites)).

```bash
cd 03-merlin/
merlin run example3-massive-scale/spec.yaml
merlin run-workers example3-massive-scale/spec.yaml
```

The worker runs with concurrency 32 (configured in the spec), executing up to 32 tasks in parallel on the node.

> **Multi-node scaling:** In a real deployment, you would start `merlin run-workers` in multiple separate Slurm allocations — each allocation connects to the same Redis queue and pulls tasks independently. Worker concurrency within each allocation is controlled by the `args` field in the spec's `merlin.resources.workers` block.

**Monitor progress:**
```bash
merlin status $(ls -td $PSCRATCH/wf-seminar-merlin/massive-scale_* | head -1)
```

## Expected Output

Upon successful completion (under `$PSCRATCH/wf-seminar-merlin/massive-scale_<timestamp>/`), Merlin creates one workspace directory per task:

```
massive-scale_<timestamp>/
├── train/
│   ├── 00000001/
│   │   └── metrics.txt
│   ├── 00000002/
│   │   └── metrics.txt
│   ...
│   └── 00001000/
│       └── metrics.txt
└── aggregate/
    └── summary.txt
```

Each `metrics.txt` contains the simulated loss for that task's hyperparameter combination. The `summary.txt` reports the total count of completed training tasks.
