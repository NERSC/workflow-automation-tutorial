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

**PostgreSQL:** Stores provenance graph, queryable via high-level Python API
**RabbitMQ:** Coordinates daemon workers for parallel execution
**Profile:** Configuration linking database, file repository, computer resources

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

**Required:**
- PostgreSQL database (provenance storage)
- RabbitMQ message broker (daemon coordination)
- SSH access to HPC systems (Perlmutter)

**Deployment options:**
1. **SPIN (recommended):** Persistent containers for PostgreSQL + RabbitMQ
2. **Dedicated allocation:** Local databases with workflow QOS

See `resources/installation-guides/aiida-database-setup.md` for deployment guide.

## Examples in This Section

1. **example1-workflow-def** - WorkGraph workflow with automatic provenance
2. **example2-provenance** - Query and restart from workflow history
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
# Setup (after database deployment)
verdi presto --use-postgres

# Register Perlmutter computer
verdi computer setup

# Run workflow
verdi run workflow.py

# Query provenance
verdi process list
verdi node graph generate <PK>
```

---

**Next:** See examples for hands-on provenance tracking on Perlmutter.
