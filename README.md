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
