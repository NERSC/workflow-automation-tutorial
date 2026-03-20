# Workflow Management Seminar Implementation Plan - Phase 3

**Goal:** Demonstrate parameter space organization and filesystem-based state management for computational experiments

**Architecture:** Three examples showing signac's progression: parameter space definition → Slurm job submission with signac-flow → result aggregation across state points

**Tech Stack:**
- signac 2.3.0 (parameter space organization)
- signac-flow 0.28.0 (Slurm integration)
- Python 3.10+

**Scope:** Phase 3 of 8 phases from original design

**Codebase verified:** 2026-03-19 (Phases 1-2 infrastructure will exist)

---

## Acceptance Criteria Coverage

This phase implements and tests:

### wf-seminar.AC4: Example specifications guide implementation
- **wf-seminar.AC4.1 Success:** Each tool has 3 example specifications - Phase 3 provides 3 signac examples
- **wf-seminar.AC4.3 Success:** Examples progress from simple to complex (parameter space → job submission → aggregation)
- **wf-seminar.AC4.4 Success:** All examples run on Perlmutter without modification

---

## Implementation Note

This is an educational materials project creating runnable examples (not production code). Verification is operational (examples execute successfully) rather than unit-tested. See Phase 1B investigation findings for testing methodology.

---

<!-- START_TASK_1 -->
### Task 1: Update 01-signac/README.md

**Verifies:** None (infrastructure)

**Files:**
- Modify: `01-signac/README.md`

**Implementation:**

Replace placeholder with complete signac overview, concepts, when to use, and example descriptions.

(Content: Overview of signac filesystem-based parameter tracking, when to use vs GNU Parallel, progression to Maestro, 3 example descriptions, links to documentation)

**Verification:**
Run: `grep "filesystem-based state tracking" 01-signac/README.md`
Expected: Shows concept description

**Commit:** Batch commit (Task 7)
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create Example 1 - Parameter Space Definition

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4

**Files:**
- Create: `01-signac/example1-parameter-space/README.md`
- Create: `01-signac/example1-parameter-space/init_project.py`
- Create: `01-signac/example1-parameter-space/explore_workspace.py`

**Implementation:**

Demonstrate 2D parameter space (temperature × pressure) with automatic directory organization.

**init_project.py** - Initialize signac project with parameter combinations:
```python
import signac

project = signac.init_project("signac-demo")

# Define 2D parameter space: temperature × pressure
temps = [300, 400, 500]
pressures = [1.0, 10.0, 100.0]

for temp in temps:
    for pressure in pressures:
        # signac automatically creates unique directory for each combination
        job = project.open_job({"temperature": temp, "pressure": pressure})
        job.init()

print(f"Initialized {len(project)} jobs")
print("Workspace structure created in workspace/")
```

**explore_workspace.py** - Show auto-generated directory structure:
```python
import signac

project = signac.get_project()

print(f"Project contains {len(project)} jobs:")
for job in project:
    print(f"Job {job.id[:8]}: temp={job.sp.temperature}, pressure={job.sp.pressure}")
    print(f"  -> Directory: {job.workspace()}")
```

**README.md** - Explains signac state point concept, unique hash-based directories, how this improves on GNU Parallel's manual parameter tracking.

**Verification:**
Run: `cd 01-signac/example1-parameter-space && python init_project.py`
Expected: Creates `workspace/` with 9 subdirectories (3×3 combinations)

**Commit:** Batch commit (Task 7)
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create Example 2 - Slurm Job Submission

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4

**Files:**
- Create: `01-signac/example2-job-submission/README.md`
- Create: `01-signac/example2-job-submission/project.py`
- Create: `01-signac/example2-job-submission/simulate.py`

**Implementation:**

Demonstrate signac-flow integration generating Slurm submit scripts.

**project.py** - signac-flow FlowProject with Slurm template:
```python
from flow import FlowProject
import signac

class SimulationProject(FlowProject):
    pass

@SimulationProject.label
def simulated(job):
    return job.isfile("results.txt")

@SimulationProject.operation
@SimulationProject.directives(
    np=1,
    walltime=0.5,
    executable="python simulate.py"
)
def run_simulation(job):
    # Simulation runs in job directory with parameters from job.sp
    pass

if __name__ == '__main__':
    SimulationProject().main()
```

**simulate.py** - Placeholder simulation script reading job parameters.

**README.md** - Explains signac-flow template generation, how `flow submit` creates Slurm scripts automatically, one script per state point.

**Verification:**
Run: `cd 01-signac/example2-job-submission && python project.py submit --pretend`
Expected: Shows Slurm commands that would be submitted

**Commit:** Batch commit (Task 7)
<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Create Example 3 - Result Aggregation

**Verifies:** wf-seminar.AC4.1, wf-seminar.AC4.3, wf-seminar.AC4.4

**Files:**
- Create: `01-signac/example3-aggregation/README.md`
- Create: `01-signac/example3-aggregation/analyze_results.py`
- Create: `01-signac/example3-aggregation/generate_fake_data.py`

**Implementation:**

Demonstrate querying jobs and aggregating results across parameter space.

**analyze_results.py** - Query completed jobs and aggregate:
```python
import signac
import numpy as np

project = signac.get_project()

# Query jobs by parameter
high_temp_jobs = project.find_jobs({"temperature": {"$gte": 400}})

# Aggregate results
results = []
for job in high_temp_jobs:
    if job.isfile("results.txt"):
        with open(job.fn("results.txt")) as f:
            value = float(f.read())
            results.append((job.sp.temperature, job.sp.pressure, value))

# Analysis
print(f"Analyzed {len(results)} completed high-temperature jobs")
mean_value = np.mean([r[2] for r in results])
print(f"Mean result: {mean_value:.2f}")
```

**generate_fake_data.py** - Populate job results for demonstration.

**README.md** - Explains signac query syntax, how to filter by parameters, aggregating across state points.

**Verification:**
Run: `cd 01-signac/example3-aggregation && python generate_fake_data.py && python analyze_results.py`
Expected: Shows aggregation across parameter space

**Commit:** Batch commit (Task 7)
<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Verify Phase 3 examples

**Verifies:** wf-seminar.AC4.4

**Implementation:**

```bash
cd 01-signac/example1-parameter-space
python init_project.py
python explore_workspace.py
ls -d workspace/*

cd ../example2-job-submission
python project.py submit --pretend

cd ../example3-aggregation
python generate_fake_data.py
python analyze_results.py
```

Expected: All examples execute without errors
<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Commit Phase 3 files

**Verifies:** None (infrastructure)

**Implementation:**

```bash
git add 01-signac/README.md
git add 01-signac/example1-parameter-space/
git add 01-signac/example2-job-submission/
git add 01-signac/example3-aggregation/

git commit -m "feat: add signac section with parameter space organization examples

Create 3 signac examples demonstrating parameter organization:
- example1-parameter-space: 2D parameter space with automatic directory organization
- example2-job-submission: signac-flow Slurm integration
- example3-aggregation: Query and aggregate results across state points

Supports AC4.1, AC4.3, AC4.4.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
<!-- END_TASK_6 -->

---

## Phase 3 Complete

**Next Phase:** Phase 4 will create Maestro DAG workflow examples.
