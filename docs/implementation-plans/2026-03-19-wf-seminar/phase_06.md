# Workflow Management Seminar Implementation Plan - Phase 6

**Goal:** Demonstrate comprehensive provenance tracking and reproducibility for publication-grade computational research

**Architecture:** Three progressive examples + infrastructure guide demonstrating AiiDA capabilities: basic workflow with provenance → provenance querying/restart → data lineage visualization. Includes PostgreSQL+RabbitMQ deployment guide for SPIN.

**Tech Stack:**
- AiiDA-Core v2.8.0 (installed via requirements.txt in Phase 1)
- AiiDA-WorkGraph v0.3.16 (modern workflow approach)
- PostgreSQL database for provenance storage
- RabbitMQ message broker for daemon processes
- Python 3.10+ for workflow execution

**Scope:** Phase 6 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phase 1-5 infrastructure will exist before this phase executes)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC1: Tool selections are justified and appropriate for HPC audience
- **wf-seminar.AC1.1 Success:** Each of 5 tools has documented rationale - Phase 6 completes with AiiDA
- **wf-seminar.AC1.2 Success:** Tool justifications include category fit, advantages, teaching value, compatibility
- **wf-seminar.AC1.4 Success:** Tool progression (parallelism → organization → dependencies → scale → provenance)
- **wf-seminar.AC1.5 Success:** Both paradigms represented - AiiDA completes database-backed paradigm

### wf-seminar.AC2: Seminar structure is pedagogically sound
- **wf-seminar.AC2.3 Success:** Each section follows pattern (motivation → concepts → demo → hands-on)
- **wf-seminar.AC2.4 Success:** Tools build on previous sections - AiiDA extends Merlin's database paradigm

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 examples - Phase 6 completes 15 total examples
- **wf-seminar.AC4.3 Success:** Examples progress simple to complex
- **wf-seminar.AC4.4 Success:** All run on Perlmutter without modification
- **wf-seminar.AC4.5 Success:** Examples show learning objectives and use cases

### wf-seminar.AC5: NERSC/Perlmutter integration
- **wf-seminar.AC5.1 Success:** Perlmutter-specific configuration for AiiDA
- **wf-seminar.AC5.3 Success:** SPIN integration for PostgreSQL+RabbitMQ
- **wf-seminar.AC5.6 Edge:** Fallback for attendees without SPIN access

### wf-seminar.AC6: Repository structure supports autonomous learning
- **wf-seminar.AC6.2 Success:** Section README with concepts and documentation links
- **wf-seminar.AC6.5 Success:** Installation guide for AiiDA database setup

---

<!-- START_TASK_1 -->
### Task 1: Create 04-aiida/README.md with provenance concepts

**Verifies:** wf-seminar.AC1.1, wf-seminar.AC1.2, wf-seminar.AC1.4, wf-seminar.AC1.5, wf-seminar.AC2.3, wf-seminar.AC6.2

**Files:**
- Create: `04-aiida/README.md`

**Implementation:**

Create comprehensive README explaining AiiDA's provenance tracking capabilities.

```markdown
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
- Don't need provenance documentation

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
```

**Verification:**

Run: `grep -c "provenance" 04-aiida/README.md`
Expected: Returns at least `15`

Run: `grep -c "WorkGraph" 04-aiida/README.md`
Expected: Returns at least `3`

**Commit:**

```bash
git add 04-aiida/README.md
git commit -m "feat(aiida): add section README with comprehensive provenance concepts

- Explains AiiDA's role completing tool progression (adds provenance to Merlin's scale)
- Documents publication-grade reproducibility and 10-year data persistence
- Covers provenance graph architecture (data+logical provenance)
- Introduces WorkGraph as modern workflow definition approach
- Explains database backend requirements (PostgreSQL, RabbitMQ)
- Decision criteria for when comprehensive provenance justified
- Documents SPIN deployment for databases and Perlmutter integration
- Links to AiiDA documentation and WorkGraph resources"
```

<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create resources/installation-guides/aiida-database-setup.md

**Verifies:** wf-seminar.AC5.3, wf-seminar.AC5.6, wf-seminar.AC6.5

**Files:**
- Create: `resources/installation-guides/aiida-database-setup.md`

**Implementation:**

Create comprehensive database setup guide for AiiDA on NERSC systems.

**Content structure (following merlin-redis-setup.md pattern):**

```markdown
# AiiDA Database Setup Guide for NERSC/Perlmutter

## Overview
- Two deployment options: SPIN (recommended) vs dedicated allocation
- Requirements: PostgreSQL + RabbitMQ

## Option 1: SPIN Deployment
- PostgreSQL container deployment
- RabbitMQ container deployment
- Network configuration for Perlmutter access
- Profile setup with `verdi presto`

## Option 2: Dedicated Allocation
- Local PostgreSQL in workflow QOS allocation
- Local RabbitMQ setup
- Profile configuration with `verdi setup`

## Perlmutter Computer Registration
- SSH key setup
- `verdi computer setup` with Slurm scheduler
- Transport configuration
- Verification steps

## Troubleshooting
- Connection issues
- Authentication problems
- Daemon startup failures
```

(Full detailed content following merlin-redis-setup.md pattern with Kubernetes manifests, verdi commands, troubleshooting steps)

**Verification:**

Run: `grep -c "PostgreSQL" resources/installation-guides/aiida-database-setup.md`
Expected: Returns at least `10`

Run: `grep -c "RabbitMQ" resources/installation-guides/aiida-database-setup.md`
Expected: Returns at least `5`

**Commit:**

```bash
git add resources/installation-guides/aiida-database-setup.md
git commit -m "feat(aiida): add PostgreSQL+RabbitMQ setup guide for SPIN

- Documents SPIN deployment (recommended) with Kubernetes manifests
- PostgreSQL configuration for provenance database
- RabbitMQ setup for AiiDA daemon coordination
- Profile configuration (verdi presto, verdi setup)
- Perlmutter computer registration with SSH configuration
- Fallback: local databases in dedicated allocation
- Troubleshooting for connection and authentication issues
- Performance tuning for large-scale provenance tracking"
```

<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create example1-workflow-def demonstrating WorkGraph with provenance

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `04-aiida/example1-workflow-def/workflow.py`
- Create: `04-aiida/example1-workflow-def/README.md`
- Create: `04-aiida/example1-workflow-def/code_wrapper.py`

**Implementation:**

Create basic AiiDA WorkGraph workflow with automatic provenance.

**File 1: `04-aiida/example1-workflow-def/README.md`**

```markdown
# Example 1: WorkGraph Workflow with Automatic Provenance

**Learning Objectives:**
- Define workflows with @task.graph decorator
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
```

**File 2: `04-aiida/example1-workflow-def/workflow.py`**

```python
#!/usr/bin/env python
"""Simple WorkGraph workflow demonstrating provenance capture."""

from aiida import orm, engine
from aiida_workgraph import task, WorkGraph

@task.calcfunction
def prepare_data(param):
    """Prepare input data."""
    return orm.Int(param * 2)

@task.calcfunction
def compute(data):
    """Perform computation."""
    result = data.value ** 2
    return orm.Int(result)

@task.calcfunction
def analyze(result):
    """Analyze result."""
    final = result.value + 100
    return orm.Dict({'final_result': final, 'status': 'complete'})

@task.graph_builder
def simple_workflow(param):
    """
    Simple 3-step workflow with automatic provenance.

    Args:
        param: Input parameter (Int)

    Returns:
        Analysis results (Dict)
    """
    wg = WorkGraph('simple_workflow')

    # Define workflow steps
    prep = wg.tasks.new(prepare_data, name='prepare', param=param)
    comp = wg.tasks.new(compute, name='compute', data=prep.outputs.result)
    anal = wg.tasks.new(analyze, name='analyze', result=comp.outputs.result)

    # Return final result
    wg.add_task(anal)
    return wg

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', type=int, default=5)
    args = parser.parse_args()

    # Submit workflow
    result = simple_workflow(orm.Int(args.param))
    print(f"Workflow submitted. Check with: verdi process list")
```

**Verification:**

Run: `grep "@task.graph" 04-aiida/example1-workflow-def/workflow.py`
Expected: Shows WorkGraph decorator

Run: `ls 04-aiida/example1-workflow-def/README.md`
Expected: File exists

**Commit:**

```bash
git add 04-aiida/example1-workflow-def/
git commit -m "feat(aiida): add workflow-def example with WorkGraph

- @task.graph_builder for workflow definition
- Three-step workflow (prepare → compute → analyze)
- Automatic provenance capture for all calculations
- README explains WorkGraph concepts and verdi commands
- calcfunction decorators for provenance-tracked functions"
```

<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create example2-provenance demonstrating query and restart

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `04-aiida/example2-provenance/query_provenance.py`
- Create: `04-aiida/example2-provenance/README.md`

**Implementation:**

**File 1: `04-aiida/example2-provenance/README.md`**

```markdown
# Example 2: Provenance Querying and Workflow Restart

**Learning Objectives:**
- Query provenance graph with QueryBuilder
- Retrieve workflow history from database
- Export workflows for reproducibility
- Understand data lineage

**Concepts:** QueryBuilder, provenance traversal, workflow export, reproducibility

## Running

```bash
# Run query examples
python query_provenance.py

# Export workflow
verdi archive create --all archive.aiida

# Import elsewhere
verdi archive import archive.aiida
```
```

**File 2: `04-aiida/example2-provenance/query_provenance.py`**

```python
#!/usr/bin/env python
"""Query provenance graph examples."""

from aiida import orm
from aiida.orm import QueryBuilder, WorkflowNode, CalcFunctionNode, Int

def query_recent_workflows():
    """Find recent workflows."""
    qb = QueryBuilder()
    qb.append(WorkflowNode, filters={'ctime': {'>': '-7d'}})
    print(f"Found {qb.count()} workflows in last 7 days")

    for node, in qb.iterall():
        print(f"  {node.pk}: {node.label}")

def query_by_input_value(target_value):
    """Find calculations with specific input value."""
    qb = QueryBuilder()
    qb.append(Int, filters={'value': target_value}, tag='input')
    qb.append(CalcFunctionNode, with_incoming='input')

    print(f"Calculations with input {target_value}:")
    for node, in qb.iterall():
        print(f"  PK {node.pk}: {node.process_label}")

def trace_provenance(pk):
    """Trace provenance of a result."""
    node = orm.load_node(pk)
    print(f"Provenance of PK {pk}:")

    # Walk inputs
    for link in node.base.links.get_incoming():
        print(f"  Input: {link.node.pk} ({link.link_label})")

    # Walk outputs
    for link in node.base.links.get_outgoing():
        print(f"  Output: {link.node.pk} ({link.link_label})")

if __name__ == '__main__':
    query_recent_workflows()
    query_by_input_value(42)
    # trace_provenance(12345)  # Replace with actual PK
```

**Verification:**

Run: `grep "QueryBuilder" 04-aiida/example2-provenance/query_provenance.py`
Expected: Shows querying

**Commit:**

```bash
git add 04-aiida/example2-provenance/
git commit -m "feat(aiida): add provenance querying example

- QueryBuilder for finding workflows by criteria
- Provenance traversal (inputs/outputs)
- Export/import for reproducibility
- README explains query patterns"
```

<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Create example3-data-graph demonstrating lineage visualization

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4, wf-seminar.AC4.5

**Files:**
- Create: `04-aiida/example3-data-graph/README.md`

**Implementation:**

**File: `04-aiida/example3-data-graph/README.md`**

```markdown
# Example 3: Data Lineage Visualization

**Learning Objectives:**
- Visualize provenance graph
- Answer "where did this result come from?"
- Generate publication-grade documentation
- Use WorkGraph GUI

**Concepts:** Data lineage, graph visualization, reproducibility documentation

## Visualizing Provenance

```bash
# Generate graph for workflow
verdi node graph generate <PK> --output lineage.pdf

# View in browser (requires graphviz)
verdi node graph generate <PK> | dot -Tpng > lineage.png

# WorkGraph GUI (interactive)
workgraph web start
# Visit http://localhost:8000/workgraph
```

## Answering Origin Questions

For any result node PK:
```bash
# Show complete provenance
verdi node show <PK>

# Recursive ancestor tree
verdi node graph generate <PK> --ancestor-depth 999
```

## Publication-Ready Export

```bash
# Export with full provenance
verdi archive create --nodes <PK> publication.aiida

# Include all calculations
verdi archive create --all full_study.aiida
```

Publication archives enable reviewers to verify computational results years later.
```

**Verification:**

Run: `grep "provenance graph" 04-aiida/example3-data-graph/README.md`
Expected: Shows visualization concepts

**Commit:**

```bash
git add 04-aiida/example3-data-graph/
git commit -m "feat(aiida): add data-graph visualization example

- verdi commands for graph generation
- WorkGraph GUI usage
- Publication-grade export
- README explains lineage visualization"
```

<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Verify all AiiDA examples

**Verifies:** None (validation)

**Files:**
- None

**Implementation:**

Verify AiiDA examples work correctly.

**Steps:**

1. Verify profile configured: `verdi status`
2. Test example1: `cd 04-aiida/example1-workflow-def && verdi run workflow.py`
3. Test example2: `cd 04-aiida/example2-provenance && python query_provenance.py`
4. Test example3: `verdi node graph generate <PK>`

**Commit:** None

<!-- END_TASK_6 -->

<!-- START_TASK_7 -->
### Task 7: Final commit for Phase 6

**Verifies:** None

**Files:**
- None

**Implementation:**

Final Phase 6 commit.

**Commit:**

```bash
git add 04-aiida/
git commit -m "feat(aiida): complete AiiDA section with provenance examples

Phase 6 complete:
- Section README with provenance tracking concepts
- Database setup guide (PostgreSQL + RabbitMQ on SPIN)
- example1-workflow-def: WorkGraph with automatic provenance
- example2-provenance: Query and export capabilities
- example3-data-graph: Lineage visualization
- All examples demonstrate publication-grade reproducibility
- Progression from Merlin: adds comprehensive provenance"
```

<!-- END_TASK_7 -->
