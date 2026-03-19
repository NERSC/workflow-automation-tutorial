# Workflow Management Seminar Design

## Summary

This design document outlines a 3-hour hands-on seminar teaching HPC researchers how to select and use workflow management tools for computational research on NERSC's Perlmutter supercomputer. The seminar uses a progressive capability-building approach, starting with GNU Parallel for simple task parallelization and advancing through five tools that incrementally add complexity: signac for parameter space organization, Maestro for DAG-based dependencies, Merlin for distributed coordination at massive scale, and AiiDA for comprehensive provenance tracking. Each tool demonstrates specific capabilities needed as research automation demands grow, from running hundreds of parameter combinations to managing millions of tasks with full reproducibility.

The implementation approach creates a git repository containing runnable examples for each tool, organized into sections matching the seminar flow. All examples are designed to execute on Perlmutter without modification, with Slurm integration and NERSC-specific best practices built in. The seminar demonstrates both filesystem-based (signac, Maestro) and database-backed (Merlin, AiiDA) workflow paradigms, deliberately avoiding tools covered in previous NERSC trainings (Balsam, FireWorks, Parsl, HyperShell, Snakemake). Supporting materials include a comparison matrix, decision framework, and troubleshooting guides to help attendees choose appropriate tools for their specific research needs.

## Definition of Done

**Primary Deliverable:** A research-based design document that enables building the seminar, containing:

1. **Tool Selection & Rationale** - Identification of 4-8 workflow tools (beyond GNU Parallel) organized into 4 task categories:
   - Preparing computational work
   - Submitting work to systems
   - Responding to outcomes (dependencies, retries, error handling)
   - Organizing data

   Each tool selection justified by: why it fits the category, why it's better than alternatives, what it teaches that others don't, how it runs on Perlmutter/Slurm (or SPIN for specific cases).

2. **Seminar Structure Outline** - Content organization showing:
   - Section 0: GNU Parallel as foundation/baseline
   - Sections 1-4: Each task category with 1-2 selected tools showing progression
   - How tools build on each other within categories
   - Estimated time allocation (~3 hours total)

3. **Tool Comparison Framework** - Matrix or structured comparison showing how the selected tools differ across dimensions like: interface type, learning curve, use case strengths, Perlmutter/SPIN compatibility, when to choose each.

4. **Example Specifications** - For each tool, description of what examples should demonstrate (not the code itself), such as: "Show tool X managing multi-step pipeline with file dependencies" - enough detail to guide implementation later.

**Out of Scope:**
- Writing actual example code
- Creating slides or presentation materials
- Building the git repository
- Tools already covered in previous trainings: Balsam, FireWorks, Parsl, HyperShell, Snakemake

## Acceptance Criteria

### wf-seminar.AC1: Tool selections are justified and appropriate for HPC audience
- **wf-seminar.AC1.1 Success:** Each of 5 tools (GNU Parallel, signac, Maestro, Merlin, AiiDA) has documented rationale explaining why it fits its category
- **wf-seminar.AC1.2 Success:** Tool justifications include: category fit, advantages over alternatives, unique teaching value, Perlmutter/Slurm compatibility
- **wf-seminar.AC1.3 Success:** Excluded tools (Balsam, FireWorks, Parsl, HyperShell, Snakemake) are not included in seminar sections
- **wf-seminar.AC1.4 Success:** Tool progression demonstrates capability building (parallelism → organization → dependencies → scale → provenance)
- **wf-seminar.AC1.5 Success:** Both paradigms represented (filesystem: signac/Maestro; database: Merlin/AiiDA)
- **wf-seminar.AC1.6 Failure:** Tools requiring commercial licenses are not included
- **wf-seminar.AC1.7 Failure:** Tools with poor HPC/Slurm integration are not selected without documented workarounds

### wf-seminar.AC2: Seminar structure is pedagogically sound and time-appropriate
- **wf-seminar.AC2.1 Success:** Structure includes Section 0 (GNU Parallel foundation) plus 4 category sections
- **wf-seminar.AC2.2 Success:** Time allocations sum to ~180 minutes (3 hours) with specific breakdown per section
- **wf-seminar.AC2.3 Success:** Each section follows pattern: motivation → concepts → demo → hands-on → decision criteria
- **wf-seminar.AC2.4 Success:** Tools build on previous sections (signac uses Parallel concepts, Maestro adds to signac, etc.)
- **wf-seminar.AC2.5 Success:** Audience assumptions documented (Slurm basics, shell scripting, Python basics, HPC concepts)
- **wf-seminar.AC2.6 Edge:** Flexibility documented for time overruns (priority ordering, reducible sections)

### wf-seminar.AC3: Comparison framework enables tool selection decisions
- **wf-seminar.AC3.1 Success:** Matrix compares all 5 tools across 5 dimensions (interface, infrastructure, dependencies, scale, use case)
- **wf-seminar.AC3.2 Success:** Decision framework provides clear guidance mapping problem characteristics to tool recommendations
- **wf-seminar.AC3.3 Success:** Each tool has documented "sweet spot" use case where it's the best choice
- **wf-seminar.AC3.4 Success:** Framework includes "when to graduate" criteria (when tool becomes insufficient)
- **wf-seminar.AC3.5 Success:** Perlmutter/SPIN compatibility documented for each tool

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 example specifications (15 total across 5 tools)
- **wf-seminar.AC4.2 Success:** Example specs describe learning objectives, not implementation code
- **wf-seminar.AC4.3 Success:** Examples progress from simple to complex within each tool section
- **wf-seminar.AC4.4 Success:** All examples specify they must run on Perlmutter without modification
- **wf-seminar.AC4.5 Success:** Example specifications include: what to demonstrate, expected concepts learned, sample use case
- **wf-seminar.AC4.6 Failure:** Example specs do not include actual implementation code (that's out of scope)

### wf-seminar.AC5: NERSC/Perlmutter integration is accurate and complete
- **wf-seminar.AC5.1 Success:** Perlmutter-specific configuration documented for each tool (Slurm integration, filesystem usage, QOS options)
- **wf-seminar.AC5.2 Success:** Anti-patterns from NERSC best practices explicitly called out (srun loops, scheduler query limits, job arrays)
- **wf-seminar.AC5.3 Success:** SPIN integration documented for database-backed tools (Merlin, AiiDA)
- **wf-seminar.AC5.4 Success:** Filesystem guidance specifies $SCRATCH for workflows, CFS for long-term storage
- **wf-seminar.AC5.5 Success:** Workflow QOS usage documented for persistent coordinator processes
- **wf-seminar.AC5.6 Edge:** Fallback approaches documented for attendees without SPIN access

### wf-seminar.AC6: Repository structure supports autonomous learning
- **wf-seminar.AC6.1 Success:** Repository organization matches seminar structure (00-gnu-parallel through 04-aiida, plus resources/)
- **wf-seminar.AC6.2 Success:** Each section includes README with concepts, when to use, and links to official documentation
- **wf-seminar.AC6.3 Success:** Setup instructions enable fresh clone to Perlmutter and immediate execution
- **wf-seminar.AC6.4 Success:** Resource materials include comparison matrix, decision tree, troubleshooting guide, further learning links
- **wf-seminar.AC6.5 Success:** Installation guides provided for all tools with Perlmutter-specific steps

## Glossary

- **AiiDA**: Open-source Python framework for computational science workflows emphasizing automated provenance tracking and reproducibility, storing complete execution history in a database to enable publication-grade documentation of how results were generated

- **DAG (Directed Acyclic Graph)**: Workflow representation where tasks are nodes and dependencies are edges, with execution flowing in one direction without cycles, enabling tools like Maestro to determine which tasks can run in parallel and which must wait for prerequisites

- **GNU Parallel**: Shell-based tool for executing independent tasks in parallel on a single node, serving as the entry point for workflow automation by providing simple parameter sweeps without dependency management

- **Maestro**: YAML-based workflow orchestration tool developed at LLNL that uses declarative specifications to define multi-step DAGs with parameter sweeps and Slurm integration, positioning between filesystem organization and distributed coordination

- **Merlin**: Distributed workflow system built on Celery and Redis (also from LLNL) that extends Maestro's YAML syntax with worker pools and persistent queuing for fault-tolerant execution at massive scale (millions of tasks)

- **Perlmutter**: NERSC's primary supercomputer (HPE Cray EX system) where all seminar examples must run, featuring AMD CPUs, NVIDIA A100 GPUs, Lustre filesystems, and Slurm scheduling

- **Provenance**: Complete historical record of workflow execution including input data, parameters, code versions, and dependencies that produced specific results, enabling verification of computational reproducibility

- **signac**: Python framework for managing parameter spaces and computational experiments using filesystem-based state tracking, where each parameter combination gets a unique directory containing job data and metadata

- **Slurm**: Workload manager used on Perlmutter for job scheduling and resource allocation, requiring proper integration patterns to avoid anti-patterns like srun loops or excessive scheduler queries

- **SPIN**: NERSC's Kubernetes-based platform for persistent services (contrast with batch computing on Perlmutter), used in this seminar for hosting databases (Redis for Merlin, PostgreSQL/RabbitMQ for AiiDA) that support workflow coordination

- **$SCRATCH**: Perlmutter's high-performance Lustre filesystem intended for temporary workflow data with 8-week retention policy, contrasted with Community File System (CFS) for long-term storage

- **Workflow QOS**: NERSC Quality of Service option for running lightweight persistent coordinator processes (daemons) that manage workflow execution without consuming excessive allocation hours

- **YAML**: Human-readable data serialization format used by Maestro and Merlin for declarative workflow specification, allowing researchers to define complex DAGs without imperative programming

## Architecture

The seminar uses a **progressive capability building** architecture where each tool incrementally adds capabilities to address increasingly complex research automation needs. The unifying narrative: "Start with simple parallelization, grow capabilities as research demands."

**Overall Flow:**
- **Section 0 (30 min)**: GNU Parallel establishes baseline automation vocabulary - simple task parallelization without dependencies
- **Category 1 (25 min)**: signac adds parameter space organization using filesystem-based tracking
- **Category 2 (30 min)**: Maestro introduces DAG-based workflow specification via declarative YAML
- **Category 3 (40 min)**: Merlin adds distributed coordination with database persistence for massive scale
- **Category 4 (35 min)**: AiiDA demonstrates comprehensive provenance tracking for reproducible research
- **Wrap-up (10 min)**: Tool comparison matrix and decision framework

**Capability Progression:**
1. **Parallelism** (GNU Parallel) → Task-level execution, no dependency management
2. **Organization** (signac) → Parameter tracking, filesystem-based state
3. **Dependencies** (Maestro) → DAG workflow, declarative specification
4. **Scale & Persistence** (Merlin) → Distributed queuing, fault tolerance, millions of tasks
5. **Provenance** (AiiDA) → Full reproducibility, publication-grade workflows

This architecture demonstrates both paradigms (filesystem: signac/Maestro; database: Merlin/AiiDA) while maintaining clear conceptual progression.

**Delivery Format:**
- Zoom presentation with optional in-person attendance
- Git repository cloneable to Perlmutter containing all examples
- Examples runnable without modification on Perlmutter
- Each section follows pattern: motivation → concepts → demo → hands-on → decision criteria

**Target Audience Assumptions:**
- Slurm basics (sbatch, squeue)
- Shell scripting (bash, loops)
- Python basics (read code, understand syntax)
- HPC concepts (nodes/cores, parallel computing, job scheduling)

## Existing Patterns

Research revealed established patterns from NERSC documentation and broader HPC workflow community that this design incorporates:

**From NERSC Official Guidance:**
- **GNU Parallel as entry point**: NERSC explicitly recommends GNU Parallel for simple parallelization before graduating to workflow systems
- **Workflow QOS pattern**: For tools requiring persistent coordinators (Merlin, AiiDA), use NERSC's workflow QOS for lightweight daemon processes
- **$SCRATCH filesystem usage**: All examples use Lustre $SCRATCH for intermediate files (8-week retention documented)
- **Anti-pattern warnings**: Avoid srun loops, excessive scheduler queries, naive job arrays - explicitly teach against these based on NERSC best practices

**From DOE Lab Standards (LLNL):**
- **YAML-based DAG specification**: Maestro → Merlin progression mirrors LLNL's production workflow stack
- **Distributed task queuing**: Merlin's Celery + Redis pattern proven at 100M+ task scale on Sierra supercomputer
- **Ensemble workflow focus**: Aligns with DOE trend toward ML/AI + simulation convergence

**From HPC Workflow Community:**
- **Progressive tool adoption**: Matches community consensus that users should start simple and add complexity only when needed
- **Provenance emphasis**: AiiDA's comprehensive provenance reflects growing requirement for reproducibility in computational science
- **Container integration**: Examples will note Apptainer/Singularity for reproducible environments (industry best practice 2025-2026)

**Divergence from Previous NERSC Trainings:**
This design intentionally avoids tools covered in previous DOE/NERSC trainings:
- **Excluded**: Balsam, FireWorks, Parsl, HyperShell, Snakemake
- **Rationale**: Attendees may have seen these; fresh tools expand toolkit
- **Exception**: GNU Parallel repeated as universal foundation (too fundamental to skip)

**SPIN Integration Pattern:**
- SPIN used for persistent service hosting (Redis for Merlin, PostgreSQL/RabbitMQ for AiiDA)
- Not used for computational workflows (wrong paradigm - that's Perlmutter/Slurm's domain)
- Demonstrates when Kubernetes supplements batch systems vs replaces them

## Implementation Phases

Implementation broken into 8 discrete phases corresponding to seminar sections plus infrastructure and validation.

<!-- START_PHASE_1 -->
### Phase 1: Repository Infrastructure Setup

**Goal:** Create foundational repository structure that attendees can clone to Perlmutter and run examples without modification.

**Components:**
- `README.md` — Seminar overview, setup instructions, agenda with time allocations
- `.gitignore` — Exclude Slurm outputs, Python caches, temporary files
- `requirements.txt` — Python dependencies for all tools (signac, maestro-wf, merlin, aiida-core)
- `environment.yml` — Conda environment specification for reproducible setup
- Top-level directory structure (`00-gnu-parallel/`, `01-signac/`, `02-maestro/`, `03-merlin/`, `04-aiida/`, `resources/`)
- `resources/installation-guides/` — Tool-specific setup instructions for Perlmutter

**Dependencies:** None (first phase)

**Done when:** Repository structure exists, `README.md` has complete setup instructions, Python environment specifications are valid and installable on Perlmutter, directory tree matches architecture design

<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: GNU Parallel Section

**Goal:** Create baseline examples demonstrating simple task parallelization that establish automation vocabulary for the seminar.

**Components:**
- `00-gnu-parallel/README.md` — Concept overview, when to use, limitations
- `00-gnu-parallel/example1-parameter-sweep/` — Simple parallel execution demo with parameter variations
- `00-gnu-parallel/example2-multi-param/` — Multiple parameter combinations using `:::` syntax
- `00-gnu-parallel/example3-slurm-integration/` — Wrapper sbatch scripts showing proper integration
- Each example includes: working code, sample data/generation script, expected output, explanation of concepts
- `resources/nersc-best-practices.md` — Anti-patterns section documenting srun loops, scheduler query issues

**Dependencies:** Phase 1 (repository structure)

**Done when:** All three examples run successfully on Perlmutter, demonstrate proper `--jobs` usage, show `$SLURM_CPUS_ON_NODE` integration, README explains progression to workflow tools

<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: signac Section

**Goal:** Demonstrate parameter space organization and filesystem-based state management for computational experiments.

**Components:**
- `01-signac/README.md` — Parameter organization concepts, filesystem schema, when signac beats manual organization
- `01-signac/example1-parameter-space/` — Define 2-3 dimensional parameter space, show auto-generated directory structure
- `01-signac/example2-job-submission/` — signac-flow integration for Slurm template generation
- `01-signac/example3-aggregation/` — Query completed jobs, aggregate results across parameter combinations
- signac project initialization showing parameter state points
- Slurm submission templates using signac-flow

**Dependencies:** Phase 2 (builds on GNU Parallel parameter concepts)

**Done when:** Examples demonstrate parameter space definition, automatic organization, integration with Slurm, result aggregation across state points, clear transition from Phase 2's manual parameter handling

<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: Maestro Section

**Goal:** Introduce declarative DAG-based workflow specification showing when dependencies require workflow orchestration beyond parameter organization.

**Components:**
- `02-maestro/README.md` — DAG concepts, YAML specification syntax, when Maestro improves on signac
- `02-maestro/example1-simple-dag/` — 3-4 step sequential workflow (prep → simulate → analyze → visualize)
- `02-maestro/example2-param-sweeps/` — Maestro's parameter syntax combined with DAG structure
- `02-maestro/example3-slurm-config/` — Perlmutter-specific batch configuration in YAML
- YAML workflow specifications
- Slurm adapter configuration for Perlmutter

**Dependencies:** Phase 3 (signac establishes parameters; Maestro adds dependencies)

**Done when:** Examples demonstrate DAG dependency resolution, parameter sweeps with workflow structure, Slurm integration via YAML config, variable substitution for paths/accounts, clear progression from filesystem organization to orchestration

<!-- END_PHASE_4 -->

<!-- START_PHASE_5 -->
### Phase 5: Merlin Section

**Goal:** Demonstrate distributed task queuing for massive scale and persistent coordination, showing when single-coordinator limits are exceeded.

**Components:**
- `03-merlin/README.md` — Distributed coordination concepts, when to use Merlin vs Maestro, infrastructure requirements
- `03-merlin/example1-distributed/` — Merlin spec extending Maestro YAML with workers, demonstrate Redis queue, show task distribution
- `03-merlin/example2-fault-tolerance/` — Workflow with intentional failures showing retry and persistence
- `03-merlin/example3-massive-scale/` — Hyperparameter search with 1000s of combinations
- Merlin YAML specifications building on Maestro syntax
- Redis deployment guide for SPIN
- Worker pool configuration matching Perlmutter architecture
- `resources/installation-guides/merlin-redis-setup.md` — SPIN deployment or dedicated allocation options

**Dependencies:** Phase 4 (Maestro YAML foundation)

**Done when:** Examples demonstrate distributed execution across allocations, persistent queue survives restarts, fault tolerance with retries, scale beyond single-coordinator capacity, Redis setup documented for SPIN, clear justification for infrastructure investment

<!-- END_PHASE_5 -->

<!-- START_PHASE_6 -->
### Phase 6: AiiDA Section

**Goal:** Demonstrate comprehensive provenance tracking and reproducibility for publication-grade computational research.

**Components:**
- `04-aiida/README.md` — Provenance concepts, when AiiDA complexity justified, database requirements
- `04-aiida/example1-workflow-def/` — AiiDA workgraph for multi-step calculation with automatic provenance
- `04-aiida/example2-provenance/` — Demonstrate full history capture, restart from any point, documentation generation
- `04-aiida/example3-data-graph/` — Visualize workflow execution with all dependencies, answer "where did this result come from?"
- AiiDA workflow definitions (workgraph or workchain)
- Slurm computer configuration for Perlmutter
- `resources/installation-guides/aiida-database-setup.md` — PostgreSQL + RabbitMQ deployment on SPIN with Perlmutter integration

**Dependencies:** Phase 5 (establishes database-backed paradigm; AiiDA extends with provenance)

**Done when:** Examples demonstrate automatic provenance capture, reproducibility verification, data lineage visualization, long-term research data management, database setup documented for SPIN, clear value proposition for comprehensive infrastructure

<!-- END_PHASE_6 -->

<!-- START_PHASE_7 -->
### Phase 7: Comparison Framework and Resources

**Goal:** Provide decision-making tools and reference materials enabling attendees to choose appropriate tools for their research.

**Components:**
- `resources/comparison-matrix.md` — 5-dimensional matrix (interface, infrastructure, dependencies, scale, use case) for all 5 tools
- `resources/decision-tree.md` — Flowchart mapping problem characteristics to tool recommendations
- `resources/nersc-best-practices.md` — Perlmutter-specific configuration cheat sheet (completed from Phase 2 foundation)
- `resources/further-learning.md` — Curated links to official docs, tutorials, community forums
- `resources/troubleshooting.md` — Common issues and solutions for each tool
- Each tool's README updated with "When to Use This Tool" section referencing decision framework

**Dependencies:** Phases 2-6 (all tool examples must exist to create meaningful comparison)

**Done when:** Comparison matrix covers all 5 dimensions for 5 tools, decision tree maps common scenarios to tool choices, NERSC cheat sheet has Perlmutter-specific snippets, all links verified as current (2026), troubleshooting covers issues discovered during example development

<!-- END_PHASE_7 -->

<!-- START_PHASE_8 -->
### Phase 8: Integration Testing and Validation

**Goal:** Verify all examples run correctly on Perlmutter, documentation is accurate, and attendees can successfully clone and execute.

**Components:**
- Test plan documenting validation for each example
- Fresh Perlmutter allocation for clean testing
- Verification that all examples run without modification after `git clone`
- Validation of setup instructions (can a new user follow them?)
- Check that resource estimates (time allocations per section) are realistic
- Review of all documentation for accuracy and completeness
- Final repository cleanup (remove debug artifacts, ensure .gitignore works)

**Dependencies:** Phases 1-7 (all content must exist)

**Done when:** All 15 examples (3 per tool) execute successfully on fresh Perlmutter clone, setup instructions validated by non-author, time estimates confirmed realistic, all documentation links valid, repository clean and ready for distribution, README reflects actual content

<!-- END_PHASE_8 -->

## Additional Considerations

**Infrastructure Dependencies:**

**Merlin and AiiDA require database services.** Two deployment options:
1. **SPIN hosting (recommended)**: Deploy Redis (Merlin) and PostgreSQL + RabbitMQ (AiiDA) as persistent services on SPIN. Examples include SPIN deployment guides.
2. **Dedicated allocation**: Run database in persistent allocation using workflow QOS (requires request form to NERSC).

SPIN recommended for production use; dedicated allocation acceptable for seminar demos if SPIN unavailable.

**Perlmutter-Specific Warnings:**

Examples explicitly teach against anti-patterns documented in NERSC best practices:
- **srun loops**: Show why this causes scheduler contention
- **Excessive scheduler queries**: Demonstrate rate limiting requirements
- **Naive job arrays**: Explain why GNU Parallel preferred for small tasks
- **Filesystem misuse**: Show $SCRATCH for workflows, CFS for long-term storage

**Time Allocation Flexibility:**

Total ~180 minutes (3 hours) with listed allocations. If sections run long:
- **Priority 1**: GNU Parallel, Maestro, Merlin (core progression)
- **Reducible**: AiiDA can be shortened to overview + pointer to resources if time constrained
- **Buffer**: 10-minute wrap-up can absorb ~5 minutes from earlier overruns

**Example Complexity:**

All examples use simple placeholder computations (sleep, echo, basic Python scripts) to focus on workflow concepts rather than domain science. Attendees adapt patterns to real research codes.

**Tool Version Pinning:**

`requirements.txt` and `environment.yml` pin specific versions tested on Perlmutter. Include note about checking for updates but prioritizing known-working versions for seminar stability.

**SPIN Access:**

Not all attendees may have SPIN access. Examples document SPIN deployment but provide fallback approaches (local Redis/PostgreSQL in allocation with workflow QOS) for Merlin/AiiDA sections.
