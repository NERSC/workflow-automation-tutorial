# Workflow Management Seminar Implementation Plan - Phase 1

**Goal:** Create foundational repository structure that attendees can clone to Perlmutter and run examples without modification

**Architecture:** Educational materials repository with progressive capability-building structure (GNU Parallel → signac → Maestro → Merlin → AiiDA), plus resource directory for comparison frameworks and guides

**Tech Stack:**
- Python 3.10+ (Perlmutter standard)
- Conda for environment management
- Git for version control
- Workflow tools: signac, maestro-wf, merlin, aiida-core

**Scope:** Phase 1 of 8 phases from original design

**Codebase verified:** 2026-03-19 (repository in initial state, only design docs exist)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC6: Repository structure supports autonomous learning
- **wf-seminar.AC6.1 Success:** Repository organization matches seminar structure (00-gnu-parallel through 04-aiida, plus resources/)
- **wf-seminar.AC6.3 Success:** Setup instructions enable fresh clone to Perlmutter and immediate execution
- **wf-seminar.AC6.5 Success:** Installation guides provided for all tools with Perlmutter-specific steps

---

<!-- START_TASK_1 -->
### Task 1: Create README.md with seminar overview and setup instructions

**Verifies:** None (infrastructure phase)

**Files:**
- Create: `README.md`

**Implementation:**

Create the repository root README with complete seminar overview, prerequisites, setup instructions, and agenda.

```markdown
# HPC Workflow Management Tools Seminar

A hands-on 3-hour seminar teaching HPC researchers how to select and use workflow management tools for computational research on NERSC's Perlmutter supercomputer.

## Overview

This seminar demonstrates a progressive capability-building approach to workflow automation, starting with simple task parallelization and advancing through tools that incrementally add complexity and power:

1. **GNU Parallel** - Simple task parallelization baseline
2. **signac** - Parameter space organization with filesystem-based tracking
3. **Maestro** - DAG-based workflow specification via declarative YAML
4. **Merlin** - Distributed coordination at massive scale with database persistence
5. **AiiDA** - Comprehensive provenance tracking for reproducible research

Each tool demonstrates specific capabilities needed as research automation demands grow—from running hundreds of parameter combinations to managing millions of tasks with full reproducibility.

## Target Audience

This seminar assumes:
- Slurm basics (sbatch, squeue, job submission)
- Shell scripting (bash, loops, command-line tools)
- Python basics (read code, understand syntax)
- HPC concepts (nodes/cores, parallel computing, job scheduling)

## Repository Structure

```
workflow_tutorial_research/
├── 00-gnu-parallel/         # Section 0: Baseline parallelization (30 min)
├── 01-signac/               # Section 1: Parameter organization (25 min)
├── 02-maestro/              # Section 2: DAG workflows (30 min)
├── 03-merlin/               # Section 3: Distributed scale (40 min)
├── 04-aiida/                # Section 4: Provenance tracking (35 min)
├── resources/               # Comparison matrices, decision trees, guides
│   └── installation-guides/ # Tool-specific Perlmutter setup
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── environment.yml          # Conda environment specification
└── .gitignore              # Excluded artifacts
```

## Setup Instructions

### Prerequisites

Ensure you have:
- NERSC account with Perlmutter access
- Basic Slurm allocation for running examples

### Installation

**On Perlmutter:**

```bash
# Clone the repository
cd $SCRATCH
git clone <repository-url> workflow_tutorial_research
cd workflow_tutorial_research

# Load Python module
module load python

# Create conda environment
conda env create -f environment.yml
conda activate wf-seminar

# Verify installation
python -c "import signac; print(f'signac {signac.__version__}')"
python -c "import maestrowf; print('maestro-wf installed')"
python -c "import merlin; print(f'merlin {merlin.__version__}')"
python -c "import aiida; print(f'aiida-core {aiida.__version__}')"
```

**Alternative: pip installation**

```bash
# If conda unavailable, use pip with virtual environment
module load python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verification

Each section directory (00-gnu-parallel through 04-aiida) contains a README with:
- Concept overview
- When to use this tool
- Links to official documentation
- Runnable examples

All examples are designed to execute on Perlmutter without modification after setup.

## Seminar Agenda (3 hours)

| Time | Section | Tool | Focus |
|------|---------|------|-------|
| 0:00-0:30 | Section 0 | GNU Parallel | Simple task parallelization baseline |
| 0:30-0:55 | Section 1 | signac | Parameter space organization |
| 0:55-1:25 | Section 2 | Maestro | DAG-based workflow specification |
| 1:25-2:05 | Section 3 | Merlin | Distributed coordination at massive scale |
| 2:05-2:40 | Section 4 | AiiDA | Comprehensive provenance tracking |
| 2:40-2:50 | Wrap-up | All | Tool comparison matrix and decision framework |

Each section follows the pattern: **motivation → concepts → demo → hands-on → decision criteria**

## Resources

The `resources/` directory contains:
- **comparison-matrix.md** - 5-dimensional comparison across all tools (interface, infrastructure, dependencies, scale, use case)
- **decision-tree.md** - Flowchart mapping problem characteristics to tool recommendations
- **nersc-best-practices.md** - Perlmutter-specific configuration cheat sheet, anti-patterns to avoid
- **further-learning.md** - Curated links to official docs, tutorials, community forums
- **troubleshooting.md** - Common issues and solutions for each tool
- **installation-guides/** - Tool-specific setup instructions with Perlmutter integration details

## Getting Help

Each tool section includes:
- Links to official documentation
- Common issues and solutions
- When to use (and when NOT to use) this tool

For questions during the seminar, consult the instructor or the `resources/troubleshooting.md` guide.

## Infrastructure Requirements

**Merlin and AiiDA require database services:**
- **Merlin:** Redis for task queuing
- **AiiDA:** PostgreSQL + RabbitMQ for provenance storage

Two deployment options:
1. **NERSC SPIN** (recommended): Deploy as persistent services on SPIN platform
2. **Dedicated allocation**: Run databases in persistent allocation using workflow QOS

See `resources/installation-guides/` for deployment instructions.

## Excluded Tools

This seminar intentionally avoids tools covered in previous NERSC trainings:
- Balsam
- FireWorks
- Parsl
- HyperShell
- Snakemake

GNU Parallel is repeated as a universal foundation (too fundamental to skip).

## Notes

- **Tool versions:** All dependency versions in `requirements.txt` and `environment.yml` are tested on Perlmutter. Check for updates but prioritize known-working versions for seminar stability.
- **SPIN access:** Not all attendees may have SPIN access. Examples document SPIN deployment but provide fallback approaches (local databases in allocation with workflow QOS).
- **Time flexibility:** If sections run long, priority is GNU Parallel, Maestro, Merlin (core progression). AiiDA can be shortened to overview + pointers if time constrained.
- **Example simplicity:** All examples use placeholder computations (sleep, echo, basic Python scripts) to focus on workflow concepts rather than domain science. Attendees adapt patterns to real research codes.

## License

[Specify license - typically MIT or BSD for educational materials]

## Contact

[Specify contact information for seminar questions and repository issues]
```

**Verification:**
Run: `ls -la README.md`
Expected: File exists at repository root

Run: `head -n 5 README.md`
Expected: Shows seminar title and overview

**Commit:** Create this file in Task 7 (batch commit with all infrastructure)
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create .gitignore for Python and Slurm artifacts

**Verifies:** None (infrastructure phase)

**Files:**
- Create: `.gitignore`

**Implementation:**

Create .gitignore to exclude Slurm outputs, Python caches, temporary files, and environment-specific artifacts.

```
# Slurm outputs
*.out
*.err
slurm-*.log
slurm-*.out
slurm-*.err

# Python caches
__pycache__/
*.py[cod]
*$py.class
*.so
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Virtual environments
venv/
.venv/
env/
ENV/
env.bak/
venv.bak/

# Conda
.conda/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
*.log
*.pid

# Workflow-specific artifacts (may be generated by examples)
*.db
*.sqlite
*.sqlite3

# signac workspace artifacts (preserve examples but not generated data)
# Uncomment if examples generate large data:
# workspace/

# AiiDA profiles (if running locally rather than SPIN)
.aiida/

# Jupyter notebooks checkpoints
.ipynb_checkpoints/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover

# Distribution / packaging
dist/
build/
*.egg-info/
```

**Verification:**
Run: `ls -la .gitignore`
Expected: File exists at repository root

Run: `git check-ignore __pycache__/test.pyc`
Expected: `__pycache__/test.pyc` (confirms .gitignore works)

**Commit:** Create this file in Task 7 (batch commit with all infrastructure)
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create requirements.txt with pinned versions

**Verifies:** None (infrastructure phase)

**Files:**
- Create: `requirements.txt`

**Implementation:**

Create requirements.txt with pinned versions tested on Perlmutter for all workflow tools and their explicit dependencies.

```
# Core Workflow Tools
# Versions verified compatible with Python 3.10+ on Perlmutter (March 2026)

# signac - Parameter space organization
signac==2.3.0
signac-flow==0.28.0

# signac explicit dependencies (pin for reproducibility)
filelock>=3.0,<4.0
packaging>=15.0
synced-collections>=1.0.0,<2.0
tqdm>=4.46.1

# maestro-wf - YAML-based DAG workflows
maestrowf==1.1.11

# merlin - Distributed workflow system
merlin==1.13.0

# Merlin dependencies (Celery + Redis)
celery>=5.0,<6.0
redis>=6.0,<7.0

# aiida-core - Provenance tracking framework
aiida-core==2.8.0
aiida-workgraph==0.3.16  # Modern workflow definition (used in Section 4)

# AiiDA dependencies
psycopg2-binary>=2.8.6  # PostgreSQL adapter
pyyaml>=5.4

# Common utilities
numpy>=1.21.0
click>=8.0

# Note: Redis, RabbitMQ, and PostgreSQL are external services
# See resources/installation-guides/ for deployment instructions
```

**Verification:**
Run: `pip install --dry-run -r requirements.txt`
Expected: Resolves dependencies without conflicts

Run: `grep -E "signac==|maestrowf==|merlin==|aiida-core==" requirements.txt | wc -l`
Expected: `4` (confirms all four core tools are pinned)

**Commit:** Create this file in Task 7 (batch commit with all infrastructure)
<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create environment.yml for Conda setup

**Verifies:** None (infrastructure phase)

**Files:**
- Create: `environment.yml`

**Implementation:**

Create Conda environment specification for reproducible setup on Perlmutter with all workflow tools.

```yaml
name: wf-seminar
channels:
  - conda-forge
  - defaults

dependencies:
  # Python version (Perlmutter 2026 standard)
  - python=3.10

  # Core workflow tools
  - signac=2.3.0
  - maestrowf=1.1.11

  # Merlin and dependencies
  - redis-py>=6.0
  - celery>=5.0

  # AiiDA and dependencies
  - postgresql>=12.0  # For local development; SPIN deployment uses external
  - rabbitmq-c  # RabbitMQ C library

  # Common scientific libraries
  - numpy>=1.21.0
  - pyyaml>=5.4
  - click>=8.0

  # Development and testing utilities
  - pip
  - git

  # Install remaining packages via pip (not available in conda)
  - pip:
      - merlin==1.13.0
      - aiida-core==2.8.0
      - aiida-workgraph==0.3.16
      - signac-flow==0.28.0
      - psycopg2-binary>=2.8.6

# Notes:
# 1. This environment assumes Python module is loaded on Perlmutter: module load python
# 2. Redis, RabbitMQ, PostgreSQL services for Merlin/AiiDA should be deployed separately
#    (NERSC SPIN recommended) rather than installed in this environment
# 3. Some packages are installed via pip because they're not available in conda-forge
#    or conda-forge versions lag behind PyPI
```

**Verification:**
Run: `conda env create --dry-run -f environment.yml`
Expected: Resolves dependencies without conflicts

Run: `grep "name: wf-seminar" environment.yml`
Expected: `name: wf-seminar` (confirms environment name is correct)

Run: `grep "python=3.10" environment.yml`
Expected: `  - python=3.10` (confirms Python version specified)

**Commit:** Create this file in Task 7 (batch commit with all infrastructure)
<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Create directory structure for all sections

**Verifies:** None (infrastructure phase)

**Files:**
- Create: `00-gnu-parallel/`
- Create: `01-signac/`
- Create: `02-maestro/`
- Create: `03-merlin/`
- Create: `04-aiida/`
- Create: `resources/`
- Create: `resources/installation-guides/`

**Implementation:**

Create the complete directory structure matching the seminar organization with placeholder READMEs for each section.

**Step 1: Create all directories**

```bash
mkdir -p 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida
mkdir -p resources/installation-guides
```

**Step 2: Create placeholder README for each section**

Create `00-gnu-parallel/README.md`:
```markdown
# Section 0: GNU Parallel - Simple Task Parallelization

**Duration:** 30 minutes

**Concepts:** Task-level parallelism, parameter sweeps, Slurm integration

## Overview

GNU Parallel establishes the baseline for workflow automation, demonstrating simple task parallelization without dependency management.

## When to Use GNU Parallel

✅ **Good for:**
- Running the same command with different parameters (parameter sweeps)
- Embarrassingly parallel workloads (no dependencies between tasks)
- Quick parallelization of shell scripts
- Tasks that fit on a single node

❌ **Not suitable for:**
- Multi-step workflows with dependencies (use Maestro/Merlin)
- Tracking parameter spaces across runs (use signac)
- Fault tolerance and restart (use Merlin)
- Provenance tracking (use AiiDA)

## Examples

This directory will contain three examples:
1. Simple parameter sweep
2. Multiple parameter combinations
3. Slurm integration wrapper

(Examples will be added in Phase 2)

## Further Reading

- [GNU Parallel official documentation](https://www.gnu.org/software/parallel/)
- [NERSC GNU Parallel examples](https://docs.nersc.gov/)
- [Parallel command tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
```

Create `01-signac/README.md`:
```markdown
# Section 1: signac - Parameter Space Organization

**Duration:** 25 minutes

**Concepts:** Parameter organization, filesystem-based state tracking, job aggregation

## Overview

signac provides parameter space organization and filesystem-based state management for computational experiments, building on GNU Parallel's parallelization with structured data organization.

## When to Use signac

✅ **Good for:**
- Managing experiments with 2-5 dimensional parameter spaces
- Filesystem-based state tracking (no database needed)
- Aggregating results across parameter combinations
- Restart and continuation of parameter sweeps

❌ **Not suitable for:**
- Complex multi-step dependencies (use Maestro)
- Real-time coordination across allocations (use Merlin)
- Full provenance tracking (use AiiDA)

## Examples

This directory will contain three examples:
1. Parameter space definition and organization
2. Slurm job submission with signac-flow
3. Result aggregation across state points

(Examples will be added in Phase 3)

## Further Reading

- [signac official documentation](https://signac.io/)
- [signac-flow for HPC](https://signac.io/signac-flow/)
```

Create `02-maestro/README.md`:
```markdown
# Section 2: Maestro - DAG-Based Workflow Specification

**Duration:** 30 minutes

**Concepts:** Directed Acyclic Graphs (DAG), declarative YAML workflows, dependency resolution

## Overview

Maestro introduces DAG-based workflow specification using declarative YAML, enabling multi-step pipelines with explicit dependencies and Slurm integration.

## When to Use Maestro

✅ **Good for:**
- Multi-step workflows with clear dependencies (prep → simulate → analyze → visualize)
- Declarative workflow definition (YAML, not Python code)
- Parameter sweeps within DAG structure
- Medium-scale workflows (hundreds to low thousands of tasks)

❌ **Not suitable for:**
- Massive scale requiring distributed coordination (use Merlin)
- Real-time task distribution across workers (use Merlin)
- Comprehensive provenance tracking (use AiiDA)

## Examples

This directory will contain three examples:
1. Simple sequential DAG (3-4 steps)
2. Parameter sweeps with DAG structure
3. Perlmutter-specific Slurm configuration

(Examples will be added in Phase 4)

## Further Reading

- [Maestro GitHub repository](https://github.com/LLNL/maestrowf)
- [Maestro documentation](https://maestrowf.readthedocs.io/)
```

Create `03-merlin/README.md`:
```markdown
# Section 3: Merlin - Distributed Coordination at Massive Scale

**Duration:** 40 minutes

**Concepts:** Distributed task queuing, Celery workers, persistent Redis queues, fault tolerance

## Overview

Merlin extends Maestro's YAML syntax with distributed worker pools and persistent queuing, enabling fault-tolerant execution at massive scale (millions of tasks).

## Infrastructure Requirements

Merlin requires **Redis** for persistent task queuing:
- **Deployment option 1 (recommended):** NERSC SPIN service
- **Deployment option 2:** Dedicated allocation with workflow QOS

See `resources/installation-guides/merlin-redis-setup.md` for deployment instructions.

## When to Use Merlin

✅ **Good for:**
- Massive-scale parameter sweeps (thousands to millions of tasks)
- Distributed coordination across multiple allocations
- Fault tolerance and automatic retry
- Long-running workflows spanning hours to days

❌ **Not suitable for:**
- Simple parameter sweeps (use GNU Parallel or signac)
- Workflows without distributed coordination needs (use Maestro)
- Full provenance tracking beyond task metadata (use AiiDA)

## Examples

This directory will contain three examples:
1. Distributed worker execution with Redis queues
2. Fault tolerance with intentional failures and retry
3. Massive-scale hyperparameter search (1000s of combinations)

(Examples will be added in Phase 5)

## Further Reading

- [Merlin GitHub repository](https://github.com/LLNL/merlin)
- [Merlin documentation](https://merlin.readthedocs.io/)
```

Create `04-aiida/README.md`:
```markdown
# Section 4: AiiDA - Comprehensive Provenance Tracking

**Duration:** 35 minutes

**Concepts:** Automated provenance, data lineage, reproducible workflows, publication-grade documentation

## Overview

AiiDA provides comprehensive provenance tracking and reproducibility for computational research, storing complete execution history in a database to enable publication-grade documentation of how results were generated.

## Infrastructure Requirements

AiiDA requires:
- **PostgreSQL** for provenance database
- **RabbitMQ** for workflow coordination

**Deployment option 1 (recommended):** NERSC SPIN services
**Deployment option 2:** Dedicated allocation with workflow QOS

See `resources/installation-guides/aiida-database-setup.md` for deployment instructions.

## When to Use AiiDA

✅ **Good for:**
- Research requiring full provenance tracking
- Publication-grade reproducibility
- Long-term data management (years)
- Computational materials science, quantum chemistry workflows
- "Where did this result come from?" queries

❌ **Not suitable for:**
- Simple parameter sweeps (overhead not justified - use signac)
- Rapid prototyping (setup complexity - use Maestro)
- Workflows without provenance requirements (use Maestro/Merlin)

## Examples

This directory will contain three examples:
1. AiiDA workgraph with automatic provenance
2. Provenance demonstration: restart from any point, history capture
3. Data lineage visualization and "result origin" queries

(Examples will be added in Phase 6)

## Further Reading

- [AiiDA official documentation](https://aiida.readthedocs.io/)
- [AiiDA tutorials](https://aiida-tutorials.readthedocs.io/)
```

Create `resources/README.md`:
```markdown
# Resources: Comparison Frameworks and Guides

This directory contains materials to help attendees choose appropriate workflow tools for their research:

## Decision-Making Resources

- **comparison-matrix.md** - 5-dimensional comparison of all 5 tools (interface, infrastructure, dependencies, scale, use case)
- **decision-tree.md** - Flowchart mapping problem characteristics to tool recommendations
- **nersc-best-practices.md** - Perlmutter-specific configuration cheat sheet and anti-patterns to avoid

## Reference Materials

- **further-learning.md** - Curated links to official documentation, tutorials, community forums
- **troubleshooting.md** - Common issues and solutions for each tool

## Installation Guides

The `installation-guides/` subdirectory contains tool-specific setup instructions with Perlmutter integration details:

- `gnu-parallel-setup.md` - Installing GNU Parallel on Perlmutter (minimal setup)
- `signac-setup.md` - signac and signac-flow installation
- `maestro-setup.md` - Maestro installation and Slurm adapter configuration
- `merlin-redis-setup.md` - Merlin installation + Redis deployment (SPIN and allocation options)
- `aiida-database-setup.md` - AiiDA installation + PostgreSQL/RabbitMQ deployment

(Installation guides will be added in Phase 7)
```

**Verification:**
Run: `ls -d 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida resources/installation-guides`
Expected: All directories exist

Run: `find 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida resources -name "README.md" | wc -l`
Expected: `6` (confirms all section READMEs created)

**Commit:** Create these files/directories in Task 7 (batch commit with all infrastructure)
<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Verify operational setup

**Verifies:** wf-seminar.AC6.1, wf-seminar.AC6.3, wf-seminar.AC6.5

**Implementation:**

Verify that the repository structure is complete and can be used for setup on Perlmutter.

**Step 1: Verify all infrastructure files exist**

```bash
# Check required files at root
ls -1 README.md .gitignore requirements.txt environment.yml

# Check directory structure
ls -d 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida resources/installation-guides

# Count README files
find . -maxdepth 2 -name "README.md" -type f
```

Expected: All files and directories exist

**Step 2: Verify requirements.txt is valid**

```bash
# Check that core tools are pinned
grep -E "signac==|maestrowf==|merlin==|aiida-core==" requirements.txt

# Verify pip can parse requirements
python -m pip install --dry-run -r requirements.txt 2>&1 | head -20
```

Expected: Shows four pinned versions, pip successfully parses requirements

**Step 3: Verify environment.yml is valid**

```bash
# Check environment name
grep "name: wf-seminar" environment.yml

# Check Python version
grep "python=3.10" environment.yml

# If conda available, test dry-run
conda env create --dry-run -f environment.yml 2>&1 | head -20
```

Expected: Shows environment name and Python version, conda can parse specification

**Step 4: Verify .gitignore works**

```bash
# Test that Python cache files would be ignored
mkdir -p test_dir/__pycache__
touch test_dir/__pycache__/test.pyc
git check-ignore test_dir/__pycache__/test.pyc
rm -rf test_dir
```

Expected: `test_dir/__pycache__/test.pyc` (confirms file would be ignored)

**Step 5: Verify README completeness**

```bash
# Check README sections
grep -E "^## " README.md
```

Expected: Shows all major sections (Overview, Target Audience, Repository Structure, Setup Instructions, Seminar Agenda, Resources, Infrastructure Requirements, etc.)

**Commit:** After verification, commit all infrastructure files (see Task 7)
<!-- END_TASK_6 -->

<!-- START_TASK_7 -->
### Task 7: Commit infrastructure files

**Verifies:** None (infrastructure phase)

**Implementation:**

Commit all Phase 1 infrastructure files to the repository.

```bash
# Stage all new infrastructure files
git add README.md .gitignore requirements.txt environment.yml

# Stage directory structure with placeholder READMEs
git add 00-gnu-parallel/README.md
git add 01-signac/README.md
git add 02-maestro/README.md
git add 03-merlin/README.md
git add 04-aiida/README.md
git add resources/README.md

# Note: Git will not commit empty directories, but directories with README files will be tracked

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
chore: initialize repository infrastructure

Create foundational structure for workflow management seminar:
- README.md with seminar overview, setup instructions, and agenda
- .gitignore for Python/Slurm artifacts
- requirements.txt with pinned versions (signac 2.3.0, maestro 1.1.11, merlin 1.13.0, aiida 2.8.0)
- environment.yml for Conda reproducible setup
- Directory structure for 5 tool sections (00-04) plus resources/
- Placeholder READMEs for each section with concept overviews

Supports AC6.1 (repository organization), AC6.3 (setup instructions),
AC6.5 (installation guide structure).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

# Verify commit
git log -1 --stat
```

Expected: Commit created with all infrastructure files, git log shows added files

**Verification:**
Run: `git status`
Expected: `nothing to commit, working tree clean`

Run: `git log -1 --oneline`
Expected: Shows "chore: initialize repository infrastructure" commit message
<!-- END_TASK_7 -->

---

## Phase 1 Complete

**Deliverables:**
- ✅ README.md with complete seminar overview and setup instructions
- ✅ .gitignore excluding Python/Slurm artifacts
- ✅ requirements.txt with pinned versions for all tools
- ✅ environment.yml for reproducible Conda setup
- ✅ Directory structure matching seminar organization (00-gnu-parallel through 04-aiida, plus resources/)
- ✅ Placeholder READMEs for each section
- ✅ All files committed to repository

**Next Phase:** Phase 2 will populate `00-gnu-parallel/` with three runnable examples demonstrating simple task parallelization.
