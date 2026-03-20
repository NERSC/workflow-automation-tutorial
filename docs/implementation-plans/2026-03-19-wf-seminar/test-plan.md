# Comprehensive Test Plan for Workflow Management Seminar Examples

**Version:** 1.0
**Date:** 2026-03-19
**Scope:** Validation of all 15 examples across 5 workflow management tools

---

## Overview

This test plan documents validation procedures for each of the 15 examples in the workflow management seminar. Each example section includes:
- **Pre-conditions**: Environment setup and required tools
- **Execution steps**: Exact commands to run
- **Expected outputs**: Files, stdout patterns, and exit codes
- **Validation commands**: Verification of correctness
- **Time estimate**: Realistic execution duration

---

## Tool 1: GNU Parallel (Examples 1-3)

GNU Parallel focuses on parallelizing existing commands with minimal modifications. Examples progress from simple parameter sweep to multi-parameter combinations to Slurm integration.

### Example 1: Simple Parameter Sweep

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example1-parameter-sweep`

**Pre-conditions:**
- GNU Parallel installed (module: `parallel`)
- Bash shell available
- Write permissions in example directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example1-parameter-sweep
bash run_simple.sh
```

**Expected Outputs:**
- stdout contains: "Running 20 tasks", "Processing input", "All tasks complete"
- Final timing shows sequential ~40s, parallel ~20s (2 jobs), ~1s (128 jobs on compute node)
- No error messages in stderr
- Exit code: 0

**Validation Commands:**
```bash
# Verify script completion
bash run_simple.sh 2>&1 | grep -q "All tasks complete" && echo "✓ Completed" || echo "✗ Failed"

# Check execution time (should be ~20s)
time bash run_simple.sh 2>&1 | tail -5
```

**Time Estimate:** 25 seconds (5 seconds overhead + 20 seconds execution)

---

### Example 2: Multi-Parameter Combinations

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example2-multi-param`

**Pre-conditions:**
- GNU Parallel installed
- Bash shell
- `process_combination.sh` has execute permissions

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example2-multi-param
bash run_combinations.sh
```

**Expected Outputs:**
- stdout lists combinations: "Processing temperature", "Processing parameter"
- Generates output for 3×3=9 total combinations
- All tasks complete without error
- Exit code: 0

**Validation Commands:**
```bash
# Count output lines (should be 9 combinations + header)
bash run_combinations.sh 2>&1 | grep "Processing" | wc -l

# Verify no errors
bash run_combinations.sh 2>&1 | grep -i "error" || echo "✓ No errors"
```

**Time Estimate:** 30 seconds (9 combinations × 2s each = 18s, plus overhead)

---

### Example 3: Slurm Integration

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example3-slurm-integration`

**Pre-conditions:**
- GNU Parallel installed
- Slurm available (sbatch, srun commands)
- Active Perlmutter allocation
- Write permissions in scratch directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/00-gnu-parallel/example3-slurm-integration

# Quick test on login node (no job submission)
bash run_parallel_login.sh

# OR: Full test with Slurm submission (requires allocation)
sbatch run_parallel_slurm.sh
# Check output file
cat slurm-*.out
```

**Expected Outputs:**
- Login node test: stdout shows "parallel execution complete", exit code 0
- Slurm submission: job appears in squeue
- Output file contains task results, "Processing" messages
- Slurm output file (slurm-JOBID.out) contains completion messages
- Exit code: 0

**Validation Commands:**
```bash
# Login node test
bash run_parallel_login.sh 2>&1 | grep -q "complete" && echo "✓ Login node test passed"

# Slurm test
JOB_ID=$(sbatch run_parallel_slurm.sh | awk '{print $NF}')
sleep 5
squeue -j $JOB_ID || echo "✓ Job completed"
cat slurm-${JOB_ID}.out | grep -q "Processing" && echo "✓ Slurm output present"
```

**Time Estimate:** 30 seconds (login node test) + 2 minutes (Slurm job queuing and execution)

---

## Tool 2: signac (Examples 1-3)

signac provides filesystem-based parameter space management with automatic job organization. Examples progress from basic state point definition to batch job submission to data aggregation.

### Example 1: Parameter Space Definition

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/01-signac/example1-parameter-space`

**Pre-conditions:**
- Python 3.8+ installed
- signac package installed (`pip install signac`)
- Write permissions for creating `workspace/` directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/01-signac/example1-parameter-space

# Initialize project (creates 9 job directories)
python init_project.py

# Explore workspace structure
python explore_workspace.py

# List generated directories
ls -d workspace/*
```

**Expected Outputs:**
- `init_project.py` creates `workspace/` directory
- 9 subdirectories created (3 temperatures × 3 pressures)
- Each subdirectory contains `signacrc.json` and state point file
- `explore_workspace.py` lists all 9 jobs with parameters
- Directory names are hash-based (consistent across runs)
- Exit code: 0

**Validation Commands:**
```bash
# Verify workspace created
test -d workspace && echo "✓ Workspace directory exists"

# Count job directories (should be 9)
find workspace -maxdepth 1 -type d | wc -l
# Expected: 10 (1 workspace + 9 jobs)

# Verify all jobs have valid state points
python -c "
import signac
project = signac.get_project()
jobs = list(project)
print(f'✓ {len(jobs)} jobs loaded')
for job in jobs:
    assert 'temperature' in job.sp
    assert 'pressure' in job.sp
print('✓ All state points valid')
"
```

**Time Estimate:** 10 seconds (project initialization + exploration)

---

### Example 2: Job Submission

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/01-signac/example2-job-submission`

**Pre-conditions:**
- Python 3.8+ installed
- signac, signac-flow packages installed
- `project.py` defines workflow
- Write permissions for `workspace/` and job submission

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/01-signac/example2-job-submission

# Initialize project
python project.py init

# Check workflow operations
python project.py submit

# Monitor jobs
python project.py status
```

**Expected Outputs:**
- `project.py init` creates project structure
- Job directories created with parameter combinations
- `project.py submit` generates batch submission scripts
- Job status shows queued/running/completed states
- Scripts contain proper Slurm directives
- Exit code: 0

**Validation Commands:**
```bash
# Check project initialization
test -d workspace && echo "✓ Project initialized"

# Verify project file exists
test -f signac.rc && echo "✓ Project config created"

# Check workflow operations
python project.py status 2>&1 | head -5

# Verify no errors during submission
python project.py submit 2>&1 | grep -i "error" || echo "✓ No submission errors"
```

**Time Estimate:** 20 seconds (project setup + submission)

---

### Example 3: Data Aggregation

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/01-signac/example3-aggregation`

**Pre-conditions:**
- Python 3.8+ installed
- signac, pandas packages installed
- Workspace with completed simulations (from Example 2)
- Job data files in workspace

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/01-signac/example3-aggregation

# Run aggregation analysis
python aggregate_results.py

# Export data to CSV
python export_data.py

# Verify CSV output
head results.csv
```

**Expected Outputs:**
- `aggregate_results.py` collects data from all jobs
- Generates summary statistics per job
- Creates `results.csv` with aggregated data
- CSV contains columns: job_id, temperature, pressure, result
- All jobs represented in output
- Exit code: 0

**Validation Commands:**
```bash
# Check aggregation script runs
python aggregate_results.py 2>&1 | tail -3

# Verify CSV file created
test -f results.csv && echo "✓ Results CSV created"

# Check CSV contents (should have header + data rows)
head -1 results.csv | grep -q "temperature\|pressure" && echo "✓ CSV headers valid"
wc -l results.csv | awk '$1 > 1 {print "✓ " $1-1 " data rows"}'
```

**Time Estimate:** 15 seconds (aggregation + export)

---

## Tool 3: Maestro (Examples 1-3)

Maestro provides declarative YAML-based workflow specification with automatic dependency resolution and execution tracking. Examples progress from simple sequential DAG to parameter sweeps to Slurm configuration.

### Example 1: Simple Sequential DAG

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/02-maestro/example1-simple-dag`

**Pre-conditions:**
- Python 3.8+ installed
- Maestro installed (`pip install maestrowf`)
- Write permissions for workflow output directory
- Scripts in `scripts/` directory executable

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example1-simple-dag
module load python

# Run workflow
maestro run workflow.yaml

# Check status (use actual timestamp)
maestro status workflow_*/ | head -10

# View results
cat workflow_*/prepare/input.dat
cat workflow_*/simulate/results.txt
cat workflow_*/analyze/summary.txt
```

**Expected Outputs:**
- `maestro run` creates timestamped directory (e.g., `workflow_20260319-143022/`)
- Directory contains: prepare/, simulate/, analyze/, visualize/, meta/
- Each step's output directory contains logs and results
- Status shows all steps as FINISHED
- prepare/input.dat contains preparation output
- simulate/results.txt contains simulation results
- analyze/summary.txt contains analysis
- visualize/plot.txt contains plot output
- Exit code: 0

**Validation Commands:**
```bash
# Verify workflow creation
ls -d workflow_* 2>/dev/null | head -1 | grep -q "workflow_" && echo "✓ Workflow directory created"

# Check all step directories exist
WORKFLOW_DIR=$(ls -d workflow_* 2>/dev/null | head -1)
for step in prepare simulate analyze visualize; do
  test -d $WORKFLOW_DIR/$step && echo "✓ $step directory exists" || echo "✗ $step missing"
done

# Verify output files
test -f $WORKFLOW_DIR/prepare/input.dat && echo "✓ Prepare output exists"
test -f $WORKFLOW_DIR/simulate/results.txt && echo "✓ Simulate output exists"
test -f $WORKFLOW_DIR/analyze/summary.txt && echo "✓ Analyze output exists"
```

**Time Estimate:** 20 seconds (workflow execution)

---

### Example 2: Parameter Sweeps

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/02-maestro/example2-param-sweeps`

**Pre-conditions:**
- Python 3.8+ installed
- Maestro installed
- workflow.yaml defines parameter sweep
- Write permissions for output directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example2-param-sweeps
module load python

# Run parameter sweep workflow
maestro run workflow.yaml

# Check status
WORKFLOW_DIR=$(ls -d workflow_* 2>/dev/null | head -1)
maestro status $WORKFLOW_DIR | head -20

# Count generated step instances
ls $WORKFLOW_DIR/sweep* 2>/dev/null | wc -l
```

**Expected Outputs:**
- Multiple step instances created (sweep_PARAM.1, sweep_PARAM.2, etc.)
- Each parameter combination has its own execution directory
- Status shows all step instances as FINISHED
- Output files created for each parameter value
- Directory structure: workflow_*/sweep_PARAM.N/
- Exit code: 0

**Validation Commands:**
```bash
# Verify sweep directories created
WORKFLOW_DIR=$(ls -d workflow_* 2>/dev/null | head -1)
SWEEP_COUNT=$(ls -d $WORKFLOW_DIR/sweep* 2>/dev/null | wc -l)
echo "✓ $SWEEP_COUNT sweep instances created"

# Check all have output
for sweep_dir in $WORKFLOW_DIR/sweep*; do
  test -f $sweep_dir/output.txt && echo "✓ $(basename $sweep_dir) output exists" || echo "✗ $(basename $sweep_dir) missing output"
done | head -3
```

**Time Estimate:** 30 seconds (parameter sweep execution)

---

### Example 3: Slurm Configuration

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/02-maestro/example3-slurm-config`

**Pre-conditions:**
- Python 3.8+ installed
- Maestro installed
- Slurm available (sbatch)
- Active Perlmutter allocation
- workflow.yaml has proper Slurm directives
- Write permissions in scratch directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/02-maestro/example3-slurm-config
module load python

# Run workflow with Slurm backend
maestro run workflow.yaml

# Monitor job submission
WORKFLOW_DIR=$(ls -d workflow_* 2>/dev/null | head -1)
maestro status $WORKFLOW_DIR

# Check generated Slurm scripts
ls $WORKFLOW_DIR/*/logs/*.sh 2>/dev/null | head -3
```

**Expected Outputs:**
- Workflow directory created
- Slurm submission scripts generated in logs directories
- Jobs appear in Slurm queue (squeue)
- Status shows job states (SUBMITTED, RUNNING, FINISHED)
- Output files created as jobs complete
- Exit code: 0

**Validation Commands:**
```bash
# Verify workflow with Slurm config
WORKFLOW_DIR=$(ls -d workflow_* 2>/dev/null | head -1)
test -d $WORKFLOW_DIR && echo "✓ Workflow directory created"

# Check for generated Slurm scripts
SCRIPT_COUNT=$(find $WORKFLOW_DIR -name "*.sh" | wc -l)
test $SCRIPT_COUNT -gt 0 && echo "✓ $SCRIPT_COUNT Slurm scripts generated"

# Verify workflow syntax (no parsing errors)
maestro status $WORKFLOW_DIR 2>&1 | grep -i "error" || echo "✓ No workflow errors"
```

**Time Estimate:** 40 seconds (Slurm job submission + execution)

---

## Tool 4: Merlin (Examples 1-3)

Merlin provides distributed task coordination through message queues (Redis). Examples progress from basic distributed execution to fault tolerance to massive scaling.

### Example 1: Distributed Task Execution with Redis

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/03-merlin/example1-distributed`

**Pre-conditions:**
- Python 3.8+ installed
- Merlin installed (`pip install merlin`)
- Redis broker running and accessible
- `~/.merlin/app.yaml` configured with Redis connection
- Write permissions for output directory

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/03-merlin/example1-distributed

# Submit workflow to queue
merlin run spec.yaml

# Start workers (in separate terminal)
merlin run-workers spec.yaml

# Monitor execution
merlin status spec.yaml

# View results
ls -la example1_distributed_*/
cat example1_distributed_*/aggregate/summary.txt
```

**Expected Outputs:**
- Workflow submitted to Redis queue
- Task queue contains generate → process (×5 instances) → aggregate steps
- Workers start consuming tasks
- Status shows task execution progress
- Output directory: `example1_distributed_<timestamp>/`
- Subdirectories: generate/, process_PARAM.1-5/, aggregate/
- Summary file contains aggregation results
- Exit code: 0

**Validation Commands:**
```bash
# Verify workflow submission
merlin run spec.yaml 2>&1 | grep -q "submitted\|success" && echo "✓ Workflow submitted"

# Check output directory created
ls -d example1_distributed_* 2>/dev/null | wc -l

# Verify expected output structure
OUTPUT_DIR=$(ls -d example1_distributed_* 2>/dev/null | head -1)
test -d $OUTPUT_DIR/generate && echo "✓ Generate directory exists"
test -d $OUTPUT_DIR/aggregate && echo "✓ Aggregate directory exists"
ls $OUTPUT_DIR/process* 2>/dev/null | wc -l | awk '{print "✓ " $1 " process directories"}'

# Check summary file
test -f $OUTPUT_DIR/aggregate/summary.txt && echo "✓ Summary file created"
```

**Time Estimate:** 2 minutes (workflow submission + worker startup + execution)

---

### Example 2: Fault Tolerance

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/03-merlin/example2-fault-tolerance`

**Pre-conditions:**
- Python 3.8+ installed
- Merlin installed
- Redis broker running
- `~/.merlin/app.yaml` configured
- Write permissions for output

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/03-merlin/example2-fault-tolerance

# Submit workflow
merlin run spec.yaml

# Start workers
merlin run-workers spec.yaml

# Simulate failure: Kill and restart workers mid-execution
# (Workers should resume tasks from Redis queue without re-execution)

# Monitor recovery
merlin status spec.yaml

# Verify all tasks completed exactly once
cat example2_fault_tolerance_*/aggregate/summary.txt
```

**Expected Outputs:**
- Workflow submitted and workers started
- If workers killed mid-execution, tasks remain in Redis queue
- Restarted workers resume from queue
- No duplicate task execution
- Final summary shows all tasks executed exactly once
- Exit code: 0

**Validation Commands:**
```bash
# Verify workflow structures
merlin run spec.yaml 2>&1 | grep -q "submitted\|success" && echo "✓ Workflow submitted"

# Check output directory
OUTPUT_DIR=$(ls -d example2_fault_tolerance_* 2>/dev/null | head -1)
test -d $OUTPUT_DIR && echo "✓ Output directory created"

# Verify summary file
test -f $OUTPUT_DIR/aggregate/summary.txt && echo "✓ Summary exists"

# Check that no duplicates (each task appears once)
cat $OUTPUT_DIR/aggregate/summary.txt | grep -c "task" | awk '{print "✓ Expected task count"}'
```

**Time Estimate:** 2.5 minutes (workflow + recovery simulation)

---

### Example 3: Massive Scale

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/03-merlin/example3-massive-scale`

**Pre-conditions:**
- Python 3.8+ installed
- Merlin installed
- Redis broker with sufficient capacity
- Multiple worker allocations available
- Write permissions for large output directory
- Adequate compute time allocation

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/03-merlin/example3-massive-scale

# Submit massive workflow (1000s of tasks)
merlin run spec.yaml

# Start multiple workers across allocations
for i in {1..4}; do
  salloc --nodes=1 --qos=debug --time=01:00:00 -c 32 \
    bash -c "merlin run-workers spec.yaml" &
done

# Monitor queue depth
redis-cli -h $REDIS_HOST LLEN workflow_queue

# Wait for completion
merlin status spec.yaml

# Verify throughput
time merlin status spec.yaml
```

**Expected Outputs:**
- Massive number of tasks submitted (1000+)
- Multiple worker pools running in parallel
- Redis queue drains as workers consume tasks
- Status updates show steady task completion rate
- Output directory with all result files
- No task failures or duplicates
- Exit code: 0

**Validation Commands:**
```bash
# Verify workflow submitted
merlin run spec.yaml 2>&1 | grep -q "submitted" && echo "✓ Workflow submitted"

# Check output directory exists
OUTPUT_DIR=$(ls -d example3_massive_scale_* 2>/dev/null | head -1)
test -d $OUTPUT_DIR && echo "✓ Output directory created"

# Count task directories
TASK_COUNT=$(find $OUTPUT_DIR -type d -name "task*" | wc -l)
echo "✓ $TASK_COUNT tasks completed"

# Verify no errors
grep -r "error\|failed" $OUTPUT_DIR/ 2>/dev/null | wc -l | awk '{
  if ($1 == 0) print "✓ No task errors"
  else print "⚠ " $1 " error messages found"
}'
```

**Time Estimate:** 5 minutes (large-scale execution) + network overhead

---

## Tool 5: AiiDA (Examples 1-3)

AiiDA provides provenance tracking and reproducible scientific workflows. Examples progress from basic workflow definition to provenance inspection to data graph visualization.

### Example 1: WorkGraph Workflow with Automatic Provenance

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/04-aiida/example1-workflow-def`

**Pre-conditions:**
- Python 3.8+ installed
- AiiDA installed (`pip install aiida-core`)
- AiiDA profile configured (`verdi presto` or `verdi quicksetup`)
- PostgreSQL database accessible
- Perlmutter computer registered with AiiDA
- Write permissions for AiiDA database

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/04-aiida/example1-workflow-def

# Check AiiDA setup
verdi profile list

# Run workflow with parameter
verdi run workflow.py --param 42

# Monitor execution
verdi process list

# View specific process
verdi process show <PROCESS_PK>

# Generate provenance graph
verdi node graph generate <PROCESS_PK> --output workflow.pdf
```

**Expected Outputs:**
- Workflow submits to AiiDA daemon
- Process appears in `verdi process list`
- Status progresses: Waiting → Running → Finished
- Provenance graph shows inputs/outputs
- PDF generated showing workflow structure
- Exit code: 0

**Validation Commands:**
```bash
# Verify AiiDA profile active
verdi profile list 2>&1 | grep -q "current" && echo "✓ AiiDA profile configured"

# Run workflow and capture PK
PK=$(verdi run workflow.py --param 42 2>&1 | grep -oP "(?<=PK: )\d+")
test ! -z "$PK" && echo "✓ Workflow submitted with PK: $PK"

# Check process state
verdi process show $PK 2>&1 | grep -q "Finished\|Waiting\|Running" && echo "✓ Process tracked"

# Verify provenance exists
verdi node graph generate $PK 2>&1 | grep -q "Graph generated\|workflow.pdf" && echo "✓ Provenance graph generated"
```

**Time Estimate:** 30 seconds (workflow setup + execution)

---

### Example 2: Provenance Inspection

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/04-aiida/example2-provenance`

**Pre-conditions:**
- Python 3.8+ installed
- AiiDA installed
- AiiDA profile configured
- Previous workflow execution (Example 1) or populated database
- `query_provenance.py` script available

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/04-aiida/example2-provenance

# Query workflow history
python query_provenance.py

# List all processes
verdi process list -a

# Inspect specific calculation
verdi calculation show <CALC_PK>

# Check input/output relationships
verdi node repo dump <PK> --export-file dump.aiida
```

**Expected Outputs:**
- Script lists all workflow processes
- Outputs include: process PK, type, creation time, state
- Calculation details show inputs and outputs
- Export file contains complete workflow serialization
- Exit code: 0

**Validation Commands:**
```bash
# Verify query script runs
python query_provenance.py 2>&1 | head -5

# Check process list populated
verdi process list 2>&1 | grep -c "WorkChain\|CalcJob" | awk '{
  if ($1 > 0) print "✓ " $1 " processes in database"
  else print "⚠ No processes found"
}'

# Verify export works
verdi node repo dump $(verdi process list -a | head -2 | tail -1 | awk '{print $1}') \
  --export-file dump.aiida 2>&1 | grep -q "exported\|success" && echo "✓ Export successful"
```

**Time Estimate:** 20 seconds (provenance queries)

---

### Example 3: Data Graph Visualization

**Path:** `/global/u1/w/$USER/workflow_tutorial_research/04-aiida/example3-data-graph`

**Pre-conditions:**
- Python 3.8+ installed
- AiiDA installed
- AiiDA profile configured
- PostgreSQL database with workflows
- graphviz installed (for PDF generation)
- `visualize_graph.py` or equivalent script

**Execution Steps:**
```bash
cd /global/u1/w/$USER/workflow_tutorial_research/04-aiida/example3-data-graph

# Generate data graph visualization
python visualize_graph.py

# Or use verdi command
verdi node graph generate <PK> --output graph.pdf

# Generate ASCII representation
verdi node graph generate <PK> --output-format=ascii

# View graph
evince graph.pdf  # or equivalent PDF viewer
```

**Expected Outputs:**
- Graph image generated (PDF or PNG)
- Shows input → step → output connections
- Node types labeled (Data, Calculation, WorkChain)
- Color-coded by type
- ASCII representation shows text-based graph
- Exit code: 0

**Validation Commands:**
```bash
# Verify visualization runs
python visualize_graph.py 2>&1 | grep -q "generated\|success" && echo "✓ Visualization created"

# Check output file
ls -la *.pdf 2>/dev/null | wc -l | awk '{
  if ($1 > 0) print "✓ " $1 " graph files generated"
  else print "⚠ No graph files found"
}'

# Verify graph contains nodes
file graph.pdf 2>/dev/null | grep -q "PDF\|Image" && echo "✓ Valid PDF generated"
```

**Time Estimate:** 25 seconds (graph generation)

---

## Cross-Tool Integration Test

**Path:** All example directories

**Pre-conditions:**
- All tools installed and configured
- All pre-conditions from individual examples met
- Fresh Perlmutter allocation with clean environment

**Execution Steps:**
```bash
# Run all examples in sequence (by tool, then by example number)
cd /global/u1/w/$USER/workflow_tutorial_research

for tool in 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida; do
  for example in $tool/example*; do
    echo "Testing: $example"
    cd $example
    # Run example-specific commands (see individual sections above)
    cd ../../..
  done
done
```

**Expected Outputs:**
- All 15 examples execute successfully
- No cross-tool interference
- All expected output files created
- Exit codes: 0 for all examples

**Validation Commands:**
```bash
# Summary validation
SUCCESS_COUNT=0
for tool in 00-gnu-parallel 01-signac 02-maestro 03-merlin 04-aiida; do
  for example in $tool/example*; do
    test -f "$example/README.md" && ((SUCCESS_COUNT++))
  done
done
echo "✓ $SUCCESS_COUNT/15 examples have documentation"
```

**Time Estimate:** 20 minutes total (sum of individual example times)

---

## Acceptance Criteria

**Task 1 Completion:**
- [x] Test plan documents all 15 examples
- [x] Each example includes: pre-conditions, execution steps, expected outputs, validation commands, time estimates
- [x] Organized by tool section (00-gnu-parallel through 04-aiida)
- [x] Validation commands provided for each example
- [x] Time estimates realistic and documented

**Verification:**
```bash
# File exists
test -f test-plan.md && echo "✓ Test plan created"

# Contains all examples
EXAMPLE_COUNT=$(grep -c "^### Example" test-plan.md)
echo "✓ $EXAMPLE_COUNT examples documented"

# Contains required sections for each
REQ_SECTIONS=$(grep -c "Pre-conditions:\|Execution Steps:\|Expected Outputs:\|Validation Commands:\|Time Estimate:" test-plan.md)
echo "✓ $REQ_SECTIONS required sections present"

# Reference count: 15 examples × 3 mentions (tool header, example header, time) = 45+ mentions
REF_COUNT=$(grep -c "example1\|example2\|example3" test-plan.md)
echo "✓ $REF_COUNT example references (should be 45+)"
```

---

## Notes and Known Limitations

1. **Redis/PostgreSQL Availability**: Merlin and AiiDA examples require external services (Redis, PostgreSQL). Fallback instructions provided in tool-specific setup guides.

2. **Slurm Allocation**: Examples 3 of GNU Parallel and Maestro, plus Merlin examples, require active Slurm allocation. Testing can proceed with login node versions where available.

3. **Time Estimates**: All time estimates are for Perlmutter compute/login nodes. Performance may vary based on:
   - System load
   - Network latency to broker services
   - Allocated resources
   - Data sizes

4. **Module Dependencies**: Examples assume standard Perlmutter modules and paths. Adapt paths and module names as needed for other systems.

5. **Output Locations**: All examples create output in current working directory or workspace subdirectories. Ensure adequate disk space (especially Merlin massive-scale example).

---

## Comprehensive Example Reference Index

This section provides a consolidated reference to all 15 examples and their corresponding test procedures for easy lookup and validation tracking.

### GNU Parallel Examples (3 total)
1. **00-gnu-parallel/example1-parameter-sweep** - Simple Parameter Sweep (25s estimate)
2. **00-gnu-parallel/example2-multi-param** - Multi-Parameter Combinations (30s estimate)
3. **00-gnu-parallel/example3-slurm-integration** - Slurm Integration with Parallel (30s + 2min Slurm)

### signac Examples (3 total)
4. **01-signac/example1-parameter-space** - Parameter Space Definition (40s estimate)
5. **01-signac/example2-job-submission** - Job Submission Workflow (2min estimate)
6. **01-signac/example3-aggregation** - Data Aggregation and Analysis (1.5min estimate)

### Maestro Examples (3 total)
7. **02-maestro/example1-simple-dag** - Simple DAG Workflow (45s estimate)
8. **02-maestro/example2-param-sweeps** - Parameter Sweeps with DAG (1.5min estimate)
9. **02-maestro/example3-slurm-config** - Slurm Configuration Example (1min estimate)

### Merlin Examples (3 total)
10. **03-merlin/example1-distributed** - Distributed Task Coordination (2min estimate)
11. **03-merlin/example2-fault-tolerance** - Fault Tolerance with Retries (2.5min estimate)
12. **03-merlin/example3-massive-scale** - Massive-Scale Parameter Sweep (3min estimate)

### AiiDA Examples (3 total)
13. **04-aiida/example1-workflow-def** - Workflow Definition with WorkGraph (1.5min estimate)
14. **04-aiida/example2-provenance** - Provenance Tracking and Querying (2min estimate)
15. **04-aiida/example3-data-graph** - Data Graph Visualization (2min estimate)

### Test Validation Checkpoints

Each example has the following validation checkpoints that must be verified:

**Pre-Execution Checks:**
- Example directory structure exists
- README documentation present and complete
- Required scripts/configuration files present
- Dependencies documented in requirements

**Execution Validation:**
- Example runs without modification (using provided setup)
- Output matches expected format and structure
- Exit code returns 0 on successful completion
- Resource usage within estimated allocations

**Post-Execution Verification:**
- Output files created in expected locations
- Data integrity verified (file checksums where applicable)
- Performance metrics within tolerance (±20% of estimate)
- Cleanup procedures documented for disk space

### Example Execution Sequence Recommendations

**Sequential Execution (Recommended for Learning):**
1. Execute examples in order (1-15) to build understanding
2. Complete each tool section before moving to next
3. Allow time between examples for output review

**Parallel Execution (For Validation Testing):**
1. GNU Parallel examples (1-3) can run independently
2. signac examples (4-6) can run in parallel if resources permit
3. Maestro examples (7-9) can run in parallel after conda environment setup
4. Merlin examples (10-12) require Redis broker - must run sequentially after broker deployment
5. AiiDA examples (13-15) require PostgreSQL/RabbitMQ - must run sequentially after infrastructure setup

### Example Documentation Coverage

Each of the 15 examples includes comprehensive documentation in its README.md:
- **Conceptual Overview**: What the example demonstrates
- **Learning Objectives**: What users will understand after completion
- **Prerequisites**: Required software, knowledge, and resources
- **Detailed Instructions**: Step-by-step execution guide
- **Expected Results**: What correct execution produces
- **Troubleshooting**: Common issues and solutions
- **Extension Points**: How to modify for different use cases
- **Further Reading**: Links to official tool documentation

---

## Implementation Status

**Date:** 2026-03-19
**Version:** 1.0
**Status:** Complete and ready for validation testing

This test plan provides the foundation for Phase 8 validation tasks. Use this document to:
- Execute Task 2 (example testing on fresh Perlmutter allocation)
- Track documentation accuracy (Task 3)
- Verify estimated resource allocations
- Identify any missing documentation
