# Example 1: WorkGraph Workflow with Automatic Provenance

**Concept:** Define and run a multi-step workflow with automatic provenance tracking

**Duration:** 10 minutes

## What This Demonstrates

- Define computation steps with `@task.calcfunction` decorators
- Wire steps into a workflow with `WorkGraph()` and `wg.tasks.new()`
- Run a workflow synchronously with `WorkGraph.run()` (no daemon needed)
- Inspect provenance with `verdi` CLI commands

## The Problem

You run a multi-step computation — prepare data, compute results, analyze output — but later cannot answer: what input produced this result? Which version of the code ran? What intermediate values were generated?

## The Solution

AiiDA's `@task.calcfunction` decorator automatically records every input, output, and the function that produced them in a provenance graph. After running the workflow, you can trace any result back to its origin:

```bash
python workflow.py --param 42
verdi process show <PK>
```

## Files in This Example

- `workflow.py` — Three-step workflow: prepare_data -> compute -> analyze, all with automatic provenance
- `code_wrapper.py` — Reference template for wrapping external codes (not used in this example)

## Prerequisites

- AiiDA profile configured with `verdi presto` (creates SQLite-backed profile, ~30 seconds)

## How to Run

```bash
# One-time setup (if not already done)
verdi presto

# Run the workflow
cd 04-aiida/example1-workflow-def
python workflow.py --param 42
```

## Expected Output

```
Running workflow with param=42...

Workflow completed! PK: 7

Explore the provenance:
  verdi process list -a                  # List all workflows
  verdi process show 7                   # Inspect this workflow
  verdi node graph generate 7            # Visualize provenance graph
```

(PK numbers will vary based on your profile state.)

**Follow the suggested commands** to explore what AiiDA captured:

```bash
# List all processes
verdi process list -a

# Inspect the workflow details
verdi process show 7

# Generate a visual provenance graph (creates PDF)
verdi node graph generate 7
```

## Key Concepts

1. **`@task.calcfunction` decorator:** Wraps a plain Python function so that every call creates provenance nodes — recording inputs, outputs, and the function that ran. No changes needed to your computation logic.

2. **`WorkGraph()` + `wg.tasks.new()`:** Builds a workflow by creating a `WorkGraph` object and wiring together multiple `@task.calcfunction` steps using `tasks.new()`. AiiDA tracks the connections between steps automatically.

3. **`load_profile()` + `WorkGraph.run()`:** `load_profile()` connects the script to your AiiDA database (SQLite via `verdi presto`). `wg.run()` executes the workflow synchronously — no daemon or message broker needed.

4. **PK (Primary Key):** Every node in AiiDA's provenance database gets an integer PK. Use it with `verdi process show <PK>` to inspect any computation.

## Exercises

1. **Change the parameter:** Run `python workflow.py --param 10` and then `python workflow.py --param 100`. Use `verdi process list -a` to see all three runs.

2. **Trace a result:** Pick a PK from `verdi process list -a` and run `verdi process show <PK>`. Can you identify the input value and all intermediate results?

3. **Visualize the graph:** Run `verdi node graph generate <PK>` to create a PDF showing the provenance graph. How many nodes does a single workflow run create?

## Progression

This is the foundation. Next examples add:
- **Example 2:** Query the provenance database programmatically with QueryBuilder
- **Example 3:** Visualize provenance graphs and learn when to upgrade to production infrastructure
