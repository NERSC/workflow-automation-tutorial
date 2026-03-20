# Example 1: WorkGraph Workflow with Automatic Provenance

**Learning Objectives:**
- Define workflows with @task.graph_builder decorator
- Submit calculations to Perlmutter via verdi
- Query automatic provenance capture
- Understand AiiDA's data model

**Concepts:** WorkGraph, provenance capture, verdi CLI, data nodes

## Workflow

prepare → compute → analyze (all steps automatically tracked in provenance graph)

## Prerequisites

- AiiDA profile configured (`verdi presto`)
- Perlmutter computer registered (`verdi computer setup`)

## Running

```bash
cd 04-aiida/example1-workflow-def
verdi run workflow.py --param 42

# Monitor
verdi process list
verdi process show <PK>

# View provenance
verdi node graph generate <PK> --output workflow.pdf
```

## Key Concepts

- Every calculation creates nodes in provenance graph
- Inputs/outputs automatically linked
- Query workflow history: `verdi process list -a`
