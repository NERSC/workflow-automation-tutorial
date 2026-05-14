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

```bash
# Generate samples
merlin run spec.yaml

# Start multiple workers for parallel execution
merlin run-workers spec.yaml --worker-name worker1 &
merlin run-workers spec.yaml --worker-name worker2 &
merlin run-workers spec.yaml --worker-name worker3 &
```

With 3 workers at concurrency 32 each, ~96 tasks execute in parallel.
