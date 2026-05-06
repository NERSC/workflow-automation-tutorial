# Workflow Tool Comparison Matrix

A comprehensive comparison of five workflow management tools across five critical dimensions to enable evidence-based tool selection.

## Tool Overview

- **GNU Parallel:** Simple command-line parallelization tool
- **signac:** Parameter study framework with Python-based workflows
- **Maestro:** HPC workflow conductor with YAML specifications
- **Merlin:** Large-scale distributed workflow execution system
- **AiiDA:** Workflow engine with full provenance tracking

---

## Comparison Matrix

### Dimension 1: Interface

| Tool | Interface Style | Command Syntax | Python API | Learning Curve |
|------|-----------------|-----------------|-----------|-----------------|
| **GNU Parallel** | CLI-first | Simple: `seq 1 10 \| parallel command {}` | Limited/None | Very low - shell familiarity sufficient |
| **signac** | Python-centric | `signac init`, `signac run`, flow decorators | Rich and powerful | Medium - requires Python knowledge |
| **Maestro** | YAML specification | YAML-based workflow definition, `maestro run spec.yaml` | Python hooks available | Medium - YAML familiarity helpful |
| **Merlin** | YAML + Python | YAML workflow, Python studies, `merlin run spec.yaml` | Studies use Python natively | Medium-high - async patterns needed |
| **AiiDA** | Python API + CLI | `verdi` CLI, Python scripts, IPython notebooks | Core interface is Python | High - complex data model |

---

### Dimension 2: Infrastructure Requirements

| Tool | Required Backend | SPIN Deployment | Node Dependencies | Setup Complexity |
|------|------------------|-----------------|-------------------|-------------------|
| **GNU Parallel** | None | No special handling | None | None - pre-installed on Perlmutter |
| **signac** | None (local only) | Standard job submission | Python 3.6+ | Low - pip install sufficient |
| **Maestro** | None (local only) | Standard job submission | Python 3.6+, optional HPC plugins | Low - pip install, optional features |
| **Merlin** | Redis server (optional), PostgreSQL (optional for production) | Requires persistent worker processes | Python 3.8+, celery, Redis/RabbitMQ for distributed mode | Medium - separate server infrastructure needed |
| **AiiDA** | SQLite (training via `verdi presto`) or PostgreSQL + RabbitMQ (production) | Training: none. Production: persistent daemon required | Python 3.8+, multi-node capable | Low (training) / High (production) |

**SPIN Compatibility Notes:**
- **GNU Parallel:** Runs within allocation, no special SPIN setup needed
- **signac:** Runs within allocation boundaries, uses standard SLURM scheduling
- **Maestro:** Can run single-allocation or multi-step; respects allocation boundaries
- **Merlin:** Requires persistent workers beyond allocation - needs special handling for SPIN (separate worker submission or custom integration)
- **AiiDA:** Training mode (`verdi presto` with SQLite) runs on login and compute nodes with no SPIN setup. Production mode requires persistent daemon — SPIN containers for PostgreSQL + RabbitMQ, or workflow QOS for the daemon process.

---

### Dimension 3: Dependency Management

| Tool | Dependency Expression | Complex DAGs | Implicit Dependencies | Cycle Detection |
|------|----------------------|---------------|----------------------|-------------------|
| **GNU Parallel** | None - sequential only | Not supported | N/A | N/A |
| **signac** | Implicit: job order, manual coordination | Limited - must write custom logic | Yes, through job conditions | Manual |
| **Maestro** | Explicit: dependencies block syntax | Good - DAG-aware scheduling | Yes, declared in dependencies | Yes, runtime check |
| **Merlin** | Explicit: task dependency syntax | Excellent - full DAG support | Detected from task specs | Yes, verified at planning stage |
| **AiiDA** | Explicit: workchain control flow | Excellent - complex DAGs supported | Automatic link tracking | Yes, enforced in type system |

**Details:**
- GNU Parallel has no multi-step support (single workflow only)
- signac requires writing custom Python coordination logic for multi-step workflows
- Maestro supports branching, looping, and conditional dependencies
- Merlin excels at large DAGs with thousands of tasks
- AiiDA enforces dependency graph as part of execution model

---

### Dimension 4: Scale (Proven Capacity)

| Tool | Typical Scale | Maximum Observed | Scaling Bottleneck | Efficiency Loss |
|------|---------------|------------------|-------------------|-----------------|
| **GNU Parallel** | Hundreds of tasks | ~5,000 tasks | Memory (task buffering) | Minimal up to 1,000 |
| **signac** | Hundreds to thousands | ~50,000 parameter combinations | Filesystem (directory tree) | ~10% overhead beyond 10k |
| **Maestro** | Thousands to tens of thousands | ~100,000 tasks | DAG graph traversal | ~5% overhead beyond 50k |
| **Merlin** | Millions of tasks | Tested to 10M+ task submissions | Worker queue saturation | Variable, depends on Redis/DB |
| **AiiDA** | Thousands to hundreds of thousands | ~500k nodes in provenance graph | Database query performance | Significant beyond 100k |

**Practical Guidance:**
- GNU Parallel: 100-1,000 tasks (embarrassingly parallel only)
- signac: 100-50,000 parameter combinations
- Maestro: 1,000-100,000 task workflows
- Merlin: 10,000-10,000,000 task workflows
- AiiDA: 1,000-500,000 tasks with full provenance tracking

---

### Dimension 5: Sweet Spot Use Cases

| Tool | Primary Use Case | Secondary Uses | Not Suitable For |
|------|------------------|-----------------|------------------|
| **GNU Parallel** | Embarrassingly parallel tasks, quick parallelization of shell commands | Single-node batch processing, simple array jobs | Multi-step workflows, dependencies, complex scheduling |
| **signac** | Parameter space exploration, systematic study organization, small-to-medium ensembles | Research reproducibility, data management workflows | Large-scale distributed computing, provenance tracking |
| **Maestro** | HPC workflow orchestration, multi-step simulations, complex task dependencies | Workflow visualization, multi-allocation campaigns | Provenance-critical work, distributed non-HPC systems |
| **Merlin** | Massive parameter sweeps (>10k tasks), machine learning pipelines, high-throughput computing | Multi-allocation workflows, campaign management | Interactive development, small exploratory runs |
| **AiiDA** | Publication-ready research with full reproducibility, complex materials science workflows, data provenance requirements | Database-backed analysis frameworks, federated computing | Quick exploratory runs, simple linear workflows |

---

## Tool Selection Guide by Characteristics

### For "I have 100 tasks to run in parallel"
→ **GNU Parallel** (simplest, no setup needed)

### For "I need to organize 1,000 parameter combinations"
→ **signac** (excellent parameter management, Pythonic)

### For "I have 10,000 tasks with complex dependencies"
→ **Maestro** (good DAG support, straightforward YAML)

### For "I have 100,000+ tasks and need scaling"
→ **Merlin** (built for distributed scale)

### For "I need full reproducibility and publication-ready provenance"
→ **AiiDA** (strongest provenance tracking, complete audit trail)

---

## Graduate-To Paths

When a tool becomes insufficient, migration paths include:

- **From GNU Parallel → signac:** When you need parameter organization
- **From GNU Parallel → Maestro:** When you need multi-step workflows
- **From signac → Maestro:** When workflows become complex (dependencies, branching)
- **From Maestro → Merlin:** When scale exceeds 100k tasks
- **From signac/Maestro → AiiDA:** When provenance and publication requirements emerge

---

## Perlmutter/SPIN Compatibility Summary

| Tool | Allocation Boundary | Worker Persistence | Special SPIN Setup | Recommended |
|------|-------------------|-------------------|-------------------|------------|
| **GNU Parallel** | Runs within allocation | N/A | None | Yes - simple case |
| **signac** | Runs within allocation | N/A | None | Yes - parameter studies |
| **Maestro** | Can span allocations via multi-step submission | Optional | Standard multi-step | Yes - flexible |
| **Merlin** | Requires persistent workers | Yes - required | Custom integration | Possible - needs worker pool setup |
| **AiiDA** | Training: runs within allocation (SQLite). Production: requires persistent daemon | Training: no. Production: yes | Training: none. Production: SPIN containers for PostgreSQL + RabbitMQ | Yes (training) / Possible (production - needs SPIN setup) |

**Key Insight:** GNU Parallel, signac, and Maestro fit naturally within SPIN constraints. Merlin requires custom worker management. AiiDA's training mode (`verdi presto` with SQLite) runs anywhere on Perlmutter; production mode requires persistent daemon infrastructure via SPIN.

---

## Quick Decision Table

| Question | Tool A | Tool B | Tool C | Tool D | Tool E |
|----------|--------|--------|--------|--------|--------|
| **"What's simplest to start?"** | GNU Parallel | signac | Maestro | Merlin | AiiDA |
| **"What scales largest?"** | GNU Parallel | signac | Maestro | **Merlin** | AiiDA |
| **"What's best for HPC?"** | GNU Parallel | signac | **Maestro** | **Merlin** | AiiDA |
| **"What has best provenance?"** | GNU Parallel | signac | Maestro | Merlin | **AiiDA** |
| **"What works best on NERSC?"** | **GNU Parallel** | **signac** | **Maestro** | Merlin | AiiDA |

---

## Detailed Comparison by Dimension

### Interface Deep Dive

**GNU Parallel Interface:**
- Operates on shell command lines with substitution (`{}`)
- No state management - each invocation independent
- Excellent for ad-hoc parallelization, poor for reproducible workflows

**signac Interface:**
- Python decorators define workflow steps
- Filesystem-based parameter storage (job directories)
- Strong for exploratory research, systematic parameter exploration
- Flow syntax: `@FlowProject.operation` and `@FlowProject.script`

**Maestro Interface:**
- YAML specifications define workflow tasks and dependencies
- Block-based syntax (params, dependencies, merge patterns)
- Good balance between declarative and procedural
- DAG-aware with visualization support

**Merlin Interface:**
- YAML study definitions + Python sample generation
- Task-level specification with explicit dependencies
- Designed for distributed execution from day one
- Native async/await patterns for multi-step coordination

**AiiDA Interface:**
- Python-first: workchains, calcjobs, workflows
- IPython notebooks and `verdi` CLI for interaction
- Type system enforces data model constraints
- Serialization and storage automated

### Infrastructure Deep Dive

**GNU Parallel Infrastructure:**
- Zero setup - pre-installed on Perlmutter
- Tasks run in current shell/node
- No background services needed

**signac Infrastructure:**
- Python 3.6+ required
- Job data stored in project directory (filesystem-based)
- Optional file storage backends for large data
- Works with standard SLURM scheduling

**Maestro Infrastructure:**
- Python 3.6+ required, optional HPC plugin packages
- Workflow state in YAML and logs (filesystem-based)
- Execution via standard HPC schedulers
- No persistent services needed

**Merlin Infrastructure:**
- Redis (for task queue management) OR RabbitMQ
- PostgreSQL (optional, for advanced features)
- Master process and worker processes (distributed)
- Workers communicate with central queue
- Complex setup but enables true distributed computing

**AiiDA Infrastructure:**
- **Training:** SQLite via `verdi presto` (zero setup, runs on login/compute nodes, no daemon needed)
- **Production:** PostgreSQL (provenance storage at scale), RabbitMQ (daemon coordination), persistent daemon process
- Local file storage for input/output data
- Training mode uses synchronous `run()` execution; production mode uses asynchronous `submit()` with daemon
- Training-to-production upgrade path documented in `resources/aiida-production-deployment.md`

### Dependencies Deep Dive

**GNU Parallel:** No dependencies (single-level execution)

**signac:** Manual - relies on job condition files and Python logic:
```python
@FlowProject.operation
@FlowProject.post(lambda job: job.isfile("done"))
def step1(job): ...

@FlowProject.operation
@FlowProject.pre(lambda job: job.isfile("done"))
def step2(job): ...
```

**Maestro:** Explicit dependencies in YAML:
```yaml
dependencies:
  - {dependency: "task_a", dependence: "DONE"}
```
Good DAG support with branching/looping.

**Merlin:** Explicit task dependency specification:
```yaml
task: my_task
depends: [previous_task]
```
Full DAG support with thousands of tasks.

**AiiDA:** Dependencies implicit in workchain control flow:
```python
result = self.submit(CalculationJob, ...)
self.expose_outputs(result, ...)
```
Type system ensures compatibility; automatic tracking.

### Scale Deep Dive

**GNU Parallel Scale:**
- Task spawning: ~1,000/second
- Memory buffering: 10MB per 1,000 tasks
- Proven: 5,000 tasks
- Limit: Process spawning overhead

**signac Scale:**
- Parameter combinations: 50,000 typical
- Filesystem tree: 1 directory per combination
- Proven: 50,000 parameters
- Limit: Filesystem directory tree (HDD inode limits)

**Maestro Scale:**
- Tasks: 100,000 typical
- DAG graph traversal: ~100ms per traversal
- Proven: 100,000+ tasks
- Limit: Graph analysis time

**Merlin Scale:**
- Task submissions: 10,000,000+ demonstrated
- Queue latency: milliseconds per task
- Proven: 10M+ tasks in campaigns
- Limit: Redis/database I/O (mitigated via sharding)

**AiiDA Scale:**
- Provenance nodes: 500,000+ possible
- Query performance: degrades with size
- Proven: ~500k nodes (academic workflows)
- Limit: Database query time, disk I/O

---

## Implementation Notes

This matrix enables selection based on:

1. **Problem characteristics** (scale, dependencies, provenance needs)
2. **Operational constraints** (HPC vs local, persistent services available)
3. **Team capabilities** (shell scripting vs Python vs DevOps)
4. **NERSC-specific factors** (SPIN constraints, Perlmutter characteristics)

Use alongside the Decision Tree (separate document) for guided recommendations.
