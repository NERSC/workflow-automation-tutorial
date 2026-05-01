# Example 2: Provenance Querying with QueryBuilder

**Concept:** Query AiiDA's provenance database to find workflows, trace data lineage, and export results

**Duration:** 10 minutes

## What This Demonstrates

- Query the provenance database with AiiDA's QueryBuilder API
- Find workflows by time range and input values
- Trace data lineage (which inputs produced which outputs)
- Export provenance archives for sharing and reproducibility

## The Problem

You ran several workflows in example 1. Now you need to answer: which runs used parameter 42? What were the intermediate results? Can I share a reproducible record of this computation?

## The Solution

AiiDA's QueryBuilder lets you search the provenance database programmatically. Every `@task.calcfunction` call created nodes that you can now query:

```bash
python query_provenance.py
```

## Files in This Example

- `query_provenance.py` — Three query patterns: recent workflows, filter by input value, trace provenance links

## Prerequisites

- AiiDA profile configured with `verdi presto`
- **Example 1 must be run first** (creates the provenance data this example queries)

## How to Run

```bash
# Make sure example 1 has been run
cd 04-aiida/example1-workflow-def
python workflow.py --param 42

# Run provenance queries
cd ../example2-provenance
python query_provenance.py
```

## Expected Output

```
Found 1 workflows in last 7 days
  7: simple_workflow

Calculations with input 42:
  PK 3: prepare_data
```

If you haven't run example 1 yet, you'll see:
```
Found 0 workflows in last 7 days

  No workflows found. Did you run example 1 first?
    cd ../example1-workflow-def
    python workflow.py --param 42
```

## Key Concepts

1. **QueryBuilder:** AiiDA's database query API. Works identically whether backed by SQLite (`verdi presto`) or PostgreSQL (production). Supports filtering by node type, creation time, attribute values, and provenance relationships.

2. **Node types:** `WorkflowNode` for workflow processes, `CalcFunctionNode` for individual calculations, `Int`/`Dict`/etc. for data nodes. Query by type to find specific kinds of provenance entries.

3. **Provenance traversal:** `with_incoming` and `with_outgoing` follow the links in the provenance graph. "Find all CalcFunctionNodes that received this Int as input" is a one-line QueryBuilder query.

4. **Archive export:** `verdi archive create --all archive.aiida` bundles the entire provenance database into a portable file. Share it with collaborators or import it into another AiiDA profile for full reproducibility.

## Exercises

1. **Query different parameters:** Run example 1 with `--param 10` and `--param 100`, then run `query_provenance.py` again. How many workflows appear now?

2. **Trace a specific result:** Uncomment the `trace_provenance()` call in `query_provenance.py` with a PK from your runs. What inputs and outputs does it show?

3. **Export and inspect:** Run `verdi archive create --all archive.aiida` to export your provenance. How large is the file? What does `verdi archive info archive.aiida` show?

## Progression

This example queries existing provenance. Next:
- **Example 3:** Visualize provenance graphs and learn when to upgrade to production infrastructure
