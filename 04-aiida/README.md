# Section 4: AiiDA - Comprehensive Provenance Tracking for Reproducible Science

**Duration:** 35 minutes

**Concepts:** Provenance graphs, data lineage, reproducibility, publication-grade workflows, database-backed coordination

## Overview

AiiDA provides **comprehensive provenance tracking** that automatically captures the complete history of how computational results were generated. Where Merlin offers distributed persistent coordination, AiiDA extends this with full data lineage ensuring long-term reproducibility and publication-grade documentation of computational workflows.

**Key capability:** Automatic provenance capture enabling answer to "where did this result come from?" years later

## Why AiiDA?

Developed for computational materials science, AiiDA has powered thousands of research publications with its provenance tracking. Key advantages:

- **Automatic provenance:** Every calculation input, output, code version captured without manual logging
- **Complete data lineage:** Full graph from initial parameters to final results
- **Long-term reproducibility:** 10-year data persistence guarantee, query workflows years later
- **Publication-ready:** Export complete workflow history for reproducible research
- **Caching:** Skip redundant calculations with identical inputs (saves computational cost)
- **Query-able:** SQL-based database enables complex workflow analysis post-execution

### When provenance tracking justified:
- Publication-grade reproducibility required
- Computational cost savings from caching offset storage overhead
- Data will be reused/analyzed years later
- Multi-person teams need shared computation history
- Audit trails required for validation

## Prerequisites

```bash
module load python
conda activate wf-seminar
```

If you haven't created the environment yet, see the [top-level README](../README.md) for full setup instructions.

## Core Concepts

### Provenance Graph

AiiDA stores workflows as a directed acyclic graph (DAG) with two types:

**Data Provenance (DAG):**
- Nodes = data (inputs/outputs) + processes (calculations)
- Links = input/create relationships
- Enables answering "How was this data generated?"
- Guarantees reproducibility (DAG ensures no cycles)

**Logical Provenance (can contain cycles):**
- Includes workflow logic and "why" decisions
- Tracks returned values and workflow nesting

### WorkGraph (Modern Workflow Definition)

```python
from aiida_workgraph import task

@task.graph_builder
def my_workflow(param1, param2):
    # Clean Pythonic workflow definition
    result1 = calculation_task(param1)
    result2 = analysis_task(result1, param2)
    return result2
```

**Advantages over legacy WorkChain:**
- Pythonic syntax with decorators
- Interactive GUI for monitoring
- Easier to learn and debug

### Database Backend

AiiDA supports two storage backends:

**SQLite (training default):** File-based database created automatically by `verdi presto`. No server process needed. Supports all QueryBuilder operations used in this tutorial. Ideal for learning, prototyping, and single-user workflows.

**PostgreSQL (production):** Full client-server database for multi-user deployments, high-throughput computation, and long-running daemon-based workflows. Paired with RabbitMQ for asynchronous job coordination.

**Profile:** Configuration linking a storage backend, file repository, and computer resources. Created by `verdi presto` (SQLite) or `verdi profile setup` (PostgreSQL).

## Progression from Merlin

**Merlin provided:** Distributed persistent coordination via Redis

**AiiDA adds:**
- Comprehensive provenance (full data lineage)
- Long-term reproducibility guarantees
- Query-able workflow history
- Publication-grade exports
- Caching for computational efficiency

**Combined value:** Use Merlin for massive scale without provenance requirements. Graduate to AiiDA when reproducibility and long-term data management justify infrastructure investment.

## Infrastructure Requirements

### Training (this seminar)

**One command:** `verdi presto` creates a ready-to-use AiiDA profile with SQLite storage and a localhost computer. No PostgreSQL, RabbitMQ, or daemon needed. Setup takes ~30 seconds.

All three examples run with this configuration.

### Production (beyond the seminar)

For long-running workflows, multi-user deployments, or high-throughput campaigns:

- **PostgreSQL** database (provenance storage at scale)
- **RabbitMQ** message broker (daemon coordination)
- **AiiDA daemon** (asynchronous job submission and fault tolerance)

**Deployment options:**
1. **SPIN containers:** Persistent PostgreSQL + RabbitMQ services
2. **Workflow QOS:** Long-running Slurm job for the AiiDA daemon

See [Production Deployment Guide](../resources/aiida-production-deployment.md) for when and how to upgrade.

## Examples in This Section

1. **example1-workflow-def** - WorkGraph workflow with automatic provenance
2. **example2-provenance** - Query provenance and trace data lineage
3. **example3-data-graph** - Visualize data lineage, answer origin questions

## When to Use AiiDA

✅ **Good for:**
- Publication-grade reproducibility
- Long-term data management (years+)
- Complex workflows needing audit trails
- Teams sharing computational history
- When caching saves significant compute hours

❌ **Stay with Merlin if:**
- Transient workflows (no long-term reproducibility needed)
- Storage overhead > computational cost savings
- Don't need automated provenance documentation or complete provenance graphs

## Official Documentation

- [AiiDA Official Website](https://www.aiida.net/)
- [AiiDA Documentation](https://aiida.readthedocs.io/)
- [AiiDA-WorkGraph](https://aiida-workgraph.readthedocs.io/)
- [AiiDA Tutorial](https://aiida-tutorials.readthedocs.io/)
- [Plugin Registry](https://aiidateam.github.io/aiida-registry/)

## Quick Start

```bash
# One-time setup (~30 seconds)
verdi presto

# Run your first workflow
cd example1-workflow-def
python workflow.py --param 42

# Query provenance
python ../example2-provenance/query_provenance.py

# Visualize the graph
verdi node graph generate <PK>
```

## Provenance Storage and Querying

AiiDA's provenance storage enables powerful retrospective analysis of computational workflows. Whether backed by SQLite (training) or PostgreSQL (production), the complete provenance graph remains queryable after workflows complete. Use QueryBuilder in Python scripts or `verdi` CLI commands to trace data lineage and export reproducible archives.

---

**Next:** Start with Example 1 to run your first provenance-tracked workflow.
