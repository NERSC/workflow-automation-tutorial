# Example 3: Massive-Scale Parameter Sweep

**Learning Objectives:**
- Use `merlin.samples` for programmatic parameter generation
- Scale to 1000+ task combinations
- Monitor large workflows with `merlin status`
- Understand when Merlin justified over Maestro

**Concepts:** Massive scale, programmatic sampling, performance at scale

## Prerequisites

Complete the [Prerequisites section](../README.md#prerequisites) in the Merlin README before starting this example. You should have Merlin installed, Redis running, and `merlin info` showing both connections as `OK`.

## Workflow

Hyperparameter search with 1000 randomly sampled combinations (learning_rates, batch_sizes, epochs).

## Running

All `merlin` commands must be run from the `03-merlin/` directory so Merlin finds the repo's `app.yaml` config automatically.

```bash
# Terminal 1: Submit workflow to queue
cd 03-merlin/
merlin run example3-massive-scale/spec.yaml

# Terminal 2: Start multiple workers (in batch allocation)
salloc --nodes=1 --qos=debug --time=00:30:00 --constraint=cpu --account=ntrain4
module load python
conda activate wf-seminar
cd 03-merlin/
merlin run-workers example3-massive-scale/spec.yaml --worker-name worker1 &
merlin run-workers example3-massive-scale/spec.yaml --worker-name worker2 &
merlin run-workers example3-massive-scale/spec.yaml --worker-name worker3 &
```

With 3 workers at concurrency 32 each, ~96 tasks execute in parallel.

## Expected Output

Upon successful completion, Merlin creates one workspace directory per task under a timestamped study root:

```
massive_scale_<timestamp>/
├── train/
│   ├── 00000001/
│   │   └── output/
│   │       └── metrics.txt
│   ├── 00000002/
│   │   └── output/
│   │       └── metrics.txt
│   ...
│   └── 00001000/
│       └── output/
│           └── metrics.txt
└── aggregate/
    └── output/
        └── summary.txt
```

Each `metrics.txt` contains the simulated loss for that task's hyperparameter combination. The `summary.txt` reports the total count of completed training tasks.
