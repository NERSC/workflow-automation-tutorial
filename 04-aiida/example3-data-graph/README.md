# Example 3: Data Lineage Visualization and Production Paths

**Concept:** Visualize provenance graphs, export reproducible archives, and understand when to upgrade infrastructure

**Duration:** 15 minutes

## What This Demonstrates

- Generate visual provenance graphs from SQLite data
- Trace data lineage ("where did this result come from?")
- Export provenance archives for sharing and reproducibility
- Understand the difference between `run()` and `submit()` execution modes

## The Problem

You've built workflows (example 1) and queried provenance (example 2). Now you need to: visualize the computation graph for a paper, share reproducible archives with collaborators, and understand when your training setup needs to be upgraded for production use.

## Prerequisites

- AiiDA profile configured with `verdi presto`
- **Examples 1 and 2 must be run first** (creates the provenance data to visualize)
- `graphviz` installed for graph rendering (included in the `wf-seminar` conda environment; if missing, install manually: `conda install graphviz -c conda-forge`)

---

## Tier 1: Training Walkthrough (SQLite)

Everything below works with the `verdi presto` SQLite profile from examples 1-2.

### Visualizing Provenance Graphs

Generate a visual graph for any workflow you ran in example 1:

```bash
# Get a PK from your previous runs
verdi process list -a

# Generate a provenance graph (creates a PNG, viewable in JupyterLab)
verdi node graph generate <PK> --output-format png

# Or generate as PDF (vector format, better for publications)
verdi node graph generate <PK>
```

The graph shows every data node (inputs, outputs) and process node (calcfunctions) connected by provenance links.

### Tracing Data Lineage

For any result, answer "where did this come from?":

```bash
# Show node details
verdi node show <PK>

# Generate ancestor tree — trace all inputs recursively
verdi node graph generate <PK> --output-format png --ancestor-depth 999

# Generate descendant tree — trace all outputs recursively
verdi node graph generate <PK> --output-format png --descendant-depth 999
```

### Exporting Provenance Archives

Create portable, reproducible bundles of your computational work:

```bash
# Export specific nodes
verdi archive create --nodes <PK> my_workflow.aiida

# Export everything in the profile
verdi archive create --all full_study.aiida

# Inspect an archive without importing
verdi archive info full_study.aiida

# Import into another AiiDA profile
verdi archive import full_study.aiida
```

Archives contain the complete provenance graph: inputs, outputs, code versions, and all intermediate steps. A reviewer can import the archive and verify every computational result.

### Expected Output

After generating a graph for a workflow PK:
```
$ verdi node graph generate 7 --output-format png
Success: Output written to 7.dot.png
```

The PNG shows a directed graph with boxes for data nodes and ovals for process nodes, connected by arrows showing provenance links.

---

## Tier 2: Going Further — Production Execution

The training examples use `run()` for synchronous execution. Production AiiDA deployments use `submit()` with a daemon for asynchronous execution. Here's when and why you'd upgrade.

### `run()` vs `submit()`: What's Different

| Aspect | `run()` (training) | `submit()` (production) |
|--------|-------------------|----------------------|
| Execution | Synchronous, in your Python process | Asynchronous, handled by AiiDA daemon |
| Blocking | Blocks until workflow completes | Returns immediately with PK |
| Infrastructure | SQLite only, no daemon needed | PostgreSQL + RabbitMQ + daemon |
| Use case | Interactive work, short workflows | Long-running jobs, HPC submission |
| Fault tolerance | None — if your process dies, workflow stops | Daemon restarts failed workflows |

**Code difference:**

```python
from aiida_workgraph import WorkGraph
from aiida.engine import submit

# Training mode (what examples 1-2 use)
wg = WorkGraph('my_workflow')
# ... add tasks ...
wg.run()
# Blocks until done, results in wg.process

# Production mode
node = submit(workflow, param=Int(42))
# Returns immediately, workflow runs in background
# Check status: verdi process list
# Get results later: verdi process show <PK>
```

### When to Upgrade from SQLite

The `verdi presto` SQLite setup is sufficient when:
- You're learning AiiDA or prototyping workflows
- Running single-user, interactive workflows
- Workflows complete in minutes, not hours

**Upgrade to PostgreSQL + RabbitMQ when:**
- Multiple users share the same AiiDA installation
- You need to submit long-running HPC jobs (hours/days)
- You want the daemon to manage job queues and handle failures
- You're running high-throughput studies with hundreds of calculations

### Production Deployment at NERSC

Two paths for production AiiDA at NERSC:

1. **SPIN containers:** Host PostgreSQL and RabbitMQ as persistent services in NERSC's container platform. Best for multi-user, always-on deployments.

2. **Workflow QOS:** Run the AiiDA daemon in a long-running Slurm job under the `workflow` QOS. Simpler setup, suitable for single-user campaigns.

See [Production Deployment Guide](../../resources/aiida-production-deployment.md) for detailed instructions on both paths.

## Key Concepts

1. **Provenance graph visualization:** `verdi node graph generate` renders the directed acyclic graph of computations. Each node is either data (what was computed) or a process (how it was computed).

2. **Archive portability:** AiiDA archives (`.aiida` files) bundle the complete provenance graph into a single file. Import them into any AiiDA profile to reproduce or verify results — the archive includes all data, not just metadata.

3. **Synchronous vs asynchronous execution:** `run()` is simple but blocking. `submit()` is production-grade but requires daemon infrastructure. Choose based on your workflow's duration and your deployment's complexity.

## Exercises

1. **Visualize your workflow:** Generate a graph for one of your example 1 PKs. How many nodes does a single 3-step workflow create? (Hint: count data nodes and process nodes separately.)

2. **Create and inspect an archive:** Export your workflows with `verdi archive create --all study.aiida`. How large is the file? Run `verdi archive info study.aiida` — what metadata does it contain?

3. **Ancestry traversal:** Pick an output node PK and use `--ancestor-depth 999`. Can you trace the final result back to the original input parameter?

## Progression

This completes the AiiDA hands-on examples. For production deployment beyond the training environment, see the [Production Deployment Guide](../../resources/aiida-production-deployment.md).
