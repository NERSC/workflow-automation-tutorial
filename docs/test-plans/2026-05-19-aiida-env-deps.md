# Human Test Plan: AiiDA Environment Dependencies

## Prerequisites

- Perlmutter login node or compute node allocation
- Conda environment `wf-seminar` rebuilt from the updated `environment.yml`:
  ```
  conda env create -f environment.yml
  ```
  or incrementally:
  ```
  conda env update -f environment.yml --prune
  ```
- All five textual checks pass (fast precondition):
  ```
  grep -c 'module load graphviz' 04-aiida/example3-data-graph/README.md  # expect 0
  grep -c 'wf-seminar' 04-aiida/example3-data-graph/README.md            # expect >= 1
  grep -c 'conda install graphviz -c conda-forge' 04-aiida/example3-data-graph/README.md  # expect 1
  grep -c 'node-graph==0.0.12' 04-aiida/CLAUDE.md                         # expect 1
  grep -c 'NodeSocket' 04-aiida/CLAUDE.md && grep -c 'TaskSocket' 04-aiida/CLAUDE.md  # both >= 1
  ```

## Phase 1: Operational Dependency Verification

| Step | Action | Expected |
|------|--------|----------|
| 1.1 | Activate the environment: `conda activate wf-seminar` | Shell prompt changes to `(wf-seminar)` |
| 1.2 | Run: `python -c "from aiida_workgraph import task, WorkGraph; print('OK')"` | Prints `OK` and exits with code 0. No ImportError or AttributeError. |
| 1.3 | Run: `pip show node-graph` and check the `Version:` line | Output includes `Version: 0.0.12` (exactly). |
| 1.4 | Run: `python -c "from aiida_workgraph import task; assert callable(task.calcfunction); assert callable(task.graph_builder); print('OK')"` | Prints `OK`. Confirms the decorators are accessible (no `AttributeError` from the `NodeSocket`/`TaskSocket` rename). |
| 1.5 | Run: `dot -V` | Prints `dot - graphviz version X.Y.Z ...` and exits with code 0. |

## Phase 2: End-to-End AiiDA Workflow with Graph Generation

**Purpose:** Validate that the graphviz binary, node-graph pin, and AiiDA stack work together in a realistic tutorial scenario, from profile creation through provenance visualization.

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Run: `verdi presto` (if no profile exists yet; skip if profile already configured) | AiiDA creates a SQLite-backed profile. Output confirms profile creation. |
| 2.2 | Run: `verdi profile list` | At least one profile is listed and marked as default. |
| 2.3 | Run: `cd 04-aiida/example1-workflow-def && python workflow.py` | Workflow executes successfully. Output shows workflow steps completing and a final result. No import errors. |
| 2.4 | Run: `verdi process list -a` | Lists at least one completed process. Note the PK of a workflow node. |
| 2.5 | Run: `verdi node graph generate <PK>` (using the PK from step 2.4) | Prints `Success: Output written to <PK>.dot.pdf`. The file `<PK>.dot.pdf` exists and has nonzero size. |
| 2.6 | Verify the PDF: `ls -la <PK>.dot.pdf` | File exists, size is greater than 0 bytes. |
| 2.7 | Clean up: `cd 04-aiida && bash cleanup.sh` | Removes `*.dot.pdf`, `*.dot.png`, `*.aiida`, `__pycache__/` artifacts. |

## Human Verification Required

| Criterion | Why Manual | Steps |
|-----------|------------|-------|
| AC1.4: A fresh pip install of `aiida-workgraph==0.3.16` without the pin resolves `node-graph>=0.1.0` and fails to import | Depends on current PyPI resolution state. Documents *why* the pin is necessary, not a regression gate. Result may change if upstream fixes their dependency spec. | 1. Create a throwaway virtualenv: `python -m venv /tmp/test-no-pin && source /tmp/test-no-pin/bin/activate`. 2. Install without pin: `pip install aiida-workgraph==0.3.16`. 3. Check resolved version: `pip show node-graph` -- expect `Version:` shows `>= 0.1.0`. 4. Attempt import: `python -c "from aiida_workgraph import task"` -- expect `ImportError` or `AttributeError` referencing `NodeSocket`. 5. Clean up: `deactivate && rm -rf /tmp/test-no-pin`. If this test *passes* without error, it means upstream has fixed the issue and the pin may eventually be removed. |
| AC2.2: `verdi node graph generate <PK>` produces a `.dot.pdf` file without error | Requires a live AiiDA profile with completed calcfunction nodes. PK is dynamic and determined by prior example execution. Full integration test spanning profile setup, workflow execution, and graphviz rendering. | Covered by Phase 2 steps 2.1 through 2.6 above. The key verification is that `verdi node graph generate <PK>` succeeds (step 2.5) and the output file exists with nonzero size (step 2.6). |

## Traceability

| Acceptance Criterion | Automated Test | Manual Step |
|----------------------|----------------|-------------|
| AC1.1: aiida_workgraph import succeeds | Operational (conda env rebuild) | Phase 1, Step 1.2 |
| AC1.2: node-graph version is 0.0.12 | Operational (conda env rebuild) | Phase 1, Step 1.3 |
| AC1.3: task decorators are callable | Operational (conda env rebuild) | Phase 1, Step 1.4 |
| AC1.4: Unpin demonstrates failure | N/A (human only) | Human Verification: AC1.4 |
| AC2.1: dot -V exits 0 | Operational (conda env rebuild) | Phase 1, Step 1.5 |
| AC2.2: verdi node graph generate produces PDF | N/A (human only) | Phase 2, Steps 2.1-2.6 |
| AC3.1: No `module load graphviz` in README | Textual grep: returns 0 | Prereq check |
| AC3.2: README mentions wf-seminar | Textual grep: returns >= 1 | Prereq check |
| AC3.3: README has conda install fallback | Textual grep: returns 1 | Prereq check |
| AC4.1: CLAUDE.md has `node-graph==0.0.12` | Textual grep: returns 1 | Prereq check |
| AC4.2: CLAUDE.md has NodeSocket and TaskSocket | Textual grep: both >= 1 | Prereq check |
